"""Disposable single GameRig export, preserving master and full baked rig motion."""
import bpy,json,sys,math
from pathlib import Path
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence/model-handoff-r4';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/r4-model-handoff')
bpy.ops.wm.open_mainfile(filepath=str(OUT/'Character_Master_Reaction_R4_20261002.blend'))
s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];rigs=[r,bpy.data.objects['Armature'],bpy.data.objects['Hair_Rig_R4']]
names=[a.name for a in bpy.data.actions if a.name.startswith('YRA_R4_')];samples={}
visible=[o for o in bpy.data.objects if o.type=='MESH' and not o.hide_render and any(m.type=='ARMATURE' and m.object in rigs for m in o.modifiers)]
mesh_worlds={o.name:o.matrix_world.copy() for o in visible}
for name in names:
 r.animation_data.action=bpy.data.actions[name];frames=[]
 for f in range(1,round(r.animation_data.action.frame_range[1])+1):
  s.frame_set(f);bpy.context.view_layer.update();frame={b.name:[list(row) for row in (o.matrix_world@b.matrix)] for o in rigs for b in o.pose.bones};frame['_pose_scales']={b.name:list(b.matrix.to_scale()) for o in rigs for b in o.pose.bones};frames.append(frame)
 samples[name]=frames
for o in rigs:
 o.animation_data_clear();o.hide_set(False)
 for b in o.pose.bones:
  b.matrix_basis=Matrix.Identity(4)
  for c in list(b.constraints):b.constraints.remove(c)
for o in bpy.context.selected_objects:o.select_set(False)
for o in rigs:o.select_set(True)
bpy.context.view_layer.objects.active=r;bpy.ops.object.join();r.name='GameRig_R4'
bpy.ops.object.mode_set(mode='EDIT');root=r.data.edit_bones.new('RuntimeRoot');root.head=(0,0,0);root.tail=(0,0,.1)
weighted={o.vertex_groups[g.group].name for o in visible for v in o.data.vertices for g in v.groups if g.weight>1e-8}
keep=set(weighted)
for n in list(weighted):
 if n not in r.data.edit_bones:continue
 b=r.data.edit_bones[n]
 while b.parent:keep.add(b.parent.name);b=b.parent
removed=[b.name for b in r.data.edit_bones if (b.name.startswith('J_Bip_') or b.name=='Root') and b.name not in keep]
for n in removed:r.data.edit_bones.remove(r.data.edit_bones[n])
for b in r.data.edit_bones:
 b.use_connect=False
 b.inherit_scale='FULL'
 b.use_inherit_rotation=True
 if b!=root and b.parent is None:b.parent=root
bpy.ops.object.mode_set(mode='OBJECT')
for o in visible:
 o.matrix_world=mesh_worlds[o.name]
 mods=[m for m in o.modifiers if m.type=='ARMATURE']
 for m in mods:m.object=r
 for m in mods[1:]:o.modifiers.remove(m)
 for g in o.vertex_groups:
  # Blender surface masks are retained, but only actual GameRig bone groups deform in FBX.
  pass
for a in list(bpy.data.actions):bpy.data.actions.remove(a)
inv=r.matrix_world.inverted();bakes=[]
for name,frames in samples.items():
 a=bpy.data.actions.new(name);a.use_fake_user=True;r.animation_data_create();r.animation_data.action=a;prev={}
 for f,frame in enumerate(frames,1):
  poses={'RuntimeRoot':r.data.bones['RuntimeRoot'].matrix_local.copy()}
  for b in r.pose.bones:
   if b.name=='RuntimeRoot':b.matrix_basis=Matrix.Identity(4);continue
   pose=inv@Matrix(frame[b.name]);pl,pq,ps=pose.decompose();pose=Matrix.LocRotScale(pl,pq,Vector(frame['_pose_scales'][b.name]));poses[b.name]=pose
   basis=b.bone.convert_local_to_pose(pose,b.bone.matrix_local,parent_matrix=poses[b.parent.name],parent_matrix_local=b.parent.bone.matrix_local,invert=True)
   loc,q,scale=basis.decompose()
   if b.name in prev and prev[b.name].dot(q)<0:q.negate()
   prev[b.name]=q.copy();b.rotation_mode='QUATERNION';b.location=loc;b.rotation_quaternion=q;b.scale=scale
   for prop in ('location','rotation_quaternion','scale'):b.keyframe_insert(prop,frame=f,group=b.name)
 for layer in a.layers:
  for st in layer.strips:
   for bag in st.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
 bakes.append({'action':name,'frames':len(frames)})
r.animation_data.action=None
for b in r.pose.bones:b.matrix_basis=Matrix.Identity(4)
s.frame_set(1)
for o in bpy.context.selected_objects:o.select_set(False)
r.select_set(True);bpy.context.view_layer.objects.active=r
for o in visible:o.hide_set(False);o.select_set(True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Character_GameRig_R4_20261002.blend'))
params=dict(use_selection=True,object_types={'ARMATURE','MESH'},add_leaf_bones=False,use_mesh_modifiers=False,path_mode='COPY',embed_textures=True)
bpy.ops.export_scene.fbx(filepath=str(OUT/'Character_GameRig_R4_20261002.fbx'),bake_anim=False,**params)
for o in visible:o.select_set(False)
for a in list(bpy.data.actions):
 if 'QA_' in a.name:bpy.data.actions.remove(a)
r.animation_data.action=None
for b in r.pose.bones:b.matrix_basis=Matrix.Identity(4)
s.frame_start=1;s.frame_end=37;s.frame_set(1);bpy.context.view_layer.update()
bpy.ops.export_scene.fbx(filepath=str(OUT/'YURI_REACTION_R4_ANIMATION_ONLY.fbx'),bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=False,bake_anim_use_all_actions=True,bake_anim_force_startend_keying=True,bake_anim_step=1,bake_anim_simplify_factor=0,**params)
report={'armatures':1,'bone_count':len(r.data.bones),'export_only_removed_unweighted_donor_bones':removed,'mesh_count':len(visible),'meshes':[o.name for o in visible],'full_rig_baked_actions':bakes,'production_fbx_takes':6,'root':'RuntimeRoot','deformation_transfer_limits':['FBX is linear skinning; native dual-quaternion + second masked linear skin modifier and pose-driven surface relaxation are not encoded.','Native gaze Geometry Nodes and Blender driver graphs are not Unity runtime logic.','Complex node material masks require material reconstruction; embedded images and native master are included.'],'vrm_reference':'Not generated: optional; no need to invent new license metadata or claim humanoid/expression acceptance before GameRig QA.'}
(E/'game_export.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('R4_GAME_EXPORT_DONE',len(r.data.bones),len(visible),flush=True)
