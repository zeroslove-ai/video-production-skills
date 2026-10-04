USER_CAN_NOW_SEE_OR_DO: 첫 실패 frame8의 기존/관절제약 pose를 정면·3/4·측면에서 비교할 수 있다. 판정 FAIL_HOLD_CONSTRAINT_RESIDUALS_OR_NEW_SURFACE_CROSSINGS; 전체 Sit/Stand/물리 접촉 승격 없음.

# R4 Sit/Stand frame8 원본 rig 관절 제약 discriminator

원본 mesh/재질/weights/modifiers/rest/bind/rig hierarchy 및78 Actions를 보존했다. 이전 실패후보8bc13115 및 packet1103147f는 그대로 남겼다. 새 rig/geometry/바인딩/충돌기/런타임을 만들지 않고 원본 R4의 추가 Action3개만 만들었다. Upper local pose reference는 이전 frame8 값으로 고정; pelvis orientation도 고정. Pelvis local translation3 + 양쪽 thigh/shin/foot exponential-map rotation18로 ONE bounded least-squares solve. Toe local rotation은 원본 OFF를 사용했다. 각 iteration은 같은 제약식의 수치해법이며 후보 강도군이 아니다.

목표는 원본 OFF whole-sole patch L218/R223 모든 vertices의 world anchors, donor 실제 관절의 anatomical knee flexion, 원본 foot→toe forward half-plane 및 sagittal lateral15mm corridor. Anchor maximum1mm/knee0.5deg를 declared tolerance로 사용했다. 관절 pose 조건이며 실제 force/지지/seat contact 증거가 아니다.

| Side | actual knee old→new / donor(deg) | new error(deg) | whole patch max anchor residual old→new(mm) | knee forward / lateral(mm) |
|---|---|---|---|---|
| L | 33.736919 → 33.890664 / donor 31.294230 | +2.596433 | 118.591608 → 23.925415 | +68.233505 / +0.942063 |
| R | 62.235782 → 55.331985 / donor 59.684881 | -4.352896 | 109.476600 → 21.548963 | +106.614873 / +15.096769 |

저장된 첫18 actual nonadjacent BODY pair identities를 다시 검사했다: retained0, removed18. 기존 pair count만 줄이는 것으로 통과시키지 않고 모든 weak/unweighted BODY/HEAD/HAIR triangles의 source OFF 대비 새 self/cross identities도 검사했다.

- Meshy_Body_NeutralCovered__self_nonadjacent: old 18 → constrained 53; introduced relative old 53.
- Character_Body_Head__self_nonadjacent: old 66 → constrained 72; introduced relative old 14.
- Hair_Replacement_R4__self_nonadjacent: old 34 → constrained 31; introduced relative old 2.
- Meshy_Body_NeutralCovered__Character_Body_Head: old 0 → constrained 0; introduced relative old 0.
- Meshy_Body_NeutralCovered__Hair_Replacement_R4: old 0 → constrained 0; introduced relative old 0.
- Character_Body_Head__Hair_Replacement_R4: old 0 → constrained 0; introduced relative old 0.

조건 residual tolerance 통과: False. Surface/pose 종합 PASS: False. 유한 iteration/180sec 내부 solve budget에서 feasible solution을 얻었는지에 대한 실험이다. 수학적 전역 infeasibility나 immutable source skin weights의 단독 원인을 증명하지 않는다. Residual이 남으면 이번 donor-angle + original whole-sole anchors + fixed upper/pelvis orientation 조합을 production 후보로 거절한다. Exact donor 체형이나 물리적 foot support를 주장하지 않는다.

원본 OFF/fresh serialized full signature 동일, source camera960×920 decoded RGBA unequal pixels0/maxdelta0. Candidate defaults OFF. 3 pose Actions-only library에 mesh/rig/objects를 넣지 않았다. Head/hair는 기존 root에 head rigid transport로 부착하고 gaze/face drivers를 유지했다. 첫 capture repair는 저장된 pose-only 후보에 old4Actions가 없어서 bind 전 KeyError로 실패했다. 보존 후 suffixR1b에서 immutable old Action library를 append하여 완료했다. 처음 manual assignment 렌더는 Action 재평가로 old/new decoded RGBA가 동일해 비교 증거에서 제외/보존했다. 별도 동일SHA candidate capture-only guard로 두 Action을 명시적으로 바인딩, exact actual triangle identities 및 mesh SHA before/after 각 렌더를 재확인한 6장을 사용한다. Solve/새candidate/121frame 재실행 없음. Native guard CPU2threads/4GiB/600sec unchanged, strict LIVE/terminal/drain PASS. SOURCE/이전candidate SHA unchanged. GPU/protectedGUI/Product/Laptop/Unity/main 변경0; TierP0/F2/StageB 미승격.

실패 시 연구 분리: donor anatomical angle을 그대로 고정하는 방식 대신, 원본 R4에서 무릎-forward와 표면 clearance를 먼저 만족하는 native seated pose/feet-contact schedule을 설계하고 donor는 phrase timing/hip-height reference로 사용한다. 이는 별도 접근 제안이며 이 checkpoint에서 추가 pose/전체121frame sweep은 실행하지 않았다. 전달용 첫 batch는 기존 NativeTalk packet135fdc26/libraryeae83ac3를 재사용할 수 있으나 Sit capability로 세지 않는다.

Candidate SHA 387286e4eec874a35f7220bdcb2fb00228d638db57a025b8a0a45102a45aee06.
Action-only SHA 494bf8702f957a2f46512b2efdc2dddfa5c93fb5e1f001e726e8769082030006.
Guard SHA ad11f3e4a9432990a738025466a0755fe9548eff139563a56900ca3a3670434d.
원본 a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa와08caad7/R2/R3d/6Reaction/닫힌 ZIP은 보존했다.
