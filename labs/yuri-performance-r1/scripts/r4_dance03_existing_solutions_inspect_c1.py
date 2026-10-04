"""Inspect existing original leg/elbow solutions only; no new Action or source save."""
import bpy,sys,json,hashlib,math
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_adapter import ReactionLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'dance03-existing-solutions-inspect-c1';O.mkdir(exist_ok=False)
P=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/target-reference/Character_Master_NeckSkin_R4.blend');assert hashlib.sha256(P.read_bytes()).hexdigest()=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);r=bpy.data.objects['Meshy_Fitted_Rig'];s=bpy.context.scene
selected=['MESHY_R2_BODY_WalkInPlace','MESHY_QA3_BODY_QA_HipStress','MESHY_R2_BODY_Reach','MESHY_R2_BODY_TalkGesture']
rows=[]
for n in selected:
 a=bpy.data.actions[n];curves=[f for l in a.layers for st in l.strips for ba in st.channelbags for f in ba.fcurves];frames=sorted({int(round(k.co.x)) for f in curves for k in f.keyframe_points});lane=ReactionLane();lane.on(n)
 relevant=['thigh.L','shin.L','foot.L','upper_arm.L','forearm.L','upper_arm.R','forearm.R'];sample=[]
 for f in frames:
  s.frame_set(f);bpy.context.view_layer.update()
  sample.append({'frame':f,'bones':{bn:{'q':list(r.pose.bones[bn].rotation_quaternion),'delta_deg':math.degrees(r.pose.bones[bn].rotation_quaternion.angle),'axis':list(r.pose.bones[bn].rotation_quaternion.axis),'head_world':list(r.matrix_world@r.pose.bones[bn].head),'tail_world':list(r.matrix_world@r.pose.bones[bn].tail)} for bn in relevant}})
 rows.append({'action':n,'frame_range':list(a.frame_range),'key_frames':sample});lane.off()
(O/'EXISTING_NATIVE_SOLUTIONS_PRIVATE_C1.json').write_text(json.dumps({'source_SHA':hashlib.sha256(P.read_bytes()).hexdigest(),'rows':rows,'source_saved':False},indent=2),encoding='utf8');print('EXISTING_NATIVE_SOLUTIONS_INSPECTED',flush=True)
