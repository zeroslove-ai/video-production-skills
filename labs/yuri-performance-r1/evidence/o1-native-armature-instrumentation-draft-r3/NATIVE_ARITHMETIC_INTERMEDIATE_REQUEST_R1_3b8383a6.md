# Native first-divergence handoff — bounded request

Owner of product changes remains LAPTOP_UNITY. This request is a source-side evidence dependency, not authorization for another product writer, a new rig or another export. Laptop will not launch Blender or replace current assets. No full384/capture rerun is requested.

## Required source evidence

Pinned original recipe/build9e2066aef7ef, Startle sourceframe11 and StruggleStrong sourceframe6. Use the same original body/rest/CSR/armature modifier route and exact saved source poses. Capture actual native arithmetic values at the original first-armature evaluation, not reconstructed from final WORLD output and not Python port interpretations.

For all57 bone slots, record names/order, original rest, native computed inverse rest, evaluated pose, resulting deformation matrix, scale/no-scale branch, pre-normalization matrix columns and quaternion conversion result, resulting real/dual quaternion. Float32 raw bytes/hex or lossless arrays required; identify column/row layout. Preserve helpers and native operation order. Ordinary modifier no-deform-matrices path must be identified separately from full_deform/crazyspace.

For source body vertex IDs **11189,14918,21485,22227,40817**, both frames: original co, ordered CSR groups/weights, mapped bone indices, hemisphere sign at each accumulation, running real/dual sums and total, normalized-by-total sums, quaternion length²/reciprocal, rotation matrix and translation, transformed co, finalize delta/co update, masked LBS blend if applicable, pre-WORLD LOCAL output, exact original object/rig matrices, post-WORLD output. Include a direct untouched source stage0/world sample for crosscheck. Do not drop zero/degenerate/positive small weights or repair quaternions/tangents.

If installed native capture is unavailable, a pinned compiled native primitive harness on these exact inputs is useful but must be labeled **native primitive harness**, not installed modifier output. Record source commit/function/caller, build/compiler/version/flags/FMA/SSE options/backend (inverse Eigen versus standalone), executable/library SHA, input/output SHA and reproducible command. Include inverse/multiply/quaternion/weighted transformation primitives individually so first divergence can be located. Do not claim a reconstructed local stage is native.

Input custody: `pose-input-kernel-provenance.json`, original recipe SHA0cd0bdd70e5a6c0670846dab74e295b0a637a79f1c6d57d503611d5cf50aafe0, native pose SHA03fdaaad90211f411910024b94ea27a6e3d6f0728578513a5c1825d33d1d71a3, QA matrices SHAf9481b723cd59791063c39447ebca7a25c9d23a72c1437a363e67d6c9257bf03. Source pose B is QA only, not a product replacement.

## Exact packet and sample selection

Committed checkpoint **8bacd64bfb64e327ccbcdfba615cbd05f4c8576d** contains `native-intermediate-request-inputs-QA-only.json`: exact A/B matrices, ordered original57 rest and names, original object world matrix, five original co/CSR rows with group-to-bone mappings and original weights. A and B values are diagnostic evidence only. Runtime reads neither this packet nor these pose arrays. Frames are original source frames11/6, not O1S2 capture ordinals.

Sample selection is based on recorded maximum-error IDs, not a new acceptance subset:11189=Startle11 B float-accumulation DQ maximum;14918=Startle11 B masked maximum;21485=Strong6 B DQ/masked maximum;22227=Startle11 A DQ/masked maximum;40817=Strong6 A DQ/masked maximum. Capture all five in both cases to compare fixed inputs. Original63561-point gates and all304799 entries remain unchanged.

## Raw buffer schema and coordinates

Use `native_intermediates.npz` plus `native_intermediates.manifest.json`. Every numerical array below is little-endian float32 `<f4`, no float64 reassignment/rounding, compression is lossless; indices are `<i4`. Record shape/dtype/coordinate frame/operation stage per array, SHA256 of the NPZ and each contiguous uncompressed array byte sequence. Provide endian-preserving float hex for ambiguous zero/nonfinite/sample values. Preserve signed zero. Never use final WORLD inverse to fill a missing LOCAL array.

| Array | Shape | Meaning / consumer counterpart |
|---|---|---|
| rest, inverse_rest, evaluated_pose, deform_matrix | [2,57,4,4] | Original armature coordinates; row-major serialized matrices, explicitly transpose native column-major storage once. Consumer originalRest, Unity inverseRest and poseInput*inverseRest respectively. Native inverse currently **missing**, Unity backend not equivalent by assumption. |
| no_scale_branch | [2,57] int32 | Source mat4_to_dquat branch; consumer DiagnosticScaleBranch. |
| normalized_rotation_columns | [2,57,3,3] | Actual mat4_to_quat input after native column normalization. Consumer intermediate normalization not yet exported as arrays; current trace has norms and input matrix. |
| real_q, dual_q | [2,57,4] | wxyz deformation quaternion, dual wxyz. Consumer float diagnostic quaternion trace supplies real_q; actual native dual/quat results **missing**. Not channel quaternion. |
| vertex_ids, csr_offsets, csr_group, csr_bone, csr_weight | [5], [6], [K], [K], [K] | Original five ordered rows, all entries including helpers/unmapped/mask retained; eligibility indicated separately, no pruning. |
| hemisphere_sign, running_total | [2,K] | Native values after each original contributing entry; noncontributing entries marked eligibility=0, state copied unchanged. Consumer accumulation stages exist but per-entry trace **not yet exported**. |
| running_real_q, running_dual_q | [2,K,4] | Ordered native accumulator state, resets at each sample vertex. |
| normalized_real_q, normalized_dual_q | [2,5,4] | After normalize_dq total-weight reciprocal, not unit-normalized quaternion. |
| quaternion_length_squared, reciprocal_length_squared | [2,5] | mul_v3m3_dq native norm/reciprocal. |
| dq_rotation_matrix, dq_translation | [2,5,3,3], [2,5,3] | Native transform terms before reciprocal length². |
| original_co, transformed_co, finalize_delta, stage00_local, stage01_local | [2,5,3] | Original body mesh-local coordinates. Consumer saved stage0/1 LOCAL outputs exist; true source LOCAL **missing**. Stage1 native caller/mask behavior must be labeled, not assumed matching consumer hybrid. |
| object_world, rig_world, premat, postmat | [2,4,4] | Actual source caller transport matrices. Consumer original sourceWorld and identity preview route known; actual native premat/postmat **missing**. |
| stage00_world, stage01_world | [2,5,3] | Source world coordinates before Unity P=(-x,z,-y). Existing reference WORLD arrays available for crosscheck. |

Native implementation references: math_matrix_c.cc multiply217ff, invert_m4_m4~1150 (Eigen vs standalone distinction), mul_m4_v3 / mul_v3_m4v3 677–695; math_rotation_c.cc mat4_to_quat, mat4_to_dquat2002–2058, add_weighted_dq_dq2091–2128, pivot2130–2171, normalize_dq2173–2196, mul_v3m3_dq2198–2249; armature_deform.cc mixer161–198, finalize caller453, full_deform selector482–490; MOD_armature.cc actual ordinary deform_verts nullopt caller. Pin exact source SHA/function spans in manifest rather than trusting line numbers across versions.

Kernel compiled custody is `float-arithmetic-compile-custody.json`: Unity6000.6.0f1, current loaded module IDd0832add-f7e9-4d43-af3a-b36cec702dd0, DLL/PDB/rsp hashes and immutable copies at `C:/YuriTransfer/outbox/O1_FLOAT_ARITHMETIC_CHECKPOINT_513ad5a8`. Original first-AB compiled binary is explicitly **not frozen**. This checkpoint confirms all8 current default A/B arrays byte-identical, not native compiler equivalence. The exact response file is available on the Laptop at that path; installed native compile/backend metadata is a separate required handoff item.

## Why this is needed

No-scale, float quaternion, float accumulation and same-LOCAL point transport have been isolated. No combination closes the source-reference gap, and arithmetic inputs before inverse/quaternion are not certified native. Maximum-error regressions prevent treating an RMS improvement as a fix. Actual normal .001° and exact ordered triangle gates stay unchanged; native intermediates are needed before further broad arithmetic replacement/promotion.
