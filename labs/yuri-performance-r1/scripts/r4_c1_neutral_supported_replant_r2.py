"""ONE R2 alternative: actual whole-sole world positions and a smooth canonical leg endpoint."""
import bpy,sys,json,hashlib,math
from pathlib import Path
import numpy as np
from mathutils import Vector,Quaternion
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_c1_contact_path_adapter_r1 import ReachFingerLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-c1-neutral-supported-replant-r2';O.mkdir(exist_ok=False)
def dump(n,d):(O/n).write_text(json.dumps(d,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
d=json.loads((B/'alpha-c1-neutral-supported-replant-r1/SUPPORTED_REPLANT_PRIVATE_R1.json').read_bytes());i=json.loads((B/'alpha-c1-neutral-bridge-inspect-r1/C1_NEUTRAL_TARGET_INSPECTION_PRIVATE_R1.json').read_bytes());P=Path(d['candidate']);assert sha(P)==d['candidate_SHA'] and sha(i['source'])==i['source_SHA'];bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered'];original=list(bpy.data.actions.keys());before=snapshot(original);raw={pb.name:pb.rotation_quaternion.copy() for pb in r.pose.bones};root=np.array(bpy.data.objects['Assembly_Root'].matrix_world)
def points(obj=body):
 e=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);w=np.array(e.matrix_world);v=v.reshape(-1,3).astype(np.float64)@w[:3,:3].T+w[:3,3];e.to_mesh_clear();return v
neutral={n:points(bpy.data.objects[n]) for n in ['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4']};sole={n:np.array(v,dtype=int) for n,v in i['sole_vertex_ids_private'].items()};floor=i['floor_source_world_z'];lane=ReachFingerLane();lane.on()
def bind_body(name):ad=r.animation_data;ad.action=bpy.data.actions[name];ad.action_slot=ad.action.slots[0]
for obj,name in d['additive_actions'].items():ad=bpy.data.objects[obj].animation_data;ad.action=bpy.data.actions[name];ad.action_slot=ad.action.slots[0]
baseline=[]
for f in range(1,62):s.frame_set(f);bpy.context.view_layer.update();baseline.append(hashlib.sha256(points().tobytes()).hexdigest())
end=points();grounded={n:ids[end[ids,2]<=floor+.002] for n,ids in sole.items()};legnames=[n+'.'+side for side in sole for n in ['thigh','shin','foot']];r1poses={};worst={}
# Cause comparison is limited to the single R1 worst97 and endpoint133, not broad branch research.
for f in range(62,134):
 s.frame_set(f);bpy.context.view_layer.update();r1poses[f]={n:r.pose.bones[n].rotation_quaternion.copy() for n in legnames}
 if f in [97,133]:
  v=points();worst[str(f)]={'sole_world_error_m':{n:float(np.linalg.norm(v[ids]-(end[ids] if f==97 and n=='R' else neutral[body.name][ids]),axis=1).max()) for n,ids in sole.items()},'body_source_component_error_m':float(np.max(np.abs(v-neutral[body.name])))}
oldbody=d['additive_actions'][r.name];a=bpy.data.actions[oldbody].copy();a.name='YURI_R4_C1_NEUTRAL_CONTACT_PATCH_BODY_R2';a.use_fake_user=True;a['source_fps']=30;a['hypothesis']='Same R1 sequential steps, actual sole world-vertex objective with native thigh/shin/foot9DOF; smooth tiny canonical leg correction during last12 settle frames';newbody=a.name;bind_body(newbody)
def ease(u):u=max(0,min(1,u));return u*u*u*(u*(u*6-15)+10)
rows=[];fail=[];jac_cache={};prev=end.copy();knee_prev=None
for t in range(1,73):
 f=61+t;s.frame_set(f);bpy.context.view_layer.update();rec={'frame':f,'sides':{}};settle=ease((t-60)/12)
 for side,ids in sole.items():
  phase=max(0,min(1,(t-6)/24 if side=='L' else (t-36)/24));blend=ease(phase);lift=.035*math.sin(math.pi*phase)**2
  goal=end[ids]*(1-blend)+neutral[body.name][ids]*blend;goal=goal.copy();goal[:,2]+=lift
  # Distributed whole-sole constraints include actual grounded patch AND ankle-edge cohorts.
  # During last12 frames, smooth the small R1 leg null-space residual toward known source pose.
  # The canonical pose is already an exact feasible end target; never post-solve snap it.
  bones=[r.pose.bones[n+'.'+side] for n in ['thigh','shin','foot']]
  for pb in bones:
   targetq=raw[pb.name].copy()
   if r1poses[f][pb.name].dot(targetq)<0:targetq.negate()
   pb.rotation_quaternion=targetq if settle==1 else r1poses[f][pb.name].slerp(targetq,settle)
  bpy.context.view_layer.update();jac=jac_cache.get(side);iterations=0
  def actual():return points()[ids]
  def cost(v):return float(np.mean((goal-v)**2))
  for it in range(5):
   current=actual();res=(goal-current).reshape(-1);mx=float(np.linalg.norm(goal-current,axis=1).max())
   if mx<.00035:break
   originals=[pb.rotation_quaternion.copy() for pb in bones]
   if jac is None or (t in [30,36,60] and it==0):
    jac=np.empty((len(res),9));eps=.001
    for k in range(9):
     pb=bones[k//3];axis=Vector(tuple(1 if j==k%3 else 0 for j in range(3)));pb.rotation_quaternion=originals[k//3]@Quaternion(axis,eps);bpy.context.view_layer.update();jac[:,k]=(actual()-current).reshape(-1)/eps;pb.rotation_quaternion=originals[k//3];bpy.context.view_layer.update()
   delta=np.linalg.solve(jac.T@jac+np.eye(9)*1e-6,jac.T@res);length=np.linalg.norm(delta)
   if length>.06:delta*=.06/length
   accepted=False
   for factor in [1,.5,.25]:
    for k,pb in enumerate(bones):
     v=Vector(delta[k*3:k*3+3]*factor);pb.rotation_quaternion=originals[k]@Quaternion(v.normalized(),v.length) if v.length>1e-10 else originals[k]
    bpy.context.view_layer.update();observed=actual()
    if cost(observed)<cost(current):accepted=True;break
   if not accepted:
    for pb,q in zip(bones,originals):pb.rotation_quaternion=q
    bpy.context.view_layer.update();break
   applied=delta*factor;change=(observed-current).reshape(-1);denom=float(applied@applied)
   if denom>1e-12:jac+=np.outer(change-jac@applied,applied)/denom
   iterations=it+1
  jac_cache[side]=jac;v=actual();error=float(np.linalg.norm(v-goal,axis=1).max());groundidx=np.nonzero(np.isin(ids,grounded[side]))[0];gerror=float(np.linalg.norm(v[groundidx]-goal[groundidx],axis=1).max())
  rec['sides'][side]={'phase_u':phase,'phase':'SWING' if 0<phase<1 else 'SUPPORT','clearance_m':lift,'whole_sole_world_constraint_max_error_m':error,'actual_grounded_patch_constraint_max_error_m':gerror,'iterations':iterations,'canonical_settle_weight':settle}
  if error>.003:fail.append({'frame':f,'side':side,'reason':'actual_whole_sole_world_constraint_over3mm','value_m':error})
  for pb in bones:pb.keyframe_insert('rotation_quaternion',frame=f,group=pb.name)
 v=points();assert np.isfinite(v).all();assert np.array_equal(root,np.array(bpy.data.objects['Assembly_Root'].matrix_world));rec['body_max_vertex_step_m']=float(np.linalg.norm(v-prev,axis=1).max());prev=v.copy();knee={side:r.matrix_world@r.pose.bones['shin.'+side].head for side in sole};rec['knee_steps_m']={side:(knee[side]-knee_prev[side]).length if knee_prev else 0 for side in sole};knee_prev={n:v.copy() for n,v in knee.items()}
 if max(rec['knee_steps_m'].values())>.030:fail.append({'frame':f,'reason':'knee_step_over30mm','value_m':max(rec['knee_steps_m'].values())})
 rec['feet_min_floor_offset_m']={side:float(v[ids,2].min()-floor) for side,ids in sole.items()};rows.append(rec);print('R2_CONTACT_PATCH_FRAME',f,{n:x['whole_sole_world_constraint_max_error_m'] for n,x in rec['sides'].items()},flush=True)
errors={n:float(np.max(np.abs(points(bpy.data.objects[n])-v))) for n,v in neutral.items()}
if any(e!=0 for e in errors.values()):fail.append({'reason':'endpoint_not_exact_source_neutral','geometry_component_error_m':errors})
# Validate actual adjacent end frame vertex displacements and every sampled contact, not only a final pose.
for la in a.layers:
 for st in la.strips:
  for ba in st.channelbags:
   for fc in ba.fcurves:
    for k in fc.keyframe_points:
     if k.co[0]>61:k.interpolation='LINEAR'
unchanged=True
for f in range(1,62):s.frame_set(f);bpy.context.view_layer.update();unchanged=unchanged and hashlib.sha256(points().tobytes()).hexdigest()==baseline[f-1]
assert unchanged;lane.off();assert snapshot(original)==before;out=O/'Character_R4_C1_NeutralContactPatch_EXPERIMENT_OFF_R2_20261004.blend';bpy.ops.wm.save_as_mainfile(filepath=str(out));assert sha(P)==d['candidate_SHA'] and sha(i['source'])==i['source_SHA'];actions={**d['additive_actions'],r.name:newbody};dump('SUPPORTED_REPLANT_PRIVATE_R2.json',{'task':'ROOT_PM_C1_REPLANT_R1_FAIL_NEXT_R2_R1','candidate':str(out),'candidate_SHA':sha(out),'candidate_bytes':out.stat().st_size,'source_SHA':i['source_SHA'],'R1_candidate_SHA_unchanged':d['candidate_SHA'],'R1_contact_causes_inspected_only97_133':worst,'hypothesis':'Same sequential R1 lift/transfer schedule and pelvis/body/head/hair; replace centroid/minZ three-scalar objective with actual sole whole-vertex world constraints through native thigh/shin/foot9DOF; smooth small leg-nullspace correction toward canonical source throughout12-frame settle; final frame not forced post-solve','additive_actions':actions,'new_body_action':newbody,'frame_range':[1,133],'source_scene_fps':24,'action_fps':30,'original_C1_frames1_61_exact':unchanged,'original_source_and_all_prior_actions_OFF_signature_exact':True,'R2_finger_action_unchanged':True,'root_exact_all_sampled':True,'frames_private':rows,'endpoint_geometry_component_error_m':errors,'last_adjacent_frame_actual_body_max_vertex_step_m':rows[-1]['body_max_vertex_step_m'],'failure_constraints':fail,'verdict':'FAIL_HOLD' if fail else 'CONTACT_AND_EXACT_NEUTRAL_STRUCTURAL_PASS_VISUAL_PENDING','normal_speed':'PENDING','TierP':0,'new_geometry_rig_skin_material_export_product_changes':False});print('R2_CONTACT_PATCH_RESULT',len(fail),errors,sha(out),flush=True)
