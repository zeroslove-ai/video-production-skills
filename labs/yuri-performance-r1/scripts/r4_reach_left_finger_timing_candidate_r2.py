"""C1 body exact versus transient finger-only NLA; source-only laterality defect proof."""
import bpy,sys,json,hashlib
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot
from r4_reach_left_finger_timing_adapter_r2 import ReachFingerLane,BODY,FINGER,TRANSPORT,ROOT
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-reach-left-finger-timing-candidate-r2';O.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();c=json.loads((B/'alpha-c1-reach-candidate-r1/C1_REACH_CANDIDATE_PRIVATE_R1.json').read_bytes());h=json.loads((B/'alpha-hand-relax-candidate-r1/HAND_RELAX_CANDIDATE_PRIVATE_R1.json').read_bytes());S=Path(c['source']);assert sha(S)==c['source_SHA']==h['source_SHA'];assert sha(c['candidate'])==c['candidate_SHA'] and sha(h['candidate'])==h['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=str(S),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered'];original=list(bpy.data.actions.keys());before=snapshot(original);(O/'SOURCE_SIGNATURE_PRIVATE_R1.json').write_text(json.dumps(before),encoding='utf8')
inputs=[B/'alpha-c1-reach-off-qa-r1/YURI_R4_C1_REACH_ACTIONS_ONLY_R1.blend',B/'alpha-reach-left-finger-off-qa-r1/YURI_R4_REACH_LEFT_FINGER_ACTIONS_ONLY_R1.blend'];input_receipts=[]
for p in inputs:
 with bpy.data.libraries.load(str(p),link=False) as (src,dst):assert not src.objects and not src.meshes and not src.armatures;dst.actions=list(src.actions)
 for action in dst.actions:action.use_fake_user=True
 input_receipts.append({'file':str(p),'SHA':sha(p)})
# Read actual original left rest axes/parents/weights; no Euler sign copying.
from mathutils import Vector,Quaternion
from r4_appearance_adapter import ReactionLane
import math
RIGHT='YURI_R4_HAND_RELAX_PREGRASP_FINGERS_R1';PREVIOUS='YURI_R4_C1_LEFT_PREGRASP_FINGERS_R1';reused=[BODY,RIGHT,PREVIOUS,*TRANSPORT.values(),ROOT];reused_signature=snapshot(reused)['actions']
left_names=[n.replace('.R','.L') for n in h['authored_bones']];h['authored_bones']=left_names
left_inventory={n:{'parent':r.pose.bones[n].parent.name,'rest_matrix':[list(row) for row in r.data.bones[n].matrix_local],'constraints':[x.type for x in r.pose.bones[n].constraints],'deform':r.data.bones[n].use_deform,'weighted_vertices':sum(any(g.group==body.vertex_groups[n].index and g.weight>0 for g in v.groups) for v in body.data.vertices)} for n in left_names}
assert all(x['deform'] and not x['constraints'] and x['weighted_vertices']>0 for x in left_inventory.values())
width=(r.pose.bones['pinky1.L'].head-r.pose.bones['index1.L'].head).normalized();long=(r.pose.bones['middle3.L'].tail-r.pose.bones['middle1.L'].head).normalized();palm=long.cross(width).normalized()
if palm.x>0:palm.negate()
assert palm.x<0
axes={n:r.pose.bones[n].matrix.to_quaternion().inverted()@(r.pose.bones[n].matrix.to_3x3().col[1].normalized().cross(palm).normalized()) for n in left_names};rest={n:r.pose.bones[n].matrix_basis.copy() for n in left_names};initial_tips={digit:r.pose.bones[digit+'3.L'].tail.copy() for digit in ['index','middle','ring','pinky','thumb']}
a=bpy.data.actions.new(FINGER);a.use_fake_user=True;a['source_fps']=30;a['lineage']='Timing-only R2: same native axes/strength/onset as R1, peak31 hold32, release33..44; exact open45..61 before prior return intersections51..55; previous Actions unchanged';a.slots.new(id_type='OBJECT',name=r.name);author=ReactionLane();author.on(FINGER)
def ease(t):t=max(0,min(1,t));return t*t*t*(t*(t*6-15)+10)
def envelope(f,delay):
 if f<=11+delay:return 0
 if f<=27+delay:return ease((f-11-delay)/16)
 if f<=32:return 1
 return 1-ease((f-32)/12)
for f in range(1,62):
 s.frame_set(f)
 for digit in ['index','middle','ring','pinky','thumb']:
  delay={'index':0,'middle':1,'ring':2,'pinky':3,'thumb':4}[digit];strength={'index':.92,'middle':1,'ring':1.04,'pinky':.90,'thumb':1}[digit];degrees=[4,6,4] if digit=='thumb' else [12,18,10]
  for j,deg in enumerate(degrees,1):
   n=f'{digit}{j}.L';pb=r.pose.bones[n];pb.rotation_mode='QUATERNION';pb.rotation_quaternion=(rest[n]@Quaternion(axes[n],math.radians(deg)*strength*envelope(f,delay)).to_matrix().to_4x4()).to_quaternion();pb.keyframe_insert('rotation_quaternion',frame=f,group=n)
 bpy.context.view_layer.update()
 if f==31:inward={digit:(r.pose.bones[digit+'3.L'].tail-initial_tips[digit]).dot(palm)*r.matrix_world.to_scale().x for digit in initial_tips}
assert all(inward[n]>0 for n in ['index','middle','ring','pinky'])
for la in a.layers:
 for st in la.strips:
  for ba in st.channelbags:
   for fc in ba.fcurves:
    for k in fc.keyframe_points:k.interpolation='LINEAR'
author.off();assert snapshot(original)==before and snapshot(reused)['actions']==reused_signature
added=[BODY,FINGER,RIGHT,PREVIOUS,*TRANSPORT.values(),ROOT];action_signatures=snapshot(added)['actions']
def curves(a):return [fc for la in a.layers for st in la.strips for ba in st.channelbags for fc in ba.fcurves]
body_paths=sorted(set(fc.data_path for fc in curves(bpy.data.actions[BODY])));finger_paths=sorted(set(fc.data_path for fc in curves(bpy.data.actions[FINGER])));assert set(body_paths).isdisjoint(finger_paths);assert len(finger_paths)==15 and all('rotation_quaternion' in p and any('"'+n+'"' in p for n in h['authored_bones']) for p in finger_paths)
def meshpoints():
 e=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);e.to_mesh_clear();return v.reshape(-1,3)
source_neutral=meshpoints().copy();base=[];lane=ReachFingerLane();lane.on(include_fingers=False)
for f in range(1,62):
 s.frame_set(f);bpy.context.view_layer.update();base.append({'matrices':{b.name:np.array(r.matrix_world@b.matrix) for b in r.pose.bones if b.name not in h['authored_bones']},'carrier':np.array(bpy.data.objects['Assembly_Root'].matrix_world),'face_root':np.array(bpy.data.objects['Armature'].matrix_world@bpy.data.objects['Armature'].pose.bones['Root'].matrix),'hair_root':np.array(bpy.data.objects['Hair_Rig_R4'].matrix_world@bpy.data.objects['Hair_Rig_R4'].pose.bones['Hair_HeadRoot'].matrix)})
 if f==1:start_body=meshpoints().copy()
 if f==61:end_body=meshpoints().copy()
lane.off();assert snapshot(original)==before
rows=[];errmax=0;lane=ReachFingerLane();lane.on();last=None;skin_step=0
for f in range(1,62):
 s.frame_set(f);bpy.context.view_layer.update();err=max(float(np.max(np.abs(np.array(r.matrix_world@r.pose.bones[n].matrix)-m))) for n,m in base[f-1]['matrices'].items());errmax=max(errmax,err);assert err==0
 for key,obj,bone in [('face_root','Armature','Root'),('hair_root','Hair_Rig_R4','Hair_HeadRoot')]:assert np.array_equal(base[f-1][key],np.array(bpy.data.objects[obj].matrix_world@bpy.data.objects[obj].pose.bones[bone].matrix))
 assert np.array_equal(base[f-1]['carrier'],np.array(bpy.data.objects['Assembly_Root'].matrix_world));v=meshpoints();assert np.isfinite(v).all()
 if last is not None:skin_step=max(skin_step,float(np.linalg.norm(v-last,axis=1).max())*body.matrix_world.to_scale().x)
 last=v.copy();rows.append({'frame':f,'finger_source_frame':f,'nonfinger_world_matrix_error':err,'finger_quaternions':{n:list(r.pose.bones[n].rotation_quaternion) for n in h['authored_bones']},'left_hand_world':{'wrist':list(r.matrix_world@r.pose.bones['hand.L'].head),'tips':{digit:list(r.matrix_world@r.pose.bones[digit+'3.L'].tail) for digit in ['index','middle','ring','pinky','thumb']}}})
 if f==1:composed_start=v.copy()
 if f==61:composed_end=v.copy()
endpoint=float(np.max(np.abs(composed_end-composed_start)));existing_endpoint=float(np.max(np.abs(end_body-start_body)));neutral_endpoint=float(np.max(np.abs(composed_end-source_neutral)));lane.off();assert snapshot(original)==before and snapshot(added)['actions']==action_signatures
P=O/'Character_R4_ReachLeftFingerTiming_CANDIDATE_OFF_R2_20261004.blend';bpy.ops.wm.save_as_mainfile(filepath=str(P));assert sha(S)==c['source_SHA'];d={'task':'ROOT_PM_SAME_HAND_CAUSAL_NEXT_TIMING_R1','source':str(S),'source_SHA':sha(S),'candidate':str(P),'candidate_SHA':sha(P),'candidate_bytes':P.stat().st_size,'frames':[1,61],'source_fps':30,'source_scene_fps':24,'movie_duration_sec':61/30,'original_actions_preserved':len(original),'additive_body_actions':{'Meshy_Fitted_Rig':BODY,**TRANSPORT,'Assembly_Root':ROOT},'finger_action':FINGER,'authored_bones':h['authored_bones'],'lineage_inputs':input_receipts,'existing_C1_candidate_SHA':c['candidate_SHA'],'existing_hand_candidate_SHA':h['candidate_SHA'],'ownership':{'active_body_Action':BODY,'body_paths':body_paths,'NLA_finger_Action':FINGER,'finger_paths':finger_paths,'overlap_paths':[],'clock':'body C1 and new LEFT finger Action both frames1..61 at30fps; NLA scale1 REPLACE disjoint channels; existing transport/carrier clock unchanged'},'existing_actions_curve_signatures_unchanged':True,'existing_action_signatures':action_signatures,'all61_evaluated_body_vertices_finite':True,'nonfinger_C1_same_time_world_matrix_max_error':errmax,'face_hair_root_carrier_same_time_exact':True,'composition_start_end_body_local_error_m':endpoint,'existing_C1_start_end_body_local_error_m':existing_endpoint,'composition_end_vs_original_neutral_local_error_m':neutral_endpoint,'maximum_evaluated_vertex_frame_step_world_m':skin_step,'OFF_signature_exact_before_save':True,'frames_private':rows,'preserved_right_finger_action':RIGHT,'preserved_previous_left_finger_action':PREVIOUS,'timing_only_change':{'curl':'12..31 unchanged','peak_hold':[31,32],'release':[33,44],'exact_open':[45,61],'previous_release':[39,57]},'left_finger_inventory_private':left_inventory,'left_finger_axes_private':{n:list(v) for n,v in axes.items()},'actual_source_tip_inward_motion_m':inward,'semantic_defects':['Return endpoint equals existing C1 start pose, not original R4 neutral. Original neutral is restored only by OFF(). Existing body curves cannot be altered under current scope.'],'source_status':'SAME_HAND_SOURCE_COMPOSITION_NEUTRAL_CONTACT_HOLD','prop_contact_physics_Unity_MUG':'HOLD','TierP':0,'new_derived_motion_curve_actions':1};(O/'REACH_LEFT_FINGER_TIMING_CANDIDATE_PRIVATE_R2.json').write_text(json.dumps(d,indent=2),encoding='utf8');print('REACH_FINGER_COMPOSITION_DONE',d['candidate_SHA'],errmax,endpoint,neutral_endpoint,flush=True)
