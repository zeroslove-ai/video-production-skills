"""ONE source-only stop bridge procedural-step correction; existing native bones only."""
import bpy,json,hashlib,sys,math,numpy as np
from pathlib import Path
from mathutils import Vector,Quaternion
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');OUT=BASE/'walk-contact-candidate-r1';OUT.mkdir(exist_ok=False)
R3=BASE/'alpha-walk-turn-candidate-r3/Character_R4_Walk_AttentionTurn_Stop_BODY_CANDIDATE_OFF_R3_20261004.blend';EXPECTED='35c5a9d00bdef2ca2b82e35645bf9da87e6f050ae6ead0ce0a9f9bd859bbf026'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(n,v):
 with (OUT/n).open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
assert sha(R3)==EXPECTED;bpy.ops.wm.open_mainfile(filepath=str(R3),use_scripts=False)
s=bpy.context.scene;rig=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered'];carrier=bpy.data.objects['Assembly_Root'];original=[a.name for a in bpy.data.actions];before=snapshot(original);dump('OFF_BEFORE_SIGNATURE_PRIVATE_R1.json',before)
def points():
 e=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();buf=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',buf);w=np.array(e.matrix_world,dtype=np.float64);v=buf.reshape(-1,3).astype(np.float64)@w[:3,:3].T+w[:3,3];e.to_mesh_clear();return v
neutral=points();floor=float(neutral[:,2].min());sole={side:np.where((neutral[:,2]<floor+.028)&((neutral[:,0]>.00195) if side=='L' else (neutral[:,0]<.00195)))[0] for side in ['L','R']};assert all(len(v)>10 for v in sole.values())
old={'Meshy_Fitted_Rig':'YURI_R4_WALK_TURN_STOP_BODY_R3','Armature':'YURI_R4_WALK_TURN_STOP_BODY_HEAD_TRANSPORT_R3','Hair_Rig_R4':'YURI_R4_WALK_TURN_STOP_BODY_HAIR_TRANSPORT_R3','Assembly_Root':'YURI_R4_WALK_TURN_STOP_ROOT_PATH_R3'}
lanes={name:ReactionLane(name) for name in ['Meshy_Fitted_Rig','Armature','Hair_Rig_R4']}
for n,l in lanes.items():l.on(old[n])
ad=carrier.animation_data;saved={'had':ad is not None,'action':ad.action if ad else None,'slot':ad.action_slot if ad else None,'handle':ad.action_slot_handle if ad else 0,'last':ad.last_slot_identifier if ad else '', 'loc':carrier.location.copy()};carrier.animation_data_create().action=bpy.data.actions[old['Assembly_Root']];carrier.animation_data.action_slot=carrier.animation_data.action.slots[0]
def observe(f):
 s.frame_set(f);bpy.context.view_layer.update();v=points();assert np.isfinite(v).all();j={n:list((rig.matrix_world@rig.pose.bones[n].matrix).translation) for n in ['root','pelvis','head','hand.L','hand.R','foot.L','foot.R','thigh.L','shin.L','thigh.R','shin.R']}
 return {'frame':f,'body_world_vertex_hash':hashlib.sha256(v.tobytes()).hexdigest(),'carrier':list(carrier.location),'joints':j,'soles':{side:{'centroid':v[idx].mean(0).tolist(),'min_z_offset_m':float(v[idx,2].min()-floor)} for side,idx in sole.items()},'head_root':list((bpy.data.objects['Armature'].matrix_world@bpy.data.objects['Armature'].pose.bones['Root'].matrix).translation),'hair_root':list((bpy.data.objects['Hair_Rig_R4'].matrix_world@bpy.data.objects['Hair_Rig_R4'].pose.bones['Hair_HeadRoot'].matrix).translation)}
baseline=[observe(f) for f in range(1,294)];dump('R3_FULL_NATIVE_BASELINE_PRIVATE_R1.json',baseline)
new={}
for obj,name in old.items():
 a=bpy.data.actions[name].copy();a.name=name.replace('_R3','_CONTACT_R1');a.use_fake_user=True;a['contact_scope']='Only244..263 stop bridge sequential procedural steps, not extracted/authored stance';new[obj]=a.name;bpy.data.objects[obj].animation_data.action=a;bpy.data.objects[obj].animation_data.action_slot=a.slots[0]
# New procedural phase annotation: L swing first half, R planted; then R swing, L planted.
# World root, pelvis and upper body remain EXACT R3. Native leg quaternion correction only.
corrections=[]
def keep_foot_world(side,wq):
 foot=rig.pose.bones['foot.'+side];rel=foot.parent.bone.matrix_local.inverted()@foot.bone.matrix_local;desired=rig.matrix_world.to_quaternion().inverted()@wq
 foot.rotation_quaternion=rel.to_quaternion().inverted()@foot.parent.matrix.to_quaternion().inverted()@desired;bpy.context.view_layer.update()
def score(side):
 v=points();idx=sole[side];return np.array([v[idx,0].mean(),v[idx,1].mean(),v[idx,2].min()-floor])
for f in range(244,264):
 s.frame_set(f);bpy.context.view_layer.update();rec={'frame':f,'sides':{}}
 for side in ['L','R']:
  a=baseline[242]['soles'][side];b=baseline[262]['soles'][side];u=max(0,min(1,(f-243)/10 if side=='L' else (f-253)/10));blend=u*u*(3-2*u)
  # sin^2 clearance has zero endpoint velocity; no root/path alteration or horizontal freeze.
  clearance=.035*math.sin(math.pi*u)**2
  goal=np.array([a['centroid'][i]*(1-blend)+b['centroid'][i]*blend for i in [0,1]]+[a['min_z_offset_m']*(1-blend)+b['min_z_offset_m']*blend+clearance])
  bones=[rig.pose.bones[k+'.'+side] for k in ['thigh','shin']];baseq=[bone.rotation_quaternion.copy() for bone in bones];foot=rig.pose.bones['foot.'+side];wq=(rig.matrix_world@foot.matrix).to_quaternion();iterations=0
  for it in range(16):
   current=score(side);res=goal-current
   if np.linalg.norm(res)<.00020:break
   originals=[bone.rotation_quaternion.copy() for bone in bones];jac=np.empty((3,6));eps=.001
   for k in range(6):
    axis=Vector(tuple(1 if i==k%3 else 0 for i in range(3)));bone=bones[k//3];bone.rotation_quaternion=originals[k//3]@Quaternion(axis,eps);bpy.context.view_layer.update();keep_foot_world(side,wq);jac[:,k]=(score(side)-current)/eps;bone.rotation_quaternion=originals[k//3];bpy.context.view_layer.update();keep_foot_world(side,wq)
   delta=jac.T@np.linalg.solve(jac@jac.T+np.eye(3)*1e-7,res);length=np.linalg.norm(delta)
   if length>.16:delta*=.16/length
   best=False
   for factor in [1,.5,.25]:
    for k,bone in enumerate(bones):
     vec=Vector(delta[k*3:k*3+3]*factor);bone.rotation_quaternion=originals[k]@Quaternion(vec.normalized(),vec.length) if vec.length>1e-10 else originals[k]
    bpy.context.view_layer.update();keep_foot_world(side,wq)
    if np.linalg.norm(goal-score(side))<np.linalg.norm(res):best=True;break
   if not best:
    for bone,q in zip(bones,originals):bone.rotation_quaternion=q
    bpy.context.view_layer.update();keep_foot_world(side,wq);break
   iterations=it+1
  residual=float(np.linalg.norm(goal-score(side)));angles=[q.rotation_difference(bone.rotation_quaternion).angle for q,bone in zip(baseq,bones)]
  assert residual<.003,(f,side,residual)
  assert max(angles)<.8,(f,side,angles)
  rec['sides'][side]={'phase':'SWING_PROCEDURAL' if 0<u<1 else 'SUPPORT_PROCEDURAL','phase_u':u,'clearance_m':clearance,'goal_centroid_XY_minZ':goal.tolist(),'actual_centroid_XY_minZ':score(side).tolist(),'solve_residual_m':residual,'iterations':iterations,'native_thigh_shin_delta_angles_rad':angles}
  for bone in [*bones,foot]:bone.keyframe_insert('rotation_quaternion',frame=f,group=bone.name)
 corrections.append(rec)
for layer in bpy.data.actions[new['Meshy_Fitted_Rig']].layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    for key in fc.keyframe_points:key.interpolation='LINEAR'
after=[observe(f) for f in range(1,294)];assert all(a['body_world_vertex_hash']==b['body_world_vertex_hash'] for a,b in zip(baseline,after) if not 244<=a['frame']<=263)
assert all(a['carrier']==b['carrier'] and a['head_root']==b['head_root'] and a['hair_root']==b['hair_root'] and a['joints']['pelvis']==b['joints']['pelvis'] and a['joints']['head']==b['joints']['head'] for a,b in zip(baseline,after))
# Candidate exact same evaluated geometry at all273 untouched frames supports image reuse.
dump('CONTACT_PHASE_SOLVE_PRIVATE_R1.json',corrections);dump('AFTER_FULL_NATIVE_PRIVATE_R1.json',after)
for lane in reversed(list(lanes.values())):lane.off()
carrier.animation_data.action=saved['action']
if saved['action'] and saved['slot']:carrier.animation_data.action_slot=saved['slot']
carrier.animation_data.action_slot_handle=saved['handle'];carrier.animation_data.last_slot_identifier=saved['last'];carrier.location=saved['loc']
if not saved['had']:carrier.animation_data_clear()
bpy.context.view_layer.update();off=snapshot(original);dump('OFF_AFTER_SIGNATURE_PRIVATE_R1.json',off);assert before==off
file=OUT/'Character_R4_Walk_StopContact_CANDIDATE_OFF_R1_20261004.blend';bpy.ops.wm.save_as_mainfile(filepath=str(file));assert sha(R3)==EXPECTED
receipt={'task':'ROOT_PM_WALK_SOURCE_CONTACT_TRANSITION_CLOSURE_R1','baseline_SHA':EXPECTED,'candidate':str(file),'candidate_bytes':file.stat().st_size,'candidate_SHA':sha(file),'additive_body_actions':new,'frames':[1,293],'source_fps':30,'source_scene_fps':24,'modified_frames':[244,263],'only_changed_channels':'Native thigh/shin/foot quaternion, L/R. Original root/carrier/pelvis/head/face/hair/torso exact all293.','all293_native_mesh_finite':True,'all273_unmodified_frames_evaluated_world_vertex_hash_identical':True,'original_OFF_all82_prior_actions_exact':True,'procedural_stance_labels':'L swing244..252/support253..263; R support244..253/swing254..262; endpoint support263. Inferred design, not donor labels.','clearance_m':.035,'max_solver_residual_m':max(s['solve_residual_m'] for r in corrections for s in r['sides'].values()),'original_R3_immutable':True,'world_root_trajectory_unchanged':True,'TierP':0,'visual_contact_physics_Unity_F2_F3':'PENDING; no promotion','before_after_visual':'PENDING fixed camera1x'};dump('CONTACT_CANDIDATE_RECEIPT_R1.json',receipt);print(json.dumps(receipt),flush=True)
