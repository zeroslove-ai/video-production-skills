---
name: video-production-director
description: Orchestrate end-to-end AI-assisted video production when Codex must turn an idea, reference, storyboard, product demo, or visual brief into a reproducible video pipeline involving research, Blender/3D, Remotion, FFmpeg, assets, rendering, and QA. Use for multi-stage video production and iteration; do not trigger for a single trivial media conversion.
---

# Video Production Director

Treat the video as a production pipeline, not a single prompt.

## Core workflow

1. Define the deliverable: duration, aspect ratio, resolution, fps, audience, style, hard constraints, and available source assets.
2. Research before building when the visual language, technical method, or assets are uncertain. Record only decisions that change production.
3. Write a compact production brief containing:
   - shot/scene list and timings;
   - style/look lock;
   - asset plan and provenance;
   - tool route per shot;
   - audio/caption plan;
   - measurable acceptance gates.
4. Choose the lightest valid production route:
   - Remotion/2D composition for UI, typography, stills, charts, or motion graphics;
   - Blender for real 3D camera/lighting/material/spatial work;
   - hybrid for 3D hero footage plus 2D overlays/editing;
   - FFmpeg for deterministic transcode, mux, trim, loudness, or contact sheets.
5. For Blender work, read `../video-blender-production/SKILL.md` and follow its inspect → mutate → verify loop.
6. Keep each long-running stage checkpointable. Save source, intermediate renders, commands/scripts, and the acceptance evidence needed to resume.
7. Run QA before declaring completion. Read `../video-production-qa/SKILL.md` for non-trivial work.

## Context discipline

Separate research/planning from the heavy build when the research context becomes large. Hand the build agent the production brief, authoritative assets, constraints, and acceptance gates rather than the entire exploratory transcript.

## Change discipline

Prefer source-driven changes over manual one-off edits. If a visual fix can be expressed in a reusable Blender Python, Remotion component, or FFmpeg command, preserve that source.

Do not silently substitute authoritative user assets, characters, logos, or reference images.

## Completion evidence

For a normal video task, retain at least:

- final render metadata: duration, dimensions, fps, codec/container when relevant;
- scene/shot coverage check;
- representative frames or contact sheet;
- audio presence/sync check when audio exists;
- known limitations;
- exact source revision or scripts sufficient to reproduce the output.
