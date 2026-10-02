# R2 원본 얼굴 — 연구용 calibration

제품 파일 수정 없이 이 세션에서 사용자가 제공한 R2 원본을 private research copy로 열었다. 원본 SHA256 `5e88819a61120b74c9a0e3de03f90b9890b7ac13eea2113e10fcada321d21d2e`는 전후 동일하다. 원본 66 actions/57 body bones를 유지했다. Shape key geometry, mesh/skin/rest rig 및 driver는 수정하지 않았다. 기존 FaceBoard main-channel driver의 mute 상태도 유지했다. Current channel 값과 render/camera만 disposable process에서 변경했다.

13 cases × front/quarter/side = 39 calibration images, 이어서 native weight / gaze amplitude만 바꾼 16 cases × 2 views, 마지막으로 neutral/A/O mouth-detail 3 cases × 3 views를 CPU로 렌더했다. 80장의 calibration 이미지를 80개의 연기 완성품으로 세지 않는다.

시각 판정:

- neutral / Blink.L / Blink.R / both / half: front와 quarter에서 독립 눈 닫힘을 확인했다. 이 판정은 정지 calibration 범위다. Blink curve timing과 실제 1x facial performance 승인까지 뜻하지 않는다.
- gaze: 좌우/위아래 native control에 실제 evaluated mesh response가 있다. ±1 대비 ±2는 더 움직이지 않는다. 처음 ±.65/.4는 작게 보였고, ±1은 가까운 화면에서 방향 변화가 읽힌다. 실제 source copy를 MCP에서 열어 확인했다. Pose-property 변경만으로 PASS를 주장하지 않았다.
- A/O: dedicated native viseme key는 없다. JawOpen + MouthWide / JawOpen + LipPucker의 approximate recipe를 시험했다. 최대 MouthWide displacement는 약 .72mm, LipPucker 1.80mm. 강도 1까지 올려도 두 입은 넓게 열린 수평 실루엣에 가깝다. **FAIL_A_O_READABILITY**. 확대 샷에서 차이가 일부 생기는 것과 올바른 A/O가 읽히는 것은 다르다. 발음/lip-sync 승인 없음.
- smile + squint의 낮은 초기 값은 표정이 약하게 읽힌다. 고급 target acting으로 승격하지 않는다. 기존 source 조명에 추가 key/fill을 사용한 calibration이므로 최종 beauty/color 승인도 아니다.

`AGENTS.md`의 "Neutral/blink L/R/eye direction/A/O must pass on the actual target face before elaborate facial recipes."를 적용한다. 고급 face recipe는 semantic proxy에서 계속 연구하고, 실제 source adapter는 얼굴을 neutral로 유지한 body/head/hand timing proof로 제한한다. Product repo 또는 rig 수정 요청으로 확대하지 않는다.

재현:

1. Blender factory-startup / CPU / threads4로 `scripts/calibrate_r2_source_face.py` 실행.
2. 같은 명령에 `-- sweep`, `-- detail`을 각각 추가.
3. `scripts/inspect_source_face_r2.py`: native key delta와 gaze node inventory, missing images 검사.
4. `python scripts/package_source_face_r2.py`; `python scripts/analyze_source_mouth_r2.py`.

데이터는 `evidence/source-face-r2/`, 렌더와 private .blend는 ignored `local/source-face-r2/`. Source/character binary는 Git에 넣지 않는다. Approved actual-Yuri performances=0.
