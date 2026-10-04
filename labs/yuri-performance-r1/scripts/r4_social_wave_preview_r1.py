"""Fixed source-only walk candidate 1x full preview, original materials, CPU only."""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_adapter import ReactionLane
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
def main(view,probe=False):
 assert view in ['front','quarter','side'];out=(BASE/'alpha-social-wave-probe-r1'/view) if probe else BASE/'alpha-social-wave-preview-r1'/view;out.mkdir(parents=True,exist_ok=False);d=json.loads((BASE/'alpha-social-wave-candidate-r1/SOCIAL_WAVE_CANDIDATE_PRIVATE_R1.json').read_bytes());source=Path(d['candidate']);assert hashlib.sha256(source.read_bytes()).hexdigest()==d['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=str(source),use_scripts=False);s=bpy.context.scene;assert s.render.fps/s.render.fps_base==24
 s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=2;s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=512;s.render.resolution_y=384;s.render.resolution_percentage=100;s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=92;s.render.image_settings.color_depth='8';s.render.image_settings.color_mode='RGB'
 root=d['frames_private'];middle=Vector((.002,-.028,.79))+Vector(tuple((min(r['root_carrier_world'][i] for r in root)+max(r['root_carrier_world'][i] for r in root))/2 for i in range(3)));cam=s.camera;cam.data.type='PERSP';cam.data.lens=50;cam.data.sensor_width=36;cam.location={'front':(middle.x,middle.y-2.0,.83),'quarter':(middle.x+1.5,middle.y-1.6,.83),'side':(middle.x+2.0,middle.y,.83)}[view];cam.rotation_euler=(middle-cam.location).to_track_quat('-Z','Y').to_euler()
 lanes=[]
 for obj in d['additive_body_actions']:
  lane=ReactionLane(obj);a=lane.on(d['additive_body_actions'][obj]);assert a['source_fps']==30;lanes.append(lane)
 
 selected=[1,31,45,91] if probe else list(range(1,92))
 for f in selected:
  s.frame_set(f);bpy.context.view_layer.update();s.render.filepath=str(out/f'{f:04d}.jpg');bpy.ops.render.render(write_still=True)
  if f%100==0:print('WALK_TURN_NORMAL1X_PREVIEW',view,f,293,flush=True)
 camera={'object':cam.name,'type':cam.data.type,'lens_mm':cam.data.lens,'sensor_width_mm':cam.data.sensor_width,'location':list(cam.location),'rotation_euler':list(cam.rotation_euler),'target':list(middle),'policy':'Fixed camera per view, no root-follow or screen-motion extraction; actual world path visible in quarter/side.'}
 with (out/'RENDER_RECEIPT_R4.json').open('x',encoding='utf8') as f:json.dump({'candidate_SHA':d['candidate_SHA'],'view':view,'camera':camera,'frames':[1,91],'fps':30,'frame_count':len(selected),'source_frame_ids':selected,'probe_only':probe,'key_interval_sec':90/30,'movie_duration_sec':91/30,'source_scene_fps_preserved':24,'per_Action_fps_readback':30,'resolution':[512,384],'CPU_threads':2,'samples':2,'still_format':'JPEG','JPEG_quality':92,'no_material_visibility_mesh_source_save_Unity_change':True,'limits':'Low-sample source preview; no final F2/F3/StageB/O1/PRIMARY claim; Authored right-hand greeting only; authored hold and prop-grip/contact missing, no hold or physics claim'},f,indent=2)
