## R4 appearance correction — 2026-10-03

[R4_APPEARANCE_PRESERVE_CORRECTION_R1_KO.md](R4_APPEARANCE_PRESERVE_CORRECTION_R1_KO.md): source R4 immutable visual authority. Original 4 rigs/97 objects/19 materials/78 Actions preserved; only 6 existing reactions + 2 QA Actions added. OFF source-camera/full-body pixels identical (0 unequal channels), including ON→OFF restore. Native 24fps sequence11sec + Strong2cycles4sec + Startle1.5sec. Prior 08caad7 and bundle unchanged; GameRig structural/animation experiment ONLY, no appearance promotion. No product/laptop/main edits. Unity AlwaysAnimate runtime/appearance remains owner gate.

## R4 model handoff checkpoint — 2026-10-02

R4 vs R3d rest rigs / 78 actions preserved. R2 66 original actions archived without curve edits. Existing 6 polished reactions reused through target-neutral retarget and grounded foot IK; 11sec native/FBX 24fps full playback complete. Export single GameRig 79 bones / 21 meshes / head 72 keys, 6 animation-only FBX takes. Full-frame fresh FBX joint error <=1.3µm. Native shader/gaze drivers and DQ/surface relax are not a Unity port; FBX material reconstruction and AlwaysAnimate runtime gate remain untested. See R4_MODEL_HANDOFF_R1_KO.md, evidence/model-handoff-r4, scripts/r4_*.py. No product/laptop/main changes.

Bundle SHA256: 48d3a241566823991801011a63ebc7e76b2c8821c6b87aaf8d013791e6330f85

## Desktop checkpoint R2: constrained dance reprojection

[DANCE_REPROJECTION_R2_KO.md](DANCE_REPROJECTION_R2_KO.md): 같은6초의 normalized 팔 제약 보정. 수동 wrist11labels 평균62.17→16.73px, actual mesh-mask IoU.5905→.6169. Unconstrained158.91deg pop 후보는 폐기했다. World/root/contact accuracy gate는 FAIL 유지. First3 native5camera 비교3영상과 relaxed-finger wave1영상 완료. 아래 checkpoint들은 작성 시점의 역사이며 최신 상태는 LATEST_RUN/evidence로 확인한다.

## Desktop checkpoint 2026-10-02: dance6sec

실제 MediaPipe / RTMW3D / MediaPipe2D+MotionBERT를 CPU 비교했다. 3 Blender/GLB와 전체1x 비교 영상은 생성·재임포트 검증됐으나 정확도 gate는 FAIL이다. 상세/재현/실패/최신 후보는 [DANCE_BENCHMARK_R1_KO.md](DANCE_BENCHMARK_R1_KO.md)에 있다. Source/model/video는 Git 제외. native5camera15영상, same-body proxy face/gaze3영상도 완료했다. 실제 R2 A/O face acceptance는 FAIL을 유지한다. GPU PRODUCT_EXCLUSIVE, product/laptop/main은 보존한다.

# Yuri Performance / Previs Lab R1

## Desktop R&D continuation — Acting R2 (진행 중)

`ACTING_R2_CHECKPOINT_KO.md`에서 이어지는 연구의 실제 제작·실패·gate를 확인한다. 기존 R1 proxy .blend를 연장해 세 연기의 독립 timing score, gaze/eyelid/brow/smile/jaw, proxy open-palm silhouette와 다섯 카메라를 작성했다. 첫 실패 프레임도 보존했다. `scripts/run_acting_r2.py`가 candidate hash를 고정하고 CPU 렌더를 순차 재개한다. 이것은 실제 Yuri face/hand acceptance나 제품 승격이 아니다. approved actual-Yuri count=0을 유지한다. GPU lease PRODUCT_EXCLUSIVE, 유료 생성 0, model video inference 0.

2026-10-02. 유리룸용 연기 자산과 영상 제작을 병행 준비하는 격리 연구 작업공간.
정본 저장소: zeroslove-ai/video-production-skills
브랜치: research/yuri-performance-previs-r1-20261002
기존 제품/아바타 worktree, main, 노트북 Codex는 변경하지 않았다.

## 실제로 완료한 것
- 48종 모션 제작 계획 JSON: signature 12, conversation 12, room 12, continuity 12. 계획 수이며 제작 완료 48개가 아니다.
- 16종 표정 의미 레시피, 자연형/애니형 프로파일, 눈/입/시선 충돌 해결 순서. 실제 캐릭터 대응은 미검증.
- 렌즈/위치/센서/해상도가 있는 6개 카메라와 샷 manifest.
- Blender 5.2.1 LTS에서 원본 절차형 proxy: 17 bones, 6 morph controls, 3개 타임라인 연기 seed, 3개 GLB.
- GLB별 skin과 실제로 변화하는 rotation/weights 곡선, 시간 0 시작, 길이, 유한 수치, 끝의 기본 자세 복귀를 검증. 캐릭터 재타깃은 미검증.
- CPU Cycles 프리뷰와 4초 384x216 12fps H.264 MP4 1개. 이는 Blender 렌더 시험이며 AI 영상 생성 결과가 아니다.
- ComfyUI 0.34.6 / Python 3.12.10 / Torch 2.10.0+cu130: 격리 CPU API 시험 PASS, core 639 nodes, /system_stats 및 /queue 확인. 검증 프로세스 종료. 기본 서비스는 켜 두지 않았다.
- 재현 스크립트, 숫자 QA, 실제 경로·해시, 코덱스 작업지시서와 영상 연구 계획.

## 완료하지 않았거나 실행하지 않은 것
- 실제 유리 얼굴 리깅, 손가락/눈꺼풀/입/혀·시선 고급 연기, 실제 유리룸 런타임 도입은 아직 아니다.
- proxy에는 원래 해부학적 얼굴 topology/눈동자 리그/손가락이 없다. 예쁜 최종 캐릭터나 애교 품질로 평가한 산출물이 아니다.
- live Blender MCP add-on 상태 조회는 보안 상태 판정 문제로 차단되어 이번 세션 live 연결 PASS로 처리하지 않았다. 별도 headless Blender 제작은 검증했다.
- C:/YuriEmbodiedLab/runtime/gpu-lease.json의 PRODUCT_EXCLUSIVE 기록을 변경하지 않았다. 과거 PID는 조회 시 보이지 않았지만 자동 해제하지 않았다. 이번 GPU 영상 inference 0회.
- Higgsfield 과금/무료 quota 사용, 새 대형 model 다운로드, ComfyUI 업데이트/partner node 실행 0회.
- Depth/OpenPose/ID 패스와 최종 유리 리타겟, 음성 동기, cloud A/B는 후속 항목.
- 장기 Codex worker, 예약 실행 또는 24시간 루프를 새로 시작하지 않았다.

## 먼저 볼 파일
`CODEX_HANDOFF_KO.md` → `STUDY_PLAN_KO.md` → `catalog/motions.json` → `catalog/face_recipes.json` → `LATEST_RUN.json`.
판정 증거는 `evidence/comfy_cpu_probe.json`, `evidence/blender_proxy_build.json`, `evidence/export_validation.json`, `evidence/reel_ffprobe.json`.

## 실행/열기
`OPEN_OUTPUTS.cmd`는 산출물 폴더만 연다. Blender 원본과 GLB, preview PNG, proxy MP4의 절대경로는 `LATEST_RUN.json`에 있다.
`RUN_CPU_PROBE.cmd`는 모델 추론 없는 격리 ComfyUI 검사 후 자신이 띄운 프로세스를 종료한다.
`RUN_PROXY_PREVIS.cmd`는 원본 proxy를 다시 만들고 검증/인코딩한다. 기존 사용자 아바타는 읽거나 쓰지 않는다.

## 다음 실제 제작 단위
승인된 실제 아바타를 고정한 뒤 인사/수줍은 시선/부탁 3종부터 몸·얼굴·시선을 연결한다. 3종의 클로즈업과 복귀/중단 품질을 먼저 보고 12→48종으로 늘린다. GPU 예약이 미해결이어도 CPU authoring과 얼굴 mapping/QA는 계속 가능한 별도 작업이다.


## 2026-10-04 · 원본 R4 finger-only 작은 후보 R1

기존 820a237 보고를 finger task 완료로 혼동했던 응답을 정정했다. 실제 원본 R4의 기존 오른손 15개 뼈에만 relaxed-open → gentle curl/pregrasp → release Action을 추가했다. 105프레임/30fps/3.5초, 손목·전완·body·root 및 나머지 body bones world matrix 차이 0, endpoint 피부 형상 차이 0, 저장 재오픈 OFF neutral RGBA 차이 0. 손 close/front/side 전체 1x 재생 및 전신 위치 증거, 실제 evaluated digit surface 제한 cohort 교차 검사 전 구간 0을 남겼다. 원본/rig/weights/rest/material/face/gaze/기존78 Actions 보존. 정밀 hand skin/whole-hand collision·prop contact·physics·Unity·MUG·TierP/F2 승격 HOLD. [manifest](evidence/alpha-hand-relax-source-candidate-r1/HAND_RELAX_MANIFEST_R1.json), [보고서](evidence/alpha-hand-relax-source-candidate-r1/YURI_R4_HAND_RELAX_SOURCE_R1.md), [packet receipt](evidence/alpha-hand-relax-source-candidate-r1/PRIVATE_PACKET_RECEIPT_R1.json).


## 2026-10-04 · C1 같은 왼손 finger layer source checkpoint

오른손 조합 R1 Action 유실 실패와 R2 보존 수정, 좌우 불일치·오른손/몸 교차를 보존했다. 기존 C1 왼손 reach에 실제 왼손 rest 축으로 별도15 finger Action을 추가해 body/wrist/root 동일시각 변환차이0, 기존78Actions/오른손Action/6개 조합Action 곡선 및 원본외형 보존, OFF RGBA차이0, 61프레임30fps 손close/front/side/fullbody 전체1x 검증. 같은 손 조합 TECH PASS이나 C1 baseline에도 표면교차가 있고 curl이 복귀51–55에서 추가교차를 만들어 CONTACT FAIL/HOLD. 시작/끝C1 baseline동일, 원본R4neutral-return·prop/physics/Unity/MUG/TierP/F2 HOLD. [manifest](evidence/alpha-reach-left-finger-source-r1/SAME_HAND_SOURCE_MANIFEST_R1.json), [causal log](evidence/alpha-reach-left-finger-source-r1/CAUSAL_FAILURE_CORRECTION_R1.json), [packet](evidence/alpha-reach-left-finger-source-r1/PRIVATE_PACKET_RECEIPT_R1.json). 다음 motion 대안 하나는 body곡선 불변으로 release를51이전에 완료하는 timing-only 실험이다.


### 2026-10-04 C1 LEFT finger timing-only R2

기존 C1 body/wrist/root/face·hair transport 및 모든 이전 Action 보존. LEFT curl은 1–32프레임 실제 native 값/axes가 R1과 동일하고, release만33–44로 앞당겨45–61 완전 open. all61 같은 시각 실제 삼각형 쌍 ON/OFF 대조에서 새 교차0. 이 subset만 PASS; C1 baseline 관통1–7/50–61과 original-neutral 복귀는 FAIL/HOLD, TierP0. OFF/reopen 원본 geometry/material/keys/weights/rest/drivers/78Actions 동일 및960×920 RGBA 변경픽셀0. 네 구도61frames30fps 전체decode와 실제1x through-end PASS. 후보3a8390e5, 독립bundle cd72853c /65,873,129bytes/109members108indexed 전체CRC/SHA/size PASS. wrapper import-path 실행실패(exit95/drain0)를 보존했고 새R2b가 동일 guarded renderer 통과. 보고: evidence/alpha-reach-left-finger-timing-r2/YURI_R4_C1_FINGER_TIMING_R2.md. 기존1153398/68b46806 실패-control packet은 변경하지 않음.


### 2026-10-04 C1 baseline LEFT hand/body contact path R1

현재task ROOT_PM_C1_BASELINE_CONTACT_PATH_R1. 한가설/한source후보: upper_arm.L quaternion4channels만8deg 바깥 endpoint arc; 접근/복귀contact1–7/50–61 수정, 원래peak18–43과R2finger timing/나머지body·wrist local/root/foot/facehair 그대로. all61 actual dynamic 삼각형 쌍 비교에서 scoped left digit/hand/arm-body/head/hair after교차0, 새교차0; hand-body36→0, digit-body156/142/90/155→0. Non-left bones/sole vertices/transport error0, originalOFF960×920 RGBA변경0, samecamera18/31peak네구도변경0. 네구도전체1x/61frame/decode검수, 뚜렷한새pose pop/wrist twist 발견없음; 원래짧고빠른C1reach/return은보존. 전신weakwebbing/물리grasp/Unity/AlwaysAnimate/TierP는승격없음. endpoint는수정후start와같고 originalneutral은여전히HOLD(worldmaxcomponent169.29mm차이). 후보5b72e501, bundle76d35045 /66,414,678bytes /151members150indexed CRC/SHA/size전부PASS. Action-only8/0objects0meshes0rigs. 비교transport누락·dynamicquadtriangulation검증실패를보존했고 수정검증/실제동적surface/strictguard전부완료. Review R1복사caption오류는R1B에서고쳤고원문을보존, 실제재생은R1B사용. 기존6ce0221/R4/08caad7/C1/R1/R2/closedpacket불변, 새export/제품repo수정/healthyprocess재시작없음. 보고 evidence/alpha-c1-baseline-contact-path-r1/YURI_R4_C1_BASELINE_CONTACT_PATH_R1.md. 다음범위는별도neutral ownership 또는registered24AIreference의read-onlymatrix; 아직PENDING이며motion완성수/Player진행으로세지않음.
