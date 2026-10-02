"""Sample preserved polished reaction rig in its own source space, read-only."""
import bpy,json,sys
from pathlib import Path
root=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
bpy.ops.wm.open_mainfile(filepath=str(root/'Character_ReactionFactory_R1_Polished.blend'))
r=bpy.data.objects['Armature'];s=bpy.context.scene
for t in r.animation_data.nla_tracks:t.mute=True
names=[a.name for a in bpy.data.actions if a.name.startswith('YRA_R1_') and not any(x in a.name for x in ('FACE_','GAZE_'))]
data={'rest':{b.name:[list(row) for row in b.matrix_local] for b in r.data.bones},'matrix_world':[list(row) for row in r.matrix_world],'clips':{}}
for name in names:
 a=bpy.data.actions[name];r.animation_data.action=a;n=round(a.frame_range[1]);samples=[]
 for f in range(1,n+1):
  s.frame_set(f);bpy.context.view_layer.update();samples.append({b.name:[list(row) for row in b.matrix] for b in r.pose.bones})
 data['clips'][name]=samples
out=Path(sys.argv[sys.argv.index('--')+1]);out.write_text(json.dumps(data),encoding='utf8');print('REACTION_SOURCE',[(n,len(v)) for n,v in data['clips'].items()])
