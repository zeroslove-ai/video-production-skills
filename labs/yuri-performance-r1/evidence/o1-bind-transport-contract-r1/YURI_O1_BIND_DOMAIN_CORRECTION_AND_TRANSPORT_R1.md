# Bind domain correction / source transport contract R1

실제 frozen Unity case를 독립 NumPy float64 polar/matrix-angle로 재계산했다. 기존10.416765mm를 world 위치 오차로 해석하면 잘못이다. `ff5806f` 원본 진단/checkpoint/packet은 보존하고 이 별도 corrective receipt로 domain을 명시한다.

| 비교 domain | translation-vector 차이 | rotation |
|---|---:|---:|
| original Unity bindpose ↔ source-derived inverse bind | **0.0104167651608 inverse-bind coordinate units** | 0.6757830959° |
| rendererWorld × inverse(Unity bindpose) ↔ source raw-rest world | **1.8645224318e-7 world meters** | **0.6757831574° FAIL** |
| actual current Unity bone world ↔ source raw-rest world | 3.9549636449e-7 world meters | 0.00002900276° |

Translation of an inverse-bind matrix is in its bone/mesh coordinate domain, with scale/orientation already involved. It is not the recovered bone's world-position error. No tolerance changed, no zero-weight waiver. Existing actual bone transform/rest PASS cannot certify the separate renderer inverse-bind row.

The actual renderer matrix matches declared source renderer basis closely (max elements1.40395e-7, rotation0.00000366838°). Source wire bind passes independently; this isolates the observed imported bindpose rotation from source raw-rest or current bone pose. Empty Cluster is a fact, but the importer treatment causing this discrepancy is not yet established from code/data.

## Transport derivation

Keep source raw rest **W_s**, source mesh world **M_s**, source inverse bind **B_s = inverse(W_s) M_s** distinct from evaluated OFF. Let exported mesh local geometry **v_u=K v_s**, target bone world **W_u=G P W_s H_b**, where G is a declared common instance transform. Matching rest geometry requires **M_u K=G P M_s**. Then:

```text
B_u = H_b B_s inverse(K)
K=H and H_b=H  =>  B_u=H B_s H
validated actual renderer frame => B_u=inverse(W_u) M_u
```

`H B_s H` is conditional on verified mesh-local geometry basis K; matching one bone pose does not establish it. Validate each renderer using exact source/import split-vertex correspondence, original topology and actual world matrix. Do not fit per-bone corrections, rewrite rest, reset source helpers, rescale vertices or replace geometry to make the equation pass. Normals/tangents need their separate declared domain transformation.

For this actual head renderer case only, the offline `inverse(sourceExpectedBoneWorld) × actualRendererWorld` proposal produces recovered source raw-rest closure about1.1e-16 matrix elements /1.1e-14°. This is algebraic closure, **not a runtime implementation/deformation PASS**. Its difference from source `H B_s H` is about1.00591e-7 elements, reflecting actual renderer numeric representation.

## All-row source bundle

NPZ provides **7 float64 matrix arrays ×1,207 original binding rows**, exact renderer/modifier/rig/bone identity and original source pointer. Source raw-rest inverse and evaluatedOFF inverse are separate. Expected converted source world matrices and conditional H geometry-basis bind matrices are separate. Stored native inverse matrices are retained unchanged; no reinversion correction is substituted into source.

All21renderers/all137rigbones are covered by original metadata. Body two Armature stages retain distinct modifier identities and do not imply two new Unity skins. The bundle is source-owned data; Laptop remains sole Unity writer. Original source/frame1/ActionNone/5posedbindhelper scales/.535 once semantics stay intact.

On an isolated clone only, consumer must establish original bone identity/order and exact renderer basis before transporting bindposes. Imported immutable mesh/source asset remains unchanged; cloned geometry/materials/ShapeKeys/weights must match before/after. Required proof: **all1,207 source binding rows including zero support** against actual renderer/bindpose matrices, all137rest/pose gates retained, then complete276/384frame fullstack world positions and CORNER normals against frozen source references. Binding algebra alone does not replace DQ/maskedLBS/corrective stack, material/gaze/F2/Player checks.

`R_MIDDLE3_DOMAIN_CORRECTION.json` records actual input hash/full matrices, both domains, unchanged0.001° gate and original rotation FAIL. `EXACT_BIND_TRANSPORT_SOURCE_CONTRACT.json` provides source pointers/array shapes/hash/readback checks. No source/FBX/Blender scene/Unity load or write, no exporter/render/bake. Prior packets/checkpoints remain immutable; current isolated Unity clone/all-row measurements still pending.
