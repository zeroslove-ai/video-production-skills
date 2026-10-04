"""Fixed read-only saved A2-A4 OFF structural reopen oracle; no rendering or saves."""
import bpy,json,sys,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
source=HERE.parent/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(source)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
out=BASE/'alpha-first4-reopen-off-r1';out.mkdir(exist_ok=False)
bpy.ops.wm.open_mainfile(filepath=str(source),use_scripts=False);names=[a.name for a in bpy.data.actions];authority=snapshot(names);result={}
for step in ['a2','a3','a4']:
 d=json.loads((BASE/f'alpha-{step}-contact-candidate-r2/CONTACT_CANDIDATE_PRIVATE_R2.json').read_bytes());candidate=Path(d['candidate']);assert sha(candidate)==d['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=str(candidate),use_scripts=False);actual=snapshot(names);diff=difference(authority,actual);assert diff=={},str(diff)
 result[step]={'candidate_SHA':sha(candidate),'source_SHA':sha(source),'original_action_count':len(names),'saved_OFF_full_snapshot_exact':True,'full_snapshot_digest':hashlib.sha256(json.dumps(actual,sort_keys=True).encode()).hexdigest(),'scene_fps':bpy.context.scene.render.fps/bpy.context.scene.render.fps_base,'action_fps':float(bpy.data.actions[d['action']]['source_fps']),'categories':list(actual),'diff':diff,'no_save_render_export_source_Unity_write':True}
with (out/'SAVED_OFF_FULL_SIGNATURE_REOPEN_R1.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
print('SAVED_OFF_SOURCE_REOPEN_EXACT',list(result),flush=True)
