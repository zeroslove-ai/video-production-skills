"""C1 body exact, fixed right-hand three views plus fullbody all-frame source proof."""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_c1_contact_path_adapter_r1 import ReachFingerLane
from r4_reach_left_finger_timing_adapter_r2 import ReachFingerLane as BaseLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
def main(probe=False):
 d=json.loads((B/'alpha-c1-contact-path-candidate-r1b/C1_CONTACT_PATH_CANDIDATE_PRIVATE_R1.json').read_bytes());P=Path(d['candidate']);assert hashlib.sha256(P.read_bytes()).hexdigest()==d['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];lane=ReachFingerLane();lane.on();world=lambda v:r.matrix_world@v
 points=[Vector(v) for row in d['frames_private'] for v in [row['left_hand_world']['wrist'],*row['left_hand_world']['tips'].values()]];centre=Vector(tuple((min(p[i] for p in points)+max(p[i] for p in points))*.5 for i in range(3)));width=(world(r.pose.bones['pinky1.L'].head)-world(r.pose.bones['index1.L'].head)).normalized();long=(world(r.pose.bones['middle3.L'].tail)-world(r.pose.bones['middle1.L'].head)).normalized();outward=long.cross(width).normalized();root=B/('alpha-c1-contact-path-probe-r1' if probe else 'alpha-c1-contact-path-preview-r1');root.mkdir(exist_ok=False)
 s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=4 if probe else 2;s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=512;s.render.resolution_y=512;s.render.resolution_percentage=100;s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=92;s.render.image_settings.color_mode='RGB';s.render.image_settings.color_depth='8';cameras={}
 for view in ['hand_close','front','side','fullbody']:
  o=root/view;o.mkdir();cam=s.camera;cam.data.type='ORTHO';cam.data.lens=50;cam.data.sensor_width=36;target=Vector((.002,-.028,.53)) if view=='fullbody' else centre;direction={'hand_close':(outward-width*.55).normalized(),'front':Vector((0,-1,0)),'side':outward,'fullbody':Vector((0,-1,0))}[view];cam.location=target+direction*.8;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.18 if view=='fullbody' else (.16 if view=='hand_close' else .5);frames=[1,14,27,35,46,61] if probe else range(1,62)
  frame_cameras=[]
  for f in frames:
   s.frame_set(f);bpy.context.view_layer.update()
   if view=='hand_close':
    hand=r.pose.bones['hand.L'];target=world(hand.head)+(r.matrix_world.to_3x3()@hand.matrix.to_3x3().col[1]).normalized()*.029;cam.location=target+direction*.8;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
   frame_cameras.append({'frame':f,'location':list(cam.location),'rotation_euler':list(cam.rotation_euler),'target':list(target)})
   s.render.filepath=str(o/f'{f:04}.jpg');bpy.ops.render.render(write_still=True)
  cameras[view]={'object':cam.name,'location':list(cam.location),'rotation_euler':list(cam.rotation_euler),'target':list(target),'type':'ORTHO','ortho_scale':cam.data.ortho_scale,'resolution':[512,512],'source_frames':list(frames),'body_fps':30,'finger_source_frame_range':[1,61],'finger_NLA_scale':1,'samples':4 if probe else 2,'fixed_camera':view!='hand_close','frame_cameras':frame_cameras,'hand_close_policy':'Hand close camera follows existing C1 wrist/bone direction only; static orientation offset. Front/side/fullbody fixed, world motion not judged from close camera.'}
  if not probe:
   lane.off();baseline_lane=BaseLane();baseline_lane.on();bp=root/'baseline_same_camera'/view;bp.mkdir(parents=True)
   for f in [1,7,18,31,50,61]:
    s.frame_set(f);bpy.context.view_layer.update();meta=next(x for x in frame_cameras if x['frame']==f);cam.location=meta['location'];cam.rotation_euler=meta['rotation_euler'];s.render.filepath=str(bp/f'{f:04}.jpg');bpy.ops.render.render(write_still=True)
   baseline_lane.off();lane=ReachFingerLane();lane.on()
  print('REACH_FINGER_PREVIEW',view,len(frames),flush=True)
 (root/'RENDER_RECEIPT_R1.json').write_text(json.dumps({'candidate_SHA':d['candidate_SHA'],'cameras':cameras,'probe':probe,'no_mesh_material_visibility_or_source_save_changes':True,'semantic':'C1 upper_arm.L8deg endpoint clearance derivative plus unchanged R2 LEFT finger timing; original neutral remains HOLD'},indent=2),encoding='utf8');lane.off()
