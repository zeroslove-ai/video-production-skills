"""Bounded original-source finger inventory; no pose/rig/mesh edits or saves."""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-hand-relax-inspect-r1';O.mkdir(exist_ok=False)
S=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/target-reference/Character_Master_NeckSkin_R4.blend');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(S)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
bpy.ops.wm.open_mainfile(filepath=str(S),use_scripts=False);r=bpy.data.objects['Meshy_Fitted_Rig'];m=bpy.data.objects['Meshy_Body_NeutralCovered'];names=[f'{finger}{j}.R' for finger in ['index','middle','ring','pinky','thumb'] for j in [1,2,3]]
weights={}
for n in ['hand.R',*names]:
 g=m.vertex_groups.get(n);w=[x.weight for v in m.data.vertices for x in v.groups if g and x.group==g.index];weights[n]={'vertices':len(w),'max':max(w,default=0),'sum':sum(w)}
actions=[]
for a in bpy.data.actions:
 channels=[]
 for layer in a.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     if any(('"'+n+'"') in fc.data_path for n in names):channels.append(fc.data_path)
 if channels:actions.append({'name':a.name,'range':list(a.frame_range),'channels':sorted(set(channels))})
bones={n:{'parent':r.pose.bones[n].parent.name,'rest_matrix':[list(row) for row in r.data.bones[n].matrix_local],'pose_matrix':[list(row) for row in r.pose.bones[n].matrix],'world_head':list(r.matrix_world@r.pose.bones[n].head),'world_tail':list(r.matrix_world@r.pose.bones[n].tail),'constraints':[c.type for c in r.pose.bones[n].constraints],'rotation_mode':r.pose.bones[n].rotation_mode,'basis':[list(row) for row in r.pose.bones[n].matrix_basis],'deform':r.data.bones[n].use_deform} for n in ['hand.R',*names]}
report={'source_SHA':sha(S),'original_actions':len(bpy.data.actions),'native_finger_bones':30,'right_finger_bones':names,'bones':bones,'weights':weights,'existing_finger_actions':actions,'modifiers':[{'type':x.type,'name':x.name,'object':getattr(getattr(x,'object',None),'name',None)} for x in m.modifiers],'rig_world':[list(row) for row in r.matrix_world],'source_saved':False,'mutation':False}
(O/'NATIVE_FINGER_INVENTORY_PRIVATE_R1.json').write_text(json.dumps(report,indent=2),encoding='utf8');assert sha(S)==report['source_SHA'];print('NATIVE_FINGER_INVENTORY_PASS',weights,len(actions),flush=True)
