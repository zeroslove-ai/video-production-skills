"""C1 body exact, fixed right-hand three views plus fullbody all-frame source proof."""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_reach_finger_adapter_r1 import ReachFingerLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
def main(probe=False):
 d=json.loads((B/'alpha-reach-finger-candidate-r2/REACH_FINGER_CANDIDATE_PRIVATE_R2.json').read_bytes());P=Path(d['candidate']);assert hashlib.sha256(P.read_bytes()).hexdigest()==d['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];lane=ReachFingerLane();lane.on();world=lambda v:r.matrix_world@v
 centre=(world(r.pose.bones['hand.R'].head)+world(r.pose.bones['middle3.R'].tail))*.5;width=(world(r.pose.bones['pinky1.R'].head)-world(r.pose.bones['index1.R'].head)).normalized();long=(world(r.pose.bones['middle3.R'].tail)-world(r.pose.bones['middle1.R'].head)).normalized();outward=-long.cross(width).normalized();root=B/('alpha-reach-finger-probe-r2' if probe else 'alpha-reach-finger-preview-r2');root.mkdir(exist_ok=False)
 s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=4 if probe else 2;s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=512;s.render.resolution_y=512;s.render.resolution_percentage=100;s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=92;s.render.image_settings.color_mode='RGB';s.render.image_settings.color_depth='8';cameras={}
 for view in ['hand_close','front','side','fullbody']:
  o=root/view;o.mkdir();cam=s.camera;cam.data.type='ORTHO';cam.data.lens=50;cam.data.sensor_width=36;target=Vector((.002,-.028,.53)) if view=='fullbody' else centre;direction={'hand_close':(outward-width*.55).normalized(),'front':Vector((0,-1,0)),'side':outward,'fullbody':Vector((0,-1,0))}[view];cam.location=target+direction*.8;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.18 if view=='fullbody' else .14;frames=[1,14,27,35,46,61] if probe else range(1,62)
  for f in frames:s.frame_set(f);bpy.context.view_layer.update();s.render.filepath=str(o/f'{f:04}.jpg');bpy.ops.render.render(write_still=True)
  cameras[view]={'object':cam.name,'location':list(cam.location),'rotation_euler':list(cam.rotation_euler),'target':list(target),'type':'ORTHO','ortho_scale':cam.data.ortho_scale,'resolution':[512,512],'source_frames':list(frames),'body_fps':30,'finger_source_frame_range':[1,105],'finger_NLA_scale':60/104,'samples':4 if probe else 2,'fixed_camera':True}
  print('REACH_FINGER_PREVIEW',view,len(frames),flush=True)
 (root/'RENDER_RECEIPT_R1.json').write_text(json.dumps({'candidate_SHA':d['candidate_SHA'],'cameras':cameras,'probe':probe,'no_mesh_material_visibility_or_source_save_changes':True,'semantic':'LEFT reach + RIGHT finger curl; laterality/neutral/contact HOLD'},indent=2),encoding='utf8');lane.off()
