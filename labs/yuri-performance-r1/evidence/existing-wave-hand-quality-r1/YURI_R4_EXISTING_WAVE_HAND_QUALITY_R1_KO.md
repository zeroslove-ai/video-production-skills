# 기존 Wave RIGHT 손 검수 보완

닫은 항목은 **손 검수 영상의 시작/복귀 손끝 잘림**이다. 신체 motion 개선이라고 주장하지 않는다. 같은 기존 Wave candidate580b8018,91프레임30fps에서 기존 wrist-offset 근접 camera R1은 actual 손 vertex가 최대215개 화면 밖이었다. camera R2는 actual hand bbox 중심을 따라가고 scale.24로 바꿔 전91프레임 모든 대상 손 vertex가5%여백 안에 들어왔다. 두 영상은 orientation이 같은 tracking close이며 translation/scale이 의도적으로 다르다. 같은 camera A/B나 body 궤적 비교가 아니다.

원래 motion·original79Actions·rig·geometry·rest·weights·material/node/texture·ShapeKeys·face/gaze drivers·finger local pose를 유지했다. 새 animation/candidate/export/packet 생성0. 기존 packetf1621cc2를 재생성/재전송하지 않았다. 두 hand capture의 source-camera neutral decodedRGBA 차이는0이다. all91 BODY/HEAD/HAIR actual geometry SHA는 새camera R2와 R1에서 동일하다. 기존3view body baseline 재렌더 없이 재사용했다. 원본 R4 SHAa30fc513 불변.

전actual weak/webbing triangle도 포함하는6종 surface 검사에서 BODY newpair 최고59, 첫23/최고41이 발견됐다. 해당 두 프레임의68쌍을 localization했을 때 dominant source bones는 forearm.R/upper_arm.R이며 dominant 실제handvertex를 포함한 쌍은0이었다. 이는 검수한 특정프레임의 ownership이며 모든 webbing의 물리적 품질PASS로 일반화하지 않는다. 전체 source surface quality는HOLD, 원인특정이나 modifier/weights오류 PROVEN도 아니다. 기존 낮은 해상도 body visual provisional 근거와 새 정확한 triangle 충돌 근거를 분리한다. 원래 static finger/neutral face, acting/finger-curl/Unity/F2/StageB 및 TierP0 제한은 유지한다.

R1의91개 근접프레임은 baseline hash 재실행용이 아니라 빠져 있던 실제 hand-detail 검사다. R2는 확인된 crop 결함만 수정했고 원래 inclusive contact ledger를 재사용해 collision sweep을 반복하지 않았다. 탐색 localizer의 원래 source render aspect와 정확512x512 aspect를 구분했으며 canonical crop수치는R2의215/0이다. native jobs3개 모두600초/4GiB/2CPU/64MiB/strict liveidentity/terminaldrain PASS.

전91프레임 두solo/한A/B MP4(3.033333초) whole decode PASS, 실제UI에서 native1x endedtrue/rate1/error없음. 손끝/손바닥이 시작·wave·복귀 모두 화면 안에 있고 gross 새 손 mesh break를 보지 못했다. noisy CPU8samples/정적 finger pose 때문에 세밀한 webbing/normal/표정 연기 품질승격은 하지 않는다.

리뷰 `C:\Users\JAEWAN\Documents\Codex\2026-10-02\files-pasted-by-the-user-yuri\outputs\alpha-social-wave-hand-quality-delivery-r1\REVIEW_EXISTING_WAVE_HAND_QUALITY_R1.html`
기존 source-only packet `YURI_R4_SOCIAL_GREETING_SOURCE_ONLY_R1_20261004.zip` SHAf1621cc2와 기존Action-only library는 그대로 공급 자산이다. 이 보완은 추가QA이며 제품 import 승인이 아니다.

다음 실제 motion defect는 기존Wave에서 확인한 RIGHT forearm/upperarm 교차다. 다음에 해당위치의 원본 자연1x visible defect와 native rotation/rest-axis 원인근거를 먼저 좁힐 수 있다. 이번에는 별도 새 elbow/wrist Action이나 rig/weights/cap sweep을 수행하지 않았다. Tour W1b 실패와 쇄골pixel FAIL은 그대로 보존한다.

추가로 부족한 handoff는 하나: 제품 owner의 실제 Avatar에서 upper_arm.R/forearm.R/hand.R Generic/native binding 및 playback receipt다. 기존 packet/Action library888d5d68을 재전송하지 않는다. 12quaternion channels,1..91의30fps key interval은3.0초이며 기존scene24fps로3.75초 재생하면 timing오류다. Actor/BonePath 및 rest/bind mapping은 제품 owner가 검증하고 state/time/weight/AlwaysAnimate/실제bones/root/mesh/OFF appearance gate를 반환해야 한다. 이Desktop은 Unity/importer/exporter를 수정하거나 결과PASS를 주장하지 않는다. 계약: EXISTING_WAVE_GENERIC_NATIVE_IMPORT_HANDOFF_R1.json.
