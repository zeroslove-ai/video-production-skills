"""One authored right-hand social greeting on original R4, existing bones only."""
import bpy,sys,json,hashlib,math
from pathlib import Path
from mathutils import Vector,Quaternion
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-social-wave-candidate-r1';O.mkdir(exist_ok=False)
S=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/target-reference/Character_Master_NeckSkin_R4.blend');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(S)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
bpy.ops.wm.open_mainfile(filepath=str(S),use_scripts=False);s=bpy.context.scene;rig=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered'];original=list(bpy.data.actions.keys());before=snapshot(original)
with (O/'SOURCE_SIGNATURE_PRIVATE_R1.json').open('x',encoding='utf8') as f:json.dump(before,f)
qrest={n:b.matrix.to_quaternion().copy() for n,b in rig.pose.bones.items()};bones=['upper_arm.R','forearm.R','hand.R'];rest={n:rig.data.bones[n].matrix_local.to_quaternion() for n in bones};dirs={'upper_arm.R':Vector((-.75,-.18,-.45)).normalized(),'forearm.R':Vector((.05,-.4,.91)).normalized(),'hand.R':Vector((-.03,-.15,1)).normalized()}
goal={n:(rest[n]@Vector((0,1,0))).rotation_difference(dirs[n])@rest[n] for n in bones}
a=bpy.data.actions.new('YURI_R4_SOCIAL_GREETING_WAVE_BODY_R1');a.use_fake_user=True;a['source_fps']=30;a['lineage']='Authored procedural R4 native right-arm gesture; no donor';a.slots.new(id_type='OBJECT',name=rig.name);lane=ReactionLane();lane.on(a.name)
def ease(t):t=max(0,min(1,t));return t*t*t*(t*(t*6-15)+10)
rows=[];last=None;maxstep=0;minimum_hand_head=100
for f in range(1,92):
 s.frame_set(f)
 if f<=12:blend=0;anticipation=math.sin(math.pi*(f-1)/11)*-.025
 elif f<=31:blend=ease((f-12)/19);anticipation=0
 elif f<=67:blend=1;anticipation=0
 else:blend=1-ease((f-67)/24);anticipation=0
 phase=(f-32)/27;wave=math.sin(phase*4*math.pi)*math.sin(math.pi*phase)**2 if 32<=f<=59 else 0
 desired={}
 for n in bones:
  target=goal[n]
  if n=='hand.R':target=Quaternion(Vector((0,-1,0)),math.radians(12)*wave)@target
  if n=='forearm.R':target=Quaternion(Vector((0,-1,0)),math.radians(3)*wave)@target
  q=qrest[n].slerp(target,blend)
  if n=='upper_arm.R' and anticipation:q=Quaternion(Vector((1,0,0)),anticipation)@q
  desired[n]=q;b=rig.pose.bones[n];parent=desired.get(b.parent.name,qrest[b.parent.name]);rel=b.parent.bone.matrix_local.inverted()@b.bone.matrix_local;b.rotation_mode='QUATERNION';b.rotation_quaternion=rel.to_quaternion().inverted()@parent.inverted()@q;b.keyframe_insert('rotation_quaternion',frame=f,group=n)
 bpy.context.view_layer.update();e=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();buf=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',buf);assert np.isfinite(buf).all();e.to_mesh_clear()
 joints={n:list((rig.matrix_world@rig.pose.bones[n].matrix).translation) for n in ['root','pelvis','head','upper_arm.R','forearm.R','hand.R','hand.L','foot.R','foot.L']}
 if last:maxstep=max(maxstep,max((Vector(joints[n])-Vector(last[n])).length for n in joints))
 minimum_hand_head=min(minimum_hand_head,(Vector(joints['hand.R'])-Vector(joints['head'])).length);last=joints;rows.append({'frame':f,'joints':joints,'blend':blend,'wave':wave,'root_carrier_world':[0,0,0]})
for layer in a.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    for k in fc.keyframe_points:k.interpolation='LINEAR'
lane.off();after=snapshot(original);assert before==after
p=O/'Character_R4_SocialGreeting_Wave_CANDIDATE_OFF_R1_20261004.blend';bpy.ops.wm.save_as_mainfile(filepath=str(p));assert sha(S)==before['source_sha256'] if 'source_sha256' in before else sha(S)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
r={'source':str(S),'source_SHA':sha(S),'candidate':str(p),'candidate_SHA':sha(p),'candidate_bytes':p.stat().st_size,'frames':[1,91],'source_fps':30,'source_scene_fps':24,'movie_duration_sec':91/30,'original_actions_preserved':len(original),'additive_body_actions':{'Meshy_Fitted_Rig':a.name},'authored_bones':bones,'lineage':'Procedural native R4 right-arm greeting; no donor, existing curated SOCIAL gap. Original rest/bone lengths retained. No skin/rest/skeleton/material/face/hair/finger changes.','timing':{'anticipation':[1,12],'raise':[13,31],'wave_two_cycles':[32,59],'hold':[60,67],'recovery':[68,91]},'max_joint_frame_step_m':maxstep,'minimum_hand_head_joint_distance_m':minimum_hand_head,'all91_body_vertices_finite':True,'OFF_signature_exact_before_save':True,'frames_private':rows,'finger_quality':'HOLD: unchanged source fingers; no finger-curl acceptance','self_intersection':'PENDING full source preview; joint distance not a mesh collision certificate','TierP':0,'visual_promotion':False}
with (O/'SOCIAL_WAVE_CANDIDATE_PRIVATE_R1.json').open('x',encoding='utf8') as f:json.dump(r,f,indent=2)
print('SOCIAL_WAVE_CANDIDATE_OFF_PASS',r['candidate_SHA'],flush=True)
