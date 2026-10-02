# VIDEO_PREVIZ_CINEMATOGRAPHY_R1 — PM review

2026-10-02 · R1 design checkpoint · branch `research/previz-cinematography-r1`.
Base: latest fetched main `29f943115c269d64d651bd641a4718b53236be00`.
HEAD/별도 Draft PR URL은 Git/완료 보고에서 확인한다. PR #4와 혼합하거나 merge하지 않는다.

## Core architecture

Idea/Script → Story Beat → Visual Reference → Shot Design/Cinematography → Storyboard → Blender Previz → Animatic → Editorial Approval → Final Blender Production 또는 existing PR #4 style handoff → Final Edit.

이번 R1은70% visual direction/cinematography/reference,20% Blender/editorial architecture,10% future handoff를 우선한다. 완성된 adult female/Yuri 캐릭터와 compatible body/facial animation/environment/prop을 입력받아 촬영/컷/연결을 결정한다. rig/topology/skin weighting/ARKit/viseme/body-facial motion/retarget를 연구하거나 구현하지 않는다.

## Deliverables and findings

| 문서 / data | PM가 검토할 결과 |
|---|---|
| [Architecture](VIDEO_PREPRODUCTION_ARCHITECTURE_R1.md) | native Blender virtual camera rehearsal, no mandatory hand drawing, state/ownership gates |
| [Cinematography bible](CINEMATOGRAPHY_BIBLE_STYLIZED_FEMALE_R1.md) |16 감정별 촬영 지침,15 appeal recipes, lens-distance/perspective/depth/eyeline/cut reasoning |
| [Reference system](VISUAL_REFERENCE_SYSTEM_R1.md) / [3 observed cards](../references/README.md) | observation과 estimate/proposed adaptation 분리, provenance/권한/approval와 taxonomy |
| [Lighting bible](LIGHTING_BIBLE_STYLIZED_CHARACTER_R1.md) |10 named looks, eye catchlight와 face readability 독립 QA |
| [Editorial language](EDITORIAL_LANGUAGE_R1.md) / [pipeline](EDITORIAL_PIPELINE_R1.md) | coverage/continuity/J-L-cut/pacing, VSE/OTIO loss contract |
| [Mode blueprint](WEB_DRAMA_CUTSCENE_BLUEPRINT_R1.md) |3 mode, story beats/assets/shot list/framing/light/timing |
| [Future handoff](COMFY_PREVIZ_HANDOFF_R1.md) | existing backend와 depth/time/ref-image semantic mismatch audit |
| [R2 backlog](R2_IMPLEMENTATION_BACKLOG.md) | visual atlas/reference calibration 먼저, prototype 나중 |
| [Fixtures](../examples/previz/README.md) / [validation](VIDEO_PREVIZ_VALIDATION_R1.md) |3 sequences/25 shot designs, schema1.1.0, validator evidence |

Camera data:36 presets=13 generic + 지정된23 emotion/coverage recipes. 각 recipe는 lens range, eye-relative height, pitch/yaw, subject/headroom/DOF, motion/speed, emotion, recommended light/duration을 기록한다. Lighting data:15 looks=5 generic+10 named recipes. Shot templates25, production modes3. 수치는 초기 design hypothesis이며 rendered artistic acceptance를 주장하지 않는다.

## Skill architecture

Existing director: mode/reference/manifest freeze와 preproduction gates. Existing Blender: durable manifest 실행 entry/scene-state/export audit. Existing QA: shot continuity, independent eye/face gates, pass alignment/OTIO loss/identity evidence.

별도 `video-storyboard-previz`와 `video-cinematography`를 제안한다. 둘 다 반복 가능한 독립 단계이며 다른 캐릭터 프로젝트로 재사용되고 기존 skill 비대화를 줄인다. `video-editorial`은 초기에는 previz reference module로 두고 실제 exchange 반복이 확인되면 분리한다. reference bible은 cinematography module로 묶어 추가 skill을 남발하지 않는다. INSTALL의 중앙 skill 정본을 따라 R2 변경 후 snapshots 동기화. 이번에는 기존 skills/README/MCP/workstation 설정을 수정하지 않았다.

## Automation vs artistic judgment

자동화 후보: beat/shot/coverage 제안, camera/lens 후보, character fit/eye target/headroom/thirds/focus, camera blocking/collision sampling, light preset, automatic board/cheap previz, VSE assembly/contact sheet, schema/state/visual QA. body/facial action은 공급 clip selection/placement/timing이며 재제작이 아니다.

사람 판단: subtext/appeal, clip performance, look key, silence/reaction timing, deliberate asymmetry/axis break. 대체 방식: approved positive/negative cards와 golden atlas, emotion별 scoring weights/rules/preset tolerance, visual candidate 비교, 좁은 exception/reviewer decision. 미적 점수 하나로 자동 final 승인하지 않는다.

## Benchmarks

| Benchmark | Duration / coverage | Required upstream inputs |
|---|---|---|
| SEQ_A CUTE_ROOM |12s/5: phone context→message insert→smileCU→slow push→eye-contact hold | Yuri/body-phone/facial-phone, bed-room/phone/message, eye/hand anchors |
| SEQ_B DIALOGUE |30s/12: establish/master/two-shot/A-B medium/OTS/CU/reaction/insert/ending | A/B assets+720f body/facial clips, café/note, script/48kHz voice/cues |
| SEQ_C GAME_REVEAL |18s/8: environment→entrance→heroMS→dialogue→reaction→action→heroCU→gameplay | character+432f authored-root/facial clips, gate/beacon, destination/engine camera/return anchors |

## PR #4 relationship / evidence limits

[PR #4](https://github.com/zeroslove-ai/video-production-skills/pull/4)는 OPEN/Draft, head `7c3d13af850ec152579183ad6bbde39515ba0f64`로 확인했다. Report/evidence를 read-only reference로 사용했다. Background render/RGB-depth/first-last/manifest/FFmpeg/hash/ffprobe는 backend 가능성을 보여주지만 이 branch에서 재실행한 증거가 아니다. 본 R1은 그 앞단의 촬영/edit 지식을 구조화한다. Depth의 camera-Z/display encoding,16fps/81f와 새24fps의 차이, ref_image가 first-frame 보장이 아닌 점을 R2 audit에 남긴다. PR #4의 code/state를 변경하지 않는다.

Blockers: R1 design의 blocking issue는 없다. Actual media/reference approval, installed runtime readiness, engine anchors는 R2 prerequisites다. Schema/semantic validation은 render/Comfy/OTIO 실행 검증을 뜻하지 않는다. 새API adapter/Comfy implementation/model download/GPU render/유료call은 수행하지 않는다.

Next recommended action: PM이 beat/coverage/length와 P0 visual atlas 계획을 검토하고 asset owner/art reviewer를 지정한다. approved Yuri look/reference calibration 후 bounded SEQ_A prototype으로 진행한다. 이 PR은 Draft로 유지하며 main 반영은 별도 PM 승인 후 진행한다.
