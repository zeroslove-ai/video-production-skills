"""Freeze compact dense-half addendum, no Blender job or duplicated authority."""
import json,hashlib,zipfile,shutil
import numpy as np
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;E=ROOT/'evidence/o1-dense-half-expression-r1';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-dense-half-expression-r1')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((E/'DENSE_HALF_SOURCE_RECEIPT.json').read_text(encoding='utf8'));p=OUT/receipt['dense_file']['path'];assert sha(p)==receipt['dense_file']['sha256'];data=np.load(p,allow_pickle=False)
assert len(data.files)==105 and all(np.isfinite(data[k]).all() for k in data.files)
attempt=np.load(OUT/'R4_Existing_DirectMorph_Half_Dense_20261003_R1_attempt01.npz',allow_pickle=False);assert set(attempt.files)==set(data.files) and all(np.array_equal(attempt[k],data[k]) for k in data.files)
report='''# R4 dense existing direct morph HALF reference R1 — 2026-10-03 KST

**Source-data addendum complete; no appearance/F2/F3/Unity/Player PASS.** Original immutable master SHA a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa and13muted bridges preserved. No GUI, source save, unmute, new rig, rest/Action/weight/material changes, video, bake or export trial.

## Dense data and correspondence

R4_Existing_DirectMorph_Half_Dense_20261003_R1.npz contains84dense world-position arrays (4groups×21original renderers) plus21uint8 polygon-used masks. Group names blink/smile/jaw/brow match existing peak NPZ schema: `<group>_<renderer>`. Array shape is originalVertexCount×3, float32 little-endian world meters. Masks `<renderer>_polygon_used_mask` use source polygon/corner loop vertex indices;1=polygon referenced,0=loose. No pruning/splitting/height rescale. Head12928 vertices includes12093polygon-used +835loose, all indexed.

Source original mesh/basis/UV/corner/polygon data and dense0/1 references are reused by exact recovery ZIP080352e24adb9db33e76e92d8aca9836aeaf444ed75818c29e2970a32dae47df pointers in REUSED_ZERO_PEAK_BASIS_POINTERS.json. No master, textures or peak arrays duplicated. Basis positions hash/mesh NPZ SHA and every dense array hash/shape are in DENSE_HALF_SOURCE_RECEIPT.json. Consumer must map all original source indices explicitly, including loose vertices; polygon-only and all-vertex results are separately reported.

## Exact half controls and outputs

blink: Blink.L/R=.5; smile: Smile.L/R=.5; jaw: JawOpen=.5; brow: BrowRaise.L/R=.5. Each group restores all original defaults before/after sampling. AST extraction reuses only exact setinput/evaluate functions from existing r4_recovery_manual_morph.py; no top-level render code executes. Receipt contains evaluated head/lash/other ShapeKey values,8material driver socket outputs,GN control driver outputs and13preserved muted bridge flags, for every half and restored OFF case.

Head half max/RMS (meters): Blink0.006898182910/0.001874510432; Smile0.001194746583/0.000181381081; Jaw0.002727372805/0.000823288341; Brow0.001299989060/0.000200451861. All21renderer max/RMS/changed counts exactly match the prior manual-morph half summary for all4groups. OFF-return geometry0m for every group; full source component diff={}; original78Actions unchanged and master SHA reverified.

## Numerical provenance and retry

Manual evaluate uses np.array(mathutils.Matrix) float32 matrix arithmetic, final outputfloat32. The previous source-data neutral NPZ used explicit float64 matrix arithmetic before float32 storage. Reused zero differs at most1.666000493e-8m; exact perrenderer delta/byte-equality flags are recorded, not hidden or compensated. Source-native half arrays and previous half summary match exactly. Consumers should account for this declared zero-reference arithmetic difference instead of pruning loose vertices or changing the source.

One bounded CPU extraction task completed after two process attempts: initial extra byte-equality guard against the reused0 reference aborted receipt writing after NPZ extraction; the guard was changed to report the observed precision difference. Second attempt produced full receipt/component restoration proof. Both attempts'105array values are byte-identical. No second export or additional video/bake/motion job. Fresh factory Blender5.2.1LTS --background --disable-autoexec/use_scripts=False. Failed attempt data/log retained locally, omitted from compact addendum as duplicate.

## Boundary

This supplies actual dense0.5 source reference for direct comparison with Unity. It does not repair Unity correspondence, set tolerances, alter source geometry, certify material/face identity or claim F2/F3 performance. Existing source rotation/bind/material/deformation/Player gates remain separate. No further work until PM review.
'''
for path in (E/'YURI_O1_DENSE_HALF_EXPRESSION_R1.md',OUT/'README.md'):path.write_text(report,encoding='utf8')
summary={'task':'YURI_O1_DENSE_HALF_EXPRESSION_REFERENCE_R1','status':'DENSE_HALF_DATA_COMPLETE / PM_REVIEW','source_preservation_PASS':True,'source_component_diff':{},'source_SHA256':receipt['source_SHA256'],'groups':4,'renderers':21,'dense_arrays':84,'mask_arrays':21,'head_total_vertices':12928,'head_polygon_used_vertices':12093,'head_loose_vertices':835,'pruned_vertices':0,'all_prior_half_summary_metrics_equal':True,'OFF_return_world_geometry_max_m':0,'reused_zero_precision_max_delta_m':max(r['max_zero_reference_delta_m'] for r in receipt['reused_zero_reference_comparison']),'original13bridges_muted':True,'one_completed_bounded_data_task':True,'background_attempts':2,'first_second_dense_arrays_identical':True,'no_video_bake_export':True,'F2_F3_appearance_Unity_Player_PASS':False,'next':'PM custody review; consumer all-index dense-half comparison'}
for path in (E/'HALF_ADDENDUM_DISPOSITION.json',OUT/'HALF_ADDENDUM_DISPOSITION.json'):path.write_text(json.dumps(summary,indent=2),encoding='utf8')
shutil.copyfile(HERE/'r4_dense_half_expression_reference.py',OUT/'r4_dense_half_expression_reference.py');shutil.copyfile(Path(__file__),OUT/'r4_dense_half_package.py')
files=[p,OUT/'DENSE_HALF_SOURCE_RECEIPT.json',OUT/'REUSED_ZERO_PEAK_BASIS_POINTERS.json',OUT/'HALF_ADDENDUM_DISPOSITION.json',OUT/'README.md',OUT/'r4_dense_half_expression_reference.py',OUT/'r4_dense_half_package.py']
manifest={'dependency_recovery_ZIP_sha256':'080352e24adb9db33e76e92d8aca9836aeaf444ed75818c29e2970a32dae47df','files':[{'path':x.name,'bytes':x.stat().st_size,'sha256':sha(x)} for x in files]};mf=OUT/'PACKAGE_HASH_MANIFEST.json';mf.write_text(json.dumps(manifest,indent=2),encoding='utf8');files.append(mf)
archive=OUT.parent/'YURI_O1_R4_DENSE_HALF_EXPRESSION_20261003_R1.zip';assert not archive.exists()
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for x in files:z.write(x,x.name)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for r in manifest['files']:assert hashlib.sha256(z.read(r['path'])).hexdigest()==r['sha256']
h=sha(archive);dest=Path('C:/YuriTransfer/outbox')/f'YURI_O1_R4_DENSE_HALF_EXPRESSION_20261003_R1_{h[:12]}.zip';assert not dest.exists();shutil.copyfile(archive,dest);assert sha(dest)==h;dest.chmod(0o444)
package={'archive':str(dest),'bytes':dest.stat().st_size,'sha256':h,'members':len(files),'CRC_all_member_SHA_verified':True,'dense_NPZ':receipt['dense_file'],'source_SHA256':receipt['source_SHA256'],'source_component_diff':{},'head_all_indices':12928,'head_loose_indices':835,'prior_half_summary_exact_match':True,'OFF_return_geometry_max_m':0,'data_only':True,'next':'PM REVIEW'}
for path in (E/'PACKAGE_RECEIPT.json',OUT/'PACKAGE_RECEIPT.json',dest.with_suffix('.receipt.json')):path.write_text(json.dumps(package,indent=2),encoding='utf8')
print(json.dumps(package,indent=2))
