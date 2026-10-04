"""Same native LEFT hand camera and fixed waist before/after, plus OFF pixel oracle."""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_grasp_left_thumb_adapter_c1 import ThumbLane,ACTIONS
from r4_appearance_signature import snapshot
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-grasp-left-thumb-preview-c1';O.mkdir(exist_ok=False);d=json.loads((B/'alpha-grasp-left-thumb-c1/LEFT_THUMB_C1_PRIVATE_MANIFEST.json').read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(d['candidate'])==d['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=d['candidate'],use_scripts=False);s=bpy.context.scene;cam=s.camera;loc=cam.location.copy();rot=cam.rotation_euler.copy();size=cam.data.ortho_scale;ctype=cam.data.type;names=list(bpy.data.actions.keys());before=snapshot(names)
lib=O/'YURI_R4_GRASP_LEFT_THUMB_C1_ACTIONS_ONLY.blend';bpy.data.libraries.write(str(lib),{bpy.data.actions[n] for n in ACTIONS.values()},fake_user=True)
with bpy.data.libraries.load(str(lib),link=False) as (src,dst):assert len(src.actions)==3 and not src.objects and not src.meshes and not src.armatures
changes=[(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',8),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',512),(s.render,'resolution_y',512),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','JPEG'),(s.render.image_settings,'color_mode','RGB'),(s.render.image_settings,'color_depth','8'),(s.render.image_settings,'quality',95),(s.render,'filepath','')];original=[(obj,key,getattr(obj,key)) for obj,key,_ in changes]
for obj,key,v in changes:setattr(obj,key,v)
lane=ThumbLane();lane.on();s.frame_set(1);bpy.context.view_layer.update();rig=bpy.data.objects['Meshy_Fitted_Rig'];hand=rig.pose.bones['hand.L'];offset=(rig.matrix_world.to_3x3()@hand.matrix.to_3x3().col[1]).normalized()*.028;meta={}
for view in ['left_hand_close','waist_3q']:
 p=O/view;p.mkdir();direction=Vector((0,-1,0)) if view=='left_hand_close' else Vector((.6,-1,0)).normalized();target=Vector((.002,-.028,.79));cam.data.type='ORTHO';cam.data.ortho_scale=.18 if view=='left_hand_close' else .62;cam.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler();s.render.resolution_x=s.render.resolution_y=512 if view=='left_hand_close' else 384;s.cycles.samples=8 if view=='left_hand_close' else 2;s.render.image_settings.quality=95 if view=='left_hand_close' else 92
 meta[view]={'frames':[1,169],'fps':24,'camera_rotation_euler':list(cam.rotation_euler),'target':list(target),'fixed':view=='waist_3q','wrist_world_translation_follow':view=='left_hand_close','constant_target_offset':list(offset) if view=='left_hand_close' else None,'ortho_scale':cam.data.ortho_scale,'resolution':[s.render.resolution_x,s.render.resolution_y]}
 for f in range(1,170):
  s.frame_set(f);bpy.context.view_layer.update();tar=rig.matrix_world@hand.head+offset if view=='left_hand_close' else target;cam.location=tar+direction*.8;s.render.filepath=str(p/f'{f:04}.jpg');bpy.ops.render.render(write_still=True)
lane.off();cam.location=loc;cam.rotation_euler=rot;cam.data.ortho_scale=size;cam.data.type=ctype;s.cycles.samples=8;s.render.resolution_x=960;s.render.resolution_y=920;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(O/'CANDIDATE_OFF_SOURCE_NEUTRAL_C1.png');bpy.ops.render.render(write_still=True)
for obj,key,v in original:setattr(obj,key,v)
assert snapshot(names)==before and sha(d['candidate'])==d['candidate_SHA']
(O/'THUMB_C1_RENDER_RECEIPT.json').write_text(json.dumps({'candidate_SHA':d['candidate_SHA'],'OFF_full_snapshot_restored':True,'source_fps':24,'views':meta,'normal_speed':'PENDING','library':{'file':str(lib),'SHA':sha(lib),'bytes':lib.stat().st_size,'actions':ACTIONS,'objects':0,'meshes':0,'armatures':0},'TierP':0},indent=2),encoding='utf-8');print('THUMB_C1_RENDER_DONE_OFF_FULL_SIGNATURE0',flush=True)
