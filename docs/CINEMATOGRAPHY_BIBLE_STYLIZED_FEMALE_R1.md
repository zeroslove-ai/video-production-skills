# Stylized female cinematography bible R1

2026-10-02 · 제안값, 캐릭터별 golden frame로 조정할 설계. 성인 stylized/anime female 캐릭터의 감정·행동 가독성을 우선한다. 외모·연기·rig/표정은 upstream authoritative asset/clip으로 고정한다. 캐릭터 자체를 수정해 shot 문제를 해결하지 않는다.

## Lens / shot-size / composition

`presets/camera_presets.json`은 실제 full-frame equivalent 계산 대신 Blender sensor width 36mm, horizontal fit, perspective 기준 mm를 기록한다. output aspect가 바뀌면 vertical FOV도 바뀌므로 9:16은 별도 reframe/review한다. Blender는 sensor fit/size와 lens로 FOV를 결정한다. [Camera manual](https://docs.blender.org/manual/sr/5.0/render/cameras.html).

| Shot size | 시작 lens | 화면에서 보여야 하는 것 | 쓰임 / reject 조건 |
|---|---|---|---|
| EWS | 24mm | 장소와 인물 위치 | geography; 얼굴 감정을 맡기지 않음 |
| WS | 35mm | 전신과 발 접촉 | 행동/게임 reveal; 발·무기 끝 의도치 않은 crop reject |
| MS | 50mm | 허리 위와 주요 gesture | 인사/대사; 손이 의미 있으면 hand-safe framing |
| MCU | 65mm | 가슴/어깨 위 | 감정 전환; 목/턱 crop와 OTS foreground 가림 검사 |
| CU | 85mm | 얼굴, 눈/눈썹/입 가독성 | 고백/반응; 가까운 wide lens를 얼굴 보정 수단으로 쓰지 않음 |
| ECU | 100mm | 눈/상징 detail | 짧은 강조; context용 인접 shot 필요 |
| INSERT | 85mm | 손/소품 | prop 상태 설명; hands clip이 없으면 upstream 요청 |

수치들은 미학적 법칙이 아닌 출발점이다. 얼굴 perspective는 lens뿐 아니라 camera distance에 의해 달라진다. fit solver가 캐릭터 크기를 바꾸는 대신 camera distance와 allowed lens range를 조절한다. portrait yaw 10–25°, pitch ±5°, roll 0°를 초기 후보로 제안하며 해당 모델의 코·눈·hair silhouette를 보고 승인한다. wide lens/low angle/dutch roll은 서사 목적이 명시될 때 예외로 기록한다.

composition 좌표는 raster normalized x right/y down. thirds eye target (0.33 또는 0.67, 0.35), symmetrical reveal (0.5,0.35), gaze 방향 lead room은 face width의 약 0.5–1.0배부터 검토한다. MS/MCU headroom 5–10% frame-height를 시작값으로 두며 CU/ECU는 승인된 intentional crop 허용. 자막 영역은 기본 y≥0.82; 실제 character height/손 gesture와 aspect별 재검토. eye anchor가 없어도 bbox만으로 CU 합격 처리하지 않는다.

## Camera motion library

| ID | 계약 | 서사 용도 | 경고 |
|---|---|---|---|
| LOCKED | 위치/회전 고정 | dialogue / emotional hold | motion 없는 clip을 자동 보완하지 않음 |
| PUSH_IN | target까지 초기 거리의 최대 10% dolly, eased | 감정 집중 | focal length zoom과 구분; eye frame 유지 |
| PAN_REVEAL | stationary camera, yaw ≤20° | 발견 / 공간 정보 | axis 넘김 검사 |
| TRACK_LATERAL | 세계 meter offset, subject follow | 이동 / spatial continuity | imported root motion과 이중 이동 방지 |
| ORBIT_REVEAL | target 주변 azimuth ≤20°, constant radius | hero/game reveal | 얼굴에서 시작해 반대편 axis로 무심코 넘어가지 않음 |
| CRANE_SETTLE | world Z ≤0.5m 상승, target tracking | 환경→인물 | scale meter 확인 |

motion path의 interpolation, start/end target, speed limit, event frame을 manifest override로 pin한다. 대사 중에는 기본 LOCKED, beat change에서만 PUSH_IN 후보. 흔들림은 초기 preset에 포함하지 않는다. camera collision, foreground occlusion, clipping은 frame sampling으로 확인한다.

## Lighting / color / eye-highlight / mood

`presets/lighting_presets.json`의 key/fill/rim 값은 **key light energy에 대한 상대값**이며 물리적 노출 ratio나 얼굴 밝기 비율을 보장하지 않는다. absolute watts는 set size/material/engine을 고려한 R2 calibration에서 결정한다. axis는 subject 바라보는 방향을 0°로 하고 좌우 azimuth와 elevation으로 배치한다.

| Look | 시작 구조 | palette / eye 정책 | art review |
|---|---|---|---|
| SOFT_DAY | 큰 key, fill 0.5, rim 0.2 | warm cream / cool blue, key와 같은 방향 catchlight | 피부/눈 색을 reference와 비교 |
| WARM_CONFESSION | side key, fill 0.35, rim 0.25 | amber / muted violet, catchlight 한 개 중심 | warmth가 blush/표정 정보를 지우는지 |
| COOL_TENSION | side key, fill 0.2, rim 0.4 | slate / restrained cyan, pupil 대비 유지 | 양 눈 가독성은 감정 의도에 따라 예외 |
| HERO_RIM | broad key, fill 0.3, rim 0.7 | blue shadow / warm rim | hair rim clipping·halo 두께 검사 |
| NIGHT_NEON | motivated colored key, fill 0.25, rim 0.5 | violet/cyan 배경, face 중립성 유지 | iris hue shift / specular flicker reject |

eye highlight는 lighting/compositing의 표현 지침이다. asset이 baked anime catchlight를 이미 가지면 추가 eye light를 기본으로 만들지 않는다. material-specific eye interface가 없으면 neutral face lighting과 upstream review로 처리한다. 임의 shader 재구성이나 eye texture 편집은 scope 밖이다. projected iris 영역에서 pupil과 catchlight가 합쳐져 solid white blob이 되는 frame은 경고. 시작/중간/끝과 head turn frame의 좌우 eye 상태를 atlas와 비교하며 deliberate blink는 오류로 분류하지 않는다.

색 기준: working `Linear Rec.709`, display sRGB, opaque PNG reference. stylized toon 기준 Standard를 시작값으로 하고 PBR/HDR-like look은 승인 후 AgX variant를 별도 pack으로 둔다. Standard는 NPR용으로 사용되고 AgX는 highlights를 tone map한다. [Displays/views](https://docs.blender.org/manual/sr/5.0/render/color_management/displays_views.html). working space와 VSE space를 프로젝트 시작 시 pin한다. [Color spaces](https://docs.blender.org/manual/en/5.0/render/color_management/color_spaces.html). 이미 view transform을 적용한 PNG에 AgX를 다시 적용하지 않는다. depth/mask/pose에는 color look을 적용하지 않는다.

## Continuity와 artistic exceptions

shot마다 subject screen side, gaze target, action axis ID/camera side, prop state, light motivation, emotional beat를 기록한다. WEB_DRAMA의 A↔B 반대 eyeline은 같은 axis의 한쪽 camera half-space에서 구성. axis crossing을 원하면 neutral-on-axis bridge/re-establish shot + exception note. 애니메이션이 source frame에서 pose continuity를 제공하지 않으면 camera로 숨기기 전 upstream에 확인한다.

자동 gate는 framing bounds, subject visibility, axis flip, camera drift, duplicate catches, palette drift의 후보를 표시한다. 미적 합격은 approved frame과 named reviewer decision으로 남긴다. Agent substitution 방법: positive/negative frame 쌍 + 수치 허용구간 + beat intent + 예외 이유를 reference pack에 저장하여 다음 shot에서 반복 적용한다. 감정 강조를 위해 deliberate crop/contrast/axis break를 선택하면 예외 대상 shot/frame과 evidence를 좁게 지정한다.

Golden atlas R2 최소안: neutral/three-quarter/profile × soft-day/tension/hero-rim, 각 MS/MCU/CU. 동일 finished asset/clip revision으로 small still을 만들고 art reviewer가 선택. R1은 reference 이미지 자체를 생성하거나 인터넷 이미지의 이용 권한을 대신 승인하지 않는다.

## Appeal: 감정별 촬영 선택

아래는 실제 portrait/continuity 참고를 stylized 캐릭터에 적용하는 **설계 가설**이다. 특정 lens가 특정 감정을 만든다는 실험 결과가 아니다. adult Yuri의 눈 크기·코/턱 비율·hair silhouette를 golden atlas로 검증해야 한다. camera height는 evaluated eye center 대비 offset meters, pitch는 아래를 향할 때 +, yaw는 character forward에 대한 camera azimuth; 회전 Euler를 그대로 복사하지 않고 target으로 계산한다. headroom은 frame-height 비율. DOF 값은 beauty용; clay/depth/mask/pose는 off.

| Emotion | Preset / framing / lens range mm | Height / pitch / yaw | Placement / headroom / eyeline | Motion / 권장 길이 |
|---|---|---|---|---|
| cute | cute_closeup_soft, CU, 65–85 | +.03m / +2° / 10° | center / .04 / near-camera | locked, 2–4s |
| lovely | reaction_closeup, CU, 70–90 | 0 / 0° / 15° | right-third / .05 / partner | locked, 2–4s |
| shy | shy_lookaway, MCU, 60–80 | +.05 / +3° / 25° | right-third / .08 / away-left | locked, 2–3.5s |
| romantic | romantic_push_in, CU, 65–85 | 0 / 0° / 10° | right-third / .05 / partner→camera | slow push, 3–5s |
| comfortable | room_candid_35, MS, 32–40 | 0 / 0° / 20° | left-third / .08 / phone | locked, 3–5s |
| playful | cute_medium_candid, MS, 45–60 | +.03 / +2° / 20° | center / .08 / partner | small truck, 1.5–3s |
| confident | character_entrance, WS/MS, 35–50 | -.10 / -3° / 10° | center / .06 / destination | track, 2–4s |
| melancholy | sad_profile_closeup, CU, 65–90 | 0 / 0° / 60° | left-third / .06 / away | locked, 3–5s |
| lonely | sad_negative_space, WS, 35–50 | +.05 / +2° / 20° | left 20% / .12 / window | locked, 4–6s |
| surprised | reaction_medium, MCU, 50–70 | 0 / 0° / 10° | center / .10 / stimulus | locked, 1–2.5s |
| angry | reaction_closeup, CU, 65–85 | 0 / 0° / 15° | thirds / .05 / partner | locked, 1.5–3s |
| heroic | hero_reveal_low, WS/MS, 28–40 | -.25 / -8° / 15° | center / .06 / goal | crane settle, 2–4s |
| mysterious | shy_side_profile, MCU, 65–85 | 0 / 0° / 45° | edge-third / .08 / hidden target | slow pan, 3–4s |
| dramatic | hero_closeup, CU, 65–85 | -.08 / -3° / 20° | center / .04 / goal | short push, 2–3s |
| action | action_tracking, WS, 28–40 | -.10 / -3° / 20° | trailing third / .10 / travel | track, 1–3s |
| sleepy | cute_medium_candid, MCU override, 50–70 | +.03 / +2° / 15° | center / .08 / soft-down | locked override, 3–4s |

| Emotion | Lighting / background separation | Beauty DOF / eye rule | Editing rule |
|---|---|---|---|
| cute / lovely | soft_beauty_key / sunset_rim; quiet contrasting BG | f/4, eye focus, retain both irises | cut to smile onset 후 readable hold |
| shy | warm_window_evening; shoulder와 BG value 분리 | f/4, near eye focus; hair 가림은 atlas 비교 | lookaway를 즉시 잘라 감정 정보를 잃지 않기 |
| romantic | warm_window_evening; foreground bokeh 작은 면적 | f/4, turn 중 focus target 유지 | push가 settle한 뒤 eye-contact 24–48f hold |
| comfortable | window_morning/cozy_room; phone/bed depth layers | f/5.6 또는 off, phone와 face 관계 가독성 | insert→reaction의 정보 순서 유지 |
| playful | window_morning; hand/hair silhouette 분리 | f/5.6, gesture focus 포함 | 작은 laugh peak/settle, 무작위 speed ramp 금지 |
| confident | hero_rim; entrance edge와 destination clear | f/5.6, feet/shoulder 가독성 | 방향 맞춘 entrance→medium cut |
| melancholy / lonely | melancholy_side_light/night_blue; empty space quiet | f/4 profile, wide는 off | longer reaction, empty space에 설명 없는 cut 남발 금지 |
| surprised | soft_beauty_key; stimulus 분리 | f/5.6, eyes+hands readable | stimulus→reaction, supplied response latency 유지 |
| angry / dramatic | melancholy_side_light/dramatic_backlight; motivated contrast | f/4; shadow eye 소실은 승인 예외 | counterpart reaction을 포함, 얼굴 변경으로 강도 보완 금지 |
| heroic | hero_rim; hair/weapon outline과 BG 분리 | f/5.6; low angle에도 eyes readable | reveal 전에 geography, 후에 hero hold |
| mysterious | night_blue/dramatic_backlight; partial foreground concealment | f/4, visible eye 강조 | delayed reveal, concealment 대상/시간 명시 |
| action | hero_rim; clear travel lane, silhouette | off 또는 f/8 | motion peak 전후 cut, feet/weapon 끝 crop 검사 |
| sleepy | cozy_room; low visual clutter | f/5.6, blink annotated | 느린 hold, blink를 실패 frame으로 scoring하지 않음 |

## Female character appeal recipes

duration은 fixed requirement가 아닌 clip event/voice cue에 맞추는 시작 범위다. 아래 recipe는 카메라가 이미 있는 performance를 읽게 하는 지침이며 새로운 표정/몸동작 제작 지시가 아니다.

| Recipe | Camera / lens / composition | Lighting / movement / duration | Editing·가독성 규칙 |
|---|---|---|---|
| cute close-up | cute_closeup_soft / 65–85 / near-center eyes | soft_beauty_key / locked / 2–4s | iris·cheek silhouette를 보인 뒤 hold |
| soft smile | reaction_closeup / 70–90 / slight three-quarter | window_morning / locked / 2–4s | smile onset→peak→settle 중 최소 두 단계 포함 |
| shy reaction | shy_lookaway / 60–80 / third+lead room | warm_window_evening / locked / 2–3.5s | 시선 회피 뒤 반응 hold; OTS shoulder가 얼굴을 막지 않기 |
| look away | shy_side_profile / 65–85 / profile with gaze space | melancholy_side_light / locked / 2–4s | look-target cut과 eyeline match, 앞머리 eye occlusion 확인 |
| eye contact | romantic_eye_contact / 70–90 / centered | soft_beauty_key / locked / 2–3s | phone/partner gaze 후 lens gaze를 별도 beat로 표시 |
| small laugh | cute_medium_candid / 45–60 / shoulders+hands safe | window_morning / tiny truck / 1.5–3s | head bounce 전체를 fit, laughter settle까지 crop 재검사 |
| surprise | reaction_medium / 50–70 / center room for gesture | soft_beauty_key / locked / 1–2.5s | stimulus 먼저; supplied clip reaction delay를 임의 단축하지 않음 |
| comfortable daily life | room_candid_35 / 32–40 / phone+face layers | cozy_room / locked / 3–5s | 손·소품 관계가 얼굴 CU로 사라지지 않게 insert 연결 |
| sleepy | cute_medium_candid MCU override / 50–70 / gentle high eye-line | cozy_room / locked / 3–4s | slow blink event 포함; motion 없는 clip 자동 보완 금지 |
| romantic moment | romantic_push_in / 65–85 / near-third gaze space | warm_window_evening / .03m/s push / 3–5s | lens zoom 없이 dolly, eye-contact 전에 settle |
| sad profile | sad_profile_closeup / 65–90 / profile lead room | melancholy_side_light / locked / 3–5s | silhouette·near eye/pupil 보존, 짧은 reaction 잘라내지 않기 |
| lonely room | sad_negative_space / 35–50 / small figure left 20% | night_blue / locked / 4–6s | empty BG 정보 제거, preceding CU로 감정 연결 |
| confident entrance | character_entrance / 35–50 / travel into third | hero_rim / .25m/s track / 2–4s | travel 방향 유지, entrance 전 destination geography |
| hero reveal | hero_reveal_low→hero_medium / 28–50 / center silhouette | sunset_rim/hero_rim / crane settle / 2–4s | 낮은 각도를 과도한 얼굴 perspective로 보상하지 않기 |
| action heroine | action_wide_dynamic→action_tracking / 24–40 / lead room | hero_rim / track / 1–3s | action-start/contact/recovery sample, 무기/발 outline 포함 |

## Perspective·depth·staging를 재현 가능한 판단으로

1. sensor=36mm/HORIZONTAL에서 horizontal FOV=`2 atan(36/(2 lens_mm))`. target plane width W와 camera-axis depth d의 근사 관계는 W=`2 d tan(FOV/2)`. head bounding box/eye projection으로 거리 후보를 얻고 최종 camera render projection으로 재검사한다. DOF, yaw, 여러 깊이의 subject에는 이 근사 하나로 fit하지 않는다.
2. 같은 위치에서 lens를 바꾸면 framing/FOV가 바뀐다. 같은 face 크기를 유지하려고 camera distance도 바꾸면 nose/ear/eye perspective가 바뀐다. cute CU는 65–85mm와 충분한 거리를 시작점으로 두고, action/environment는 wider frame에 얼굴을 작게 배치한다. Nikon의 focal-length 설명은 FOV/portrait 거리 선택 참고이며 stylized 수치는 본 설계 제안이다. [Nikon focal length](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/understanding-focal-length).
3. foreground=quiet frame/shoulder, midground=acting face/hand/phone, background=motivated set. foreground 면적을 작게 시작하고 eyes/gesture occlusion을 reject 후보로 둔다. frame-within-frame은 창/문선이 head와 tangent를 만들지 않게 camera 위치를 바꾼다.
4. negative space는 외로움/망설임에 사용하되 gaze/travel lead room과 구별한다. lonely shot의 빈 공간에 밝은 prop나 text를 넣으면 의도가 바뀐다. 반대로 playful shot은 gesture가 들어갈 empty space를 확보한다.
5. blocking은 compatible clip 선택·root placement·timing·camera rehearsal이다. actor facing, hand prop contact, action crossing이 맞지 않으면 upstream clip 요청. supplied animation을 reauthor하지 않는다. 두 인물은 겹친 silhouette보다 depth/angle로 분리하고 가까운 actor와 먼 actor의 eye height를 각각 projection한다.
6. motion은 감정 변화 한 번에 한 동기로 제한한다. push는 집중, pull-out은 거리감/공간 공개, truck는 관계/이동, pan은 정보 reveal, orbit는 hero 공간 설명, crane은 hierarchy 변화. handheld_sim은 action subjective reference가 있을 때만 bounded amplitude/seed를 R2에 추가하며 기본 beauty/dialogue에 자동 적용하지 않는다.

## Evidence와 scoring

자동 점검: eye projection/visibility, framing occupancy, headroom/lead room, foreground eye overlap, face/BG separation, silhouette crop, camera settle와 clip event/cut 간 시간. ranking score는 각 metric과 reference revision을 공개하고 서로 다른 감정에 동일 weight를 쓰지 않는다. 후보 3개를 비교해 규칙 내 상위 후보는 agent가 선택할 수 있으나 기준 atlas 없는 경우 draft다. emotion/subtext/intentional asymmetry는 art 승인과 exception log로 전달한다.
