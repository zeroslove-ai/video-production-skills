"""Causal restoration control, reuses finished render bytes; no new render/motion."""
import bpy,sys,json,hashlib
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_native_grasp_adapter_r1 import NativeGraspLane
from r4_appearance_signature import snapshot,difference
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-native-grasp-left-close-restore-r1b';O.mkdir(exist_ok=False);P=B/'alpha-native-grasp-left-close-r1'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();d=json.loads((B/'alpha-native-grasp-candidate-r1b/NATIVE_GRASP_CANDIDATE_PRIVATE_R1B.json').read_bytes());idx=json.loads((P/'COMPLETED_RENDER_SHA_INDEX_R1.json').read_bytes());assert len(idx)==169
for n,x in idx.items():p=P/'left_hand_close'/n;assert sha(p)==x['SHA'] and p.stat().st_size==x['bytes']
bpy.ops.wm.open_mainfile(filepath=d['candidate'],use_scripts=False);s=bpy.context.scene;cam=s.camera;loc=cam.location.copy();rot=cam.rotation_euler.copy();size=cam.data.ortho_scale;ctype=cam.data.type;names=list(bpy.data.actions.keys());before=snapshot(names)
changes=[(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',8),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',512),(s.render,'resolution_y',512),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','JPEG'),(s.render.image_settings,'color_mode','RGB'),(s.render.image_settings,'color_depth','8'),(s.render.image_settings,'quality',95),(s.render,'filepath',str(P/'left_hand_close/0169.jpg'))]
original=[(obj,key,getattr(obj,key)) for obj,key,_ in changes]
for obj,key,v in changes:setattr(obj,key,v)
lane=NativeGraspLane();lane.on();s.frame_set(1);bpy.context.view_layer.update();rig=bpy.data.objects['Meshy_Fitted_Rig'];hand=rig.pose.bones['hand.L'];offset=(rig.matrix_world.to_3x3()@hand.matrix.to_3x3().col[1]).normalized()*.028;direction=Vector((0,-1,0));cam.data.type='ORTHO';cam.data.ortho_scale=.18;cam.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler();cameras=[]
for f in range(1,170):
    s.frame_set(f);bpy.context.view_layer.update();wrist=rig.matrix_world@hand.head;target=wrist+offset;cam.location=target+direction*.8;cameras.append({'frame':f,'wrist':list(wrist),'target':list(target),'camera_location':list(cam.location),'camera_rotation_euler':list(cam.rotation_euler)})
lane.off();cam.location=loc;cam.rotation_euler=rot;cam.data.ortho_scale=size;cam.data.type=ctype
render_override_diff=difference(before,snapshot(names));assert set(render_override_diff)=={'scene'},render_override_diff
for obj,key,v in original:setattr(obj,key,v)
after=snapshot(names);diff=difference(before,after)
(O/'RESTORATION_DIFFERENCE_R1B.json').write_text(json.dumps({'before_render_settings_restoration':render_override_diff,'after_all_settings_restored':diff,'all169_existing_render_bytes_unchanged':True,'native_rerendered':False,'source_candidate_byte_hash_unchanged':sha(d['candidate'])==d['candidate_SHA'] and sha(d['source'])==d['source_SHA']},indent=2),encoding='utf-8');assert not diff
(O/'LEFT_ACTIVE_HAND_CAMERA_RECEIPT_R1B.json').write_text(json.dumps({'task':'ROOT_PM_NATIVE_GRASP_MOVING_HAND_VIEW_SCOPE_R1','candidate_SHA':d['candidate_SHA'],'source_SHA':d['source_SHA'],'existing_library_SHA':'a2808d19d71cf55165b35b3bebcf752eebad8d76f5f4d6018c8b9a7435a8aeb2','motion_changed':False,'source_files_saved':False,'original_OFF_snapshot_restored':True,'source_fps':24,'frames':[1,169],'native_all169_rendered':True,'render_origin':'Original R1 rendered all169 but final assertion failed due only transient scene render settings. Preserved failure. R1b replayed identical candidate/pose/camera and confirmed model categories unchanged, scene-only difference; restored all settings gives full signature0. No rerender. Render bytes pinned unchanged.','view':'LEFT active hand; wrist-world-translation follow with constant world target offset and fixed camera rotation; no rotation follow','ortho_scale_m':.18,'resolution':[512,512],'CPU_samples':8,'materials_lights_original_preserved':True,'whole_body_foot_root_verdict_uses':'Existing fixed front/waist and prior all169 mesh/world measurements only','camera_frames':cameras,'normal_speed':'Pending encoded actual1x playback','visual':'PENDING; no physical grasp/prop/Unity/TierP claim','TierP':0},indent=2),encoding='utf-8')
print('SCENE_ONLY_CAUSE_AND_FULL_RESTORATION_PASS_REUSED169_RENDER_BYTES',flush=True)
