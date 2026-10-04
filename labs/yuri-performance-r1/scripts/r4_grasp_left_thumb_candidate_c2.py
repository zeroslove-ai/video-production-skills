"""ONE left thumb-base opposition candidate; no rig/mesh/source curve rewrite."""
import bpy,sys,json,hashlib,math
from pathlib import Path
import numpy as np
from mathutils import Vector,Quaternion
from mathutils.bvhtree import BVHTree
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
from r4_native_grasp_adapter_r1 import NativeGraspLane,ACTIONS
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-grasp-left-thumb-c2';O.mkdir(exist_ok=False);d=json.loads((B/'alpha-native-grasp-candidate-r1b/NATIVE_GRASP_CANDIDATE_PRIVATE_R1B.json').read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(d['candidate'])==d['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=d['candidate'],use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered'];names=list(bpy.data.actions.keys());before=snapshot(names)
old=bpy.data.actions[ACTIONS[r.name]];a=old.copy();a.name='YURI_R4_GRASP_LEFT_THUMB_OPPOSITION_BODY_C2';a.use_fake_user=True;path='pose.bones["thumb1.L"].rotation_quaternion';curves=[f for l in a.layers for st in l.strips for ba in st.channelbags for f in ba.fcurves];assert len([f for f in curves if f.data_path==path])==4
base=NativeGraspLane();base.on();s.frame_set(85);bpy.context.view_layer.update();pb=r.pose.bones['thumb1.L'];tip=r.pose.bones['thumb3.L'].tail;target=(r.pose.bones['index2.L'].head+r.pose.bones['middle2.L'].head)*.5;joint=pb.head
c1=json.loads((B/'alpha-grasp-left-thumb-c1/LEFT_THUMB_C1_PRIVATE_MANIFEST.json').read_bytes());local_axis=Vector(c1['native_axis']['native_thumb1_local_opposition_axis']);assert abs(local_axis.length-1)<1e-5;wrist=np.array([x['wrist_world']['L'] for x in d['frames_private']]);step=np.linalg.norm(np.diff(wrist,axis=0),axis=1);return_onset=min(j+2 for j,x in enumerate(step) if j+2>120 and x>.0001);release_end=return_onset-1;release_start=119;assert return_onset==136;axis_info={'reference_frame':85,'thumb_tip_rig':list(tip),'finger_target_rig':list(target),'thumb_base_rig':list(joint),'native_thumb1_local_opposition_axis':list(local_axis),'maximum_opposition_degrees':20,'maximum_longitudinal_roll_degrees':10,'C1_actual_axis_and_angles_reused_exact':True,'onset_zero_until':61,'full_opposition_frame':85,'release_start':release_start,'release_end':release_end,'native_final_wrist_return_onset':return_onset,'return_detection':'First source LEFT wrist world step >0.1mm after120 is136; stationary120–135. Thumb release119–135 completes before this native final return.','basis':'Actual LEFT current thumb-base/tip vs index2-middle2 target, no right-hand constants/Euler signs/R5 donor geometry'};base.off()
for l in a.layers:
 for st in l.strips:
  for ba in st.channelbags:
   for fc in list(ba.fcurves):
    if fc.data_path==path:ba.fcurves.remove(fc)
oldcurves={fc.array_index:fc for l in old.layers for st in l.strips for ba in st.channelbags for fc in ba.fcurves if fc.data_path==path};ln=ReactionLane();ln.on(a.name)
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
for f in range(1,170):
 s.frame_set(f);q=Quaternion([oldcurves[j].evaluate(f) for j in range(4)]);w=ease((f-61)/24)*(1-ease((f-release_start)/(release_end-release_start)));pb.rotation_quaternion=q@Quaternion(local_axis,math.radians(20)*w)@Quaternion((0,1,0),math.radians(10)*w);pb.keyframe_insert('rotation_quaternion',frame=f,group='thumb1.L')
ln.off();new_curves=[fc for l in a.layers for st in l.strips for ba in st.channelbags for fc in ba.fcurves];assert len(new_curves)==294
def curve_record(fc):return [(k.co[:],k.handle_left[:],k.handle_right[:],k.interpolation) for k in fc.keyframe_points]
oldother={(f.data_path,f.array_index):curve_record(f) for l in old.layers for st in l.strips for ba in st.channelbags for f in ba.fcurves if f.data_path!=path};assert oldother=={(f.data_path,f.array_index):curve_record(f) for f in new_curves if f.data_path!=path}
thumbgroups={body.vertex_groups['thumb'+str(j)+'.L'].index for j in [1,2,3]};thumbverts={v.index for v in body.data.vertices if sum(g.weight for g in v.groups if g.group in thumbgroups)>.01};palmgroup=body.vertex_groups['hand.L'].index;palmverts={v.index for v in body.data.vertices if any(g.group==palmgroup and g.weight>.01 for g in v.groups)};otherdigitgroups={body.vertex_groups[n+str(j)+'.L'].index for n in ['index','middle','ring','pinky'] for j in [1,2,3]};otherv={v.index for v in body.data.vertices if any(g.group in otherdigitgroups and g.weight>.01 for g in v.groups)}
fixed=None
def geometry():
 global fixed
 e=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();m.calc_loop_triangles();v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);v=v.reshape(-1,3).astype(np.float64);mat=np.array(e.matrix_world);v=v@mat[:3,:3].T+mat[:3,3];tri=[tuple(t.vertices) for t in m.loop_triangles];polys=[tuple(p.vertices) for p in m.polygons];assert np.isfinite(v).all()
 if fixed is None:fixed=(len(v),polys)
 else:assert fixed==(len(v),polys)
 e.to_mesh_clear();return v,tri
def contacts(v,t):
 ti=[i for i,x in enumerate(t) if any(j in thumbverts for j in x)];tt=BVHTree.FromPolygons(v.tolist(),[t[i] for i in ti],all_triangles=True,epsilon=0);alltree=BVHTree.FromPolygons(v.tolist(),t,all_triangles=True,epsilon=0);non=set();adj=set();same=set();palm=set();digits=set()
 for i,j in tt.overlap(alltree):
  x=t[ti[i]];y=t[j];key=(tuple(sorted(x)),tuple(sorted(y)))
  if set(x)==set(y):same.add(key)
  elif set(x)&set(y):adj.add(key)
  else:
   non.add(key)
   if any(k in palmverts for k in y):palm.add(key)
   if any(k in otherv for k in y):digits.add(key)
 return {'nonadjacent_all_body':non,'nonadjacent_palm_inclusive':palm,'nonadjacent_other_digits_inclusive':digits,'shared_vertex_adjacent_raw':adj,'identical_triangle_raw':same},len(ti)
base=NativeGraspLane();base.on();ref={};poses={};baseline={};rows=[];root=np.array(bpy.data.objects['Assembly_Root'].matrix_world)
for f in range(1,170):
 s.frame_set(f);bpy.context.view_layer.update();v,t=geometry();ref[f]=v;poses[f]={p.name:np.array(p.matrix) for p in r.pose.bones if p.name not in ['thumb1.L','thumb2.L','thumb3.L']};baseline[f]=contacts(v,t)[0]
base.off();lanes=[]
for obj,name in {**ACTIONS,r.name:a.name}.items():lane=ReactionLane(obj);lane.on(name);lanes.append(lane)
maxunchanged=0;maxotherpose=0;maxnew={};maxcounts={};distance={}
unaffected=[i for i in range(len(body.data.vertices)) if all(g.group not in thumbgroups or g.weight==0 for g in body.data.vertices[i].groups)]
for f in range(1,170):
 s.frame_set(f);bpy.context.view_layer.update();v,t=geometry();pairs,nt=contacts(v,t);unchanged=float(np.max(np.abs(v[unaffected]-ref[f][unaffected])));maxunchanged=max(maxunchanged,unchanged);pose=max(float(np.max(np.abs(np.array(r.pose.bones[n].matrix)-m))) for n,m in poses[f].items());maxotherpose=max(maxotherpose,pose);assert np.array_equal(root,np.array(bpy.data.objects['Assembly_Root'].matrix_world));counts={k:len(x) for k,x in pairs.items()};added={k:len(x-baseline[f][k]) for k,x in pairs.items()};rows.append({'frame':f,'after_counts':counts,'before_counts':{k:len(x) for k,x in baseline[f].items()},'new_pairs_same_frame':added,'unaffected_vertex_error_m':unchanged,'nonthumb_bone_matrix_error':pose,'thumb_inclusive_triangles':nt})
 for k in pairs:maxnew[k]=max(maxnew.get(k,0),added[k]);maxcounts[k]=max(maxcounts.get(k,0),counts[k])
 if f in [1,85,169]:distance[str(f)]={'thumb_tip_to_finger_target_m':float((r.pose.bones['thumb3.L'].tail-(r.pose.bones['index2.L'].head+r.pose.bones['middle2.L'].head)*.5).length),'baseline_thumb_to_target_m':float((Vector(axis_info['thumb_tip_rig'])-Vector(axis_info['finger_target_rig'])).length) if f==85 else None,'baseline_geometry_error_m':float(np.max(np.abs(v-ref[f])))}
 if f%24==1:print('THUMB_OPPOSITION_ACTUAL_INCLUSIVE',f,counts,added,flush=True)
for lane in reversed(lanes):lane.off()
assert snapshot(names)==before and maxunchanged==0 and maxotherpose==0;assert distance['1']['baseline_geometry_error_m']==0 and distance['169']['baseline_geometry_error_m']==0
out=O/'Character_R4_Grasp_LeftThumb_C2_EXPERIMENT_OFF_20261005.blend';bpy.ops.wm.save_as_mainfile(filepath=str(out));assert sha(d['candidate'])==d['candidate_SHA'] and sha(d['source'])==d['source_SHA']
meta={'task':'ROOT_PM_LEFT_THUMB_C2_PHASE_ONLY_R1','source':d['source'],'source_SHA':d['source_SHA'],'base_candidate':d['candidate'],'base_candidate_SHA':d['candidate_SHA'],'candidate':str(out),'candidate_SHA':sha(out),'body_action':a.name,'actions':{**ACTIONS,r.name:a.name},'frame_range':[1,169],'fps':24,'native_axis':axis_info,'changed_curves_only':['thumb1.L quaternion4channels'],'all_other290_curves_exact':True,'prior81Actions_and_OFF_snapshot_preserved':True,'max_unaffected_geometry_component_error_m':maxunchanged,'max_nonthumb_bone_matrix_error':maxotherpose,'endpoints_base_neutral_geometry_error':{k:distance[k]['baseline_geometry_error_m'] for k in ['1','169']},'thumb_target_distances':distance,'maximum_actual_inclusive_pairs':maxcounts,'maximum_new_same_frame_inclusive_pairs':maxnew,'contact_verdict':'FAIL/HOLD' if maxnew.get('nonadjacent_all_body',0)>0 else 'SCOPED_NONADJACENT_SURFACE_PASS','scope':'ALL triangles with ANY LEFT thumb1/2/3 weight>.01 against ALL actual body triangles, including hand.L palm and other-digit weak weights. No palm/webbing exclusion. Shared-vertex/identical triangle raw intersections explicitly reported, compared same frame before/after; these are mesh adjacency, not certified penetration depth. Nonadjacent actual intersections and new pairs separately counted. Full volumetric containment/adjacent deformation quality/physical grasp not certified.','frames_private':rows,'visual_normal_speed':'PENDING','TierP':0}
(O/'LEFT_THUMB_C2_PRIVATE_MANIFEST.json').write_text(json.dumps(meta,indent=2),encoding='utf-8');print('ONE_THUMB_CANDIDATE',meta['contact_verdict'],meta['candidate_SHA'],distance,flush=True)
