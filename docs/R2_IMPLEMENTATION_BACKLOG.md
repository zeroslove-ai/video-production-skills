# R2 implementation backlog

2026-10-02 · PM review. R1 effort 중심: cinematography/reference/shot design 약 70%, Blender/editorial architecture 약 20%, future PR #4 handoff 약 10%. 실제 시간 측정값이 아닌 우선순위 배분이다.

| Priority | Work / input | Acceptance evidence |
|---|---|---|
| P0-A | approved adult Yuri asset + compatible body/facial clips + landmarks + small room/phone | immutable hash/revision/binding, clip events, root policy; missing capability upstream 요청 |
| P0-B | visual atlas: CU/MCU, 65/75/85mm, eye/three-quarter, soft key/window | cheap reference frames와 eye/face 별도 art decision; lens/distance perspective 비교 |
| P0-C | reference cards→preset calibration, candidate framing evaluator | negative crop/eye/foreground 사례 거부, emotion-specific ranked candidates |
| P0-D | 기존 workstation gates와 installed build/API capability pin | skill discovery, bounded MCP read/write/read/visual evidence; 기존 운영 절차 재사용 |
| P0-E | manifest→proxy scene/camera rehearsal/GP annotation/VSE prototype | SEQ_A 5 shots low-res panels/animatic, manual drawing 없음; idempotent owned state |
| P1-A | SEQ_B coverage/eyeline/axis/audio prototype | 12 planned shots, reaction/J/L-cut/voice timing, contact sheet+cue review |
| P1-B | editorial semantic validation + optional OTIO bridge | ID/order/range/audio/markers/subtitles, 24000/1001/gap round-trip + editor relink |
| P1-C | SEQ_C gameplay return rehearsal | 8 shots, cinematic/target camera samples, collision/focus/exposure/axis handback |
| P1-D | existing PR #4 export contract compatibility audit | manifest version/frame/fps/color/depth/camera mismatches listed; no new provider adapter |
| P2 | after separate approval, reuse existing backend proof route | installed local models only, single-shot visual adherence comparison; optional stage |

## Automation roadmap

Immediately formalizable: story beat/coverage proposals, preset selection, lens recommendation, shot/sequence manifest, contact sheet layout, checklists and reference retrieval. R1 provides design data only.

R2 Blender automation: automatic character framing/eye look target/headroom/thirds, focus target, camera placement/motion/collision sampling, preset lighting, automatic storyboard panels, cheap previz, VSE assembly/audio markers, evidence capture. Look target moves camera or selects compatible authored gaze clip; it does not procedurally rebuild facial/body performance. Physical contacts/root motion remain incoming asset QA.

Human operation reduction: approve golden examples once, reuse bounded rules/presets/visual ranking, route only ambiguous mismatch or intentional exceptions to art review. Do not promise fully automatic aesthetic correctness. emotion recognition from a supplied clip and uncalibrated image scores require validation before autonomous final approval.

## PR #4 relationship and non-goals

[Draft PR #4](https://github.com/zeroslove-ai/video-production-skills/pull/4), source head observed `7c3d13af850ec152579183ad6bbde39515ba0f64`, is preserved as a backend experiment. Its reported background render/RGB-depth export/manifest/first-last/FFmpeg/hash/ffprobe evidence is reference material, not execution performed in this branch. Actual generation remains partial in its report. New R1 branches from latest main `29f9431`; no PR #4 code is copied, rewritten or merged. No provider comparison, paid API call, API adapter or Comfy runtime expansion in this backlog's P0/P1.

## PM next decision

Approve benchmark story/coverage and art reviewer; assign upstream asset/clip owner; approve P0-A/B/C visual calibration before scene automation. Runtime dependencies missing are future implementation prerequisites, not R1 design blockers. PR remains Draft until PM review; main integration is a separate approval.
