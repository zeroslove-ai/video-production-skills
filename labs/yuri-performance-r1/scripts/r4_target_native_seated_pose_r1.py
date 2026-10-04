"""ONE target-native high-seat pose, anatomy-derived two-bone IK. Donor timing only."""
import bpy,sys,json,hashlib,ast,math,collections
from pathlib import Path
import numpy as np
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-target-native-seated-pose-r1';O.mkdir(exist_ok=False);source=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/target-reference/Character_Master_NeckSkin_R4.blend');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();sourceSHA=sha(source);assert sourceSHA=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
bpy.ops.wm.open_mainfile(filepath=str(source),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];names=list(bpy.data.actions.keys());before=snapshot(names);assert len(names)==78
for fn,defs in [('r4_native_walk_source_supply_r1.py',['contact']),('r4_existing_reach_contact_closure_r1.py',['geom'])]:
 tree=ast.parse((H/fn).read_text(encoding='utf8'));exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in defs],type_ignores=[]),'<pinned_actual_source_mesh_helpers>','exec'))
fixed={};mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4'];body=bpy.data.objects[mesh_names[0]];gn={g.index:g.name for g in body.vertex_groups}
def evaluate():return {n:geom(bpy.data.objects[n]) for n in mesh_names}
neutral=evaluate();basepairs,_=contact(neutral);v0=neutral[mesh_names[0]][0];floor=float(v0[:,2].min());footids={q:np.array([v.index for v in body.data.vertices if sum(g.weight for g in v.groups if gn[g.group] in ['foot.'+q,'toe.'+q])>.5],int) for q in ['L','R']};patch={q:ids[v0[ids,2]<=floor+.003] for q,ids in footids.items()};offworld={b.name:r.matrix_world@b.matrix for b in r.pose.bones};offquat={b.name:b.rotation_quaternion.copy() for b in r.pose.bones};offpose={b.name:(b.location.copy(),b.rotation_quaternion.copy(),b.scale.copy()) for b in r.pose.bones};actions={};lanes=[]
for ob in ['Meshy_Fitted_Rig','Armature','Hair_Rig_R4']:
 a=bpy.data.actions.new('YURI_R4_TARGET_NATIVE_HIGH_SEAT_'+ob+'_R1');a.use_fake_user=True;a.slots.new(id_type='OBJECT',name=ob);actions[ob]=a;ln=ReactionLane(ob);ln.on(a.name);lanes.append(ln)
# One reachable high stool witness: pelvis drop equals 20% of native mean hip-knee-ankle chain, posterior shift10%. No donor pose/angles/stance/floor-fit.
lengths={q:[(offworld['thigh.'+q].translation-offworld['shin.'+q].translation).length,(offworld['shin.'+q].translation-offworld['foot.'+q].translation).length] for q in ['L','R']};leg=float(np.mean([sum(x) for x in lengths.values()]));delta=Vector((0,.10*leg,-.20*leg));goalpelvis=offworld['pelvis'].translation+delta;pb=r.pose.bones['pelvis'];actual=r.matrix_world@pb.head;linear=r.matrix_world.to_3x3()@pb.parent.matrix.to_3x3()@(pb.parent.bone.matrix_local.inverted()@pb.bone.matrix_local).to_3x3();pb.location+=linear.inverted()@(goalpelvis-actual);bpy.context.view_layer.update();goals={};desired={};forward={};reachable={}
for q in ['L','R']:
 hip=offworld['thigh.'+q].translation+delta;ankle=offworld['foot.'+q].translation.copy();axis=(ankle-hip).normalized();d=(ankle-hip).length;l1,l2=lengths[q];reachable[q]=abs(l1-l2)<d<l1+l2;assert reachable[q];aa=(l1*l1-l2*l2+d*d)/(2*d);height=math.sqrt(max(0,l1*l1-aa*aa));fwd=offworld['toe.'+q].translation-offworld['foot.'+q].translation;fwd.z=0;fwd.normalize();forward[q]=fwd.copy();pole=fwd-axis*fwd.dot(axis);pole.normalize();knee=hip+axis*aa+pole*height;goals[q]={'hip':hip,'knee':knee,'ankle':ankle}
 for n,oldvec,newvec in [('thigh',offworld['shin.'+q].translation-offworld['thigh.'+q].translation,knee-hip),('shin',offworld['foot.'+q].translation-offworld['shin.'+q].translation,ankle-knee)]:desired[n+'.'+q]=oldvec.normalized().rotation_difference(newvec.normalized())@offworld[n+'.'+q].to_quaternion()
 desired['foot.'+q]=offworld['foot.'+q].to_quaternion()
for b in r.pose.bones:
 if b.name not in desired:continue
 pq=desired.get(b.parent.name,offworld[b.parent.name].to_quaternion());rel=b.parent.bone.matrix_local.inverted()@b.bone.matrix_local;b.rotation_quaternion=rel.to_quaternion().inverted()@pq.inverted()@desired[b.name]
bpy.context.view_layer.update();headDelta=(r.matrix_world@r.pose.bones['head'].matrix).translation-offworld['head'].translation
# Original head/hair root rotation untouched: only native local translation maps body upper translation.
headRigGoals={}
for ob,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]:
 oo=bpy.data.objects[ob];b=oo.pose.bones[bn];old=oo.matrix_world@b.matrix;b.location+=b.bone.matrix_local.to_3x3().inverted()@oo.matrix_world.to_3x3().inverted()@headDelta;bpy.context.view_layer.update();want=Matrix.Translation(headDelta)@old;headRigGoals[ob]=float(np.abs(np.array(oo.matrix_world@b.matrix)-np.array(want)).max())
bpy.context.view_layer.update();actualPelvis=r.matrix_world@r.pose.bones['pelvis'].head;posed=evaluate();pairs,_=contact(posed);vv=posed[mesh_names[0]][0];metrics={}
for q in ['L','R']:
 hip=r.matrix_world@r.pose.bones['thigh.'+q].head;knee=r.matrix_world@r.pose.bones['shin.'+q].head;ankle=r.matrix_world@r.pose.bones['foot.'+q].head;angle=180-math.degrees((hip-knee).angle(ankle-knee));dist=np.linalg.norm(vv[patch[q]]-v0[patch[q]],axis=1);lateral=forward[q].cross(Vector((0,0,1)));offset=knee-(hip+ankle)*.5
 metrics[q]={'native_anatomical_knee_degrees':angle,'knee_forward_m':offset.dot(forward[q]),'knee_lateral_m':offset.dot(lateral),'hip_goal_error_m':(hip-goals[q]['hip']).length,'knee_goal_error_m':(knee-goals[q]['knee']).length,'ankle_goal_error_m':(ankle-goals[q]['ankle']).length,'whole_original_patch_max_anchor_error_m':float(dist.max()),'patch_XY_max_drift_m':float(np.linalg.norm(vv[patch[q],:2]-v0[patch[q],:2],axis=1).max()),'original_patch_gap_min_max_m':[float((vv[patch[q],2]-floor).min()),float((vv[patch[q],2]-floor).max())],'whole_foot_min_gap_m':float(vv[footids[q],2].min()-floor),'original_support_patch_vertices':len(patch[q]),'joint_pose_only_not_force_contact':True}
counts={k:{'source_OFF_absolute':len(v),'pose_absolute':len(pairs[k]),'new_vs_OFF':len(pairs[k]-v)} for k,v in basepairs.items()};ranks={}
for k,v in pairs.items():
 if not k.startswith(mesh_names[0]+'__self'):continue
 rank=collections.Counter()
 for pair in v-basepairs[k]:
  labels=[]
  for tri in pair:
   weights=collections.Counter()
   for idx in tri:
    for g in body.data.vertices[idx].groups:weights[gn[g.group]]+=g.weight
   labels.append(weights.most_common(1)[0][0] if weights else 'unweighted')
  rank[' / '.join(sorted(labels))]+=1
 ranks[k]=rank.most_common(16)
for ob,a in actions.items():
 for b in bpy.data.objects[ob].pose.bones:b.keyframe_insert('location',frame=1,group=b.name);b.keyframe_insert('rotation_quaternion',frame=1,group=b.name)
s.frame_set(1);bpy.context.view_layer.update();check=evaluate();assert all(np.array_equal(check[n][0],posed[n][0]) for n in mesh_names)
cam=s.camera;savecam=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale);settings=[(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',8),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',384),(s.render,'resolution_y',384),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','PNG'),(s.render.image_settings,'color_mode','RGBA'),(s.render,'filepath','')];saved=[(o,k,getattr(o,k)) for o,k,_ in settings]
for o,k,v in settings:setattr(o,k,v)
capture=[]
for label in ['seated','standing_OFF']:
 if label=='standing_OFF':
  for ln in reversed(lanes):ln.off()
 target_data=posed if label=='seated' else neutral
 for view,direction in [('front',(0,-1,0)),('quarter',(.6,-1,0)),('side',(1,0,0))]:
  target=Vector((.002,.02,.48));cam.data.type='ORTHO';cam.data.ortho_scale=1.18;cam.location=target+Vector(direction).normalized()*.8;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(O/(label+'_'+view+'.png'));bpy.ops.render.render(write_still=True);actual=evaluate();assert all(np.array_equal(actual[n][0],target_data[n][0]) for n in mesh_names);capture.append({'label':label,'view':view,'actual_all_mesh_equal_measured_before_after_render':True,'SHA':sha(s.render.filepath)})
cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale=savecam
for o,k,v in saved:setattr(o,k,v)
assert snapshot(names)==before
candidate=O/'Character_R4_TargetNativeHighSeat_EXPERIMENT_OFF_R1.blend';bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=False);lib=O/'YURI_R4_TARGET_NATIVE_HIGH_SEAT_ACTIONS_ONLY_R1.blend';bpy.data.libraries.write(str(lib),set(actions.values()),fake_user=True)
for o,k,v in settings:setattr(o,k,v)
s.render.resolution_x=960;s.render.resolution_y=920;s.render.filepath=str(O/'OFF_SOURCE_CAMERA_NEUTRAL.png');bpy.ops.render.render(write_still=True)
for o,k,v in saved:setattr(o,k,v)
assert snapshot(names)==before;bpy.ops.wm.open_mainfile(filepath=str(candidate),use_scripts=False);assert snapshot(names)==before
posepass=all(v['whole_original_patch_max_anchor_error_m']<=.001 and v['whole_foot_min_gap_m']>=-1e-6 and v['knee_forward_m']>=0 and abs(v['knee_lateral_m'])<=.015 and v['ankle_goal_error_m']<=.00001 for v in metrics.values()) and all(x['new_vs_OFF']==0 for x in counts.values());pelvis=list(goalpelvis);result={'task':'ROOT_PM_SIT_STAND_DONOR_REPLICATION_EXIT_NATIVE_AUTHORING_R1','source_SHA':sourceSHA,'candidate':str(candidate),'candidate_SHA':sha(candidate),'library':str(lib),'library_SHA':sha(lib),'original78_fullraw_OFF_serialized_equal':True,'original78_signature_private':before,'one_native_high_seat_pose_only':True,'donor_contribution':'Intent/timing only; no donor angles/stance/body or extraction in this native pose.','native_leg_length_m':leg,'pelvis_delta_world_m':list(delta),'pelvis_goal_world_m':pelvis,'seat_witness':{'plane_z_world_m':goalpelvis.z-.035,'height_above_floor_m':goalpelvis.z-.035-floor,'pelvis_clearance_design_m':.035,'actual_pelvis_goal_error_m':(Vector(pelvis)-actualPelvis).length,'not_physical_prop_or_support_proof':True},'actual_joint_and_whole_sole_metrics':metrics,'surface_counts':counts,'new_BODY_pair_regions_from_original_weights':ranks,'all_new_pair_identities_private':{k:sorted(v-basepairs[k]) for k,v in pairs.items()},'head_hair_translation_goal_max_matrix_error':headRigGoals,'capture':capture,'pose_pass':posepass,'verdict':'PASS_SOURCE_POSE_ONLY' if posepass else 'FAIL_HOLD_NATIVE_SEATED_POSE_CONTACT_OR_ANCHOR_RESIDUAL','TierP':0,'next_if_FAIL':'Stop seated candidate family; select existing original MESHY_R2_BODY_Wave as independent missing native source greeting batch, not accepted Talk substitution.'};(O/'TARGET_NATIVE_SEATED_POSE_PRIVATE_R1.json').write_text(json.dumps(result,indent=2),encoding='utf8');assert sha(source)==sourceSHA;print('TARGET_NATIVE_SEATED_RESULT',metrics,counts,'PASS',posepass,flush=True)
