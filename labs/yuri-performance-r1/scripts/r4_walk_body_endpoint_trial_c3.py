"""ONE left-leg discrete endpoint derivative repair; C2 root/stance fixed."""
import bpy,sys,json,hashlib,ast,time
from pathlib import Path
import numpy as np
from mathutils import Quaternion,Vector
from mathutils.bvhtree import BVHTree
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_walk_root_endpoint_adapter_c2 import WalkRootEndpointLane,ACTIONS as C2A
from r4_walk_body_endpoint_adapter_c3 import WalkBodyEndpointLane,ACTIONS
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');W=B/'alpha-walk-root-contact-c1';C2=B/'alpha-walk-root-endpoint-c2b';O=B/'alpha-walk-body-endpoint-c3';O.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();m=json.loads((C2/'WALK_ROOT_ENDPOINT_PRIVATE_C2.json').read_bytes());P=Path(m['source']);C=Path(m['candidate']);assert sha(P)==m['source_SHA'] and sha(C)==m['candidate_SHA'];start=time.perf_counter()
bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);source_names=list(bpy.data.actions.keys());source_sig=snapshot(source_names)
bpy.ops.wm.open_mainfile(filepath=str(C),use_scripts=False);s=bpy.context.scene;names=list(bpy.data.actions.keys());before=snapshot(names);assert len(names)==87 and snapshot(source_names)==source_sig
module=ast.parse((H/'r4_existing_reach_contact_closure_r1.py').read_text(encoding='utf8'));exec(compile(ast.Module(body=[x for x in module.body if isinstance(x,ast.FunctionDef) and x.name=='geom'],type_ignores=[]),'<pinned_actual_mesh>','exec'));fixed={}
mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4'];rig=bpy.data.objects['Meshy_Fitted_Rig'];carrier=bpy.data.objects['Assembly_Root'];body=bpy.data.objects[mesh_names[0]];fps=24
cache=np.load(W/'SOURCE_AND_CANDIDATE_SOLE_TRAJECTORIES_PRIVATE_C1.npz');ids={q:cache[q+'_vertex_ids'] for q in ['L','R']};floor=json.loads((B/'alpha-native-walk-source-r1/NATIVE_WALK_SOURCE_PRIVATE_R1.json').read_bytes())['source_floor_plane_world_z_m'];masks={q:[set(np.where(v[:,2]-floor<=.003)[0].tolist()) for v in cache[q+'_source']] for q in ids}
def curves(a):return [f for l in a.layers for st in l.strips for bag in st.channelbags for f in bag.fcurves]
def keys(a):return [(f.data_path,f.array_index,[(list(k.co),k.interpolation) for k in f.keyframe_points]) for f in curves(a)]
new={}
for ob,old in C2A.items():
 a=bpy.data.actions[old].copy();a.name=ACTIONS[ob];a.use_fake_user=True;new[ob]=a
selected=['thigh.L','shin.L','foot.L'];changes=[];N=4;k=lambda i:i*(1-i/N)**2
for bn in selected:
 path='pose.bones["'+bn+'"].rotation_quaternion';fs=sorted([f for f in curves(new['Meshy_Fitted_Rig']) if f.data_path==path],key=lambda f:f.array_index);assert len(fs)==4
 vals=np.array([[f.evaluate(t) for f in fs] for t in range(1,98)]);first=vals[1]-vals[0];last=vals[-1]-vals[-2];target=(first+last)/2;out=vals.copy()
 for i in range(1,N):out[i]+=(target-first)*k(i)/k(1);out[96-i]-=(target-last)*k(i)/k(1)
 # Quaternion normalization after vector-space compact tangent correction; actual mesh QA determines residual.
 changed=[1,2,3,93,94,95]
 for i in changed:out[i]/=np.linalg.norm(out[i]);out[i]*=1 if np.dot(out[i],vals[i])>=0 else -1
 for fc in fs:
  for kp in fc.keyframe_points:
   idx=int(round(kp.co.x))-1
   if idx in changed:kp.co.y=float(out[idx,fc.array_index]);kp.interpolation='LINEAR'
 changes.append({'bone':bn,'path':path,'components':[0,1,2,3],'changed_source_frames':[i+1 for i in changed],'max_quaternion_angle_delta_degrees':max(float(Quaternion(vals[i]).rotation_difference(Quaternion(out[i])).angle*180/np.pi) for i in changed),'before_derivative_quaternion_vector_mismatch_per_second':float(np.linalg.norm((last-first)*fps)),'after_derivative_quaternion_vector_mismatch_per_second':float(np.linalg.norm(((out[-1]-out[-2])-(out[1]-out[0]))*fps))})
for ob in ['Armature','Hair_Rig_R4','Assembly_Root']:assert keys(new[ob])==keys(bpy.data.actions[C2A[ob]])
unchanged_paths=[f for f in curves(new['Meshy_Fitted_Rig']) if not any('"'+bn+'"' in f.data_path for bn in selected)];oldcurves={(f.data_path,f.array_index):f for f in curves(bpy.data.actions[C2A['Meshy_Fitted_Rig']])}
assert all([(list(k.co),k.interpolation) for k in f.keyframe_points]==[(list(k.co),k.interpolation) for k in oldcurves[(f.data_path,f.array_index)].keyframe_points] for f in unchanged_paths)
# Actual C2 control plus C3 all193 frames. Control images reuse already completed native C2 corpus.
control={};poses={};roots={};triangles=None
ln=WalkRootEndpointLane();ln.on()
for f in range(1,194):
 s.frame_set(f);bpy.context.view_layer.update();gg={n:geom(bpy.data.objects[n]) for n in mesh_names};control[f]={n:x[0] for n,x in gg.items()};poses[f]={b.name:np.array(b.matrix_basis) for b in rig.pose.bones};roots[f]=np.array(carrier.matrix_world)[:3,3]
 if triangles is None:triangles={n:x[1] for n,x in gg.items()}
ln.off();assert snapshot(names)==before
# Any actual shifted BODY vertex + weak left-leg cohort supplies affected triangles; all target triangles tested.
groupids={body.vertex_groups[n].index for n in ['thigh.L','shin.L','foot.L','toe.L'] if n in body.vertex_groups};cohort={v.index for v in body.data.vertices if any(g.group in groupids and g.weight>.01 for g in v.groups)}
def contact(g,affected):
 v=g[mesh_names[0]];t=triangles[mesh_names[0]];aid=[i for i,x in enumerate(t) if any(j in affected for j in x)];alltree=BVHTree.FromPolygons(v.tolist(),t,all_triangles=True,epsilon=0);atree=BVHTree.FromPolygons(v.tolist(),[t[i] for i in aid],all_triangles=True,epsilon=0);non=set()
 for i,j in atree.overlap(alltree):
  x=t[aid[i]];y=t[j]
  if not set(x)&set(y):non.add(tuple(sorted([tuple(sorted(x)),tuple(sorted(y))])))
 out={'affected_vs_body_nonadjacent':non}
 for n in mesh_names[1:]:
  tr=BVHTree.FromPolygons(g[n].tolist(),triangles[n],all_triangles=True,epsilon=0);out['all_body_vs_'+n]={(tuple(sorted(t[i])),tuple(sorted(triangles[n][j]))) for i,j in alltree.overlap(tr)}
 return out
ln=WalkBodyEndpointLane();ln.on();rows=[];feet={q:[] for q in ids};actualroot=[];seam={};contactrows=[];phase_contact_cache={}
for f in range(1,194):
 s.frame_set(f);bpy.context.view_layer.update();g={n:geom(bpy.data.objects[n])[0] for n in mesh_names};phase=(f-1)%96+1;delta={n:float(np.linalg.norm(g[n]-control[f][n],axis=1).max()) for n in mesh_names};pd={b.name:float(np.abs(np.array(b.matrix_basis)-poses[f][b.name]).max()) for b in rig.pose.bones};rr=np.array(carrier.matrix_world)[:3,3];assert np.array_equal(rr,roots[f]);actualroot.append(rr);rows.append({'frame':f,'phase':phase,'finite':all(np.isfinite(x).all() for x in g.values()),'geometry_delta_vs_C2_m':delta,'changed_pose_bones':{n:v for n,v in pd.items() if v>1e-8},'root_exact_C2':True})
 for q in ids:feet[q].append(g[mesh_names[0]][ids[q]])
 if f in [1,2,96,97,98,192,193]:seam[f]=g
 if phase in [1,2,3,4,94,95,96] and phase not in phase_contact_cache:
  affected=cohort|set(np.where(np.linalg.norm(g[mesh_names[0]]-control[f][mesh_names[0]],axis=1)>1e-9)[0]);cp=contact(control[f],affected);npairs=contact(g,affected);row={'phase_frame':phase,'actual_global_frame':f,'affected_vertices':len(affected),'counts_C2':{k:len(v) for k,v in cp.items()},'counts_C3':{k:len(v) for k,v in npairs.items()},'new_pair_identities_vs_C2':{k:len(v-cp[k]) for k,v in npairs.items()},'removed_pair_identities_vs_C2':{k:len(cp[k]-v) for k,v in npairs.items()}};contactrows.append(row);phase_contact_cache[phase]=row;print('C3_CONTACT',row,flush=True)
ln.off();assert snapshot(names)==before
seams={role:{n:float(np.linalg.norm(((gg[97][n]-gg[96][n])-(gg[98][n]-gg[97][n]))*fps,axis=1).max()) for n in mesh_names} for role,gg in [('C2',control),('C3',seam)]};foot_summary={}
for role in ['C2','C3']:
 foot_summary[role]={}
 for q in ids:
  vv=np.array([control[f][mesh_names[0]][ids[q]] for f in range(1,194)]) if role=='C2' else np.array(feet[q]);mask=[masks[q][i%96] for i in range(193)];intervals=[];i=0;step=0
  while i<193:
   if not mask[i]:i+=1;continue
   j=i
   while j+1<193 and mask[j+1]:j+=1
   common=sorted(set.intersection(*mask[i:j+1]));intervals.append({'frames':[i+1,j+1],'common_vertices':len(common),'anchored_XY_excursion_m':float(np.linalg.norm(vv[i:j+1,common,:2]-vv[i,common,:2],axis=2).max()) if common else None});i=j+1
  for i in range(1,193):
   common=sorted(mask[i-1]&mask[i])
   if common:step=max(step,float(np.linalg.norm(vv[i,common,:2]-vv[i-1,common,:2],axis=1).max()))
  foot_summary[role][q]={'intervals':intervals,'max_anchored_XY_excursion_m':max(x['anchored_XY_excursion_m'] for x in intervals if x['anchored_XY_excursion_m'] is not None),'max_persistent_XY_step_m':step,'min_gap_m':float((vv[:,:,2]-floor).min()),'frozen_C1_source_mask':True}
assert all(x['geometry_delta_vs_C2_m'][n]<1e-6 for x in rows for n in mesh_names[1:]);assert max(x['geometry_delta_vs_C2_m'][mesh_names[0]] for x in rows if x['phase'] not in [2,3,4,94,95,96])<1e-7
candidate=O/'Character_R4_WalkBodyEndpoint_EXPERIMENT_OFF_C3_20261005.blend';bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=False);assert snapshot(names)==before;lib=O/'YURI_R4_WALK_BODY_ENDPOINT_ACTIONS_ONLY_C3.blend';bpy.data.libraries.write(str(lib),set(new.values()),fake_user=True)
with bpy.data.libraries.load(str(lib),link=False) as (src,dst):assert len(src.actions)==4 and not src.objects and not src.meshes and not src.armatures
cs=sha(candidate);bpy.ops.wm.open_mainfile(filepath=str(candidate),use_scripts=False);s=bpy.context.scene;assert snapshot(names)==before and snapshot(source_names)==source_sig
meta={'task':'ROOT_PM_WALK_C2_CLOSE_TO_BODY_ENDPOINT_C3_R1','source':str(P),'source_SHA':m['source_SHA'],'C2_candidate':str(C),'C2_candidate_SHA':m['candidate_SHA'],'original87_signature_private':before,'source78_C2prior87_fresh_serialized_OFF_equal':True,'candidate':str(candidate),'candidate_SHA':cs,'library':{'file':str(lib),'sha256':sha(lib),'actions':4,'objects':0,'meshes':0,'armatures':0},'actions':ACTIONS,'method':'ONE compact discrete quaternion endpoint tangent repair, left thigh/shin/foot four components each; normalized quaternions, first/last3 samples only, N4 cubic bump. No root or right-leg or pelvis repair, parameter sweep, full-source replacement.','changes':changes,'rows_private':rows,'seam_max_actual_mesh_velocity_mismatch_m_per_s':seams,'feet':foot_summary,'contact_regression':contactrows,'contact_scope':'All actual BODY triangles versus head/hair; affected BODY triangles (actual moved vertices union weakANY left-leg weights>.01) versus ALL BODY triangles, nonadjacent identities. Seven unique changed/boundary phase samples; other frames actual full geometry unchanged, phase repetition and uniform root translation preserve pair identities. Existing source contact HOLD remains. No forces/COM/containment certificate.','root_path_all193_exact_C2':True,'loop_delta_world_m':m['loop_delta_world_m'],'fps':24,'unique_video_frames':192,'actual_eval_frames':193,'TierP':0,'Unity_F2_StageB_promotion':False,'elapsed_before_render_seconds':time.perf_counter()-start}
np.savez_compressed(O/'ACTUAL_C2_C3_SOLE_ROOT_PRIVATE_C3.npz',root=np.array(actualroot),L_C3=np.array(feet['L']),R_C3=np.array(feet['R']))
(O/'WALK_BODY_ENDPOINT_PRIVATE_C3.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
# Exact approved C2 camera metadata reused; all C2 images reused unchanged offline, only C3 actual new captures.
cam=s.camera;savecam=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width);saves=[]
for ob,k,v in [(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',2),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',320),(s.render,'resolution_y',320),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','JPEG'),(s.render.image_settings,'color_mode','RGB'),(s.render.image_settings,'color_depth','8'),(s.render.image_settings,'quality',92),(s.render,'filepath','')]:saves.append((ob,k,getattr(ob,k)));setattr(ob,k,v)
ln=WalkBodyEndpointLane();ln.on()
for view,cv in m['views'].items():
 folder=O/'C3_two_cycles_native'/view;folder.mkdir(parents=True);cam.data.type='ORTHO';cam.data.ortho_scale=cv['ortho_scale'];cam.location=cv['location'];cam.rotation_euler=cv['rotation_euler']
 for f in range(1,193):s.frame_set(f);bpy.context.view_layer.update();s.render.filepath=str(folder/f'{f:04}.jpg');bpy.ops.render.render(write_still=True)
ln.off();cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width=savecam;s.render.resolution_x=960;s.render.resolution_y=920;s.cycles.samples=8;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(O/'BODY_ENDPOINT_OFF_SOURCE_NEUTRAL_C3.png');bpy.ops.render.render(write_still=True)
for ob,k,v in saves:setattr(ob,k,v)
assert snapshot(names)==before and snapshot(source_names)==source_sig and sha(P)==m['source_SHA'] and sha(C)==m['candidate_SHA'] and sha(candidate)==cs;meta['views']=m['views'];meta['actual_two_cycle_capture_complete']=True;meta['fullraw_OFF_after_render_equal']=True;meta['elapsed_seconds']=time.perf_counter()-start;(O/'WALK_BODY_ENDPOINT_PRIVATE_C3.json').write_text(json.dumps(meta,indent=2),encoding='utf8');print('C3_ONE_CANDIDATE_COMPLETE',seams,foot_summary,flush=True)
