# R4 원본 쇄골 교차 읽기 전용 검수

C2의 다음 미완료 source defect로 쇄골 교차 1쌍을 선택해 확인했다. **실제 보이는 해당 결함은 미확인, 후보 생성0, strict contact HOLD 유지**다. 팔꿈치 C3나 가중치/rig/외형 수정은 수행하지 않았다.

기존 source81 Action 후보와 immutable R4 source를 그대로 사용했다. 1/289/302/303/337/370/371/385/472의 실제 BODY/HEAD/HAIR geometry SHA는 기존 원본 ledger와 모두 동일하다. source 내부에 이미 있는 교차이며 adapter 첫 차이는 없다. 최초 교차 직전302와303의 clavicle.L/neck/upper_arm.L local pose 변화, 해당6 vertex의 원본 skin weights, 원본 modifier/constraints/rest 근거를 private intake에 보존했다. 여러 관절의 동시 skin deformation이므로 한 관절이나 weight/modifier를 원인으로 단정하지 않는다.

정면/3⁄4의 OFF/ON을 원래 재질 그대로 302/303/337/370에서 같은 카메라로 렌더했다. 자연 화면에서 목·어깨 실루엣의 뚜렷한 파손이나 해당 내부 쌍만의 defect를 분리하지 못했다. 3번째 diagnostic pane은 두 triangle의 투영 위치만 표시하며 visibility/occlusion/depth 증거가 아니다. 스틸 검사이며 새 정상속도 PASS로 세지 않는다. C2 97프레임 전체1x 비교 근거는 기존 checkpoint8ea4766에 남아 있다.

R1은 OFF 스틸 타임라인370을 마지막 복구 검사에서 남겨 snapshot FAIL했다. 실패 입력과 캡처는 보존하고 완료로 세지 않았다. 별도 R2는 원래 프레임을 복구한 뒤 동일 검사를 통과했다.

읽기 전용 R2 job은 CPU2/4GiB/600초/64MiB 및 strict live identity·terminal drain을 유지해 PASS. source81/OFF/signature와 source bytes 복구는 PASS지만 새 neutral PNG의 decoded RGBA 비교는 FAIL/HOLD다. 1,302,700 channels 불일치, 최대221, 평균 절대차2.945735이며 원인을 확정하지 않았다. 이번 capture 실험을 외형 PASS로 승격하지 않는다. 기존 C2 checkpoint의 neutral 픽셀0 증거와 별도로 기록한다. 새 candidate, export, product/Unity/OS/GPU 변경은 없다. TierP0, Unity/F2/StageB 미검증.

다음 방향은 해당 쌍의 원본 가시성과 원인을 증명할 때만 별도 관절 Action 후보를 하나 만드는 것이다. 검증 없이 쇄골을 재가중하거나 팔꿈치를 더 줄이지 않는다. 전체Tour 손목/head/hair HOLD도 유지한다.

Local review: C:\Users\JAEWAN\Documents\Codex\2026-10-02\files-pasted-by-the-user-yuri\outputs\alpha-tour-clavicle-source-intake-r2\REVIEW_CLAVICLE_SOURCE_INTAKE_R1.html

최초302→303의 local 회전 변화는 upper_arm.L 3.191127도이며 clavicle.L/neck은0, 세 관절의 local 위치 변화는0이다. 원본 BODY에는 Armature2개, Corrective Smooth1개, Smooth4개와 기존 joint/shoulder smoothing mask가 있다. 이는 source deformation 경로의 단서이며 특정 modifier/weight의 오류 증명은 아니다. 이 가시성·원인 미확인 및 neutral pixel FAIL을 모두 해결하기 전 후보를 만들지 않는다.
