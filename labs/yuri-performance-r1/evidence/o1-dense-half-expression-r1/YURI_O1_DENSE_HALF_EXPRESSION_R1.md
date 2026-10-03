# R4 dense existing direct morph HALF reference R1 — 2026-10-03 KST

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
