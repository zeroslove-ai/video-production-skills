# USER_CAN_NOW_SEE_OR_DO: root 이음새 악화를 제거한 C2를 C1과 누적 두 cycle8초1x 비교 가능; 원본 BODY derivative seam HOLD

2026-10-05. ONE endpoint method/ONE saved C2 candidate. Source body pose·stance mask·rootZ·head relative geometry를 유지하고 root 시작/끝 discrete velocity를 평균값으로 맞췄다. first/last8frames compact cubic bump 최대0.643240mm, 원래 cycle endpoint 이동량은 그대로다. 각 cycle마다0.419831m가 누적되어1/97/193frame rootY는0/-0.419831/-0.839663m; reset/teleport0.

| actual 두 cycle 검사 | C1 → C2 |
|---|---|
| root 경계속도차 |0.02017236 → **0m/s** |
| BODY seam 최고 정점 velocity delta |0.08950745 →0.07018240m/s, 원본derivative 수준/HOLD |
| HEAD seam |0.02136687 →0.00700236m/s |
| HAIR seam |0.02135641 →0.00700378m/s |
| L stance anchoredXY 최고 |2.042214 →2.042214mm |
| R stance anchoredXY 최고 |1.201737 →1.844900mm, +0.643163mm tradeoff |
| root 속도범위 |0.078990–0.107004 →0.078990–0.111733m/s |
| 최고 root 가속도 |0.672260 →0.672260m/s² |
| BODY localpose matrix |전193samples C1대비delta0 |
| full body/head/hair C1+root수정 대비 |최고0.000200914mm 차이 |
| source-camera OFF pixels |decodedRGBA changed pixels0/max delta0 |

첫 job은 source BODY FCurves에 이미364Cycles modifiers가 존재하는데 비어 있다고 가정한 assertion에서 중단됐다. C2 후보 저장 전이었다. 실패script/config/guardSHA7daa22d77544860cfe05f99c42a67cb924329fe3516db9d61fa0e52a1abe8600을 보존했다. 새pinned C2b script는 복사한 Action에서 기존Cycles를 사용하며 중복Cycles를 추가하지 않는다. 원본modifier/Actions는 그대로다. 이는 같은 한 가지 방법의 구현 수정이며 strength/tangent 후보family가 아니다. Saved C2 motion candidate1개뿐이다.

C1 serialized OFF를 실제로 다시 열어 original source78/fullrawsignature 동일을 확인했고, C2도 SaveAs(relative_remap=False) 후 fresh reopen하여 C1원래83/원본78/fullrawOFF 동일을 확인했다. geometry/rest/weights/ShapeKeys/drivers/material/shader/node/texture/hierarchy 동일. 기존C1/source/R2/08caad7/닫힌packets를 덮어쓰지 않았다. BODY/Hair key values/interpolation 동일, 새4Action copies의 loop modifier만 actual 반복에 맞추었다. Carrier 및 unparented head-root location은REPEAT_OFFSET, BODY/hair/quaternion은REPEAT. Original source BODY의364Cycles는 원본에서 변경0이다.

원본BODY derivative가 heterogeneous라는 causal limitation을 증명했다. Cycle boundary97의 actual body 정점 속도 차이 field를d_v라고 할 때, uniform root derivative 보정은 모든 정점에 동일한 vector를 더할 뿐이다. 임의translation vector에도 max정점residual≥max_axis(range(d_v))/2이며 actual하한은 **0.05602734m/s**다. 따라서 body pose/timing을 그대로 두는 root tangent만으로 seam0을 만들 수 없다. Raw field는 private NPZ로 보존했다. C2는C1root가 추가한 악화만 제거하며 source BODY derivative PASS를 주장하지 않는다.

Source actual near-floor3mm stance/common vertex mask를 동일 phase로 두번 반복해 C1/C2에 그대로 적용했다. 오른발 residual 증가와 구간별 maxima/step/min gap를 scalar에 기록했다. 원래 양발 동시near-floor33frame/28persistenttransition의 요구속도 충돌을 재선정·회피하지 않았다. RootZ0, 최저footgap은L0.117180mm/R0.00002170mm로 동일범위다. 근접sole anchoring은 force support/COM/balance/physics proof가 아니다. 기존head contact gate, Unity/TierP/F2/StageB HOLD 유지.

Global1..193을 실제로 평가했다. 97/193의 endpoint geometry에서 각각누적translation을 제거하면BODY약1.08nm/HEAD0.120µm/HAIR0.055µm 수준으로 반복된다. 전193frame original BODY localpose0, 전체 body/head/hair actual 형상은C1+알려진root수정과0.000200914mm 이내다. 3구도1x에서 새로운 큰 mesh break/headhair 분리/loop reset은 관찰되지 않았다. 이는 기존collision gate를 새로PASS하거나 contact epsilon/precision 연구를 반복한 것이 아니다.

영상은192unique frames/24fps/8.0sec이며 terminal duplicate193만 encode에서 제외한다. 고정 wider front/quarter/side320×320 ORTHO1.55m/CPU2samples/JPEG92로2cycle 전체가 보인다. **C1cycle1은 기존native1..96images를 카메라metadata로 계산한 ortho affine/BICUBIC reframe하여 재사용했고 baseline render를 반복하지 않았다.** C1cycle2와C2전192frames는 실제 신규native renders다. Cached-to-native97frame의 noise/resampling 변화는 공개된 재사용한계이며 shader/pose 보정증거가 아니다. 모든C2두cycle grids 및C1side두cycle grids/세matchedcomparison1x를 검토했다. C1/C2/비교9MP4 full192decode와 actualUI3comparison1x ended8sec/errornull 완료; first/mid/last만으로 판정하지 않았다.

Exact sourceSHA a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa; 보존C1SHA d5018ac15af694f87c8cc6e9097c6cadf66d268b3f5c68d9fc9afa11b88b88fc; C2OFFcandidateSHA 16505cad36e795cd5f08e6df13e8233b9ea9849518cc8597bbe1fec691276dc1;4Action-only librarySHA b0d63636378e65478d8cd269facbdcd7bae756de2d6b04e6ce65a074427bfa01,objects/meshes/armatures0. Portable Blender Action binder는sourceRig와4Actions만 연결·복원한다. Unity에서Cycles serialization/root delta accumulation/clip/state/time/weight/AlwaysAnimate는 미검증이며FBX/exporter/runtimeadapter를 추가하지 않았다.

수정job CPU2threads4GiB/600sec guard 안에서 native432.805sec,strictLIVE/exit0/Jobactive0. 첫 실패와 정상종료 두guard 모두 증거로 남긴다. ProtectedGUI/GPUlease/product/Laptop 변경0. Source/HEAD/Idle/corpus/precision broad rerender 없음.

다음 권고 하나: separate animation-only copy에서 원본 BODY endpoint derivative를 좁게 검수·보정하고 sole mask QA와 함께 비교한다. 현재 slice에서는 body pose/timing을 변경하거나C3를 만들지 않았다. C2의 root endpoint 보정은 완료됐지만 최종seamless walk/physics/TierP/F2 승격은 하지 않는다.
