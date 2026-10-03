# Actual source-local capture R2: Laptop data domain

2026-10-03 KST. One approved CPU source read, original Blender5.2.1LTS build9e2066aef7ef, owned PID48516/creation FILETIME134355112332756338. Independent source-data validation and actual owned-Job exit0/Active0/PIDs[] are scoped PASS. This does not rewrite R1/R5 FAIL, certify Unity/Cycles/PBR fidelity, or identify the first comparative divergence. No further Blender execution is needed for this pair.

## Exact custody and source activation

Source master SHAa30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa; unchanged Action library SHA6874ec69d5721f385d31edaa06ef0d58c89a543b98bacd961f8f575ff57eef4d; original full CSR recipe SHA0cd0bdd70e5a6c0670846dab74e295b0a637a79f1c6d57d503611d5cf50aafe0. These private source files are not duplicated into the transfer packet or public Git.

| NPZ | Original frame / time | Bytes | SHA256 |
| --- | --- | --- | --- |
| YRA_R4_Startle_Short_frame011_native_local_seven_stages.npz | 11 /10÷24s | 26474118 | 78ffc7c9f0522c596e8ae0a4ddbda01e1aa75bba069e3dcbd7535e1a3d989dd8 |
| YRA_R4_Struggle_Strong_Loop_frame006_native_local_seven_stages.npz | 6 /5÷24s | 26470968 | 5a5425c0703b386f7fa1e70641e89ce15dbfb53209801de3e65e56d959a3283d |

Unmodified ReactionLane appends the existing exact Action, binds OBMeshy_Fitted_Rig, evaluates `scene.frame_set(frame)` directly at24fps, then restores original Action/slot/channel/frame bindings. This capture has exactly two frames, not full clip playback or loop QA. Native data directory is private `outputs/o1-exact-source-local-stage-capture-r2`.

## NPZ domain and stages

Each NPZ has46 arrays, SHA/shape/dtype recorded in the independent validation and raw data manifest. Load with `numpy.load(..., allow_pickle=False)` and retain float32 raw bits; do not normalize/reorder/prune.

| Array key | Domain / meaning |
| --- | --- |
| stage_00..06_local_position | float32[63561,3], original body control-point row ID; native evaluated mesh.vertices.co in original body object local coordinates, before world transform |
| stage_00..06_local_corner_normal | float32[254602,3], original polygon CORNER/loop row ID; native evaluated mesh.corner_normals.vector, not point normals or triangle averages |
| stage_00..06_world_position | Separately derived float32[63561,3]: native local converted to float64, applied evaluated bodyWorld linear/translation, rounded float32 |
| stage_00..06_world_corner_normal | Separately derived float32[254602,3]: native local normal transported by inverse transpose using bodyWorld float64, normalized, rounded float32 |
| stage_00..06_evaluated_body_world | float64[4,4], actual evaluated object's matrix values. Column-vector equation world=M·local; saved array row-transform implementation local@M[:3,:3].T+M[:3,3] |
| original_corner_vertex / original_corner_edge | int32[254602], CORNER→original vertex/edge IDs. Normal fans need complete original adjacency, not just focused polygon neighbors |
| original_polygon_start / total / material | int32[63781], original polygon→CORNER intervals and original material slots |
| rest_local_f64 / pose_rig_local_f64 | float64[57,4,4], original rig.data.bones / pose.bones order; rest matrix_local and evaluated pose matrix in rig space |
| raw_quaternion_wxyz_f32 | float32[57,4], original pose channels, wxyz, no world/local decomposition or extra normalization |
| body_world_f64 / rig_world_f64 | Actual separate body/rig matrices, never conflated |
| driver_factors_f32 | float32[5], original CorrectiveSmooth then four Smooth factors in modifier order |

Bone names in CAPTURE_RESULT_R1.json define the original57-slot order, including nondeforming helpers; do not translate to runtime55 or remove zeros. Full ordered CSR304799 entries/37310zero entries and mask52/groups58 were checked live against the exact owned recipe. Full scene hash identity covers original skin weights/rest/geometry/ShapeKeys/materials/textures/nodes/drivers and78 Actions. All-rig private pose/rest JSON records137 bones across the source rigs with independent file/content fingerprints.

Stages: **0 primary Armature,1 secondary Armature,2 CorrectiveSmooth,3–6 four original Smooth modifiers**. Each uses a disposable body object copy sharing immutable original mesh data; later modifiers alone are disabled on the copy. Original stack settings/factors/weights/drivers remain. These are **cumulative ablation evaluations**, not internally instrumented in-flight modifier buffers. Getter can recompute normal caches. Native operator/cache branch remains **UNKNOWN_NOT_READ**.

No Unity P reflection, runtime instance matrix, material partition or triangle winding conversion has been applied to the local arrays. Compare actual consumer SOURCE_LOCAL original63561/254602 buffers directly in this domain first. For consumer rendered/world output, explicitly preserve `instance.localToWorldMatrix * P * sourceWorld`; do not apply P/world twice. CORNER transport requires inverse transpose, not position matrix multiplication. Rounded WORLD arrays cannot reconstruct these native local bits.

## Independent checks and focused comparison

Both final stage6 local/world positions and CORNER normals equal their frozen native final reference **bit-for-bit**. All14 saved WORLD stage arrays per frame equal the earlier seven-stage source WORLD data. Independent transform recomputation matches separately saved WORLD bits. Scene before/after hashes are equal with differences{}, and source/Action/recipe/dependency SHA are unchanged.

Focused original polygon/CORNER IDs derive from the frozen NORMAL_TESS_DOMAIN_CONTRACT_R1 SHA0e6e0e6693639e93fafe0647ff104dbd44b3ad11e5ca49ded671997b1fae9552. Startle11 has20 focused points/CORNERs; Strong6 has15. Their native **LOCAL** position and CORNER-normal bits are unchanged stage0→6 as independently measured. This strengthens the source-side invariant previously known only in rounded WORLD arrays. It does not show a consumer discrepancy occurs at stage0 without the consumer arrays. Keep adjacent fan support and complete original weights; the focused IDs are not an exhaustive failure population.

Next comparison: saved actual consumer stage0 local buffers on these original IDs, then stage1/2, with full per-array custody and exact activation/bone/instance mapping. No new source job or relaxed0.001deg normal threshold is needed. No approximate normals, forced source triangles, rest rewrite or epsilon patch is proposed.

## Actual addon and terminal evidence

R2 before/after preferences and loaded-enabled names match exactly: **bl_pkg, cycles, io_anim_bvh, io_curve_svg, io_mesh_uv_layout, io_scene_fbx, io_scene_gltf2, pose_library**. Each resolves to pinned installed entry/spec origin SHA.315 installed Python files were checked. This is actual R2 evidence, not retrospective identification of R1's failed inventory or packet-level network proof. No addon preferences were edited or modules manually enabled/disabled.

Whole R2 guard separately records owned exit0, total1/limit-terminated0, Active0/PIDs[] before close, signaled handle after close and no cleanup errors. Native active1/affinity3/8GiB limits read back. Source collector22.808s; owned guard25.216s. GUI PID129152 and PRODUCT_EXCLUSIVE lease were only observed and untouched. No render/export/save/GPU/acquisition/build occurred.

Raw NPZ/all-rig matrices stay private. Public research Git contains numeric-array hashes/shapes/domain metadata and source/Job/scene/origin receipts only. Private ZIP member SHA and CRC are verified; transfer/outbox custody points to the exact packet. Receiver must verify byte custody before comparison. PM independently accepted source data and terminal scope; first cause/native renderer/PBR/PRIMARY remain pending.
