# Dance motion benchmark R1 — 2026-10-02 Desktop 연구

20.000–26.000초, 6초/360프레임을 실제 추출·보정·리타깃했다. **정확도 acceptance는 FAIL**이다. 파일 생성, 유한한 관절 값, GLB 재임포트는 PASS지만 안무 재현 PASS와 구분한다. 후렴/전체 길이로 확장하지 않았다. 제품, 노트북, main은 변경하지 않았다.

## Reference

[공개 reference](https://www.youtube.com/watch?v=IrqXrM4CaiE)는 BLACK CAT의 RESCENE Pretty Girl Dance Practice [MIRRORED], 5인 영상이다. 1920×1080, 실제 인코딩 60fps, 12,457프레임, 영상 207.616667초다. 10–20초 인접 프레임 검사에서 30fps 반복 프레임 패턴은 관측되지 않았다. 화면에 보이는 mirrored 안무를 그대로 재현하며 원래 performer의 해부학적 좌우로 되돌렸다고 주장하지 않는다.

시작/끝 held pose를 포함한 visible performance는 0–207.616667초다. 동작 시작은 2.25±0.25초, final pose 도달은 206.0±0.5초의 시각 추정이다. frame-exact choreography 경계와 후렴 라벨은 미확정이다. 20–26초 오디오 motif의 강한 반복 후보는 91.6–97.6초이며 chroma similarity 0.9673이다. 오디오 반복을 안무 반복/후렴 확정으로 세지 않는다.

선택한 오른쪽 흰색 layered dress performer는 이 구간에서 전신과 신발이 보인다. skirt가 hip centre를 가리고 wrist/hair/torso overlap이 있다. 다른 performer의 occlusion과 formation 변화는 전체 영상에서 존재한다. 이름이나 identity를 추정하지 않았다.

전체 reference는 framing/zoom/pan 변화가 있다. 20–26초의 두 벽 seam은 모든 360프레임에서 x=485/1387px로 고정이며 2Hz floor edge도 고정이다. 26초 이후 framing 변화 때문에 8초 후보를 6초로 줄였다. native60fps scene scan(480×270, threshold .20)은 hard-cut 후보 0개이며 모든 편집 부재의 증명은 아니다. 이동 dancer를 포함한 affine ECC는 correlation .343까지 떨어지고 거짓 302px translation을 내므로 camera correction에서 제외했다.

이 segment의 2D camera stability만 검증했다. 6DOF camera, 실제 intrinsics, metric floor plane, 실제 body height는 미확정이다. 키1.65m/focal1700px 가정으로 lateral root 약 .24–.26m가 나오지만 depth root는 관측되지 않아 고정한다. hip-relative XYZ를 world-root 결과로 표시하지 않는다.

## 실제 비교와 최신 후보 조사

| 실제 실행 | 입력/출력 | CPU 실행 | 결과 |
|---|---|---|---|
| MediaPipe Heavy | 33 landmarks, hip-relative XYZ + image XY | 8초480프레임 18.891s | 2D baseline, depth ambiguity |
| RTMW3D-X / ONNX | 133 whole-body, decoded XY + relative Z | 동일480프레임 52.234s | 손/팔의 depth direction reversal이 더 많음 |
| MediaPipe2D + MotionBERT Lite | 같은2D, 30fps temporal H36M17 →60fps 보간 | 6초180입력 1.031s, CPU/Torch | third temporal ablation, 독립2D detector 아님 |

원래33/133point raw NPZ와 decoder unit을 보존했다. 공통17point raw/cleaned JSON은6초다. RTMW3D의 XY pixel과 Z metre를 동일 world 좌표로 착각하지 않도록 focal/actor-distance 가정을 명시했다. MotionBERT의 head-top은 nose/neck에서 합성하고 heel/toe offset은 MediaPipe에서 이어받으므로 모델 고유 관측으로 세지 않는다. 모든 CPU inference에서 CUDA inference를 실행하지 않았으며 shared ComfyUI 설치를 변경하지 않았다.

[MediaPipe 공식 문서](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker)의 world landmarks는 hip-relative이므로 trajectory 추정과 분리한다. [RTMW3D 공식 코드](https://github.com/open-mmlab/mmpose/tree/main/projects/rtmpose3d), [rtmlib](https://github.com/Tau-J/rtmlib), [MotionBERT 공식 코드](https://github.com/Walter0807/MotionBERT)를 실제 사용했다. 모델 SHA, source-file SHA, version freeze는 evidence에 저장한다.

[WHAM](https://wham.is.tue.mpg.de/index.html)은 camera motion/contact 기반 world trajectory 비교 후보다. [GVHMR](https://github.com/zju3dv/GVHMR)은 moving-camera world motion에 맞는 다음 후보이며 official project의 2026 TPAMI 확장과 현재 SimpleVO 경로를 확인했다. [HTD-Refine](https://github.com/ant-research/HTD-Refine)는 초기 GVHMR/TRAM 결과의 full-sequence refinement 후보이며 단독 detector로 세지 않는다. 이들 local CUDA/SMPL 및 multi-GB dependencies는 PRODUCT_EXCLUSIVE lease와 별도 model/license 준비가 필요한 상태라 실행하지 않았다. 공개 GVHMR demo의 config endpoint는 HTTP502였고 upload/inference는 없었다.

[DanceHMR 2026](https://shenwenhao01.github.io/dancehmr/)는 dance/hand 연구 후보지만 확인한 공식 페이지에서 재현 가능한 released checkpoint/code를 찾지 못했다. 논문 결과를 이번 영상의 실제 비교로 세지 않는다. 유료 Rokoko/DeepMotion/Plask/Move AI는 계정·가격·라이선스 확인과 실제 비교가 없으므로 추천 winner로 선정하지 않았다.

## 정규화 리타깃과 cleanup

권리 문제 없는 기존 original procedural ProxyHumanoid를 사용했다. 원본 proxy SHA를 재확인하며 17bones의 target shoulder .4m/hip .2m와 각 upper/lower limb 길이를 기준으로 joint positions를 재구성한다. root height는 source median leg length 대 target thigh+shin 길이로 정규화한다. arm direction을 target length에 재투영하고 leg contact goal은 knee pole을 유지하는 positional IK를 사용한다. 단순 bone rotation copy가 아니다.

관측되지 않은 axial twist는 parallel transport, quaternion은 hemisphere continuity를 사용한다. wrist position은 반영하지만 손바닥 orientation/finger motion은 이번 benchmark에서 해결하지 못했다. 불안정한 head pitch/yaw는 적용하지 않고 눈 선의 screen-space roll만 적용한다. 얼굴/표정/gaze layer는 제외했다.

raw는 수정하지 않고 cleaned를 별도 저장한다. isolated one-frame reversal, root/depth jitter, wrist jitter를 제한적으로 보정한다. image acceleration 상위15%를 보존해 원래 sharp beat를 과도하게 smoothing하지 않게 했다. contact는 shoe image lift/speed/confidence 기반 heuristic이며 stance ankle+sole을 함께 lock한다. floor penetration correction과 knee pole continuity를 적용한다. depth 방향 보정/최대20deg-per-frame 제한은 기록하며 정확한 beat 보존의 증명으로 취급하지 않는다.

실패 기록: heel/toe index가 뒤바뀐 첫 RTMW3D mapping 수정; 양팔 fully-folded analytic IK의 singular flip 제거; 초기 hip-height scale의 leg stretch 수정; 179.5/154.9deg axial roll pop 수정; 3D head-direction의 false down-pitch 폐기. 초기3D contact는 sparse audit1/12와4/12였고 image-space contact로 각각9/12까지 개선했다. 이러한 개선도 acceptance PASS에는 부족하다.

## QA 및 판정

| 측정 | MediaPipe | RTMW3D | MotionBERT |
|---|---:|---:|---:|
| 독립 수동65point/6frames 평균 reprojection px |17.61|19.55|17.61 (같은2D)|
| 수동 sparse shoe-contact12labels |9/12|9/12|같은 MediaPipe contact heuristic|
| retarget 팔 방향 제한 보정 횟수 |75|242|64|
| 60fps 최대 bone quaternion step deg |24.08|30.52|20.07|
| retarget hand trajectory 좌/우 평균 px |45.18/28.79|31.82/45.99|30.71/64.13|

manual annotation 오차는 약15px이며17.61 대19.55 차이로 winner를 선언하지 않는다. hand trajectory는360frames 전체의 single global shoulder/hip orthographic alignment로 retarget wrist와 estimator XY를 비교한 diagnostic이며 독립 camera-calibrated accuracy가 아니다. MotionBERT는 direction stability가 개선돼도 오른손 궤적은 악화했다. 따라서 temporal smoothing만으로 해결됐다고 볼 수 없다.

모든360frames finite/rotation/root/contact sliding 검사를 수행했다. 최종6초180frame preview를 original audio와 time-sync하고 browser1x 재생 종료(currentTime=duration=6, ended=true)를 확인했다. GLB3개를 fresh Blender에 import해17bones/active Animation/시간별 joint movement를 검증했다. 이는 재사용 가능한 파일 검증이며 안무 정확도 PASS가 아니다.

pelvis rhythm lag0ms는 source estimator 대비 cleanup timing preservation이다. music beat accuracy는 아직 독립적으로 확정하지 않았다. silhouette IoU는 skeleton capsule 대 model person mask의 전체360frame proxy이며 실제 Blender mesh 대 reference silhouette의 metric이 아니다. contact strike/lift의 전체 onset timing, depth trajectory, actual hand/head rhythm, held-out left/right audit, perspective-aware silhouette QA가 남았다. 화면에서 팔/손 궤적과 knee/depth 움직임 차이가 보이므로 정확도 gate FAIL을 유지한다.

## 재현과 산출물

전용 ignored venv에서 requirements를 사용한다. source reference와 model cache는 local-only이며 Git에 넣지 않는다. model receipt URL/SHA를 확인한다. Python scripts의 root는 laboratory folder다.

1. `dance_prepare_r1.py` / `dance_extract_r1.py`로 선택 ROI raw 추출.
2. `dance_motionbert_r1.py`로 같은 MediaPipe2D temporal ablation. 현재 read-only existing Torch runtime 경로를 config에 기록.
3. `dance_clean_r1.py`로 raw/cleaned/common17/contact evidence 생성.
4. Blender `-b --python dance_retarget_r1.py -- METHOD`로 private .blend/GLB 생성.
5. `dance_render_r1.py`, `dance_qa_r1.py`, `dance_extra_qa_r1.py`, `dance_glb_roundtrip_r1.py`, `dance_package_r1.py`로 전체 구간 검사 및 비교 영상.

reference manifest/timecodes, raw NPZ, raw+cleaned JSON/NPZ, 3 .blend/GLB, retarget config, 1x comparison MP4, model/source receipts, QA/failed-correction 기록을 local deliverable package로 제공한다. 비교 영상에는 공개 source6초 픽셀/오디오가 들어가므로 이것도 Git에는 넣지 않는다. 공개 reference 원본이나 model weights는 배포 package에도 포함하지 않는다. reusable motion이 핵심이며 MP4를3D animation으로 대체하지 않는다.

## 다음 bounded experiment

1. 같은6초에서 GVHMR world/contact estimate를 비교한다. 먼저 owner가 GPU lease를 해제했는지 확인하고 SMPL/model licence 및 download 크기를 준비한다. CPU 결과로 world reconstruction 성공을 주장하지 않는다.
2. reference의60fps contact strike/lift 및 wrist path를 독립 annotation으로 확대하고 moving-camera calibration을 별도 평가한다. source mirror convention을 audit한다.
3. target normalized limb constraints와 perspective reprojection을 공동 optimize해 MotionBERT 오른손 오차 및 knee direction을 줄인다. held-out frames로 평가하고 sharp beat 가중치를 유지한다.
4. 실제 retarget mesh silhouette/foot contact timing acceptance가 통과한 뒤 phrase→chorus→whole dance로 늘린다. face timing은 body acceptance 뒤 별도 semantic layer로 추가한다.
