"""One immutable R4 existing BODY_HeadGazeHair visual authority capture; no authoring."""
import bpy,sys,json,hashlib,time
from pathlib import Path
import numpy as np
from mathutils import Vector
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-native-head-visual-source-r1';O.mkdir(exist_ok=False)
P=H.parent/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend';SHA='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(P)==SHA
start=time.perf_counter();bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);s=bpy.context.scene;names=list(bpy.data.actions.keys());before=snapshot(names);assert len(names)==78
name='MESHY_R2_BODY_HeadGazeHair';a=bpy.data.actions[name];assert len(a.slots)==1 and a.slots[0].target_id_type=='OBJECT'
curves=[f for l in a.layers for st in l.strips for bag in st.channelbags if bag.slot_handle==a.slots[0].handle for f in bag.fcurves];assert curves
compatible=[]
for ob in bpy.data.objects:
 try:
  for f in curves:
   v=ob.path_resolve(f.data_path)
   if hasattr(v,'__len__'):assert f.array_index<len(v)
  compatible.append(ob.name)
 except (ValueError,AttributeError,AssertionError):pass
assert compatible==['Meshy_Fitted_Rig'],compatible
rig=bpy.data.objects[compatible[0]];key=bpy.data.objects['Character_Body_Head'].data.shape_keys
frames=sorted({float(k.co.x) for f in curves for k in f.keyframe_points});lo=int(min(frames));hi=int(max(frames));fps=s.render.fps/s.render.fps_base;assert [lo,hi]==[1,97] and fps==24
def worldverts(ob):
 eo=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=eo.to_mesh();v=np.empty(len(me.vertices)*3);me.vertices.foreach_get('co',v);v=v.reshape(-1,3);w=np.array(eo.matrix_world);eo.to_mesh_clear();return v@w[:3,:3].T+w[:3,3]
mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4'];neutral={n:worldverts(bpy.data.objects[n]) for n in mesh_names}
def values():return {k.name:float(k.value) for k in key.key_blocks}
offvals=values();eye_names=[b.name for b in bpy.data.objects['Armature'].pose.bones if 'eye' in b.name.lower()];head=bpy.data.objects['Armature'];hair=bpy.data.objects['Hair_Rig_R4']
lane=ReactionLane(compatible[0]);lane.on(name);assert rig.animation_data.action==a and rig.animation_data.action_slot==a.slots[0]
rows=[];motion={n:0. for n in mesh_names};pose_first=None
for f in range(lo,hi+1):
 s.frame_set(f);bpy.context.view_layer.update();vv={n:worldverts(bpy.data.objects[n]) for n in mesh_names}
 for n in mesh_names:assert np.isfinite(vv[n]).all();motion[n]=max(motion[n],float(np.linalg.norm(vv[n]-neutral[n],axis=1).max()))
 poses={ob.name:{bn:np.array(ob.matrix_world@ob.pose.bones[bn].matrix).tolist() for bn in (['head','neck'] if ob==rig else eye_names+['Root','J_Bip_C_Head','J_Bip_C_Neck'] if ob==head else ['Hair_HeadRoot']) if bn in ob.pose.bones} for ob in [rig,head,hair]}
 rows.append({'frame':f,'native_time_seconds':(f-lo)/fps,'morph_values':values(),'actual_pose_world_private':poses,'mesh_world_coordinate_sha256':{n:hashlib.sha256(vv[n].tobytes()).hexdigest() for n in mesh_names},'max_mesh_displacement_vs_source_OFF_m':{n:float(np.linalg.norm(vv[n]-neutral[n],axis=1).max()) for n in mesh_names}})
lane.off();assert snapshot(names)==before
meta={'task':'ROOT_PM_HEAD_BOUNDARY_CLOSE_TO_NATIVE_HEAD_VISUAL_R1','source':str(P),'source_SHA':SHA,'existing_action':name,'action_signature_SHA':before['actions'][name],'slot':{'identifier':a.slots[0].identifier,'handle':a.slots[0].handle,'type':a.slots[0].target_id_type},'all_original_curve_RNA_compatible_targets':compatible,'target_binding':'Unique complete original BODY curve RNA resolution plus exact Meshy_Fitted_Rig owner; no first-slot fallback','curve_count':len(curves),'curve_paths':sorted({f.data_path for f in curves}),'range':[lo,hi],'source_fps':fps,'source_fps_base':s.render.fps_base,'endpoint_span_seconds':(hi-lo)/fps,'encoded_duration_seconds':(hi-lo+1)/fps,'speed_factor':1,'source78_preserved':True,'no_additive_transport_no_FACE_GAZE_HAIR_action_assignment':True,'scope':'Existing native BODY_HeadGazeHair only plus all existing original face/gaze/hair drivers/constraints. Auxiliary native FACE KEY/GAZE/HAIR takes not bound: do not claim whole multi-channel facial performance. Measured actual morph/eye outputs retained. No driver unmute/rebuild/export/new candidate/contact counts.','neutral_morph_values':offvals,'eye_bones':eye_names,'max_actual_mesh_displacement_vs_OFF_m':motion,'rows_private':rows,'original_source_signature':before,'TierP':0}
(O/'NATIVE_HEAD_VISUAL_SOURCE_PRIVATE_R1.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
cam=s.camera;savecam=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width);saves=[]
for ob,k,v in [(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',8),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',384),(s.render,'resolution_y',384),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','PNG'),(s.render.image_settings,'color_mode','RGBA'),(s.render.image_settings,'color_depth','8'),(s.render,'filepath','')]:saves.append((ob,k,getattr(ob,k)));setattr(ob,k,v)
lane=ReactionLane(compatible[0]);lane.on(name);views={};target=Vector((.001950026,-.032999933,.86756835));size=.28
for view,direction in [('front',(0,-1,0)),('positiveX_side',(1,0,0))]:
 folder=O/view;folder.mkdir();cam.data.type='ORTHO';cam.data.ortho_scale=size;cam.location=target+Vector(direction)*.7;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();views[view]={'type':'ORTHO','target':list(target),'location':list(cam.location),'rotation_euler':list(cam.rotation_euler),'ortho_scale':size,'lens_mm':cam.data.lens,'sensor_width_mm':cam.data.sensor_width,'resolution':[384,384],'fixed':True,'source_fps':fps,'frames':[lo,hi]}
 for f in range(lo,hi+1):
  s.frame_set(f);bpy.context.view_layer.update();s.render.filepath=str(folder/f'{f:04}.png');bpy.ops.render.render(write_still=True)
 print('HEAD_VISUAL_VIEW_COMPLETE',view,flush=True)
lane.off();cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width=savecam;s.render.resolution_x=960;s.render.resolution_y=920;s.render.filepath=str(O/'NATIVE_HEAD_VISUAL_OFF_SOURCE_NEUTRAL_R1.png');bpy.ops.render.render(write_still=True)
for ob,k,v in saves:setattr(ob,k,v)
assert snapshot(names)==before and sha(P)==SHA;meta['views']=views;meta['all97_both_views_complete']=True;meta['full_raw_OFF_snapshot_equal']=True;meta['source_bytes_unchanged']=True;meta['collector_elapsed_seconds']=time.perf_counter()-start
(O/'NATIVE_HEAD_VISUAL_SOURCE_PRIVATE_R1.json').write_text(json.dumps(meta,indent=2),encoding='utf8');print('NATIVE_HEAD_VISUAL_SOURCE_COMPLETE',flush=True)
