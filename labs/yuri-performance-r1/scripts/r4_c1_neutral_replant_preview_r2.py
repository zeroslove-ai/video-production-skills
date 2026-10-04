"""Two complete fixed-camera native views of the one replant experiment, no source save."""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_c1_contact_path_adapter_r1 import ReachFingerLane
from r4_appearance_signature import snapshot
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-c1-neutral-replant-preview-r2';O.mkdir(exist_ok=False);d=json.loads((B/'alpha-c1-neutral-supported-replant-r2/SUPPORTED_REPLANT_PRIVATE_R2.json').read_bytes());P=Path(d['candidate']);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(P)==d['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);s=bpy.context.scene;cam=s.camera;cloc=cam.location.copy();crot=cam.rotation_euler.copy();cscale=cam.data.ortho_scale;names=list(bpy.data.actions.keys());before=snapshot(names);lane=ReachFingerLane();lane.on()
for obj,name in d['additive_actions'].items():
 ad=bpy.data.objects[obj].animation_data;ad.action=bpy.data.actions[name];ad.action_slot=ad.action.slots[0]
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=2;s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=384;s.render.resolution_y=384;s.render.resolution_percentage=100;s.render.image_settings.file_format='JPEG';s.render.image_settings.color_mode='RGB';s.render.image_settings.color_depth='8';s.render.image_settings.quality=92;meta={}
for view,target,direction,scale in [('fullbody_front',(.002,-.028,.53),(0,-1,0),1.18),('feet_side',(.002,-.035,.13),(1,0,0),.58)]:
 p=O/view;p.mkdir();tar=Vector(target);cam.data.type='ORTHO';cam.data.ortho_scale=scale;cam.location=tar+Vector(direction)*.8;cam.rotation_euler=(tar-cam.location).to_track_quat('-Z','Y').to_euler();meta[view]={'target':list(tar),'location':list(cam.location),'rotation_euler':list(cam.rotation_euler),'ortho_scale':scale,'resolution':[384,384],'frames':[61,133],'fps':30,'fixed':True}
 for f in range(61,134):
  s.frame_set(f);bpy.context.view_layer.update();s.render.filepath=str(p/f'{f-60:04}.jpg');bpy.ops.render.render(write_still=True)
 print('NEUTRAL_REPLANT_COMPLETE_VIEW',view,73,flush=True)
lane.off();lib=O/'YURI_R4_C1_NEUTRAL_CONTACT_PATCH_ACTIONS_ONLY_R2.blend';selected=[*d['additive_actions'].values(),'YURI_R4_C1_LEFT_PREGRASP_FINGERS_TIMING_R2'];assert len(set(selected))==5;bpy.data.libraries.write(str(lib),{bpy.data.actions[n] for n in selected},fake_user=True)
with bpy.data.libraries.load(str(lib),link=False) as (src,dst):
 assert sorted(src.actions)==sorted(selected) and not src.objects and not src.meshes and not src.armatures
(O/'ACTION_ONLY_CUSTODY_R2.json').write_text(json.dumps({'file':str(lib),'SHA':sha(lib),'bytes':lib.stat().st_size,'named_actions':selected,'objects':0,'meshes':0,'armatures':0,'canonical_character':False,'motion_verdict':d['verdict'],'receiver_recipe':'Immutable original source plus these5Actions, same body/head/hair/root clock1..133, unchanged LEFT finger NLA1..61 REPLACE/HOLD scale1. Source-only experiment; exact contact/neutral acceptance according to report, no product promotion.'},indent=2),encoding='utf-8')
cam.location=cloc;cam.rotation_euler=crot;cam.data.ortho_scale=cscale
# OFF authoritative source-camera render, independent of whether ON transition succeeded.
s.cycles.samples=8;s.render.resolution_x=960;s.render.resolution_y=920;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(O/'CANDIDATE_OFF_SOURCE_NEUTRAL_R2.png');bpy.ops.render.render(write_still=True);assert sha(P)==d['candidate_SHA'];(O/'PREVIEW_RECEIPT_R2.json').write_text(json.dumps({'candidate_SHA':d['candidate_SHA'],'complete_frames_rendered':73,'views':meta,'source_materials_meshes_drivers_unchanged':True,'no_candidate_or_source_save':True,'transition_verdict_from_actual_constraints':d['verdict'],'normal_speed_PLAYBACK':'PENDING encoding and actual through-end playback; these are rendered native frames only','original_C1_frames1_61_exact':d['original_C1_frames1_61_exact']},indent=2),encoding='utf-8')
