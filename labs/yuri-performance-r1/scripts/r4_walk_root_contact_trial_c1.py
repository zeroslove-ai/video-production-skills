"""Single source-foot-derived XY root trial, no pose/ankle/knee locks or precision sweep."""
import bpy,sys,json,hashlib,ast,time
from pathlib import Path
import numpy as np
from mathutils import Vector,Matrix
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_native_walk_adapter_r1 import NativeWalkLane
from r4_walk_root_contact_adapter_c1 import WalkRootContactLane,ACTIONS
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');W=B/'alpha-native-walk-source-r1';O=B/'alpha-walk-root-contact-c1';O.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();m=json.loads((W/'NATIVE_WALK_SOURCE_PRIVATE_R1.json').read_bytes());P=Path(m['source']);C=Path(m['candidate']);assert sha(P)==m['source_SHA'] and sha(C)==m['candidate_SHA'];start=time.perf_counter()
bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);source_names=list(bpy.data.actions.keys());source_sig=snapshot(source_names)
bpy.ops.wm.open_mainfile(filepath=str(C),use_scripts=False);s=bpy.context.scene;names=list(bpy.data.actions.keys());before=snapshot(names);assert len(names)==81 and snapshot(source_names)==source_sig
module=ast.parse((H/'r4_existing_reach_contact_closure_r1.py').read_text(encoding='utf8'));exec(compile(ast.Module(body=[x for x in module.body if isinstance(x,ast.FunctionDef) and x.name=='geom'],type_ignores=[]),'<pinned_actual_mesh>','exec'));fixed={}
mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4'];body=bpy.data.objects[mesh_names[0]];rig=bpy.data.objects['Meshy_Fitted_Rig'];carrier=bpy.data.objects['Assembly_Root'];face=bpy.data.objects['Armature'];hair=bpy.data.objects['Hair_Rig_R4'];assert rig.parent==carrier and body.parent==carrier and hair.parent==carrier and face.parent is None
groupnames={g.index:g.name for g in body.vertex_groups};ids={side:np.array([v.index for v in body.data.vertices if sum(g.weight for g in v.groups if groupnames[g.group] in ['foot.'+side,'toe.'+side])>.5],int) for side in ['L','R']};floor=m['source_floor_plane_world_z_m'];neutral={n:geom(bpy.data.objects[n])[0] for n in mesh_names};fps=24
old=NativeWalkLane();old.on();foot={q:[] for q in ids};geometry=[];localposes=[];facebasis=[];faceobject=[]
for f in range(1,98):
 s.frame_set(f);bpy.context.view_layer.update();g={n:geom(bpy.data.objects[n])[0] for n in mesh_names};geometry.append(g)
 for q in ids:foot[q].append(g[mesh_names[0]][ids[q]].copy())
 localposes.append({b.name:np.array(b.matrix_basis) for b in rig.pose.bones});facebasis.append(face.pose.bones['Root'].location.copy());faceobject.append(face.matrix_world.copy())
old.off();assert snapshot(names)==before
foot={q:np.array(v) for q,v in foot.items()};contacts={q:[set(np.where(v[:,2]-floor<=.003)[0].tolist()) for v in vs] for q,vs in foot.items()};steps=[];offset=np.zeros((97,3));double=[]
for i in range(1,97):
 per={}
 for q in ids:
  common=sorted(contacts[q][i-1]&contacts[q][i])
  if common:per[q]={'xy_step':np.median(foot[q][i,common,:2]-foot[q][i-1,common,:2],axis=0),'vertices':len(common)}
 assert per,'No persistent near-floor sole at '+str(i+1)
 # One equal-foot compromise in double support; never pin two incompatible feet or solve ankles.
 step=-np.mean([x['xy_step'] for x in per.values()],axis=0);offset[i]=offset[i-1];offset[i,:2]+=step
 conflict=float(np.linalg.norm(per['L']['xy_step']-per['R']['xy_step'])) if len(per)==2 else None
 if conflict is not None:double.append({'frames':[i,i+1],'incompatible_sole_velocity_difference_m_per_s':conflict*fps,'best_equal_foot_residual_lower_bound_m_per_s':conflict*fps/2,'simultaneous_3mm_proximity_is_not_force_support':True})
 steps.append({'frame':i+1,'near_floor_feet':list(per),'persistent_vertices':{q:x['vertices'] for q,x in per.items()},'root_xy_step_m':step.tolist(),'double_support_velocity_conflict_m_per_s':conflict*fps if conflict is not None else None})
root=bpy.data.actions.new(ACTIONS['Assembly_Root']);root.slots.new(id_type='OBJECT',name=carrier.name);root.use_fake_user=True;root['scope']='C1: integrate negative median actual near-floor persistent sole XY step; equal-foot double support compromise. Z0, no pose or contact-force solver.';root['source_fps']=24
head=bpy.data.actions['YURI_R4_NATIVE_WALK_HEAD_TRANSPORT_R1'].copy();head.name=ACTIONS['Armature'];head.use_fake_user=True;head['scope']='Original existing head Root action plus world XY locomotion translation only; original driver/basis/rotation preserved.'
def curves(a):return [f for l in a.layers for st in l.strips for bag in st.channelbags for f in bag.fcurves]
headcurves={(c.data_path,c.array_index):c for c in curves(head)};rootloc=carrier.location.copy();parentworld=carrier.parent.matrix_world if carrier.parent else Matrix.Identity(4);world_to_local=parentworld.inverted().to_3x3();rootrest=face.pose.bones['Root'].bone.matrix_local.to_3x3().inverted()
# Author ONLY carrier translation and existing unparented face root translation on separate Actions.
had_root_ad=carrier.animation_data is not None;ad=carrier.animation_data_create();savead=(ad.action,ad.action_slot,ad.action_slot_handle,ad.last_slot_identifier);ad.action=root;ad.action_slot=root.slots[0]
for i in range(97):
 carrier.location=rootloc+world_to_local@Vector(offset[i]);carrier.keyframe_insert('location',frame=i+1,group='SOURCE_SOLE_XY_ROOT_C1')
 localdelta=rootrest@faceobject[i].inverted().to_3x3()@Vector(offset[i]);value=facebasis[i]+localdelta
 for j in range(3):
  fc=headcurves[('pose.bones["Root"].location',j)]
  kp=next(k for k in fc.keyframe_points if abs(k.co.x-(i+1))<1e-6);kp.co.y=value[j]
for ac in [root,head]:
 for fc in curves(ac):
  for k in fc.keyframe_points:k.interpolation='LINEAR'
ad.action=savead[0]
if savead[0] and savead[1]:ad.action_slot=savead[1]
ad.action_slot_handle=savead[2];ad.last_slot_identifier=savead[3];carrier.location=rootloc
if not had_root_ad:carrier.animation_data_clear()
bpy.context.view_layer.update();assert snapshot(names)==before
lane=WalkRootContactLane();lane.on();actualfoot={q:[] for q in ids};rows=[];endgeometry=[]
for i in range(97):
 s.frame_set(i+1);bpy.context.view_layer.update();g={n:geom(bpy.data.objects[n])[0] for n in mesh_names};res={n:float(np.abs(g[n]-(geometry[i][n]+offset[i])).max()) for n in mesh_names};poseerr=max(float(np.abs(np.array(b.matrix_basis)-localposes[i][b.name]).max()) for b in rig.pose.bones)
 for q in ids:actualfoot[q].append(g[mesh_names[0]][ids[q]].copy())
 rows.append({'frame':i+1,'root_offset_world_m':offset[i].tolist(),'world_translation_residual_by_actual_mesh_m':res,'original_body_bone_local_matrix_error':poseerr,'minimum_floor_gap_m':{q:float(actualfoot[q][-1][:,2].min()-floor) for q in ids},'finite':all(np.isfinite(g[n]).all() for n in mesh_names)})
 if i in [0,1,95,96]:endgeometry.append((i,g))
lane.off();assert snapshot(names)==before and snapshot(source_names)==source_sig
def footsummary(vs):
 out={}
 for q,v in vs.items():
  v=np.array(v);intervals=[];i=0;maxstep=0
  while i<97:
   if not contacts[q][i]:i+=1;continue
   j=i
   while j+1<97 and contacts[q][j+1]:j+=1
   common=sorted(set.intersection(*contacts[q][i:j+1]));travel=float(np.linalg.norm(v[i:j+1,common,:2]-v[i,common,:2],axis=2).max()) if common else None;intervals.append({'frames':[i+1,j+1],'common_source_contact_vertices':len(common),'anchored_world_XY_excursion_m':travel});i=j+1
  for i in range(1,97):
   common=sorted(contacts[q][i-1]&contacts[q][i])
   if common:maxstep=max(maxstep,float(np.linalg.norm(v[i,common,:2]-v[i-1,common,:2],axis=1).max()))
  out[q]={'stance_intervals':intervals,'max_anchored_stance_XY_excursion_m':max([x['anchored_world_XY_excursion_m'] for x in intervals if x['anchored_world_XY_excursion_m'] is not None]),'max_persistent_source_sole_XY_step_m':maxstep,'floor_min_gap_m':float((v[:,:,2]-floor).min()),'floor_gap_exact_vs_original_max_error_m':float(np.abs(v[:,:,2]-foot[q][:,:,2]).max())}
 return out
summary={'original':footsummary(foot),'candidate':footsummary(actualfoot)};vel=np.diff(offset,axis=0)*fps;seam={}
eg=dict(endgeometry)
for n in mesh_names:seam[n]={'translation_normalized_endpoint_error_m':float(np.abs((eg[96][n]-offset[96])-eg[0][n]).max()),'velocity_seam_delta_max_m_per_s':float(np.linalg.norm(((eg[96][n]-eg[95][n])-(eg[1][n]-eg[0][n]))*fps,axis=1).max()),'original_velocity_seam_delta_max_m_per_s':m['loop']['last_to_first_native_velocity_difference_max_m_per_s'][n]}
candidate=O/'Character_R4_WalkRootContact_EXPERIMENT_OFF_C1_20261005.blend';bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=False);assert snapshot(names)==before and snapshot(source_names)==source_sig
lib=O/'YURI_R4_WALK_ROOT_CONTACT_ACTIONS_ONLY_C1.blend';bpy.data.libraries.write(str(lib),{bpy.data.actions[n] for n in ACTIONS.values()},fake_user=True)
with bpy.data.libraries.load(str(lib),link=False) as (src,dst):assert len(src.actions)==4 and not src.objects and not src.meshes and not src.armatures
np.savez_compressed(O/'SOURCE_AND_CANDIDATE_SOLE_TRAJECTORIES_PRIVATE_C1.npz',root_world_offset=offset,**{q+'_source':v for q,v in foot.items()},**{q+'_candidate':np.array(v) for q,v in actualfoot.items()},**{q+'_vertex_ids':v for q,v in ids.items()})
meta={'task':'ROOT_PM_NATIVE_HEAD_SOURCE_CLOSE_TO_WALK_CONTACT_R1','source':str(P),'source_SHA':m['source_SHA'],'old_candidate':str(C),'old_candidate_SHA':m['candidate_SHA'],'old_library_SHA':m['library']['sha256'],'candidate':str(candidate),'candidate_SHA':sha(candidate),'library':{'file':str(lib),'sha256':sha(lib),'actions':4,'objects':0,'meshes':0,'armatures':0},'actions':ACTIONS,'frames':[1,97],'fps':24,'speed_factor':1,'method':'ONE source-sole XY negative median persistent vertex step, equal foot compromise double support; root Z0; no smoothing, ankle/knee IK or proportion edits. Separate Assembly_Root/face-root translation only. Original BODY/hair Actions reused unchanged.','foot_summary':summary,'root':{'end_displacement_world_m':offset[-1].tolist(),'path_length_m':float(np.linalg.norm(np.diff(offset,axis=0),axis=1).sum()),'speed_m_per_s_min_max':[float(np.linalg.norm(vel,axis=1).min()),float(np.linalg.norm(vel,axis=1).max())],'max_acceleration_m_per_s2':float(np.linalg.norm(np.diff(vel,axis=0)*fps,axis=1).max()),'speed_seam_difference_m_per_s':float(np.linalg.norm(vel[-1]-vel[0])),'loop_requires_accumulate_endpoint_delta_not_position_reset':True},'double_support_proximity_steps':double,'step_rows_private':steps,'actual_rows_private':rows,'loop_seam':seam,'source78_prior81_OFF_raw_identical':True,'no_force_COM_physics_support_proof':True,'existing_head_contact_HOLD_not_researched_or_waived':True,'gross_collision_gate':'Translation residual of all actual original body/head/hair vertices bounds geometry change; no new contact count epsilon research. Existing source contacts remain HOLD.','TierP':0}
(O/'WALK_ROOT_CONTACT_PRIVATE_C1.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
# Match original frozen97 front/quarter/side camera/resolution exactly; do not rerender control.
cam=s.camera;savecam=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width);saves=[]
for ob,k,v in [(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',2),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',320),(s.render,'resolution_y',320),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','JPEG'),(s.render.image_settings,'color_mode','RGB'),(s.render.image_settings,'color_depth','8'),(s.render.image_settings,'quality',92),(s.render,'filepath','')]:saves.append((ob,k,getattr(ob,k)));setattr(ob,k,v)
lane=WalkRootContactLane();lane.on()
for view,v in m['views'].items():
 folder=O/view;folder.mkdir();cam.data.type=v['type'];cam.data.ortho_scale=v['ortho_scale'];cam.location=v['location'];cam.rotation_euler=v['rotation_euler'];cam.data.lens=v['lens_mm'];cam.data.sensor_width=v['sensor_width_mm']
 for f in range(1,98):s.frame_set(f);bpy.context.view_layer.update();s.render.filepath=str(folder/f'{f:04}.jpg');bpy.ops.render.render(write_still=True)
lane.off();cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width=savecam;s.render.resolution_x=960;s.render.resolution_y=920;s.cycles.samples=8;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(O/'ROOT_CONTACT_OFF_SOURCE_NEUTRAL_C1.png');bpy.ops.render.render(write_still=True)
for ob,k,v in saves:setattr(ob,k,v)
assert snapshot(names)==before and snapshot(source_names)==source_sig and sha(P)==m['source_SHA'] and sha(C)==m['candidate_SHA'] and sha(m['library']['file'])==m['library']['sha256'];meta['views']=m['views'];meta['matched_all97_three_views_complete']=True;meta['full_raw_OFF_restored']=True;meta['elapsed_seconds']=time.perf_counter()-start;(O/'WALK_ROOT_CONTACT_PRIVATE_C1.json').write_text(json.dumps(meta,indent=2),encoding='utf8');print('WALK_ROOT_CONTACT_ONE_CANDIDATE_COMPLETE',summary,flush=True)
