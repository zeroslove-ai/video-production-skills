실제 새 Windows capability 증가: 0. 이 checkpoint는 DESKTOP source-only Action 후보와 검증 자료다.

# R4 source appearance / clip clock / reuse contract

Canonical visual authority는 원본 Character_Master_NeckSkin_R4.blend, SHA a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa다. 원본 scene24fps와 기존 four-rig hierarchy/geometry/material/ShapeKeys/weights/rest/face/gaze drivers를 유지한다. 08caad7 GameRig는 historical compatibility experiment이며 canonical character로 승격하지 않는다. 이전 corrective820a237과 Reaction 6개는 재제작 없이 재사용한다.

| Group | Source scene | Body Action clock | Preview | Interpretation |
|---|---:|---:|---:|---|
| Preserved Reaction 6 corrective820a237 | 24fps | 24fps | 24fps | 기존 mapping/receipt 재사용, Unity AlwaysAnimate gate 여전히 required |
| A1 Female_Idle R3 | 24fps | 30fps | 30fps | frames1–301, 10.0s key interval /10.033333s container |
| A2 idle_02 R2 | 24fps | 30fps | 7.5fps | native3608frames 전체 geometry 검사; 영상902poses every4nativeframes, 120.233333s key interval /120.266667s container |
| A3 l_aro_2_32 R2 | 24fps | 30fps | 30fps | 137frames, look proxy이며 authored listen 아님 |
| A4 wei_rl_11 R2 | 24fps | 30fps | 30fps | 252frames, weight shift; authored seamless loop 아님 |

A2–A4 original BVH timebase30.0003fps를 metadata에 별도 보존했다. 사전 converted FBX의 소수 frame endpoints를 정수 native sampling으로 읽어 target Action1부터 재키잉했다. raw BVH timing bit-exact 주장 없음. 원본 donor 파일은 변경하지 않았다. donor rest/world axis에서 target original hierarchy에 rest-aware limb swing, native bone length와 hip-height-normalized pelvis displacement를 적용했다. 단순 bone rotation copy나 Reaction J_Bip mapping 재사용을 하지 않았다. LaFAN22 donor에는 fingers/face/gaze가 없어서 target 원본 해당 채널을 건드리지 않았다.

Consumer는 각 clip clock metadata를 읽어야 한다. scene24만 보고 신규30fps Action을 재생하면 25% 느려진다. 기존 Reaction24를 일괄30으로 바꾸는 것도 금지한다. source BLEND / additive Action / Laptop-owned runtime adapter를 분리하며 이 checkpoint에서 새 exporter/runtime/product 구현은 하지 않는다.

Contact는 original evaluated neutral sole vertex cohort의 minimum-floor와 near-floor2mm phase proxy로 측정한다. foot joint origin 이동 범위는 sole slide와 다른 domain이다. 바닥 근처 장시간 centroid drift는 보류 근거로 기록하되, authored stance label / donor matched timing 없이 자동 slip FAIL 또는 physics PASS를 선언하지 않는다. 새로운 cleanup은 grounded support-Z pelvis Action correction뿐이며 수평 step은 보존했다. 원본 skin/rest/mesh를 고쳐서 발 접촉을 맞추지 않는다.

DATA_PASS는 source subset 원본 보존과 actual native finite-body/byte custody에 한정된다. Blender native PASS나 complete1x media playback이 Unity runtime PASS 또는 visual product PASS를 의미하지 않는다. TierP=0 / StageB / O1 / PRIMARY / F2-F3 HOLD. CPU 저해상도 preview는 최종 연기/손/표정 품질 판정이 아니다. A2 guard output cap 실패는 보존했고 fresh128x192 preview로 우회하며64MiB/600s/4GiB guard를 그대로 유지한다.

다음 bounded 실험 후보: A2 donor와 target의 planted-foot timing correspondence를 좁게 비교해 수평 sole drift의 authored stepping 여부를 먼저 분리한다. PM/consumer gate를 대신하거나 A3를 authored listen으로 relabel하지 않는다.
