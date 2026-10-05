"""Read-only existing Walk input sampling; no export framework or source save."""
import bpy,sys,json,hashlib,math
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'b-pass1-existing-walk-consumer-r1';O.mkdir(exist_ok=False)
old=json.loads((B/'alpha-native-walk-source-r1/NATIVE_WALK_SOURCE_PRIVATE_R1.json').read_bytes())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
P=Path(old['candidate']);assert sha(P)==old['candidate_SHA']
bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False)
names=list(bpy.data.actions.keys());before=snapshot(names);s=bpy.context.scene
A=old['actions'];assert len(A)==3
def curves(a):return [fc for la in a.layers for st in la.strips for ba in st.channelbags for fc in ba.fcurves]
def channels(an):
 return [{'action':an,'path':f.data_path,'index':f.array_index,'keys':[{'frame':i,'value':float(f.evaluate(i))} for i in range(1,98)],'source_interpolation':sorted({k.interpolation for k in f.keyframe_points})} for f in curves(bpy.data.actions[an])]
def write(fn,v):(O/fn).write_text(json.dumps(v,separators=(',',':'),ensure_ascii=False),encoding='utf8')
bodyan=A['Meshy_Fitted_Rig'];bodychannels=channels(bodyan);assert len(bodychannels)==364
write('NativeWalkBody97.json',{'fps':24,'frameStart':1,'frameEnd':97,'channels':bodychannels})
for ob,fn in [('Armature','NativeWalkHead97.json'),('Hair_Rig_R4','NativeWalkHairTransport97.json')]:write(fn,{'fps':24,'frameStart':1,'frameEnd':97,'channels':channels(A[ob])})
extra={a.name:channels(a.name) for a in bpy.data.actions if 'WalkInPlace' in a.name and a.name!=old['source_action']}
write('OriginalWalkSemanticChannels97.json',{'fps':24,'frameStart':1,'frameEnd':97,'actions':extra,'warning':'Semantic FACE/GAZE/HAIR research reference. Single-owner integration; never double-drive roots or hair transport.'})
mapping={}
for ob in A:
 rig=bpy.data.objects[ob];mapping[ob]=[{'bone':p.name,'parent':p.parent.name if p.parent else None,'rest_parent_local_matrix':list(map(list,p.parent.bone.matrix_local.inverted()@p.bone.matrix_local if p.parent else p.bone.matrix_local)),'rest_scale':list(p.bone.matrix_local.to_scale())} for p in rig.pose.bones]
lanes=[]
for ob,an in A.items():ln=ReactionLane(ob);ln.on(an);lanes.append(ln)
rows=[]
for f in range(1,98):
 s.frame_set(f);bpy.context.view_layer.update();rigs={}
 for ob in A:
  rig=bpy.data.objects[ob];rr=[]
  for p in rig.pose.bones:
   local=p.parent.matrix.inverted()@p.matrix if p.parent else p.matrix
   loc,rot,scale=local.decompose();basloc,basrot,basscale=p.matrix_basis.decompose()
   vals=[*loc,*rot,*scale,*basloc,*basrot,*basscale];assert all(math.isfinite(x) for x in vals)
   rr.append({'bone':p.name,'local_position':list(loc),'local_rotation_xyzw':[rot.x,rot.y,rot.z,rot.w],'local_scale':list(scale),'basis_position':list(basloc),'basis_rotation_xyzw':[basrot.x,basrot.y,basrot.z,basrot.w],'basis_scale':list(basscale)})
  rigs[ob]=rr
 rows.append({'frame':f,'time':(f-1)/24,'rigs':rigs})
for ln in reversed(lanes):ln.off()
assert snapshot(names)==before;assert sha(P)==old['candidate_SHA'] and sha(old['source'])==old['source_SHA']
write('NativeWalkLocalTRS97.json',{'fps':24,'frameStart':1,'frameEnd':97,'coordinate_space':'Blender native right-handed meters, evaluated parent-local; quaternions xyzw. NOT Unity/world coordinates. For current Unity imported rest use native basis channels and its existing H reflection adapter.','mapping':mapping,'frames':rows})
files={p.name:{'path':str(p),'SHA256':sha(p),'bytes':p.stat().st_size} for p in O.glob('*.json')}
write('WALK_CONSUMER_SAMPLES_MANIFEST_R1.json',{'scope':'ONE existing original Walk, no new motion/export framework; Tier-C source-only','source_SHA':old['source_SHA'],'source_action':old['source_action'],'source_action_SHA':old['source_action_SHA'],'candidate_SHA':old['candidate_SHA'],'library_SHA':old['library']['sha256'],'actions':A,'action_signatures':{an:before['actions'][an] for an in A.values()},'files':files,'fps':24,'samples':97,'unique_loop_samples':96,'loop_seconds':4,'loop_duplicate_endpoint':97,'original81_OFF_full_signature_exact':True,'source_candidate_bytes_unchanged':True,'Unity_consumer_schema':'Existing O1OriginalFaceGazeIdlePartial.Recipe/Channel/Key. NativeWalkBody97 matches Talk116 channel schema; current bound_action expected name must be Walk-specific. No Unity implementation edit.','basis_adapter':'Current ApplyBodyBone: q Unity=(x,-y,-z,w), loc=(-x,y,z), localRotation=importedRestRotation*q, localPosition=restPosition+restMatrix.MultiplyVector(loc); scale=original rest. Do not treat pose basis as direct parent-local TRS.','root_motion':'In-place root world translation range0; external actor navigation; transport roots are not extra world locomotion.','ownership':'BODY/head/hair same clock, each channel one owner; FACE semantics separate overlay, do not double-bind Armature/Root or Hair_HeadRoot.','precision':'Foot/contact/seam TierP0 HOLD; no new precision QA','product_modified':False})
print('EXISTING_WALK_CONSUMER97_FINITE_SOURCE81_OFF_UNCHANGED',flush=True)
