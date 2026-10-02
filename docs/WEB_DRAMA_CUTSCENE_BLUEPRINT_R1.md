# Three production mode blueprints R1

모든 sequence는 설계 fixture. 24fps, 1280×720, 16:9, straight cuts. 아래 길이는 clip availability와 대사 녹음에 맞춰 R2에서 수정한다. assets/animation은 다른 프로젝트에서 납품받는다. 단순 proxy set/prop layout은 이 repo가 담당할 수 있다.

## Mode별 운영 계약

| Mode | 우선 목표 | 필수 입력 | edit / delivery |
|---|---|---|---|
| CHARACTER_SHORT | 한 인물의 readable emotional turn | A finished asset + compatible gesture/face clip, simple set | 3 shots/12s, first/last/eye frames, captions optional |
| WEB_DRAMA | dialogue와 관계/eyeline continuity | A/B finished assets + talk/listen clips + timed voice cues, prop states | 6 shots/30s, coverage map, isolated audio tracks, J/L-cut 후보 |
| GAME_CUTSCENE | 공간 reveal와 gameplay로 돌아가는 위치 | finished clips/root-motion policy + environment anchors + return-state | 6 shots/24s, camera samples + spatial metadata; engine import는 R2 |

시작/end action pose는 supplied clips에서 선택한다. 다른 rig에 clip을 retarget하거나 body/facial performance를 생성하지 않는다. clip이 없으면 blocking GP placeholder와 upstream request를 기록하고 final proof 생성을 보류한다.

## CS01 — 창가의 인사 / CHARACTER_SHORT

필요 assets: `CHAR_A` adult anime female finished `.blend` library, `CLIP_A_GREETING` 288 frames/24fps compatible action (idle→turn→greeting→hold, face 포함), `SET_WINDOW` meter-scale small room/window plane, optional approved greeting audio. landmarks eye_center/head/hand와 root policy=locked. fixture audio는 없음, 자막도 선택.

| Shot | Edit frame / sec | Size / lens / motion | Purpose / asset slice | Gate |
|---|---|---|---|---|
| CS01_SH010 | 0–96 / 4s | MS 50 / LOCKED | window와 A, clip 1–96 | head/hand safe |
| CS01_SH020 | 96–192 / 4s | MCU 65 / PUSH_IN | turn/greeting, clip 97–192 | iris/catchlight, camera dolly |
| CS01_SH030 | 192–288 / 4s | CU 85 / LOCKED | emotional hold, clip 193–288 | 마지막 48 frames hold 의도 검토 |

SOFT_DAY 동일 motivation을 유지. R2 P0 첫 smoke는 이 sequence 3 shots의 start/mid/end 9 still과 low-res animatic로 한정한다.

## WD01 — 카페의 약속 / WEB_DRAMA

필요 assets: `CHAR_A`, `CHAR_B` compatible finished libraries; `CLIP_A_DIALOGUE`, `CLIP_B_DIALOGUE` 각 720 frames/24fps (seated talk/listen/response, synced face 포함); `SET_CAFE` table/chairs/window; `PROP_NOTE` 닫힘/열림 상태; `A_VOICE`, `B_VOICE` cue sheet+48kHz wav (녹음은 외부 입력). prop 손동작은 supplied clip이 책임진다.

Floorplan: A=(-1,0,0), B=(1,0,0), action axis A→B world X. camera는 world Y<0 half-space에 유지. A는 screen-left, B는 screen-right; A gaze right/B gaze left. OTS occluder는 foreground shoulder로 한정하고 눈/입을 가리지 않는다.

| Shot | Edit frame / sec | Camera preset | Beat / clip selection | Continuity |
|---|---|---|---|---|
| WD01_SH010 | 0–120 / 5s | WS35_LOCKED | two-shot 관계/장소, A/B 1–120 | table/note CLOSED |
| WD01_SH020 | 120–264 / 6s | OTS65_LOCKED | A가 약속을 설명, A/B 121–264 | B foreground, A gaze right |
| WD01_SH030 | 264–384 / 5s | MCU65_LOCKED | B silent reaction, A/B 265–384 | B gaze left, pause 확보 |
| WD01_SH040 | 384–504 / 5s | INSERT85_LOCKED | note OPEN, A/B 385–504 | prop transition clip 필요 |
| WD01_SH050 | 504–624 / 5s | CU85_LOCKED | A 결심, A/B 505–624 | eyes/face identity |
| WD01_SH060 | 624–720 / 4s | MS50_LOCKED | two-shot resolution, A/B 625–720 | 시작 axis 재확인 |

WARM_CONFESSION look을 고정. synthetic cue 계획: A voice edit `[120,264)`, B voice `[384,480)`; 실제 녹음이 없으며 fixtures는 경로/placement만 표시한다. J/L-cut은 source audio trim과 placement를 분리해서 R2에서 조정한다. 말하는 인물보다 듣는 인물에 cut하는 판단은 자동 speaker detector가 대신하지 않는다. 대사의 semantic turn과 approved pause range를 rule로 제공한다.

## GC01 — 관문 발견 / GAME_CUTSCENE

필요 assets: `CHAR_A`; `CLIP_A_GATE` 576 frames/24fps walk→stop→look→hold→return-facing (finished body/face, authored root motion); `SET_GATE` meter-scale courtyard/gate; `PROP_BEACON` emissive marker; start/end gameplay anchor와 camera convention sidecar. 캐릭터 translation은 clip root motion 한 번만 적용하며 추가 이동은 금지. fixture는 world Z up, camera local -Z forward/+Y up, gameplay engine 미지정.

| Shot | Edit frame / sec | Camera preset | Beat / clip selection | Gate |
|---|---|---|---|---|
| GC01_SH010 | 0–96 / 4s | EWS24_LOCKED | gate geography, clip 1–96 | A와 destination 동시 가독성 |
| GC01_SH020 | 96–192 / 4s | WS35_TRACK | approach, clip 97–192 | feet/contact는 입력 clip 평가만 |
| GC01_SH030 | 192–288 / 4s | MS50_ORBIT | stop/reveal, clip 193–288 | orbit 20° 한도, axis 유지 |
| GC01_SH040 | 288–384 / 4s | INSERT85_LOCKED | beacon light cue, clip 289–384 | cue frame camera metadata |
| GC01_SH050 | 384–480 / 4s | CU85_LOCKED | reaction, clip 385–480 | supplied expression |
| GC01_SH060 | 480–576 / 4s | WS35_LOCKED | return orientation, clip 481–576 | anchor/last-frame handoff |

HERO_RIM look, beacon cue는 환경 이벤트로만 애니메이트 가능. engine conversion은 engine 이름/축/단위/vertical-vs-horizontal FOV를 확인한 뒤 수행한다. Blender beauty export를 engine-ready camera/animation이라고 표현하지 않는다. skip/branch/interactive gameplay는 R1 linear sequence model 밖이며 stable sequence/event IDs로 R2 확장한다.

## PM 검토 / R2 수락 기준

fixtures: `examples/previz/{CS01,WD01,GC01}.sequence.json`와 15개 Shot JSON. 자산은 placeholder, frames는 반개구간 start+duration; 표의 end는 배타적 edit end, clip 범위 설명은 inclusive이다.

PM은 shot purpose/duration/mode scope를 검토하고 asset owner는 clip range/compatibility/root policy를 확인한다. Art reviewer는 look/eye/angle/pace를 승인한다. 기술 gate는 15 shot preset/reference/asset ID와 time consistency를 검사한다. 실제 production gate는 state + rendered evidence + audio/engine 검증까지 별도로 필요하다.
