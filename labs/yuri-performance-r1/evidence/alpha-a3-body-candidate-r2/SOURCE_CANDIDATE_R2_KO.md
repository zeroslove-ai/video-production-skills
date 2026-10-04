# A3 R4 appearance-preserved source candidate

실제 Windows capability 구현 증가: 0. DESKTOP source-only 후보이며 TierP=0 / StageB / O1 / PRIMARY / F2-F3 HOLD.

DONE: 원본 R4 SHA `a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa` 유지. 원본 geometry/material/ShapeKeys/weights/rest/driver와 기존 Actions OFF snapshot exact, neutral RGBA difference 0. 신규 Action과 pelvis support-Z cleanup만 추가. Candidate bytes 26872836, SHA `1e16f3529566ed3e4132ca0e3ede86051bab35a89bc23e155c5f82a9cfab9fe8`. 21 original body bones mapped; native fingers/face/gaze/hair preserved. Native guarded inspect/bake/contact/render 모두 PASS.

CLOCK: source scene24 unchanged / Action30 native readback / original BVH30.0003 / frame range [1, 137]. Key interval 4.533333s; video container 4.566667s. A2는 4 native frames마다 pose를 취한 7.5fps 영상, source-time 1x이다. A3/A4 영상은 30fps 전 native frames. 실제 Unity/export는 미실행; consumer는 scene24 대신 Action.source_fps30 적용 필요.

QA: 137 native frames evaluated, root range [0.0, 0.0, 0.0]m, finite mesh. 실제 발바닥 vertex cohort와 near-floor phase proxy를 검사했으며 관절 전체 이동 범위를 sole slide FAIL로 오판하지 않음. 물리 contact/완전한 self-intersection/stance slip 인증은 HOLD. 세 시점 full movie decode와 UI normal1x ended/error-null 관찰 완료. Low sample256x384는 final-quality 판정 자료가 아님.

SEMANTICS: look proxy, NOT authored listen. Face/gaze/finger layer 신규 제작 없음.

FAILED/HOLD: 기존 A1 R1 pelvis channel 및 R2 support float는 수정 후 별도 R3 보존. A2 contact batch의 A3 duplicate preparation은 exclusive path 보호로 중복 실행 전 차단; 개별 A3/A4 native PASS와 구분. 이번 로컬 video metadata script의 HTML quoting syntax를 native 실행 전에 수정. Healthy render 중단/재시작 없음.

CAUSE/FIX: neutral/rest 바꾸지 않고 원본 pelvis Action channels에서 grounded support sole 높이만 보정. 수평 stepping은 강제 고정하지 않음.

NEXT: PM source-subset 리뷰 이후 Laptop 단일 consumer가 clip clock30/AlwaysAnimate/actual bone motion을 독립 검증. authored listen/loop 또는 최종 연기 품질로 승격하지 않음. 새로운 exporter/runtime/product writer 없음.

VISUAL_EVIDENCE: `C:\Users\JAEWAN\Documents\Codex\2026-10-02\files-pasted-by-the-user-yuri\outputs\alpha-a3-contact-candidate-r2` (3 MP4, multiview grid, whole interval samples, OFF PNG); private bundle `C:\Users\JAEWAN\Documents\Codex\2026-10-02\files-pasted-by-the-user-yuri\outputs\YURI_R4_A3_BODY_CANDIDATE_R2_20261004.zip`, 29374129 bytes, SHA `d21b3e91c35f6d145423ad4dacb01153e1d74db34a92d12c1dcc0ad0bc8a8b91`. 공개 Git에는 분석 metadata와 workflow만 기록.
