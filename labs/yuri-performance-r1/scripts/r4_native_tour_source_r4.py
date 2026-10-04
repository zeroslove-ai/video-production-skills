"""ONE exact existing native Tour supply, original immutable R4, no cleanup/retiming."""
import bpy,sys,json,hashlib,math,ast,gzip,time,collections
from pathlib import Path
import numpy as np
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot,props
from r4_appearance_adapter import ReactionLane
from r4_native_tour_adapter_r1 import ACTIONS
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-native-tour-source-r4';O.mkdir(exist_ok=False);P=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/target-reference/Character_Master_NeckSkin_R4.blend');SHA='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(P)==SHA;start=time.perf_counter()
bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];names=list(bpy.data.actions.keys());before=snapshot(names);old=bpy.data.actions['MESHY_R2_BODY_Tour'];expected='e70ea471c4c0aa20efdb2ae05cbcecc49eff3e1c598e47100a1caa36fcf31202';assert len(names)==78 and before['actions'][old.name]==expected
def curves(a):return [f for l in a.layers for st in l.strips for ba in st.channelbags for f in ba.fcurves]
def record(a):return [(f.data_path,f.array_index,f.extrapolation,[(list(k.co),list(k.handle_left),list(k.handle_right),k.interpolation,k.handle_left_type,k.handle_right_type) for k in f.keyframe_points],[props(mo) for mo in f.modifiers]) for f in curves(a)]
fc=curves(old);times=sorted({float(k.co.x) for f in fc for k in f.keyframe_points});lo,hi=int(min(times)),int(max(times));assert min(times)==lo and max(times)==hi and lo==1 and hi==769;F=hi;fps=s.render.fps/s.render.fps_base;assert fps==24
tracks=collections.Counter();bones=set()
for f in fc:
 bn=f.data_path.split('"')[1] if f.data_path.startswith('pose.bones[') else '(object)';bones.add(bn);tracks[bn+' / '+f.data_path.rsplit('.',1)[-1]]+=1
print('NATIVE_TOUR_INTAKE',F,fps,len(fc),sorted(bones),flush=True)
for fn,defs in [('r4_native_walk_source_supply_r1.py',['contact']),('r4_existing_reach_contact_closure_r1.py',['geom'])]:
 tree=ast.parse((H/fn).read_text(encoding='utf8'));exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in defs],type_ignores=[]),'<pinned_actual_whole_mesh_helpers>','exec'))
fixed={};mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4'];body=bpy.data.objects[mesh_names[0]];gn={g.index:g.name for g in body.vertex_groups}
def evaluate():return {n:geom(bpy.data.objects[n]) for n in mesh_names}
neutral=evaluate();basepairs,rawbase=contact(neutral);v0=neutral[mesh_names[0]][0];floor=float(v0[:,2].min());footids={q:np.array([v.index for v in body.data.vertices if sum(g.weight for g in v.groups if gn[g.group] in ['foot.'+q,'toe.'+q])>.5],int) for q in ['L','R']};patch={q:ids[v0[ids,2]<=floor+.003] for q,ids in footids.items()};offworld={b.name:r.matrix_world@b.matrix for b in r.pose.bones};refhead=offworld['head'];refs={ob:bpy.data.objects[ob].matrix_world@bpy.data.objects[ob].pose.bones[bn].matrix for ob,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]};nativehash={};nativeMatrices=[]
lane=ReactionLane();lane.on(old.name)
for f in range(lo,hi+1):
 s.frame_set(f);bpy.context.view_layer.update();
 if (f-lo)%96==0:
  v=geom(body)[0];nativehash[f]=hashlib.sha256(v.tobytes()).hexdigest();print('TOUR_ORIGINAL_SELECTED_BODY_REFERENCE',f,flush=True)
 nativeMatrices.append({n:np.array(r.matrix_world@r.pose.bones[n].matrix) for n in r.pose.bones.keys()})
lane.off();assert snapshot(names)==before
a=old.copy();a.name=ACTIONS[r.name];a.use_fake_user=True;a['source_fps']=fps;a['source_Action_SHA']=expected;a['scope']='Exact original native Tour tracks/duration incl all original body channels. No retiming/rootfit/footcleanup/donor/rig/face modification.';assert record(a)==record(old);lanes=[];ln=ReactionLane();ln.on(a.name);lanes.append(ln)
for ob in ['Armature','Hair_Rig_R4']:
 ac=bpy.data.actions.new(ACTIONS[ob]);ac.use_fake_user=True;ac.slots.new(id_type='OBJECT',name=ob);ac['source_fps']=fps;ac['scope']='Existing full-world native transport, not seated additive translation';ln=ReactionLane(ob);ln.on(ac.name);lanes.append(ln)
for f in range(lo,hi+1):
 s.frame_set(f);bpy.context.view_layer.update();delta=(r.matrix_world@r.pose.bones['head'].matrix)@refhead.inverted();delta=Matrix.LocRotScale(delta.translation,delta.to_quaternion(),Vector((1,1,1)))
 for ob,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]:
  oo=bpy.data.objects[ob];pb=oo.pose.bones[bn];bb=pb.bone.matrix_local.inverted()@oo.matrix_world.inverted()@delta@refs[ob];pb.location=bb.translation;pb.rotation_quaternion=bb.to_quaternion();pb.keyframe_insert('location',frame=f,group=bn);pb.keyframe_insert('rotation_quaternion',frame=f,group=bn)
for ob in ['Armature','Hair_Rig_R4']:
 for ff in curves(bpy.data.actions[ACTIONS[ob]]):
  for k in ff.keyframe_points:k.interpolation='LINEAR'
rows=[];feet={q:[] for q in footids};ledger={'baseline':{k:sorted(v) for k,v in basepairs.items()},'frames':[]};endpoints={};prior=None;roots=[];rigidmax={ob:0 for ob in ['Armature','Hair_Rig_R4']};meshRigidMax={n:0 for n in mesh_names[1:]};baselineBodyMatrix=np.array(r.matrix_world);assemblyOff=np.array(bpy.data.objects['Assembly_Root'].matrix_world)
for f in range(lo,hi+1):
 s.frame_set(f);bpy.context.view_layer.update();data=evaluate();v=data[mesh_names[0]][0];assert f not in nativehash or hashlib.sha256(v.tobytes()).hexdigest()==nativehash[f];assert all(np.array_equal(np.array(r.matrix_world@r.pose.bones[n].matrix),z) for n,z in nativeMatrices[f-lo].items());ps,raw=contact(data);new={k:ps[k]-basepairs[k] for k in ps};delta=(r.matrix_world@r.pose.bones['head'].matrix)@refhead.inverted();delta=Matrix.LocRotScale(delta.translation,delta.to_quaternion(),Vector((1,1,1)));errors={}
 for ob,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]:
  oo=bpy.data.objects[ob];actual=oo.matrix_world@oo.pose.bones[bn].matrix;err=float(np.abs(np.array(actual)-np.array(delta@refs[ob])).max());rigidmax[ob]=max(rigidmax[ob],err);errors[ob]={'actual_world_matrix_private':np.array(actual).tolist(),'expected_full_world_matrix_private':np.array(delta@refs[ob]).tolist(),'max_matrix_component_error':err}
 dm=np.array(delta)
 for n in mesh_names[1:]:
  rigid=neutral[n][0]@dm[:3,:3].T+dm[:3,3];meshRigidMax[n]=max(meshRigidMax[n],float(np.abs(rigid-data[n][0]).max()))
 footrow={}
 for q,ids in footids.items():
  vv=v[ids];feet[q].append(vv.copy());footrow[q]={'lowest_floor_gap_m':float(vv[:,2].min()-floor),'near_floor3mm_vertices':int((vv[:,2]-floor<=.003).sum()),'below_floor1mm_vertices':int((vv[:,2]-floor<-.001).sum()),'original_patch_gap_min_max_m':[float((v[patch[q],2]-floor).min()),float((v[patch[q],2]-floor).max())]}
 mats={n:np.array(r.matrix_world@r.pose.bones[n].matrix).tolist() for n in ['root','pelvis','head','hand.L','hand.R','foot.L','foot.R']};roots.append({'frame':f,'assembly_world':np.array(bpy.data.objects['Assembly_Root'].matrix_world).tolist(),'body_object_world':np.array(r.matrix_world).tolist(),'body_joint_world':mats});step=float(np.linalg.norm(v-prior,axis=1).max()) if prior is not None else 0;prior=v.copy();rows.append({'frame':f,'finite':True,'all_native_bone_matrices_exact_original':True,'raw_BODY_geometry_vs_original_checked':f in nativehash,'actual_mesh_hash_private':{n:hashlib.sha256(z[0].tobytes()).hexdigest() for n,z in data.items()},'new_surface_pair_counts':{k:len(v) for k,v in new.items()},'absolute_surface_pair_counts':{k:len(v) for k,v in ps.items()},'feet':footrow,'max_body_vertex_step_m':step,'body_head_hair_actual_transform_private':errors});ledger['frames'].append({'frame':f,'new_pair_identities':{k:sorted(v) for k,v in new.items()}})
 if f in [lo,hi]:endpoints[f]={n:z[0].copy() for n,z in data.items()}
 if f%24==1:print('NATIVE_TOUR_ACTUAL_FRAME',f,{k:len(v) for k,v in new.items()},rigidmax,flush=True)
support={}
for q,allv in feet.items():
 vv=np.array(allv);patchix=np.array([np.where(footids[q]==ix)[0][0] for ix in patch[q]]);labels=[];persteps=[]
 for t in range(F):
  mask=np.where(vv[t,:,2]-floor<=.003)[0];common=np.intersect1d(mask,np.where(vv[max(0,t-1),:,2]-floor<=.003)[0]);step=float(np.linalg.norm(vv[t,common,:2]-vv[max(0,t-1),common,:2],axis=1).max()) if len(common) else None;gap=float(vv[t,:,2].min()-floor);label='airborne_kinematic' if gap>.003 else ('below_floor_kinematic' if gap<-.001 else ('planted_proximity_candidate' if step is not None and step<=.002 else 'moving_near_floor'));labels.append(label);persteps.append({'frame':t+lo,'label':label,'persistent_proximity_vertices':len(common),'persistent_XY_step_m':step,'lowest_gap_m':gap})
 intervals=[];a0=0
 for t in range(1,F+1):
  if t==F or labels[t]!=labels[a0]:intervals.append({'frames':[a0+lo,t-1+lo],'label':labels[a0],'duration_endpoint_seconds':max(0,t-a0-1)/fps});a0=t
 support[q]={'labels_are_proximity_motion_only_not_force_support':True,'classification_thresholds':{'gap_m':.003,'below_floor_m':-.001,'max_world_XY_step_m':.002},'intervals':intervals,'per_frame_private':persteps,'original_patch_max_XY_excursion_vs_source_OFF_m':float(np.linalg.norm(vv[:,patchix,:2]-v0[patch[q],:2],axis=2).max()),'whole_sole_XY_excursion_vs_first_m':float(np.linalg.norm(vv[:,:,:2]-vv[0,:,:2],axis=2).max()),'max_persistent_proximity_XY_step_m':max([z['persistent_XY_step_m'] for z in persteps if z['persistent_XY_step_m'] is not None],default=0),'minimum_gap_m':float(vv[:,:,2].min()-floor)}
rootSummary={}
for name in ['root','pelvis','head','hand.L','hand.R','foot.L','foot.R']:
 ar=np.array([x['body_joint_world'][name] for x in roots]);yaw=np.unwrap(np.arctan2(ar[:,1,0],ar[:,0,0]));rootSummary[name]={'position_range_xyz_m':np.ptp(ar[:,:3,3],axis=0).tolist(),'max_position_step_m':float(np.linalg.norm(np.diff(ar[:,:3,3],axis=0),axis=1).max()),'world_heading_yaw_range_degrees':float(np.ptp(yaw)*180/math.pi),'net_world_heading_yaw_degrees':float((yaw[-1]-yaw[0])*180/math.pi),'max_heading_yaw_step_degrees':float(np.abs(np.diff(yaw)).max()*180/math.pi)}
for ln in reversed(lanes):ln.off()
assert snapshot(names)==before and record(a)==record(old) and sha(P)==SHA
candidate=O/'Character_R4_NativeTour_EXPERIMENT_OFF_R1_20261005.blend';bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=False);bpy.ops.wm.open_mainfile(filepath=str(candidate),use_scripts=False);assert snapshot(names)==before
with gzip.open(O/'NATIVE_TOUR_SURFACE_IDENTITIES_PRIVATE_R1.json.gz','wt',encoding='utf8') as ff:json.dump(ledger,ff)
np.savez_compressed(O/'NATIVE_TOUR_ACTUAL_FEET_PRIVATE_R1.npz',**{q:np.array(v) for q,v in feet.items()},**{q+'_original_patch_ids':patch[q] for q in patch})
peaks={k:max(x['new_surface_pair_counts'][k] for x in rows) for k in basepairs};passScope=not any(peaks.values()) and all(v<=1e-5 for v in rigidmax.values());meta={'task':'ROOT_PM_NATIVE_SEAT_CLOSE_TO_TOUR_SOURCE_R1','source':str(P),'source_SHA':SHA,'source_action':'MESHY_R2_BODY_Tour','source_Action_SHA':expected,'source_Action_original_props_private':dict(bpy.data.actions['MESHY_R2_BODY_Tour'].items()),'source_action_curves':len(fc),'source_action_track_counts':dict(tracks),'native_pose_rotation_modes':{n:bpy.data.objects['Meshy_Fitted_Rig'].pose.bones[n].rotation_mode for n in bones if n in bpy.data.objects['Meshy_Fitted_Rig'].pose.bones},'original78_signature_private':before,'original78_OFF_and_fresh_serialized_signature_equal':True,'candidate':str(candidate),'candidate_SHA':sha(candidate),'candidate_bytes':candidate.stat().st_size,'library':'PENDING separate pure3Action existing Blender library-write job; author/data combined output cap64MiB preserved','actions':ACTIONS,'fps':fps,'frames':[lo,hi],'native_distinct_key_times':len(times),'all_original_tracks_copied_exact':True,'native_retime_factor':1,'endpoint_span_seconds':(hi-lo)/fps,'container_native_samples_seconds':F/fps,'all769_original_track_keys_handles_modifier_values_and_native_joint_matrices_exact':True,'nine_original_BODY_geometry_samples_exact_frames':sorted(nativehash),'all_frames_finite':True,'source_floor_world_z_m':floor,'root_turn_look_trajectory':rootSummary,'carrier_world_max_component_change_vs_original':max(float(np.abs(np.array(x['assembly_world'])-assemblyOff).max()) for x in roots),'body_object_world_max_component_change_vs_original':max(float(np.abs(np.array(x['body_object_world'])-baselineBodyMatrix).max()) for x in roots),'head_hair_full_world_transport_max_matrix_error':rigidmax,'head_hair_actual_vertex_max_component_error_vs_source_OFF_rigid_transport_m':meshRigidMax,'support':support,'all_surface_peak_new_vs_OFF':peaks,'original_OFF_absolute_pair_counts':{k:len(v) for k,v in basepairs.items()},'original_OFF_raw_contact_diagnostics':rawbase,'full_pair_identity_scope':'All weak/unweighted BODY HEAD HAIR triangles/self nonadjacent and cross with original vertex-triple IDs; shared-vertex/identical adjacency excluded. Baseline intersections retained. No penetration volume/depth/contact-force claim.','max_body_vertex_step_m':max(x['max_body_vertex_step_m'] for x in rows),'endpoint_geometry_vs_OFF_component_error_m':{str(f):{n:float(np.abs(z-neutral[n][0]).max()) for n,z in data.items()} for f,data in endpoints.items()},'all_rows_private':rows,'root_rows_private':roots,'scoped_motion_contact_pass':passScope,'verdict':'PASS_SOURCE_SCOPE_PENDING_VISUAL_OFF_RGBA' if passScope else 'FAIL_HOLD_NATIVE_TOUR_SURFACE_OR_ATTACHMENT','visual_1x':'PENDING_CAPTURE','TierP':0,'collector_elapsed_seconds':time.perf_counter()-start};(O/'NATIVE_TOUR_SOURCE_PRIVATE_R1.json').write_text(json.dumps(meta,indent=2),encoding='utf8');print('NATIVE_TOUR_SOURCE_DATA_COMPLETE',F,peaks,rigidmax,'PASS',passScope,flush=True)
