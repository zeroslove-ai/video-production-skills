"""One discrete endpoint velocity repair, accumulated two cycles, immutable C1 prerequisite."""
import bpy,sys,json,hashlib,ast,time
from pathlib import Path
import numpy as np
from mathutils import Matrix,Vector
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_walk_root_contact_adapter_c1 import ACTIONS as C1A
from r4_walk_root_endpoint_adapter_c2 import WalkRootEndpointLane,ACTIONS
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');W=B/'alpha-walk-root-contact-c1';O=B/'alpha-walk-root-endpoint-c2';O.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();m=json.loads((W/'WALK_ROOT_CONTACT_PRIVATE_C1.json').read_bytes());P=Path(m['source']);C=Path(m['candidate']);assert sha(P)==m['source_SHA'] and sha(C)==m['candidate_SHA'];start=time.perf_counter()
bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);source_names=list(bpy.data.actions.keys());source_sig=snapshot(source_names)
bpy.ops.wm.open_mainfile(filepath=str(C),use_scripts=False);s=bpy.context.scene;names=list(bpy.data.actions.keys());before=snapshot(names);assert len(names)==83 and snapshot(source_names)==source_sig # Fresh serialized C1 OFF prerequisite.
module=ast.parse((H/'r4_existing_reach_contact_closure_r1.py').read_text(encoding='utf8'));exec(compile(ast.Module(body=[x for x in module.body if isinstance(x,ast.FunctionDef) and x.name=='geom'],type_ignores=[]),'<pinned_actual_mesh>','exec'));fixed={}
mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4'];rig=bpy.data.objects['Meshy_Fitted_Rig'];carrier=bpy.data.objects['Assembly_Root'];face=bpy.data.objects['Armature'];cache=np.load(W/'SOURCE_AND_CANDIDATE_SOLE_TRAJECTORIES_PRIVATE_C1.npz');root1=cache['root_world_offset'];fps=24;v1=np.diff(root1,axis=0)*fps;target=(v1[0]+v1[-1])/2;correction=np.zeros_like(root1);N=8;k=lambda i:i*(1-i/N)**2
for i in range(1,N):correction[i]=(target-v1[0])/fps*k(i)/k(1);correction[96-i]=-(target-v1[-1])/fps*k(i)/k(1)
root2=root1+correction;v2=np.diff(root2,axis=0)*fps;assert np.linalg.norm(v2[-1]-v2[0])<1e-12 and np.array_equal(root2[[0,96]],root1[[0,96]]) and np.all(correction[:,2]==0)
def curves(a):return [f for l in a.layers for st in l.strips for bag in st.channelbags for f in bag.fcurves]
def keys(a):return [(f.data_path,f.array_index,[(list(k.co),k.interpolation) for k in f.keyframe_points]) for f in curves(a)]
control={};new={}
for ob,oldname in C1A.items():
 a=bpy.data.actions[oldname].copy();a.name='QA_C1_ACCUMULATED_CONTROL_'+ob;control[ob]=a.name
 c=bpy.data.actions[oldname].copy();c.name=ACTIONS[ob];c.use_fake_user=True;new[ob]=c
 for ac in [a,c]:
  for fc in curves(ac):
   assert len(fc.modifiers)==0
   mod=fc.modifiers.new('CYCLES');mode='REPEAT_OFFSET' if ob=='Assembly_Root' or (ob=='Armature' and fc.data_path.endswith('.location')) else 'REPEAT';mod.mode_before=mode;mod.mode_after=mode
# Preserve all source pose keys; change ONLY two translated object/face location streams near endpoints.
rootlinear=(carrier.parent.matrix_world if carrier.parent else Matrix.Identity(4)).inverted().to_3x3();facelinear=face.pose.bones['Root'].bone.matrix_local.to_3x3().inverted()@face.matrix_world.inverted().to_3x3()
for ob,linear,path in [('Assembly_Root',rootlinear,'location'),('Armature',facelinear,'pose.bones["Root"].location')]:
 for fc in curves(new[ob]):
  if fc.data_path==path:
   for kp in fc.keyframe_points:
    i=int(round(kp.co.x))-1;kp.co.y+=float((linear@Vector(correction[i]))[fc.array_index]);kp.interpolation='LINEAR'
assert keys(new['Meshy_Fitted_Rig'])==keys(bpy.data.actions[C1A['Meshy_Fitted_Rig']]) and keys(new['Hair_Rig_R4'])==keys(bpy.data.actions[C1A['Hair_Rig_R4']])
body=bpy.data.objects[mesh_names[0]];ids={q:cache[q+'_vertex_ids'] for q in ['L','R']};floor=json.loads((B/'alpha-native-walk-source-r1/NATIVE_WALK_SOURCE_PRIVATE_R1.json').read_bytes())['source_floor_plane_world_z_m'];sourcefoot={q:cache[q+'_source'] for q in ids};masks={q:[set(np.where(v[:,2]-floor<=.003)[0].tolist()) for v in vv] for q,vv in sourcefoot.items()}
# C1 two-cycle motion is new consumer control, no source corpus/Walk head analysis or baseline render rerun.
ln=WalkRootEndpointLane(control);ln.on();controlgeom=[];controlpose=[];controlroot=[]
for f in range(1,194):
 s.frame_set(f);bpy.context.view_layer.update();controlgeom.append({n:geom(bpy.data.objects[n])[0] for n in mesh_names});controlpose.append({b.name:np.array(b.matrix_basis) for b in rig.pose.bones});controlroot.append(np.array(carrier.matrix_world)[:3,3])
ln.off();assert snapshot(names)==before
ln=WalkRootEndpointLane();ln.on();rows=[];foot2={q:[] for q in ids};rootactual=[];seamgeom={}
for f in range(1,194):
 s.frame_set(f);bpy.context.view_layer.update();phase=(f-1)%96;cyc=(f-1)//96;g={n:geom(bpy.data.objects[n])[0] for n in mesh_names};res={n:float(np.abs(g[n]-(controlgeom[f-1][n]+correction[phase])).max()) for n in mesh_names};pose=max(float(np.abs(np.array(b.matrix_basis)-controlpose[f-1][b.name]).max()) for b in rig.pose.bones);rootactual.append(np.array(carrier.matrix_world)[:3,3]);rows.append({'frame':f,'source_phase_frame':phase+1,'cycle_index':cyc,'pose_matrix_error_vs_C1':pose,'world_translation_residual_vs_C1_plus_endpoint_correction_m':res,'expected_accumulated_root_m':(root2[phase]+cyc*root2[-1]).tolist(),'root_world_translation_vs_first_m':(rootactual[-1]-rootactual[0]).tolist(),'finite':all(np.isfinite(g[n]).all() for n in mesh_names)})
 for q in ids:foot2[q].append(g[mesh_names[0]][ids[q]])
 if f in [1,2,96,97,98,192,193]:seamgeom[f]=g
ln.off();assert snapshot(names)==before
seams={}
for role,gg in [('C1',controlgeom),('C2',[seamgeom.get(f) for f in range(1,194)])]:
 seams[role]={n:{'cycle_boundary97_velocity_delta_max_m_per_s':float(np.linalg.norm(((gg[96][n]-gg[95][n])-(gg[97][n]-gg[96][n]))*fps,axis=1).max()),'cycle_endpoint193_vs_start1_translation_normalized_error_m':float(np.abs((gg[192][n]-2*root1[-1])-gg[0][n]).max())} for n in mesh_names}
# Translation cannot remove heterogeneous native BODY derivative differences: pair separation bound.
d=((seamgeom[97][mesh_names[0]]-seamgeom[96][mesh_names[0]])-(seamgeom[98][mesh_names[0]]-seamgeom[97][mesh_names[0]]))*fps;lower_bound=float(np.ptp(d,axis=0).max()/2)
foot_summary={}
for role in ['C1','C2']:
 foot_summary[role]={}
 for q in ids:
  vv=np.array([x[mesh_names[0]][ids[q]] for x in controlgeom]) if role=='C1' else np.array(foot2[q]);intervals=[];mask=[masks[q][i%96] for i in range(193)];i=0;maxstep=0
  while i<193:
   if not mask[i]:i+=1;continue
   j=i
   while j+1<193 and mask[j+1]:j+=1
   common=sorted(set.intersection(*mask[i:j+1]));travel=float(np.linalg.norm(vv[i:j+1,common,:2]-vv[i,common,:2],axis=2).max()) if common else None;intervals.append({'frames':[i+1,j+1],'common_vertices':len(common),'anchored_XY_excursion_m':travel});i=j+1
  for i in range(1,193):
   common=sorted(mask[i-1]&mask[i])
   if common:maxstep=max(maxstep,float(np.linalg.norm(vv[i,common,:2]-vv[i-1,common,:2],axis=1).max()))
  foot_summary[role][q]={'intervals':intervals,'max_anchored_XY_excursion_m':max(x['anchored_XY_excursion_m'] for x in intervals if x['anchored_XY_excursion_m'] is not None),'max_persistent_XY_step_m':maxstep,'min_gap_m':float((vv[:,:,2]-floor).min()),'two_cycle_source_mask_reused':True}
rootactual=np.array(rootactual);controlroot=np.array(controlroot);speed={}
for role,r in [('C1',controlroot),('C2',rootactual)]:
 v=np.diff(r,axis=0)*fps;speed[role]={'boundary_velocity_delta_m_per_s':float(np.linalg.norm(v[95]-v[96])),'speed_m_per_s_min_max':[float(np.linalg.norm(v,axis=1).min()),float(np.linalg.norm(v,axis=1).max())],'max_acceleration_m_per_s2':float(np.linalg.norm(np.diff(v,axis=0)*fps,axis=1).max()),'frame1_97_193_accumulated_world_m':[(r[i]-r[0]).tolist() for i in [0,96,192]]}
# Only C2 is a saved candidate; remove newly created consumer-control wrappers after unbinding.
for n in control.values():bpy.data.actions.remove(bpy.data.actions[n])
assert snapshot(names)==before;candidate=O/'Character_R4_WalkRootEndpoint_EXPERIMENT_OFF_C2_20261005.blend';bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=False);assert snapshot(names)==before
lib=O/'YURI_R4_WALK_ROOT_ENDPOINT_ACTIONS_ONLY_C2.blend';bpy.data.libraries.write(str(lib),set(new.values()),fake_user=True)
with bpy.data.libraries.load(str(lib),link=False) as (src,dst):assert len(src.actions)==4 and not src.objects and not src.meshes and not src.armatures
# Fresh C2 serialized OFF gate in this same job; no external source sweep.
cs=sha(candidate);bpy.ops.wm.open_mainfile(filepath=str(candidate),use_scripts=False);s=bpy.context.scene;assert snapshot(names)==before and snapshot(source_names)==source_sig
meta={'task':'ROOT_PM_WALK_C1_TO_ENDPOINT_VELOCITY_C2_R1','source':str(P),'source_SHA':m['source_SHA'],'C1_candidate_SHA':m['candidate_SHA'],'C1_fresh_serialized_OFF_source78_equal':True,'C1_original83_signature':before,'candidate':str(candidate),'candidate_SHA':cs,'library':{'file':str(lib),'sha256':sha(lib),'actions':4,'objects':0,'meshes':0,'armatures':0},'actions':ACTIONS,'one_method':'Endpoint equal average discrete root step using cubic compact bump i(1-i/8)^2 only first/last8 frames; fixed endpoint positions,rootZ0, max correction0.643241mm; no parameter sweep.','first_last_root_step_target_m_per_s':target.tolist(),'max_correction_m':float(np.linalg.norm(correction,axis=1).max()),'loop_delta_world_m':root2[-1].tolist(),'native_fps':24,'two_cycles_unique_frames':192,'sampled_with_terminal_endpoint_frames':193,'actual_rows_private':rows,'seam':seams,'root_speed':speed,'feet':foot_summary,'body_derivative_uniform_translation_unavoidable_max_residual_lower_bound_m_per_s':lower_bound,'original_BODY_HAIR_all_key_values_and_interpolation_exact':True,'source78_C1prior83_fullraw_OFF_unchanged':True,'C2_fresh_serialized_OFF_source78_C1prior83_equal':True,'Cycles_scope':'Carrier+head location REPEAT_OFFSET;body/hair/quaternion REPEAT. Only C2 copies contain new Cycles modifiers. Actual global1..193 evaluated, no root reset.','head_contact_force_COM_Unity_TierP_F2_HOLD':True,'TierP':0}
np.savez_compressed(O/'ROOT_ENDPOINT_AND_BODY_SEAM_PRIVATE_C2.npz',C1_world_root=root1,C2_world_root=root2,correction=correction,body_velocity_difference_field=d)
(O/'WALK_ROOT_ENDPOINT_PRIVATE_C2.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
# Wider FIXED two-cycle view; cached C1 cycle1 will be orthographically reframed offline, never rerendered.
cam=s.camera;savecam=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width);saves=[]
for ob,k,v in [(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',2),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',320),(s.render,'resolution_y',320),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','JPEG'),(s.render.image_settings,'color_mode','RGB'),(s.render.image_settings,'color_depth','8'),(s.render.image_settings,'quality',92),(s.render,'filepath','')]:saves.append((ob,k,getattr(ob,k)));setattr(ob,k,v)
views={}
# Recreate unsaved C1 loop controls from immutable original83, only for cycle2 new needed footage.
control={}
for ob,oldname in C1A.items():
 a=bpy.data.actions[oldname].copy();a.name='QA_C1_ACCUMULATED_RENDER_'+ob;control[ob]=a.name
 for fc in curves(a):
  mod=fc.modifiers.new('CYCLES');mode='REPEAT_OFFSET' if ob=='Assembly_Root' or (ob=='Armature' and fc.data_path.endswith('.location')) else 'REPEAT';mod.mode_before=mode;mod.mode_after=mode
for role,mapping,fr in [('C1_cycle2_native',control,range(97,193)),('C2_two_cycles_native',ACTIONS,range(1,193))]:
 ln=WalkRootEndpointLane(mapping);ln.on()
 for view,oldview in m['views'].items():
  folder=O/role/view;folder.mkdir(parents=True);oldtarget=Vector(oldview['target']);target=oldtarget+Vector(root1[-1]);direction=(Vector(oldview['location'])-oldtarget).normalized();cam.data.type='ORTHO';cam.data.ortho_scale=1.55;cam.location=target+direction*.8;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();right=cam.rotation_euler.to_matrix()@Vector((1,0,0));up=cam.rotation_euler.to_matrix()@Vector((0,1,0));views[view]={'type':'ORTHO','ortho_scale':1.55,'target':list(target),'location':list(cam.location),'rotation_euler':list(cam.rotation_euler),'resolution':[320,320],'fixed':True,'original_cached_camera':oldview,'cached_to_new_pixel_scale':oldview['ortho_scale']/1.55,'cached_to_new_center_shift_xy_pixels':[float((oldtarget-target).dot(right)*320/1.55),float(-(oldtarget-target).dot(up)*320/1.55)],'C1_cycle1':'Reuse cached native C1frames1..96 via calibrated orthographic affine reframe; resampling disclosed. C1cycle2 and C2all192 are actual new renders.'}
  for f in fr:s.frame_set(f);bpy.context.view_layer.update();s.render.filepath=str(folder/f'{f:04}.jpg');bpy.ops.render.render(write_still=True)
 ln.off()
for n in control.values():bpy.data.actions.remove(bpy.data.actions[n])
cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width=savecam;s.render.resolution_x=960;s.render.resolution_y=920;s.cycles.samples=8;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(O/'ROOT_ENDPOINT_OFF_SOURCE_NEUTRAL_C2.png');bpy.ops.render.render(write_still=True)
for ob,k,v in saves:setattr(ob,k,v)
assert snapshot(names)==before and snapshot(source_names)==source_sig and sha(C)==m['candidate_SHA'] and sha(P)==m['source_SHA'] and sha(candidate)==cs;meta['views']=views;meta['actual_two_cycle_capture_complete']=True;meta['fullraw_OFF_after_two_cycle_render_equal']=True;meta['elapsed_seconds']=time.perf_counter()-start;(O/'WALK_ROOT_ENDPOINT_PRIVATE_C2.json').write_text(json.dumps(meta,indent=2),encoding='utf8');print('C2_ENDPOINT_ONE_TRIAL_COMPLETE',seams,speed,foot_summary,flush=True)
