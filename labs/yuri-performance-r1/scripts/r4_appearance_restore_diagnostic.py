import bpy,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from r4_appearance_adapter import ReactionLane
from r4_appearance_signature import props,anim,custom
p=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/r4-appearance-preserve-correction-r1/Character_R4_Animation_OFF_20261003.blend')
bpy.ops.wm.open_mainfile(filepath=str(p),use_scripts=False)
r=bpy.data.objects['Meshy_Fitted_Rig']
def state():return {'obj':props(r),'anim':anim(r),'pose':{b.name:props(b) for b in r.pose.bones},'custom':custom(r)}
a=state();lane=ReactionLane();lane.on('YRA_R4_Struggle_Strong_Loop');bpy.context.scene.frame_set(19);lane.off();b=state()
for c in a:
 if a[c]!=b[c]:
  print('DIFF',c,json.dumps({k:[a[c].get(k),b[c].get(k)] for k in set(a[c])|set(b[c]) if a[c].get(k)!=b[c].get(k)},indent=2))
print('AD_RNA',[(p.identifier,p.is_readonly) for p in r.animation_data.bl_rna.properties])
