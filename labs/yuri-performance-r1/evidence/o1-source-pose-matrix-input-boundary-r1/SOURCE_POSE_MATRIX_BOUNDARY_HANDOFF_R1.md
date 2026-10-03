# Original input boundary: channel reconstruction versus matrix operator

2026-10-03 KST. File-only source authority review following frozen ea015db. No Blender/native build/acquisition/replay/product edit or duplicate packet transfer. PM verified Laptop's actual inbox ZIP54354923bytes SHA41798f214f1b5a67c78765c42e9d82d3763157e85da0dca9c81964db10cdbedf/CRC11members and both original native NPZ SHAs. The receiver41802754 packet is not sent again. Delivery custody evidence is pinned in the JSON analysis; the earlier handoff's “receiver unconfirmed” records its earlier observation, not current state.

PM now reports actual direct LOCAL stage0 differences versus consumer39: full-body max~1.311979e-6/1.899182e-6 source-local units, focused~0.439367e-6/0.926304e-6. Rest is f32 exact; pose maximum component differences~2.115934e-6/1.956017e-6 occur at R3_Shoulder_L_Bind; sign-aligned quaternion components differ~5.5e-7; bodyWorld differs~2.622604e-8; actual consumer rigWorld was not separately recorded. These current metrics are PM-reported, **not recomputed on Desktop here**. Older PM WORLD/pose A/B receipts are provenance/history, not substitutes for current exact LOCAL comparisons. Cause is not isolated and no DQ blame follows.

## Source evaluation dependency boundaries

Exact original Action+OBMeshy_Fitted_Rig slot and direct source frame11 or6 at24fps → original animated pose channels → Blender parent/inheritance/constraints evaluation → evaluated rig-local pose matrix P. R4 existing hierarchy/flags/rest/helper bones are preserved. This is not simple quaternion-to-rotation plus rest copy. Existing metadata identifies original parents/rest/rig settings; do not invent missing channels or bypass constraints as an unlabelled “equivalent” reconstruction.

The driver branch separately reads original SINGLE_PROP quaternion wxyz components → original five body modifier factors. Native raw components, normalized orientation quaternions and sign-aligned diagnostic quaternions are distinct inputs. Sign alignment can help compare rotation equivalence; it does not authorize sign changes or renormalization of components feeding drivers. Primary stage0 precedes secondary/corrective/smooth effects; hold the factors separately when testing stage2.

Pinned cached native `armature_update.cc:BKE_pose_bone_done` explicitly computes:

1. `float imat[4][4] = inverse(bone.arm_mat)`.
2. `pchan.chan_mat = pchan.pose_mat * imat`.
3. Native deform DQ is built from rest and chan_mat only for bones without BONE_NO_DEFORM.

Do not fabricate helper-bone DQs. A nondeforming helper can still affect descendants' evaluated poses through the original hierarchy. Rest identity alone does not establish inverse-rest/operator identity, and evaluated pose differs from its deformation matrix. R2 captured direct rest and pose, **not** native inverse-rest/chan_mat/DQ intermediate arithmetic. The R7 draft adds trace points but was not run; it supplies no measured numeric intermediates.

Pinned cached `armature_deform.cc` active `#else` route computes armature_to_target=`body.world_to_object * rig.object_to_world`, then target_to_armature=`inverse(armature_to_target)`. The alternative direct `rig.world_to_object * body.object_to_world` route is disabled under `#if0`; source comment explicitly retains the old double-inverse because equivalent formulas caused small numeric test differences. Retain separate body/rig inputs and exact arithmetic ordering. This source review is not actual capture of internal cached inverse-object matrices. Native internal cache/operator branch remains unknown.

Coordinate equations above describe column-vector transforms. NPZ/Python matrices are serialized mathematical row/column arrays; flatten C-order and map once to consumer m[row,column]. Blender C internal storage conventions do not justify a second transpose of saved Python matrices. No P reflection/runtime instance transform is applied to direct source-local arrays.

## Existing authoritative data and independent observations

| Existing data | Boundary isolated / limits |
| --- | --- |
| raw_quaternion_wxyz_f32[57,4] | Direct original pose channel values at exact activation/frame. Verified bit-identical to matching previous276-frame raw dataset in original57-slot order. Raw quaternion alone is not a complete LRS/constraints/inheritance record. |
| driver_factors_f32[5] | Original driver output factors. Verified bit-identical to previous dataset; hold separately to avoid channel-driver confounds. |
| pose_rig_local_f64[57,4,4] | Direct original evaluated pose P in rig space, bypasses world recovery/TRS decomposition. Each saved value is an exact float32 value widened to float64, independently verified. Direct JSON pose_local equals NPZ bits. |
| rest_local_f64[57,4,4] | Direct source rest matrix_local, exact original full recipe f32 bits. Keep original slot order and helper flags; do not rewrite rest. |
| body_world_f64 / rig_world_f64 | Separate direct native matrices; both are widened f32 values. Native rigWorld is already provided, even though current consumer receipt lacks its separately recorded counterpart. |
| all-rig JSON pose_world | Blender computed mathutils `rigWorld @ pose` before storing numbers. This world result is rounded separately and cannot replace direct P. |
| stage_00_local_position[63561,3] | Actual native cumulative-copy primary output, source-local raw f32. Direct consumer LOCAL comparisons avoid P/world transport confounds. The other6 stages and CORNER normals are already delivered. |
| full recipe0cd0bdd7 + original source metadata | Original63561 points/57 slots/304799 ordered CSR including37310zeros/groups58/mask52, original flags/rest. Never prune, renormalize, substitute bind geometry, or make helpers deform. |

Independent Desktop numeric control uses **NumPy float64** inverse(native rigWorld) × native already-rounded poseWorld, then casts f32. Startle11 differs from direct P in60 f32 components, maxcomponent5.5394719034e-8; Strong6 differs in84, max5.5269079313e-8. This proves that recovery path is not byte-equivalent to direct native pose for these files. It is not native matrix code, not a current consumer replay, and does not explain or subtract the reported consumer pose error. Direct matrix source arrays avoid this unnecessary recovery.

## Bounded consumer comparisons using existing source arrays

1. Freeze actual current consumer time/Action-equivalent slot/channel order, raw quaternion components and both separate object matrices alongside LOCAL stage0/1/2. Compare source input rawbit hashes first. Do not mix prior39 buffers with later source/PE snapshots without custody. Native source channels and matrices already exist; no new Desktop capture is requested.
2. Keep geometry/ordered CSR/rest/flags/bodyWorld/rigWorld fixed. Replay exact native raw quaternion channels through the same consumer hierarchy/constraint/inheritance reconstruction, changing only channel input. Difference from direct native P localizes the reconstruction boundary only if other LRS/hierarchy semantics are proved equivalent. Do not assume quaternion equality proves pose equality.
3. Separately bypass that reconstruction with direct source P in a transient diagnostic; hold all other inputs identical. Compare LOCAL stage0. Improvement quantifies pose-input contribution under those controls; residual is not automatically DQ arithmetic error. This is diagnostic authority, not production pose-table substitution.
4. Hold direct P/rest/weights while replacing actual bodyWorld and rigWorld independently, then together, with direct source arrays. Consumer rigWorld must be separately identified first. Never infer it from bodyWorld or recover it from poseWorld. Maintain source double-inverse route ordering for premat/postmat.
5. Only after exact original input identity is demonstrated inspect inverse-rest/deform/premat/postmat/DQ arithmetic. R2 does not store those internal native intermediates. A demonstrated specific missing datum may justify a later narrowly reviewed capture; no new Blender/build/acquisition is authorized by this analysis.

The companion LAPTOP_EXISTING_INPUT_AB_CONTRACT_R1.json provides these input domains/controls. SOURCE_POSE_MATRIX_BOUNDARY_ANALYSIS_R1.json records actual source reproducibility, hashes, matrix-recovery control and explicit limits. Full numeric pose/channel/geometry data remains in already-delivered private custody; this public checkpoint contains only identities/counts/derived diagnostics. R5/R1 failures and R2 fallback are preserved; native renderer/PBR/PRIMARY promotion remain HOLD.
