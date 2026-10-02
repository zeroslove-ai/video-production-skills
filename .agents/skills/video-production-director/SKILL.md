---
name: video-production-director
description: Orchestrate end-to-end AI-assisted video production when Codex must turn an idea, reference, storyboard, product demo, or visual brief into a reproducible video pipeline involving research, Blender/3D, Remotion, FFmpeg, assets, rendering, and QA. Use for multi-stage video production and iteration; do not trigger for a single trivial media conversion.
---

# Video Production Director

Treat the video as a production pipeline, not a single prompt.

1. Define duration, aspect ratio, resolution, fps, audience, style, hard constraints, and authoritative assets.
2. Research uncertain visual/technical choices before expensive production.
3. Freeze a compact production brief: shot timings, look, assets/provenance, tool route, audio/captions, measurable gates.
4. Choose the lightest valid route: Remotion/2D, Blender/3D, hybrid, or FFmpeg-only.
5. For Blender work, use the `video-blender-production` skill.
6. When handing Blender previs to ComfyUI or an external video provider, export a **shot manifest package** (`docs/PREVIS_VIDEO_PIPELINE_R1.md`, `previs/schema/shot-manifest.schema.json`) and run adapter dry-run validation before any live generation gate.
7. Keep long stages checkpointable and preserve deterministic source/scripts.
8. Run `video-production-qa` before declaring non-trivial work complete.

Separate exploratory research context from the build handoff. Do not silently substitute authoritative user assets, characters, logos, or references.

Retain final metadata, representative frames/contact sheet, audio/sync checks where relevant, known limitations, and source revisions sufficient to reproduce the output.
