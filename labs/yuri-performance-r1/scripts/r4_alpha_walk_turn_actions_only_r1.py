"""Reuse existing libraries.write route; source character remains immutable."""
import bpy,json,hashlib
from pathlib import Path
BASE=Path(r"C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs")
SOURCE=BASE/"alpha-walk-turn-candidate-r3/Character_R4_Walk_AttentionTurn_Stop_BODY_CANDIDATE_OFF_R3_20261004.blend"
OUT=BASE/"alpha-walk-turn-actions-only-r1"
EXPECTED="35c5a9d00bdef2ca2b82e35645bf9da87e6f050ae6ead0ce0a9f9bd859bbf026"
NAMES=["YURI_R4_WALK_TURN_STOP_BODY_R3","YURI_R4_WALK_TURN_STOP_ROOT_PATH_R3","YURI_R4_WALK_TURN_STOP_BODY_HEAD_TRANSPORT_R3","YURI_R4_WALK_TURN_STOP_BODY_HAIR_TRANSPORT_R3"]
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
OUT.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False)
LIB=OUT/"YURI_R4_WALK_TURN_STOP_ACTIONS_ONLY_R1.blend"
assert not LIB.exists()
bpy.data.libraries.write(str(LIB),{bpy.data.actions[n] for n in NAMES},fake_user=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(LIB),link=False) as (src,dst):
    assert sorted(src.actions)==sorted(NAMES)
    assert not src.objects and not src.meshes and not src.armatures
    dst.actions=list(NAMES)
assert len(bpy.data.actions)==4 and not bpy.data.objects and not bpy.data.meshes and not bpy.data.armatures
receipt={"source_candidate_sha256":EXPECTED,"file":LIB.name,"bytes":LIB.stat().st_size,"sha256":hashlib.sha256(LIB.read_bytes()).hexdigest(),"objects":len(bpy.data.objects),"meshes":len(bpy.data.meshes),"armatures":len(bpy.data.armatures),"action_names":NAMES,"fps":30,"character_geometry_included":False,"method":"existing bpy.data.libraries.write Action-only route"}
(OUT/"ACTION_ONLY_CUSTODY_R1.json").write_text(json.dumps(receipt,indent=2),encoding="utf8")
print(json.dumps(receipt),flush=True)
