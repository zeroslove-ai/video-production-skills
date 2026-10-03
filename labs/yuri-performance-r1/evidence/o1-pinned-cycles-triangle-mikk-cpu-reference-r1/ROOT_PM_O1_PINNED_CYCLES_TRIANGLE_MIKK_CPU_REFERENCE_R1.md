# ROOT_PM_O1_PINNED_CYCLES_TRIANGLE_MIKK_CPU_REFERENCE_R1

Status: DONE_PINNED_ALGORITHM_REFERENCE. Actual Cycles renderer-buffer proof / runtime PBR: HOLD. Overall all-tangents unit gate: FAIL_ZERO_TANGENTS.

## Preserved authority and native execution

Consumed only four frozen actual evaluated Body inputs from dbc18a1. No Blender job, render, GPU, master save, export or product changes. All 16 input hashes matched before and after execution; GUI Blender PID129152 remains. Existing 08caad7 and correction history are retained.

Unmodified pinned 9e2066aef7ef Cycles types_normal.h + 16 transitive util headers and four Mikk headers are included. Original MikkMeshWrapper and Triangle::compute_normal blocks are extracted unchanged from scene/mesh.cpp into pinned_wrapper.inc. Research Mesh facade supplies native ordered positions, triangles, smooth flags and current corner attributes; it does not emulate renderer allocation or produce an actual renderer buffer. All source provenance and licenses are included in the packet; no third-party source is added to Unity/product repositories.

MSVC cl.exe file version 19.44.35228.0, x64, /std:c++20 /EHsc /O2 /fp:precise /LD. Default pinned x64 SSE support; no TBB or AVX2 definitions. These are explicit standalone harness flags, not asserted identical to installed Blender compile options. 23 pinned upstream files total ~222 KB; no large downloads/installations. Body has no sharp_face attribute, hence default smooth polygons; current custom-normal CORNER route is used. Current UVMap is always supplied.

Each canonical output stores uint32 packed normals, decoded normals, per-triangle-corner tangent/sign, original corner/vertex/polygon/material mapping and smooth flags. Duplicated original corners stay duplicated. No averaging into one original corner. RawNormalWrapper is an explicitly separate float-normal ablation; frozen rest triangles are another ablation.

## Measurements

| Case | Zero canonical tangents | Packing normal max ° | Raw vs packed tangent max ° | Rest vs dynamic tangent max ° on identical triangles | Unmatched triangles | Changed matched corners > .001° |
|---|---:|---:|---:|---:|---:|---:|
| YRA_R4_Startle_Short 1 | 4 | 0.003651 | 0.011584 | 69.700749 | 11 | 52 |
| YRA_R4_Startle_Short 11 | 5 | 0.003615 | 0.006664 | 49.120720 | 25 | 172 |
| YRA_R4_Struggle_Strong_Loop 6 | 8 | 0.003583 | 0.575317 | 86.047508 | 42 | 289 |
| YRA_R4_Struggle_Strong_Loop 44 | 7 | 0.003609 | 0.006514 | 48.338038 | 41 | 287 |

All arrays are finite and signs are exactly ±1. Decoded normal max unit error ≤1.39e-7; nonzero tangent max unit error ≤1.74e-7. These checks do not erase the 24 zero tangents across canonical cases. Full all-tangent unit error is 1.0 and gate FAIL. Zero tangent triangle/corner/vertex/polygon IDs, geometric area and UV area are recorded in the manifest. Cause requires further native-source/degenerate-group inspection; no source edits or replacement vectors were applied. Angular statistics explicitly count undefined zero-vector comparisons rather than claiming 0° matches. Raw vs packed signs are unchanged; matching rest/dynamic triangle signs are unchanged, but different unmatched triangle sets are not comparable.

Large rest/dynamic changes can extend to identical triangles through Mikk grouping/accumulation. Exact per-triangle-corner arrays permit independent investigation; this report does not claim a visual-render equivalence result.

## Failed attempts and reproducibility

compile_attempt01_missing_namespace.log records missing CCL namespace definitions; compile_attempt02.log records an unnecessary map_to_sphere duplicate (already provided by the real math header). compile_attempt03.log records successful build. The pinned algorithms were not modified to fix these harness setup errors.

execution.log records Strong6 strict unit assertion failure before any NPZ output. A second sanity-only call repeated the same assertion before output (console-only). The completed diagnostic execution records finite/nonzero-unit checks separately, saves the original zero tangents and retains FAIL_ZERO_TANGENTS. This is data capture with an explicit quality defect, not a waiver. execution_completed.log records all 12 calls (four cases × canonical/raw/rest). Native calls ~0.07–0.10s each; total data generation elapsed 5.875s. CPU process PID 116972, exited. No original Blender capture was repeated.

Five initial guessed download paths returned HTTP404 (extern/mikktspace/* and intern/cycles/LICENSE); corrected Mikk path intern/mikktspace used. Apache-2.0 license supplied from previously verified pinned-source packet. All upstream downloaded bytes are unchanged and hash pinned.

r4_pinned_cycles_mikk_build.py rebuilds in a fresh directory from download_receipt.json and the saved research facade. r4_pinned_cycles_mikk_cpu_reference.py performs canonical and both ablations against immutable source arrays. Reproduction must use new output directories; frozen outputs must not be overwritten.

## Remaining gates

Actual Cycles Mesh::update_tangents packed/tangent buffer readback has not been captured. Unity actual corner identity/readback, equivalent normal-map PBR and physical Player remain separate acceptance gates. No full 384-frame expansion, precomputed runtime substitution, tolerance waiver or visual promotion follows this algorithm checkpoint. Next: inspect the recorded zero tangent groups and/or obtain native Cycles buffer instrumentation under a bounded review.

32,522,690 bytes of four NPZ algorithm references are frozen with sources/compiler/execution logs and hash/CRC custody. Source master and original reference video are excluded from Git and the algorithm packet.
