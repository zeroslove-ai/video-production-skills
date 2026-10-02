# Editorial pipeline R1

2026-10-02 · 설계. Blender VSE를 shot assembly/animatic의 첫 경로로 사용하고, 최종 encode는 기존 FFmpeg/Remotion 경로를 재사용한다. 새로운 NLE를 만들지 않는다. 상세 시간 규약과 OTIO mapping은 [architecture](VIDEO_PREPRODUCTION_ARCHITECTURE_R1.md)의 단일 계약을 따른다.

## VSE 운영

Edit Scene의 V1은 순서가 정해진 SceneStrip/proxy shot과 explicit gap. speech/ambience/music은 독립 audio track role이며 source trim과 timeline placement를 분리한다. GP/text review overlay는 clean proxy와 분리한다. source shot Scene에는 Edit Scene을 참조하지 않는다. 수동 edit은 VSE snapshot→manifest diff→approved revision으로 반영하며 stale manifest를 자동 overwrite하지 않는다.

Animatic review: shot duration, cue onset/end, reaction pause, reveal frame, camera-motion settle, 전체 pacing을 확인한다. 말하는 인물에만 자동 cut하지 않는다. audio cue sheet의 semantic turn과 beat/hold range를 사용한다. shot/reverse coverage는 같은 action axis, 반대 eyeline, matching-action source continuity, prop 상태를 같이 검토한다.

| 대상 | R1 정책 | R2 구현/검증 |
|---|---|---|
| Shot ordering/clip trim | single V1, straight cuts, integer frames | 동일 shot ID/order/source range round-trip |
| Gap | manifest explicit range + reason | 비선언 gap/overlap 거부 |
| Transitions | cut baseline; dissolve/wipe는 research/loss matrix만 | handles 확보 후 effect capability/bake 검증 |
| Markers | sequence frame + stable event ID | OTIO Marker와 event sidecar, frame drift 확인 |
| Dialogue | independent role=dialogue audio clips | J/L-cut; 실제 voice waveform/sync 검사 |
| Ambience/music | independent role, gain_db | loops/ducking은 baked mix + loss report 또는 future envelope 계약 |
| Subtitle | timed cues와 language를 optional schema에 기록 | SRT/VTT sidecar; VSE text styling은 bake/loss report |
| Metadata | shot/preset/reference/asset revision sidecar | namespaced metadata 보존, adapter별 loss report |
| Editorial exchange | native `.otio` + proxy URI + manifest | target editor 1개에서 relink 실제 검증 |

R1 schema에 complex transitions나 retime curve를 억지로 encode하지 않는다. 지원하지 않는 데이터를 발견하면 보고하거나 bake하며 fidelity를 주장하지 않는다. transition은 adjacent handles와 timing 의미가 검증된 다음 schema revision으로 추가한다.

## OTIO 사용 가능성

OTIO는 frame-addressed editorial structure와 media references를 교환하기 적합하다. `.blend` scene/camera/material/animation graph 교환은 manifest/export sidecar 책임이다. 공식 core/native adapter와 optional plugin format을 구분하며 Blender bridge는 custom R2 구현으로 남긴다. [OTIO adapters](https://opentimelineio.readthedocs.io/en/latest/tutorials/adapters.html).

OTIO 파일은 직접 JSON serializer를 새로 만들지 않고 official library로 read/write한다. 사용자 metadata는 `video_preproduction` namespace에 넣는다. [File format specification](https://opentimelineio.readthedocs.io/en/latest/tutorials/otio-file-format-specification.html). source/parent time 좌표와 handles 변환은 [time ranges](https://opentimelineio.readthedocs.io/en/latest/tutorials/time-ranges.html)에 따른다.

Export package: sequence manifest/hash, shot manifests/hash, relative proxy paths, `.otio`, audio/subtitle sidecars, `loss_report.json`, optional burned-in review mp4. loss report는 feature/location/source representation/target representation/action(kept/baked/dropped)/reason을 기록한다. unknown media는 MissingReference와 missing report를 사용하며 asset substitution을 하지 않는다.

## 게임 cinematic ↔ gameplay 카메라

Gameplay return event에 character world transform, active animation sample/time, camera world matrix와 FOV semantics, lens/sensor/shift, focus/DOF, target engine unit/axis/aspect를 저장한다. end anchor가 없으면 handoff는 pending이다. Blender camera를 엔진에 바로 적용한다고 가정하지 않는다.

R2 선택지: hard cut on matched frame, 12–24-frame eased camera blend, motivated occlusion cut. destination camera가 gameplay logic으로 움직이면 endpoint뿐 아니라 blend 시간의 target samples도 받아야 한다. position lerp + quaternion interpolation + FOV interpolation을 후보로 삼고 collision/near clipping/subject framing을 프레임별 검사한다. 롤·DOF·exposure pop와 screen direction 변화도 QA. control handback 순간 input lock 해제와 event ownership은 engine session 책임이다. skip은 같은 authoritative return-state로 이동해야 한다.

## 수락 기준

SEQ_A/B/C의 order/source/duration/audio/markers/subtitles를 manifest→OTIO→manifest 비교. 24 및 24000/1001 fps, explicit gap, independent dialogue onset을 검증한다. pure OTIO library round-trip와 editor plugin relink는 별도 gate다. artifact references와 missing/loss report를 함께 검토하고 실제 플레이백 증거 없이 editorial-ready라고 하지 않는다.
