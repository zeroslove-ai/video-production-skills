# USER_CAN_NOW_SEE_OR_DO: 원본 대비 발 미끄러짐을 줄여0.420m 전진하는 native Walk 후보를3구도1x로 비교 가능; velocity seam/기존head contact는 HOLD

2026-10-05. ONE source-derived root-contact animation-only C1. 원본 actual sole stance를 동일 frame/time/pose에서 고정 기준으로 비교해, 가장 큰 XY drift가134.123975mm에서2.042214mm로98.477% 감소했다. 발목/무릎/몸 proportion을 바꾸지 않았다. Partial kinematic improvement이며 Unity/TierP/F2/StageB 승격은 없다.

| 항목 | 원본 → C1 |
|---|---|
| L stance최대 anchored XY excursion |134.124 →2.042mm |
| R stance최대 anchored XY excursion |134.124 →1.202mm |
| persistent sole frame XY step최대 L/R |4.602 →1.309mm |
| 실제 floor gap 변화 |최대0.00002392mm, rootZ0 |
| BODY bone local pose |전97프레임 matrix delta0 |
| 전체 body/head/hair 형상 |원본+rootTranslation과 최대0.0001533mm 차이 |
| root 이동 |fixed → world[0,-0.419831333,0]m/4sec |
| root 속도 |0 →0.078990–0.107003m/s |
| root 최대 가속도 |0.672241m/s² |
| BODY seam velocity delta |0.070183 →0.089507m/s, **악화/HOLD** |
| HEAD/HAIR seam delta |0.007001 →약0.021366m/s, **HOLD** |
| root seam speed difference |0.020172m/s, **HOLD** |
| root 누적 translation 제거 후 endpoint geometry |BODY約1.32nm,HEAD約0.091µm; closed geometry만으로 velocity PASS 금지 |

방법 하나만 실행했다. Source 실제 foot/toe weight>.5 정점들 중 source floor3mm 이내이며 연속frame 공통인 sole 정점들의 XY delta median을 발별 계산한다. 그 음수의 equal-foot 평균을 Assembly_Root XY 이동으로 적분한다. 기존 BODY/hair Actions는 그대로 재사용하고, unparented Armature.Root에 동일 world translation을 별도 Action으로 더한다. RootZ/원본 BODY curve/머리rotation/driver/rest/weights/material 변경0. 새root와head translation2Actions만 추가하며 기존81/원본78 모두 raw signature 보존.

동시에 양발이3mm 가까운 frame은33/97, 양발persistent velocity가 함께 존재하는 transition은28/96이다. 최고 두 sole 요구속도 차이0.056019m/s: rigid root 하나로 둘을 완전히 고정할 수 없으며 equal-foot 해의 residual 하한은발별0.028010m/s이다. 이 값과 남는1–2mm slip을 공개한다. 3mm proximity는 침투/기울기/foot roll을 포함한 기하 기준이며 force support/COM/balance/physics 결과가 아니다. Source contact mask/common vertex 집합을 C1에도 그대로 써서 숫자가 좋아 보이도록 stance를 재선정하지 않았다.

보존된 source와 기존 source-only Walk 후보·Action library·R2/08caad7·닫힌 Walk/head reference packets는 SHA 동일. Source-camera neutral960×920 decodedRGBA changed pixels0/max delta0. Existing hierarchy/geometry/skin/rest/shader/material/node/texture/face/gaze drivers/원본78/기존81Actions 모두 source OFF 원본과 동일. 새 후보는 animation OFF로 별도 SaveAs(relative_remap=False)했다. Writer의 before/afterSaveAs rawOFF gate는 통과했으나 이1job에서는 새 serialized candidate fresh reopen을 추가로 실행하지 않았고, 이를 consumer gate로 남겼다.

Gross geometry 비교는 전97프레임 실제 full body/head/hair 정점 전체가 원본+uniform root translation과0.0001533mm 이내임을 확인한 범위다. BODY local pose0/body-head-hair 상대 연결 유지,3구도1x에서 새 큰 mesh break/head detachment/collision은 관찰되지 않았다. 기존 head contactHOLD를 면제하거나 triangle epsilon/count를 재연구하지 않았다. 형상동일성 bound는 collision/contact-force clearance 인증이 아니다.

원본 프리뷰는 재렌더하지 않았다. 고정 front/side/quarter(기존 source fullbody QA 카메라; product Unity 카메라 PASS 아님)의 기존97 images/videos와 C1 신규97images를 같은320×320CPU2sample/JPEG92 설정으로 비교했다. 모든97 source/candidate3구도 grids, 새candidate3 MP4와 source-left/candidate-right3 MP4 full decode, 실제UI3comparison1x ended/error null 확인. original24fps/full97=4.041667sec,endpointspan4sec. Candidate Rootdelta 누적 locomotion loop가 필요하며 제자리로 reset하면0.420m teleport한다. 실제 two-cycle seamless loop/Unity root-motion import는 미검증이다.

원본sourceSHA: a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa. 기존Walk후보SHA: 80e1b5db465fafdd810852e244186bd47cbcc7907c819b810823b7d208fdf408. 신규OFF후보SHA: d5018ac15af694f87c8cc6e9097c6cadf66d268b3f5c68d9fc9afa11b88b88fc. Action-only4Actionlibrary SHA: 3008d478ce72e2d5c6a6706d3a0b8818278db67f32351d5cd2f0d2c7c2c0f089;objects/meshes/armatures0. Source/원본control/newcandidate/library/soletrajectory/camera/fullproof/ownedguard/workflow를 separate private packet에 포함한다. 공개Git에는script/scalar/SHA만 관리한다.

CPU2threads4GiB owned guard1job, native240.087sec/strictLIVEbarriersPASS/exit0/Jobactive0. GUI/GPUlease/product/Laptop 변경0. 메모리/output guard 원래설정 유지. Native precision/ReplantR2/Idle/Head97 rerender/각도IKstrength sweep0.

최소 다음 대안 하나: 기존BODY pose와 stance mask를 그대로 둔 채 carrier loop endpoint velocity/tangent만 constrain하고 residual sole drift를 다시 검사하는 bounded experiment. 이번에는 실행하지 않았다. C1은2mm급 slip 개선을 보여주는 root-motion handoff 실험이며 seam/force/기존contact gates가 남아 있는 최종걷기asset은 아니다.
