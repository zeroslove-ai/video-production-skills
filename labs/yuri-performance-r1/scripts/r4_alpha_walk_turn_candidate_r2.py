"""One bounded original-R4 walk RM -> attention-turn proxy -> idle-stop placeholder.
Existing object/bone Actions only. Original skin/rest/rig/material/driver ownership unchanged.
"""
import bpy,json,hashlib,sys,math,numpy as np
from pathlib import Path
from mathutils import Matrix,Vector,Quaternion
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');OUT=BASE/'alpha-walk-turn-candidate-r2';OUT.mkdir(exist_ok=False);INPUT=BASE/'alpha-walk-turn-inspect-r1/WALK_TURN_SOURCE_INSPECTION_PRIVATE_R2.json';data=json.loads(INPUT.read_bytes());SOURCE=Path(data['source'])
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(n,d):
 with (OUT/n).open('x',encoding='utf8') as f:json.dump(d,f,indent=2)
assert sha(SOURCE)==data['source_SHA'];bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False);s=bpy.context.scene;rig=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered'];carrier=bpy.data.objects['Assembly_Root'];face=bpy.data.objects['Armature'];hair=bpy.data.objects['Hair_Rig_R4'];original=[a.name for a in bpy.data.actions];before=snapshot(original);dump('SOURCE_SIGNATURE_PRIVATE_R2.json',before)
assert rig.parent==carrier and body.parent==carrier and hair.parent==carrier and face.parent is None
TW=rig.matrix_world.copy();ref_head=TW@rig.pose.bones['head'].matrix;ref_face=face.matrix_world@face.pose.bones['Root'].matrix;ref_hair=hair.matrix_world@hair.pose.bones['Hair_HeadRoot'].matrix
mapping_ual={'pelvis':'pelvis','spine':'spine_01','chest':'spine_03','neck':'neck_01','head':'Head'};mapping_lafan={'pelvis':'Hips','spine':'Spine','chest':'Spine2','neck':'Neck','head':'Head'}
for side,l in [('L','l'),('R','r')]:
 for t,d in [('clavicle','clavicle'),('upper_arm','upperarm'),('forearm','lowerarm'),('hand','hand'),('thigh','thigh'),('shin','calf'),('foot','foot'),('toe','ball')]:mapping_ual[t+'.'+side]=d+'_'+l
 label='Left' if side=='L' else 'Right'
 for t,d in [('clavicle','Shoulder'),('upper_arm','Arm'),('forearm','ForeArm'),('hand','Hand'),('thigh','UpLeg'),('shin','Leg'),('foot','Foot'),('toe','Toe')]:mapping_lafan[t+'.'+side]=label+d
assert len(mapping_ual)==len(mapping_lafan)==21
N=Matrix.Rotation(math.pi,4,'Z') # UAL source world left-X/forward+Y -> R4 left+X/forward-Y; rotation, not mirror

def adapt(label,clip,mapping,normalize):
 d=data['donors'][label];dw=Matrix(d['world']);rest={n:normalize@dw@Matrix(v['matrix_local']) for n,v in d['bones'].items()};rq={n:m.to_quaternion() for n,m in rest.items()};scale=(TW@rig.data.bones['pelvis'].head_local).z/rest[mapping['pelvis']].translation.z;cal={}
 for t,n in mapping.items():
  tq=(TW@rig.data.bones[t].matrix_local).to_quaternion();cal[t]=(tq@Vector((0,1,0))).rotation_difference(rq[n]@Vector((0,1,0)))@tq if t.split('.')[0] in ['clavicle','upper_arm','forearm','hand','thigh','shin','foot','toe'] else tq
 samples=d['clips'][clip]['samples'];first=normalize@Matrix(samples[0][mapping['pelvis']]);first_root=(normalize@Matrix(samples[0]['root'])).translation if label=='walk' else Vector((first.translation.x,first.translation.y,0));residual_first=first.translation-first_root;out=[]
 for values in samples:
  mats={n:normalize@Matrix(v) for n,v in values.items()};root=mats['root'].translation-first_root if label=='walk' else Vector((mats['Hips'].translation.x-first.translation.x,mats['Hips'].translation.y-first.translation.y,0));desired={t:TW.to_quaternion().inverted()@(mats[n].to_quaternion()@rq[n].inverted())@cal[t] for t,n in mapping.items()};rot={}
  for b in rig.pose.bones:
   if b.name not in mapping:continue
   rel=b.bone.matrix_local if b.parent is None else b.parent.bone.matrix_local.inverted()@b.bone.matrix_local;pq=desired.get(b.parent.name,b.parent.bone.matrix_local.to_quaternion()) if b.parent else Quaternion();rot[b.name]=rel.to_quaternion().inverted()@pq.inverted()@desired[b.name]
  absolute_root=root+first_root;delta=(mats[mapping['pelvis']].translation-absolute_root-residual_first)*scale;parent=rig.pose.bones['pelvis'].parent;pq=desired.get(parent.name,parent.bone.matrix_local.to_quaternion());rel=parent.bone.matrix_local.inverted()@rig.data.bones['pelvis'].matrix_local;loc=(pq@rel.to_quaternion()).inverted()@TW.to_quaternion().inverted()@delta/TW.to_scale().x
  markers={side:(mats['ball_'+suffix].translation if label=='walk' else mats[lab+'Toe'].translation) for side,suffix,lab in [('L','l','Left'),('R','r','Right')]}
  out.append({'rotation':rot,'pelvis':loc,'root':root*scale,'source_markers':markers,'source_scale':scale})
 return out,scale
walk_name=next(n for n in data['donors']['walk']['clips'] if n.endswith('|Walk_Loop'));idle_name=next(n for n in data['donors']['walk']['clips'] if n.endswith('|Idle_Loop') and not any(x in n for x in ['Crouch','Pistol','Sitting','Spell','Swim']));turn_name=next(iter(data['donors']['turn_proxy']['clips']))
walk,walk_scale=adapt('walk',walk_name,mapping_ual,N);idle,_=adapt('walk',idle_name,mapping_ual,N);turn,turn_scale=adapt('turn_proxy',turn_name,mapping_lafan,Matrix.Identity(4));assert len(walk)==41 and len(turn)==147
sequence=[];root_period=walk[-1]['root']-walk[0]['root'];marker_period=N@Matrix(data['donors']['walk']['clips'][walk_name]['samples'][-1]['root']);marker_period=marker_period.translation
for i in range(81):
 cycle=(i-1)//40 if i else 0;phase=(i-1)%40+1 if i else 0;q=walk[phase];sequence.append({**q,'root':q['root']+root_period*cycle,'source_markers':{k:v+marker_period*cycle for k,v in q['source_markers'].items()},'segment':'walk_RM','donor_frame':phase+1,'cycle':cycle+1})
def blend(a,b,t,root,segment):
 u=t*t*(3-2*t);return {'rotation':{k:a['rotation'][k].slerp(b['rotation'][k],u) for k in a['rotation']},'pelvis':a['pelvis'].lerp(b['pelvis'],u),'root':root,'segment':segment,'source_markers':None,'donor_frame':None}
def hermite(p0,p1,v0,v1,t,T):return p0*(2*t**3-3*t**2+1)+v0*(t**3-2*t**2+t)*T+p1*(-2*t**3+3*t**2)+v1*(t**3-t**2)*T
last=sequence[-1];velocity=(last['root']-sequence[-2]['root'])*30;T=16/30;proxy_velocity=(turn[1]['root']-turn[0]['root'])*30;anchor=last['root']+velocity*T*.5
for j in range(1,17):sequence.append(blend(last,turn[0],j/16,hermite(last['root'],anchor,velocity,proxy_velocity,j/16,T),'walk_to_attention_proxy_deceleration'))
for i,q in enumerate(turn[1:],2):sequence.append({**q,'root':anchor+q['root'],'segment':'attention_turn_proxy','donor_frame':i,'cycle':1})
last=sequence[-1];velocity=(last['root']-sequence[-2]['root'])*30;T=20/30;stop=last['root']+velocity*T*.5
for j in range(1,21):sequence.append(blend(last,idle[0],j/20,hermite(last['root'],stop,velocity,Vector((0,0,0)),j/20,T),'stop_to_idle_placeholder'))
for i,q in enumerate(idle[1:31],2):sequence.append({**q,'root':stop.copy(),'segment':'idle_stop_hold','donor_frame':i,'cycle':1})
assert len(sequence)==293
lanes={name:ReactionLane(name) for name in ['Meshy_Fitted_Rig','Armature','Hair_Rig_R4']};names={'Meshy_Fitted_Rig':'YURI_R4_WALK_TURN_STOP_BODY_R2','Armature':'YURI_R4_WALK_TURN_STOP_BODY_HEAD_TRANSPORT_R2','Hair_Rig_R4':'YURI_R4_WALK_TURN_STOP_BODY_HAIR_TRANSPORT_R2'}
for r,name in names.items():a=bpy.data.actions.new(name);a.use_fake_user=True;a['source_fps']=30;a.slots.new(id_type='OBJECT',name=r);a['scope']='additive body motion / rigid head-root transport only; no expression/gaze/secondary authored channels';lanes[r].on(name)
cad=carrier.animation_data;saved_carrier={'had_ad':cad is not None,'action':cad.action if cad else None,'slot':cad.action_slot if cad else None,'handle':cad.action_slot_handle if cad else 0,'last':cad.last_slot_identifier if cad else '','loc':carrier.location.copy()};a=bpy.data.actions.new('YURI_R4_WALK_TURN_STOP_ROOT_PATH_R2');a.use_fake_user=True;a['source_fps']=30;a.slots.new(id_type='OBJECT',name=carrier.name);a['scope']='Existing Assembly_Root world locomotion carrier; source RM translation preserved, procedural transition segments explicitly labeled';carrier.animation_data_create().action=a
source_frame=s.frame_current;source_subframe=s.frame_subframe

def points():
 e=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();buf=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',buf);w=np.array(e.matrix_world,dtype=np.float64);v=buf.reshape(-1,3).astype(np.float64)@w[:3,:3].T+w[:3,3];e.to_mesh_clear();return v
# Neutral sole identities are read from original OFF body before any candidate key exists.
base=points();floor=float(base[:,2].min());sole={side:np.where((base[:,2]<floor+.028)&((base[:,0]>.00195) if side=='L' else (base[:,0]<.00195)))[0] for side in ['L','R']};assert all(len(v)>10 for v in sole.values())
rows=[];previous_q={};previous_joints=None;max_step=0;corrections=[]
for f,q in enumerate(sequence,1):
 s.frame_set(f);carrier.location=saved_carrier['loc']+q['root']
 for name,rot in q['rotation'].items():
  b=rig.pose.bones[name];rot=rot.copy()
  if name in previous_q and previous_q[name].dot(rot)<0:rot.negate()
  previous_q[name]=rot.copy();b.rotation_mode='QUATERNION';b.rotation_quaternion=rot;b.location=q['pelvis'] if name=='pelvis' else (0,0,0)
 bpy.context.view_layer.update();v=points();offset=min(float(v[idx,2].min()-floor) for idx in sole.values());assert abs(offset)<.15,'Floor correction outside bounded walking support envelope'
 b=rig.pose.bones['pelvis'];parent=b.parent;rel=parent.bone.matrix_local.inverted()@b.bone.matrix_local;vector=(parent.matrix.to_quaternion()@rel.to_quaternion()).inverted()@rig.matrix_world.to_quaternion().inverted()@Vector((0,0,1))/rig.matrix_world.to_scale().x;b.location-=vector*offset;corrections.append(offset)
 for name in q['rotation']:
  b=rig.pose.bones[name];b.keyframe_insert('rotation_quaternion',frame=f,group=name)
  if name=='pelvis':b.keyframe_insert('location',frame=f,group=name)
 carrier.keyframe_insert('location',frame=f,group='SOURCE_RM_ROOT_PATH')
 bpy.context.view_layer.update();head_delta=(rig.matrix_world@rig.pose.bones['head'].matrix)@ref_head.inverted();head_delta=Matrix.LocRotScale(head_delta.translation,head_delta.to_quaternion(),Vector((1,1,1)))
 for obj,bn,ref in [(face,'Root',ref_face),(hair,'Hair_HeadRoot',ref_hair)]:
  bone=obj.pose.bones[bn];desired=obj.matrix_world.inverted()@head_delta@ref;basis=bone.bone.matrix_local.inverted()@desired;bone.rotation_mode='QUATERNION';bone.location=basis.translation;bone.rotation_quaternion=basis.to_quaternion();bone.keyframe_insert('location',frame=f,group=bn);bone.keyframe_insert('rotation_quaternion',frame=f,group=bn)
 bpy.context.view_layer.update();v=points();assert np.isfinite(v).all();joints={n:list((rig.matrix_world@rig.pose.bones[n].matrix).translation) for n in ['root','pelvis','head','hand.L','hand.R','foot.L','foot.R']}
 if previous_joints:max_step=max(max_step,max((Vector(joints[n])-Vector(previous_joints[n])).length for n in joints))
 previous_joints=joints
 face_head=(face.matrix_world@face.pose.bones['J_Bip_C_Head'].matrix).translation;hair_head=(hair.matrix_world@hair.pose.bones['Hair_HeadRoot'].matrix).translation
 rows.append({'frame':f,'segment':q['segment'],'donor_frame':q['donor_frame'],'root_carrier_world':list(q['root']),'joints':joints,'soles':{side:{'offset_m':float(v[idx,2].min()-floor),'centroid':v[idx].mean(0).tolist()} for side,idx in sole.items()},'source_toe_markers_world':{k:list(x) for k,x in q['source_markers'].items()} if q['source_markers'] else None,'body_min_z_offset_m':float(v[:,2].min()-floor),'face_socket_body_head_distance_m':(face_head-Vector(joints['head'])).length,'hair_socket_body_head_distance_m':(hair_head-Vector(joints['head'])).length})
 if f%60==0:print('WALK_TURN_BODY_QA',f,len(sequence),flush=True)
for name in [*names.values(),a.name]:
 action=bpy.data.actions[name]
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
for lane in reversed(list(lanes.values())):lane.off()
carrier.animation_data.action=saved_carrier['action']
if saved_carrier['action'] and saved_carrier['slot']:carrier.animation_data.action_slot=saved_carrier['slot']
carrier.animation_data.action_slot_handle=saved_carrier['handle'];carrier.animation_data.last_slot_identifier=saved_carrier['last'];carrier.location=saved_carrier['loc']
if not saved_carrier['had_ad']:carrier.animation_data_clear()
s.frame_set(before and data['target']['objects'] and lanes['Meshy_Fitted_Rig'].scene.frame_current);bpy.context.view_layer.update();after=snapshot(original);dump('OFF_SIGNATURE_PRIVATE_R2.json',after);assert before==after,'Original OFF data changed'
dest=OUT/'Character_R4_Walk_AttentionTurn_Stop_BODY_CANDIDATE_OFF_R2_20261004.blend';bpy.ops.wm.save_as_mainfile(filepath=str(dest));assert sha(SOURCE)==data['source_SHA'];root=np.array([r['joints']['root'] for r in rows]);segments={n:[min(r['frame'] for r in rows if r['segment']==n),max(r['frame'] for r in rows if r['segment']==n)] for n in dict.fromkeys(r['segment'] for r in rows)}
receipt={'task':'ROOT_PM_ALPHA_SOURCE_WALK_TURN_CANDIDATE_R2','source':str(SOURCE),'source_SHA':sha(SOURCE),'candidate':str(dest),'candidate_SHA':sha(dest),'candidate_bytes':dest.stat().st_size,'inspection_SHA':sha(INPUT),'source_fps':30,'source_scene_fps':24,'turn_original_BVH_fps':30.0003,'frames':[1,len(rows)],'key_interval_sec':(len(rows)-1)/30,'movie_duration_sec':len(rows)/30,'original_actions_preserved':len(original),'additive_body_actions':{**names,'Assembly_Root':a.name},'mapped_body_bones':21,'no_expressive_face_gaze_secondary_hair_channels_written':True,'rigid_head_hair_root_transport_required':'Original Armature.Root and Hair_Rig_R4.Hair_HeadRoot carry body head transform; no parent/constraint/rest/weight/mesh/driver edits. Original Assembly_Root carries world path for body/hair; body local root is not a world-root lock.','OFF_signature_exact_before_save':True,'root_world_range_m':np.ptp(root,0).tolist(),'root_end_displacement_m':float(np.linalg.norm(root[-1]-root[0])),'root_path_length_m':float(np.linalg.norm(np.diff(root,axis=0),axis=1).sum()),'max_joint_frame_step_m':max_step,'floor_support_Z_correction_range_m':[min(corrections),max(corrections)],'segments':segments,'source_normalization':'UAL world yaw180deg rotation, no mirror; LaFAN identity; target native limb lengths and hip-height ratios','walk_hip_height_ratio':walk_scale,'turn_hip_height_ratio':turn_scale,'dedicated_turn':'MISSING; existing MIT lb_lef_2_08 attention-turn proxy only, no dedicated locomotion heading-change claim','dedicated_stop':'MISSING; Hermite world-root deceleration plus smooth body-pose blend to existing CC0 Idle_Loop placeholder, not authored stop','root_policy':'RM source trajectory retained/scaled for two40-frame cycles; explicit16frame procedural deceleration bridge; source Hips XY of attention proxy transported in world; explicit20frame stop-to-idle bridge; world root finally stationary during actual idle hold. No in-place walk falsely relabeled locomotion.','donors':{k:{'file':v['file'],'sha256':v['sha256'],'bytes':v['bytes'],'license':'CC0-1.0' if k=='walk' else 'MIT'} for k,v in data['donors'].items()},'selected_donor_actions':[walk_name,turn_name,idle_name],'all293_evaluated_body_vertices_finite':True,'frames_private':rows,'TierP':0,'loop_authored':False,'foot_slip_contact_physics_certified':False,'visual_gate':'PENDING full1x preview; source subset only','physics_contract':'Root carrier + original-rig transport separate editable Actions. No Unity/runtime implementation, actual consumer contract PENDING.'}
dump('WALK_TURN_STOP_CANDIDATE_PRIVATE_R2.json',receipt);print('WALK_TURN_SOURCE_CANDIDATE_SAVED_OFF',receipt['candidate_SHA'],receipt['candidate_bytes'],flush=True)
