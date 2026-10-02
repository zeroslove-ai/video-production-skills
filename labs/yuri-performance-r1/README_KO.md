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
