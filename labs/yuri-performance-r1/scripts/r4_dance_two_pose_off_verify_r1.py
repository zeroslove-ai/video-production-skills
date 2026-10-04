"""Read-only OFF verification; no pose re-authoring, rerender or candidate rewriting."""
import bpy,sys,json,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'dance-two-pose-off-verify-r1';O.mkdir(exist_ok=False);R=B/'dance-two-pose-native-r1'
P=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/target-reference/Character_Master_NeckSkin_R4.blend');C=R/'Character_R4_DanceStatic03_16_EXPERIMENT_OFF_R1_20261005.blend';L=R/'YURI_R4_DANCE_STATIC03_16_ACTIONS_ONLY_R1.blend';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
pins={str(p):sha(p) for p in [P,C,L,*R.glob('*.png')]}
bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);names=list(bpy.data.actions.keys());src=snapshot(names);tex={i.name:{'filepath':i.filepath,'resolved':bpy.path.abspath(i.filepath),'packed':[hashlib.sha256(x.packed_file.data).hexdigest() for x in i.packed_files]} for i in bpy.data.images if i.type!='RENDER_RESULT'}
with bpy.data.libraries.load(str(L),link=False) as (a,b):assert len(a.actions)==2 and not a.objects and not a.meshes and not a.armatures;b.actions=list(a.actions)
assert snapshot(names)==src
# On/off original source verifies restoration for each static Action; existing source never saved.
for n in ['YURI_R4_DANCE_STATIC_03_BODY_R1','YURI_R4_DANCE_STATIC_16_BODY_R1']:
 lane=ReactionLane();lane.on(n);lane.off();assert snapshot(names)==src
bpy.ops.wm.open_mainfile(filepath=str(C),use_scripts=False);can=snapshot(names);diff={k:{'source':src[k],'candidate':can[k]} for k in src if src[k]!=can[k]}
candidate_tex={i.name:{'filepath':i.filepath,'resolved':bpy.path.abspath(i.filepath),'packed':[hashlib.sha256(x.packed_file.data).hexdigest() for x in i.packed_files]} for i in bpy.data.images if i.type!='RENDER_RESULT'}
rawdiff={n:{'source':tex[n],'candidate':candidate_tex[n]} for n in tex if tex[n]!=candidate_tex[n]}
# Diagnostic normalization of only image path strings after SaveAs, transient/no save.
for n,v in tex.items():bpy.data.images[n].filepath=v['filepath']
norm=snapshot(names);remaining=[k for k in src if src[k]!=norm[k]]
assert all(sha(p)==v for p,v in pins.items())
d={'task':'ROOT_PM_DANCE_TWO_POSE_NATIVE_QA_R1','input_pins':pins,'source_SHA':sha(P),'action_only_library_source_OFF_full_snapshot_equal':True,'both_static_action_ON_OFF_source_snapshot_equal':True,'candidate_OFF_raw_snapshot_differing_categories':list(diff),'image_filepath_SaveAs_differences':rawdiff,'candidate_OFF_after_transient_source_image_path_strings_remaining_categories':remaining,'raw_candidate_OFF_equality_verdict':'PASS' if not diff else 'RAW_PATH_STRING_DIFF_NOT_WAIVED','source_original78Actions_preserved':len(names)==78,'geometry_rest_material_weights_morph_drivers_category_equality':{k:src[k]==can[k] for k in src if k not in ['textures']},'no_rerender_no_new_pose_no_candidate_write':True}
(O/'OFF_READONLY_VERIFY_RECEIPT_R1.json').write_text(json.dumps(d,indent=2),encoding='utf8');print('SOURCE_ACTION_LIBRARY_OFF_FULL_EQUAL_CANDIDATE_DIFF',list(diff),'REMAINING',remaining,flush=True)
