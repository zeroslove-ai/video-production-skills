# R4 기존 native Tour 전체 구도 검수 — 2026-10-05

**FAIL/HOLD: 기존 native Tour의 팔꿈치·손목 주변 새 표면 교차가 남는다. 공급용 source packet은 만들지 않았다.** 같은 후보의 정면·3/4·측면을 원본 24fps 전체 769프레임으로 촬영하고 실제 1배속 끝까지 재생했다. 사용할 수 있는 범위는 제자리 showcase 연기의 연구/reference evidence다. root 이동·회전이 모두 0이므로 walk/turn/navigation motion으로 세지 않는다. StageB 준비 자료이며 Stage A 완료, Unity, F2, TierP 승격을 뜻하지 않는다. TierP=0.

## 고정 입력과 원본 보존

- Immutable source `Character_Master_NeckSkin_R4.blend`: SHA256 `a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa`.
- 기존 Action `MESHY_R2_BODY_Tour`: SHA256 `e70ea471c4c0aa20efdb2ae05cbcecc49eff3e1c598e47100a1caa36fcf31202`. 52 bones / 364 curves / frames 1–769 / 24fps. Key·handle·modifier 값과 원본 clock 그대로다. endpoint span=32.0초, inclusive container=32.041667초.
- 이미 저장된 OFF 후보 SHA256 `378ad46ef4ccfd6e0db475534c777072c9c05cb1a8f4de81cdc4b1a2bca2cfa0`, 27,119,089 bytes. 추가 authoring·재저장·retime·rig rebuild·mesh merge·donor geometry·exporter 제작은 이번 closure에서 0회다.
- 원본 78 Actions, geometry, hierarchy/rest, weights, materials/nodes/textures, ShapeKeys, gaze/face drivers와 OFF bindings/pose 보존. cold source와 후보 OFF 서명이 일치한다. 각 전체 구도 종료 후 source camera 960×920 decoded RGBA 차이 0. 기존 `08caad7`, corrective `820a237`, R2/R3d, 닫힌 후보와 실패 출력은 보존했다.
- head/hair는 기존 full-world transport를 사용했다. 769프레임 root goal matrix 최대 component 오차는 face Armature `8.940696716308594e-8`, HairRig `2.980232238769531e-7`. seated 실험의 잘못된 additive adapter를 재사용하지 않았고, 이번 Tour에서 adapter mismatch가 입증되지 않아 새 adapter 수정은 하지 않았다.

## 실제 움직임과 접촉 측정

원본 root 위치·yaw 범위는 0이다. pelvis Z 범위는 21.935mm, head yaw 범위는 약 36°다. 새로운 공간 이동이나 회전 연기로 해석하지 않는다.

769프레임 actual BODY/HEAD/HAIR geometry finite 및 topology를 검사했다. 각 전체 구도는 프레임별 실제 세 mesh hash가 recovery 평가와 같을 때만 촬영했다. 모든 actual self-nonadjacent surface pairs와 BODY↔HEAD↔HAIR 조합을 source OFF baseline의 pair identity와 비교했다. 공유 정점 adjacency는 제외하고 BVH epsilon=0을 사용했다. count만으로 PASS를 정하지 않았으며 새로운 교차 identity가 남으므로 FAIL이다. 교차 깊이/volume나 물리 접촉력은 이 검사 범위가 아니다.

| 새 교차 종류 | 전 구간 최대 |
|---|---:|
| BODY self | 33 |
| HEAD self | 96 |
| HAIR self | 42 |
| BODY–HEAD | 5 |
| BODY–HAIR / HEAD–HAIR | 0 / 0 |

최초 BODY 실패는 f302 / 12.541667초의 7 pairs, 원본 지배 weights는 `forearm.L / upper_arm.L`다. 최대 BODY 실패는 f472 / 19.625초의 33 pairs: right forearm/hand 13, left forearm/hand 11, right forearm self 6, left forearm self 3. 지배 weights 분류는 위치를 설명하며 skin weights 하나만을 원인으로 확정하지 않는다. f1/302/472/769에서 새 pair identity 전체를 다시 평가해 완료 ledger와 정확히 일치했다. 원본 native curves를 그대로 적용하는 pose/skin 조합의 surface failure이며, 접촉/appearance 품질 PASS로 공급하지 않는다.

발 구간 분류는 actual persistent vertices의 근접/이동을 사용했다. gap>3mm는 airborne, gap<−1mm는 below-floor, persistent XY step≤2mm는 planted-proximity candidate, 나머지는 moving-near-floor다. 이는 contact force/support proof가 아니다. 최소 gap L+0.117158mm/R0mm; near-floor persistent XY 최대 step L7.983239/R5.496415mm; 원본 support patch XY anchor 최대 excursion L69.45905/R69.48385mm다. 171–288의 발 이동/들림이 포함되고 상세 좌우 구간은 scalar JSON에 있다. floor fitting/contact correction을 수행하지 않았다.

## 전체 1배속과 근접 시각 증거

정면 기존 촬영은 재시작하지 않았다. 이미 실행 중이던 quarter/side를 같은 writer에서 순차 완료했다. 세 구도 모두 256×256 CPU Cycles 2 samples, 769 frames, 24fps, 32.041667초다. JPG frame SHA 확인, MP4 전 구간 decode와 frame count 확인, 실제 UI play 버튼으로 세 video 모두 playbackRate=1 / ended=true / error=null을 기록했다. 실제 종료 화면은 `WHOLE_NORMAL1X_UI_VIEWPORT_R2.png`다. 최초 fullPage 캡처는 텍스트가 좁게 렌더된 capture artifact여서 보존하고 정상 viewport screenshot을 별도로 남겼다.

전신 영상은 gross motion과 시간 확인용이다. sampling noise와 작은 projected joint 크기 때문에 내부 surface 교차를 부정할 수 없다. 기존 상위 결함 f302 왼팔꿈치, f472 좌우 손목만 front/quarter 동일 카메라 OFF/ON 512×512 CPU8samples, 총 12장 근접 촬영했다. 새 authoring/전체 고해상도 렌더는 없으며 해당 ON geometry는 기존 recovery frame hash와 같고 종료 OFF/source78 복원도 일치한다.

| 결함 | 직접 보이는 부분 | 확인 못한 부분 |
|---|---|---|
| f302 LEFT elbow | 정면/3/4에 내측 접힘 자국·좁은 crease가 보임 | 7개 내부 교차를 shading만으로 각각 식별 불가. 측면에서는 팔꿈치가 몸에 가려짐 |
| f472 LEFT wrist | 강한 손목 굽힘, 압축된 손/전완 silhouette와 crease가 보임 | 렌더에 깊이/삼각형 구분이 없어 모든 11 pairs의 관통 깊이 판정 불가 |
| f472 RIGHT wrist | 굽힘·안쪽 접힘과 view-dependent hand silhouette가 보임 | 3/4에서 일부 palm이 forearm에 가려짐. 13 pairs의 내부 상태 전체 판정 불가 |

몸·얼굴·헤어의 gross explosion이나 detach는 전신 witness에서 보이지 않는다. 이것을 미세 contact/skin PASS로 바꾸지 않는다. **Blender 근접 증거의 변형은 실제 보이지만, 제품에서 보이는지는 Unity를 열지 않았으므로 미검증**이다. immutable source의 외형/재질은 그대로 사용했고 개선된 런타임 shader를 가정하지 않았다.

## 실패 원인과 출력 한도 복구

실패한 실행/스크립트/출력은 수정하거나 덮어쓰지 않았다. 최초 intake frame 제한 600은 실제 Tour 769와 달라 source-r1이 실패했고 readonly intake로 실제 clock을 확인했다. source-r2는 FModifier memory repr 비교 오류였으며 후속 별도 script는 stable RNA 값을 비교했다. source-r3 전체 mesh cache는 combined 64MiB cap으로 실패했다. source-r4는 candidate와 769 surface ledger를 완료했지만 candidate 27.12MB와 fullfoot NPZ 39.93MB 및 logs의 합이 한도를 넘어 NPZ 종료 footer 쓰기 중 중단되었다. 따라서 source-r4 guard는 FAIL 그대로다.

손상 NPZ SHA `ffd01813f9a6dfeec76ae588636d9c74e6e4850efdfed2bed9ffdc427425731a`, 39,932,726 bytes는 PK header만 있고 ZIP footer가 없다. 첫 recovery의 BadZipFile은 이 파일 손상 때문이며 mkdir/Blender/candidate의 문제로 해석하지 않는다. 손상 파일을 믿거나 재포장하지 않았다.

recovery-r2는 SAME saved candidate에서 필요한 769 whole-sole scalar와 원본 L218/R223 support patch coordinates만 다시 평가했다. full769 collision/authoring을 다시 하지 않았다. 작은 lossless NPZ 1,053,929 bytes, SHA `e65638226244f92bb6797df6cf7d965bfbe293df0ecea692a3299f221b04f661`는 CRC/shape/finite/readback 후 atomic finalized verified copy를 만들었다. 600sec/4GiB/2CPU/64MiB 한도를 늘리지 않았다. capture-front-r1 wrapper의 import 실패도 보존하며 r2에 script path를 고정했다.

| 종료된 실행 | 결과 | guard SHA256 |
|---|---|---|
| source-r4 | output cap FAIL 보존 | ab3a71b17f9f9f0bd6b197460d17ad7ecc05f5ce3d25d279aedcc9c72ae8f6d8 |
| recovery-r2 | strict terminal PASS | 5583d6b5be7998cf63413b25ab96f1d41251d9bd8f23331eeb7bacb39d615d25 |
| front-r2 | strict terminal PASS | 841ddeefdf44e222a05769433e2b80ea66cace0809e11800511ef47eee8e0175 |
| quarter-r2 | strict terminal PASS | f3b83110b710565037f74e7872e9fbc31742cc97405fbd5b47f49d2510b0d2dc |
| side-r2 | strict terminal PASS | cdda729598edd3b2a3c7563411ca7b03fb1e916b7b1194526468b1a02552b808 |
| ranked close-r1 | strict terminal PASS | 1165301ec9a3ab475de4745910ee92e7c5d1bd191bc8b64d5b33ac23abd56f57 |

모든 native 작업은 한 번에 하나, CPU2, 보호된 GUI Blender 및 PRODUCT_EXCLUSIVE GPU lease 불변이며 live before/after와 terminal exit0/drain을 확인했다. guard PASS는 해당 실행의 완료/원본 보존을 뜻하며 motion acceptance PASS가 아니다. 모든 guard 경로/SHA, 실패 status는 scalar QA JSON에 있다.

## 사용 가능한 증거와 다음 한 방향

Local delivery: `C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/alpha-native-tour-delivery-r1/REVIEW_NATIVE_TOUR_SOURCE_R1.html`. 같은 폴더에 front/quarter/side MP4, native-clock grid, 구간 witness sheets, 세 matched defect images, whole UI receipt/screenshot이 있다. 검수 탭: http://127.0.0.1:18942/REVIEW_NATIVE_TOUR_SOURCE_R1.html . 파일/영상 SHA는 `VIDEO_CUSTODY_PUBLIC_R1.json`; raw geometry/motion은 공개 Git에 올리지 않았다.

최소 correction 후보 한 방향: **최초 실패 f302 주변 왼팔꿈치 굽힘 경로만 별도 Action-copy에서 줄이고**, 원본 타이밍을 유지한 상태에서 exact new pair identities와 인접 구간 continuity를 재평가한다. skin/rest/재질/geometry 수정은 금지한다. 원본에서 벗어난 pose 수정임을 명시하고 f472 양손목은 별도 HOLD로 유지한다. 이 correction은 이번 범위에서 실행하지 않았다. 신규 corpus/donor/Walk/Sit/duplicate Talk/Wave 연구로 확대하지 않는다.

결론은 evidence closure다. **surface gate 실패 때문에 reusable source asset/library/runtime packet export는 생략**했다. Unity product/laptop, TierP/F2/MUG/physics, Active Ragdoll과 main merge는 수행하지 않았다. 기존 Reaction appearance correction을 다시 baseline 실행하거나 승격하지 않았다.
