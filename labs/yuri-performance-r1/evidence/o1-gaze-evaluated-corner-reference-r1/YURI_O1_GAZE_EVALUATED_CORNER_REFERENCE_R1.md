# Source evaluated gaze CORNER authority R1

Neutral + existing four cardinal gaze cases에서 `Character_Body_Head`, `Globe.L/R`의 실제 evaluated Geometry Nodes/modifier output을 측정했다. 원본 R4 source/frame1/OFF body 그대로이며 13 muted bridges를 유지했다. body data job이 끝난 뒤 같은 worker가 순차 CPU phase로 실행했다. 기존 GUI Blender는 건드리지 않았다.

각 source mesh의 original loop index별 **local/world corner normal**과 각 기존 UV의 **local/world tangent, bitangent, handedness sign**를 저장했다. averaged POINT normal과 split CORNER normal을 혼용하지 않는다. 기존 `CORNER_BASIS`는 unevaluated original mesh reference이며 새 evaluated gaze reference를 대신하지 않는다.

전체 5×3 cases의 evaluated vertex/loop count, loop→vertex, polygon loop start/total/material slot, UV를 frozen original topology와 정확히 대조했다. local/world positions는 기존 `080352` frozen case arrays와 정확히 일치했다. source split custom normals와 smooth polygon 정책을 변경하지 않았고 해당 상태/count를 manifest에 기록했다.

Blender Z-up world meters. row-vector position `p A^T+t`, normal `normalize(n inverse(A))`는 column inverse-transpose와 동일하다. tangent은 `t A^T`를 world normal에 정사영해 직교화·정규화한다. bitangent는 `sign cross(normal,tangent)`이며 world sign에는 object determinant parity를 반영한다. float64 계산 후 float32 저장, 원본 UV 기준, Y flip 없음. source loop domains를 유지하며 corner를 vertex 평균으로 축약하지 않는다.

원본 source 전체 component diff=0, input SHA256 모두 유지, 원래 78 Actions 보존, OFF controls와 evaluated world corner normals 복귀=0. export/render/bake/master save/Unity 수정 0회다. 5개 compact NPZ의 per-file SHA256, domains/shapes/controls/position equality는 `GAZE_EVALUATED_CORNER_MANIFEST.json`, outbox independent ZIP 및 manifest custody는 `PACKET_CUSTODY.json`에 있다.

이 자료는 source authority다. 기존 POINT↔CORNER 149° 비교는 서로 다른 domain의 비교이므로 실제 corner FAIL 측정으로 채택하거나 tolerance를 완화하지 않는다. 새 authority와 actual Unity split corner mapping으로 독립 QA가 필요하며 Unity/PBR/F2/Player PASS를 주장하지 않는다.
