# Original R4 CORNER normal / tangent semantics — 2026-10-03

Source-only specification/evidence support; **zero Blender jobs**, evaluations, exports, renders or source/consumer/PM writes. Reused original21 mesh/corner-basis NPZ, evaluated gaze references and two seven-stage Body datasets. Native carrier `3b37…` is distinct from rebuilt GameRig. No tolerance waiver, alternate source appearance or competing runtime implementation.

## Source input pointers

`CORNER_NORMAL_TANGENT_SEMANTIC_RECEIPT.json` inventories all21 mesh input paths/SHA256, exact array keys, domains/types/shapes, original corner-edge relations, polygon sizes, UV layers, triangulation and tangent availability. Arrays are reused from the existing source-fidelity packet, not duplicated.

| Original mesh | Packed custom normal array | CORNER count | Nonzero alpha entries |
|---|---|---:|---:|
| Character_Body_Head | `attribute_19_value` | 66,861 | 1,687 |
| Hair_Replacement_R4 | `attribute_9_value` | 32,994 | 31,578 |
| Meshy_Body_NeutralCovered | `attribute_13_value` | 254,602 | 3,337 |

Source semantic type is **CORNER INT16_2D**, serialized in NPZ as int32 pairs. All values round-trip to signed int16 without loss; canonical packed-payload hashes are in the receipt. Do not interpret these pairs as xyz vectors. These three meshes' explicit sharp_edge arrays are all false; Body/Head sharp_face is absent (default false), Hair's is present/all false. This does not remove fan breaks caused by boundary, nonmanifold topology or winding. Head835 loose vertices remain source vertices with no CORNER data.

Body topology: `loop_vertex_indices`, `polygon_loop_start/total`, `edge_vertex_indices`, `.corner_edge=attribute_12_value`; `uv_0=UVMap`. Head/Hair keys and every other mesh are enumerated in the receipt. All21 corner-edge endpoints were verified exactly against consecutive original polygon corners. Keep original adjacency, not split Unity triangle adjacency.

## Normal algorithm

Pinned build [mesh_normals.cc](https://github.com/blender/blender/blob/9e2066aef7ef/source/blender/blenkernel/intern/mesh_normals.cc): `Mesh::corner_normals` selects `normals_calc_corners` for the original short2 CORNER custom attribute. Current deformed positions and original polygons produce true face normals. Sharp/flat/winding/nonmanifold boundaries partition smooth fans; angle-weighted face normals and current edge directions define each fan's normal space. Original packed pairs are **integer-averaged within the fan**, then decoded using its freshly computed reference axes/angles. Alpha zero or invalid space falls back to the fan normal. Preserve signed encoding, traversal/cyclic ordering, approximate acos and degeneracy rules. Short2 is not the direct float3 custom-attribute branch.

Pinned [mesh_runtime.cc](https://github.com/blender/blender/blob/9e2066aef7ef/source/blender/blenkernel/intern/mesh_runtime.cc) invalidates normal caches when positions change. The seven Body deform-only stages change coordinates; they do not intentionally rewrite packed custom-normal attributes. Reconstruct fan spaces at the desired cumulative stage. Plain LBS of frozen xyz normals, triangle averaging or stale rest normals do not reproduce that contract. The existing stage capture proves actual evaluated CORNER results; packed attribute preservation across stages is specified from the coordinate-only source algorithms, not claimed as a new per-stage attribute capture.

Separate Body CorrectiveSmooth geometric tangent frames (delta restoration) from shading UV tangent frames. Head/eye GN gaze operations require the existing **evaluated** gaze-corner receipt; original static packed data alone does not substitute for those outputs.

## Tangent policy and a real missing reference

Pinned [RNA mesh API](https://github.com/blender/blender/blob/9e2066aef7ef/source/blender/makesrna/intern/rna_mesh_api.cc) routes `Mesh.calc_tangents(UVMap)` to `calc_uv_tangent_tris_quads`. Its input is current local positions, final CORNER normals and per-corner UV. Frozen original/gaze tangents use that route where supported. [mesh_tangent.cc](https://github.com/blender/blender/blob/9e2066aef7ef/source/blender/blenkernel/intern/mesh_tangent.cc) supplies corner tangents/sign to pinned Mikk, with `B=sign*cross(N,T)`.

**Body has 399 pentagons and one heptagon. Its original receipt explicitly records `Tangent space can only be computed for tris/quads` and has no `tangent_uv0`/sign array.** This missing Body tangent reference must not be called PASS. LowerLashes L/R contain24/26 hexagons and have no original UV layer/tangent arrays; they are not listed as a failed UV calculation because that call was not made for them.

The general BKE `calc_uv_tangents` route accepts corner triangulation and reconstructs quads; it is distinct from the RNA reference route. For ngons, use current geometry's native triangulation with original corner/polygon correspondence. Frozen original triangulation is not an all-frame deformed triangulation claim. For quad Mikk processing, the [pinned implementation](https://github.com/blender/blender/blob/9e2066aef7ef/intern/mikktspace/mikktspace.hh) picks the shorter UV diagonal, then geometry on a UV tie, with0–2 as final tie preference. A consumer triangle list may differ. Reusing static tangents after normals/positions change, or flipping UV V without changing handedness, requires separate proof.

World-space transport follows existing receipts: row normal `normalize(n_local inverse(A))`; tangent is transformed by `A^T`, projected perpendicular to the world normal and normalized; world sign gains `sign(det(A))`. Consumer basis K, winding/UV conventions and shader negative-scale handling need explicit verification to avoid applying a mirror sign twice. No Body Mikk computation or PBR shader equivalence is asserted here.

## Actual indexed normal evidence

Frozen `424517b` stage files store world normals per **original CORNER**, and final stage6 exactly equals the prior full-stack reference. Independent float64-normalized `atan2(cross,dot)` comparison of existing arrays gives:

| Corrective stage2 vs stage1 | Max angle | Worst source CORNER / vertex | Corners >0.001° |
|---|---:|---|---:|
| Startle11 | 6.445871885° | 7,278 / 1,980 | 68,663 |
| Strong6 | 108.251917616° | 6,757 / 1,844 | 93,296 |

These are actual source stage changes, **not consumer errors**. A sub-micrometre position PASS does not establish CORNER-normal or tangent/PBR PASS. Compare exact source-loop correspondence; no averaging away large changes or replacing the threshold. Later four Smooth stages have zero position/normal effect in these two cases, as already recorded.

## Consumer evidence / next bounded step

Laptop remains sole implementation writer. For exact normal QA, supply actual clone normal buffers with source control-point/loop identity and source-local/world basis matrices. For tangent/PBR QA additionally supply tangent4, UV0, actual triangles/submesh/winding, importer normal/tangent settings, UV-V-flip and shader sign/normal-texture conventions. If these fields are unavailable, keep the gate pending and route the specific request through Root PM.

Compare current deformed CORNER normals against stage arrays/full-body references first. Original fan topology/short2 semantics and existing corner identity support are sufficient specifications to proceed. Exact Body dynamic Mikk tangent reference is **not present**; any later source evaluation would require a separately authorized bounded probe through the general ngons-capable path. This checkpoint stops at that evidence boundary.

Unmodified official source at build `9e2066aef7ef` is included with URL/hash provenance. BKE/RNA files are GPL-2.0-or-later (Blender COPYING included); pinned Mikk headers/dependencies are Apache-2.0 (license included). Source algorithms are supplied for specification review, not integrated into a competing consumer implementation. `r4_corner_normal_tangent_semantics.py` reproduces the inventory/diagnostics from frozen inputs; `r4_source_reference_packet_freeze.py normals` freezes the small packet and verifies hashes/CRC.
