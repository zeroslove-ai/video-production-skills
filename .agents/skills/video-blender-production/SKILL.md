---
name: video-blender-production
description: Build, modify, animate, light, render, and debug Blender scenes for AI-assisted video production using live MCP control plus saved bpy Python. Use for reproducible Blender scene work, animation/render iteration, and checkpointed 3D production.
---

# Video Blender Production

Use Blender MCP as a live instrument and saved Python as durable production source.

Before mutation, confirm the intended blend file, scene, frame range, render engine, resolution/fps, output path, and checkpoint. Inspect structured scene state first.

Use MCP for inspection, targeted live corrections, small experiments, and visual verification. Use saved `bpy` for repeatable geometry/hierarchy, materials/nodes, rigs, keyframes, procedural animation, batch operations, and deterministic render configuration.

For each meaningful stage:
1. inspect state;
2. make one bounded change;
3. re-inspect affected state;
4. render/capture visual evidence when appropriate;
5. compare to the brief/reference;
6. save a checkpoint only after the stage passes.

Do not judge transforms, animation continuity, scale, ground contact, or object state from screenshots alone. Query state/sample frames, then use images as confirmation.

Keep one writer for a live Blender scene. Recover from checkpoints rather than rebuilding from memory. Validate cheap representative renders before expensive full renders.
