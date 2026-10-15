# ComfyUI dry-run conventions (R1)

## Workflow template location

- Canonical template: `previs/adapters/comfyui/workflows/previs_handoff_v1.api.json`
- Adapter: `previs/adapters/comfyui/adapter.py` (`ComfyUIAdapter`)

## Input staging

Dry-run staging layout under `<work_dir>/staging/`:

- `shot-manifest.json` — copied authoritative manifest
- `inputs/beauty/` — beauty pass frames from the package
- `inputs/contact_sheet.png` — optional contact sheet
- `comfyui_request.json` — bound workflow + metadata
- `expected_output_manifest.json` — what a live run should produce (not executed in R1)

## Manifest → workflow binding

Bindings are explicit in `comfyui_request.json` → `bindings`:

| Binding key | Workflow node | Manifest source |
|-------------|---------------|-----------------|
| `load_image_beauty` | node `1` LoadImage | `render_passes[id=beauty]` |
| `prompt_encode` | node `2` CLIPTextEncode | `prompts.prompt` |
| `negative_prompt_encode` | node `3` CLIPTextEncode | `prompts.negative_prompt` |
| `seed` | node `4` KSampler | `seed.value` |

Width/height/frame_count/fps are carried for a future video node but are not executed in R1.

## Expected output manifest

Written to `staging/expected_output_manifest.json` during `dry_run_validate`. Live ComfyUI runs should replace `mode: dry_run_expected` with actual artifact paths and hashes.

## Next live gate

1. Point ComfyUI at the staged `workflow` JSON (or import into UI).
2. Confirm node class_types match the local install.
3. Run one frame smoke test, then full shot.
4. Record PASS/FAIL in `EXPERIMENT_LOG.md` with server version and workflow hash.

## R2 workstation runs

- Live generation evidence belongs in `docs/VIDEO_STUDIO_R2_RUNBOOK.md` and `EXPERIMENT_LOG.md`; do not label a dry-run or API queue submission as a rendered-video PASS.
- Keep the canonical ComfyUI install read-only. For isolated runs, use a separate port, output/user directories, and an explicit extra-model-path file.
- Save the submitted API workflow, ComfyUI history, MP4, SHA-256, frame/FPS metadata, and sampled GPU values in a unique run directory.
- Record system RAM alongside VRAM for large LTX models. A Task Manager `3D` engine percentage does not represent CUDA utilization; retain `nvidia-smi` observations as the GPU evidence.
- A Blender guide video and an LTX image-to-video run are distinct input modes. Claim Layout-to-Render/V2V only when the actual guide video is connected to a compatible video-conditioning workflow.
- Treat proxy animation as previs. Do not report its pivot keyframes as a humanoid Action, FBX, BVH, or retargeted character motion.

## R2 workstation runs

- Live generation evidence belongs in `docs/VIDEO_STUDIO_R2_RUNBOOK.md` and `EXPERIMENT_LOG.md`; do not label a dry-run or API queue submission as a rendered-video PASS.
- Keep the canonical ComfyUI install read-only. For isolated runs, use a separate port, output/user directories, and an explicit extra-model-path file.
- Save the submitted API workflow, ComfyUI history, MP4, SHA-256, frame/FPS metadata, and sampled GPU values in a unique run directory.
- Record system RAM alongside VRAM for large LTX models. A Task Manager `3D` engine percentage does not represent CUDA utilization; retain `nvidia-smi` observations as the GPU evidence.
- A Blender guide video and an LTX image-to-video run are distinct input modes. Claim Layout-to-Render/V2V only when the actual guide video is connected to a compatible video-conditioning workflow.
- Treat proxy animation as previs. Do not report its pivot keyframes as a humanoid Action, FBX, BVH, or retargeted character motion.
