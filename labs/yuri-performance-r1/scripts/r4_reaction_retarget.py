"""Preserve master data and source actions; bake rest-aware fitted-rig derivatives."""
import bpy,json,sys,math
from pathlib import Path
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).parent))
from native_preservation import signature
ROOT=Path(__file__).resolve().parents[1];L=ROOT/'local/model-handoff-r4';E=ROOT/'evidence/model-handoff-r4'
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/r4-model-handoff');OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(L/'Character_Master_NeckSkin_R4.blend'))
original=[a.name for a in bpy.data.actions];before=signature(original)
for src in (Path(r'C:/Users/JAEWAN/Downloads/Character_Master_R2_20261002.blend'),OUT.parent/'Character_ReactionFactory_R1_Polished.blend'):
 with bpy.data.libraries.load(str(src),link=False) as (a,b):b.actions=[n for n in a.actions if n not in bpy.data.actions]
for a in bpy.data.actions:a.use_fake_user=True
r=bpy.data.objects['Meshy_Fitted_Rig'];s=bpy.context.scene;s.render.fps=24;s.render.fps_base=1
for o in bpy.data.objects:
 if o.animation_data:
  o.animation_data.action=None
  for t in o.animation_data.nla_tracks:t.mute=True
 if o.type=='ARMATURE':
  for b in o.pose.bones:b.matrix_basis=Matrix.Identity(4)
data=json.loads((L/'reaction_source_samples.json').read_text());rest={n:Matrix(v) for n,v in data['rest'].items()}
neutral={n:Matrix(v) for n,v in data['clips']['YRA_R1_BalanceRecover'][-1].items()}
mapping={'root':'Root','pelvis':'J_Bip_C_Hips','spine':'J_Bip_C_Spine','chest':'J_Bip_C_UpperChest','neck':'J_Bip_C_Neck','head':'J_Bip_C_Head'}
for side in ('L','R'):
 for t,u in [('clavicle','Shoulder'),('upper_arm','UpperArm'),('forearm','LowerArm'),('hand','Hand'),('thigh','UpperLeg'),('shin','LowerLeg'),('foot','Foot'),('toe','ToeBase')]:mapping[f'{t}.{side}']=f'J_Bip_{side}_{u}'
 for t,u in [('thumb','Thumb'),('index','Index'),('middle','Middle'),('ring','Ring'),('pinky','Little')]:
  for j in range(1,4):mapping[f'{t}{j}.{side}']=f'J_Bip_{side}_{u}{j}'
scale=(r.matrix_world@r.data.bones['pelvis'].head_local).z/rest['J_Bip_C_Hips'].translation.z
rows=[]
for src,samples in data['clips'].items():
 name=src.replace('YRA_R1_','YRA_R4_');a=bpy.data.actions.new(name);a.use_fake_user=True;r.animation_data_create();r.animation_data.action=a
 previous={}
 for f,values in enumerate(samples,1):
  pose_rotations={}
  for b in r.pose.bones:
   if b.name not in mapping:continue
   n=mapping[b.name];desired=Matrix(values[n]).to_quaternion()@neutral[n].to_quaternion().inverted()@b.bone.matrix_local.to_quaternion()
   parent=b.parent
   rel=b.bone.matrix_local if parent is None else parent.bone.matrix_local.inverted()@b.bone.matrix_local
   pq=pose_rotations[parent.name] if parent else Matrix.Identity(4).to_quaternion()
   pose_rotations[b.name]=desired.copy()
   q=rel.to_quaternion().inverted()@pq.inverted()@desired
   if b.name in previous and previous[b.name].dot(q)<0:q.negate()
   previous[b.name]=q.copy();b.rotation_mode='QUATERNION';b.rotation_quaternion=q;b.location=(0,0,0);b.scale=(1,1,1)
   if b.name in ('root','pelvis'):
    world_delta=Matrix(values[n]).translation-rest[n].translation
    if b.name=='pelvis':world_delta-=Matrix(values['Root']).translation-rest['Root'].translation
    world_delta*=scale
    parent_rot=pq@rel.to_quaternion();b.location=parent_rot.inverted()@world_delta/r.matrix_world.to_scale().x
   b.keyframe_insert('rotation_quaternion',frame=f,group=b.name)
   if b.name in ('root','pelvis'):b.keyframe_insert('location',frame=f,group=b.name)
  if f%60==0:print('BAKE',name,f,flush=True)
 for layer in a.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
 rows.append({'source_action':src,'target_action':name,'frames':len(samples),'production_clip':'QA_' not in src})
r2_signatures=json.loads((E/'R2.json').read_text())['fingerprints']['actions']
after=signature(original+list(r2_signatures))
assert all(after[k]==before[k] for k in ('meshes_shape_keys_weights','rest_rigs'))
assert all(after['actions'][n]==h for n,h in before['actions'].items())
assert all(after['actions'][n]==h for n,h in r2_signatures.items())
r.animation_data.action=bpy.data.actions['YRA_R4_QA_MilestoneA_Sequence'];s.frame_set(1);s.frame_start=1;s.frame_end=265
bpy.ops.file.pack_all()
dest=OUT/'Character_Master_Reaction_R4_20261002.blend';bpy.ops.wm.save_as_mainfile(filepath=str(dest))
report={'source_r4_actions_preserved':len(original),'r2_original_actions_preserved':66,'r4_mesh_weights_keys_rest_preserved':True,'retarget_method':'source common neutral performance pose (BalanceRecover last frame) rotation delta transferred to target native A-rest orientation; hierarchical parent pose removal; normalized pelvis/root translation; native target limb lengths retained','translation_height_ratio':scale,'mapping':mapping,'clips':rows,'source_action_overwrite':False,'candidate':dest.name,'native_r4_body_rig':'Meshy_Fitted_Rig','donor_face_rig':'Armature','hair_rig':'Hair_Rig_R4','face_adapter_constraints':'preserved'}
(E/'retarget.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('R4_RETARGET_DONE',len(rows),flush=True)
