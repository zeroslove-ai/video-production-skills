"""Fixed staged CC0 walk RM/MIT attention-turn inspection; original R4 read only."""
import bpy,json,hashlib
from pathlib import Path
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');OUT=BASE/'alpha-walk-turn-inspect-r1';OUT.mkdir(exist_ok=False)
SOURCE=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/target-reference/Character_Master_NeckSkin_R4.blend')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(m):return [list(v) for v in m]
def bones(r):return {b.name:{'parent':b.parent.name if b.parent else None,'matrix_local':rows(b.matrix_local),'head':list(b.head_local),'tail':list(b.tail_local)} for b in r.data.bones}
donors={}
for label,file,h in [('walk','Native/5a5f5de6f18e9c91.fbx','5a5f5de6f18e9c91cdbc40eb26319ec85cc45070bc00965bc2737beb4b2984ea'),('turn_proxy','BVH/bc5e6bd9a98755f6.fbx','417f3257f323815c13dc89ca5bfe4349ef58f762a990b093bbc5acf2eaed45da')]:
 path=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/UnityQA/Assets/Motions')/file;assert sha(path)==h;bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.render.fps=30;bpy.ops.import_scene.fbx(filepath=str(path),use_anim=True,automatic_bone_orientation=False);rs=[o for o in bpy.data.objects if o.type=='ARMATURE'];assert len(rs)==1;r=rs[0]
 actions=[a for a in bpy.data.actions if 'Walk_Loop' in a.name or 'Idle_Loop' in a.name] if label=='walk' else [r.animation_data.action];clips={}
 for a in actions:
  r.animation_data.action=a
  if a.slots:r.animation_data.action_slot=a.slots[0]
  start,end=map(round,a.frame_range);samples=[]
  for f in range(start,end+1):
   bpy.context.scene.frame_set(f);bpy.context.view_layer.update();samples.append({b.name:rows(r.matrix_world@b.matrix) for b in r.pose.bones})
  clips[a.name]={'frame_range':list(a.frame_range),'sampled_frames':[start,end],'samples':samples}
 donors[label]={'file':str(path),'sha256':sha(path),'bytes':path.stat().st_size,'world':rows(r.matrix_world),'bones':bones(r),'clips':clips,'source_fps':30,'original_BVH_fps':30.0003 if label=='turn_proxy' else None,'all_imported_actions':[a.name for a in bpy.data.actions]}
assert sha(SOURCE)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa';bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False)
target={'objects':{o.name:{'type':o.type,'parent':o.parent.name if o.parent else None,'parent_type':o.parent_type,'parent_bone':o.parent_bone,'world':rows(o.matrix_world),'constraints':[{'name':c.name,'type':c.type,'target':getattr(getattr(c,'target',None),'name',None),'subtarget':getattr(c,'subtarget',None)} for c in o.constraints],'modifiers':[{'type':m.type,'object':getattr(getattr(m,'object',None),'name',None)} for m in o.modifiers]} for o in bpy.data.objects},'rigs':{o.name:{'world':rows(o.matrix_world),'bones':bones(o)} for o in bpy.data.objects if o.type=='ARMATURE'},'fps':bpy.context.scene.render.fps/bpy.context.scene.render.fps_base,'actions':len(bpy.data.actions)}
with (OUT/'WALK_TURN_SOURCE_INSPECTION_PRIVATE_R1.json').open('x',encoding='utf8') as f:json.dump({'source':str(SOURCE),'source_SHA':sha(SOURCE),'donors':donors,'target':target,'no_save_export_source_mutation':True},f)
print('STAGED_WALK_TURN_INSPECTION_DONE',{k:list(v['clips']) for k,v in donors.items()},flush=True)
