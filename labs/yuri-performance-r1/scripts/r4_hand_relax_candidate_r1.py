"""One right finger-only source R4 open/curl/release Action; no rig/skin change."""
import bpy,sys,json,hashlib,math
from pathlib import Path
from mathutils import Vector,Quaternion
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-hand-relax-candidate-r1';O.mkdir(exist_ok=False)
S=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/target-reference/Character_Master_NeckSkin_R4.blend');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(S)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
bpy.ops.wm.open_mainfile(filepath=str(S),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered'];original=list(bpy.data.actions.keys());before=snapshot(original);(O/'SOURCE_SIGNATURE_PRIVATE_R1.json').write_text(json.dumps(before),encoding='utf8')
fingers=['index','middle','ring','pinky','thumb'];names=[f'{n}{j}.R' for n in fingers for j in [1,2,3]];fixed={b.name:(r.matrix_world@b.matrix).copy() for b in r.pose.bones if b.name not in names};rest={n:r.pose.bones[n].matrix_basis.copy() for n in names}
width=(r.pose.bones['pinky1.R'].head-r.pose.bones['index1.R'].head).normalized();long=(r.pose.bones['middle3.R'].tail-r.pose.bones['middle1.R'].head).normalized();palm=long.cross(width).normalized();assert palm.x>0
axes={n:r.pose.bones[n].matrix.to_quaternion().inverted()@(r.pose.bones[n].matrix.to_3x3().col[1].normalized().cross(palm).normalized()) for n in names};a=bpy.data.actions.new('YURI_R4_HAND_RELAX_PREGRASP_FINGERS_R1');a.use_fake_user=True;a['source_fps']=30;a['lineage']='Authored original-R4 native finger-only gentle curl; no donor or prop';a.slots.new(id_type='OBJECT',name=r.name);lane=ReactionLane();lane.on(a.name)
def ease(t):t=max(0,min(1,t));return t*t*t*(t*(t*6-15)+10)
def envelope(f,delay):
 if f<=15+delay:return 0
 if f<=48+delay:return ease((f-15-delay)/33)
 if f<=69:return 1
 return 1-ease((f-69)/36)
rows=[];fixedmax=0;last=None;maxstep=0;endpoint=None;skinmax=0;baseline=None
for f in range(1,106):
 s.frame_set(f)
 for digit in fingers:
  delay={'index':0,'middle':1,'ring':2,'pinky':3,'thumb':4}[digit];strength={'index':.92,'middle':1,'ring':1.04,'pinky':.90,'thumb':1}[digit];degrees=[4,6,4] if digit=='thumb' else [12,18,10]
  for j,deg in enumerate(degrees,1):
   n=f'{digit}{j}.R';pb=r.pose.bones[n];q=(rest[n]@Quaternion(axes[n],math.radians(deg)*strength*envelope(f,delay)).to_matrix().to_4x4()).to_quaternion();pb.rotation_mode='QUATERNION';pb.rotation_quaternion=q;pb.keyframe_insert('rotation_quaternion',frame=f,group=n)
 bpy.context.view_layer.update();err=max(max(abs((r.matrix_world@r.pose.bones[n].matrix)[i][j]-m[i][j]) for i in range(4) for j in range(4)) for n,m in fixed.items());fixedmax=max(fixedmax,err);assert err==0
 e=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();buf=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',buf);assert np.isfinite(buf).all();e.to_mesh_clear()
 if baseline is None:baseline=buf.copy()
 skinmax=max(skinmax,float(np.linalg.norm((buf-baseline).reshape(-1,3),axis=1).max())*body.matrix_world.to_scale().x)
 if f==105:endpoint=float(np.max(np.abs(buf-baseline)))
 tips={digit:list(r.matrix_world@r.pose.bones[digit+'3.R'].tail) for digit in fingers}
 if last:maxstep=max(maxstep,max((Vector(tips[n])-Vector(last[n])).length for n in fingers))
 last=tips;rows.append({'frame':f,'tips_world':tips,'fixed_nonfinger_world_matrix_error':err})
for layer in a.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    for k in fc.keyframe_points:k.interpolation='LINEAR'
lane.off();assert snapshot(original)==before
P=O/'Character_R4_HandRelax_CANDIDATE_OFF_R1_20261004.blend';bpy.ops.wm.save_as_mainfile(filepath=str(P));assert sha(S)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
d={'source':str(S),'source_SHA':sha(S),'candidate':str(P),'candidate_SHA':sha(P),'candidate_bytes':P.stat().st_size,'frames':[1,105],'source_fps':30,'source_scene_fps':24,'movie_duration_sec':3.5,'original_actions_preserved':len(original),'additive_body_actions':{'Meshy_Fitted_Rig':a.name},'authored_bones':names,'frames_private':rows,'palm_inward_rig_axis':list(palm),'axes_local_private':{n:list(v) for n,v in axes.items()},'timing':{'source_open':[1,15],'curl_stagger':[16,52],'gentle_pregrasp_hold':[53,69],'release_to_source_open':[70,105]},'fixed_nonfinger_world_matrix_error':fixedmax,'all105_body_vertices_finite':True,'skin_max_world_motion_m':skinmax,'endpoint_evaluated_body_error_local_m':endpoint,'maximum_fingertip_frame_step_m':maxstep,'OFF_signature_exact_before_save':True,'lineage':'Procedural right finger-only palm-plane curl on original existing bones. Earlier GameRig axis method inspected but no geometry/axis values copied. Source 13 finger-channel Actions preserved, not appended donor. Original source open pose used as relaxed-open endpoint. No palm/wrist approach or prop contact claim.','hand_quality':'PENDING actual multiview full playback','TierP':0,'visual_promotion':False,'prop_contact_physics_Unity_MUG':'HOLD'}
(O/'HAND_RELAX_CANDIDATE_PRIVATE_R1.json').write_text(json.dumps(d,indent=2),encoding='utf8');print('HAND_RELAX_FINGER_ONLY_PASS',d['candidate_SHA'],fixedmax,endpoint,skinmax,flush=True)
