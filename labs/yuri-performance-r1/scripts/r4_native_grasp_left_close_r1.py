"""One active LEFT-hand camera supplement; immutable169-frame native candidate."""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_native_grasp_adapter_r1 import NativeGraspLane
from r4_appearance_signature import snapshot
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-native-grasp-left-close-r1';O.mkdir(exist_ok=False)
d=json.loads((B/'alpha-native-grasp-candidate-r1b/NATIVE_GRASP_CANDIDATE_PRIVATE_R1B.json').read_bytes());P=Path(d['candidate']);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(P)==d['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False)
s=bpy.context.scene;cam=s.camera;loc=cam.location.copy();rot=cam.rotation_euler.copy();size=cam.data.ortho_scale;ctype=cam.data.type;names=list(bpy.data.actions.keys());before=snapshot(names)
lane=NativeGraspLane();lane.on();s.frame_set(1);bpy.context.view_layer.update();rig=bpy.data.objects['Meshy_Fitted_Rig'];hand=rig.pose.bones['hand.L'];offset=(rig.matrix_world.to_3x3()@hand.matrix.to_3x3().col[1]).normalized()*.028;direction=Vector((0,-1,0));cam.data.type='ORTHO';cam.data.ortho_scale=.18;cam.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler()
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=8;s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=512;s.render.resolution_y=512;s.render.resolution_percentage=100;s.render.image_settings.file_format='JPEG';s.render.image_settings.color_mode='RGB';s.render.image_settings.color_depth='8';s.render.image_settings.quality=95
frames=O/'left_hand_close';frames.mkdir();cameras=[]
for f in range(1,170):
    s.frame_set(f);bpy.context.view_layer.update();wrist=rig.matrix_world@hand.head;target=wrist+offset;cam.location=target+direction*.8
    cameras.append({'frame':f,'wrist':list(wrist),'target':list(target),'camera_location':list(cam.location),'camera_rotation_euler':list(cam.rotation_euler)})
    s.render.filepath=str(frames/f'{f:04}.jpg');bpy.ops.render.render(write_still=True)
lane.off();cam.location=loc;cam.rotation_euler=rot;cam.data.ortho_scale=size;cam.data.type=ctype
assert snapshot(names)==before and sha(P)==d['candidate_SHA'] and sha(d['source'])==d['source_SHA']
(O/'LEFT_ACTIVE_HAND_CAMERA_RECEIPT_R1.json').write_text(json.dumps({'task':'ROOT_PM_NATIVE_GRASP_MOVING_HAND_VIEW_SCOPE_R1','candidate_SHA':d['candidate_SHA'],'source_SHA':d['source_SHA'],'existing_library_SHA':'a2808d19d71cf55165b35b3bebcf752eebad8d76f5f4d6018c8b9a7435a8aeb2','motion_changed':False,'source_files_saved':False,'original_OFF_snapshot_restored':True,'source_fps':24,'frames':[1,169],'native_all169_rendered':True,'view':'LEFT active hand; wrist-world-translation follow with constant world target offset and fixed camera rotation; no rotation follow','ortho_scale_m':.18,'resolution':[512,512],'CPU_samples':8,'materials_lights_original_preserved':True,'whole_body_foot_root_verdict_uses':'Existing fixed front/waist and prior all169 mesh/world measurements only','camera_frames':cameras,'normal_speed':'Pending encoded actual1x playback','visual':'PENDING; no physical grasp/prop/Unity/TierP claim','TierP':0},indent=2),encoding='utf-8')
print('LEFT_ACTIVE_HAND_ALL169_DONE_NO_MOTION_CHANGE',flush=True)
