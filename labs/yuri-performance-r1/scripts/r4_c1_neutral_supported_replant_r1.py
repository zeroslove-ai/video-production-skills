"""ONE staged native-surface replant hypothesis, private failed candidates retained."""
import bpy,sys,json,hashlib,math
from pathlib import Path
import numpy as np
from mathutils import Vector,Quaternion,Matrix
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot
from r4_c1_contact_path_adapter_r1 import ReachFingerLane,BODY,TRANSPORT,ROOT
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-c1-neutral-supported-replant-r1';O.mkdir(exist_ok=False)
def dump(n,d):(O/n).write_text(json.dumps(d,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
i=json.loads((B/'alpha-c1-neutral-bridge-inspect-r1/C1_NEUTRAL_TARGET_INSPECTION_PRIVATE_R1.json').read_bytes());S=Path(i['source']);assert sha(S)==i['source_SHA'];bpy.ops.wm.open_mainfile(filepath=str(S),use_scripts=False)
s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered'];s.frame_set(1);bpy.context.view_layer.update();original=list(bpy.data.actions.keys());before=snapshot(original)
def points(obj=body):
 e=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);w=np.array(e.matrix_world);v=v.reshape(-1,3).astype(np.float64)@w[:3,:3].T+w[:3,3];e.to_mesh_clear();return v
neutral={n:points(bpy.data.objects[n]) for n in ['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4']};raw={pb.name:(pb.location.copy(),pb.rotation_quaternion.copy(),pb.scale.copy()) for pb in r.pose.bones};headref=r.matrix_world@r.pose.bones['head'].matrix
transref={n:bpy.data.objects[n].matrix_world@bpy.data.objects[n].pose.bones[bn].matrix for n,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]};transraw={n:(bpy.data.objects[n].pose.bones[bn].location.copy(),bpy.data.objects[n].pose.bones[bn].rotation_quaternion.copy()) for n,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]}
sole={n:np.array(v,dtype=int) for n,v in i['sole_vertex_ids_private'].items()};floor=i['floor_source_world_z'];targetfootq={n:(r.matrix_world@r.pose.bones['foot.'+n].matrix).to_quaternion() for n in sole}
def score(side,v=None):
 if v is None:v=points()
 idx=sole[side];return np.array([v[idx,0].mean(),v[idx,1].mean(),v[idx,2].min()-floor])
target={n:score(n,neutral[body.name]) for n in sole};root=np.array(bpy.data.objects['Assembly_Root'].matrix_world);lib=Path(i['action_library']);assert sha(lib)==i['action_library_SHA']
with bpy.data.libraries.load(str(lib),link=False) as (src,dst):dst.actions=list(src.actions)
for a in dst.actions:a.use_fake_user=True
reused=[a.name for a in dst.actions];oldactions=snapshot(reused)['actions'];lane=ReachFingerLane();lane.on();baseline=[]
for f in range(1,62):s.frame_set(f);bpy.context.view_layer.update();baseline.append(hashlib.sha256(points().tobytes()).hexdigest())
end={pb.name:(pb.location.copy(),pb.rotation_quaternion.copy(),pb.scale.copy()) for pb in r.pose.bones};endmesh=points();start={n:score(n,endmesh) for n in sole};endfootq={n:(r.matrix_world@r.pose.bones['foot.'+n].matrix).to_quaternion() for n in sole}
names=[]
for a in bpy.data.actions[BODY].layers:
 for st in a.strips:
  for ba in st.channelbags:
   for fc in ba.fcurves:
    if fc.data_path.startswith('pose.bones['):names.append(fc.data_path.split('"')[1])
names=sorted(set(names));assert all(n in raw for n in names)
new={}
for obj,old in {r.name:BODY,**TRANSPORT,'Assembly_Root':ROOT}.items():
 a=bpy.data.actions[old].copy();a.name=old+'_NEUTRAL_REPLANT_R1';a.use_fake_user=True;a['source_fps']=30;a['hypothesis']='One foot at a time L then R, actual evaluated sole centroid/floor solver; no rig or geometry changes';new[obj]=a.name;bpy.data.objects[obj].animation_data.action=a;bpy.data.objects[obj].animation_data.action_slot=a.slots[0]
def ease(u):u=max(0,min(1,u));return u*u*u*(u*(u*6-15)+10)
def keep_foot(side,wq):
 pb=r.pose.bones['foot.'+side];rel=pb.parent.bone.matrix_local.inverted()@pb.bone.matrix_local;pb.rotation_quaternion=rel.to_quaternion().inverted()@pb.parent.matrix.to_quaternion().inverted()@r.matrix_world.to_quaternion().inverted()@wq;bpy.context.view_layer.update()
prevq={n:r.pose.bones[n].rotation_quaternion.copy() for n in names};prevmesh=endmesh.copy();prevknee={side:r.matrix_world@r.pose.bones['shin.'+side].head for side in sole};rows=[];failures=[];jac_cache={};support_anchor={n:endmesh[ids].copy() for n,ids in sole.items()}
# Six support/weight-transfer frames, 24 L swing, six support switch, 24 R swing, 12 settle.
# Only one foot has nonzero clearance. Centroid COM shift is a pelvis recipe, not a dynamics certificate.
for t in range(1,73):
 f=61+t;s.frame_set(f);u=ease(t/72)
 for n in names:
  pb=r.pose.bones[n];a=end[n];z=raw[n];pb.location=a[0].lerp(z[0],u);pb.rotation_quaternion=a[1].slerp(z[1],u);pb.scale=a[2].lerp(z[2],u)
 pelvis=r.pose.bones['pelvis'];support_shift=-.018*math.sin(math.pi*min(1,t/36))**2 if t<=36 else .018*math.sin(math.pi*min(1,(t-36)/36))**2
 rel=pelvis.parent.bone.matrix_local.inverted()@pelvis.bone.matrix_local;world_to_local=(r.matrix_world@pelvis.parent.matrix@rel).inverted().to_3x3();pelvis.location+=world_to_local@Vector((support_shift,0,-.008*math.sin(math.pi*t/72)**2));bpy.context.view_layer.update()
 rec={'frame':f,'t':t,'pelvis_support_shift_world_m':support_shift,'sides':{}}
 for side in ['L','R']:
  phase=(t-6)/24 if side=='L' else (t-36)/24;phase=max(0,min(1,phase));blend=ease(phase);clear=.035*math.sin(math.pi*phase)**2;goal=start[side]*(1-blend)+target[side]*blend;goal[2]+=clear;wq=endfootq[side].slerp(targetfootq[side],blend)
  # Toe rotation is held during support, changed only with this foot's swing.
  toe=r.pose.bones['toe.'+side];toe.rotation_quaternion=end[toe.name][1].slerp(raw[toe.name][1],blend)
  bones=[r.pose.bones[n+'.'+side] for n in ['thigh','shin']]
  for pb in bones:pb.rotation_quaternion=prevq[pb.name].slerp(pb.rotation_quaternion,.15)
  bpy.context.view_layer.update();keep_foot(side,wq);jac=jac_cache.get(side);iterations=0
  for it in range(12):
   current=score(side);res=goal-current
   if np.linalg.norm(res)<.00020:break
   old=[pb.rotation_quaternion.copy() for pb in bones]
   if jac is None or it==6:
    jac=np.empty((3,6));eps=.001
    for k in range(6):
     pb=bones[k//3];axis=Vector(tuple(1 if j==k%3 else 0 for j in range(3)));pb.rotation_quaternion=old[k//3]@Quaternion(axis,eps);bpy.context.view_layer.update();keep_foot(side,wq);jac[:,k]=(score(side)-current)/eps;pb.rotation_quaternion=old[k//3];bpy.context.view_layer.update();keep_foot(side,wq)
   delta=jac.T@np.linalg.solve(jac@jac.T+np.eye(3)*1e-7,res);length=np.linalg.norm(delta)
   if length>.12:delta*=.12/length
   accepted=False
   for factor in [1,.5,.25]:
    for k,pb in enumerate(bones):
     vec=Vector(delta[k*3:k*3+3]*factor);pb.rotation_quaternion=old[k]@Quaternion(vec.normalized(),vec.length) if vec.length>1e-10 else old[k]
    bpy.context.view_layer.update();keep_foot(side,wq)
    if np.linalg.norm(goal-score(side))<np.linalg.norm(res):accepted=True;break
   if not accepted:
    for pb,q in zip(bones,old):pb.rotation_quaternion=q
    bpy.context.view_layer.update();keep_foot(side,wq);break
   applied=delta*factor;observed=score(side)-current;denom=applied@applied
   if denom>1e-12:jac+=np.outer(observed-jac@applied,applied)/denom
   iterations=it+1
  jac_cache[side]=jac;residual=float(np.linalg.norm(goal-score(side)))
  rec['sides'][side]={'phase':'SWING' if 0<phase<1 else 'SUPPORT','phase_u':phase,'clearance_m':clear,'actual_XY_minZ':score(side).tolist(),'goal_XY_minZ':goal.tolist(),'solver_residual_m':residual,'iterations':iterations}
  if residual>.003:failures.append({'frame':f,'side':side,'reason':'native_surface_solver_residual','value_m':residual})
 # Rigid face/hair transport via existing original roots, exact raw source properties at the target.
 bpy.context.view_layer.update();d=(r.matrix_world@r.pose.bones['head'].matrix)@headref.inverted();d=Matrix.LocRotScale(d.translation,d.to_quaternion(),Vector((1,1,1)))
 for obj,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]:
  o=bpy.data.objects[obj];pb=o.pose.bones[bn];basis=pb.bone.matrix_local.inverted()@(o.matrix_world.inverted()@d@transref[obj]);pb.location=basis.translation;pb.rotation_quaternion=basis.to_quaternion()
  if t==72:pb.location,pb.rotation_quaternion=transraw[obj]
  pb.keyframe_insert('location',frame=f,group=bn);pb.keyframe_insert('rotation_quaternion',frame=f,group=bn)
 bpy.context.view_layer.update();v=points();assert np.isfinite(v).all();assert np.array_equal(root,np.array(bpy.data.objects['Assembly_Root'].matrix_world))
 rec['body_max_vertex_step_m']=float(np.linalg.norm(v-prevmesh,axis=1).max());rec['knee_step_m']={};rec['support_contact_vertex_drift_m']={}
 for side,ids in sole.items():
  knee=r.matrix_world@r.pose.bones['shin.'+side].head;rec['knee_step_m'][side]=(knee-prevknee[side]).length;prevknee[side]=knee.copy()
  phase=rec['sides'][side]['phase_u']
  if phase==0:anchor=support_anchor[side]
  elif phase==1:
   if t==(30 if side=='L' else 60):support_anchor[side]=v[ids].copy()
   anchor=support_anchor[side]
  else:anchor=None
  if anchor is not None:
   drift=float(np.linalg.norm(v[ids]-anchor,axis=1).max());rec['support_contact_vertex_drift_m'][side]=drift
   if drift>.003:failures.append({'frame':f,'side':side,'reason':'support_surface_shape_or_vertex_drift','value_m':drift})
  if rec['knee_step_m'][side]>.030:failures.append({'frame':f,'side':side,'reason':'knee_step_over30mm','value_m':rec['knee_step_m'][side]})
 for n in names:
  pb=r.pose.bones[n];q=pb.rotation_quaternion
  if q.dot(prevq[n])<0:q.negate()
  prevq[n]=q.copy();pb.keyframe_insert('location',frame=f,group=n);pb.keyframe_insert('rotation_quaternion',frame=f,group=n);pb.keyframe_insert('scale',frame=f,group=n)
 prevmesh=v.copy();rows.append(rec);print('SUPPORTED_REPLANT_FRAME',f,rec['sides']['L']['solver_residual_m'],rec['sides']['R']['solver_residual_m'],flush=True)
# Never force a target snap. The solved endpoint itself must equal the original raw neutral.
errors={n:float(np.max(np.abs(points(bpy.data.objects[n])-v))) for n,v in neutral.items()};posegap={n:float(raw[n][1].rotation_difference(r.pose.bones[n].rotation_quaternion).angle) for n in names}
if any(e>1e-7 for e in errors.values()):failures.append({'reason':'solved_endpoint_not_exact_source_neutral','geometry_component_error_m':errors})
for obj in new:
 for la in bpy.data.actions[new[obj]].layers:
  for st in la.strips:
   for ba in st.channelbags:
    for fc in ba.fcurves:
     for k in fc.keyframe_points:
      if k.co[0]>61:k.interpolation='LINEAR'
unchanged=True
for f in range(1,62):s.frame_set(f);bpy.context.view_layer.update();unchanged=unchanged and hashlib.sha256(points().tobytes()).hexdigest()==baseline[f-1]
assert unchanged;lane.off();assert snapshot(original)==before;assert snapshot(reused)['actions']==oldactions;P=O/'Character_R4_C1_NeutralReplant_EXPERIMENT_OFF_R1_20261004.blend';bpy.ops.wm.save_as_mainfile(filepath=str(P));assert sha(S)==i['source_SHA']
dump('SUPPORTED_REPLANT_PRIVATE_R1.json',{'task':'ROOT_PM_NEUTRAL_CONTACT_BOUNDARY_R1','source_SHA':sha(S),'candidate':str(P),'candidate_SHA':sha(P),'candidate_bytes':P.stat().st_size,'additive_actions':new,'frame_range':[1,133],'reaction_original_frames1_61_exact':unchanged,'unchanged_R2_finger_action':True,'source_scene_fps':24,'action_fps':30,'hypothesis':'L lift/replant t6..30 while R supported; R lift/replant t36..60 while L supported; pelvis shift18mm/support lowering8mm; actual surface-centroid dampedJacobian solver reused with12 iterations, warm-start and .12rad step clamp; toe/worldfoot orientation changes ONLY swing. 12frames settle, never forced raw-pose snap.','world_root_exact_all_sampled':True,'OFF_signature_exact':True,'original_and_reused_actions_unchanged':True,'endpoint_geometry_component_error_m':errors,'endpoint_native_rotation_gap_rad':posegap,'frames_private':rows,'failure_constraints':failures,'verdict':'FAIL_HOLD' if failures else 'STRUCTURAL_CANDIDATE_PENDING_VISUAL','TierP':0,'visual_normal_speed':'NOT_RUN pending constraints','actual_dependency_if_failed':'Centroid+minZ three scalar constraints with thigh/shin rotations do not guarantee a rigid planted sole surface or restore the canonical leg null-space pose. Exact neutral requires contact-patch/orientation and branch/pose constraints beyond this reused solver; no rig/skin changes authorized.'})
print('SUPPORTED_REPLANT_RESULT',len(failures),errors,sha(P),flush=True)
