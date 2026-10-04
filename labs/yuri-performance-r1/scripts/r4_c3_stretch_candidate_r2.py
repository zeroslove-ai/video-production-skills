"""One bounded original-R4 walk RM -> attention-turn proxy -> idle-stop placeholder.
Existing object/bone Actions only. Original skin/rest/rig/material/driver ownership unchanged.
"""
import bpy,json,hashlib,sys,math,numpy as np
from pathlib import Path
from mathutils import Matrix,Vector,Quaternion
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');OUT=BASE/'alpha-c3-stretch-candidate-r2';OUT.mkdir(exist_ok=False);INPUT=BASE/'alpha-c3-stretch-inspect-r1/C3_STRETCH_SOURCE_INSPECTION_PRIVATE_R1.json';data=json.loads(INPUT.read_bytes());SOURCE=Path(data['source'])
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
 samples=d['clips'][clip]['samples'];first=normalize@Matrix(samples[0][mapping['pelvis']]);first_root=(normalize@Matrix(samples[0]['root'])).translation if label=='UAL_UNUSED' else Vector((first.translation.x,first.translation.y,0));residual_first=first.translation-first_root;out=[]
 for values in samples:
  mats={n:normalize@Matrix(v) for n,v in values.items()};root=mats['root'].translation-first_root if label=='UAL_UNUSED' else Vector((mats['Hips'].translation.x-first.translation.x,mats['Hips'].translation.y-first.translation.y,0));desired={t:TW.to_quaternion().inverted()@(mats[n].to_quaternion()@rq[n].inverted())@cal[t] for t,n in mapping.items()};rot={}
  for b in rig.pose.bones:
   if b.name not in mapping:continue
   rel=b.bone.matrix_local if b.parent is None else b.parent.bone.matrix_local.inverted()@b.bone.matrix_local;pq=desired.get(b.parent.name,b.parent.bone.matrix_local.to_quaternion()) if b.parent else Quaternion();rot[b.name]=rel.to_quaternion().inverted()@pq.inverted()@desired[b.name]
  absolute_root=root+first_root;delta=(mats[mapping['pelvis']].translation-absolute_root-residual_first)*scale;parent=rig.pose.bones['pelvis'].parent;pq=desired.get(parent.name,parent.bone.matrix_local.to_quaternion());rel=parent.bone.matrix_local.inverted()@rig.data.bones['pelvis'].matrix_local;loc=(pq@rel.to_quaternion()).inverted()@TW.to_quaternion().inverted()@delta/TW.to_scale().x
  markers={side:(mats['ball_'+suffix].translation if label=='UAL_UNUSED' else mats[lab+'Toe'].translation) for side,suffix,lab in [('L','l','Left'),('R','r','Right')]}
  out.append({'rotation':rot,'pelvis':loc,'root':root*scale,'source_markers':markers,'source_scale':scale})
 return out,scale
clip_name=next(iter(data['donors']['reach']['clips']));reach,reach_scale=adapt('reach',clip_name,mapping_lafan,Matrix.Identity(4));assert len(reach)==215
sequence=[{**q,'segment':'C3_original_stretch','donor_frame':i,'cycle':1} for i,q in enumerate(reach,1)]
last=reach[-1]
for i in range(1,49):
 t=i/48;u=t*t*t*(t*(t*6-15)+10)
 sequence.append({'rotation':{n:q.slerp(Quaternion(),u) for n,q in last['rotation'].items()},'pelvis':last['pelvis']*(1-u),'root':last['root']*(1-u),'source_markers':None,'source_scale':reach_scale,'segment':'PROCEDURAL_neutral_recovery_48','donor_frame':None,'cycle':1})
assert len(sequence)==263
lanes={name:ReactionLane(name) for name in ['Meshy_Fitted_Rig','Armature','Hair_Rig_R4']};names={'Meshy_Fitted_Rig':'YURI_R4_C3_STRETCH_BODY_R2','Armature':'YURI_R4_C3_STRETCH_BODY_HEAD_TRANSPORT_R2','Hair_Rig_R4':'YURI_R4_C3_STRETCH_BODY_HAIR_TRANSPORT_R2'}
for r,name in names.items():a=bpy.data.actions.new(name);a.use_fake_user=True;a['source_fps']=30;a.slots.new(id_type='OBJECT',name=r);a['scope']='additive body motion / rigid head-root transport only; no expression/gaze/secondary authored channels';lanes[r].on(name)
cad=carrier.animation_data;saved_carrier={'had_ad':cad is not None,'action':cad.action if cad else None,'slot':cad.action_slot if cad else None,'handle':cad.action_slot_handle if cad else 0,'last':cad.last_slot_identifier if cad else '','loc':carrier.location.copy()};a=bpy.data.actions.new('YURI_R4_C3_STRETCH_ROOT_PATH_R2');a.use_fake_user=True;a['source_fps']=30;a.slots.new(id_type='OBJECT',name=carrier.name);a['scope']='Existing Assembly_Root world locomotion carrier; source RM translation preserved, procedural transition segments explicitly labeled';carrier.animation_data_create().action=a
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
assert float(np.max(np.abs(v-base)))<0.00001,'Recovery endpoint not original neutral geometry'
dest=OUT/'Character_R4_C3_Stretch_Reach_BODY_CANDIDATE_OFF_R2_20261004.blend';bpy.ops.wm.save_as_mainfile(filepath=str(dest));assert sha(SOURCE)==data['source_SHA'];root=np.array([r['joints']['root'] for r in rows]);segments={n:[min(r['frame'] for r in rows if r['segment']==n),max(r['frame'] for r in rows if r['segment']==n)] for n in dict.fromkeys(r['segment'] for r in rows)}
receipt={'task':'ROOT_PM_EXISTING_C3_STRETCH_SOURCE_FALLBACK_R1','source':str(SOURCE),'source_SHA':sha(SOURCE),'candidate':str(dest),'candidate_SHA':sha(dest),'candidate_bytes':dest.stat().st_size,'inspection_SHA':sha(INPUT),'source_fps':30,'source_scene_fps':24,'frames':[1,len(rows)],'key_interval_sec':(len(rows)-1)/30,'movie_duration_sec':len(rows)/30,'original_actions_preserved':len(original),'additive_body_actions':{**names,'Assembly_Root':a.name},'mapped_body_bones':21,'no_expressive_face_gaze_secondary_hair_channels_written':True,'rigid_head_hair_root_transport_required':'Existing original Armature.Root and Hair_HeadRoot rigid transport; no hierarchy/rest/weight/material/driver changes.','OFF_signature_exact_before_save':True,'root_world_range_m':np.ptp(root,0).tolist(),'root_end_displacement_m':float(np.linalg.norm(root[-1]-root[0])),'root_path_length_m':float(np.linalg.norm(np.diff(root,axis=0),axis=1).sum()),'max_joint_frame_step_m':max_step,'floor_support_Z_correction_range_m':[min(corrections),max(corrections)],'segments':segments,'source_normalization':'StayStill/LAFAN staged world axes retained, no mirror; native limb lengths/rest-aware21-bone mapping; hip height ratio','hip_height_ratio':reach_scale,'donor':{k:v for k,v in data['donors']['reach'].items() if k in ['file','sha256','bytes','source_fps']},'license':'MIT StayStill existing staged BVH-to-FBX input','selected_donor_action':clip_name,'motion_id':'c7cb1c20db655031333f','plan_step':'C3','use':'Existing 215-frame restrained chest-forward stretch ends extended; appended48-frame quintic Action-only neutral recovery. No prop/contact fixture or new motion family.','root_policy':'Imported Hips XY displacement retained/scaled; pelvis residual and sole-support Z corrected only. No horizontal foot/root locking.','all263_evaluated_body_vertices_finite':True,'procedural_recovery_frames':48,'original_donor_frames_retained':215,'recovery_end_body_world_max_abs_delta_from_original_OFF_m':float(np.max(np.abs(v-base))),'frames_private':rows,'TierP':0,'loop_authored':False,'prop_grip_contact_hold_certified':False,'visual_gate':'PENDING full1x source preview, no Unity/final visual claim'}
dump('C3_STRETCH_CANDIDATE_PRIVATE_R2.json',receipt);print('WALK_TURN_SOURCE_CANDIDATE_SAVED_OFF',receipt['candidate_SHA'],receipt['candidate_bytes'],flush=True)
