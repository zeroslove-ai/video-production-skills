# Four-sample source-domain/operator handoff

Scoped R5 source-data identity and terminal cleanup are accepted by PM; R5 guard remains FAIL and raw artifacts stay immutable at checkpoint1a0b20b. This additive work reads existing arrays/receipts/code only. It runs no Blender, normal-recalculation implementation, render, export, native build/trace, or product writes. Laptop remains implementation owner. Private consumer code was read as two small pinned Git blobs at8bacd64bfb64e327ccbcdfba615cbd05f4c8576d; raw copies stay outside public Git. No source model, geometry coordinates or full weight payload is republished.

| Actual sample | Wrong triangle rows / slot0 | Actual max normal error | CORNERs over unchanged0.001deg gate | Focused ear polygons |
| --- | --- | --- | --- | --- |
| Startle1 | 7 | 0.0923661471deg | 2967 | 62555,63672,63678 |
| Startle11 | 8 | 0.0428837514deg | 9847 | 63361,63450,63483,63678 |
| Strong6 | 7 | 0.0513632515deg | 11404 | 63450,63672,63683 |
| Strong44 | 5 | 0.0324554016deg | 11707 | 63450,63672 |

UV and slots1/2 are exact in the existing actual runtime receipt; actual tangent count0 is not a tangent PASS. These are PM-read actual renderer failures, not newly reproduced Unity measurements. Exact receipt/source-file hashes are in NORMAL_TESS_DOMAIN_CONTRACT_R1.json.

## Indexed failure domain and completeness

All **12 focused PM ear-trace polygon instances** map to original pentagons, spanning seven distinct polygons and33 original control points. The JSON gives each polygon's original corner interval, ordered vertex/edge identities, current source triangles and material slot, plus33 original CSR intervals tied to exact recipe0cd0bdd7. It verifies every published first_mismatches row against its source NPZ after the single declared winding reversal. This maps20 of27 actual wrong rows. It does **not** claim that the seven polygons or33 vertices are an exhaustive normal/tessellation failure population; full actual wrong-row buffers and normal-error CORNER IDs are missing here. PM's focused trace independently reproduced geometry-sensitive initial signs at divergence0; ear continuation/all same-coordinate triangles are not independently proven by that receipt.

Quad-source-input PASS does not test these pentagons. Initial convex/concave signs differ before ear sweep, with reported local coordinate deltas from~19nanometers to~0.926micrometers. No epsilon, forced reference triangles, shortest-diagonal replacement, pruning or tolerance change follows from that sensitivity.

## Earliest stage that existing data can establish

Actual final **SOURCE_LOCAL coordinate inputs already differ before normal and tessellation**, and initial ear signs diverge at trace0. Existing corrected normal receipts for Startle1/11 and Strong6 show same-local CSharp/independent gaps only2.3675e-6/2.7679e-6/4.1508e-6deg, while source errors remain~0.09/0.043/0.051deg. This narrows that measured same-local discrepancy; it does not certify native Blender arithmetic or supply Strong44 same-local proof.

Independent indexing of frozen seven-stage **source** arrays finds:

- Startle11: focused20 points are WORLD f32 bit-identical from source DQ stage0 through stage6. Secondary/corrective stages change25295/25369 vertices elsewhere, so this is a local statement. Final stage6 equals the complete dynamic reference exactly.
- Strong6: focused15 points are likewise bit-identical stage0→6; secondary/corrective change25719/27994 points elsewhere. Final stage6 equals the complete dynamic reference exactly.
- All four samples' four ordinary Smooth factors are exactly0 in frozen raw driver data. For the focused targets, corrective output is inactive: Startle1 factor0; the other samples have target mask53 all0. Startle1's focused neck pentagon includes positive secondary mask52, so do not infer DQ-only for all its points.

The next useful comparison starts at **actual consumer DQ stage0** for Startle11/Strong6 targets, then stage1/2. The source target outputs are already final at stage0 in these two references. This prioritizes DQ pose/bind/order/float-operation provenance; it does not establish the first comparative upstream divergence because matching actual consumer stage arrays are unavailable. Existing R7 native trace targets11189/14918/21485/22227/40817 overlap none of these33 points, and R7 native arithmetic was never captured. Do not cite its synthetic fixtures as evidence for these failures.

FOCUSED_NORMAL_STAGE_SUPPORT_R1.json independently compares the already captured source WORLD CORNER normal arrays at those pentagon loops: Startle11's20 focused CORNERs and Strong6's15 focused CORNERs are also bit-identical stage0→6, with angular stage difference0. These are measured source invariants only. They neither identify the global worst-normal CORNERs nor let a consumer omit original adjacent fan support; point invariance alone would not generally imply normal invariance.

## Before/after operator contract

| Boundary | Required input and output | Actionable missing evidence |
| --- | --- | --- |
| Recipe → DQ0 | Original63561 basis points; exact57 source rest/pose/flags; all304799 ordered CSR including zeros/nondeforming helpers; body and rig matrices separate. Output source-local f32 co. | Consumer stage0 local bits on focused points; actual native pose/deform/DQ branch/intermediate values before claiming identical arithmetic. Preserve every original influence and hemisphere/order. |
| DQ0 → secondary1 | Cached original input for LBS, mask52, previous DQ output; no second deformation of DQ coordinates. | Consumer DiagnosticStageObserver stage0/1 local+rendered arrays. Do not repair bind/rest or fit canonical geometry. |
| Secondary1 → corrective2 → Smooth3–6 | Original ORCO, original edge adjacency/ordered accumulation, raw wxyz driver factors, mask/boundary/cache contract. | Existing source stage arrays are **WORLD f32 only** for Startle11/Strong6. Their inverse world transform cannot reconstruct exact source-local ULPs after rounding. Compare rendered/world outputs with explicit instance/P/sourceWorld; require separately authorized native source-local stage evidence only if finer localization remains necessary. No new source job is authorized here. |
| Final local co → CORNER normal | Original polygons/edge IDs, sharp attrs, signed short2; true Newell normals, ordered smooth fans, fresh fan spaces, integer-averaged short2 decode. Output original CORNER local normals, then inverse-transpose/world/P transport once. | Full max-error CORNER/fan IDs and actual local buffer. Retain normalization/approx-acos/trig rounding and degeneracy rules. Approximate triangle/vertex normals or source-normal substitution are prohibited. |
| Final local co → corner triangles | Original polygon/corner order; native projection/sign/ear sequence; output original CORNER IDs; then material partition and P winding once. | Full27 actual mismatch triples and actual cache/projection/ear branch data. Cached native `Mesh::corner_tris()` can call dirty `corner_tris_calc` or `corner_tris_calc_with_normals(face_normals())`. Current portable Project unconditionally computes Newell; actual source cache branch is missing, so this static term is a review target, not a proven cause. |
| Normal/triangles → Mikk/PBR | Actual renderer normal/tangent4/UV0/winding, packed-normal policy, shader signs/textures. | Source-data identity does not satisfy Cycles buffer/native numeric or rendered fidelity. Tangent count0 and PBR HOLD remain explicit. |

Pinned cached mesh_normals.cc distinguishes `face_normals_true()` from `face_normals()`: for short2 custom CORNER data, the latter can average decoded CORNER normals into FACE values. `corner_normals()` uses true face normals; dirty/with-normals tessellation routing can use the other cache. Also preserve original-edge identity when testing fan closure, not neighbor vertex identity in general. These are exact source-domain contracts; actual native cache/rounding branch capture remains pending.

## Laptop evidence request without new source authoring

Use the already present DiagnosticStageObserver in the pinned O1SourceBodyArmature: it emits copied original-local coordinates and rendered coordinates through `instance.localToWorldMatrix * P * sourceWorld`. For Startle11/Strong6 supply actual saved stage0..6 arrays and instance matrix, with original IDs/float-bit fidelity; compare existing source WORLD stage arrays only after the declared basis/instance mapping. Supply all27 actual wrong triangle rows and all four samples' top normal-error CORNER/fan identities, preferably complete actual normal buffers with their capture hashes. The JSON contains focused33 point IDs/CSR intervals and source NPZ hashes for indexing. Normal fans need all adjacent original faces/edges, not only the pentagon points; this focused list is not a complete normal neighborhood.

No bone/action/source geometry or shader rewrite is proposed. No approximate recalculated normals are generated. Acceptance remains exact original topology/ordered CSR, normal0.001deg and actual renderer/PBR proof. Next bounded task: compare saved actual consumer stage0/1/2 data on the focused points; request exact missing native local arithmetic only after that comparison identifies a specific boundary.
