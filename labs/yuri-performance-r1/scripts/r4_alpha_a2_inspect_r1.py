"""Fixed A1 source/donor inspection; private matrices, no save/export/render."""
import bpy,json,hashlib
from pathlib import Path
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'alpha-a2-inspect-r1'
PACKAGE=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1')
SOURCE=PACKAGE/'target-reference/Character_Master_NeckSkin_R4.blend'
DONOR=PACKAGE/'donors/A2_6a79b21a2dae5a576971/ba9ffd70eae04361.fbx'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(m):return [list(v) for v in m]
def bones(r):return {b.name:{'parent':b.parent.name if b.parent else None,'matrix_local':rows(b.matrix_local),'head':list(b.head_local),'tail':list(b.tail_local),'inherit_scale':b.inherit_scale,'use_deform':b.use_deform} for b in r.data.bones}
assert sha(SOURCE)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
assert sha(DONOR)=='2aab45156daf265bda22b8a345f470fba6760fb408ff90839881e5ba63999e4d'
OUT.mkdir(exist_ok=False)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.scene.render.fps=30
bpy.ops.import_scene.fbx(filepath=str(DONOR),use_anim=True,automatic_bone_orientation=False)
rigs=[o for o in bpy.data.objects if o.type=='ARMATURE'];assert len(rigs)==1
d=rigs[0];action=d.animation_data.action;assert action is not None
donor={'world':rows(d.matrix_world),'bones':bones(d),'action':action.name,'frame_range':list(action.frame_range),'fps':30,'samples':[],'source_original_fps':30.0003,'source_original_frame_range':[0, 3607]}
for frame in range(round(action.frame_range[0]),round(action.frame_range[1])+1):
    bpy.context.scene.frame_set(frame);bpy.context.view_layer.update()
    donor['samples'].append({b.name:rows(d.matrix_world@b.matrix) for b in d.pose.bones})
bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False)
s=bpy.context.scene
target={'frame':s.frame_current,'fps':s.render.fps/s.render.fps_base,'rigs':{o.name:{'world':rows(o.matrix_world),'bones':bones(o),'pose':{b.name:rows(b.matrix) for b in o.pose.bones},'constraints':{b.name:[{'type':c.type,'name':c.name,'target':getattr(getattr(c,'target',None),'name',None),'subtarget':getattr(c,'subtarget',None)} for c in b.constraints] for b in o.pose.bones if b.constraints},'active_action':o.animation_data.action.name if o.animation_data and o.animation_data.action else None} for o in bpy.data.objects if o.type=='ARMATURE'},'mesh_armatures':{o.name:[{'modifier':m.name,'rig':m.object.name if m.object else None} for m in o.modifiers if m.type=='ARMATURE'] for o in bpy.data.objects if o.type=='MESH'}}
result={'source_SHA':sha(SOURCE),'donor_SHA':sha(DONOR),'donor':donor,'target':target,'no_save_export_render':True}
with (OUT/'A2_SOURCE_DONOR_INSPECTION_PRIVATE_R1.json').open('x',encoding='utf8') as f:json.dump(result,f)
print('A1_INSPECTION_COMPLETE',list(target['rigs']),donor['action'],len(donor['samples']),flush=True)
