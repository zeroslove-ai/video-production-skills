"""Two static native R4 poses, additive Actions only, evaluated QA and matched renders."""
import bpy,sys,json,hashlib,math
from pathlib import Path
import numpy as np
from mathutils import Vector,Quaternion
from mathutils.bvhtree import BVHTree
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'dance03-constrained-native-c1';O.mkdir(exist_ok=False)
P=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/target-reference/Character_Master_NeckSkin_R4.blend')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
sourceSHA=sha(P);assert sourceSHA=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False)
s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered'];names=list(bpy.data.actions.keys());before=snapshot(names)
original_pose={b.name:tuple(b.rotation_quaternion) for b in r.pose.bones};fixed={}
def update():bpy.context.view_layer.update()
def geometry(obj):
 e=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();m.calc_loop_triangles();v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);mat=np.array(e.matrix_world);v=v.reshape(-1,3).astype(float)@mat[:3,:3].T+mat[:3,3];tri=[tuple(t.vertices) for t in m.loop_triangles];edges=np.array([tuple(x.vertices) for x in m.edges],dtype=int);polys=[tuple(p.vertices) for p in m.polygons]
 assert np.isfinite(v).all()
 if obj.name not in fixed:fixed[obj.name]=(len(v),polys)
 else:assert fixed[obj.name]==(len(v),polys)
 e.to_mesh_clear();return v,tri,edges
def cohort(groups,threshold=.01):
 ids={body.vertex_groups[n].index for n in groups}
 return {v.index for v in body.data.vertices if sum(g.weight for g in v.groups if g.group in ids)>threshold}
armgroups={side:[n+'.'+side for n in ['clavicle','upper_arm','forearm','hand']]+[n+str(j)+'.'+side for n in ['thumb','index','middle','ring','pinky'] for j in [1,2,3]] for side in ['L','R']}
cohorts={side:cohort(gs) for side,gs in armgroups.items()}
cohorts['left_leg']=cohort(['thigh.L','shin.L','foot.L','toe.L'])
floor=float(bpy.data.objects['Contact_Ground'].matrix_world.translation.z)
v0,t0,ed=geometry(body);h0,ht0,_=geometry(bpy.data.objects['Character_Body_Head']);hair0,hairt0,_=geometry(bpy.data.objects['Hair_Replacement_R4'])
feet={};soles={}
for side in ['L','R']:
 ids=sorted(cohort(['foot.'+side,'toe.'+side],.5));zmin=float(v0[ids,2].min());patch=[i for i in ids if v0[i,2]<=zmin+.002];feet[side]=ids;soles[side]=patch
def contacts():
 v,t,e=geometry(body);alltree=BVHTree.FromPolygons(v.tolist(),t,all_triangles=True,epsilon=0);res={};sets={}
 for label,verts in cohorts.items():
  ids=[i for i,x in enumerate(t) if any(j in verts for j in x)];tree=BVHTree.FromPolygons(v.tolist(),[t[i] for i in ids],all_triangles=True,epsilon=0);non=set();adj=set();same=set()
  for i,j in tree.overlap(alltree):
   x=t[ids[i]];y=t[j];key=tuple(sorted([tuple(sorted(x)),tuple(sorted(y))]))
   if set(x)==set(y):same.add(key)
   elif set(x)&set(y):adj.add(key)
   else:non.add(key)
  sets[label+'__all_body_nonadjacent']=non;res[label]={'inclusive_triangles':len(ids),'nonadjacent_all_body':len(non),'shared_vertex_adjacent_raw':len(adj),'identical_triangle_raw':len(same)}
  for tag,objname in [('head','Character_Body_Head'),('hair','Hair_Replacement_R4')]:
   vv,tt,_=geometry(bpy.data.objects[objname]);other=BVHTree.FromPolygons(vv.tolist(),tt,all_triangles=True,epsilon=0);pairs={(tuple(sorted(t[ids[i]])),tuple(sorted(tt[j]))) for i,j in tree.overlap(other)};sets[label+'__'+tag]=pairs;res[label][tag+'_intersections']=len(pairs)
 return res,sets
baseline_counts,baseline_sets=contacts()
def worldpoint(n,tail=False):b=r.pose.bones[n];return r.matrix_world@(b.tail if tail else b.head)
def axisrotate(n,axis,degrees):
 b=r.pose.bones[n];local=b.matrix.to_3x3().inverted()@(r.matrix_world.to_3x3().inverted()@Vector(axis));b.rotation_quaternion=b.rotation_quaternion@Quaternion(local.normalized(),math.radians(degrees));update()
def aim(n,direction):
 b=r.pose.bones[n];current=(worldpoint(n,True)-worldpoint(n)).normalized();desired=Vector(direction).normalized();q=current.rotation_difference(desired);axis,ang=q.to_axis_angle();axisrotate(n,axis,math.degrees(ang))
def aimtarget(n,target):aim(n,Vector(target)-worldpoint(n))
# ONE source-native constrained03 solution; no sweeps or generic IK framework.
existing=json.loads((B/'dance03-existing-solutions-inspect-c1/EXISTING_NATIVE_SOLUTIONS_PRIVATE_C1.json').read_bytes())
walk=next(x for x in existing['rows'] if x['action']=='MESHY_R2_BODY_WalkInPlace')
leg_source=next(x for x in walk['key_frames'] if x['frame']==39)
reach=next(x for x in existing['rows'] if x['action']=='MESHY_R2_BODY_Reach')
hinge_source=next(x for x in reach['key_frames'] if x['frame']==77)['bones']['forearm.L']
native_hinge=Vector(hinge_source['axis']).normalized()
oldlib=B/'dance-two-pose-native-r1/YURI_R4_DANCE_STATIC03_16_ACTIONS_ONLY_R1.blend'
oldlib_sha=sha(oldlib)
with bpy.data.libraries.load(str(oldlib),link=False) as (aa,bb):bb.actions=['YURI_R4_DANCE_STATIC_03_BODY_R1']
oldright=bb.actions[0]
oldright_q={}
for n in ['upper_arm.R','forearm.R']:
 path='pose.bones["'+n+'"].rotation_quaternion'
 cs={f.array_index:f for l in oldright.layers for st in l.strips for ba in st.channelbags for f in ba.fcurves if f.data_path==path}
 oldright_q[n]=Quaternion([cs[j].evaluate(1) for j in range(4)])
bpy.data.actions.remove(oldright)
assert snapshot(names)==before
constraint={}
def set_pose(pid):
 assert pid=='03'
 # Reuse exact existing Walk39 LEFT thigh/shin/foot solution; source pelvis/root and RIGHT leg stay untouched.
 for n in ['thigh.L','shin.L','foot.L']:r.pose.bones[n].rotation_quaternion=Quaternion(leg_source['bones'][n]['q'])
 for n,q in oldright_q.items():r.pose.bones[n].rotation_quaternion=q
 update()
 shoulder=worldpoint('upper_arm.L');l1=(worldpoint('upper_arm.L',True)-shoulder).length;l2=(worldpoint('forearm.L',True)-worldpoint('forearm.L')).length
 target=Vector((.025,-.220,.700));pole=Vector((.170,-.105,.650));delta=target-shoulder;dist=delta.length;u=delta.normalized()
 assert abs(l1-l2)+.005<dist<l1+l2-.005
 along=(l1*l1-l2*l2+dist*dist)/(2*dist);height=math.sqrt(max(0,l1*l1-along*along));p=pole-shoulder;p=(p-u*p.dot(u)).normalized();elbow=shoulder+u*along+p*height
 ud=(elbow-shoulder).normalized();fd=(target-elbow).normalized();normal=ud.cross(fd).normalized()
 aim('upper_arm.L',ud)
 axis=(r.matrix_world.to_3x3()@r.pose.bones['forearm.L'].matrix.to_3x3()@native_hinge).normalized()
 axisproj=(axis-ud*axis.dot(ud)).normalized()
 # Explicit bounded upper-arm axial twist to align the native elbow hinge with the pole plane.
 twist=math.atan2(ud.dot(axisproj.cross(normal)),axisproj.dot(normal));bound=math.radians(35);applied=max(-bound,min(bound,twist));axisrotate('upper_arm.L',ud,math.degrees(applied))
 current=(worldpoint('forearm.L',True)-worldpoint('forearm.L')).normalized();axis=(r.matrix_world.to_3x3()@r.pose.bones['forearm.L'].matrix.to_3x3()@native_hinge).normalized()
 bend=math.atan2(axis.dot(current.cross(fd)),current.dot(fd));bnd=math.radians(85);clamped=max(-bnd,min(bnd,bend))
 r.pose.bones['forearm.L'].rotation_quaternion=Quaternion(native_hinge,clamped);update()
 actual_elbow=worldpoint('forearm.L');actual_wrist=worldpoint('forearm.L',True)
 constraint.update({'native_two_bone_lengths_m':[l1,l2],'target_world_m':list(target),'pole_world_m':list(pole),'analytic_elbow_world_m':list(elbow),'actual_elbow_world_m':list(actual_elbow),'actual_wrist_world_m':list(actual_wrist),'target_distance_m':dist,'actual_wrist_target_error_m':(actual_wrist-target).length,'native_elbow_hinge_axis_from_Reach77':list(native_hinge),'requested_upper_axial_twist_degrees':math.degrees(twist),'applied_upper_axial_twist_degrees':math.degrees(applied),'upper_axial_twist_bound_degrees':35,'requested_elbow_bend_degrees':math.degrees(bend),'applied_elbow_bend_degrees':math.degrees(clamped),'elbow_bend_bound_degrees':85,'existing_leg_source':'MESHY_R2_BODY_WalkInPlace39 exact3quaternions; pelvis/root/lowerRIGHT unchanged','existing_leg_delta_degrees':{n:leg_source['bones'][n]['delta_deg'] for n in ['thigh.L','shin.L','foot.L']},'right_arm_previous03_quaternions_exact':True,'one_candidate_no_sweep':True})
 update()

changed={'03':['thigh.L','shin.L','foot.L','upper_arm.R','forearm.R','upper_arm.L','forearm.L'],'16':['upper_arm.R','forearm.R','upper_arm.L','forearm.L']}
rows=[];action_names={};pose_quats={}
for pid in ['03']:
 a=bpy.data.actions.new('YURI_R4_DANCE03_CONSTRAINED_'+pid+'_BODY_C1');a.use_fake_user=True;a.slots.new('OBJECT',r.name);lane=ReactionLane();lane.on(a.name);set_pose(pid)
 for n in changed[pid]:r.pose.bones[n].keyframe_insert('rotation_quaternion',frame=1,group=n)
 s.frame_set(1);update();pose_quats[pid]={n:list(r.pose.bones[n].rotation_quaternion) for n in changed[pid]};action_names[pid]=a.name
 v,t,edges=geometry(body);counts,pairs=contacts();new={k:len(x-baseline_sets[k]) for k,x in pairs.items()}
 sole={}
 for side in ['L','R']:
  ids=feet[side];patch=soles[side];delta=v[patch]-v0[patch];sole[side]={'vertices':len(ids),'bottom_patch_vertices':len(patch),'source_min_gap_m':float(v0[ids,2].min()-floor),'posed_min_gap_m':float(v[ids,2].min()-floor),'source_patch_gap_range_m':[float(v0[patch,2].min()-floor),float(v0[patch,2].max()-floor)],'posed_patch_gap_range_m':[float(v[patch,2].min()-floor),float(v[patch,2].max()-floor)],'max_patch_drift_m':float(np.linalg.norm(delta,axis=1).max()),'max_all_foot_vertices_drift_m':float(np.linalg.norm(v[ids]-v0[ids],axis=1).max())}
 angles={n:math.degrees(r.pose.bones[n].rotation_quaternion.rotation_difference(Quaternion(original_pose[n])).angle) for n in changed[pid]}
 oldlen=np.linalg.norm(v0[edges[:,0]]-v0[edges[:,1]],axis=1);newlen=np.linalg.norm(v[edges[:,0]]-v[edges[:,1]],axis=1);valid=oldlen>1e-6;ratios=newlen[valid]/oldlen[valid]
 deformation={'finite':True,'topology_identical':True,'edge_ratio_min':float(ratios.min()),'edge_ratio_max':float(ratios.max()),'edge_ratio_p01_p99':list(np.quantile(ratios,[.01,.99])),'source_zero_edges_skipped':int((~valid).sum()),'scope':'Evaluated world geometry; edge ratios are deformation diagnostics, not anatomical ROM limits or volume certification.'}
 crossing=None
 if pid=='16':
  ra=np.array(worldpoint('forearm.R'));rb=np.array(worldpoint('forearm.R',True));la=np.array(worldpoint('forearm.L'));lb=np.array(worldpoint('forearm.L',True));xz=[0,2];mat=np.column_stack([(rb-ra)[xz],-(lb-la)[xz]])
  st=np.linalg.solve(mat,(la-ra)[xz]);rp=ra+st[0]*(rb-ra);lp=la+st[1]*(lb-la)
  crossing={'R_parameter':float(st[0]),'L_parameter':float(st[1]),'both_within_forearms':bool(np.all(st>=0) and np.all(st<=1)),'R_y_m':float(rp[1]),'L_y_m':float(lp[1]),'R_camera_nearer_depth_m':float(lp[1]-rp[1]),'right_nearer_front_camera':bool(rp[1]<lp[1]),'scope':'Bone centerline projected crossing, separate from actual surface intersection/clearance.'}
 # Conservative whole-surface minimum vertex-to-triangle distance for opposite arm and remote torso, weak-weight cohort included.
 gaps={}
 for side in ['L','R']:
  vertex_ids=sorted(cohorts[side]);other='R' if side=='L' else 'L'
  targets={'opposite_arm':[x for x in t if any(j in cohorts[other] for j in x) and not any(j in cohorts[side] for j in x)],'remote_body':[x for x in t if not any(j in cohorts[side] for j in x)]}
  for label,tri in targets.items():
   tree=BVHTree.FromPolygons(v.tolist(),tri,all_triangles=True,epsilon=0);dist=[tree.find_nearest(Vector(v[i]))[3] for i in vertex_ids];gaps[side+'__'+label]={'min_vertex_to_triangle_m':float(min(dist)),'query_vertices':len(vertex_ids),'target_triangles':len(tri),'scope':'ANY summed relevant arm/digit weight>.01 query; target excludes triangles touching same cohort to avoid own/skin adjacency. Shoulder boundary may yield near-zero; all-body inclusive nonadjacent intersection gate separately includes these triangles. Distance alone not complete triangle-triangle minimum or containment.'}
 row={'pose':pid,'changed_bones':changed[pid],'quaternion_delta_degrees':angles,'actual_sole':sole,'deformation':deformation,'inclusive_counts':counts,'new_pairs_vs_source':new,'crossing':crossing,'clearance_diagnostics':gaps,'contact_verdict':'FAIL/HOLD' if any(new.values()) else 'SCOPED_NO_NEW_NONADJACENT_SURFACE_INTERSECTION','geometric_floor_verdict':'MEASURED_ONLY_NO_FORCE_COM_PHYSX','static_only':True,'TierP':0}
 rows.append(row);print('STATIC_POSE_QA',pid,json.dumps(row),flush=True);lane.off();assert snapshot(names)==before
candidate=O/'Character_R4_Dance03_Constrained_EXPERIMENT_OFF_C1_20261005.blend';bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=False)
lib=O/'YURI_R4_DANCE03_CONSTRAINED_ACTION_ONLY_C1.blend';bpy.data.libraries.write(str(lib),{bpy.data.actions[x] for x in action_names.values()},fake_user=True)
with bpy.data.libraries.load(str(lib),link=False) as (src,dst):assert len(src.actions)==1 and not src.objects and not src.meshes and not src.armatures
# Matched existing source-camera/light setup, camera temporary only; all settings restored.
cam=s.camera;origcam=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale)
changes=[(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',8),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',768),(s.render,'resolution_y',1024),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','PNG'),(s.render.image_settings,'color_mode','RGBA'),(s.render.image_settings,'color_depth','8'),(s.render,'filepath','')]
original=[(ob,k,getattr(ob,k)) for ob,k,_ in changes]
for ob,k,val in changes:setattr(ob,k,val)
views={}
for view,direction in [('front',Vector((0,-1,0))),('left',Vector((1,0,0)))]:
 target=Vector((.00195,-.028,.50));cam.data.type='ORTHO';cam.data.ortho_scale=1.12;cam.location=target+direction*3;cam.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler();views[view]={'position':list(cam.location),'rotation':list(cam.rotation_euler),'target':list(target),'ortho_scale':1.12,'resolution':[768,1024],'anatomical_camera':view}
 for pid in ['OFF','03']:
  lane=None
  if pid!='OFF':lane=ReactionLane();lane.on(action_names[pid]);s.frame_set(1);update()
  s.render.filepath=str(O/(pid+'_'+view+'.png'));bpy.ops.render.render(write_still=True)
  if lane:lane.off()
cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale=origcam
s.render.resolution_x=960;s.render.resolution_y=920;s.render.filepath=str(O/'CANDIDATE_OFF_SOURCE_NEUTRAL.png');bpy.ops.render.render(write_still=True)
for ob,k,val in original:setattr(ob,k,val)
assert snapshot(names)==before;assert sha(P)==sourceSHA
meta={'task':'ROOT_PM_DANCE03_CONSTRAINED_NATIVE_CORRECTION_R1','source':str(P),'source_SHA':sourceSHA,'candidate':str(candidate),'candidate_SHA':sha(candidate),'candidate_OFF_full_snapshot_equal':True,'original78Actions_preserved':len(names)==78,'action_names':action_names,'action_only_library':{'file':str(lib),'sha256':sha(lib),'bytes':lib.stat().st_size,'actions':1,'objects':0,'meshes':0,'armatures':0},'native_constraint_private':constraint,'pose_quaternions_private':pose_quats,'baseline_counts':baseline_counts,'rows':rows,'floor_z_m':floor,'views':views,'original_neutral_pixel_oracle':'PENDING_EXTERNAL_RGBA_COMPARE','source_original_geometry_rest_weights_material_morph_drivers_preserved':True,'collision_scope':'Actual evaluated body triangles selected if ANY vertex has summed relevant bone/digit weights>.01, vs ALL actual body triangles. No weak-weight/palm/webbing exception. Same/shared vertices counted separately; nonadjacent compared to source baseline. Body cohorts also against ALL actual head/hair. Baseline source intersections and adjacency are not silently approved. No volumetric containment/adjacent deformation/PhysX certification.','limits':'Static03 ONLY, no timing/transition/full dance/mocap/AI anatomy trace/Unity/F2/TierP;06/14/16 remain unexpanded.'}
(O/'DANCE03_CONSTRAINED_PRIVATE_MANIFEST_C1.json').write_text(json.dumps(meta,indent=2),encoding='utf8');print('DANCE_TWO_POSE_DONE_OFF_EQUAL',sha(candidate),flush=True)
