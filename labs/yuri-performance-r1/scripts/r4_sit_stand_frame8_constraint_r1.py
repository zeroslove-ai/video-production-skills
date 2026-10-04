"""One native joint-pose discriminator. No geometry/weight/rest modifications."""
import bpy,sys,json,hashlib,ast,gzip,math,time
from pathlib import Path
import numpy as np
from mathutils import Matrix,Vector,Quaternion
from mathutils.bvhtree import BVHTree
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
from r4_sit_stand_adapter_r1 import SitStandLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');P=B/'alpha-sit-stand-source-candidate-r1';O=B/'alpha-sit-stand-frame8-constraint-r1';O.mkdir(exist_ok=False)
m=json.loads((P/'SIT_STAND_SOURCE_PRIVATE_R1.json').read_bytes());i=json.loads((B/'alpha-sit-stand-source-intake-r1/SIT_STAND_SOURCE_INTAKE_PRIVATE_R1.json').read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(m['source'])==m['source_SHA'] and sha(m['candidate'])==m['candidate_SHA'] and sha(m['library']['file'])==m['library']['sha256']
bpy.ops.wm.open_mainfile(filepath=m['source'],use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];names=list(bpy.data.actions.keys());before=snapshot(names)
assert before==m['original78_signature_private']
for fn,defs in [('r4_native_walk_source_supply_r1.py',['contact']),('r4_existing_reach_contact_closure_r1.py',['geom'])]:
 tree=ast.parse((H/fn).read_text(encoding='utf8'));exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in defs],type_ignores=[]),'<pinned_actual_mesh_helpers>','exec'))
fixed={};mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4'];body=bpy.data.objects[mesh_names[0]]
def evaluate():return {n:geom(bpy.data.objects[n]) for n in mesh_names}
neutral=evaluate();basepairs,_=contact(neutral);v0=neutral[mesh_names[0]][0];floor=float(v0[:,2].min());gn={g.index:g.name for g in body.vertex_groups}
footids={q:np.array([v.index for v in body.data.vertices if sum(g.weight for g in v.groups if gn[g.group] in ['foot.'+q,'toe.'+q])>.5],int) for q in ['L','R']};patch={q:ids[v0[ids,2]<=floor+.003] for q,ids in footids.items()}
offquat={b.name:b.rotation_quaternion.copy() for b in r.pose.bones};refhead=r.matrix_world@r.pose.bones['head'].matrix;refs={ob:bpy.data.objects[ob].matrix_world@bpy.data.objects[ob].pose.bones[bn].matrix for ob,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]}
forward={}
for q in ['L','R']:
 d=(r.matrix_world@r.pose.bones['toe.'+q].head)-(r.matrix_world@r.pose.bones['foot.'+q].head);d.z=0;forward[q]=np.array(d.normalized());assert np.linalg.norm(forward[q])>.9
with bpy.data.libraries.load(m['library']['file'],link=False) as (src,dst):dst.actions=src.actions
oldlane=SitStandLane();oldlane.on();s.frame_set(8);bpy.context.view_layer.update()
old=evaluate();oldpairs,_=contact(old);oldposes={b.name:(b.location.copy(),b.rotation_quaternion.copy(),b.scale.copy()) for b in r.pose.bones};oldjoints={n:np.array(r.matrix_world@r.pose.bones[n].head) for n in ['pelvis']+[b+'.'+q for q in ['L','R'] for b in ['thigh','shin','foot']]}
frozen=json.loads(gzip.open(P/'SIT_STAND_TRIANGLE_IDENTITIES_PRIVATE_R1.json.gz','rt',encoding='utf8').read());original18={tuple(tuple(t) for t in pair) for pair in next(x for x in frozen['frames'] if x['frame']==8)['new_pair_identities'][mesh_names[0]+'__self_nonadjacent']};assert len(original18)==18 and oldpairs[mesh_names[0]+'__self_nonadjacent']-basepairs[mesh_names[0]+'__self_nonadjacent']==original18
oldlane.off();assert snapshot(names)==before
actions={};lanes=[]
for ob in ['Meshy_Fitted_Rig','Armature','Hair_Rig_R4']:
 a=bpy.data.actions.new('YURI_R4_SIT_FRAME8_NATIVE_CONSTRAINT_'+ob);a.use_fake_user=True;a.slots.new(id_type='OBJECT',name=ob);actions[ob]=a;ln=ReactionLane(ob);ln.on(a.name);lanes.append(ln)
for b in r.pose.bones:b.location,b.rotation_quaternion,b.scale=oldposes[b.name]
for q in ['L','R']:r.pose.bones['toe.'+q].rotation_quaternion=offquat['toe.'+q]
bpy.context.view_layer.update()
src={n:Matrix(v) for n,v in i['samples_private']['Sitting_Enter'][7].items()};desired={}
for q,u in [('L','l'),('R','r')]:
 aa=np.array(src['thigh_'+u].translation)-np.array(src['calf_'+u].translation);bb=np.array(src['foot_'+u].translation)-np.array(src['calf_'+u].translation);desired[q]=math.pi-math.acos(float(np.clip(np.dot(aa,bb)/(np.linalg.norm(aa)*np.linalg.norm(bb)),-1,1)))
lower=[b+'.'+q for q in ['L','R'] for b in ['thigh','shin','foot']];qbase={n:r.pose.bones[n].rotation_quaternion.copy() for n in lower};lbase=r.pose.bones['pelvis'].location.copy();x=np.zeros(21)
def setpose(x):
 r.pose.bones['pelvis'].location=lbase+Vector(x[:3])
 for j,n in enumerate(lower):r.pose.bones[n].rotation_quaternion=qbase[n]@Quaternion(Vector(x[3+3*j:6+3*j]))
 bpy.context.view_layer.update()
def measures(v):
 out={}
 for q in ['L','R']:
  hip=np.array(r.matrix_world@r.pose.bones['thigh.'+q].head);knee=np.array(r.matrix_world@r.pose.bones['shin.'+q].head);ankle=np.array(r.matrix_world@r.pose.bones['foot.'+q].head);a=hip-knee;b=ankle-knee;angle=math.pi-math.acos(float(np.clip(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)),-1,1)));mid=(hip+ankle)*.5;off=knee-mid;lat=np.cross(forward[q],np.array([0,0,1]));fwd=float(np.dot(off,forward[q]));lateral=float(np.dot(off,lat));dist=np.linalg.norm(v[patch[q]]-v0[patch[q]],axis=1)
  out[q]={'knee_flexion_degrees':math.degrees(angle),'desired_donor_knee_degrees':math.degrees(desired[q]),'knee_angle_error_degrees':math.degrees(angle-desired[q]),'knee_forward_m':fwd,'knee_lateral_m':lateral,'whole_original_patch_max_anchor_error_m':float(dist.max()),'patch_rms_anchor_error_m':float(np.sqrt((dist**2).mean())),'patch_max_XY_drift_m':float(np.linalg.norm(v[patch[q],:2]-v0[patch[q],:2],axis=1).max()),'patch_gap_min_max_m':[float((v[patch[q],2]-floor).min()),float((v[patch[q],2]-floor).max())],'whole_foot_min_gap_m':float(v[footids[q],2].min()-floor)}
 return out
def residual(x):
 setpose(x);v=geom(body)[0];z=[]
 for q in ['L','R']:z.extend(((v[patch[q]]-v0[patch[q]])/math.sqrt(len(patch[q]))).ravel())
 met=measures(v)
 for q in ['L','R']:
  u=met[q];z.extend([.10*math.radians(u['knee_angle_error_degrees']),min(0,u['knee_forward_m']),max(0,abs(u['knee_lateral_m'])-.015)])
 z.extend(1e-5*x);return np.array(z)
oldmetrics=measures(old[mesh_names[0]][0]) # reset actual joints to old pose for exact old readback
for b in r.pose.bones:b.location,b.rotation_quaternion,b.scale=oldposes[b.name]
bpy.context.view_layer.update();oldmetrics=measures(old[mesh_names[0]][0])
history=[];start=time.perf_counter();lam=1e-5;rr=residual(x);eps=3e-4
for it in range(18):
 if time.perf_counter()-start>180:break
 jac=np.column_stack([(residual(x+np.eye(21)[j]*eps)-rr)/eps for j in range(21)])
 dx=np.linalg.solve(jac.T@jac+lam*np.eye(21),-jac.T@rr);dx[:3]=np.clip(dx[:3],-.025,.025);dx[3:]=np.clip(dx[3:],-.18,.18)
 trial=x+dx;rt=residual(trial);accepted=float(rt@rt)<float(rr@rr)
 if accepted:x,rr=trial,rt;lam=max(1e-8,lam*.4)
 else:lam*=8
 history.append({'iteration':it,'objective':float(rr@rr),'accepted':accepted,'damping':lam});print('FRAME8_CONSTRAINT_SOLVE',history[-1],flush=True)
 if accepted and np.linalg.norm(dx)<1e-5:break
setpose(x);new=evaluate();newmetrics=measures(new[mesh_names[0]][0]);delta=(r.matrix_world@r.pose.bones['head'].matrix)@refhead.inverted();delta=Matrix.LocRotScale(delta.translation,delta.to_quaternion(),Vector((1,1,1)))
for ob,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]:
 pb=bpy.data.objects[ob].pose.bones[bn];bb=pb.bone.matrix_local.inverted()@bpy.data.objects[ob].matrix_world.inverted()@delta@refs[ob];pb.location=bb.translation;pb.rotation_quaternion=bb.to_quaternion()
bpy.context.view_layer.update();new=evaluate();newpairs,_=contact(new);key=mesh_names[0]+'__self_nonadjacent';newbody=newpairs[key]-basepairs[key];retained=original18&newbody
for ob,a in actions.items():
 for b in bpy.data.objects[ob].pose.bones:
  b.keyframe_insert('location',frame=1,group=b.name);b.keyframe_insert('rotation_quaternion',frame=1,group=b.name)
newPose={b.name:(b.location.copy(),b.rotation_quaternion.copy(),b.scale.copy()) for b in r.pose.bones}
cam=s.camera;savecam=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale);settings=[(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',8),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',384),(s.render,'resolution_y',384),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','PNG'),(s.render.image_settings,'color_mode','RGBA'),(s.render,'filepath','')];saved=[(o,k,getattr(o,k)) for o,k,_ in settings]
for o,k,v in settings:setattr(o,k,v)
for label,pose in [('old',oldposes),('constraint',newPose)]:
 for b in r.pose.bones:b.location,b.rotation_quaternion,b.scale=pose[b.name]
 bpy.context.view_layer.update();delta=(r.matrix_world@r.pose.bones['head'].matrix)@refhead.inverted();delta=Matrix.LocRotScale(delta.translation,delta.to_quaternion(),Vector((1,1,1)))
 for ob,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]:
  pb=bpy.data.objects[ob].pose.bones[bn];bb=pb.bone.matrix_local.inverted()@bpy.data.objects[ob].matrix_world.inverted()@delta@refs[ob];pb.location=bb.translation;pb.rotation_quaternion=bb.to_quaternion()
 for view,direction in [('front',(0,-1,0)),('quarter',(.6,-1,0)),('side',(1,0,0))]:
  target=Vector((.002,.02,.48));cam.data.type='ORTHO';cam.data.ortho_scale=1.18;cam.location=target+Vector(direction).normalized()*.8;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(O/(label+'_'+view+'.png'));bpy.ops.render.render(write_still=True)
cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale=savecam
for ln in reversed(lanes):ln.off()
for o,k,v in saved:setattr(o,k,v)
assert snapshot(names)==before
candidate=O/'Character_R4_SitFrame8_CONSTRAINT_EXPERIMENT_OFF_R1.blend';bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=False);assert snapshot(names)==before
lib=O/'YURI_R4_SIT_FRAME8_CONSTRAINT_ACTIONS_ONLY_R1.blend';bpy.data.libraries.write(str(lib),set(actions.values()),fake_user=True)
assert snapshot(names)==before
oSave=[(o,k,getattr(o,k)) for o,k,_ in settings]
for o,k,v in settings:setattr(o,k,v)
s.render.resolution_x=960;s.render.resolution_y=920;s.render.filepath=str(O/'OFF_SOURCE_CAMERA_NEUTRAL.png');bpy.ops.render.render(write_still=True)
for o,k,v in oSave:setattr(o,k,v)
# Reopening invalidated previous settings owner pointers; restore canonical from file again, no save.
bpy.ops.wm.open_mainfile(filepath=str(candidate),use_scripts=False);assert snapshot(names)==before
constraints_ok=all(abs(v['knee_angle_error_degrees'])<=.5 and v['whole_original_patch_max_anchor_error_m']<=.001 and v['knee_forward_m']>=0 and abs(v['knee_lateral_m'])<=.015 for v in newmetrics.values())
counts={k:{'old_new_vs_OFF':len(oldpairs[k]-basepairs[k]),'constraint_new_vs_OFF':len(newpairs[k]-basepairs[k]),'introduced_vs_old':len(newpairs[k]-oldpairs[k])} for k in basepairs}
result={'task':'ROOT_PM_SIT_STAND_FRAME8_NATIVE_CONSTRAINT_REPAIR_R1','source_SHA':m['source_SHA'],'old_candidate_SHA':m['candidate_SHA'],'candidate':str(candidate),'candidate_SHA':sha(candidate),'library':str(lib),'library_SHA':sha(lib),'frame8_only':True,'solve_iteration_history':history,'solve_seconds':time.perf_counter()-start,'variables':'21 pelvis-local translation + 6 native lower bone exponential-map rotation deltas; upper local reference fixed; toe original OFF local rotation. No rest/bind/skin/mesh change.','whole_original_sole_anchor_vertices':{q:len(v) for q,v in patch.items()},'corridor_definition':'Knee in original foot/toe forward half-plane relative hip/ankle midpoint; sagittal lateral residual <=15mm. Joint-pose constraints only, not force/support.','old_actual':oldmetrics,'constraint_actual':newmetrics,'constraints_all_residuals_within_declared_tolerance':constraints_ok,'exact_old18_retained':len(retained),'exact_old18_removed':len(original18-retained),'all_crossings_counts':counts,'source78_fullraw_OFF_and_serialized_candidate_equal':True,'original78_signature_private':before,'new_original18_retained_private':sorted(retained),'all_old_new_pair_identities_private':{'old':{k:sorted(v-basepairs[k]) for k,v in oldpairs.items()},'constraint':{k:sorted(v-basepairs[k]) for k,v in newpairs.items()}},'pose_pass':constraints_ok and not newbody and all(not (newpairs[k]-basepairs[k]) for k in newpairs),'TierP':0,'next':'No complete121frame rerender unless source pose constraints AND new crossing gates improve; infeasible combination is rejected, not physically validated.'}
(O/'FRAME8_NATIVE_CONSTRAINT_PRIVATE_R1.json').write_text(json.dumps(result,indent=2),encoding='utf8');assert sha(m['source'])==m['source_SHA'] and sha(m['candidate'])==m['candidate_SHA'];print('FRAME8_RESULT',newmetrics,counts,'OLD18_RETAINED',len(retained),'PASS',result['pose_pass'],flush=True)
