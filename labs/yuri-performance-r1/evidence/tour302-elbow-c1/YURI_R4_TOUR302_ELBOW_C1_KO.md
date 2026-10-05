# Tour f302 왼팔꿈치 — ONE Action-only candidate closure, 2026-10-05

**f302의 최초 7개 교차가 제거되고 팔꿈치 접힘이 완화됐지만, 국소 strict contact gate는 FAIL/HOLD다.** f303–370에 원래 존재한 clavicle/neck 교차 1개가 남는다. 해당 삼각형 좌표는 보정 전후 f303·337에서 정확히 같다. 전체 Tour, f472 양 손목, 기존 head/hair 결함은 HOLD다. source packet/Unity/F2 승격 없음, TierP=0. 기존 9a8595e FAIL/HOLD를 보존했다.

## 고정 입력과 한 관절 후보

Immutable R4 SHA256 `a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa`; 기존 MESHY_R2_BODY_Tour Action SHA256 `e70ea471c4c0aa20efdb2ae05cbcecc49eff3e1c598e47100a1caa36fcf31202`; 과거 OFF 후보 SHA256 `378ad46ef4ccfd6e0db475534c777072c9c05cb1a8f4de81cdc4b1a2bca2cfa0`. 원본 769frames/24fps/root 위치·회전0의 제자리 showcase다. 원본78 Actions/R2/R4/08caad7/820a237와 모든 이전 파일을 수정하거나 덮어쓰지 않았다.

완료 ledger의 BODY 실패 구간 f302–371을 확인하고 forearm.L 굽힘이 0으로 돌아오는 원래 f289·385를 gesture 경계로 택했다. 실제 국소 QA는 여유 경계를 포함한 f288–386의 99 samples다. 전체769 baseline/render는 재실행하지 않았다.

기존 BODY Action을 복사하고 **forearm.L local Euler Z만** f290–384에서 비례 축소했다. 마지막 무교차 f301의 63.4764°에서 2° margin을 빼 최대61.4764°로 정했다. 원본 peak81.6976° 대비 scale0.7524876866114935다. 시작·hold·회복의 원본 key time/interpolation, 경계 밖 key·handle·modifier와 나머지360 curves는 동일하다. Quaternion을 XYZ로 분리해 X/Y를 보존하고 Z만 축소한 뒤 Quaternion으로 되돌렸다. 실제 X/Y 오차는 1e-6rad 미만이며 다른 관절의 local pose와 non-descendant world matrix 오차는 전 구간0이다. 얼굴·헤어의 실제 geometry도 전 구간 동일하다.

**원본 pose를 의도적으로 바꿨다.** 최대 굽힘은 약20.22° 줄고, 왼손·손가락은 forearm의 FK descendants로 이동한다. 다른 관절의 local 값을 직접 수정하지 않았지만 hand world trajectory가 원본과 같다고 주장하지 않는다. rig/hierarchy/rest/weights/geometry/ShapeKeys/material/node/texture/face/gaze drivers는 수정하지 않았다. 원래81 Actions/OFF 상태를 보존하고 corrective Action 하나를 추가한 82 Actions 실험본이다.

새 OFF 후보: `C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/alpha-tour302-elbow-c1d/Character_R4_Tour302_LEFT_ELBOW_C1_OFF_20261005.blend`.

SHA256 `e4d4ef74674ed840b65057776485ab01c230bc4975e780e5f3de7dde36165b7e`, 27,509,233 bytes. Action `YURI_R4_NATIVE_TOUR_LEFT_ELBOW_C1`. 저장/reopen 후 원래81/OFF 서명과 새 Action records까지 검증했다. 새 exporter/library/runtime packet은 만들지 않았다.

## 실제 geometry와 continuity QA

기존 actual BODY/HEAD/HAIR 및 동일 all-surface BVH oracle, epsilon0, source OFF baseline의 exact vertex-triple pair IDs를 사용했다. 공유 정점 adjacency만 제외했다. 매 프레임 원본과 후보를 순차 평가했고 원본 actual mesh hashes는 기존769 recovery 기록과 일치했다. count만으로 성공을 판단하지 않았으며 f302의 7 identities 소멸과 같은 원본 프레임에 없던 introduced pair0을 확인했다.

| 검사 | 결과 |
|---|---|
| f302 BODY 새 교차 / 최초7 identities | 원본7→후보0. 최초7 identities는 전99 samples에서 잔존0 |
| 국소 BODY 최대 새 교차 | 32→1 |
| 후보의 최초 잔여 실패 | f303 /12.583333sec, 원본17→후보1 |
| 같은 원본 프레임에 없는 introduced pair, 6 surface 종류 | 전99 samples 최대0 |
| 같은 원본 프레임보다 BODY count 증가 | 0 samples |
| finite / polygon topology | 전99 samples 유지 |
| 새 면적 collapse / 상대 면적 ratio<0.1 | 0/0. 원본 area>1e-10m²를 유효 대상으로, 후보 area<1e-12m²를 collapse로 정의. 최저 relative area ratio0.2866602 |
| forearm 최대 각속도 | 170.0076→127.9512deg/sec |
| 인접 frame 각속도 magnitude jump 최대 | 34.8392→26.2330deg/sec, 증가 없음 |
| 연결 경계 actual geometry | f288/289/385/386 BODY·HEAD·HAIR hashes 원본 동일 |
| other local joints / non-descendant world / head/hair | local/world max component0, head/hair vertices 동일 |
| 좌우 whole foot vertices / verified support patch | 전99 samples 원본 동일, patch component error L/R0m |
| f472 BODY/HEAD/HAIR | corrective Action을 실제 평가해 기존 원본3 mesh SHA와 일치. 양 손목 미수정 |

각속도 검사는 24fps 인접 Quaternion rotation-difference의 각속도와 magnitude 차다. signed angular acceleration, subframe continuous collision, skin 체적, 관통 깊이, 물리 접촉력을 증명한 것은 아니다. threshold를 완화하지 않았으며 `scoped_local_QA_pass=false`를 유지한다.

## 잔여1 pair의 원인 범위

f303의 잔여1 pair를 원본/보정 f303·337에서 평가했다. 두 삼각형의 원본 bone influence는 주로 clavicle.L/neck/upper_arm.L이다. 삼각형별 합산 weight는 clavicle.L 약2.113/2.021, neck 약0.474/0.526, upper_arm.L 약0.359/0.401이다. 해당6 vertices의 실제 world coordinates 최대 component 차는 두 프레임 모두0m다.

이 pair는 처음7 elbow pairs와 다르며 이번 수정으로 생긴 regression이 아니다. weights 하나를 원인으로 단정하지 않는다. 이번 forearm.L 변경에 반응하지 않는 기존 clavicle/neck 결함이라는 실제 범위까지 확인했다. 이를 고치려고 팔꿈치 굽힘을 계속 줄일 근거는 없다.

## 정상속도 전후 시각 증거

front/quarter의 같은 카메라·조명·원본 재질, 384×384 CPU Cycles8samples로 ORIGINAL/CORRECTED 각각 f289–385 전체97 samples를 촬영했다. 모든 촬영 프레임의 actual BODY/HEAD/HAIR hash가 data oracle와 일치했다. 각 구도 종료 후 source camera960×920 OFF render가 cold source baseline과 decoded RGBA exact 동일, 차0이다. 원래81/OFF/render/camera 복원과 후보 파일 bytes 불변을 확인했다.

4개 단독 MP4와2개 좌우 paired MP4는 각각97frames/24fps/4.041667sec, 전체 decode 통과. 원본 global12–16sec 구간을 clip0sec에서 재생하되 retime은 없다. 실제 UI 버튼으로 front/quarter paired movies를 정상1배속으로 모두 끝까지 재생해 endedtrue/time4.041667/rate1/errornull을 저장했다. 종료 neutral 경계에서 양쪽을 비교할 수 있다.

matchedf302/337/371에서 보정 쪽의 팔꿈치가 더 열리고 안쪽 접힘이 얕아 보인다. 손이 낮고 바깥쪽으로 이동한 원본 pose와의 차이도 분명하다. preview noise/투영으로 내부 pair별 깊이는 시각 판정하지 않는다. 보이는 변화와 exact7 제거를 함께 기록하되 visual/F2/Unity PASS로 바꾸지 않는다. 잔여 clavicle/neck 내부1pair는 이 elbow framing에서 시각 분리가 어려워 HOLD다. Blender 원본 재질의 증거이며 제품 가시성은 미검증이다.

Local review: `C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/alpha-tour302-delivery-r1/REVIEW_TOUR302_LOCAL_C1.html`; live tab http://127.0.0.1:18943/REVIEW_TOUR302_LOCAL_C1.html . 같은 folder에6 movies/6 matched images/전체1x 종료 UI PNG·JSON/video SHA·frame·decode receipts가 있다. 공개 Git에는 scripts/scalar QA/SHA pointers만 관리하고 blend/이미지/영상/실제 motion arrays는 local에 보존했다.

## 실행 실패와 완료 기록

ONE pose 가설을4개 motion 후보로 바꾼 것이 아니다. c1/c1b/c1c는 저장 이전 실행 실패라 후보가 없고, c1d만 후보를 저장해 data QA를 완료했다. c1 outside-key assertion은 FCurve.update의 경계 밖 AUTO handle 재계산을 검출했다. c1b에서는 경계 밖 handle 복원 검사를 통과했지만99프레임 actual geometry 참조를 쌓아4GiB MemoryError가 발생했다. c1c는 frame-streaming으로 바꿨으나 전체scene/OFF 서명을99회 재계산하는 비용으로600sec WATCHDOG에 도달했다. 실패 script/output/guard를 보존했으며 자원 한도를 늘리지 않았다.

c1d는 같은 pose·oracle·frame-streaming에서 geometry/other joints/whole feet를 전99 samples 비교하고, 전체81/OFF 서명은 시작·99 종료·save/reopen에서 확인했다. 186.855sec, strict terminal PASS다. 원본 보호 대상이나 pose/geometry threshold를 줄이지 않았고 실패 출력도 PASS로 바꾸지 않았다. before/after live identity, terminal exit0/ownedJob drain을 통과한 뒤 처음으로 capture를 시작했다. CPU2/4GiB/600sec/64MiB/one native job과 보호 GUI/GPU PRODUCT_EXCLUSIVE를 유지했다. 전후2구도 capture와 잔여 localization도 순차 strict 종료PASS다.

모든 guard SHA/status/error/wall seconds와 private custody는 `TOUR302_LOCAL_SCALAR_QA_C1.json`에 있다. 이전 손상 fullfeet NPZ는 읽거나 고치거나 재포장하지 않았고, 검증된1.05MB R2 supportpatch만 사용했다. 제품/Laptop/Unity/main은 수정하지 않았다.

## 다음 최소 방향 — 미실행

같은 forearm.L에서 **전체 phase의 일정 amplitude 축소 대신, 원본의 작은 굽힘은 유지하고 큰 굽힘만 연속 soft-cap하는 Action-only 가설**을 선택한다. pose/hand trajectory 차이를 줄이면서 같은 f302 elbow identities·인접 surface·각속도 gate로 다시 검사하는 방향이다. 안전 각도 이하의 원본 keys는 보존하고 hard clamp의 속도 jump를 피해야 한다. 아직 새 후보를 만들지 않았고 PASS 자산으로 승인하지 않았다.

변화하지 않은 clavicle/neck1pair는 별도 HOLD로 유지한다. 다른 관절/큰 rig/weight 연구/donor/exporter/Unitywriter로 확대하지 않는다. f472 손목과 기존 head/hair도 미수정이다. 이번 bounded closure는 **팔꿈치 개선 실증과 잔여 실패의 정확한 위치·영향 범위 확인**까지다.
