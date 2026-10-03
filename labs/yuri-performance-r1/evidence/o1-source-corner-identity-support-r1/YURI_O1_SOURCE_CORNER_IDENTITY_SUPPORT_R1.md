# R4 source corner identity support — 2026-10-03

Immutable R4 source remains the visual authority. This checkpoint reads existing frozen data and the exact 3b37 carrier; it performs no Blender load/render/export, source mesh edit, rig/weight/material/ShapeKey/driver change, or product/PM repository write. Existing 08caad7 and all prior checkpoints remain ancestors.

## Result

All 21 FBX meshes retain original control point positions, polygon corner control point IDs, polygon sizes/start offsets and UV corner values exactly. Material assignments resolve to the same named source materials. **Raw material slot numbers are not identical for Body:** source has three slots referencing the same material; FBX connects that material once. This is an existing compatibility serialization limitation, not permission to collapse source slots or promote the FBX as canonical appearance. The native source and animation-only Action lane remain the authority.

Head retains 12,928 original control points, including **835 loose vertices** with no polygon corners. No synthetic corner identity is assigned to loose vertices. Source triangulation is available through the frozen corner-basis NPZ; Unity importer diagonal/corner order remains unverified without actual consumer triangles.

The six ambiguous Unity split vertices correspond to three source pairs. Their source/actual-FBX UV0 values differ clearly:

| Unity split vertex candidates | Source control point → UV0 |
|---|---|
| 12977, 12980 | 11325 → (0.1020408198, 1); 11343 → (0.1224489808, 1) |
| 12926, 12929 | 11631 → (0.4489795864, 1); 11649 → (0.4693877697, 1) |
| 9859, 9865 | 12549 → (0.5217391253, 1); 12567 → (0.5434782505, 1) |

Each control point has two source loops. The machine receipt contains polygon ID, loop ID, corner ordinal, material slot, UV direct index/value, corner normal, tangent/sign, triangle IDs and all 72 source relative ShapeKey deltas. All 71 exported FBX shape channels × six control points = **426 exact delta matches**. Shape deltas do not distinguish these paired points; UV does. Source Basis has no exported shape channel.

**Consumer identity remains unresolved for all six vertices.** The existing Unity inventory contains vertices, bones, bindposes, weights, material references and shape names/frame counts/weights, but no actual UV0, triangles or per-frame shape deltas. A nearest-position pick is not accepted as semantic identity.

## Smallest next consumer capture

Laptop sole writer captures UV0 for split vertex IDs `9859, 9865, 12926, 12929, 12977, 12980` from the actual isolated clone imported from carrier SHA256 `3b37f3570742617b42215e980a70260490ffe92c7480c33a5de5060dd38c90c1`. Record mesh/clone identity, capture commit/blob SHA and UV convention. Those six UV0 rows should distinguish the three pairs without another source extraction. Validate actual touching triangles/submeshes and winding for complete corner correspondence; source loop triangulation alone is insufficient to prove importer corner order. Capture named ShapeKey deltas/normals/tangents only if consumer UV/topology still leaves a tie.

Previous renderer-frame correction remains in force: do not move Body/Hair renderer transforms to satisfy an unskinned geometry equation. This receipt grants no bind/deformation/appearance waiver. Full Unity deformation, shader/gaze/face and AlwaysAnimate gates remain consumer-owned.

## Verification and failure record

Executed plain Python `r4_source_corner_identity_support.py`; all 21 exact geometry/topology/UV assertions passed. FBX material parser initially required ByPolygon; AllSame materials required explicit expansion. The next check exposed the existing Body duplicate-slot compaction; the receipt separately retains raw slot equality and material-name semantics rather than claiming slot preservation. No exporter or source file was changed to repair either condition.

Master rehash remains `a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa`. Existing Blender OFF neutral pixel/geometry preservation and six reaction playback evidence remain in `R4_APPEARANCE_PRESERVE_CORRECTION_R1_KO.md`; they were not rerendered or broadened into Unity PASS here.

Reproduction requires the frozen inputs named/hashes in `SOURCE_CORNER_IDENTITY_RECEIPT.json`, NumPy, the installed standalone FBX parser and read-only Git access to the existing PM inventory blob. The output directory guard prevents overwriting the frozen receipt. `r4_source_reference_packet_freeze.py corners` creates and reads back one small immutable ZIP with per-member hashes and CRC.
