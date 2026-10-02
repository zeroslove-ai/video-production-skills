# Workflow skeletons

`wan22_fun_control.api.json` is an authored ComfyUI **API prompt graph**, not UI canvas JSON.
`pipeline.py comfy` binds typed `$variables`. It feeds pre-rendered depth directly into
`Wan22FunControlToVideo`; first.png feeds **ref_image**, not a first-frame anchor.
The inspected schema exposes ref_image/control_video and does not expose start_image,
even though its Python execute signature contains start_image. Follow the schema.
Do not apply Canny/DWPose to an already prepared depth/pose video.
The no-LoRA, two-stage sampler is based on inspecting the official template at
`Comfy-Org/workflow_templates@9fac9ca259773c82c25553103edd51b6550d5fc4`,
`templates/video_wan2_2_14B_fun_control.json` (MIT). No upstream files are vendored.

Before submission `/object_info` checks node presence, required inputs and model enum availability.
This is a compatibility check, not proof of adequate VRAM, connected output types, or visual quality.
The script then uploads first.png and depth.mp4 to a shot-specific input folder, queues once,
and records prompt_id. Inspect `/history/{prompt_id}` separately; submission is not completion.

Variants to build in the installed UI, then export **API format**:

- Start/end: official `video_wan2_2_14B_fun_inpaint.json`; use matching Fun Inp high/low
  weights and `WanFunInpaintToVideo(start_image, end_image)`. Do not just swap a node into
  this Control graph while retaining Control weights.
- Character movement: `video_wan2_2_14B_animate.json`; reference image + pose/face video.
  DWPose and KJNodes version compatibility needs an independent gate.
- Camera: `video_wan2_2_14B_fun_camera.json`; convert Blender camera matrices into the
  model's expected camera convention; raw Blender matrices are not drop-in controls.
- VACE: source-video/mask/reference-image adapter needs a matching VACE checkpoint;
  image-to-video checkpoints do not accept arbitrary video conditioning.

For pose, replace control_video with a separately validated OpenPose-style sequence
rendered from a named rig, with correct joint order, colors, camera projection and occlusion.
The cube exporter deliberately has no human rig and produces **no pose control**.
