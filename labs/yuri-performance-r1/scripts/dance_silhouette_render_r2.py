"""CPU actual-mesh alpha silhouettes using the frozen image-fit camera."""
from pathlib import Path
import bpy,json,math,hashlib,sys
R=Path(__file__).resolve().parents[1];E=R/'evidence/dance-benchmark-r1';L=R/'local/dance-benchmark-r1';method=sys.argv[-1];path=L/(method+'_DANCE_R1.blend');sha=hashlib.sha256(path.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(path));s=bpy.context.scene;rig=bpy.data.objects['ProxyHumanoid'];camera=json.loads((E/'arm_reprojection_r2.json').read_text())['camera_fit_frozen_from_r1'];scale=camera['scale_px_per_m'];ox,oy=camera['translation_px'];cx=(1380+230-ox)/scale;cz=-(100+460-oy)/scale
for o in bpy.data.objects:
    if o.type=='MESH':o.hide_render=not any(m.type=='ARMATURE' and m.object==rig for m in o.modifiers)
bpy.ops.object.camera_add(location=(cx,-5,cz));cam=bpy.context.object;cam.rotation_euler=(math.pi/2,0,0);cam.data.type='ORTHO';cam.data.ortho_scale=920/scale;s.camera=cam;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=1;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=230;s.render.resolution_y=460;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';folder=L/(method+'_silhouette_'+sha[:10]);folder.mkdir(exist_ok=True)
for fi in range(360):
    s.frame_set(fi+1);p=folder/f'{fi:04d}.png'
    if not p.exists():s.render.filepath=str(p);bpy.ops.render.render(write_still=True)
    if fi%60==0:print('MESH_SILHOUETTE',method,fi,flush=True)
assert hashlib.sha256(path.read_bytes()).hexdigest()==sha
(E/(method+'_silhouette_render.json')).write_text(json.dumps({'method':method,'candidate_sha256':sha,'frames':360,'resolution':[230,460],'camera_frozen_from_r1':camera,'ortho_camera_location':[cx,-5,cz],'ortho_scale':920/scale,'render_folder':str(folder),'engine':'CYCLES_CPU','samples':1,'actual_geometry':'armature-modified proxy meshes, floor hidden, alpha mask; not capsule approximation','scope':'proxy body/clothing proportions differ; reference mask still model-derived, not manual silhouette ground truth'},indent=2))
