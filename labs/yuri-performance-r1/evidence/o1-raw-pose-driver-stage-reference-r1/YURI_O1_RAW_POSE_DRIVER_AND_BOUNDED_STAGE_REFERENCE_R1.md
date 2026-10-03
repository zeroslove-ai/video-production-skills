# R4 raw pose driver and bounded stage reference — 2026-10-03

Completed exactly one CPU background source probe from immutable R4 + existing Action library. No source save/export/render/bake, existing GUI shutdown, product change, rig/rest/skin/material/ShapeKey/driver rewrite or new motion authoring. Native original-bind carrier `3b37…` remains distinct from the earlier rebuilt GameRig. This source reference supports the current source-equivalent adapter; it does not promote carrier visual equivalence or reset that adapter.

## Capture and custody

- Original 57 Meshy_Fitted_Rig bone names/order and raw `rotation_quaternion[0..3]` **wxyz** captured at all **276 unique authored frames** across existing six reactions. No extra normalization, matrix decomposition or Unity local-quaternion substitution.
- Actual five original modifier `.factor` outputs captured at every frame; path, complete original driver definitions/targets/mute/FCurve metadata and Action/slot/timing retained in the manifest.
- 384 loop-inclusive sample semantics retained; 108 repeated second-cycle samples actually reevaluated and raw quaternions/factors checked bit-for-bit, without duplicating geometry for all clips.
- Independent plain-Python verification evaluated the original arithmetic expressions using frozen raw quaternion targets: all **276 × 5 = 1,380 factor outputs match exactly as float32**. Restricted AST permits numeric arithmetic/min/max only.
- Original all137 world pose matrices match the previous frozen source reference at every unique frame, maximum element delta **0**. This is a provenance check separate from the new raw pose channels.
- Only **Startle11 and Strong6** have cumulative seven-stage geometry references. Each stage stores 63,561 original-index world positions and 254,602 original **CORNER** world normals, unaveraged. Original polygon order, material indices and UV match before capture. Intermediate normals are native recomputation after that ablation.
- Both final stage6 outputs match existing full-stack reference **bit-for-bit** for local/world positions and local/world corner normals. No alternate authority was created.
- OFF restored after each clip; raw bone channels and factors equal initial OFF. Original78 Actions and full appearance/hierarchy/rest/driver fingerprint preserved: source component diff `{}`. Before/after hashes of master, Action library and all other frozen inputs remain identical.

Master SHA256: `a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa`.

Action library SHA256: `6874ec69d5721f385d31edaa06ef0d58c89a543b98bacd961f8f575ff57eef4d`.

## Exact problem frames

| Clip/frame | Actual Corrective factor | stage1 − DQ max | stage2 − stage1 max | Corrective worst source vertex |
|---|---:|---:|---:|---:|
| Startle11 | 0.019812777638435364 | 0.785762421mm | 0.259765903mm | 1889 |
| Strong6 | 0.3373560309410095 | 1.677910627mm | 1.772832604mm | 1981 |

Stage0=original DQ; stage1=original DQ + masked multi-Armature LBS; stage2=original CorrectiveSmooth; stages3/4=shoulder L/R; stages5/6=hip L/R. At both problem frames all four shoulder/hip factors are **0**, and their incremental position/normal differences are **0**.

CorrectiveSmooth changes actual CORNER normals as well: maximum world-normal vector difference stage2 vs stage1 is 0.112442367 at Startle11 and 1.620614409 at Strong6. These are **vector distances, not degrees**. Tiny positional correction does not authorize keeping stage1 normals or comparing averaged vertex normals instead. The indexed native corner references remain the consumer target.

The Strong6 corrective positional effect matches the scale of PM's reported ≈1.77mm remaining prototype residual. This is direct source-stage evidence of a missing contribution, **not proof** that the consumer prototype already equals source stage1 at every vertex/bind row. Laptop should first compare its DQ+secondary output against this exact stage1 array, then implement/compare stage2 at the actual factor above. If stage1 differs, fix that earlier difference before assigning all residual to CorrectiveSmooth. Stage differences are cumulative/nonlinear; do not add frozen offsets as a general animation correction.

## Runtime input contract

Use the per-clip arrays `[source_frame-1, original_bone_index, wxyz_component]` and `[source_frame-1, modifier_index 2..6]`. Sample authored `(frame-1)/24` seconds; loop mapping is explicit in `clips[].samples`. Preserve raw original quaternion channel semantics independent of evaluated bone matrices. For the benchmark, provided source factors can isolate the geometry algorithm from channel conversion; a reusable runtime adapter must subsequently prove its own source-channel reconstruction.

Original masks/order/ORCO/corner topology/bind parameters remain in the `6e71474` modifier contract. No all-frame full geometry recapture was performed; use the previous 18-volume full-body reference for final deformation QA. These two stage datasets expose exactly the former Strong6/Startle11 stage evidence gap. They do not grant a Unity deformation/shader/face/gaze/AlwaysAnimate PASS.

## Execution and resource evidence

Command: Blender 5.2.1 LTS build `9e2066aef7ef`, `--background --factory-startup --threads 4 --python r4_raw_pose_driver_stage_reference.py`. One job, PID85780, 39.3287 seconds. Preflight Windows free physical memory 31,311,632KiB; in-flight 31,134,072KiB; after 31,976,660KiB. Observed job PeakWorkingSet64 1,405,853,696bytes at process snapshot; this is not a continuous peak profiler. Existing GUI PID129152 remained open. GPU PRODUCT_EXCLUSIVE was preserved; no render/inference/GPU task launched.

Three versioned NPZ total **25,635,120bytes**. All arrays read back exactly/finite; normals have unit-length error below 1e-6; all frozen input hashes independently rechecked. Run `r4_raw_pose_driver_stage_verify.py` for independent numerical verification (guard rejects overwriting an existing receipt). Run `r4_source_reference_packet_freeze.py rawpose` for one independently readable ZIP below100MiB, with member SHA256 and CRC verification. Scripts, adapter/fingerprint dependencies and JSON receipts are included; immutable master/Action inputs are referenced by exact hash, not redistributed or modified.

Next bounded task: Laptop compares exact source stage1 then stage2 for both problem frames using original source indices/corner correspondence. Retain all other consumer gates and source fidelity requirements.
