# Desktop Animation / Video R&D — Acting R2 checkpoint

2026-10-02. 실행 상태: 연구 진행 중. 연구 repo `C:/Users/JAEWAN/projects/yuri-motion-previs-lab-r1`, branch `research/yuri-performance-previs-r1-20261002`, 시작 HEAD `f5752b7`. 제품 repo와 노트북 작업은 수정하지 않는다. main merge 없음.

## 재현한 출발점

README/HANDOFF/STUDY_PLAN/catalog/evidence/LATEST_RUN과 과거 H3 실패/회복 기록을 읽었다. R1의 17-bone 절차형 proxy 원본 hash는 `271b0fdd060810ae133e5604869976382a2df9ca0af0c863854daffd0ff75c32`. 기존 세 GLB의 실제 rotation/weights 곡선·zero start·복귀를 `validate_exports.py`로 재검증 PASS. 원본 .blend를 열어 연장했고 처음부터 재구축하지 않았다.

## 이번 실제 제작

greeting_wave / shy_lookaway / please_tilt에 5초 / 24fps의 독립 연기 score를 작성했다. 여섯 구간은 anticipation → motion → emotional peak → hold → follow-through → recovery. body/head/gaze/blink L/R/brow L/R/smile/squint/jaw에 각기 다른 곡선을 사용한다. R1의 body skeleton 17개는 보존했다. 원본 proxy에만 eye white/pupil/catchlight와 단순 open-palm finger silhouette를 추가했다. 이는 실제 Yuri topology 또는 완성 face/finger rig가 아니다.

- greeting: 작은 역방향 준비, 얼굴 옆 hand raise, wrist wave, 지연된 smile/jaw, 여운과 복귀.
- shy: 눈이 먼저 옆/아래를 보고 head/neck이 따라감, 시선 회피 hold, return smile, 복귀. 의미 곡선에서 gaze lead 4frames.
- please: 작은 역방향 준비, tilt/forward attention, brow 비대칭, mouth/jaw peak 분리, 살짝 overshoot 후 복귀.

`scripts/acting_recipe.py`는 Blender 의존성이 없는 의미 레시피다. degree와 normalized intent는 실제 target의 blendshape weight 표준이 아니다. 실제 target의 neutral/blink L/R/gaze/A/O gate는 미완료로 유지한다. approved actual-Yuri performance count=0; planned catalog count=48. 렌더 카메라/강도 조합을 완성된 모션 수로 세지 않는다.

## Hybrid 제작과 확인

연구용 Blender만 새로 실행했다. 기존 설치 add-on을 instance에서 enable/start했고 shared preferences/config를 저장하지 않았다. MCP addon status/scene read/Python execution/viewport screenshot 통과. Add-on protocol=7, 서버 기대=13; 기본 사용 경로만 확인했고 업데이트하지 않았다. 구버전이라고 최신 capability 전체 PASS로 보고하지 않는다.

Live camera correction(거리 1.65→2.25m)을 `build_acting_r2.py`로 back-port했다. `.blend` 재open 직후 MCP context.screen이 None인 실패를 기록하고 window_manager.windows의 screen.areas로 수정했다. 이후 viewport 확인 통과. Durable bpy는 factory-startup의 owned background process에서 실행한다.

## 성공/실패를 보존한 gate

- 첫 close-up은 bone anchor가 화면 안이어도 머리 silhouette가 잘렸다. `failed-first-pass/face_clipped.png` 보존. Camera distance로 수정. Bone-anchor framing PASS만으로 silhouette PASS를 주장하지 않는다.
- 첫 finger proxy는 축이 틀려 손 안에 묻혔다. `fingers_buried.png` 보존. 기존 손바닥 축소와 finger length axis 수정. 실제 anatomy/retarget gate는 아니다.
- 더 읽히는 얼굴 옆 wave로 바꾸자 lift 회전 step이 16.39°/frame로 연구 guard 15°를 초과했다. `lift-speed-gate.log` 보존. 리프트를 1.45→1.58s로 늦춘 후 14.12°/frame PASS; guard를 느슨하게 하지 않았다.
- 세 자연형 score의 all-frame 구조 gate: root=0, foot anchor drift=0, neutral return matrix difference=0. Max step greeting 14.12°, shy 2.12°, please 2.53°. 이것은 proxy 구조 검증이며 최종 연기 미학 승인과 다르다.

## 다음 controlled experiments

같은 natural score를 full body / waist-up 3/4 / face close-up / hand+face / vertical에서 비교한다. lens, sensor, transform, target, resolution은 `evidence/acting-r2/camera_metadata.json`에 저장했다. 15개 파생 샷은 CPU 렌더 중이다.

Head amplitude A/B는 head의 한 axis gain=1 vs 1.45만 변경한다. body의 다른 bone·face·gaze·hold timing 동일성을 assert했다. 전체 natural vs anime style 완성품 비교라고 부르지 않는다. Shy simultaneous vs delayed head-follow는 gaze/smile/blink를 고정하고 head-follow envelope 하나를 바꾸지만 neck/chest/brow가 그 envelope를 따르는 종속 변수임을 명시했다.

CSV/SVG timing sheets와 17 bone world pose를 실제로 출력했다. CPU BVH metric depth, binary subject mask, original object IDs, camera-projected custom pose를 3 clips × 2 cameras × first/middle/last로 생성했다. Depth=카메라 origin의 Euclidean distance(m), background=0, preview는 고정 1–7m near-white. Custom 17-bone pose는 OpenPose가 아니며 Fun Control adapter 미검증이다. 이 데이터는 비디오 모델에 아직 제출하지 않았다.

## ComfyUI / provider

PRODUCT_EXCLUSIVE GPU lease를 read-only로 존중한다. owner release 없이 model inference를 시작하지 않는다. GPU 사용률이 낮아도 lease를 회수하지 않는다. 기존 설치 업데이트/모델 다운로드/partner node 사용 없음.

ComfyUI 0.34.6의 격리 CPU core API / queue / 639 nodes 재현 PASS. 별도 CPU instance에서 같은 Blender start PNG를 LoadImage→ImageScale→SaveImage로 두 번 처리했다. 변경 변수는 bicubic vs nearest-exact뿐. 두 model-free graph PASS, video generation benefit는 미검증. 새 프로세스만 종료했으며 기존 서비스/설정을 건드리지 않았다.

H3의 이전 cartoon reference 지배, RAM watchdog 실패, 회복 8/8 technical PASS, T2V 인원 1→3 실패를 읽었다. Wan 5B 설치를 pose/depth control 구현 완료로 간주하지 않는다. Owner lease 해제 후 first-frame 유무 A/B 한 샷부터; 동일 prompt/seed/model/steps/resolution/frame count로 고정한다.

Higgsfield Cinema Studio 3.0 live schema와 5초 720p 비용만 조회: 25credits, 제출 0. 현재 schema에는 image/start/end image만 있고 driving video role 없음. 유료 호출이나 free quota를 소비하지 않았다. 실제 identity용 approved target first frame 없이 proxy를 Yuri identity reference로 보내지 않는다.

## 재현 명령과 산출물

1. `Blender --background --factory-startup --threads 4 --python-exit-code 1 --python labs/yuri-performance-r1/scripts/build_acting_r2.py`
2. 동일 Blender flags로 `render_acting_r2.py -- qa`.
3. `python labs/yuri-performance-r1/scripts/run_acting_r2.py` — candidate SHA와 job receipts를 확인하고 CPU shots를 순차 재개. 후보가 바뀌면 중단한다.
4. `python labs/yuri-performance-r1/scripts/analyze_timing_r2.py`; Blender로 `conditioning_passes_r2.py`.
5. `python labs/yuri-performance-r1/scripts/comfy_conditioning_r2.py` — model-free CPU만.

Native candidate: `C:/Users/JAEWAN/projects/yuri-motion-previs-lab-r1/labs/yuri-performance-r1/local/acting-r2/YURI_PERFORMANCE_ACTING_R2.blend`. 각 영상과 REVIEW_ACTING_R2.html도 같은 local/acting-r2 아래. 원본 바이너리/렌더는 local ignored이며 의미 레시피/스크립트/구조 evidence/소량의 original failure PNG만 Git에 기록한다.

추가 checkpoint: natural 세 연기 × 다섯 camera = 15개 CPU videos를 생성했다. Head amplitude / lead A/B 네 샷은 별도로 렌더 중이다. 이 19개는 파생 reference shots이며 19개 완성 모션이 아니다. 세 연기의 여섯 beat와 first/middle/last 및 1x 품질은 별도 평가한다. Please hand acting이 약하게 읽히므로 signature를 아직 확장하지 않는다.

실제 source의 neutral/blink/gaze/A/O calibration은 `SOURCE_FACE_R2_CALIBRATION_KO.md`를 따른다. A/O readability FAIL로 실제 얼굴의 고급 레시피 승격을 보류한다. Face-neutral native body timing 후보는 `NATIVE_BODY_R3_CHECKPOINT_KO.md`에 구조 검사/실패/수정/시각 PENDING을 분리했다.

Wan 5B의 설치된 official template와 cached core schema를 사용해 first-frame 유무 A/B graph를 `workflows/acting-r2/`에 준비했다. Graph 준비는 model inference 성공이 아니다. Required weights 존재 확인, 제출=0. Owner GPU lease 해제 전 model `/prompt`는 호출하지 않는다.

다음 bounded task: native body contact의 팔/손 실루엣과 pose continuity를 보고 가장 약한 please hand 또는 greeting raise 하나만 수정한다. 첫 세 연기가 reference로 쓸 만해졌다는 증거 전에는 signature candidate를 확장하지 않는다.
