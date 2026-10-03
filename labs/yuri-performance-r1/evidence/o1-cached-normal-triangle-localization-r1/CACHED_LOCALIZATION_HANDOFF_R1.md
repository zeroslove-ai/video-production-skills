새 Windows 기능 없음 — cached34triangle rows와 normal peaks의 관계를 구분했다. **READY_SUPPORT_WAIT**.

DONE: 기존5440445/addendum을 재사용해 미확인 localization만 완료했다. 34WORST rows는 **17 source quads: slot3 ContinuousEyeSkin.L16개, slot4 ContinuousEyeSkin.R1개**다. 모두 원본 Upper corrective delta support가 있다. GN→Armature 사이 triangle-corner arrays 및 object world matrices는 정확히 같다. Source/cached8NPZ SHA 불변; Blender launch/Unity write/export/새 baseline/ZIP/transport0.

CAUSE discrimination: 34diagonal changes는 SHAPE_ONLY vsOFF 때 이미 생겼으며 GN/FULL에서 추가로 바뀌지 않는다. Global WORST normal peak는 변경 polygon/vertex/fan과 겹치지 않고, 가까운 changed vertex까지 **2.2534mm /4 source-edge hops**다. 같은 left-lid material 영역의 근접성은 pixel/triangle coincidence 증거가 아니다. Changed polygon CORNER들의 GN→FULL max angle은 **0.548368°**, global peak는 **5.034670°**다. 따라서 이 stage의 큰 normal 변화가 추가 diagonal 교체 때문이라고 말할 수 없다.

Normal 분포: WORST GN→FULL의 >1° CORNER는 L skin58/R skin32/internal headlash7이며, slot1 main skin0이다. Internal headlash slot6 max1.208541°. 기존 NEUTRAL peak는 CORNER23318/vertex4082/polygon7766/slot1/max6.935202°로 source skin 영역이며 변경 lid quads와 별개다; exact 기존 위치는 `../o1-morph67-two-input-native-normal-result-r1/ARMATURE_NORMAL_SCOPE_ADDENDUM_R1.json`을 재사용한다.

Consumer checks **세 곳만** (source zero-based IDs, Unity triangle IDs가 아님):

| 목적 | CORNER / vertex / polygon | slot | GN→FULL angle |
|---|---|---:|---:|
| Global normal peak, unchanged tessellation fan | 58781 /11616 /19153 | 3 left eyelid skin | 5.034670° |
| Changed upper-lid quad 중 normal max | 60494 /11286 /19614 | 3, Blink.L/UpperSurface.L support | 0.548368° |
| Internal headlash peak, distinct tessellation fan | 46052 /7980 /15344 | 6, Blink.R/EyePath.R/UpperSurface.R support | 1.208541° |

세 위치의 original topological smooth-fan component는 각각4 CORNER/4 polygons, selected fan에 sharp/boundary/nonmanifold edges0, packed alpha-zero4개다. Source shader slot 경계는 smooth fan을 자동 분리하는 sharp-edge 증거가 아니다. Alpha0는 기존 source semantics상 geometric fan-normal fallback이며, numerical BKE traversal/degenerate fan 처리까지 trace했다는 뜻은 아니다. 첫 peak polygon의 모든 원본 shape delta support는0이다; 이를 정확한 lower/upper anatomical patch로 임의 명명하지 않는다.

동일 local CORNER 비교+object matrix exact는 이 관측에서 exporter/world-space 변환 차이를 배제한다. Intrinsic evaluated source modifier output 변화는 확인했지만 Armature 내부 normal 처리와 fan recomputation 중 exact BKE cause는 아직 trace하지 않았다. Static normal rotate/vertex averaging/blanket DN0를 source-derived policy로 승격하지 않는다.

정확한34old/new CORNER rows 및 fan polygon/edge index는 private `outputs/o1-cached-normal-triangle-localization-r1/CHANGED_TRIANGLE_FAN_INDEX_PRIVATE_R1.json`,21,302bytes, SHA256 **752103a1ec42e71e3f3bcd8fa855dce70d67fe971126574266f7ac8db7fa9a33**. 이미 receiver가 받은 ce5c1cb7… bundle8NPZ+originalhead cache로 재구성 가능하므로 packet 재전송은 필요 없다. Public receipt는 counts/hashes/top3 mapping metadata만 공급한다; numeric connectivity/source recipe는 private에 유지한다.

FAILED-HOLD / only missing mapping: 알려진 bright upper-lid pixels의 **actual renderer/material/submesh+triangle와3 original source CORNER IDs 또는 verified split-vertex→source-loop 대응**, sameinput/pre-vs-postskin normal scope가 기존 PM pixel-count/screens 자료에 없다. 그래서 17quads 또는 위 fan이 그 bright triangles인지 확정할 수 없다. Broad inventory나 새 native probe는 필요하지 않다.

NEXT: 기존 sole writer에게 위3 locations를 전달하고 실제 bright pixel의 source identity 한 건만 받아 대응을 확인한다. Original polygon/fan adjacency·smooth/material/UV 및 per-stage native triangle rows를 유지해서 normal oracle와 비교한다. 이는 visible lid 문제를 tessellation/skin normal/internal lash 중 어디에서 확인할지 좁히며 product normal policy/PRIMARY/appearance PASS를 결정하지 않는다. Root PM transport HOLD 동안 다른 writer를 만들지 않는다.

VISUAL_EVIDENCE: 새 render/image 없음. Known bright triangle과의 coincidence는 미판정. Historical guard FAIL, F2/F3/PBR/PRIMARY HOLD, immutable R4/source/actions 보존. 필요한 cached 지원 분석은 완료되어 **READY_SUPPORT_WAIT**.
