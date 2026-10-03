# Source all-bind / seven-plus weights diagnostic R1

이번 source-side 결과는 **FBX exporter weight loss를 배제**하고 R_Middle3의 source/rest/wire evidence를 고정한다. 실제 Unity all-bind 불일치의 단일 원인은 아직 확정할 수 없다. zero-weight row도 gate에 남긴다. source/master/Product Unity를 수정하거나 재-export하지 않았다.

## Exact body weights

원본 `Meshy_Body_NeutralCovered` 63,561 vertices의 raw group rows를 CSR로 모두 보존했다. zero entries와 7개의 procedural masks도 삭제하지 않는다. 각 group의 원래 rig/bone name/index/path/deform identity를 manifest에 매핑했다. bone과 mask를 합쳐 normalize하면 안 된다.

| 원본 count 정의 | 최대 bone influences |
|---|---:|
| weight > 0 (literal) | 8 |
| weight > 1e-20 / 1e-12 / 1e-8 | 7 |
| weight > 1e-6 | 6 |

이 thresholds는 분포 설명이며 prune/tolerance 정책이 아니다. 정확히7개 positive bone weights가 있는 vertices1,467개, 8개151개, 합계1,618개의 **모든 seven-plus raw rows**를 별도 gzip JSON에 보존했다. 최대7번째 weight **9.152620918939647e-7**, 최대8번째 **2.225572503568459e-22**. 따라서 기존 “원본7” 표현은 literal >0 최대값과 구분해야 한다. 작은 값을 삭제하거나 Unity count6을 PASS로 처리하지 않는다.

Frozen `5a04` model FBX의 실제 binary Cluster `Indexes/Weights`를 읽었다. body **172,591 positive bone entries 전부 원본과 정확히 동일**, 누락/값차이/extra positive entries 모두0이다. 신규 importer/exporter 실행이 없다. 기존 Blender-import weight receipt도 numeric bone influence delta0을 보고한다. source7+가 native FBX에 남으므로 consumer의 six-count discrepancy는 raw exporter loss가 아니다. actual Unity split-vertex correspondence와 stored weights를 비교해 consumer count/normalization/threshold 단계를 분리해야 한다.

원본 bone-only sum은 **0.8786206692457199–1.0000000351685363**이다. CSR에 raw float32 weights와 별도 derived float64 bone sum/normalized bone weights를 제공한다. derived 값은 source 수정이나 final DQ substitute가 아니다. [Blender 공식 upstream armature code](https://github.com/blender/blender/blob/main/source/blender/blenkernel/intern/armature_deform.cc)는 bone contribution만 집계하고 LBS/DQ의 합산 결과를 normalize하며 modifier mask를 별도로 적용한다. 이 current code를 installed5.2.1 C++와 bit-identical이라고 주장하지 않는다. 실제 source modifier 설정과 전체276frame source reference가 해당 build 결과의 authority다.

## R_Middle3 / all-bind

21 renderers의 모든 source binding rows **1,207개**를 포함했다. body의 두 Armature modifiers는 별도 rows/settings를 유지하며 imported carrier의 한 skin과 구분한다. rest/evaluatedOFF inverses, recovered Blender bind world error, weight support, wire correspondence를 저장했다. all137 skeleton wire 계약은 기존 receipt 그대로이며 FaceBoard13은 mesh bind rows를 가지지 않는 별도 rig다.

Head `J_Bip_R_Middle3` index42는 positive source vertices0이지만, frozen FBX에 **empty Indexes/Weights Cluster와 Transform/TransformLink가 실제 존재**한다. raw model bind와 animation Pose는 exact 같다. source converted raw-rest wire residual은 **5.960464477539063e-8 matrix elements**다.

| 해당 bone의 비교 domain | position | polar rotation |
|---|---:|---:|
| source raw rest ↔ saved Blender-import recovered bind | 1.5628819493e-7 m | 0.00001860955° |
| source raw rest ↔ source evaluated OFF | 1.8848643662e-7 m | 0.00000140604° |
| PM/consumer 보고 source ↔ Unity head bind row | 0.010416765 m | 0.675783° |

Source OFF frame1/ActionNone 또는 5 helper posed scales와 이 bone의 raw rest 차이로 10.4mm를 설명할 수 없다. source→Blender reconstructed bind residual도 그 크기가 아니다. empty cluster가 consumer importer에서 다른 bind row로 생성/해석되는 가능성과 renderer/export basis 혼용은 **검증할 가설**이며 확인된 원인이라고 주장하지 않는다. 원래 all137 local-rest pair PASS는 renderer별 inverse bind correctness의 대체 증거가 아니다.

기존 consumer의 실제 선언 P/H (원본 보고서 SHA 포함)를 재사용해 이 bone의 **expected Unity raw rest, evaluatedOFF, renderer source-world, inverse-rest-bind matrices**를 `R_MIDDLE3_HEAD_CASE.json`에 제공했다. 실제 Unity head bindpose row / renderer localToWorld / matched bone identity+rest/OFF / scale policy가 없으므로 보고된10.416765mm/.675783deg를 독립 재계산하지 않았다. 이것이 최종 consumer 원인 판정에 필요한 정확한 missing fields다. 새 source extraction이나 rest rewrite 대신 이 case buffer를 비교한다.

## Preservation / next

CPU-light 기존 JSON/gzip/NPZ/FBX binary read only, GUI/source load/save/import/render/bake/export0회. 세 번의 bounded read-only parser 실행으로 초기 진단, bone-only normalization/consumer basis, source modifier identity를 순서대로 보강했다. 모든 frozen input SHA256 unchanged. source component mutation0은 source를 로드/수정하지 않은 작업 범위와 이전 authoritative receipts로 보장하며 이번에 master를 재-evaluate했다고 주장하지 않는다. strict Blender source/import rotation FAIL 유지, zero-row/influence gate waiver 없음.

다음 실제 source-fidelity 작업은 consumer exact R_Middle3 buffers로 domain/basis를 확정하고 raw CSR seven-plus weights와 Unity stored weights를 source correspondence로 대조하는 것이다. DQ+maskedLBS+corrective/smooth stack settings/pointers를 이번 receipt에 포함했으며, 기존 full-body276frames와 evaluated gaze corner references를 재추출하지 않는다. Unity 구현은 Laptop sole writer가 수행한다. source diagnostic/data custody 완료와 runtime all-bind/deformation PASS를 구분한다.
