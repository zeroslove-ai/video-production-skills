"""Fresh FBX import, full clip skeleton comparison and CPU visual roundtrip."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence/model-handoff-r4';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/r4-model-handoff')
bpy.ops.wm.open_mainfile(filepath=str(OUT/'Character_GameRig_R4_20261002.blend'));r=bpy.data.objects['GameRig_R4'];s=bpy.context.scene
refs={};skinrefs={}
for a in bpy.data.actions:
 if not a.name.startswith('YRA_R4_') or 'QA_' in a.name:continue
 r.animation_data.action=a;r.animation_data.action_slot=a.slots[0];end=round(a.frame_range[1]);frames=[]
 for f in range(1,end+1):
  s.frame_set(f);bpy.context.view_layer.update();frames.append({b.name:list(r.matrix_world@b.head) for b in r.pose.bones})
  if f in {1,round(end/2),end}:
   o=bpy.data.objects['Meshy_Body_NeutralCovered'].evaluated_get(bpy.context.evaluated_depsgraph_get());skinrefs[a.name,f]=[o.matrix_world@v.co for v in o.data.vertices]
 refs[a.name]=frames
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
for a in list(bpy.data.actions):bpy.data.actions.remove(a)
bpy.ops.import_scene.fbx(filepath=str(OUT/'Character_GameRig_R4_20261002.fbx'))
rigs=[o for o in bpy.data.objects if o.type=='ARMATURE'];assert len(rigs)==1;r=rigs[0]
meshes=[o for o in bpy.data.objects if o.type=='MESH'];assert len(meshes)==21 and len(r.data.bones)==json.loads((E/'game_export.json').read_text())['bone_count']
shape_counts={o.name:len(o.data.shape_keys.key_blocks) if o.data.shape_keys else 0 for o in meshes}
bpy.ops.import_scene.fbx(filepath=str(OUT/'YURI_REACTION_R4_ANIMATION_ONLY.fbx'))
extra=[o for o in bpy.data.objects if o.type=='ARMATURE' and o!=r]
actions=[a for a in bpy.data.actions if 'YRA_R4_' in a.name];assert len(actions)==6
for o in extra:bpy.data.objects.remove(o,do_unlink=True)
s=bpy.context.scene;s.render.fps=24;s.render.fps_base=1
checks=[]
for a in actions:
 name=next(n for n in refs if n in a.name);r.animation_data_create();r.animation_data.action=a;r.animation_data.action_slot=a.slots[0];end=len(refs[name]);errors=[];skin=[]
 for f in range(1,end+1):
  s.frame_set(f);bpy.context.view_layer.update();pairs=[((r.matrix_world@b.head-Vector(refs[name][f-1][b.name])).length,b.name) for b in r.pose.bones];errors.append(max(pairs)[0])
  if f==1:print('FIRST_WORST',name,max(pairs),flush=True)
  if (name,f) in skinrefs:
   o=bpy.data.objects['Meshy_Body_NeutralCovered'].evaluated_get(bpy.context.evaluated_depsgraph_get());vs=skinrefs[name,f]
   if len(vs)==len(o.data.vertices):skin.append({'frame':f,'max_corresponding_vertex_difference_m':max((o.matrix_world@v.co-p).length for v,p in zip(o.data.vertices,vs))})
 checks.append({'action':name,'frames':end,'max_world_joint_position_error_m':max(errors),'sampled_skin_difference':skin,'skeleton_roundtrip':'PASS' if max(errors)<1e-4 else 'FAIL'})
missing=[i.name for i in bpy.data.images if i.source=='FILE' and not i.packed_file and not Path(bpy.path.abspath(i.filepath)).is_file()]
report={'master_armatures':1,'master_bones':len(r.data.bones),'master_meshes':len(meshes),'shape_key_counts':shape_counts,'imported_actions':len(actions),'clips':checks,'missing_images':missing,'runtime_engine':'Fresh Blender FBX importer; Unity untested'}
(E/'fbx_roundtrip.json').write_text(json.dumps(report,indent=2),encoding='utf8')
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=4;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=256;s.render.resolution_y=384;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
s.world=bpy.data.worlds.new('QAWorld');s.world.color=(.12,.14,.18)
for name,loc,power in [('Key',(-1,-2,2),140),('Fill',(1,-1,1.3),65)]:
 d=bpy.data.lights.new(name,'AREA');o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=loc;d.energy=power;d.size=1.4;o.rotation_euler=(Vector((0,0,.6))-o.location).to_track_quat('-Z','Y').to_euler()
d=bpy.data.cameras.new('QA');cam=bpy.data.objects.new('QA',d);s.collection.objects.link(cam);s.camera=cam;d.type='ORTHO';d.ortho_scale=1.18;cam.location=(1.8,-3,.62);cam.rotation_euler=(Vector((.002,-.025,.49))-cam.location).to_track_quat('-Z','Y').to_euler()
for a in actions:
 name=next(n for n in refs if n in a.name);r.animation_data.action=a;r.animation_data.action_slot=a.slots[0]
 for f in sorted({1,round(len(refs[name])/2),len(refs[name])}):
  s.frame_set(f);dest=OUT/'fbx_roundtrip_frames'/name;dest.mkdir(parents=True,exist_ok=True);s.render.filepath=str(dest/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Character_GameRig_R4_FBX_Roundtrip_QA.blend'))
print('R4_FBX_ROUNDTRIP',[(c['action'],c['max_world_joint_position_error_m']) for c in checks],flush=True)
