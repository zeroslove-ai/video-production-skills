USER_CAN_NOW_SEE_OR_DO: R4 원본 rig에서 stand→sit→1.67초 seated hold→stand의 실제 전신 전환을 front·quarter·side 30fps 정상속도 전체로 볼 수 있다. 새 BODY 교차·발 지지/entry pose 문제 때문에 source 후보는 FAIL/HOLD이며 승격하지 않는다.

# Sit/Stand ONE source-only retarget R1 — 2026-10-05

C3 3984e9c/closed4fae853e의 왼발 바닥 회귀는 보존하고 Walk root/tangent family를 더 만들지 않았다. 기존 shortlist/readiness의 전용 CC0 UAL1 source 한 파일만 사용했다. R4 원본에는 dedicated sitting Action이 없음을 확인했다. donor FBX는 EMPTY 임시 intake scene에서만 읽고 원본 R4를 열기 전에 모두 폐기했다. donor geometry/Rig를 R4 외형에 섞지 않았다. Rig/rest/weights/geometry/keys/drivers/shaders/materials/texture와 원본78Actions(기존66 포함)는 변경하지 않았다.

| 원본 Action identity | native frames / fps / endpoint span |
|---|---|
| Armature|Armature|Sitting_Enter | 1..40 /30fps /1.3s |
| Armature|Armature|Sitting_Idle_Loop | 1..51 /30fps /1.666667s |
| Armature|Armature|Sitting_Exit | 1..32 /30fps /1.033333s |

중복 joint endpoint의 다음 phase첫frame만 생략: candidate1..40 enter /40..90 hold /90..121 exit, 총121samples/4.0s endpointspan/4.033333s MP4. Source-native1x이며 time respeed0. Canonical/candidate 저장 scene24fps는 유지하고 QA encode30fps를 사용한다. Playback session에서만30fps로 맞춘다.

방법 하나: source world basis180°Z로 anatomical left를 맞추고, lower의 anatomical-rest delta/upper의 공통 standing-neutral delta를 target의 기존 hierarchy/native bone lengths에 풀어 넣었다. Limb scale/rest 변경 없이 target/source leg length ratio0.567134891로 pelvis translation을 정규화했다. 단일 actual lowest-sole floor-fit pelvisZ를 사용했다. Raw bone rotation copy가 아니며 새 GameRig/exporter/mesh merge/body substitution은 없다. 이 **whole donor-pose transfer + lowest-sole floorfit 조합은 Sit/Stand용으로 기각**한다. 모든 외부 motion/정규화 retarget 정책 일반을 기각할 증거는 아니다.

| actual result | 값 / 판정 |
|---|---|
| 실제 pelvis stand→seat | XYZ −1.433 /+138.941 /−221.507mm |
| 고정 seated pelvis anchor | [0.003535,0.144966,0.262922]m, hold deviation0 |
| 고정 seat plane witness | source floor 위227.922mm, pelvis clearance design35mm; 실물 prop/force 없음 |
| original support patch L/R | 218/223 actual source vertices, 원본3mm mask 유지 |
| ON first stance vs original OFF patch XY | L115.517/R196.174mm, 원본 neutral entry와 다름 |
| first ON anchored patch movement | frame2: L0.151564/R1.470674mm |
| original patch 전체 XY excursion | L27.573/R277.681mm; 계획된 R step 포함, 전부 sliding이라고 부르지 않음 |
| actual persistent3mm proximity max XY step | L2.656/R13.946mm, force support 인증 실패 |
| min whole-foot floor gap | L−0.0000423/R−0.0000565mm 수치 범위; 최저점0 근처가 planted support 증거는 아님 |
| source original patch gap span | L≤12.610/R≤44.572mm |
| new nonadjacent BODY self pairs | firstframe8:18 /peakframe96:1794 → FAIL |
| HEAD/Hair self + BODY-HEAD new pairs | peak103/45/2, 기존 source 접촉을 해결하지 않음 |
| neck/head/hair rigid root goal | max matrix error2.38419e−7, 새 gross head detach 관찰0; fine deformation HOLD |
| original raw OFF/fresh serialized OFF | source78 full signature 동일, 후보82Actions=78+4 |
| OFF source camera pixel | 960×920 decodedRGBA changedpixels0/maxdelta0 |
| first↔last ON BODY/HEAD/HAIR geometry | exact0; original neutral OFF와는 BODY176.048mm/headhair26.616mm 다름 |

Angle ROM은 원본 OFF 대비 shortest local quaternion delta: hip/thigh L19.031–106.178°,R18.041–105.222°; shin L21.631–81.182°,R43.456–79.530°; shoulder/upperarm L0–25.863°,R0–65.139°. 이는 clinical hingeROM이 아니다. 실제 joint positions의 knee flexion L23.899–87.145°,R16.565–85.388°를 별도로 저장했다. 최초 author quaternion.angle0..360 범위는 sign 의존하므로 shortest/local/world readback으로 보완했고 raw 기록을 그대로 보존한다.

## 좁은 원인 종료: 가설3개, 실제 lower joint 비교

1. lower basis/rotation 전달의 수치 오류 또는 L/R flip: **검사한8/40/96frames에서 뒷받침되지 않음**. Intended world quaternion goal과 실제 target lower pose 오차 magnitude≤0.000011°, donor→target local lower delta 차이 약0.0001° 이하다. First8 right shin donor61.438282°/target61.438296°. 단, 실제 anatomical knee는 donor59.684881°/target62.235786°로 target native rest bias +2.550905°가 남는다. Source의 first standing은 staggered stance이고 canonical R4 OFF와 다른 pose이며, upper는 다른 common-neutral 기준을 의도적으로 썼다. 따라서 donor body fidelity/neutral entry 동등성은 PASS가 아니다.

2. 해당 target pose 범위에서의 surface/deformation/clearance: **실제 교차로 지지**, weights 단독 원인은 UNKNOWN. First8 pairs18 중 shin.R–thigh.R16/thigh.R–thigh.R2. Peak96 spine–thigh.L205/spine–thigh.R177/hand.R–shin.R120 및 다수 digit–leg, knee/hip/pelvis 교차다. Dominant weight group에는 R3_Joint_CorrectiveSmooth mask도 포함되며 bone라고 오인하지 않는다. Canonical weights는 동일하지만 donor 형태 자체의 intersection-free 여부/target weights 단독 책임을 이 검사로 확정할 수 없다. Adjacent/volume 교차/피부물성 승인도 아니다.

3. 최저 sole 1점 height fit이 whole support patch/stance/seat 조건을 보존하지 못함: **확인**. Source right foot JOINT은 enter에서67.6mm 올라가는 step이고 donor actual sole/force labels는 없다. Candidate persistent-step peak118→119는13.946mm, corresponding donor right FOOT JOINT +18.458mm인데 target lowest sole≈0이다. Original support patch excursion277.681mm에는 stepping이 포함되지만 height-only fit로 planted support를 인증할 수 없다는 실패는 유지한다. Seat anchor는 floorfit 후 fitted witness일 뿐 지정 실물좌석과 맞았다는 인증이 아니다.

다음 실험 **하나만 권고, 미실행**: 첫 교차 frame8에서 원본 R4 native hip/knee/foot를 donor와 같은 anatomical knee flexion으로 맞추되 원본 whole-sole world anchor와 knee-forward corridor를 제약하는 한 pose probe. Upper reference는 고정해 현재 right-knee18pair identities와 비교한다. 없어지면 target rest/pose transfer 문제를 지지하고, 남으면 원본 rig의 해당 deformation range 문제를 추가로 지지한다. Native constrained Sit/Stand는 이 작은 probe를 통과한 뒤 같은 original neutral stance/좌석 anchor로 authoring하며, mesh/weight/rest/bind를 덮어쓰지 않는다. 새 candidate/angle/root strength family는 지금 만들지 않았다. Root가 다음 patch 범위를 선택한다.

실용적인 기존 first-batch 대안은 accepted native upper TalkGesture packet135fdc26/libraryeae83ac3 재사용이다. 이미 있는 공급을 다시 제작하지 않으며 Sit capability를 대체한다고 주장하지 않는다.

## 실제 영상 / 실패 provenance

모든121actual BODY/HEAD/HAIR triangles(weak/unweighted 포함) self/cross nonadjacent identity를 source OFF와 비교했고 실제 sole/pose/trajectory를 측정했다. Front/quarter/side121frames 전체decode/30fps1x UI through-end/errornull 및 all1213grid 검수 완료. 몸을 내려 앉고 유지한 뒤 일어나는 동작이 보이며, 깊은 thigh/hip 접힘과 손/다리 간격이 충분치 않아 영상에서도 source 완성품으로 채택하지 않는다. 낮은384CPU2sample shading noise와 원본 pale/grey hair 외형은 shader 수정으로 숨기지 않는다.

첫 native guard5e4e7697은 author121data/freshserializedOFF/후보 저장 뒤384영상 캡처 중600.2526675sec WATCHDOG FAIL, exit90/draintrue/active0. Partial154images와 모든 원본/후보를 보존했다. 별도 exact-SHA render-only completion guard285c9906은 strict LIVE/terminal/drain PASS: 기존154native images byteexact 재사용 +209missing captures만 추가. Retarget/121contact oracle/새candidate 재실행0. Completion의 첫 indentation 실패3f1755e2와 offline montage 변수충돌 실패도 보존하고 suffix repair만 적용했다. Native source intake guard08849076은 PASS. 종료/cleanup/input/candidate SHA는 failure ledger/capture receipt에 있다. CPU2threads/4GiB/600sec limits 변경0, protectedGUI/GPUlease/Product/Laptop/Unity 변경0.

Source SHA a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa.
Known CC0 donor FBX SHA21b32d912da3cb93426d974fb945e86f5b2e86970acd2ce89905e0fbf9f1dcc2.
Candidate SHA8bc13115e1a2ee5055b413c7f015650ddd1b039d34b34be9acccfe4e0de7860e/26752741bytes.
Action-only SHAa423f2ef52eac9d8af935a382b655cf272ea91607d548fb70910f679fac2b1a6/1056328bytes/4Actions/0objects0meshes0rigs.
Closed packet exact SHA/bytes/index/CRC는 PRIVATE_PACKET_RECEIPT_R1.json.

판정: R4 외형 보존 PASS, 이 Sit/Stand source motion은 FAIL/HOLD. Original66/Reaction/C3/08caad7/닫힌bundle 보존. 새 캐릭터나 physical seat runtime을 만들지 않았다. Unity/AlwaysAnimate runtime/TierP/F2/StageB/Product 승격은 없다.
