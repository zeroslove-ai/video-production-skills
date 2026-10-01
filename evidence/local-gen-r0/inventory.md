# Local Video Generation R0 — Read-only Inventory

Captured: 2026-09-18 KST
Repository: `zeroslove-ai/video-production-skills`
Branch: `research/local-video-gen-r0`
Repository HEAD: `e082ac7b7c5260cbfae3e111a2c001d9b7a81664`

## Scope and safety

- Inventory was read-only against the existing workstation installation.
- The Yuri Room workspace was not modified.
- No Python, Torch, CUDA, GPU driver, custom node, model, or ComfyUI core changes were made.
- ComfyUI API was not running at the first check (`127.0.0.1:8188` connection refused).

## Host

- OS: Windows 10 Pro, version `10.0.19045`, build `19045`
- Installed/visible RAM: `64,546,164 KiB` (~61.58 GiB visible)
- Free RAM at inventory: `40,530,208 KiB` (~38.63 GiB)
- C: free: `287,891,386,368` bytes (~268.1 GiB)
- D: free: `438,361,362,432` bytes (~408.2 GiB)

## Python / Torch / CUDA

System Python (`C:\Program Files\Python313\python.exe`):

- Python `3.13.3`
- `torch` not installed in system Python; this is not the ComfyUI runtime.

Existing ComfyUI embedded runtime:

- Python `3.12.10`
- Executable: `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\python_embeded\python.exe`
- PyTorch `2.10.0+cu130`
- Torch CUDA `13.0`
- `torch.cuda.is_available()`: `True`

## GPU / driver

`nvidia-smi` inventory snapshot:

```text
GPU: NVIDIA GeForce RTX 4080 SUPER
Driver: 595.97
VRAM total: 16376 MiB
VRAM used: 2370 MiB
VRAM free: 13676 MiB
GPU utilization: 37%
```

## ComfyUI

- Path: `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI`
- Version: `0.34.6`
- Git state: detached HEAD
- Git HEAD: `8fed37813848259fbdd2548ae3cd9f14df7fd68b`
- Git commit date: `2026-09-07 19:24:58 +0000`
- Known launcher retained: `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\Start ComfyUI.bat`
- Initial API status: not running; `GET /system_stats` was refused.

## Existing H3 model files

All paths below are under the existing ComfyUI installation and were not moved or changed.

| File | Bytes |
|---|---:|
| `models/diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors` | 20,970,379,616 |
| `models/text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` | 15,687,142,551 |
| `models/vae/minimax_h3_video_vae_fp16.safetensors` | 5,207,808,496 |
| `models/vae/minimax_h3_audio_vae_fp32.safetensors` | 605,254,808 |

Related existing Wan files were also present:

- `models/diffusion_models/wan2.2_ti2v_5B_fp16.safetensors` — `9,999,658,848` bytes
- `models/checkpoints/wan2.2-i2v-rapid-aio.safetensors` — `23,387,012,595` bytes
- `models/vae/wan2.2_vae.safetensors` — `1,409,400,960` bytes

## Existing workflows and evidence

- H3 UI workflow copy: `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\h3_r3_official_i2v.json` — `71,242` bytes
- H3 workflow is the official `LoadImage -> MiniMaxH3ImageToVideo -> MiniMaxH3SigmaShift -> BasicGuider -> SamplerCustomAdvanced -> VAEDecode/VAEDecodeAudio -> VHS_VideoCombine` graph, stored in ComfyUI UI workflow format.
- Existing H3 output family: `ComfyUI/output/H3_R3/h3_i2v_smoke_*`
- Existing H3 metadata: `ComfyUI/output/H3_R3/h3_i2va_nurse_compare_v001_meta.json`
- Existing metadata records a prior H3 pass at 576x1024, 124 frames @ 24 fps, 4 steps, 242.203 s, peak dedicated VRAM 13,623 MiB, with audio enabled. It is historical evidence only; it was not used as the new smoke replay.
- Existing user workflow directory: `ComfyUI/user/default/workflows/`
- Existing Wan low-memory workflow copies: `wan 저사양.json`, `wan 저사양1.json`

## Relevant custom nodes

- `ComfyUI-WanVideoWrapper`
- `ComfyUI-GGUF`
- `comfyui-videohelpersuite`
- `ComfyUI-Easy-Use`
- `ComfyUI-WanAnimatePreprocess`
- `comfyui-frame-interpolation`
- `comfyui-itools`

MiniMax H3 nodes are present in the pinned ComfyUI core under `comfy_extras/nodes_minimax_h3.py`.

## Gate A result

Inventory complete. Gate B is pending ComfyUI restart and unchanged H3 smoke replay.
