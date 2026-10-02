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
