# R3 H3 Photoreal T2V Gate — 2026-09-18

## Authority consumed

- Pulled `research/local-video-gen-r0` from origin to commit `3cbac8b7e2e3d2c8d33fc6dc9f65ef322ed3a46d`.
- Read `R3_CODEX_PHOTOREAL_T2V_BRIEF.md`.
- Read `workflows/local_gen/h3_t2v_photoreal_4step.json`.
- Read the latest Issue #2 comment, `R3 corrective action — photoreal T2V`, posted by `zeroslove-ai` on 2026-09-18.

## Graph audit

- Pure T2V: PASS
- `LoadImage` node: absent
- `first_frame`: absent
- `last_frame`: absent
- UNET: `minimax_h3_fl2va_pruned_int8_convrot.safetensors`
- Text encoder: `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`
- Turbo LoRA: `minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors`
- LoRA strength: `1.0`
- Scheduler / steps / sampler: `simple` / `4` / `res_multistep`
- Resolution / frames: `864x480` / `124`
- Audio output: disconnected
- Existing `example.png`: not referenced

## LoRA inventory

The required LoRA was initially missing. Only the official Comfy-Org file was downloaded:

`https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/main/loras/minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors`

- Size: `1,956,192,992` bytes
- SHA-256: `c396a9a06f58399e9df9754b18299818d84a2ddd371724ba48fe4a41221437dc`
- Local path: `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI\models\loras\minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors`

No ComfyUI, Torch, CUDA, Python, driver, or custom-node upgrade was performed.

## Single gate render

- Run: `r3-t2v-photoreal-seed101-20260918`
- Seed: `101`
- Result: technical PASS; exactly one clip generated
- Wall time: `47.711 s`
- Peak VRAM: `15,130 MiB`
- Minimum available RAM: `26.911 GiB`
- Peak used RAM: `34.645 GiB`
- Peak ComfyUI RSS: `16.982 GiB`
- MP4 SHA-256: `75d1896ad731eadeae6a0109dbee568c22e96ae310e19c603522f8b56aae4378`
- ffprobe: H.264, `864x480`, `124` frames, `24 fps`, `5.166667 s`, no audio stream

Output:

`C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI\output\video-production-skills\local-gen-r0\r3-t2v-photoreal-seed101-20260918\result.mp4`

Extracted frames:

- First: `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI\output\video-production-skills\local-gen-r0\r3-t2v-photoreal-seed101-20260918\first-frame.png`
- Middle: `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI\output\video-production-skills\local-gen-r0\r3-t2v-photoreal-seed101-20260918\middle-frame.png`
- Last: `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI\output\video-production-skills\local-gen-r0\r3-t2v-photoreal-seed101-20260918\last-frame.png`

## Visual gate

Photorealism/style: PASS. The first, middle, and last frames show photographic-looking children, realistic skin/hair/clothing, real stage lighting, floor reflections, and live-action camera appearance. They are not cartoon, anime, illustration, or 3D doll renders.

Overall visual acceptance: PARTIAL. The singular requested dancer became three similar performers across all inspected frames. This is a major subject-duplication artifact even though each performer is photorealistic and anatomically recognizable. No second clip and no batch were generated.

Visual classification: `photoreal/live-action with major subject-duplication artifact`.

## Safety and watchdog

- Existing ComfyUI only; `--fast-disk --preview-method none` retained.
- Available-RAM soft warning `<8 GiB`; hard stop `<5 GiB` for 3 consecutive samples.
- VRAM telemetry only; no external VRAM kill.
- No threshold hit, timeout, OOM, or queue concurrency.
