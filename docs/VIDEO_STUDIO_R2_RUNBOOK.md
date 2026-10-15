# Video Studio R2 — Workstation run

Updated: 2026-10-15

## Scope

Work was isolated on branch `work/video-studio-r2` in the video-production repository. The Yuri Unity checkout and its current branch were not changed. The installed ComfyUI was inspected read-only. The successful generation used a separate server on `127.0.0.1:8190` with separate user/output folders and custom nodes disabled.

## Verified workstation

- ComfyUI `0.34.6`, embedded Python `3.12.10`, PyTorch `2.10.0+cu130`, CUDA `13.0`, RTX 4080 SUPER with 16 GB VRAM, 64 GB system RAM.
- The LTX 2.5 distilled INT8 transformer and Gemma INT8 encoder together exceed available VRAM, so substantial weights were offloaded to system RAM.
- No LTX Layout-to-Render IC-LoRA or matching latent upscaler was installed. The official IC-LoRA repository is gated; it was not accessed or downloaded.
- The repository contains no Yuri humanoid rig. The Blender scene below is an editable proxy made from simple meshes and animated pivots.

## Local LTX image-to-video

- MP4: `D:\AI\LTX25-R3\output\video-studio-r2\greeting_wave_20261015\greeting_wave.mp4`
- 448×768, 24 FPS, 73 frames, 3.0417 s, H.264; 602,495 bytes.
- LTX 2.5 22B distilled INT8 ConvRot transformer; Gemma 4 12B INT8 ConvRot encoder; BF16 video/audio VAEs; 8 steps, CFG 1, seed `20261015`, no LoRA.
- ComfyUI history reported success. Generation took 416.07 s including cold model initialization. Peak sampled VRAM was 15,676 MiB of 16,376 MiB across 135 samples. `nvidia-smi` utilization reached 98% during inference.
- RAM observation during the same run: about 39 GiB working set for the ComfyUI Python process, about 4.9 GiB system RAM free, and 82.6/133.1 GiB committed. The captured Task Manager row showed about 37,060 MB for the app group and `GPU 0 - 3D`; this is a point-in-time graphics-engine field, not a CUDA measurement. After the isolated server stopped, free RAM returned to about 43.6 GiB, committed memory to 29.7 GiB, and GPU memory to 656 MiB.
- Visual review: partial pass. The face, outfit and background mostly hold; a blink, soft smile and greeting-hand lift are visible. The hand movement is weak for much of the clip and shows a bright fringe near the end.
- `workflow.json`, `history.json`, `metrics.json`, `keyframes_start_mid_end.png`, and `motion_review_sheet.png` are alongside the MP4. The source image path is not copied into the report.

## Blender motion guide

Blender `5.2.1 LTS` rendered an editable 448×768, 24 FPS, 73-frame greeting-wave proxy. The `.blend`, start/peak/end frame stills, MP4 and `blender_metrics.json` are in:

`D:\AI\LTX25-R3\output\video-studio-r2\blender_previs\`

Shoulder/elbow pivots, brief eye blinks and subtle torso bobbing are keyed. This is previs only, not a Yuri rig, humanoid Action, FBX or BVH.

## Higgsfield Genjutsu motion transfer

One free `hf_mult_motion_control` generation completed at 720p. The four-second 512×878 H.264 guide and avatar reference image were uploaded as the two inputs. The estimate returned 0 credits with both media roles present; the account remained at 8.6 paid credits and its free-motion counter is now 0. No free trial was started.

- MP4: `D:\AI\LTX25-R3\output\video-studio-r2\higgsfield_genjutsu\higgsfield_motion_transfer.mp4`
- 720×1280, 24 FPS, 97 frames, 4.0417 s, H.264; 3,695,167 bytes.
- Review frames: `start.png`, `middle.png`, `end.png`; full metadata and SHA-256 are in `higgsfield_metrics.json`.
- Visual review: one character, face, outfit and portrait composition remain recognizable. The arm rises and holds; the output does not show a clear wrist-wave cycle or return to idle. Treat it as a partial motion-transfer result.

## Remaining gates

1. Do not label the local route Blender-to-ComfyUI V2V: the successful ComfyUI run was I2V from a still. Local Layout-to-Render remains blocked by the missing/gated IC-LoRA and upscaler.
2. Compare the local I2V and free Genjutsu results as separate candidates; both need improved wave articulation for the greeting loop.
3. Use the actual avatar humanoid rig before attempting a reusable Blender Action or FBX/BVH retarget. No motion-capture extraction ran in this slice.
4. Keep LoRA catalogue/download automation and local motion-estimation setup as later work. No model, LoRA, custom node or trial was added or changed here.

See `previs/adapters/comfyui/CONVENTIONS.md` and `EXPERIMENT_LOG.md` for run-record rules and hashes.
