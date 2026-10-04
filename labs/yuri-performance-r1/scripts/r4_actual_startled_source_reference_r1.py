"""One actual FACE16 expression on immutable original R4; source-rest diagnostic only."""
import bpy,sys,json,hashlib,time
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference,props
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
SOURCE=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/target-reference/Character_Master_NeckSkin_R4.blend')
OUT=BASE/'r4-actual-startled-mouth-source-reference-r1'
SHA='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
FACE=['JawOpen','Smile.L','Smile.R','Blink.L','Blink.R','BrowRaise.L','BrowRaise.R','BrowKnit.L','BrowKnit.R','CheekLift.L','CheekLift.R','LipPucker','MouthWide','ExprSmileCurve','ExprMouthDown','ExprBrowInnerUp']
INPUT=[.72,.000242401089,.000242401089,0,0,.92,.84,0,0,0,0,0,.16,0,0,.15]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 assert not OUT.exists() and sha(SOURCE)==SHA;OUT.mkdir()
 bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False)
 s=bpy.context.scene;assert s.frame_current==1
 head=bpy.data.objects['Character_Body_Head'];keys=head.data.shape_keys
 names=set(bpy.data.actions.keys());before=snapshot(names)
 saved=[k.value for k in keys.key_blocks];gaze=[head['Face_GazeYaw'],head['Face_GazePitch']]
 assert s.camera.name=='Assembly_Review_Camera'
 camera={'name':s.camera.name,'matrix_world':[list(r) for r in s.camera.matrix_world],'settings':props(s.camera.data),'resolution':[s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage],'policy':'Unchanged authored source head close camera; runtime camera correspondence UNKNOWN'}
 for name,value in zip(FACE,INPUT):keys.key_blocks[name].value=value
 head['Face_GazeYaw']=.04;head['Face_GazePitch']=.45
 head.update_tag();keys.update_tag();s.frame_set(1);bpy.context.view_layer.update()
 e=head.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();coords=np.array([tuple(v.co) for v in m.vertices]);assert np.isfinite(coords).all()
 evaluated={'stage':'FULL_SOURCE original Geometry Nodes + Armature modifier stack','vertices':len(m.vertices),'polygons':len(m.polygons),'corners':len(m.loops),'finite':True,'modifier_flags':[[x.name,x.type,x.show_viewport,x.show_render] for x in head.modifiers]};e.to_mesh_clear()
 readback={k.name:k.value for k in keys.key_blocks}
 # Render in a transient scene copy: original camera, lights, world and material operands remain authored.
 render_scene=s.copy();render_scene.name='TEMP_SOURCE_EXPRESSION_REFERENCE'
 render_scene.render.engine='CYCLES';render_scene.cycles.device='CPU';render_scene.cycles.samples=8;render_scene.cycles.seed=0;render_scene.cycles.use_animated_seed=False;render_scene.cycles.use_denoising=False
 render_scene.render.threads_mode='FIXED';render_scene.render.threads=2
 render_scene.render.image_settings.file_format='PNG';render_scene.render.image_settings.color_mode='RGBA';render_scene.render.image_settings.color_depth='8'
 png=OUT/'R4_SOURCE_ACTUAL_STARTLED_MOUTH98_REST_R1.png';render_scene.render.filepath=str(png)
 bpy.ops.render.render(write_still=True,scene=render_scene.name)
 bpy.data.scenes.remove(render_scene)
 for key,value in zip(keys.key_blocks,saved):key.value=value
 head['Face_GazeYaw'],head['Face_GazePitch']=gaze
 head.update_tag();keys.update_tag();s.frame_set(1);bpy.context.view_layer.update()
 after=snapshot(names);delta=difference(before,after);assert not delta,delta
 assert sha(SOURCE)==SHA
 receipt={'source':str(SOURCE),'source_SHA256':SHA,'source_bytes_unchanged':True,'source_frame':1,'runtime_witness_seconds':2.96682239,'runtime_label':'Mouth98','frame_domain':'Runtime witness label is NOT authored Blender frame 98','native_FACE16':dict(zip(FACE,INPUT)),'native_GAZE2':[.04,.45],'evaluated_key_readback':readback,'evaluated':evaluated,'camera':camera,'source_restore_signature_difference':delta,'original_actions_preserved':len(names),'source_body_pose':'Original source-rest; exact runtime bone pose UNKNOWN','runtime_camera':'UNKNOWN','parity':'UNKNOWN; source-only expression reference, no full Blender/Player parity claim','render':{'CPU_threads':2,'samples':8,'seed':0,'original_color_world_lights_materials':True},'image_SHA256':sha(png),'no_source_save_export_product_change':True}
 with (OUT/'SOURCE_REFERENCE_PRIVATE_R1.json').open('x',encoding='utf8') as f:json.dump(receipt,f,indent=2)
 print('SOURCE_EXPRESSION_REFERENCE_PASS',sha(png),flush=True)
if __name__=='__main__':main()
