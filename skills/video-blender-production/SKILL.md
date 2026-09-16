---
name: video-blender-production
description: Build, modify, animate, light, render, and debug Blender scenes for AI-assisted video production using a hybrid of live MCP control and saved bpy Python. Use when Codex needs reproducible Blender scene work, camera/lighting/material animation, render iteration, or long-running 3D production with checkpoints and evidence.
---

# Video Blender Production

Use Blender MCP as a live instrument and saved Python as durable production source.

## Before mutation

1. Confirm the intended `.blend` file, scene, frame range, render engine, resolution, fps, and output path.
2. Inspect current scene state before changing it: objects, collections, active camera, transforms, materials, modifiers, animation, render settings, and relevant dependencies.
3. Save or verify a checkpoint before destructive/high-volume changes.

## Hybrid control rule

Use MCP for:

- scene inspection and API/documentation lookup;
- targeted live corrections;
- small experiments;
- screenshots/viewport/render inspection;
- verifying the result of scripts.

Use saved `bpy` Python for:

- geometry or hierarchy construction;
- repeatable material/node setup;
- camera and light rigs;
- keyframes and procedural animation;
- batch operations;
- deterministic render configuration.

If a live MCP edit becomes structurally important, back-port it into the saved source or record it explicitly so the scene remains reproducible.

## Production loop

For each meaningful stage:

1. Inspect structured state.
2. Make one bounded change.
3. Re-inspect the affected state.
4. Render or capture visual evidence when the change is visual.
5. Compare against the production brief/reference.
6. Save a checkpoint only after the stage passes.

Do not judge animation, transforms, camera continuity, scale, ground contact, or object state from screenshots alone. Query Blender state and sample relevant frames first; use images as confirmation.

## Long-running work

Break work into resumable stages such as blockout → lookdev → camera → animation → lighting → final render. Record frame ranges, output paths, script revisions, and unresolved issues after each stage.

Keep one writer for the live Blender scene. Multiple review/research agents may inspect artifacts, but they must not concurrently mutate the same live scene.

## Rendering

Prefer preview renders before expensive final renders. Validate a representative low-cost frame/sample set before launching the full frame range. Preserve render settings in source or documented scene state.

If a renderer, MCP bridge, or Blender process fails, recover from the last checkpoint; do not rebuild from memory when source/checkpoints exist.

## Safety

Treat Blender MCP execution as unsandboxed code execution inside the Blender process. Use a workspace without unrelated sensitive data and avoid granting unnecessary filesystem/network scope.
