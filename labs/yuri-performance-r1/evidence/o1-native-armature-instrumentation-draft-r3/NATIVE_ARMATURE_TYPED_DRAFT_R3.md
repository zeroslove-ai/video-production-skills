# Typed native armature draft R3

Actual source patch `native_armature_typed_r3.patch` adds default-OFF `WITH_YURI_ARMATURE_TRACE_R1` CMake switch and typed debug hooks to ordinary MOD_armature `deform_verts`, armature_deform mixers, BKE_pose_bone_done and native math_rotation functions. Copied pinned source apply-check passed. This is prepared source code, not compiled or captured output. Existing V4/V5 resource packets and source blends remain untouched.

The exact Laptop3b8383a6 request is included. Static frozen source slot order has all57 Meshy_Fitted_Rig names, including nondeforming root/helpers. Selection is Startle source11 / Strong source6, body63561, five original vertex IDs11189/14918/21485/22227/40817. Rig/object/modifier name plus actual DEG frame are gated. Actual active Action/recipe verification and arming must be supplied by the future owned invocation adapter; the current debug begin API has no RNA binding. It must arm before dependency graph pose evaluation and disarm before Action switching. No installed ABI probing/GUI hooks.

## Reachable native hooks

| Source site | Actual values copied without replacing arithmetic |
|---|---|
| BKE_pose_bone_done | original bone arm_mat, pose_mat, computed imat immediately after actual invert_m4_m4, chan_mat after actual multiply; slot selected by original name |
| mat4_to_dquat / mat4_to_quat | actual scale/no-scale branch, R and normalized rotation columns, resulting real/dual wxyz; repeated conversion events preserved |
| ordinary modifier nullopt caller | original caller input/output LOCAL and native forward object-world transform; actual object/rig matrices and deformflag; first DQ and second masked LBS separately |
| get_armature_deform_params | actual legacy double-inverse premat/postmat, mask group, full_deform=false; actual operation order unchanged |
| vertex task / mixers | original CSR order including zero/unmapped/helpers/masks; mapped slot and eligibility, running total/quaternion or LBS delta after each entry; mask/cache/early return; normalized-by-total quaternions, native transformed co/finalize delta and local update |
| add_weighted_dq_dq / mul_v3m3_dq | actual flipped branch sign; actual length²/reciprocal, M and t before reciprocal transform; pivot scale path still runs original code |

Noncontributing CSR entries retain the accumulator and total without pruning. Full_deform/editmesh/crazyspace are excluded from the normal path. B-bone/envelope events are indicated; unexpected branches require review, not silent flattening. Ordinary second modifier uses original previous-coordinate mask interpolation, not a replacement hybrid formula.

## Raw schema and limits

Exclusive new case files under `C:/YuriTransfer/native-cycles-readback-r1/capture`; directory/resources are not created by this work. `YRA1` magic/version plus records: eight little-endian uint32 fields (row, modifier, bone, vertex, entry, tag length, float count, reserved), UTF8 tag then raw float32 bits. Context signed indices use int32 interpretation. Matrices transpose column-major storage once into row-major bytes. No decimal formatting, float64 conversion, repairs, inverse-WORLD LOCAL reconstruction or expected-array injection.

Logger caps64MiB/100000records/64float values per event, serializes writes through a mutex, latches failures and requires final flush+close after all worker joins. Worker context is copied by value through deform params; no source pointers survive a hook. Existing files are rejected. Owned build/capture must also use the approved external process resource/timeout supervisor; source logger limits alone are not process guards.

`armature_trace_unpack_r1.py` verifies bounded record format and preserves raw bytes into lossless NPZ event arrays plus each uncompressed array SHA, shape/dtype and context. Signed-zero/subnormal/nonfinite format preservation and truncation rejection passed a synthetic in-memory test. That test is not native evidence. Repeated events remain repeated. This converter intentionally does not fabricate complete canonical Laptop arrays; strict canonical mapper/cardinality validation remains a next source task.

## Explicit gaps and next gates

1. Implement owned Action/recipe/SHA verification plus typed begin/finish invocation binding, force intended pose evaluation, reject incomplete57-slot and five-CSR contexts. No raw pose evaluation has been run here.
2. Canonical Laptop NPZ mapping must select the final quaternion conversion normalization event by actual conversion scope, preserve duplicate diagnostics, convert exact small group/slot diagnostics to int32, derive CSR offsets, and reject absent/ambiguous events. Currently raw-event schema only.
3. Nondeforming helpers run inverse/rest/deform but never native mat4_to_dquat: their quaternion/no-scale fields are NOT_EXECUTED, not zero-filled proof. Ambiguous/non-executed cases require an explicit validity mask/schema agreement before a complete canonical claim.
4. Source math_matrix_c.cc is pinned as backend context. imat capture records actual caller result, not a separately recomputed inverse. Eigen/SSE/compiler/per-TU FP/FMA configuration remains a compiled-build custody requirement.
5. Small source static checks and copied-source apply passed; full typed API/CMake configure/build/link remains pending resources and separate owned build approval. No header-only surrogate compile is claimed.
6. Postcompile guard closure and actual bounded capture acceptance precede runtime evidence. Original63561/all304799 acceptance gates, installed equivalence, Cycles hostcenter, shaded renderer and Unity/PBR remain separate. These armature hooks are not Cycles hostcenter route hooks.

R1 draft apply-check was successful but review found missing explicit DEG query include and CMake switch; its bytes remain preserved. R2 applied successfully but receipt generation failed on a stale R1 patch filename; partial draft remains preserved. R3 repairs these in a separate revision. Earlier generator attempts also stopped on exact-anchor guards rather than altering runtime source. No Blender process was launched or attached and no GPU/large resources used.
