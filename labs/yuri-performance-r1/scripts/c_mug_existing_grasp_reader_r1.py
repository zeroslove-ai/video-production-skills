"""Existing native consumer reader; scalar phase/hand anchor, no new motion or save."""
import bpy,sys,json,hashlib,math
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
from r4_native_grasp_adapter_r1 import NativeGraspLane,ACTIONS
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'c-mug-existing-grasp-reader-r1';O.mkdir(exist_ok=False)
old=json.loads((B/'alpha-native-grasp-candidate-r1b/NATIVE_GRASP_CANDIDATE_PRIVATE_R1B.json').read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();P=Path(old['candidate']);assert sha(P)==old['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);names=list(bpy.data.actions.keys());before=snapshot(names);s=bpy.context.scene
def curves(an):return [f for la in bpy.data.actions[an].layers for st in la.strips for ba in st.channelbags for f in ba.fcurves]
def channels(an):return [{'action':an,'path':f.data_path,'index':f.array_index,'keys':[{'frame':i,'value':float(f.evaluate(i))} for i in range(1,170)],'interpolation':sorted({k.interpolation for k in f.keyframe_points})} for f in curves(an)]
def write(n,x):(O/n).write_text(json.dumps(x,separators=(',',':')),encoding='utf8')
for ob,an in ACTIONS.items():write(('NativeGraspBody169' if ob=='Meshy_Fitted_Rig' else 'NativeGraspHead169' if ob=='Armature' else 'NativeGraspHairTransport169')+'.json',{'fps':24,'frameStart':1,'frameEnd':169,'channels':channels(an)})
assert len(curves(ACTIONS['Meshy_Fitted_Rig']))==294
mapping={ob:[{'bone':p.name,'parent':p.parent.name if p.parent else None,'rest_parent_local':list(map(list,p.parent.bone.matrix_local.inverted()@p.bone.matrix_local if p.parent else p.bone.matrix_local))} for p in bpy.data.objects[ob].pose.bones] for ob in ACTIONS}
ln=NativeGraspLane();ln.on();rows=[];r=bpy.data.objects['Meshy_Fitted_Rig'];bone_names=old['selected_upper_and_finger_bones'];digit_names={side:[n for n in bone_names if n.endswith('.'+side) and n.startswith(('index','middle','ring','pinky','thumb'))] for side in ['L','R']};rest={n:r.pose.bones[n].rotation_quaternion.copy() for n in bone_names}
from mathutils import Vector
for f in range(1,170):
 s.frame_set(f);bpy.context.view_layer.update();rigs={}
 for ob in ACTIONS:
  rr=[]
  for p in bpy.data.objects[ob].pose.bones:
   m=p.parent.matrix.inverted()@p.matrix if p.parent else p.matrix;l,q,z=m.decompose();bl,bq,bs=p.matrix_basis.decompose();assert all(math.isfinite(v) for v in [*l,*q,*z,*bl,*bq,*bs]);rr.append({'bone':p.name,'parentLocalPosition':list(l),'parentLocalRotationXYZW':[q.x,q.y,q.z,q.w],'parentLocalScale':list(z),'basisPosition':list(bl),'basisRotationXYZW':[bq.x,bq.y,bq.z,bq.w],'basisScale':list(bs)})
  rigs[ob]=rr
 hands={}
 for side in ['L','R']:
  pb=r.pose.bones['hand.'+side];world=r.matrix_world@pb.matrix;offset=Vector((0,pb.bone.length*.5,0));hands[side]={'wristWorld':list(world.translation),'palmMidpointHandLocal':list(offset),'palmMidpointWorld':list(world@offset),'handWorldMatrix':list(map(list,world)),'digitClosureRadiansSum':sum(rest[n].rotation_difference(r.pose.bones[n].rotation_quaternion).angle for n in digit_names[side])}
 rows.append({'frame':f,'seconds':(f-1)/24,'rigs':rigs,'hands':hands})
ln.off();assert snapshot(names)==before and sha(P)==old['candidate_SHA'] and sha(old['source'])==old['source_SHA']
# Equality of authored native channels identifies static hold; no smoothing/retiming.
allc=channels(ACTIONS['Meshy_Fitted_Rig']);values=[[c['keys'][f-1]['value'] for c in allc] for f in range(1,170)];changes=[max(abs(a-b) for a,b in zip(values[i],values[i-1])) for i in range(1,169)]
static=[];start=None
for i,d in enumerate(changes,start=2):
 if d<=1e-8 and start is None:start=i-1
 if d>1e-8 and start is not None:
  if i-start>=4:static.append([start,i-1])
  start=None
if start is not None:static.append([start,169])
digit={side:[x['hands'][side]['digitClosureRadiansSum'] for x in rows] for side in ['L','R']};peak=max(digit['L']);hold=max(static,key=lambda x:x[1]-x[0]);h=rows[hold[0]-1]
phase={'static_native_channel_ranges':static,'central_hold_frames':hold,'recommended_grasp_frame':hold[0],'recommended_release_start_frame':hold[1]+1,'reach_before_hold':[1,hold[0]],'return_release_after_hold':[hold[1],169],'finger_closure_first_nonzero_frame':next((i+1 for i,x in enumerate(digit['L']) if x>1e-6),None),'finger_closure_last_nonzero_frame':max(i+1 for i,x in enumerate(digit['L']) if x>1e-6),'left_digit_max_radians_sum':peak,'right_digit_max_radians_sum':max(digit['R']),'fingers_neutral_endpoints':digit['L'][0]<1e-6 and digit['L'][-1]<1e-6,'right_wrist_world_max_component_motion_m':max(max(abs(x-y) for x,y in zip(row['hands']['R']['wristWorld'],rows[0]['hands']['R']['wristWorld'])) for row in rows),'left_hand_hold_anchor':h['hands']['L'],'anchor_definition':'Provisional palm midpoint in hand.L local +Y half bone length; NOT fitted mug handle/contact center. Runtime writer aligns actual handle socket, applies attach at start hold and releases before retreat. No source transform/mesh changes.'}
write('GRASP_PHASE_ANCHOR_PRIVATE_R1.json',phase);write('NativeGraspLocalTRS169.json',{'fps':24,'frameStart':1,'frameEnd':169,'coordinate_space':'Blender right-handed meters/quaternionXYZW; basis fields are native rest delta, not direct Unity local','mapping':mapping,'frames':rows})
files={p.name:{'path':str(p),'SHA':sha(p),'bytes':p.stat().st_size} for p in O.glob('*.json')}
write('MUG_GRASP_CONSUMER_MANIFEST_R1.json',{'source_SHA':old['source_SHA'],'source_action_SHA':old['source_action_SHA'],'candidate_SHA':old['candidate_SHA'],'actions':ACTIONS,'original81_OFF_signature_exact':True,'source_candidate_bytes_unchanged':True,'fps':24,'frame_range':[1,169],'key_interval_seconds':7,'body_channels':294,'upper_and_digit_bones':42,'hand':'LEFT','files':files,'consumer':'Existing Talk/native Recipe Channel(action,path,index,keys(frame,value)); same ApplyBodyBone reflected basis/rest. No consumer code edited. BODY294 upper42 only; lower/root remain current provider. HEAD/HAIR transports one clock, no double root writers.','phase_scalar':{k:v for k,v in phase.items() if k!='left_hand_hold_anchor'},'TierP':0,'precision':'Finger webbing/thumb/prop contact/fidelity PASS2 HOLD; no new precision checks','new_motion':False,'new_export_framework':False})
print('C_MUG_EXISTING_GRASP_READER_SOURCE_OFF_IDENTICAL',phase['central_hold_frames'],phase['finger_closure_first_nonzero_frame'],flush=True)
