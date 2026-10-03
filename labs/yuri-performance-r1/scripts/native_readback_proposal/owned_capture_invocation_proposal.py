"""UNRUN future owned background invocation; no launch/build/download code here.
Use only after native compilation, wrapper link and denial self-tests accepted.
Supervisor must separately verify process exit0 and immutable/output hashes.
"""
from pathlib import Path
import hashlib, json, sys
import bpy
ROOT=Path(r'C:/YuriTransfer/native-cycles-readback-r1/capture')
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
SOURCE=Path(r'C:/Users/JAEWAN/projects/yuri-motion-previs-lab-r1/labs/yuri-performance-r1/local/model-handoff-r4/Character_Master_NeckSkin_R4.blend')
LIB=BASE/'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'
EXPECTED=BASE/'o1-guarded-native-resource-sizing-r1/expected-Strong6-v3'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert bpy.app.background and Path(bpy.data.filepath).resolve()==SOURCE.resolve()
assert sha(SOURCE)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
assert sha(LIB)=='6874ec69d5721f385d31edaa06ef0d58c89a543b98bacd961f8f575ff57eef4d'
receipt=json.loads((EXPECTED/'EXPECTED_INPUTS.json').read_text())
for row in receipt['files']: assert sha(EXPECTED/row['path'])==row['sha256']
# Reuse existing preservation/signature adapter. No other datablocks appended.
WORKFLOW=Path(r'C:/Users/JAEWAN/projects/yuri-motion-previs-lab-r1/labs/yuri-performance-r1/scripts')
sys.path.insert(0,str(WORKFLOW))
from r4_appearance_signature import snapshot, difference
from r4_appearance_adapter import ReactionLane
original_actions=[a.name for a in bpy.data.actions]
before=snapshot(original_actions)
clip='YRA_R4_Struggle_Strong_Loop'
with bpy.data.libraries.load(str(LIB),link=False) as (src,dst):dst.actions=[clip]
assert not difference(before,snapshot(original_actions)),'source appearance/component drift after action append'
lane=ReactionLane()
try:
    lane.on(clip);bpy.context.scene.frame_set(6)
    dg=bpy.context.evaluated_depsgraph_get()
    scene=bpy.context.scene
    temporal={'source_motion_blur':getattr(scene.render,'use_motion_blur',None),
     'frame':scene.frame_current,'subframe':scene.frame_subframe,'fps':scene.render.fps,
     'fps_base':scene.render.fps_base}
    assert ROOT.is_dir(),'Supervisor creates only the approved owned process directory'
    output=ROOT/'Strong6-native-host';audit=ROOT/'Strong6-native-audit.jsonl'
    assert not output.exists() and not audit.exists()
    import _cycles
    assert hasattr(_cycles,'host_mesh_readback'),'compile/link/registration acceptance missing'
    assert _cycles.host_mesh_readback(bpy.context,bpy.context.preferences,dg,
     str(EXPECTED),str(output),str(audit)) is True
    after_temporal={'source_motion_blur':getattr(scene.render,'use_motion_blur',None),
     'frame':scene.frame_current,'subframe':scene.frame_subframe,'fps':scene.render.fps,
     'fps_base':scene.render.fps_base}
    assert after_temporal==temporal
    events=[json.loads(line) for line in audit.read_text().splitlines()]
    assert events[-1]=={'native_driver_returned':True,'native_engine_freed':True}
    ended=next(row for row in events if row.get('scope_ended'))
    assert ended['denied_attempts']==0 and ended['CPU_contexts']==1
finally:
    lane.off()
    assert not difference(before,snapshot(original_actions)),'ON→OFF source drift'
assert sha(SOURCE)==receipt['source_R4_sha256'] and sha(LIB)==receipt['Action_library_sha256']
files=[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(output.iterdir()) if p.is_file()]
result={'status':'DATA_AND_NATIVE_CLEANUP_VALIDATED_PENDING_SUPERVISOR_EXIT0',
 'source_temporal_settings':temporal,'OFF_restore_exact':True,
 'source_temporal_settings_unchanged':after_temporal==temporal,
 'local_ccl_motion':'MOTION_NONE_FORCED_CUSTOM_HOST_CENTER_SNAPSHOT',
 'installed_renderer_equivalence':False,'runtime_PBR':'HOLD','files':files}
(ROOT/'Strong6-pending-process-exit.json').write_text(json.dumps(result,indent=2))
# Do not write final acceptance here; supervisor owns process/tree cleanup receipt.
