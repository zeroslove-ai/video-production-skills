---
name: video-production-qa
description: Verify non-trivial AI-assisted video and Blender outputs using structured state, representative frames, render metadata, timing, audio, continuity, and reproducibility evidence. Use before final delivery or after a material video/3D revision; do not use as a substitute for building the artifact.
---

# Video Production QA

Verify evidence, not confidence.

## Gate order

1. Source gate — authoritative inputs and intended revision are identified.
2. Structural gate — scene/composition/frame range/settings are internally consistent.
3. Motion gate — sample important frames and transitions; check discontinuities, clipping, camera jumps, scale changes, ground contact, and timing.
4. Visual gate — inspect representative rendered frames/contact sheet at the intended aspect ratio.
5. Audio gate — confirm expected tracks exist, duration is aligned, speech/music levels are reasonable, and there is no unintended silence or clipping.
6. Delivery gate — verify final duration, dimensions, fps, container/codec when relevant, and file opens/plays through the end.
7. Reproducibility gate — identify the source revision, scripts/project files, and known limitations.

## Blender-specific rule

Do not pass a Blender scene only because a screenshot looks right. Inspect object/scene/animation/render state and sample the frames that matter, then use screenshots or renders as visual confirmation.

## Failure handling

When a gate fails, report the smallest reproducible failure, affected stage, evidence, and next bounded fix. Do not hide a failed gate behind an overall qualitative judgement.

## Completion record

Append the final test to `EXPERIMENT_LOG.md` when this skillstack itself is being evaluated or changed. Record date, environment/tool versions, task, result, failure mode, and the skill change implied by the evidence.
