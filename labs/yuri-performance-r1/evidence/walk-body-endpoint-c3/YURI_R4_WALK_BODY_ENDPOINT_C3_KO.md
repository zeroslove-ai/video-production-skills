USER_CAN_NOW_SEE_OR_DO: C2 왼쪽/C3 오른쪽 front·quarter·side 두 주기 전체를 24fps 정상속도 8초로 볼 수 있다. BODY 이음새는 줄었으나 왼발 바닥 침투가 생겨 C3는 FAIL/HOLD다.

# ONE BODY endpoint derivative C3 — 2026-10-05

C2 게시 완료 8fa454c를 보존하고 별도 animation-only 후보 한 개만 제작했다. 원본 R4/08caad7/R2/C1/C2와 닫힌 packet은 그대로다. 외형 승격·GameRig/mesh merge/donor geometry/새 exporter/제품·Laptop·Unity 변경은 없다.

read-only 경계 diagnostic의 큰 quaternion component derivative mismatch가 왼쪽 thigh/shin/foot에 집중되어 이 세 관절의 12개 quaternion FCurves만 수정했다. source phase2/3/4/94/95/96의 compact N4 cubic endpoint tangent average 후 quaternion normalization 방식 하나이며 sweep이 아니다. 원본 key와 endpoint pose/다른 BODY channels/root/head/hair keys는 보존한다. component norm은 rad/s가 아니므로 실제 evaluated mesh derivative를 주 판정으로 쓴다.

| Gate | C2 → C3 |
|---|---|
| 실제 BODY 경계 최대 vertex velocity mismatch | 0.070182402 → 0.013003284 m/s, 잔차 있음 |
| 실제 HEAD / HAIR 경계 mismatch | 0.007002363 / 0.007003785 m/s 그대로 |
| pose 변경 범위 | 왼쪽 thigh/shin/foot만, 최대 0.356082° / 0.910850° / 0.552491° |
| BODY 최대 실제 surface deviation | 1.516690 mm; HEAD/HAIR geometry deviation 0 |
| 고정 source stance L/R 최대 XY drift | L2.042214 / R1.844900 mm 그대로 |
| L boundary stance96..127 drift | 1.260772 → 1.624927 mm, 악화 |
| L/R persistent sole max XY step | 1.308374 / 1.347184 mm 그대로 |
| L min floor gap | +0.117180 → −0.519185 mm: **회귀 / FAIL** |
| R min floor gap | +0.000021699 mm 그대로 |
| root path actual all193 | C2와 정확히 동일, 0→−0.419831→−0.839663 m 누적, 리셋0 |
| fresh serialized OFF | 원본 source78 및 C2 prior87 full raw signature 동일 |
| source-camera OFF pixels | 960×920 decoded RGBA changed pixels0/max delta0 |

actual global1..193 전체 geometry/pose/root/sole를 측정했다. 변경된 global frames2/3/4/94/95/96/98/99/100/190/191/192 밖 BODY shape는 C2와 동일하다. Root/face/hair 3 Actions는 값과 interpolation 동일. 무변경 BODY mesh라고 주장하지 않는다. Candidate defaults OFF, original87+4 copiedActions=91; Action library4/objects0/meshes0/armatures0.

접촉 회귀: 실제 moved vertex union weak ANY left-leg weights>.01 affected triangles를 ALL BODY triangles와 비인접 identity로 비교하고 ALL BODY triangles vs HEAD/HAIR를 비교했다. 7 unique 변경/경계 phase1/2/3/4/94/95/96 new pair identities0. 나머지 phase의 actual whole geometry 동일 및 cycle의 uniform translation 때문에 새 접촉 영향이 없다는 범위다. 기존 BODY-HEAD44 source 접촉과 기존 Walk HEAD/HAIR self-contact HOLD는 해결했다고 주장하지 않는다. HEAD/HAIR actual vertices0 변화, neck/head 연결의 새 gross visible break 관찰0. Adjacent deformation/volume/forces/COM/seat support는 인증하지 않는다.

C2 native fixed-camera192frames×3를 closed C2 index SHA와 대조해 byte-exact 재사용, 재렌더/reframe0. C3 matching camera192frames×3 CPU2samples로 새 캡처했다. 9개 MP4 whole decode192/24/8sec PASS. 3개 비교영상 실제 UI playbackRate1/endedtrue/errornull; C3 cycle2 all96 grids3views와 cycle1 side grid 실제 확인. Low-resolution preview에서 큰 새 pop이나 detachment는 안 보이나 sub-mm floor regression을 영상으로 면제하지 않는다. 따라서 C3는 **FAIL/HOLD**이고 자동 승격하지 않는다.

Diagnostic guard0ed8885561aa656f2dd7848d4e937184b1def9fc60799ad32898f42aa4a71917, candidate guardf9e8fa4ae16b2be65fcc9bede032845894f805da7190310915ef536bc08af4f9 모두 strict LIVE/terminal/drain PASS; 후보 collector354.517sec/CPU2threads/4GiB/600sec. Protected Blender/GPU lease/Product 보존. Process PASS와 모션 FAIL은 별개다.

Candidate SHA 6573ca7c6a3b09d95de7a0546c8eb4083db50b45f1cb495ee31c8310e49f7fc7.
Action-only SHA c8f7ccdcbff04fb624f153cfbbc7b9942e8aae78ee0a925139f0910d056e8cea.
Source authority SHA a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa.
Private packet closure는 PRIVATE_PACKET_RECEIPT_C3.json 참고. Raw motion/geometry/images/video/source는 public Git 제외.

원인: endpoint angular tangent 수정은 mesh 속도를 줄이지만 actual floor/support constraint를 직접 보존하지 않는다. 또 다른 root/tangent strength family는 만들지 않는다. Walk 이음새 연구는 비차단 backlog로 분리한다. 처음 제안한 shortlist st_arm_1_33은 미실행이며 Root 새 지시로 다음 범위는 전용 Sitting_Enter→Sitting_Idle_Loop→Sitting_Exit의 source-only stand→sit→short hold→stand 공급으로 바뀌었다. Dedicated existing CC0 UAL1_Standard.fbx를 제한적으로 검사하며 기존 R4 rig/외형 보존, static seated label만으로 완료하지 않는다. Unity/TierP/F2/StageB는 계속 HOLD다.
