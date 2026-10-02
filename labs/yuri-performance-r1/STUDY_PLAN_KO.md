## R4 model handoff checkpoint — 2026-10-02

R4 vs R3d rest rigs / 78 actions preserved. R2 66 original actions archived without curve edits. Existing 6 polished reactions reused through target-neutral retarget and grounded foot IK; 11sec native/FBX 24fps full playback complete. Export single GameRig 79 bones / 21 meshes / head 72 keys, 6 animation-only FBX takes. Full-frame fresh FBX joint error <=1.3µm. Native shader/gaze drivers and DQ/surface relax are not a Unity port; FBX material reconstruction and AlwaysAnimate runtime gate remain untested. See R4_MODEL_HANDOFF_R1_KO.md, evidence/model-handoff-r4, scripts/r4_*.py. No product/laptop/main changes.

Bundle SHA256: 48d3a241566823991801011a63ebc7e76b2c8821c6b87aaf8d013791e6330f85

## Desktop checkpoint R2: constrained dance reprojection

[DANCE_REPROJECTION_R2_KO.md](DANCE_REPROJECTION_R2_KO.md): 같은6초의 normalized 팔 제약 보정. 수동 wrist11labels 평균62.17→16.73px, actual mesh-mask IoU.5905→.6169. Unconstrained158.91deg pop 후보는 폐기했다. World/root/contact accuracy gate는 FAIL 유지. First3 native5camera 비교3영상과 relaxed-finger wave1영상 완료. 아래 checkpoint들은 작성 시점의 역사이며 최신 상태는 LATEST_RUN/evidence로 확인한다.

## Desktop checkpoint 2026-10-02: dance6sec

실제 MediaPipe / RTMW3D / MediaPipe2D+MotionBERT를 CPU 비교했다. 3 Blender/GLB와 전체1x 비교 영상은 생성·재임포트 검증됐으나 정확도 gate는 FAIL이다. 상세/재현/실패/최신 후보는 [DANCE_BENCHMARK_R1_KO.md](DANCE_BENCHMARK_R1_KO.md)에 있다. Source/model/video는 Git 제외. native5camera15영상, same-body proxy face/gaze3영상도 완료했다. 실제 R2 A/O face acceptance는 FAIL을 유지한다. GPU PRODUCT_EXCLUSIVE, product/laptop/main은 보존한다.

# 영상·연기 연구를 실제 자산으로 남기는 순서

## 1. 두 결과물을 분리한다
게임용 결과물은 bone motion, facial curves, gaze targets, contact windows, entry/exit pose, interruption markers다. 영상용 결과물은 previz/RGB/first-last/depth/pose/mask/camera metadata와 편집된 MP4다. MP4를 재사용 가능한 3D 모션으로 세지 않는다. 생성영상에서 움직임을 복원하는 경우 별도 추정·리타겟·접촉·얼굴 정리 실험으로 기록한다.

## 2. 연기부터
첫 3개는 인사, 수줍음, 부탁이다. 각 연기의 이유, 바라보는 상대, 감정 정점, 여운, 복귀가 읽혀야 한다. 자연형과 애니형은 각각 타이밍·포즈·표정 한계를 캘리브레이션하고 전 채널을 같은 비율로 키우지 않는다. 웃음은 mouthSmile 하나가 아니라 눈·눈썹·볼·입꼬리·턱과 머리/어깨 흐름을 함께 검수한다. 눈과 손이 클로즈업에서 버텨야 한다.

## 3. 구도 실험
같은 연기를 전신, 허리 위 3/4, 얼굴 클로즈업으로 비교한다. 카메라 위치·센서 폭·렌즈·피사체 거리를 함께 저장한다. 전신은 머리·발끝 여백, 애교는 얼굴과 손 silhouette, 시선은 상대방 위치를 검수한다. 세로 영상은 가로 crop이 아니라 별도 프레이밍으로 검증한다. 유리룸 플레이 중 카메라를 강제로 바꾸지 않는다.

## 4. 프리비즈 패스
각 샷에 beauty, previz.mp4, first/last frame, depth, pose, ID mask, camera metadata를 연결한다. 현재 R1에서 실제 생성한 패스는 proxy beauty/프리비즈/카메라다. Depth/OpenPose/ID는 아직 생성하지 않았고 빈 manifest 값을 완료로 간주하지 않는다. Blender depth의 거리 단위/정규화, pose의 키포인트 규약과 occlusion, mask의 객체 ID를 각 소비 모델과 맞춘 뒤 사용한다.

## 5. ComfyUI
현재 설치와 과거 성공 workflow를 유지한다. CPU API 재검증과 실제 GPU 영상 생성은 구분한다. Wan TI2V-5B I2V는 시작 프레임 실험 후보. pose/depth 강제는 별도의 Fun Control 등 모델이 필요하다. 관련 core 노드가 있어도 weights가 있다는 뜻은 아니다. 16GB GPU는 resolution/frame/activation/host RAM/decode까지 전체 과정으로 측정한다.
H3는 과거 기술적 8/8 영상 성공과 스타일 실패, 이후 1인→3인 증식이 기록되어 있다. 단일 인물·고정 identity·시작 이미지 조건을 먼저 통제한다. 이 R1에서 GPU inference 및 신규 모델 설치는 하지 않았다.

## 6. Higgsfield
좋은 표정·카메라·타이밍 후보 또는 최종 영상 픽셀 제작을 맡긴다. Blender가 canonical 데이터 원본이다. 웹의 Cinema Studio 기능 이름과 MCP 모델 ID는 구분한다. 현재 MCP로 읽은 모델은 Cinema Studio Video 3.0이며 웹 문서의 4.0 기능을 동일 API에 임의로 전달하지 않는다. 실험은 동일 원화·동일 행동·동일 길이의 한 샷 A/B부터.

## 7. 편집·오디오
검증용 MP4는 CPU libx264를 썼다. 기존 NVENC API 불일치 기록 때문에 GPU encoder 준비 완료로 말하지 않는다. 후속은 first/middle/last frame 검사→전체 재생→샷 연결→자막→음량/음성 동기→최종 규격이다. 기존 video-motion-production-skills/Remotion 자산을 재사용한다. 음성 합성/보이스 선택·비용은 따로 확인한다. Audio-to-face는 speech/emotion 입력을 얼굴 곡선으로 옮기는 보조 경로이며 리깅/몸연기/시선 전체를 대신하지 않는다.

## 8. 유리룸 도입
현재 제품 브랜치의 실제 rig mapping과 runtime adapter를 확인한다. GLB bone+weights 수치 PASS만으로 VRM/Unity/Three.js 런타임 PASS라고 하지 않는다. 동일 캐릭터 round-trip 후 seated/standing 혼합, 컵 들고 중단, 스프링본 중복, mouth override, 저사양 프레임 예산까지 통과한 클립만 제품 라이브러리에 넣는다.

## 실험 기록 템플릿
질문/가설, source hashes·라이선스, 고정 변수, 바꾼 변수 1개, frame range·fps·카메라, 타이밍곡선, first-middle-last 및 MP4, 구조 검증/눈·입·손·접촉·구도 판정, RAM/VRAM/시간/비용, 실패 원인, 다음 실험 1개를 남긴다. 완료된 연기만 완료 수로 세고 계획·파생 조합·스키마 항목 수는 따로 쓴다.
