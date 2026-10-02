# Desktop R&D R3 checkpoint — 2026-10-02

## 재현한 범위

- R2 프록시: 3개 semantic acting recipe, 5개 카메라의 natural 15샷 + head amplitude 비교 3샷 + head-follow timing 비교 1샷. 총 19개 파생 MP4이며 완성된 Yuri 모션 19개라는 뜻이 아니다.
- 각 샷은 5초, 24fps, 120개 encoded frames. 별도 121번째 프레임은 neutral endpoint 검사에 사용한다. CPU Cycles 4 threads, H.264, 무음.
- 기존 프레임을 재사용해 5구도 비교 3개, head amplitude 비교 3개, eye-lead 비교 1개를 편집했다. 입력 SHA와 first/middle/last 프레임을 `evidence/comparison-r3/delivery.json`에 남겼다. 새로운 물리 motion recipe는 0개다.
- 실제 R2 개인 연구 사본: greeting/shy/please body-only 3개, 원본 66 actions·mesh·native shape geometry·skin weights·rest rig fingerprint 보존. 얼굴은 neutral. 제품 코드와 노트북 작업 변경 없음.

## 성공과 남은 결함

Greeting의 anticipation→손 들어 올리기→손목 wave→hold→내리기→neutral 복귀를 프록시와 native body reference에서 확인했다. Shy의 프록시에서는 눈이 먼저 움직이고 머리가 약 0.18초 뒤따른다. Native shy는 neutral 얼굴이므로 눈 선행을 구현했다고 주장하지 않는다. Please의 기존 낮은 손/펼친 palm은 부탁 silhouette가 약했다. 손 위치와 palm orientation을 함께 바꾼 별도 후보에서 가슴 앞 부탁 gesture가 읽힌다. 이는 두 요소를 묶은 hand strategy 실험이고 순수 한 변수 A/B가 아니다.

Native 전체 121프레임의 evaluated mesh가 finite이며 topology가 일정하고 gross bounds가 유지됐다. 삼각형 BVH 검사에서는 손끼리 겹침이 없었다. 일부 hand↔body 표면 겹침의 dominant deform group은 torso가 아니라 같은 쪽 LowerArm이었다. 손목 crease에 생긴 자체 겹침이며 penetration depth/physics contact PASS가 아니다.

손 위치/palm을 고정하고 elbow pole을 아래로 바꾼 후보는 peak/hold의 wrist surface overlap을 0으로 줄였다. 진입/복귀에는 일부 남고 half-frame 최대 회전은 6.80→9.25도라 개선이 모든 지표에 걸쳐 일어나지는 않는다. `evidence/native-body-r3-please-elbow/mesh_qa.json`과 structural QA를 함께 판단한다.

## 프록시 blink 단일 변수 실험

기존 삼각 pulse는 24fps sampling에서 양눈 완전 closure가 한번도 동시에 잡히지 않았다. Centre를 frame에 맞추고 짧은 closure plateau를 넣은 후보는 3개 recipe 각각 2개 full-closure frame을 확보했다. 121 samples의 body/head/gaze 및 blink 이외 모든 face intent가 정확히 동일함을 assert했다. 실제 target eye quality PASS가 아니라 semantic sampling PASS다. 별도 candidate: `local/acting-r3-blink/YURI_PERFORMANCE_ACTING_R3_BLINK.blend`.

## 설치를 바꾸지 않은 ComfyUI 연구

`COMFY_VIDEO_R3_KO.md` 참조. 기존 설치의 core video nodes로 CPU LoadVideo→GetVideoComponents→CreateVideo→SaveVideo roundtrip을 실제 실행했다. Legacy/dynamic SaveVideo schema 둘 다 성공. 24fps/5초/120프레임 유지, whole-clip SSIM 0.993819, first/middle/last PSNR 약 41dB. Wan T2V/first-frame 그래프 두 개는 실제 installed backend validator를 통과했고 모델 loader guard의 호출은 0이었다. 이는 모델 생성 품질 또는 first-frame의 유용성 증거가 아니다.

GPU lease는 `PRODUCT_EXCLUSIVE`이며 소유자 해제 전 video-model inference를 하지 않는다. PID가 stale해 보여도 lease를 해제하지 않는다. Higgsfield는 한 샷 입력 역할/25 credits 견적만 확인했고 generation/quota 소비는 0이다.

## 실패 재현

1. q/-q 부호는 같은 orientation인데 naive angle 보고가 359도를 보였다. shortest physical angle 측정으로 수정.
2. quaternion bake의 hemisphere가 바뀌며 실제 intermediate 180도 회전이 생겼다. adjacent keys 부호 연속성 적용.
3. two-bone IK의 pole/roll이 불안정해 greeting step이 컸다. wrist arc와 stable bone frame으로 줄였고 10도/half-frame gate는 완화하지 않았다.
4. 기존 greeting action 읽기에서 자동 slot binding만으로 motion이 0처럼 보였다. Armature를 unhide하고 OBJECT target slot을 명시하면 Greeting_Wave 3초/최대18.91도-per-frame, MOTION5H_Legacy_Greeting_Wave 6초/9.59도가 재현된다. SEC5H/SEC5HM 유사 이름은 KEY target이므로 body replay에서 제외한다.
5. append한 action의 user가 0이면 save/reopen 뒤 사라졌다. R4 조립 후보에서 fake user를 명시하고 reopen/structural QA를 다시 수행한다. 실패 로그를 보존하고 stale frames를 candidate mtime 기준으로 다시 렌더한다.

## 다음 bounded experiment

선택한 body reference 3개를 한 private candidate에 조립하고 waist-up 3/4 카메라를 약39도 azimuth로 수정해 실제 silhouette를 검토한다. 원본 66 actions의 fingerprint를 다시 검사한다. 프록시에는 기존 얼굴/시선 action bindings만 바꿔 동일한 body를 재사용하는 proof를 만든다. Actual R2는 A/O readability gate 실패가 해결될 때까지 elaborate facial recipe와 signature 확장을 완료로 계산하지 않는다.

## 재현 명령

공통 Blender: `C:/Program Files/Blender Foundation/Blender 5.2/blender.exe --background --factory-startup --threads 4 --python-exit-code 1 --python <script> -- <args>`.

- `python scripts/qa_blink_r3.py`
- Blender `scripts/qa_native_mesh_r3.py` / `-- please_elbow`
- `python scripts/run_polish_r3.py` — 3개 blink closeup + 2개 elbow body shot, 순차 CPU 실행
- `python scripts/edit_comparisons_r3.py`
- Blender `scripts/inspect_existing_greeting_r3.py`
- Blender `scripts/build_native_camera_r4.py`, 이후 `scripts/render_native_body_r3.py -- qa camera_r4`
- Blender `scripts/build_face_mix_r4.py`

모든 명령은 `labs/yuri-performance-r1` 기준. Scripts/evidence는 Git, source .blend와 rendered MP4/PNG는 ignored local에 둔다.
