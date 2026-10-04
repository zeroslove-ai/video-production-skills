"""Failure91/92 discriminator: one original control, rigid math, no whole97 rerender."""
import bpy,sys,json,hashlib,gzip,ast,math
from pathlib import Path
import numpy as np
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
from r4_native_walk_adapter_r1 import NativeWalkLane,ACTIONS
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-walk-head-boundary-r1';O.mkdir(exist_ok=False);W=B/'alpha-native-walk-source-r1';meta=json.loads((W/'NATIVE_WALK_SOURCE_PRIVATE_R1.json').read_bytes());P=Path(meta['source']);C=Path(meta['candidate']);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(P)==meta['source_SHA'] and sha(C)==meta['candidate_SHA']
with gzip.open(W/'NATIVE_WALK_TRIANGLE_IDENTITIES_PRIVATE_R1.json.gz','rt',encoding='utf8') as f:ledger=json.load(f)
saved={x['frame']:x for x in ledger['frames'] if x['frame'] in [91,92]};mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4'];fixed={}
module=ast.parse((H/'r4_existing_reach_contact_closure_r1.py').read_text(encoding='utf8'));exec(compile(ast.Module(body=[x for x in module.body if isinstance(x,ast.FunctionDef) and x.name=='geom'],type_ignores=[]),'<pinned_actual_mesh_helper>','exec'))
def evaluate():return {n:geom(bpy.data.objects[n]) for n in mesh_names}
def selfpairs(v,t,eps=0):
 tree=BVHTree.FromPolygons(v.tolist(),t,all_triangles=True,epsilon=eps);ps=set()
 for i,j in tree.overlap(tree):
  if i>=j:continue
  a=tuple(sorted(t[i]));b=tuple(sorted(t[j]))
  if not(set(a)&set(b)):ps.add(tuple(sorted((a,b))))
 return ps
def pairs(data,eps=0):
 trees={n:BVHTree.FromPolygons(v.tolist(),t,all_triangles=True,epsilon=eps) for n,(v,t,e) in data.items()};out={n+'__self_nonadjacent':selfpairs(data[n][0],data[n][1],eps) for n in mesh_names}
 for a,b in [(mesh_names[0],mesh_names[1]),(mesh_names[0],mesh_names[2]),(mesh_names[1],mesh_names[2])]:
  out[a+'__'+b]={(tuple(sorted(data[a][1][i])),tuple(sorted(data[b][1][j]))) for i,j in trees[a].overlap(trees[b])}
 return out
def drvstate():
 state={}
 for n in ['Armature','Hair_Rig_R4']:
  ob=bpy.data.objects[n];state[n]={'nonroot_basis':{p.name:np.array(p.matrix_basis) for p in ob.pose.bones if p.name not in ['Root','Hair_HeadRoot']},'root_mode':ob.pose.bones['Root' if n=='Armature' else 'Hair_HeadRoot'].rotation_mode,'constraints':{p.name:[{'name':c.name,'type':c.type,'mute':c.mute,'influence':c.influence,'target':getattr(getattr(c,'target',None),'name',None),'subtarget':getattr(c,'subtarget',None)} for c in p.constraints] for p in ob.pose.bones if p.constraints},'object_world':np.array(ob.matrix_world)}
 state['shape_values']={k.name:float(k.value) for k in bpy.data.objects['Character_Body_Head'].data.shape_keys.key_blocks};return state
def maxstate(a,b):return {'max_nonroot_basis_error':{n:max(float(np.abs(a[n]['nonroot_basis'][p]-b[n]['nonroot_basis'][p]).max()) for p in a[n]['nonroot_basis']) for n in ['Armature','Hair_Rig_R4']},'max_original_shape_value_delta':max(abs(a['shape_values'][k]-b['shape_values'][k]) for k in a['shape_values'])}
def delta():
 d=(r.matrix_world@r.pose.bones['head'].matrix)@refhead.inverted();return Matrix.LocRotScale(d.translation,d.to_quaternion(),Vector((1,1,1)))
def rigid(data,d):
 w=np.array(d);return {n:(v@w[:3,:3].T+w[:3,3],t,e) for n,(v,t,e) in data.items()}
def attributes(n):
 ob=bpy.data.objects[n];ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();m.calc_loop_triangles();tri={tuple(sorted(x.vertices)):{'polygon':x.polygon_index,'material_slot':m.polygons[x.polygon_index].material_index,'material':ob.material_slots[m.polygons[x.polygon_index].material_index].name} for x in m.loop_triangles};ev.to_mesh_clear();return tri
def vertexregion(n,ids):
 ob=bpy.data.objects[n];weights={}
 for i in ids:
  for g in ob.data.vertices[i].groups:
   if g.weight>.001:weights[ob.vertex_groups[g.group].name]=weights.get(ob.vertex_groups[g.group].name,0)+g.weight
 shapes=[]
 if ob.data.shape_keys:
  basis=ob.data.shape_keys.reference_key
  for k in ob.data.shape_keys.key_blocks:
   if k==basis:continue
   amp=max((k.data[i].co-basis.data[i].co).length for i in ids)
   if amp>1e-6:shapes.append([k.name,float(amp)])
 return {'bone_weights':sorted(weights.items(),key=lambda x:-x[1])[:8],'source_ShapeKey_support':sorted(shapes,key=lambda x:-x[1])[:12]}
def pair_detail(a,b,ta,tb,data,attrs):
 va=data[a][0][list(ta)];vb=data[b][0][list(tb)];na=np.cross(va[1]-va[0],va[2]-va[0]);nb=np.cross(vb[1]-vb[0],vb[2]-vb[0]);la=np.linalg.norm(na);lb=np.linalg.norm(nb);distance=np.linalg.norm(va[:,None,:]-vb[None,:,:],axis=2)
 return {'objects':[a,b],'triangles_private':[list(ta),list(tb)],'regions':[vertexregion(a,ta),vertexregion(b,tb)],'materials':[attrs[a][ta],attrs[b][tb]],'world_center_m':np.concatenate([va,vb]).mean(axis=0).tolist(),'world_bounds_m':[np.concatenate([va,vb]).min(axis=0).tolist(),np.concatenate([va,vb]).max(axis=0).tolist()],'nearest_vertex_distance_m':float(distance.min()),'triangle_area_m2':[float(la/2),float(lb/2)],'absolute_normal_dot':float(abs(np.dot(na,nb)/(la*lb))) if la*lb>1e-30 else None,'opposite_plane_max_distance_m':[float(np.abs((vb-va[0])@na/la).max()) if la>1e-20 else None,float(np.abs((va-vb[0])@nb/lb).max()) if lb>1e-20 else None]}
bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];source_names=list(bpy.data.actions.keys());source_sig=snapshot(source_names);neutral=evaluate();state0=drvstate();refhead=r.matrix_world@r.pose.bones['head'].matrix;refs={n:bpy.data.objects[n].matrix_world@bpy.data.objects[n].pose.bones[bn].matrix for n,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]};basepairs=pairs(neutral)
# Existing cached coordinates reused only after numerical identity check, never assumed canonical.
cache=B/'o1-morph67-two-input-native-compare-r1/NEUTRAL_FULL_SOURCE_PRIVATE_R1.npz'
with np.load(cache,allow_pickle=False) as z:cached=z['local_position']@z['world_matrix'][:3,:3].T+z['world_matrix'][:3,3]
cache_error=float(np.abs(cached-neutral['Character_Body_Head'][0]).max());np.savez_compressed(O/'ORIGINAL_NEUTRAL_CACHED_REFERENCE_PRIVATE_R1.npz',cached_head_world=cached,actual_source_head_world=neutral['Character_Body_Head'][0]);control={};ln=ReactionLane();ln.on('MESHY_R2_BODY_WalkInPlace')
for f in [91,92]:
 s.frame_set(f);bpy.context.view_layer.update();data=evaluate();ps=pairs(data);control[f]={'data':data,'pairs':ps,'state':drvstate(),'delta':delta(),'root_world':{n:np.array(bpy.data.objects[n].matrix_world@bpy.data.objects[n].pose.bones[bn].matrix) for n,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]}}
ln.off();assert snapshot(source_names)==source_sig
bpy.ops.wm.open_mainfile(filepath=str(C),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];names=list(bpy.data.actions.keys());before=snapshot(names);assert snapshot(source_names)==source_sig;full={};lane=NativeWalkLane();lane.on();details=[]
for f in [91,92]:
 s.frame_set(f);bpy.context.view_layer.update();data=evaluate();ps=pairs(data);d=delta();expected=rigid(neutral,d);inverse=d.inverted();back=rigid(data,inverse);attrs={n:attributes(n) for n in mesh_names};current_state=drvstate();assert np.array_equal(data[mesh_names[0]][0],control[f]['data'][mesh_names[0]][0]);residual={n:float(np.linalg.norm(data[n][0]-expected[n][0],axis=1).max()) for n in mesh_names[1:]};new={k:v-basepairs[k] for k,v in ps.items()};assert all(new[k]=={tuple(tuple(z) for z in p) for p in saved[f]['new_pairs_exact'][k]} for k in new)
 detail=[]
 for key,ids in new.items():
  if not ids:continue
  if key.endswith('__self_nonadjacent'):a=b=key.split('__')[0]
  else:a,b=key.split('__')
  for ta,tb in sorted(ids):detail.append({'category':key,**pair_detail(a,b,ta,tb,data,attrs)})
 robust={}
 for eps in [0,2e-7,2e-6]:
  bp=pairs(neutral,eps);pp=pairs(back,eps);robust[str(eps)]={k:len(v-bp[k]) for k,v in pp.items()}
 root_error={}
 for obj,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]:root_error[obj]=float(np.abs(np.array(bpy.data.objects[obj].matrix_world@bpy.data.objects[obj].pose.bones[bn].matrix)-np.array(d@refs[obj])).max())
 full[f]={'data':data,'state':current_state,'rigid_residual_m':residual,'root_world_matrix_vs_rigid_target_error':root_error,'driver_basis_shape_vs_original_control':maxstate(current_state,control[f]['state']),'body_same_original_control':True,'raw_new':{k:len(v) for k,v in new.items()},'control_raw_new':{k:len(v-basepairs[k]) for k,v in control[f]['pairs'].items()},'head_hair_back_reference_epsilon_sensitivity':robust,'details_private':detail,'rigid_expected':expected,'delta':d};details.append({'frame':f,**{k:v for k,v in full[f].items() if k not in ['data','state','rigid_expected','delta']}})
 np.savez_compressed(O/f'FAILED_FRAME_{f}_SAVED_ACTION_COORDINATES_PRIVATE_R1.npz',**{label+'__'+n:data0[n][0] for label,data0 in [('actual',data),('original_body_only',control[f]['data']),('mathematical_rigid',expected),('inverse_rigid_reference',back)] for n in mesh_names},unit_rigid_delta=np.array(d))
 print('HEAD_BOUNDARY_FAILURE_DISCRIMINATOR',f,residual,root_error,full[f]['driver_basis_shape_vs_original_control'],flush=True)
lane.off();assert snapshot(names)==before
# A minimal remedy is justified only by nonrigid root-domain error while nonroot drivers/bases stay unchanged.
proven_root_fault=all(max(x['rigid_residual_m'].values())>1e-4 and max(x['root_world_matrix_vs_rigid_target_error'].values())>5e-5 and max(x['driver_basis_shape_vs_original_control']['max_nonroot_basis_error'].values())==0 and x['driver_basis_shape_vs_original_control']['max_original_shape_value_delta']==0 for x in full.values())
fix=None
if proven_root_fault:
 # One object-level rigid transport alternative; existing root pose/driver/rest untouched.
 objects={n:(ob.location.copy(),ob.rotation_euler.copy(),ob.rotation_quaternion.copy(),ob.rotation_axis_angle[:],ob.scale.copy()) for n in ['Armature','Hair_Rig_R4'] for ob in [bpy.data.objects[n]]};new_actions={'Meshy_Fitted_Rig':ACTIONS['Meshy_Fitted_Rig']};ln=ReactionLane();ln.on(ACTIONS['Meshy_Fitted_Rig']);riglanes=[]
 for n in ['Armature','Hair_Rig_R4']:
  ac=bpy.data.actions.new('YURI_R4_NATIVE_WALK_'+('HEAD' if n=='Armature' else 'HAIR')+'_OBJECT_RIGID_C1');ac.use_fake_user=True;ac.slots.new(id_type='OBJECT',name=n);ac['source_fps']=24;new_actions[n]=ac.name;rl=ReactionLane(n);rl.on(ac.name);riglanes.append(rl)
 for f in range(1,98):
  s.frame_set(f);bpy.context.view_layer.update();d=delta()
  for n in ['Armature','Hair_Rig_R4']:
   ob=bpy.data.objects[n];ob.matrix_world=d@Matrix(state0[n]['object_world'].tolist());ob.keyframe_insert('location',frame=f);ob.keyframe_insert('scale',frame=f);ob.keyframe_insert('rotation_quaternion' if ob.rotation_mode=='QUATERNION' else 'rotation_euler',frame=f)
 for rl in reversed(riglanes):rl.off()
 ln.off()
 for n,v in objects.items():ob=bpy.data.objects[n];ob.location,ob.rotation_euler,ob.rotation_quaternion,ob.rotation_axis_angle,ob.scale=v
 bpy.context.view_layer.update();assert snapshot(names)==before and snapshot(source_names)==source_sig
 fixfile=O/'Character_R4_Walk_HeadObjectTransport_CANDIDATE_OFF_C1_20261005.blend';bpy.ops.wm.save_as_mainfile(filepath=str(fixfile),relative_remap=False);fixlib=O/'YURI_R4_WALK_HEAD_OBJECT_TRANSPORT_ACTIONS_ONLY_C1.blend';bpy.data.libraries.write(str(fixlib),{bpy.data.actions[n] for n in new_actions.values()},fake_user=True);fix={'candidate':str(fixfile),'candidate_SHA':sha(fixfile),'library':str(fixlib),'library_SHA':sha(fixlib),'actions':new_actions,'status':'ONE_MINIMAL_SOURCE_ROOT_DOMAIN_CANDIDATE_PENDING_AFFECTED_FRAME_TEST'}
class ObjectFixLane:
 def on(self):
  self.saved={n:(ob.location.copy(),ob.rotation_euler.copy(),ob.rotation_quaternion.copy(),ob.rotation_axis_angle[:],ob.scale.copy()) for n in ['Armature','Hair_Rig_R4'] for ob in [bpy.data.objects[n]]};self.lanes=[]
  for n,a in fix['actions'].items():rl=ReactionLane(n);rl.on(a);self.lanes.append(rl)
 def off(self):
  for rl in reversed(self.lanes):rl.off()
  for n,v in self.saved.items():ob=bpy.data.objects[n];ob.location,ob.rotation_euler,ob.rotation_quaternion,ob.rotation_axis_angle,ob.scale=v
  bpy.context.view_layer.update()
if fix:
 q=ObjectFixLane();q.on();tests=[]
 for f in [91,92]:
  s.frame_set(f);bpy.context.view_layer.update();v=evaluate();ex=rigid(neutral,delta());res={n:float(np.linalg.norm(v[n][0]-ex[n][0],axis=1).max()) for n in mesh_names[1:]};ps=pairs(v);tests.append({'frame':f,'rigid_residual_m':res,'old_residual_m':full[f]['rigid_residual_m'],'new_pair_counts':{k:len(z-basepairs[k]) for k,z in ps.items()}})
 q.off();assert snapshot(names)==before;fix['affected_tests']=tests;fix['status']='SCOPED_ROOT_RESIDUAL_IMPROVED_CONTACT_HOLD' if all(max(t['rigid_residual_m'].values())<max(t['old_residual_m'].values())/10 for t in tests) else 'FAIL_HOLD_ONE_MINIMAL_CANDIDATE_STOP'

# No invented visible-defect verdict: raw identities, anatomy, exact preserved drivers and view proof remain separate.
maxres=max(max(x['rigid_residual_m'].values()) for x in full.values());maxbasis=max(max(x['driver_basis_shape_vs_original_control']['max_nonroot_basis_error'].values()) for x in full.values());maxshape=max(x['driver_basis_shape_vs_original_control']['max_original_shape_value_delta'] for x in full.values());result={'task':'ROOT_PM_WALK_CLOSE_TO_HEAD_BOUNDARY_R1','source_SHA':meta['source_SHA'],'old_candidate_SHA':meta['candidate_SHA'],'old_library_SHA':meta['library']['sha256'],'failure_frames':[91,92],'one_original_control':'original BODY_WalkInPlace, no additive face/hair transport; same91/92 and affected74..97 only, acceptedIdle not rerun','existing_triangle_ledger_sha256':sha(W/'NATIVE_WALK_TRIANGLE_IDENTITIES_PRIVATE_R1.json.gz'),'cached_original_head_source_coordinates_sha256':sha(cache),'cached_vs_actual_original_OFF_max_component_error_m':cache_error,'frames_private':details,'max_actual_head_hair_vs_mathematical_rigid_residual_m':maxres,'max_nonroot_basis_delta_vs_original_control':maxbasis,'max_original_shape_value_delta_vs_original_control':maxshape,'proven_nonrigid_root_domain_fault':proven_root_fault,'minimal_candidate':fix,'source78_prior81_OFF_raw_snapshot_equal':True,'old_source_candidate_library_bytes_unchanged':True,'triangles_include_hidden_or_internal_or_seam_geometry_not_visibility_or_depth_certification':True,'classification':'RIGID_PRECISION_BOUNDARY_RESEARCH_NO_CANDIDATE' if maxres<2e-6 and maxbasis==0 and maxshape==0 else ('PROVEN_ROOT_DOMAIN_TRANSPORT_FAULT_ONE_CANDIDATE' if proven_root_fault else 'UNRESOLVED_LOCAL_NONRIGID_DRIVER_OR_BOUNDARY_NOT_WAIVED'),'TierP':0}
(O/'HEAD_BOUNDARY_DISCRIMINATOR_PRIVATE_R1.json').write_text(json.dumps(result,indent=2),encoding='utf8')
# Actual affected-segment matched source cadence proof; no whole97 render or Idle rerender.
cam=s.camera;savecam=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width);saves=[]
for ob,k,v in [(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',8),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',384),(s.render,'resolution_y',384),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','PNG'),(s.render.image_settings,'color_mode','RGBA'),(s.render.image_settings,'color_depth','8'),(s.render,'filepath','')]:saves.append((ob,k,getattr(ob,k)));setattr(ob,k,v)
vv=neutral['Character_Body_Head'][0];center=Vector(((vv[:,0].min()+vv[:,0].max())/2,(vv[:,1].min()+vv[:,1].max())/2,(vv[:,2].min()+vv[:,2].max())/2));size=float(vv[:,2].max()-vv[:,2].min()+.08);views={}
roles=['existing_full_transport','one_minimal_object_transport'] if fix else ['original_body_only_control','existing_full_transport']
for role in roles:
 if role=='existing_full_transport':ln=NativeWalkLane();ln.on()
 elif role=='one_minimal_object_transport':ln=ObjectFixLane();ln.on()
 else:ln=ReactionLane();ln.on('MESHY_R2_BODY_WalkInPlace')
 for view,direction in [('face_front',(0,-1,0)),('neck_positiveX_side',(1,0,0))]:
  p=O/role/view;p.mkdir(parents=True);cam.data.type='ORTHO';cam.data.ortho_scale=size;cam.location=center+Vector(direction)*.7;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();views[view]={'center':list(center),'location':list(cam.location),'rotation_euler':list(cam.rotation_euler),'ortho_scale':size,'resolution':[384,384],'fixed':True,'source_fps':24,'segment_frames':[74,97]}
  for f in range(74,98):s.frame_set(f);bpy.context.view_layer.update();s.render.filepath=str(p/f'{f:04}.png');bpy.ops.render.render(write_still=True)
 ln.off()
cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width=savecam;s.render.resolution_x=960;s.render.resolution_y=920;s.render.filepath=str(O/'HEAD_BOUNDARY_OFF_SOURCE_NEUTRAL_R1.png');bpy.ops.render.render(write_still=True)
for ob,k,v in saves:setattr(ob,k,v)
assert snapshot(names)==before and snapshot(source_names)==source_sig and sha(P)==meta['source_SHA'] and sha(C)==meta['candidate_SHA'] and sha(meta['library']['file'])==meta['library']['sha256'];result['views']=views;result['matched24frame74_97_original24fps_complete']=True;result['temporary_render_settings_restored_FULL_RAW_OFF_equal']=True;(O/'HEAD_BOUNDARY_DISCRIMINATOR_PRIVATE_R1.json').write_text(json.dumps(result,indent=2),encoding='utf8');print('HEAD_BOUNDARY_DISCRIMINATOR_COMPLETE',result['classification'],maxres,maxbasis,maxshape,flush=True)
