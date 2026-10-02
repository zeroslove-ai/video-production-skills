# PoC 실행

repo root에서 실행. Python 표준 라이브러리 + Blender + FFmpeg/ffprobe만 필요하다.
Blender source는 새 background process 전용이다. 기존 .blend/UI 세션에 실행하지 않는다.
출력 폴더는 새 이름을 사용하고 실패한 source/log를 보존한다.

## 1. 새 scene 렌더

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --factory-startup --threads 4 --python tools/previz/blender_export.py -- --manifest examples/previz/shot.json --out work/run-001
python -X utf8 tools/previz/pipeline.py prepare --assets work/run-001 --out work/run-001/prepare-result.json
```

저비용 구조 확인은 exporter에 `--smoke` 추가: 320×192, 9 frames.
smoke 에셋은 live 제출을 거부한다. Blender가 끝난 뒤 scene-state.json이 있는지 확인한다.
Blender는 script exception에도 exit code 0을 줄 수 있으므로 log와 state 모두 확인한다.

출력: `previz.blend`, beauty/depth PNG, beauty/depth MP4, `reference-video.mp4`,
first/last PNG, scene state, asset SHA-256 및 ffprobe metadata.
reference-video는 640×640 letterbox/24 fps; 임의 속도 변경 없이 재샘플링한다.
`assets.json.reference_video_eligible`은 길이/파일 크기 gate이며 provider 사용 가능 판정은 아니다.

## 2. 비용 없는 요청 준비

```powershell
python -X utf8 tools/previz/pipeline.py comfy --assets work/run-001 --out work/run-001/comfy-request.json
python -X utf8 tools/previz/pipeline.py fal --model seedance15 --assets work/run-001 --out work/run-001/seedance15-request.json
python -X utf8 -m unittest discover -s tests/previz -v
```

dry-run은 네트워크 제출/업로드 없이 파일만 만든다. 1.5 이미지 입력은 base64 data URI다.
요청 JSON에는 실제 이미지가 들어가므로 자산 접근 권한에 맞게 보관한다.

2.0/2.5 reference 경로는 manifest를 새 파일로 복사하고 `reference_images`에 승인
캐릭터 이미지 HTTPS URL, `reference_video_url`에 reference-video.mp4의 실제 URL을 넣는다.
provider에서 접근 가능한 storage에 미리 업로드해야 한다. placeholder URL을 실행하지 않는다.
스크립트는 URL 형식/count만 검사한다. 원격 URL의 파일 진위/길이/해상도/권한은 운영자가
업로드 결과와 ffprobe로 확인해야 한다. smoke reference는 2초 미만이라 사용 불가다.

```powershell
python -X utf8 tools/previz/pipeline.py fal --model seedance2 --manifest work/hosted-shot.json --assets work/run-001 --out work/run-001/seedance2-request.json
python -X utf8 tools/previz/pipeline.py fal --model seedance25 --manifest work/hosted-shot.json --assets work/run-001 --out work/run-001/seedance25-request.json
```

## 3. 실제 ComfyUI: 설치/가중치 확인 후

운영 중인 queue와 공유 GPU를 피한 전용 환경을 권장한다. 이 repo는 설치·노드·가중치를
자동 변경하지 않는다. [필요 노드/weights](../../workflows/previz/README.md)를 확인한다.

```powershell
python -X utf8 tools/previz/pipeline.py comfy --assets work/run-001 --base http://127.0.0.1:8188 --submit --out work/run-001/comfy-job.json
python -X utf8 tools/previz/pipeline.py comfy-status --base http://127.0.0.1:8188 --state work/run-001/comfy-job.json --out work/run-001/comfy-status-001.json
```

status를 재조회할 때 새 파일 이름을 준다. history가 빈 객체면 아직 완료가 아니다.
`status.completed`, `status.status_str`, error messages와 outputs를 함께 확인한다.
다운로드/최종 QA 자동화는 아직 없다. 결과 파일은 ComfyUI output에 생성된다.
모델과 입력 검사는 GPU/VRAM/품질을 보장하지 않는다.

## 4. 실제 fal: 계정/credential 및 과금 확인 후

`FAL_KEY`를 환경변수로 설정한다. 키를 manifest/커밋/log에 넣지 않는다.
dry-run과 동일 CLI에 `--submit`을 붙이면 업로드한 reference나 이미지가 외부로 전달되고
유료 queue 요청이 한 번 발생한다. 2.x는 위의 hosted-shot manifest를 사용한다.

```powershell
python -X utf8 tools/previz/pipeline.py fal --model seedance15 --assets work/run-001 --submit --out work/run-001/fal-job.json
python -X utf8 tools/previz/pipeline.py fal-status --state work/run-001/fal-job.json --out work/run-001/fal-status-001.json
```

submit 응답의 request_id와 URL을 보존한다. timeout/연결 실패로 응답이 없으면 provider
dashboard에서 접수 여부부터 확인한다. 같은 shot을 자동 재전송하지 않는다.
status는 한 번만 조회한다. 반복은 상태 파일을 바꿔 수동 재조회하거나 후속 scheduler를 둔다.
COMPLETED이면 result도 조회하지만 returned video URL은 자동 다운로드하지 않는다.
provider result schema/error/출력 metadata와 [품질 gate](REPORT.md)를 확인해야 한다.

## 한계

이 스켈레톤에는 queue scheduler, quota/budget enforcement, 취소, 자동 결과 다운로드,
provider 간 완전한 capability router, camera convention 변환, rig pose exporter,
캐릭터 LoRA 학습이 없다. API adapters는 문서와 로컬 검증을 기반으로 준비했으며
실제 provider/ComfyUI 생성까지 검증된 production integration으로 표시하지 않는다.
