"""Only grounded retarget derivatives: analytical two-bone contact cleanup."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence/model-handoff-r4';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/r4-model-handoff')
bpy.ops.wm.open_mainfile(filepath=str(OUT/'Character_Master_Reaction_R4_20261002.blend'));r=bpy.data.objects['Meshy_Fitted_Rig'];s=bpy.context.scene
reports=[]
for name,start,end in [('YRA_R4_Startle_Short',1,37),('YRA_R4_Land_Soft',1,43),('YRA_R4_BalanceRecover',1,55),('YRA_R4_QA_MilestoneA_Sequence',169,265)]:
 a=bpy.data.actions[name];r.animation_data.action=a;targets={side:r.data.bones['foot.'+side].head_local.copy() for side in ('L','R')};before=[];after=[]
 for f in range(start,end+1):
  s.frame_set(f);bpy.context.view_layer.update();before.append(max((r.matrix_world.to_3x3()@(r.pose.bones['foot.'+side].head-targets[side])).length for side in ('L','R')))
  for side in ('L','R'):
   thigh=r.pose.bones['thigh.'+side];shin=r.pose.bones['shin.'+side];foot=r.pose.bones['foot.'+side]
   h=thigh.head.copy();oldk=shin.head.copy();oldf=foot.head.copy();target=targets[side];v=target-h;distance=v.length;axis=v.normalized();l1=thigh.bone.length;l2=shin.bone.length
   d=min(max(distance,abs(l1-l2)+1e-7),l1+l2-1e-7);along=(l1*l1-l2*l2+d*d)/(2*d);height=math.sqrt(max(0,l1*l1-along*along))
   pole=oldk-h-axis*(oldk-h).dot(axis)
   if pole.length<1e-6:pole=Vector((0,-1,0))-axis*axis.dot(Vector((0,-1,0)))
   knee=h+axis*along+pole.normalized()*height
   q1=(oldk-h).rotation_difference(knee-h)@thigh.matrix.to_quaternion();q2=(oldf-oldk).rotation_difference(target-knee)@shin.matrix.to_quaternion()
   for b,q,pq in [(thigh,q1,thigh.parent.matrix.to_quaternion()),(shin,q2,q1),(foot,foot.bone.matrix_local.to_quaternion(),q2)]:
    rel=b.parent.bone.matrix_local.inverted()@b.bone.matrix_local;newq=rel.to_quaternion().inverted()@pq.inverted()@q
    if b.rotation_quaternion.dot(newq)<0:newq.negate()
    b.rotation_quaternion=newq;b.keyframe_insert('rotation_quaternion',frame=f,group=b.name)
   bpy.context.view_layer.update()
  after.append(max((r.matrix_world.to_3x3()@(r.pose.bones['foot.'+side].head-targets[side])).length for side in ('L','R')))
 reports.append({'action':name,'frames':[start,end],'before_max_ankle_rest_target_error_m':max(before),'after_max_ankle_rest_target_error_m':max(after),'modified_channels':'thigh/shin/foot quaternion only; no root/pelvis/arm/face/source action edit'})
 for layer in a.layers:
  for st in layer.strips:
   for bag in st.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
print('CONTACT_CHECK',reports,flush=True)
assert max(x['after_max_ankle_rest_target_error_m'] for x in reports)<.002
r.animation_data.action=bpy.data.actions['YRA_R4_QA_MilestoneA_Sequence'];s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Character_Master_Reaction_R4_20261002.blend'))
(E/'ground_contact.json').write_text(json.dumps({'method':'Analytical target-proportion two-bone IK; preserve source knee bend plane; rest ankle target; only grounded phases','clips':reports},indent=2),encoding='utf8');print('R4_CONTACT',reports,flush=True)
