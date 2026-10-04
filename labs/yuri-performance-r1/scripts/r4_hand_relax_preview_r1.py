"""CPU source hand three fixed views and fullbody witness; no saved camera edits."""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_adapter import ReactionLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
def main(probe=False):
 D=json.loads((B/'alpha-hand-relax-candidate-r1/HAND_RELAX_CANDIDATE_PRIVATE_R1.json').read_bytes());P=Path(D['candidate']);assert hashlib.sha256(P.read_bytes()).hexdigest()==D['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];world=lambda v:r.matrix_world@v
 centre=(world(r.pose.bones['hand.R'].head)+world(r.pose.bones['middle3.R'].tail))*.5;normal=Vector(D['palm_inward_rig_axis']);outward=-(r.matrix_world.to_3x3()@normal).normalized();width=(world(r.pose.bones['pinky1.R'].head)-world(r.pose.bones['index1.R'].head)).normalized()
 s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=4 if probe else 2;s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=512;s.render.resolution_y=512;s.render.resolution_percentage=100;s.render.image_settings.file_format='JPEG';s.render.image_settings.quality=92;s.render.image_settings.color_mode='RGB';s.render.image_settings.color_depth='8';lane=ReactionLane();a=lane.on(D['additive_body_actions']['Meshy_Fitted_Rig']);assert a['source_fps']==30
 root=B/('alpha-hand-relax-probe-r1' if probe else 'alpha-hand-relax-preview-r1');root.mkdir(exist_ok=False);cameras={}
 for view in ['hand_close','front','side','fullbody']:
  o=root/view;o.mkdir();cam=s.camera;cam.data.type='ORTHO';cam.data.lens=50;cam.data.sensor_width=36
  target=Vector((.002,-.028,.53)) if view=='fullbody' else centre;direction={'hand_close':(outward-width*.55).normalized(),'front':Vector((0,-1,0)),'side':outward,'fullbody':Vector((0,-1,0))}[view];cam.location=target+direction*.8;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.18 if view=='fullbody' else .12
  selected=[1,32,53,69,87,105] if probe else ([1,53,105] if view=='fullbody' else range(1,106))
  for f in selected:
   s.frame_set(f);bpy.context.view_layer.update();s.render.filepath=str(o/f'{f:04}.jpg');bpy.ops.render.render(write_still=True)
  cameras[view]={'object':cam.name,'location':list(cam.location),'rotation_euler':list(cam.rotation_euler),'target':list(target),'type':'ORTHO','ortho_scale':cam.data.ortho_scale,'resolution':[512,512],'source_frames':list(selected),'source_fps':30,'source_scene_fps':24,'samples':4 if probe else 2}
  print('HAND_PREVIEW_VIEW_DONE',view,len(selected),flush=True)
 (root/'RENDER_RECEIPT_R1.json').write_text(json.dumps({'candidate_SHA':D['candidate_SHA'],'cameras':cameras,'probe':probe,'no_mesh_visibility_material_source_write':True},indent=2),encoding='utf8')
 lane.off()
