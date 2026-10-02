# Blender previz export / optional Comfy handoff R1

2026-10-02 · contract 설계와 공식 workflow 조사. 다운로드·Comfy 실행·GPU benchmark·video provider 호출 없음. Blender animatic를 기준 결과로 유지하며 Comfy proof는 camera/identity/continuity 보장 수단으로 취급하지 않는다.

Scope correction: 이 문서는 이전 R1의 minimal 조사와 export 계약을 보존하는 **future handoff 문서**다. 이번 보완에서 Comfy 구현/provider 비교/API adapter를 추가하지 않는다. [Draft PR #4](https://github.com/zeroslove-ai/video-production-skills/pull/4)의 backend experiment를 read-only 참고했으며 복사·수정·merge하지 않았다. 최종 Blender production과 generative handoff는 editorial approval 후의 선택 경로다.

## Export bundle contract

project relative `exports/<shot_id>/<revision>/`. `index.json`은 manifest SHA256, asset/clip SHA256, exact Blender build/engine, preset revision, OCIO config hash, fps rational, source range/handles, resolution/pixel aspect, coordinate system, 파일별 frame/channel/color/encoding/checksum, status를 가진다. shot JSON의 `export_contract`는 요청이며 outputs 생성 증거가 아니다. R2 index schema는 별도 구현한다.

| Product | Format / 의미 | Alignment / fallback |
|---|---|---|
| beauty | PNG8 sRGB opaque view-baked, optional scene-linear EXR master | GP notes/burn-ins 없는 clean frames; look/OCIO pin |
| clay | 별도 neutral material override view-layer/scene의 PNG8 | builtin pass로 가정하지 않음; camera/clip geometry 같은 evaluation |
| depth | raw float32 EXR, nearest-surface distance meters, non-color | DOF/motion blur off; invalid/background 별도 validity mask |
| mask | PNG8 grayscale per entity, white=selected/black=background | Cryptomatte extraction 또는 capability-tested isolated layer; hash→entity map |
| pose | existing evaluated joints의 JSON per frame + optional OpenPose-style PNG | incoming joint map으로 screen projection; rig/animation 재생성 없음 |
| first_frame | cut 시작 beauty의 exact copy PNG | handles 제외 `source.start` |
| last_frame | cut 마지막 beauty의 exact copy PNG | `source.start+duration-1`; exclusive end를 렌더하지 않음 |
| camera_metadata | JSON per frame | world matrix 4×4 row-major, meters/Z up, local -Z forward/+Y up, lens/sensor/fit/shift/clip/focus, evaluated frame |

Depth는 Blender native depth의 surface-distance 의미를 따른다. [Passes](https://docs.blender.org/manual/en/latest/render/layers/passes.html) (latest는 열람 시 5.2 LTS; 5.0 대응 [manual](https://docs.blender.org/manual/zh-hans/5.0/render/layers/passes.html)도 확인). 엔진별 pass/transparent/toon shader 차이가 있으므로 installed build로 다시 검증한다. depth를 선형 camera-Z라고 가정하지 않으며 단위·ray-distance 표현을 index에 기록한다. depth/mask는 blur/DOF 없는 별도 control render에서 camera/geometry를 공유한다. beauty와 pixel coverage가 의도적으로 달라지는 blur/transparency 사례를 evidence에 설명한다.

정규화 control depth 파생안: sequence 고정 `near_m`, `far_m`에 대해 `v=1-clamp((d-near)/(far-near),0,1)` (가까움 white), invalid=0; raw EXR+validity 보존. per-frame min/max normalize를 금지하여 temporal pumping을 방지한다. 특정 model의 기대 polarity/representation은 graph별 확인하고 `depth_mapping.json`으로 기록. model이 camera-Z를 요구하면 explicit 변환한다.

Mask는 color-ID 이미지의 색상 유사도 threshold로 얻지 않는다. Cryptomatte를 사용할 경우 실제 support를 확인하고 matte를 PNG로 추출한다. hair transparency/outline/eye whites를 foreground와 일치시킬지 entity policy에 명시한다. unavailable pass를 빈 black file로 성공 처리하지 않는다.

Pose JSON: source frame, entity ID, joint_map_id, world meter xyz, normalized raster xy (x right/y down), visibility/occlusion, confidence/nullability, camera revision. body/hand/face joint가 없으면 missing joint 목록. synthetic anime rig와 OpenPose topology는 같지 않으므로 upstream map 없이는 automatic conversion 금지. JSON만 available이어도 OpenPose control PNG ready로 표시하지 않는다. projection/rasterizer adapter는 R2로 남긴다.

Camera metadata는 target/preset만 저장하지 않고 evaluated per-frame matrix를 저장한다. 렌즈 애니메이션/shift, render resolution, pixel aspect, sensor fit과 camera object scale도 검사한다. engine target이 없으면 Blender-native conventions만 납품한다.

Optional review derivatives: `previz.mp4`, `beauty.mp4`, `clay.mp4`, normalized `depth.mp4`, `normal.mp4`, `mask.mp4`, `pose.mp4`, `edge.mp4`, `silhouette.mp4`; endpoints PNG, `camera.json`, `shot_manifest.json`. normal은 non-color XYZ 의미/space와 display mapping을 명시하고 edge/silhouette는 pose/geometry source에서 파생한다. MP4는 review/model-specific 파생물이며 raw metric depth EXR/pose JSON/mask 원본을 대체하지 않는다. frame range/fps/resolution/camera movement/lens/sensor/focus distance/DOF(enabled,fstop,focus target)는 camera sidecar에 보존한다.

## PR #4 compatibility audit boundary

Read-only source head `7c3d13af850ec152579183ad6bbde39515ba0f64`, report `research/blender-previz/REPORT.md`. 그 보고서의 depth는 **camera-space Z shader + display-encoded grayscale PNG**이며 본 설계의 native surface-distance float EXR과 다르다. 단위/representation/polarity/gamma를 sidecar로 구분하고 같은 depth라고 바로 교환하지 않는다. 그 PoC는81 frames/16fps=5.0625s, 새 benchmarks는24fps; endpoint간 시간과 encoded duration도 구별한다. target backend graph의 `ref_image`는 first-frame anchor를 뜻하지 않으므로 first-frame 보장으로 승격하지 않는다. 이 세 mismatch를 R2 compatibility audit로 남기며 exporter/Comfy graph를 수정하지 않는다.

## Comfy workflow 비교 (local / optional)

| Candidate | Handoff | Strength to test | 제한 / R2 선택 |
|---|---|---|---|
| Wan2.2 TI2V 5B native | first beauty + prompt | 상대적으로 작은 local I2V baseline | endpoint/camera path control 약함; installed weights 있으면 첫 후보 |
| Wan2.2 A14B I2V native | first beauty + locked identity/scene prompt | appearance proof | 중간/끝 identity drift 및 motion hallucination 평가 |
| Wan2.2 14B FLF2V native | first + last beauty | endpoint composition bridge | 두 endpoint 사이 경로나 exact pose를 보장하지 않음 |
| Wan2.2 Fun Control FP8 | first beauty + preprocessed pose/depth/edge control video | previz trajectory/pose에 대한 adherence | map/encoding 검증 필요, mask는 universal native 입력으로 가정하지 않음 |
| Fun Control + optional 4-step LoRA | 같은 control, matching expert LoRA | bounded proof의 속도/quality A/B | dynamics 손실 가능, 장비별 memory 재검증 |

공식 Comfy 문서는 5B/I2V/FLF2V native template와 `WanFirstLastFrameToVideo`를 설명한다. FLF2V는 I2V weights를 사용하는 Comfy workflow이며 별도 official Wan2.2 FLF2V checkpoint가 있다는 뜻은 아니다. 5B에 대해 문서는 native offloading의 8GB VRAM 가능성을 제시하지만 이 workstation에서 검증하지 않았다. [Wan2.2 native workflows](https://docs.comfy.org/tutorials/video/wan/wan2_2).

Fun Control 공식 예시는 preprocessed pose video와 start image, high/low-noise FP8 weights를 사용하며 optional matching 4-step LoRA를 제공한다. 지원 control 후보는 pose/depth/edge 등이며 exact graph 조합은 template revision으로 검사한다. built-in Canny 이외 preprocessing은 추가 도구가 필요할 수 있다. acceleration은 dynamics tradeoff가 있다. [Fun Control](https://docs.comfy.org/tutorials/video/wan/wan2-2-fun-control).

이들은 유료 provider 호출 없이 local 실행 가능한 후보라는 의미다. 무료 다운로드가 GPU/전력/라이선스 준수 비용이 없음을 뜻하지 않는다. Comfy Cloud/partner nodes는 사용하지 않는다. GGUF/WanVideoWrapper는 추가 custom-node 의존성 때문에 R1 recommended baseline에서 제외; 필요 시 R2 pin/license/node audit 후 별도 비교한다.

## Handoff protocol와 proof gate

1. approved manifest/export index/reference scope를 확인. workflow JSON와 node/model filename/hash/license/source revision을 기록하며 missing model이면 `NOT_RUN_MISSING_WEIGHTS`로 종료한다. auto-download 하지 않는다.
2. first/last PNG는 view-baked sRGB, control은 non-color 파생물로 전달. conditioning frames와 prompt의 shot/character/set ID를 일치시킨다. depth/pose는 영상 전체가 같은 fps/resolution/time mapping을 가진다.
3. mode별 하나의 2s proof 구간만 선택, installed local 모델이 허용하는 width/height/frame-count constraints를 먼저 확인. model fps와 edit fps가 다르면 source/edit mapping sidecar를 쓰고 임의 duration reinterpretation을 금지한다. R1 preset fps=24가 model native fps를 의미하지 않는다.
4. R2 bounded run 제안: 총 wall-time 120s cap, 1 candidate/seed, local resource cap; 실패 시 중단. 해당 장비에서 이를 만족하지 않으면 still/Blender-only proof로 종료. 긴 generation으로 자동 확대하지 않는다.
5. Blender start/mid/end + generated 동일 대응 frame을 side-by-side 검사. identity(얼굴/hair/outfit/눈), silhouette/prop state, screen direction, camera motion, pose/joint, endpoints, temporal flicker를 보고한다. exact equivalence를 주장하지 않는다.
6. 결과는 `proof/<shot_id>/<take>/`에 graph/prompt/seed/output hash/time mapping/comparison/reviewer decision으로 저장. accepted proof도 manifest나 original animation을 자동 덮어쓰지 않는다.

I2V/FLF2V는 geometry/animation 입력을 이미지로만 전달한다. Fun Control도 constraint fidelity를 보장하지 않는다. failed proof의 수정은 control encoding/shot framing/prompt를 좁게 바꾸거나 Blender route로 반환하며 캐릭터 asset/animation 재제작 연구를 시작하지 않는다.
