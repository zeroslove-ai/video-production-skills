# R4 Walk head/hair boundary — 원인 배제 checkpoint

원본 Walk만 연결한 대조군과 기존 animation-only 공급 후보의 **91/92프레임 body63561/head12928/hair10408 정점 좌표가 모두 exact 동일**하다. 추가 head/hair transport Action은 이 두 프레임의 교차 원인에서 배제된다. 신규 교정 후보는 만들지 않았다. 원본 외형·driver를 수정하여 원본 motion의 문제를 숨기지 않는다.

원본 R4 SHA256: a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa. 기존 Walk 후보80e1b5db465fafdd810852e244186bd47cbcc7907c819b810823b7d208fdf408 및 Action-only library6f356c1abe82f30ca713c75a53926c1cfe45e7be00fad63bdea6df7c4dcf0463 byte 보존. 원본78/후보81 Actions 및 geometry/material/texture/ShapeKey/weights/rest/drivers 전체 OFF signature 동일. 원본 source-camera960×920 decodedRGBA changed pixels0/max delta0. 기존08caad7/R2/닫힌 ZIP 보존, 외형 승격·GameRig/mesh/donor/substitution/export·제품 Unity 변경0.

| 검사 | 결과 |
|---|---|
| f91 새로운 비인접 triangle identity | head2/hair2/body–head2; 원본 BODY-only 대조군도 동일 |
| f92 새로운 identity | head30/hair1/body–head0; 대조군도 동일 |
| 원본 대비 nonroot bone basis / ShapeKey values | delta0 / delta0 |
| face/hair root vs rigid target matrix | 최대약5.96e-8; root-domain 운반 결함 입증 실패 |
| head vs 단일 rigid transform | 최대0.542001mm 잔차; 원본 대조군에도 존재 |
| hair vs 단일 rigid transform | 최대0.065167µm 잔차; 교차를 수치오차로 면제하지 않음 |
| 과거 cached neutral vs 실제 source OFF | 최대18.456951µm 차이; cache 동일성 주장 금지, 실제 source OFF를 기준으로 사용 |
| CPU 보호 실행 | 1job/2threads/195.838초/정상 종료0/Job active0 |

실제 material 및 vertex weights/ShapeKey 영향 영역으로 localize했다. head 교차는 ContinuousEyeSkin.L/R 및 brow-support surface에 포함되고, body–head 두 pair는 Neck transition.001과 neck weight 접합부다. hair pair는 Hair_Pearl_PBR/Hair_HeadRoot 영역이다. ShapeKey 지원 영역에 속한다는 사실은 해당 ShapeKey가 변경되었거나 원인이라는 증거가 아니다. 내부/가려진/seam triangles도 포함한 정확한 identity ledger를 private 증거에 보존했다. 침투 깊이·가시성·접촉 힘은 이 검사 범위가 아니다.

추가 transport의 인과는 배제했으나, 원본 head의 비강체 잔차가 modifier/skinning/boundary 중 무엇에서 발생하는지 분리하지 못했다. inverse rigid reference의 교차 수는 좌표변환에 따라 변했고 epsilon0/0.2µm/2µm에서는 동일했다. 따라서 모든 교차를 floating-point noise라고 단정하지 않는다. **CONTACT_HOLD / SOURCE_REFERENCE_ONLY / TierP0** 유지. 기존 Walk의 fixed root, near-floor134.124mm 이동, velocity seam HOLD도 변경하지 않는다.

이미 승인된 Idle 또는 전체97프레임을 다시 렌더하지 않았다. 실패 프레임91/92 분석과 기존 source control 하나, 영향 구간74..97만 두 고정 구도에서 비교했다. 각각24frames/24fps/1초, source-native speed factor1. 두 역할의48 matched image pairs는 decodedRGBA exact 동일이며 네 MP4도 역할 간 동일 SHA. 전체96 PNG 그리드 검토 및 네 영상 전체 decode와 실제 UI1x 끝까지 재생 완료/error null. 눈에 띄는 새로운 face/neck/hair break가 없다는 시각 판정은 strict contact PASS를 대체하지 않는다.

재현 workflow와 raw 좌표/triangle ledger/guard/normal-speed proof는 별도 private supplement ZIP에 들어 있다. 기존 Walk self-contained packet은 재포장하지 않았다. 공개 Git에는 이 scalar 보고서·SHA receipt·script만 관리한다.

다음 유용한 bounded 연구 후보는 기존 native BODY_HeadGazeHair의 source-only continuity 검수다. 이번 checkpoint에서는 실행하지 않았다. Laptop Unity integration/AlwaysAnimate/state/time/weight/F2/F3는 해당 owner의 별도 검사이며 이 결과로 승인하지 않는다.
