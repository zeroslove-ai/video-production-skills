"""Corrective checkpoint: fresh immutable R4 + eight pre-existing Actions only.

Run with Blender --factory-startup --background --disable-autoexec --python ...
Does not touch source R4, prior derivatives, rig hierarchy or any appearance data.
"""
import bpy,sys,json,hashlib,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference
from r4_appearance_adapter import ReactionLane
ROOT=HERE.parent
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/r4-appearance-preserve-correction-r1')
E=ROOT/'evidence/r4-appearance-preserve-correction-r1'
SOURCE=ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
DONOR=OUT.parent/'r4-model-handoff/Character_Master_Reaction_R4_20261002.blend'
EXPECTED='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
MASTER=OUT/'Character_R4_Animation_OFF_20261003.blend'
LIB=OUT/'YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'
NAMES=['YRA_R4_'+n for n in ['Startle_Short','Lift_Start','Struggle_Light_Loop','Struggle_Strong_Loop','Land_Soft','BalanceRecover','QA_MilestoneA_Sequence','QA_Release_Placeholder']]
def write(name,value):
    for p in (E/name,OUT/'metadata'/name):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf8')
def source_hash():return hashlib.sha256(SOURCE.read_bytes()).hexdigest()
assert source_hash()==EXPECTED
OUT.mkdir(parents=True,exist_ok=True);E.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False)
original_actions=[a.name for a in bpy.data.actions]
before=snapshot(original_actions);write('authority_before.json',before)
print('AUTHORITY_CAPTURED',flush=True)
with bpy.data.libraries.load(str(DONOR),link=False) as (src,dst):
    assert all(n in src.actions for n in NAMES),(NAMES,src.actions)
    dst.actions=list(NAMES)
for name in NAMES:bpy.data.actions[name].use_fake_user=True
after=snapshot(original_actions);delta=difference(before,after)
write('authority_after_append.json',after);write('append_diff.json',delta)
assert not delta,delta
assert len(bpy.data.actions)==len(original_actions)+len(NAMES)
# Save OFF: source pose channels, source frame, cameras, all binding/driver state.
bpy.ops.wm.save_as_mainfile(filepath=str(MASTER),relative_remap=False)
bpy.data.libraries.write(str(LIB),{bpy.data.actions[n] for n in NAMES},fake_user=True)
bpy.ops.wm.open_mainfile(filepath=str(MASTER),use_scripts=False)
reopened=snapshot(original_actions);delta=difference(before,reopened)
write('authority_reopened.json',reopened);write('reopen_diff.json',delta)
assert not delta,delta
lane=ReactionLane();lane.on('YRA_R4_Struggle_Strong_Loop');bpy.context.scene.frame_set(19);lane.off()
restored=snapshot(original_actions);delta=difference(before,restored)
write('authority_after_on_off.json',restored);write('on_off_diff.json',delta)
assert not delta,delta
assert source_hash()==EXPECTED
write('preservation_receipt.json',{'source_sha256':EXPECTED,'historical_checkpoint':'08caad76e6a279d07698cbfaa33d5c50f2aa097d',
    'canonical_visual_authority':'source/Character_Master_NeckSkin_R4.blend','source_original_actions':len(original_actions),
    'added_physical_clips':6,'added_QA_helpers':2,'appearance_differences':{},'append':'PASS','saved_reopen':'PASS','animation_ON_to_OFF':'PASS',
    'master_default':'ANIMATION OFF; original source pose, frame, action bindings and drivers',
    'prior_GameRig':'historical structural/animation compatibility experiment ONLY; NOT canonical appearance',
    'new_GameRig_construction':False,'mesh_merge':False,'donor_geometry_append':False,'source_immutable':True,
    'tested_categories':list(before),'Unity_runtime_AlwaysAnimate':'REQUIRED pending isolated product-owner import; not a Blender assertion'})
dest=OUT/'source';dest.mkdir(exist_ok=True)
shutil.copyfile(SOURCE,dest/SOURCE.name)
workflow=OUT/'workflow';workflow.mkdir(exist_ok=True)
for name in ['native_preservation.py','r4_appearance_adapter.py','r4_appearance_signature.py','r4_appearance_build.py']:
    shutil.copyfile(HERE/name,workflow/name)
print('R4_APPEARANCE_BUILD_PASS',flush=True)
