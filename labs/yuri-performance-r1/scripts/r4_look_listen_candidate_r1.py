"""Reuse existing licensed A3 native upper-body rotations for one look/listen candidate."""
import bpy,sys,json,hashlib,math,numpy as np
from pathlib import Path
from mathutils import Matrix,Vector,Quaternion
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference
from r4_appearance_adapter import ReactionLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-look-listen-candidate-r1';O.mkdir(exist_ok=False)
S=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/target-reference/Character_Master_NeckSkin_R4.blend');OLD=B/'alpha-a3-contact-candidate-r2/Character_R4_A3_BODY_CANDIDATE_OFF_R2_20261004.blend';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(S)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa' and sha(OLD)=='1e16f3529566ed3e4132ca0e3ede86051bab35a89bc23e155c5f82a9cfab9fe8'
bpy.ops.wm.open_mainfile(filepath=str(S),use_scripts=False);s=bpy.context.scene;rig=bpy.data.objects['Meshy_Fitted_Rig'];head=bpy.data.objects['Character_Body_Head'];body=bpy.data.objects['Meshy_Body_NeutralCovered'];face=bpy.data.objects['Armature'];hair=bpy.data.objects['Hair_Rig_R4'];original=list(bpy.data.actions.keys());before=snapshot(original)
with (O/'SOURCE_SIGNATURE_PRIVATE_R1.json').open('x',encoding='utf8') as f:json.dump(before,f)
bones=['chest','neck','head'];original_q={n:rig.pose.bones[n].rotation_quaternion.copy() for n in bones};refhead=rig.matrix_world@rig.pose.bones['head'].matrix;refface=face.matrix_world@face.pose.bones['Root'].matrix;refhair=hair.matrix_world@hair.pose.bones['Hair_HeadRoot'].matrix
with bpy.data.libraries.load(str(OLD),link=False) as (src,dst):
 assert 'YURI_R4_A3_BODY_CANDIDATE_R2' in src.actions;dst.actions=['YURI_R4_A3_BODY_CANDIDATE_R2']
reused=dst.actions[0];tmp=ReactionLane();tmp.on(reused.name);s.frame_set(1);bpy.context.view_layer.update();first={n:rig.pose.bones[n].rotation_quaternion.copy() for n in bones};s.frame_set(49);bpy.context.view_layer.update();peak={n:rig.pose.bones[n].rotation_quaternion.copy() for n in bones};tmp.off();bpy.data.actions.remove(reused);assert not difference(before,snapshot(original))
strength={'chest':.15,'neck':.33,'head':.33};goal={}
for n in bones:
 delta=first[n].inverted()@peak[n]
 if delta.w<0:delta.negate()
 goal[n]=original_q[n]@Quaternion().slerp(delta,strength[n])
names={'Meshy_Fitted_Rig':'YURI_R4_LOOK_LISTEN_BODY_R1','Armature':'YURI_R4_LOOK_LISTEN_HEAD_TRANSPORT_R1','Hair_Rig_R4':'YURI_R4_LOOK_LISTEN_HAIR_TRANSPORT_R1'};lanes={n:ReactionLane(n) for n in names}
for n,name in names.items():
 a=bpy.data.actions.new(name);a.use_fake_user=True;a['source_fps']=30;a['lineage']='Existing A3 native Action local quaternion delta frame1->49, reduced; procedural attention clock/hold/nod/return';a.slots.new(id_type='OBJECT',name=n);lanes[n].on(name)
def points(o):
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();buf=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',buf);w=np.array(e.matrix_world,dtype=np.float64);v=buf.reshape(-1,3).astype(np.float64)@w[:3,:3].T+w[:3,3];e.to_mesh_clear();return v
def ease(t):t=max(0,min(1,t));return t*t*t*(t*(t*6-15)+10)
base=points(body);floor=float(base[:,2].min());sole=np.where(base[:,2]<floor+.028)[0];assert len(sole)>20;ref_forward=refhead.to_quaternion()@Vector((0,0,1));rows=[];maxsole=0;maxstep=0;last=None
for f in range(1,152):
 s.frame_set(f);u=0 if f<=12 else ease((f-12)/30) if f<=42 else 1 if f<=102 else 1-ease((f-102)/49)
 nod=math.radians(1.5)*math.sin(math.pi*(f-63)/20)**2 if 63<=f<=83 else 0
 for n in bones:
  b=rig.pose.bones[n];q=original_q[n].slerp(goal[n],u)
  if n=='neck':q=q@Quaternion(Vector((1,0,0)),nod)
  b.rotation_mode='QUATERNION';b.rotation_quaternion=q;b.keyframe_insert('rotation_quaternion',frame=f,group=n)
 bpy.context.view_layer.update();delta=(rig.matrix_world@rig.pose.bones['head'].matrix)@refhead.inverted();delta=Matrix.LocRotScale(delta.translation,delta.to_quaternion(),Vector((1,1,1)))
 for obj,bn,ref in [(face,'Root',refface),(hair,'Hair_HeadRoot',refhair)]:
  b=obj.pose.bones[bn];basis=b.bone.matrix_local.inverted()@obj.matrix_world.inverted()@delta@ref;b.rotation_mode='QUATERNION';b.location=basis.translation;b.rotation_quaternion=basis.to_quaternion();b.keyframe_insert('location',frame=f,group=bn);b.keyframe_insert('rotation_quaternion',frame=f,group=bn)
 bpy.context.view_layer.update();v=points(body);assert np.isfinite(v).all() and np.isfinite(points(head)).all();foot_delta=float(np.max(np.abs(v[sole]-base[sole])));maxsole=max(maxsole,foot_delta);assert foot_delta<1e-7,'Upper-body-only source foot geometry changed'
 joints={n:list((rig.matrix_world@rig.pose.bones[n].matrix).translation) for n in ['root','pelvis','head','hand.L','hand.R','foot.L','foot.R']}
 if last:maxstep=max(maxstep,max((Vector(joints[n])-Vector(last[n])).length for n in joints))
 last=joints;hm=rig.matrix_world@rig.pose.bones['head'].matrix;angle=math.degrees((hm.to_quaternion()@refhead.to_quaternion().inverted()).angle);forward=delta.to_quaternion()@Vector((0,-1,0));rows.append({'frame':f,'phase':'neutral' if f<=12 else 'look' if f<=42 else 'listen_hold' if f<=102 else 'return','head_world_matrix':[list(r) for r in hm],'head_delta_degrees':angle,'head_forward_world':list(forward),'joints':joints,'root_carrier_world':[0,0,0],'sole_max_abs_world_delta_m':foot_delta,'body_min_z_offset_m':float(v[:,2].min()-floor),'face_body_head_socket_distance_m':((face.matrix_world@face.pose.bones['J_Bip_C_Head'].matrix).translation-Vector(joints['head'])).length})
for name in names.values():
 for layer in bpy.data.actions[name].layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
endpoint=float(np.max(np.abs(v-base)));assert endpoint<1e-7
for lane in reversed(list(lanes.values())):lane.off()
assert not difference(before,snapshot(original));p=O/'Character_R4_LookListen_CANDIDATE_OFF_R1_20261004.blend';bpy.ops.wm.save_as_mainfile(filepath=str(p));assert sha(S)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
r={'source':str(S),'source_SHA':sha(S),'candidate':str(p),'candidate_SHA':sha(p),'candidate_bytes':p.stat().st_size,'source_fps':30,'source_scene_fps':24,'frames':[1,151],'movie_duration_sec':151/30,'key_interval_sec':150/30,'original_actions_preserved':len(original),'additive_body_actions':names,'authored_bones':bones,'timing':{'neutral':[1,12],'look':[13,42],'listen_hold':[43,102],'small_listen_nod':[63,83],'return':[103,151]},'lineage':{'reused_A3_candidate':str(OLD),'reused_A3_SHA':sha(OLD),'reused_Action':'YURI_R4_A3_BODY_CANDIDATE_R2','source_frame_delta':[1,49],'local_rotation_strength':strength,'donor_motion_id':'833e5d992179b527040b','donor':'StayStill l_aro_2_32','license':'MIT','listen_semantics':'Procedural hold+1.5deg nod; A3 was look proxy only, NOT donor-authored listen'},'head_animation_ownership':{'motion_owner':'Meshy_Fitted_Rig.chest/neck/head rotation + existing Armature.Root/Hair_HeadRoot rigid transport','gaze_inputs_written':False,'Face_GazeYaw_Pitch_and_original_face_drivers':'Retained source, no Action keys or driver edits','canonical_runtime_gaze_adapter_arbitration':'HOLD: actual consumer adapter not exercised; simultaneous head/neck writers require explicit owner/blend, not double head rotation'},'max_sole_world_delta_m':maxsole,'return_endpoint_body_max_abs_world_delta_m':endpoint,'max_joint_frame_step_m':maxstep,'head_max_world_delta_degrees':max(r['head_delta_degrees'] for r in rows),'all151_body_and_head_vertices_finite':True,'feet_root_pelvis_channels_written':False,'OFF_signature_exact_before_save':True,'frames_private':rows,'TierP':0,'StageB_F2_final_promotion':False,'visual_gate':'PENDING full three-view1x; source-only','finger_contact_exact_intersection':'HOLD'}
with (O/'LOOK_LISTEN_CANDIDATE_PRIVATE_R1.json').open('x',encoding='utf8') as f:json.dump(r,f,indent=2)
print('LOOK_LISTEN_SOURCE_OFF_PASS',r['candidate_SHA'],r['head_max_world_delta_degrees'],flush=True)
