# 2026-10-02 KST — 실행 / 검증 기록

전체 결과 **PARTIAL**. 로컬 프리비즈·패키징·요청 준비는 PASS.
ComfyUI/외부 provider의 실제 확산 생성과 결과 품질은 **NOT RUN**.

## 격리 / 기준

- 정본 remote main: `29f943115c269d64d651bd641a4718b53236be00` (작업 종료 전 재확인).
- 별도 clone의 새 branch: `research/blender-previz-provider-poc-20261002`.
- 기존 research tip `48b300bc0c9834be7b1ce5b63221f6a62c461879`은 읽기만 함.
- 기존 production scene/설치/노드/model/config/다른 checkout 수정 없음.
- Blender MCP/R1 readiness gate는 수행하지 않음. 새 background Blender scene만 생성.

## 환경

- Blender 5.2.1 LTS, build `9e2066aef7ef`; CPU Cycles, 4 samples, 4 threads.
- Python 3.13.3; FFmpeg/ffprobe installed; 추가 Python 패키지 없음.
- GPU inventory: RTX 4080 SUPER, 16,376 MiB. Blender 검증은 CPU로 실행.
- 기존 ComfyUI core `8fed37813848259fbdd2548ae3cd9f14df7fd68b`, source read-only.
- 8188 API closed; Fun Control high/low weights와 Wan2.1 VAE 없음.
- `FAL_KEY` 환경변수 미설정. provider 키 값은 조회/출력하지 않음.

## 실제 실행

1. `--smoke`: 320×192, 9 RGB + 9 depth frames 성공; 대표 이미지 육안 확인.
2. Full: 640×384, 81 RGB + 81 depth frames 성공. 렌더 log 약 80.5초.
3. save-before-render `previz.blend` checkpoint와 구조 state 기록.
4. FFmpeg 인코딩, ffprobe frame count/dimensions 검증, 입력 hash 확인.
5. ComfyUI graph typed parameter binding, Seedance 1.5 이미지 data URI request 생성.
6. Seedance 2.0/2.5 constructor는 **example.com fixture URLs**로만 shape 검증;
   업로드/실제 reference fetch/외부 queue submit 없음.
7. 8 unit tests PASS. pinned official UI template의 node class 존재 여부와 설치된 core의
   static input schema를 비교: 17 nodes 모두 일치. GPU runtime/model compatibility 검증 아님.

| Encode | Resolution | fps | Frames | Duration | Bytes |
|---|---|---|---|---|---|
| beauty | 640×384 | 16 | 81 | 5.0625s | 111723 |
| depth | 640×384 | 16 | 81 | 5.0625s | 59027 |
| external reference | 640×640 padded | 24 | 122 | 5.083333s | 116661 |

provider 요청 길이는 5초다. reference video fps 변환의 끝 프레임 반올림을 기록하고,
원본/source와 provider output의 event time을 최종 QA에서 정렬해야 한다.
모든 영상은 silent; audio stream 없음.

## 구조 / 이미지 검토

`scene-state.json`: plane, cube, camera, area light의 object set과 render state.
frame 1/41/81에서 cube X는 -1.3 / 약 0 / +1.3, camera X는 6 / 5 / 4;
cube Z 0.8에 반변 길이 0.8이므로 바닥 접촉 유지. camera matrix가 기록됨.

`contact-sheet.png` 윗줄은 RGB 첫/중간/끝, 아랫줄은 동시간 depth.
한 개 cube가 화면 왼쪽에서 오른쪽으로 이동하고 camera 변화가 보인다.
depth는 near=white, far=black의 연속 경사와 cube 실루엣을 보이며
RGB와 같은 구도다. raw metric Z-pass 또는 human pose라고 표시하지 않는다.
낮은 샘플수의 프리비즈로 확인했으며 final photoreal look 검증은 아니다.

## 포함된 증거

- `previz.mp4`, `depth.mp4`, `contact-sheet.png`: 작은 실행 결과.
- `blender-render.log`, `scene-state.json`: 실행과 구조 확인.
- `assets.json`: 원래 render/package 파일 SHA-256, ffprobe metadata.
  raw sequence/previz.blend/reference-video.mp4는 ignored `work/full-001/`에 보존.
  repo에서 해당 hash 파일을 재생성하면 byte identity는 Blender/FFmpeg build에 영향받을 수 있음.
- `comfy-request.json`: bound dry-run graph; 실제 prompt_id가 아님.
- `graph-audit.json`, `provider-request-audit.json`, `unit-tests.log`: 검증 범위 명시.

## 남은 gate

독립 ComfyUI 환경의 weights/VRAM gate → depth conditioning generation → 인간 rig/pose
+ character reference 테스트 → Seedance 실제 업로드/API 한 take → identity/motion/camera A/B.
미완료 항목은 [REPORT](../../research/blender-previz/REPORT.md)의 후속 실험과 연결됨.
