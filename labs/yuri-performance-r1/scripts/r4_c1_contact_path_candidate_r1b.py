"""One source-owned C1 left upper-arm outward path hypothesis, unchanged original source."""
import bpy,sys,json,hashlib,math
from pathlib import Path
import numpy as np
from mathutils import Vector,Quaternion
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
from r4_reach_left_finger_timing_adapter_r2 import ReachFingerLane as BaseLane
from r4_c1_contact_path_adapter_r1 import ReachFingerLane,BODY,FINGER,TRANSPORT,ROOT
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-c1-contact-path-candidate-r1b';O.mkdir(exist_ok=False);load=lambda p:json.loads(Path(p).read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();prior=load(B/'alpha-reach-left-finger-timing-candidate-r2/REACH_LEFT_FINGER_TIMING_CANDIDATE_PRIVATE_R2.json');S=Path(prior['source']);assert sha(S)==prior['source_SHA'];bpy.ops.wm.open_mainfile(filepath=str(S),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered'];original=list(bpy.data.actions.keys());before=snapshot(original);(O/'SOURCE_SIGNATURE_PRIVATE_R1.json').write_text(json.dumps(before),encoding='utf-8');lib=B/'alpha-reach-left-finger-timing-off-qa-r2/YURI_R4_REACH_LEFT_FINGER_TIMING_ACTIONS_ONLY_R2.blend'
with bpy.data.libraries.load(str(lib),link=False) as (src,dst):assert len(src.actions)==7 and not src.objects and not src.meshes and not src.armatures;dst.actions=list(src.actions)
for a in dst.actions:a.use_fake_user=True
reused=[a.name for a in dst.actions];old_signatures=snapshot(reused)['actions'];OLD='YURI_R4_C1_REACH_BODY_R1';name='upper_arm.L';old=bpy.data.actions[OLD];new=old.copy();new.name=BODY;new.use_fake_user=True;new['lineage']='C1 body copy; ONLY upper_arm.L quaternion values changed: 8deg world-outward shoulder arc at inherited contact endpoints; unchanged peak/path18..43, reused R2 finger timing';new['source_fps']=30
curves=lambda a:[fc for la in a.layers for st in la.strips for ba in st.channelbags for fc in ba.fcurves]
def signature(fc):return {'path':fc.data_path,'index':fc.array_index,'keys':[(list(k.co),list(k.handle_left),list(k.handle_right),k.interpolation,k.type) for k in fc.keyframe_points],'modifiers':[m.type for m in fc.modifiers]}
oldcurves={(fc.data_path,fc.array_index):signature(fc) for fc in curves(old)}
def worldmesh():
 e=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);w=np.array(e.matrix_world);v=v.reshape(-1,3).astype(np.float64)@w[:3,:3].T+w[:3,3];e.to_mesh_clear();return v
neutral=worldmesh();floor=neutral[:,2].min();sole=np.where(neutral[:,2]<floor+.028)[0];allowed={name};changed=True
while changed:
 changed=False
 for b in r.pose.bones:
  if b.parent and b.parent.name in allowed and b.name not in allowed:allowed.add(b.name);changed=True
base=[];author=BaseLane();author.on(include_fingers=False)
for f in range(1,62):
 s.frame_set(f);bpy.context.view_layer.update();pb=r.pose.bones[name];parent=pb.parent;rel=parent.bone.matrix_local.inverted()@pb.bone.matrix_local
 if f==1:
  arm=(r.matrix_world@r.pose.bones['hand.L'].head-r.matrix_world@pb.head).normalized();axis=arm.cross(Vector((1,0,0))).normalized();assert axis.length>.9
 base.append({'quat':pb.rotation_quaternion.copy(),'basis_world_quat':(r.matrix_world@parent.matrix@rel).to_quaternion(),'matrices':{b.name:np.array(r.matrix_world@b.matrix) for b in r.pose.bones if b.name not in allowed},'wrist':r.matrix_world@r.pose.bones['hand.L'].head,'soles':worldmesh()[sole].copy(),'head':np.array(bpy.data.objects['Armature'].pose.bones['Root'].matrix),'hair':np.array(bpy.data.objects['Hair_Rig_R4'].pose.bones['Hair_HeadRoot'].matrix),'carrier':np.array(bpy.data.objects['Assembly_Root'].matrix_world)})
author.off();assert snapshot(original)==before
# Quintic envelope affects contact endpoints only, no peak change.
def ease(t):t=max(0,min(1,t));return t*t*t*(t*(t*6-15)+10)
def weight(f):
 if f<=7:return 1
 if f<18:return 1-ease((f-7)/11)
 if f<=43:return 0
 if f<50:return ease((f-43)/7)
 return 1
values=[]
for f,v in enumerate(base,1):
 q=Quaternion(v['basis_world_quat'].inverted()@axis,math.radians(8)*weight(f))@v['quat']
 if values and values[-1].dot(q)<0:q.negate()
 values.append(q)
path='pose.bones["upper_arm.L"].rotation_quaternion'
for fc in curves(new):
 if fc.data_path==path:
  for k in fc.keyframe_points:k.co[1]=values[int(round(k.co[0]))-1][fc.array_index]
changed_paths=[]
for fc in curves(new):
 key=(fc.data_path,fc.array_index)
 if signature(fc)!=oldcurves[key]:changed_paths.append(key);assert fc.data_path==path
assert len(changed_paths)==4 and snapshot(reused)['actions']==old_signatures
lane=ReachFingerLane();lane.on();rows=[];prev=None;maxstep=0;maxangle=0;outside=0;foot=0
for f in range(1,62):
 s.frame_set(f);bpy.context.view_layer.update();b=base[f-1];err=max(float(np.max(np.abs(np.array(r.matrix_world@r.pose.bones[n].matrix)-m))) for n,m in b['matrices'].items());assert err==0;v=worldmesh();assert np.isfinite(v).all();soleerr=float(np.max(np.abs(v[sole]-b['soles'])));foot=max(foot,soleerr);assert soleerr==0
 for obj,bn,key in [('Armature','Root','head'),('Hair_Rig_R4','Hair_HeadRoot','hair')]:assert np.array_equal(b[key],np.array(bpy.data.objects[obj].pose.bones[bn].matrix))
 assert np.array_equal(b['carrier'],np.array(bpy.data.objects['Assembly_Root'].matrix_world));wrist=r.matrix_world@r.pose.bones['hand.L'].head;q=r.pose.bones[name].rotation_quaternion.copy();delta=q.rotation_difference(b['quat']).angle;maxangle=max(maxangle,delta)
 if prev is not None:maxstep=max(maxstep,(wrist-prev).length)
 prev=wrist.copy();rows.append({'frame':f,'weight':weight(f),'left_wrist_world':list(wrist),'left_wrist_delta_world':list(wrist-b['wrist']),'left_hand_world':{'wrist':list(wrist),'tips':{n:list(r.matrix_world@r.pose.bones[n+'3.L'].tail) for n in ['index','middle','ring','pinky','thumb']}},'nonleft_arm_world_matrix_max_error':err,'sole_vertex_error_m':soleerr,'upper_arm_quaternion':list(q)})
 if f==1:first=v.copy()
 if f==61:last=v.copy()
assert rows[0]['left_wrist_delta_world'][0]>0 and rows[-1]['left_wrist_delta_world'][0]>0
lane.off();assert snapshot(original)==before and snapshot(reused)['actions']==old_signatures;added=[BODY,*reused];signatures=snapshot(added)['actions'];P=O/'Character_R4_C1_LeftArmClearance_CANDIDATE_OFF_R1B_20261004.blend';bpy.ops.wm.save_as_mainfile(filepath=str(P));assert sha(S)==prior['source_SHA'];d={'task':'ROOT_PM_C1_BASELINE_CONTACT_PATH_R1','source':str(S),'source_SHA':sha(S),'candidate':str(P),'candidate_SHA':sha(P),'candidate_bytes':P.stat().st_size,'original_actions_preserved':len(original),'lineage_action_library':{'file':str(lib),'SHA':sha(lib)},'previous_timing_candidate_SHA':prior['candidate_SHA'],'frames':[1,61],'source_fps':30,'source_scene_fps':24,'movie_duration_sec':61/30,'additive_body_actions':{'Meshy_Fitted_Rig':BODY,**TRANSPORT,'Assembly_Root':ROOT},'finger_action':FINGER,'preserved_previous_body_action':OLD,'preserved_previous_left_finger_action':prior['preserved_previous_left_finger_action'],'preserved_right_finger_action':prior['preserved_right_finger_action'],'existing_action_signatures':signatures,'existing_reused_actions_curve_signatures_unchanged':True,'changed_body_channels':changed_paths,'allowed_left_arm_descendants':sorted(allowed),'world_outward_axis':list(axis),'hypothesis':'8deg world-outward upper_arm.L only; weight1 frames1..7, quintic taper7..18 to0, exact original peak18..43, quintic43..50 to1, weight1 through61; unchanged lower arm/wrist local values inherit shoulder rigid change.','frames_private':rows,'maximum_upper_arm_correction_deg':math.degrees(maxangle),'nonleft_arm_C1_same_time_world_error':0,'sole_vertex_same_C1_max_error_m':foot,'carrier_face_hair_transport_same_C1_exact':True,'maximum_left_wrist_step_m':maxstep,'composition_start_end_body_world_error_m':float(np.max(np.abs(last-first))),'composition_end_vs_original_neutral_world_error_m':float(np.max(np.abs(last-neutral))),'all61_evaluated_body_vertices_finite':True,'OFF_signature_exact_before_save':True,'ownership_limit':'Only LEFT upper_arm.L local quaternion channels changed. All other C1 body local channels/transport/root copied exactly. Original neutral requires other body/right-arm ownership and remains HOLD.','contact':'PENDING actual full paired surface oracle','TierP':0};(O/'C1_CONTACT_PATH_CANDIDATE_PRIVATE_R1.json').write_text(json.dumps(d,indent=2),encoding='utf-8');print('C1_CONTACT_PATH_CANDIDATE',d['candidate_SHA'],rows[0]['left_wrist_delta_world'],maxstep,flush=True)
