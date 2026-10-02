"""Export QA sequence take, then re-import on GameRig mesh for full CPU playback."""
import bpy,json
from pathlib import Path
from mathutils import Vector,Matrix
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/r4-model-handoff')
bpy.ops.wm.open_mainfile(filepath=str(OUT/'Character_GameRig_R4_20261002.blend'));r=bpy.data.objects['GameRig_R4']
for o in bpy.context.selected_objects:o.select_set(False)
r.hide_set(False);r.select_set(True);bpy.context.view_layer.objects.active=r
for a in list(bpy.data.actions):
 if a.name!='YRA_R4_QA_MilestoneA_Sequence':bpy.data.actions.remove(a)
r.animation_data.action=None
for b in r.pose.bones:b.matrix_basis=Matrix.Identity(4)
bpy.context.scene.frame_set(1);bpy.context.view_layer.update()
bpy.ops.export_scene.fbx(filepath=str(OUT/'YURI_REACTION_R4_QA_SEQUENCE.fbx'),use_selection=True,object_types={'ARMATURE'},add_leaf_bones=False,bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=True,bake_anim_step=1,bake_anim_simplify_factor=0)
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
for a in list(bpy.data.actions):bpy.data.actions.remove(a)
bpy.ops.import_scene.fbx(filepath=str(OUT/'Character_GameRig_R4_20261002.fbx'));r=next(o for o in bpy.data.objects if o.type=='ARMATURE')
bpy.ops.import_scene.fbx(filepath=str(OUT/'YURI_REACTION_R4_QA_SEQUENCE.fbx'));a=next(a for a in bpy.data.actions if 'MilestoneA_Sequence' in a.name)
for o in list(bpy.data.objects):
 if o.type=='ARMATURE' and o!=r:bpy.data.objects.remove(o,do_unlink=True)
r.animation_data_create();r.animation_data.action=a;r.animation_data.action_slot=a.slots[0]
s=bpy.context.scene;s.render.fps=24;s.render.fps_base=1;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=4;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=256;s.render.resolution_y=384;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
s.world=bpy.data.worlds.new('QAWorld');s.world.color=(.12,.14,.18)
for name,loc,power in [('Key',(-1,-2,2),140),('Fill',(1,-1,1.3),65)]:
 d=bpy.data.lights.new(name,'AREA');o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;d.energy=power;d.size=1.4;o.rotation_euler=(Vector((0,0,.6))-o.location).to_track_quat('-Z','Y').to_euler()
d=bpy.data.cameras.new('QA');cam=bpy.data.objects.new('QA',d);s.collection.objects.link(cam);s.camera=cam;d.type='ORTHO';d.ortho_scale=1.18;cam.location=(1.8,-3,.62);cam.rotation_euler=(Vector((.002,-.025,.49))-cam.location).to_track_quat('-Z','Y').to_euler()
dest=OUT/'fbx_sequence_frames';dest.mkdir(exist_ok=True)
for f in range(1,266):
 s.frame_set(f);s.render.filepath=str(dest/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
print('R4_FBX_SEQUENCE_RENDER_DONE',flush=True)
