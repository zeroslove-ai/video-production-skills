"""Fixed Female_Idle -> original R4 body action; no donor objects/export/source save."""
import bpy,sys,json,hashlib,math
from pathlib import Path
from mathutils import Matrix,Vector,Quaternion
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'alpha-a1-idle-candidate-r2'
INPUT=BASE/'alpha-a1-idle-inspect-r1/A1_SOURCE_DONOR_INSPECTION_PRIVATE_R1.json'
SOURCE=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/target-reference/Character_Master_NeckSkin_R4.blend')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,value):
    with (OUT/name).open('x',encoding='utf8') as f:json.dump(value,f,indent=2)
assert sha(SOURCE)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
OUT.mkdir(exist_ok=False);data=json.loads(INPUT.read_bytes());bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False)
s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];original=[a.name for a in bpy.data.actions]
before=snapshot(original);dump('SOURCE_SIGNATURE_PRIVATE_R1.json',before)
pose={b.name:(b.rotation_mode,tuple(b.location),tuple(b.rotation_quaternion),tuple(b.rotation_euler),tuple(b.rotation_axis_angle),tuple(b.scale)) for b in r.pose.bones}
had_ad=r.animation_data is not None;ad=r.animation_data;old_action=ad.action if ad else None
oldslot=ad.action_slot if ad else None;oldhandle=ad.action_slot_handle if ad else 0;oldlast=ad.last_slot_identifier if ad else ''
frame=s.frame_current;subframe=s.frame_subframe
mapping={'pelvis':'Hips','spine':'Spine','chest':'Spine2','neck':'Neck','head':'Head'}
for side,label in [('L','Left'),('R','Right')]:
    for t,d in [('clavicle','Shoulder'),('upper_arm','Arm'),('forearm','ForeArm'),('hand','Hand'),('thigh','UpLeg'),('shin','Leg'),('foot','Foot'),('toe','ToeBase')]:mapping[t+'.'+side]=label+d
    for t,d in [('thumb','Thumb'),('index','Index'),('middle','Middle'),('ring','Ring'),('pinky','Pinky')]:
        for j in range(1,4):mapping[f'{t}{j}.{side}']=label+'Hand'+d+str(j)
mapping={t:'mixamorig:'+d for t,d in mapping.items()}
assert len(mapping)==51 and all(n in data['donor']['bones'] for n in mapping.values())
dw=Matrix(data['donor']['world']);tw=r.matrix_world.copy();drest={n:dw@Matrix(v['matrix_local']) for n,v in data['donor']['bones'].items()}
qrest={n:m.to_quaternion() for n,m in drest.items()};tworldq=tw.to_quaternion()
scale=(tw@r.data.bones['pelvis'].head_local).z/drest['mixamorig:Hips'].translation.z
calibration={}
for t,n in mapping.items():
    tq=(tw@r.data.bones[t].matrix_local).to_quaternion()
    # Virtual target T calibration in ACTION only; never edits target rest.
    if t.split('.')[0] in ['clavicle','upper_arm','forearm','hand','thigh','shin','foot','toe'] or any(t.startswith(f) for f in ['thumb','index','middle','ring','pinky']):
        swing=(tq@Vector((0,1,0))).rotation_difference(qrest[n]@Vector((0,1,0)))
        calibration[t]=swing@tq
    else:calibration[t]=tq
a=bpy.data.actions.new('YURI_R4_A1_Female_Idle_BODY_CANDIDATE_R2');a.use_fake_user=True;r.animation_data_create().action=a
first=Matrix(data['donor']['samples'][0]['mixamorig:Hips']).translation
previous={};foot_samples=[];pelvis_samples=[];max_step=0;last_points=None
for f,values in enumerate(data['donor']['samples'],1):
    desired={}
    for b in r.pose.bones:
        if b.name not in mapping:continue
        n=mapping[b.name];dq=Matrix(values[n]).to_quaternion()@qrest[n].inverted()
        desired[b.name]=tworldq.inverted()@dq@calibration[b.name]
    for b in r.pose.bones:
        if b.name not in mapping:continue
        n=mapping[b.name] # THIS bone donor channel; retain failed R1.
        rel=b.bone.matrix_local if b.parent is None else b.parent.bone.matrix_local.inverted()@b.bone.matrix_local
        pq=desired.get(b.parent.name,b.parent.bone.matrix_local.to_quaternion()) if b.parent else Quaternion()
        q=rel.to_quaternion().inverted()@pq.inverted()@desired[b.name]
        if b.name in previous and previous[b.name].dot(q)<0:q.negate()
        previous[b.name]=q.copy();b.rotation_mode='QUATERNION';b.rotation_quaternion=q;b.location=(0,0,0);b.scale=(1,1,1)
        if b.name=='pelvis':
            delta=(Matrix(values[n]).translation-first)*scale
            b.location=(pq@rel.to_quaternion()).inverted()@tw.to_quaternion().inverted()@delta/tw.to_scale().x
            b.keyframe_insert('location',frame=f,group=b.name)
        b.keyframe_insert('rotation_quaternion',frame=f,group=b.name)
    s.frame_set(f);bpy.context.view_layer.update()
    points={n:list((tw@r.pose.bones[n].matrix).translation) for n in ['root','pelvis','foot.L','foot.R','hand.L','hand.R','head']}
    if last_points:max_step=max(max_step,max((Vector(points[n])-Vector(last_points[n])).length for n in points))
    foot_samples.append({n:points[n] for n in ['foot.L','foot.R']});pelvis_samples.append(points['pelvis']);last_points=points
for layer in a.layers:
    for strip in layer.strips:
        for bag in strip.channelbags:
            for fc in bag.fcurves:
                for k in fc.keyframe_points:k.interpolation='LINEAR'
# Save additive library in animation OFF state with every original binding/pose.
r.animation_data.action=old_action
if old_action and oldslot:r.animation_data.action_slot=oldslot
r.animation_data.action_slot_handle=oldhandle;r.animation_data.last_slot_identifier=oldlast
s.frame_set(frame,subframe=subframe)
for n,v in pose.items():
    b=r.pose.bones[n];b.rotation_mode,b.location,b.rotation_quaternion,b.rotation_euler,b.rotation_axis_angle,b.scale=v
if not had_ad:r.animation_data_clear()
bpy.context.view_layer.update();after=snapshot(original);dump('OFF_SIGNATURE_PRIVATE_R1.json',after)
assert before==after,'Source neutral/structural/driver ownership changed'
dest=OUT/'Character_R4_A1_Female_Idle_BODY_CANDIDATE_OFF_R2_20261004.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(dest),check_existing=True)
assert sha(SOURCE)==data['source_SHA']
dump('A1_RETARGET_RECEIPT_PRIVATE_R1.json',{'source_SHA':sha(SOURCE),'donor_SHA':data['donor_SHA'],'inspection_SHA':sha(INPUT),'candidate':str(dest),'candidate_bytes':dest.stat().st_size,'candidate_SHA':sha(dest),'action':a.name,'frames':[1,301],'fps':30,'duration_sec':10,'original_action_count':len(original),'mapped_bones':len(mapping),'mapping':mapping,'body_only':True,'face_gaze_hair_channels_written':0,'OFF_signature_exact':True,'original_rest_weights_neutral_drivers_preserved':True,'root_policy':'root stays original; pelvis displacement relative first donor frame scaled by native target/donor hip height; no object transform animation','scale':scale,'rest_axis_method':'Donor world delta and virtual limb-longitudinal swing calibration to donor T-rest, native target rest untouched; hierarchical parent removal; target native limb lengths retained','max_sampled_joint_frame_step_m':max_step,'foot_samples':foot_samples,'pelvis_samples':pelvis_samples,'loop_authored':False,'floor_or_IK_cleanup_applied':False,'gate':'CANDIDATE_ONLY; contact/visual QA pending; TierP0/StageB/O1/finalquality not promoted'})
print('A1_ADDITIVE_CANDIDATE_SAVED_OFF',dest.stat().st_size,sha(dest),flush=True)
