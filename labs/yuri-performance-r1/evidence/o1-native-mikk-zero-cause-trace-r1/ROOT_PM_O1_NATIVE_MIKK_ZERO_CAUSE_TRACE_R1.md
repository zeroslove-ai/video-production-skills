# ROOT_PM_O1_NATIVE_MIKK_ZERO_CAUSE_TRACE_R1

DONE_DIAGNOSTIC_NATIVE_ALGORITHM_TRACE. R4 authority and prior reference/DLL/outputs unchanged. Unit tangent FAIL, actual Cycles renderer buffer/PBR HOLD, original CORNER normal 0.001° gate unchanged. No Blender/GPU/render/Unity/source-save job.

## Observed first zero

All canonical 24 corners were traced through a separate copied native Mikk header with read-only hooks. Original arithmetic remains intact; instrumentation.diff records inserted observations. The normal angle observer evaluates the same pinned fast_acosf expression separately; the original computed contribution itself is recorded. Native decoded normals match the source-linked baseline exactly.

| Case | Targets/groups | Contributions per group | Float32 fCos range | Cause |
|---|---:|---:|---|---|
| Strong 6 | 8 | 1 | 1–1.00000012 | angle0 → contribution0 |
| Startle 1 | 4 | 1 | 1 | angle0 → contribution0 |
| Startle 11 | 5 | 1 | 1–1.00000012 | angle0 → contribution0 |
| Strong 44 | 7 | 1 | 1–1.00000012 | angle0 → contribution0 |

Source triangle tangent and its projection into decoded corner normal's plane are nonzero (projected tangent length ≈1); target triangles are not markDegenerate and not groupWithAny. fCos is the original float32 dot product of projected normalized edges. It reaches 1 or the next float above1 (1.0000001192092896), clamp yields1, fast_acosf returns0. The original contribution multiplication produces (0,0,0). Each distinct group receives just this one zero contribution, so sum_before/sum_after/pre_normalize/post_normalize all remain zero. No nonzero contribution cancellation, projected-tangent zero, or normalization underflow is observed. The first zero contribution is the angular-weight multiplication, not final normalization.

The prior source geometry/UV areas are finite nonzero; tiny triangles can have edge projections whose float32 angle collapses to0. That explains this pinned CPU execution, not an assertion of identical installed Cycles compiler/parallel/render behavior. No geometry, tangent or normal was replaced or discarded.

## Equivalence and evidence

Four completed diagnostic outputs each contain381,120 triangle corners. packed uint32 normal, decoded normal, tangent and sign arrays are bitwise equal to the uninstrumented frozen canonical reference in all four cases. Per-case JSONL logs record triangle init, target group assignment, every target-group contribution and sum, pre/post normalization. Source-linked JSON records original corner/vertex/polygon/material IDs, packed uint32 and raw/decode normal, dynamic triangles and complete target details. All original reference-directory60 file hashes and16 provenance-input hashes were verified before/after; four input NPZ post hashes separately verified. Original source/master/library/rest/rig/material data untouched. Existing GUI PID129152 preserved.

MSVC cl file version19.44.35228.0; same /std:c++20 /EHsc /O2 /fp:precise /LD x64 serial Mikk flags as original harness. Separate diagnostic DLL and exact diff/hooks/compile log included. Existing original DLL never overwritten. Instrumented Mikk header explicitly marked modified; all other copied pinned sources unchanged. Apache-2.0 and GPL-2.0-or-later licenses included; GPL platform build reference is for research only, not copied to Unity.

## Failures honestly retained

First native attempt failed with access violation because temporary NPZ arrays' pointer addresses outlived Python array storage. Fix: retain position, normal and UV arrays as variables. Empty/failed trace is failure evidence only.

Second attempt completed Strong6 native arrays and trace, then JSON serialization failed on a NumPy int64 count. Cast count to Python int and resumed saved data without a second successful Strong6 call. A metadata-only resume then hit an undefined corners binding; moved bindings outside branch. Final resume recovered Strong6 metadata and ran the other three cases. There were four completed canonical calls total; one earlier failed call provides no algorithm evidence. All three failure logs and final execution log remain in packet. Final resume PID124848, elapsed2.1866912s; this duration excludes previous attempts and is not total task time.

Saved setup accepts a fresh diagnostic directory and copies the frozen source/DLL harness inputs before applying hooks. Saved trace accepts that directory; existing frozen final manifests block rerun. No full384-frame expansion.

See ACTUAL_CYCLES_BUFFER_MINIMUM_PATH_R1.md for the next actual native-buffer acquisition path, resources, side effects and strict output scope. No additional Blender/build/render job is scheduled by this checkpoint.
