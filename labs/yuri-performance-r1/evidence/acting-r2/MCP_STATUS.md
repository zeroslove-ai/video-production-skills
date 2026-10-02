# Live MCP evidence

2026-10-02. Initial get_addon_status and get_scene_info: could not connect. No settings or addon updates were made to solve that failure.

An owned research Blender GUI process was then launched with the R2 .blend and `start_research_live.py`. Existing installed community addon was enabled and localhost server started in that process; no preferences were saved. Subsequent get_addon_status: Blender 5.2.1 LTS, native protocol 7 vs expected 13, existing telemetry consent=true (unchanged), no premium generators. Basic scene query returned 52 objects. Native execute_code returned actual sampled head Euler, wrist world positions and pupil location curves. Viewport screenshot confirmed the proxy. These are basic-path successes, not certification of every modern server capability.

Live face_close camera distance was corrected and back-ported into saved authoring source. A later scene re-open cleared transient GUI context: `bpy.context.screen` was None in the MCP handler. The failed call had already reopened the file and bound the shy actions before the exception. Recovery used `bpy.context.window_manager.windows` → `window.screen.areas` and did not repeat the preceding mutation. get_viewport_screenshot and get_scene_info then succeeded. Lesson: context in a timer/socket handler differs from interactive operator context; do not assume screen/area exists.

MCP mutations only targeted the owned `yuri-motion-previs-lab-r1` scene. No product/laptop Blender scene, shared MCP settings or addon file was modified. The live correction is reproducible in the saved bpy source; the GUI state is a disposable audition, not the canonical saved action selection.
