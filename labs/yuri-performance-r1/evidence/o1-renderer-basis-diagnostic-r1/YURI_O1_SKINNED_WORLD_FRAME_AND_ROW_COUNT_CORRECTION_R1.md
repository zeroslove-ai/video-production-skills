# Source renderer basis / skinned world correction R1

기존 source/FBX와 실제 Unity raw inventory `fd19f8d6` Git blob을 read-only로 조사했다. 신규 Blender/Unity capture/export/render/bake/source writes0회. 143 raw renderer-frame differences를 physical runtime FAIL로 판정하지 않는다.

## Row domains

실제 **1,150 stored bind rows =20renderers×57 + hair10**. source **1,207 modifier binding rows**는 body의 두 번째 Armature57 rows를 추가로 포함한다. 후자는 같은 rig를 쓰는 original masked LBS stage이며 중복 Unity bind storage를 만들지 않는다. source DQ + secondArmature + corrective/surface stack은 모두 별도로 구현/검증해야 한다.

## Geometry / indices

21renderers 모두 frozen original mesh positions와 actual FBX `Vertices` control points가 **exact**, source polygon corner→vertex indices와 FBX polygon index sequence도 **exact**다. 실제 Unity split mesh-local vertices는 선언된 **H (local X reflection)** positions와 최대 약 **3.26e-8m** 차이다. Hair/Body도 raw local geometry H 관계가 맞는다. 이것은 renderer world frame까지 H 관계가 맞다는 뜻이 아니다.

모든 source vertices를 유지하고 Unity split vertices의 nearest/candidate source ID sets를 NPZ에 보존했다. Head6vertices는1e-6 mesh-local query 내 positional ambiguity가 있다. nearest ID를 exact UV/triangle/corner/ShapeKey identity로 주장하지 않는다. actual Unity raw inventory에는 triangles/UV/corner normals/ShapeKey deltas가 없어 이 fields 또는 frozen correct3b37carrier correspondence가 다음 필요 자료다. source↔FBX topology identity는 별도 확정된 증거다.

FBX Model ancestry/properties도 실제 binary에서 읽었다. Hair/Body mesh 및 `Assembly_Root`에 각각 약 -90°X LclRotation이 있고 geometric TRS는 identity다. Body local scale .535는 한 번이다. 이 ancestry는 observed raw renderer frame과 source-declared frame 차이를 설명하는 observable representation evidence이며 source 또는 exporter를 수정하지 않았다. bone binding/skin palette와 해당 raw renderer matrix를 혼용하지 않는다.

## Skinned world policy correction

이전 `9375af8` 계약의 **Mu K=G P Ms**는 **UNSKINNED rest geometry condition**이다. source-equivalent SKINNED binding의 독립 필수 gate로 쓰면 안 된다. Historical receipt/packet은 보존하고 이 corrective checkpoint로 적용 범위를 정정한다. Hair/Body renderer를 그 조건만 맞추려고 이동하지 않는다.

```text
local skinned output = inverse(Mu) sum(Wbone Bu vu weight)
world skinned output = sum(Wbone Bu vu weight)
Mu cancels.

Wbone_u = G P Wbone_s Hb ; vu = K vs
=> source bind transport Bu = Hb Bs inverse(K)
```

따라서 `Mu inverse(bindpose)` raw recovered frame이 source bone world와 다르다는 사실만으로 physical skinning defect를 확정하지 않는다. `inverse(Wsource_expected) Mu`를 algebraically 닫는 것 역시 source-equivalent bind proof가 아니다. verified actual bone/local geometry frames와 exact original bind values를 기준으로 계산한다. shader/object-space/normals/culling semantics는 별도 검증 대상이며 이 식이 모든 Blender modifier나 render fidelity를 증명하지 않는다.

| Actual raw carrier diagnostic | Head | Hair | Body |
|---|---:|---:|---:|
| unskinned Mu geometry vs source world max m | 1.52e-7 | 1.3863 | 1.1646 |
| actual Wbone×B×vertex firstArmature LBS shadow vs source evaluatedOFF LBS world max m | 3.85e-7 | 3.45e-7 | 5.16e-7 |

전체21renderer LBS shadow maximum **5.16089181e-7m**. This is existing raw OFF source-normalized firstArmature LBS diagnostic, not actual BakeMesh or full DQ/GN/corrective result. 원본bone weights8 including tiny values remain, actual imported counts6 remain a separate gate; no epsilon/prune waiver. LBS shadow equality does not certify normals/material/shape data.

Actual Bu vs source H Bs H rotation diagnostic gives **76 rows >0.001°**, all source-positive support0. This is a distinct inverse-bind comparison after positional local-H corroboration, not relabeling the raw143 table. Zero support does not waive all-bind contract. Specific R_Middle3 captured rotation mismatch remains. Exact split-corner identity and isolated clone matrices/Bind/BakeMesh proof are still needed before physical/runtime verdicts or corrections.

## Next consumer fields / gates

Use existing correct3b37carrier source correspondence if frozen and verified; otherwise supply actual Unity triangles, per-split UV/corner-normal/tangent, ShapeKey delta and original FBX control-point/corner mapping. Head6ambiguous sets must resolve or retain ambiguity explicitly. Compare actual1150stored rows with original identity and verified Bu transport while retaining both body modifier passes. Then full276unique/384loop-inclusive frames with actual world BakeMesh positions, source CORNER normals, DQ/maskedLBS/corrective/smooth stages, all original8bone influences and material/gaze/F2/Player gates. No renderer move, bone/rest rewrite, new rig or geometry replacement authorized by this diagnostic.
