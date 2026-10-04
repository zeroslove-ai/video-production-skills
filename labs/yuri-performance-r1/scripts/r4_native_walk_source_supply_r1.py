"""ONE original Walk reuse: full native cadence/source preservation/contact/feet/video."""
import bpy,sys,json,hashlib,math,ast,gzip,time
from pathlib import Path
import numpy as np
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
from r4_native_walk_adapter_r1 import NativeWalkLane,ACTIONS
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-native-walk-source-r1';O.mkdir(exist_ok=False)
P=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/target-reference/Character_Master_NeckSkin_R4.blend');SHA='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(P)==SHA
def write(n,v): (O/n).write_text(json.dumps(v,indent=2),encoding='utf8')
start=time.perf_counter();bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];names=list(bpy.data.actions.keys());before=snapshot(names);assert len(names)==78
old=bpy.data.actions['MESHY_R2_BODY_WalkInPlace'];fps=s.render.fps/s.render.fps_base;assert fps==24
def curves(a):return [f for l in a.layers for st in l.strips for ba in st.channelbags for f in ba.fcurves]
def record(a):return [(f.data_path,f.array_index,f.extrapolation,[(list(k.co),list(k.handle_left),list(k.handle_right),k.interpolation,k.handle_left_type,k.handle_right_type) for k in f.keyframe_points]) for f in curves(a)]
fc=curves(old);frames=sorted({float(k.co.x) for f in fc for k in f.keyframe_points});assert [min(frames),max(frames)]==[1,97]
module=ast.parse((H/'r4_existing_reach_contact_closure_r1.py').read_text(encoding='utf8'));exec(compile(ast.Module(body=[x for x in module.body if isinstance(x,ast.FunctionDef) and x.name in ['geom','topweights']],type_ignores=[]),'<existing_pinned_actual_mesh_helpers>','exec'))
fixed={};body=bpy.data.objects['Meshy_Body_NeutralCovered'];groupnames={g.index:g.name for g in body.vertex_groups};bonegroups={g.index:g.name for g in body.vertex_groups if g.name in r.pose.bones}
mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4']
def evaluate():return {n:geom(bpy.data.objects[n]) for n in mesh_names}
def meshhash(v):return hashlib.sha256(v.tobytes()).hexdigest()
def contact(data):
 trees={n:BVHTree.FromPolygons(v.tolist(),t,all_triangles=True,epsilon=0) for n,(v,t,e) in data.items()};ps={};raw={}
 for n in mesh_names:
  t=data[n][1];non=set();adj=set();same=set()
  for i,j in trees[n].overlap(trees[n]):
   if i>j:continue
   a=tuple(sorted(t[i]));b=tuple(sorted(t[j]));key=tuple(sorted((a,b)))
   if a==b:same.add(key)
   elif set(a)&set(b):adj.add(key)
   else:non.add(key)
  ps[n+'__self_nonadjacent']=non;raw[n]={'shared_vertex_adjacent':len(adj),'identical_triangles':len(same),'actual_triangles':len(t)}
 for a,b in [(mesh_names[0],mesh_names[1]),(mesh_names[0],mesh_names[2]),(mesh_names[1],mesh_names[2])]:
  ta=data[a][1];tb=data[b][1];ps[a+'__'+b]={(tuple(sorted(ta[i])),tuple(sorted(tb[j]))) for i,j in trees[a].overlap(trees[b])}
 return ps,raw
neutral=evaluate();basepairs,baseraw=contact(neutral);v0=neutral[mesh_names[0]][0];floor=float(v0[:,2].min());edges=neutral[mesh_names[0]][2];base_lengths=np.linalg.norm(v0[edges[:,0]]-v0[edges[:,1]],axis=1);valid=base_lengths>1e-6
region_vertices={}
for n in ['pelvis']+[n+'.'+side for side in ['L','R'] for n in ['clavicle','upper_arm','forearm','thigh','shin','foot']]:
 gi=body.vertex_groups[n].index;region_vertices[n]={v.index for v in body.data.vertices if any(g.group==gi and g.weight>.01 for g in v.groups)}
region_edges={n:np.array([i for i,e in enumerate(edges) if valid[i] and any(int(j) in ids for j in e)],int) for n,ids in region_vertices.items()}
footids={side:np.array([v.index for v in body.data.vertices if sum(g.weight for g in v.groups if groupnames[g.group] in ['foot.'+side,'toe.'+side])>.5],int) for side in ['L','R']};assert all(len(v)>0 for v in footids.values())
weak_diagnostics={n:{'actual_triangles':len(x[1]),'all_triangles_included_even_weak_or_unweighted':True} for n,x in neutral.items()}
native_hashes=[];lane=ReactionLane();lane.on(old.name)
for f in range(1,98):
 s.frame_set(f);bpy.context.view_layer.update();native_hashes.append(meshhash(geom(body)[0]))
lane.off();assert snapshot(names)==before
refhead=r.matrix_world@r.pose.bones['head'].matrix;refs={obj:bpy.data.objects[obj].matrix_world@bpy.data.objects[obj].pose.bones[bn].matrix for obj,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]}
a=old.copy();a.name=ACTIONS[r.name];a.use_fake_user=True;a['source_fps']=fps;a['source_action']=old.name;a['source_action_SHA']=before['actions'][old.name];a['scope']='Exact full original native Walk curves; no retiming, root/foot cleanup, new rig or physical walk proof';assert record(a)==record(old)
lane=ReactionLane();lane.on(a.name);lanes=[lane]
for obj in ['Armature','Hair_Rig_R4']:
 ac=bpy.data.actions.new(ACTIONS[obj]);ac.use_fake_user=True;ac.slots.new(id_type='OBJECT',name=obj);ac['source_fps']=fps;ac['scope']='Rigid existing head transport only; original face/gaze/keys/drivers untouched';ln=ReactionLane(obj);ln.on(ac.name);lanes.append(ln)
for f in range(1,98):
 s.frame_set(f);bpy.context.view_layer.update();delta=(r.matrix_world@r.pose.bones['head'].matrix)@refhead.inverted();delta=Matrix.LocRotScale(delta.translation,delta.to_quaternion(),Vector((1,1,1)))
 for obj,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]:
  ob=bpy.data.objects[obj];pb=ob.pose.bones[bn];basis=pb.bone.matrix_local.inverted()@ob.matrix_world.inverted()@delta@refs[obj];pb.location=basis.translation;pb.rotation_quaternion=basis.to_quaternion();pb.keyframe_insert('location',frame=f,group=bn);pb.keyframe_insert('rotation_quaternion',frame=f,group=bn)
for obj in ['Armature','Hair_Rig_R4']:
 for f in curves(bpy.data.actions[ACTIONS[obj]]):
  for k in f.keyframe_points:k.interpolation='LINEAR'
rows=[];private_pairs={'baseline':{k:[list(p) for p in sorted(v)] for k,v in basepairs.items()},'frames':[]};rootrows=[];bone_motion=[];geometryframes=[];footframes={side:[] for side in ['L','R']};prior=None;raw_bones=[]
lower=['root','pelvis']+[n+'.'+side for side in ['L','R'] for n in ['thigh','shin','foot','toe']]
for f in range(1,98):
 s.frame_set(f);bpy.context.view_layer.update();data=evaluate();v=data[mesh_names[0]][0];assert meshhash(v)==native_hashes[f-1];pairs,raw=contact(data);new={k:len(v-basepairs[k]) for k,v in pairs.items()};lens=np.linalg.norm(v[edges[:,0]]-v[edges[:,1]],axis=1);rat=lens[valid]/base_lengths[valid];deform={}
 for n,ids in region_edges.items():
  rr=lens[ids]/base_lengths[ids];ix=ids[int(np.argmax(rr))];deform[n]={'p01_p99':np.quantile(rr,[.01,.99]).tolist(),'min_ratio':float(rr.min()),'max_ratio':float(rr.max()),'worst_source_length_m':float(base_lengths[ix]),'worst_posed_length_m':float(lens[ix]),'worst_dominant_bones':topweights(edges[ix])}
 foot={}
 for side,ids in footids.items():
  vv=v[ids].copy();footframes[side].append(vv);gaps=vv[:,2]-floor;contactids=np.where(gaps<=.003)[0];foot[side]={'whole_foot_vertices':len(ids),'minimum_floor_gap_m':float(gaps.min()),'source_rest_patch_floor_min_max_m':None,'contact_candidate_vertex_count_3mm':len(contactids),'whole_foot_centroid_world_m':vv.mean(axis=0).tolist(),'below_floor_vertices_1mm':int((gaps<-.001).sum())}
  restpatch=np.where(v0[ids,2]<=v0[ids,2].min()+.002)[0];foot[side]['source_rest_patch_vertices_2mm']=len(restpatch);foot[side]['source_rest_patch_floor_min_max_m']=[float(gaps[restpatch].min()),float(gaps[restpatch].max())]
 root={'assembly_world':np.array(bpy.data.objects['Assembly_Root'].matrix_world).tolist(),'root_bone_world':np.array(r.matrix_world@r.pose.bones['root'].matrix).tolist(),'pelvis_head_world_m':list(r.matrix_world@r.pose.bones['pelvis'].head)};rootrows.append(root)
 mats={n:np.array(r.matrix_world@r.pose.bones[n].matrix) for n in lower};raw_bones.append(mats);geometryframes.append({n:x[0].copy() for n,x in data.items()} if f in [1,2,96,97] else None)
 step=float(np.linalg.norm(v-prior,axis=1).max()) if prior is not None else 0;prior=v.copy()
 rows.append({'frame':f,'time_seconds':(f-1)/fps,'finite':True,'topology_equal':True,'body_hash_exact_original_native_same_frame':True,'absolute_nonadjacent_pair_counts':{k:len(v) for k,v in pairs.items()},'new_vs_source_OFF_pair_counts':new,'shared_vertex_raw':raw,'deformation_regions':deform,'all_edge_min_max':[float(rat.min()),float(rat.max())],'all_edge_p01_p99':np.quantile(rat,[.01,.99]).tolist(),'max_body_vertex_step_m':step,'feet':foot})
 private_pairs['frames'].append({'frame':f,'pair_identity_sha256':{k:hashlib.sha256(json.dumps(sorted(v)).encode()).hexdigest() for k,v in pairs.items()},'new_pairs_exact':{k:[list(p) for p in sorted(v-basepairs[k])] for k,v in pairs.items()}})
 if f%12==1:print('NATIVE_WALK_FULL_SAMPLE',f,new,{q:foot[q]['minimum_floor_gap_m'] for q in foot},flush=True)
first,last=geometryframes[0],geometryframes[-1];prevlast=geometryframes[-2];nextfirst=geometryframes[1]
loop={'geometry_first_last_component_error_m':{n:float(np.max(np.abs(first[n]-last[n]))) for n in mesh_names},'last_to_first_native_velocity_difference_max_m_per_s':{n:float(np.linalg.norm(((last[n]-prevlast[n])-(nextfirst[n]-first[n]))*fps,axis=1).max()) for n in mesh_names},'lower_world_matrix_first_last_error':{n:float(np.max(np.abs(raw_bones[0][n]-raw_bones[-1][n]))) for n in lower},'first_last_vs_OFF_component_error_m':{str(f):{n:float(np.max(np.abs(geometryframes[f-1][n]-neutral[n][0]))) for n in mesh_names} for f in [1,97]}}
foot_summary={}
for side,vvs in footframes.items():
 vv=np.array(vvs);contacts=[set(np.where(x[:,2]-floor<=.003)[0].tolist()) for x in vv];steps=[]
 for i in range(1,len(vv)):
  ids=sorted(contacts[i-1]&contacts[i]);steps.append({'frames':[i,i+1],'persistent_contact_vertices':len(ids),'max_world_xy_step_m':float(np.linalg.norm(vv[i,ids,:2]-vv[i-1,ids,:2],axis=1).max()) if ids else None,'median_world_xy_step_m':float(np.median(np.linalg.norm(vv[i,ids,:2]-vv[i-1,ids,:2],axis=1))) if ids else None})
 intervals=[];i=0
 while i<len(contacts):
  if not contacts[i]:i+=1;continue
  j=i
  while j+1<len(contacts) and contacts[j+1]:j+=1
  ids=sorted(set.intersection(*contacts[i:j+1]));exc=float(np.linalg.norm(vv[i:j+1,ids,:2]-vv[i,ids,:2],axis=2).max()) if ids else None;intervals.append({'frames':[i+1,j+1],'common_contact_vertices':len(ids),'max_anchored_world_xy_displacement_m':exc,'contact_basis':'min actual foot gap<=3mm, kinematic proximity only; includes penetration, not force/support proof'});i=j+1
 foot_summary[side]={'minimum_gap_m':min(x['feet'][side]['minimum_floor_gap_m'] for x in rows),'maximum_minimum_gap_m':max(x['feet'][side]['minimum_floor_gap_m'] for x in rows),'frames_near_floor3mm':sum(bool(c) for c in contacts),'persistent_vertex_world_xy_steps':steps,'near_floor_intervals':intervals,'maximum_persistent_contact_xy_step_m':max([x['max_world_xy_step_m'] for x in steps if x['max_world_xy_step_m'] is not None],default=None),'loop_foot_world_error_m':float(np.linalg.norm(vv[0]-vv[-1],axis=1).max())}
roots={k:np.array([x[k] for x in rootrows]) for k in rootrows[0]};trajectory={'assembly_translation_range_xyz_m':np.ptp(roots['assembly_world'][:,:3,3],axis=0).tolist(),'root_bone_translation_range_xyz_m':np.ptp(roots['root_bone_world'][:,:3,3],axis=0).tolist(),'pelvis_head_range_xyz_m':np.ptp(roots['pelvis_head_world_m'],axis=0).tolist(),'assembly_max_matrix_step':float(np.abs(np.diff(roots['assembly_world'],axis=0)).max()),'root_bone_max_world_translation_step_m':float(np.linalg.norm(np.diff(roots['root_bone_world'][:,:3,3],axis=0),axis=1).max()),'lower_motion_world_matrix_peak_vs_first':{n:max(float(np.max(np.abs(x[n]-raw_bones[0][n]))) for x in raw_bones) for n in lower}}
for ln in reversed(lanes):ln.off()
assert record(a)==record(old) and snapshot(names)==before and sha(P)==SHA
candidate=O/'Character_R4_NativeWalkInPlace_CANDIDATE_OFF_R1_20261005.blend';bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=False);assert snapshot(names)==before
library=O/'YURI_R4_NATIVE_WALK_ACTIONS_ONLY_R1.blend';bpy.data.libraries.write(str(library),{bpy.data.actions[n] for n in ACTIONS.values()},fake_user=True)
with bpy.data.libraries.load(str(library),link=False) as (src,dst):assert sorted(src.actions)==sorted(ACTIONS.values()) and not src.objects and not src.meshes and not src.armatures
candidate_sha=sha(candidate);bpy.ops.wm.open_mainfile(filepath=str(candidate),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];assert snapshot(names)==before
with gzip.open(O/'NATIVE_WALK_TRIANGLE_IDENTITIES_PRIVATE_R1.json.gz','wt',encoding='utf8') as f:json.dump(private_pairs,f)
meta={'task':'ROOT_PM_NATIVE_WALK_SOURCE_PRODUCT_PREP_R1','source':str(P),'source_SHA':SHA,'candidate':str(candidate),'candidate_SHA':candidate_sha,'candidate_bytes':candidate.stat().st_size,'library':{'file':str(library),'sha256':sha(library),'bytes':library.stat().st_size,'actions':3,'objects':0,'meshes':0,'armatures':0},'actions':ACTIONS,'source_action':'MESHY_R2_BODY_WalkInPlace','source_action_SHA':before['actions']['MESHY_R2_BODY_WalkInPlace'],'source_action_properties_private':dict(bpy.data.actions['MESHY_R2_BODY_WalkInPlace'].items()),'source_scene_fps':fps,'source_scene_fps_base':s.render.fps_base,'source_native_frames':[1,97],'distinct_key_times':len(frames),'source_body_curves':len(fc),'all_native_body_curves_copied_exact':True,'all97_body_hashes_exact_original_native_same_frame':True,'native_retiming_factor':1,'endpoint_span_seconds':96/fps,'encoded97sample_duration_seconds':97/fps,'loop_two_cycle_unique96_encode_seconds':192/fps,'original78_OFF_raw_full_snapshot_and_candidate_reopen_equal':True,'source_and_prior_candidates_not_saved':True,'source_floor_plane_world_z_m':floor,'floor_basis':'minimum original OFF actual body vertexZ; no solver/contact/translation correction','weak_weight_inclusive_scope':weak_diagnostics,'source_OFF_absolute_nonadjacent_counts':{k:len(v) for k,v in basepairs.items()},'source_OFF_shared_vertex_raw':baseraw,'all97_rows_private':rows,'root_trajectory':trajectory,'root_rows_private':rootrows,'loop':loop,'feet':foot_summary,'scope':'All actual body/head/hair triangle surface identities including weak/unweighted vertices; identical/shared-vertex same-mesh adjacency separated. Baseline identities unchanged expected contacts reported; no volume/depth or force balance. In-place foot-local motion is not translational walk proof. Foot proximity3mm not actual planted force contact. No foot/root cleanup or product/Unity/F2/TierP promotion.','surface_verdict':'SCOPED_ALL97_NEW_SURFACE_ZERO' if not any(any(x['new_vs_source_OFF_pair_counts'].values()) for x in rows) else 'FAIL_HOLD_NEW_SURFACE_INTERSECTIONS','foot_verdict':'SOURCE_COORDINATE_MEASUREMENTS_HOLD_WORLD_PLANT_ACCEPTANCE','visual':'PENDING_ORIGINAL_NATIVE_1X','TierP':0}
write('NATIVE_WALK_SOURCE_PRIVATE_R1.json',meta)
# Necessary source proof, one candidate, three fixed fullbody views; original native24fps.
cam=s.camera;savecam=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width);changes=[(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',2),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',320),(s.render,'resolution_y',320),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','JPEG'),(s.render.image_settings,'color_mode','RGB'),(s.render.image_settings,'color_depth','8'),(s.render.image_settings,'quality',92),(s.render,'filepath','')];saves=[(ob,k,getattr(ob,k)) for ob,k,_ in changes]
for ob,k,v in changes:setattr(ob,k,v)
lane=NativeWalkLane();lane.on();views={}
for view,direction in [('front',(0,-1,0)),('quarter',(.6,-1,0)),('side',(1,0,0))]:
 p=O/view;p.mkdir();target=Vector((.002,-.028,.53));cam.data.type='ORTHO';cam.data.ortho_scale=1.18;cam.location=target+Vector(direction).normalized()*.8;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();views[view]={'type':'ORTHO','ortho_scale':1.18,'target':list(target),'location':list(cam.location),'rotation_euler':list(cam.rotation_euler),'lens_mm':cam.data.lens,'sensor_width_mm':cam.data.sensor_width,'fixed':True,'resolution':[320,320],'fps':fps,'frames':[1,97]}
 for f in range(1,98):s.frame_set(f);bpy.context.view_layer.update();s.render.filepath=str(p/f'{f:04}.jpg');bpy.ops.render.render(write_still=True)
 print('NATIVE_WALK_COMPLETE_VIEW',view,97,flush=True)
lane.off();cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width=savecam;s.render.resolution_x=960;s.render.resolution_y=920;s.cycles.samples=8;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(O/'NATIVE_WALK_OFF_SOURCE_CAMERA_NEUTRAL_R1.png');bpy.ops.render.render(write_still=True)
for ob,k,v in saves:setattr(ob,k,v)
assert snapshot(names)==before and sha(candidate)==candidate_sha and sha(P)==SHA
meta['views']=views;meta['complete97_three_views']=True;meta['temporary_render_camera_settings_restored_full_raw_snapshot_equal']=True;meta['collector_elapsed_seconds']=time.perf_counter()-start;write('NATIVE_WALK_SOURCE_PRIVATE_R1.json',meta);print('NATIVE_WALK_ONE_SOURCE_SUPPLY_COMPLETE',meta['surface_verdict'],candidate_sha,flush=True)
