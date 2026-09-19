# Local Video Generation R0 — RTX 4080 SUPER 16GB

## Purpose

Turn the existing local ComfyUI installation into a repeatable video-generation workstation for Codex-driven experiments.

This track is additive to the existing Blender/MCP production stack. Do not replace or destabilize the existing ComfyUI, Blender, Unity, ARDY/Kimodo, or product environments.

## Known workstation baseline

- OS: Windows 64-bit
- CPU: Ryzen 7 9800X3D
- RAM: 64GB DDR5
- GPU: RTX 4080 SUPER 16GB
- ComfyUI: `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI`
- Known ComfyUI version: 0.34.6
- Python: 3.12.10
- PyTorch: 2.10.0+cu130
- Existing API path: `/system_stats`, `/prompt`, history already validated

### Existing measured passes

MiniMax H3:
- Model footprint: 39.554 GiB
- 608×352
- 22 frames @ 24 fps (~0.92 s)
- wall time: 24.759 s
- peak VRAM: 15,484 / 16,376 MiB
- output: `h3_i2v_smoke_00001-audio.mp4`
- result: PASS, no OOM

Wan 2.2 TI2V-5B:
- 320×192
- 9 frames @ 24 fps
- 4 steps
- wall time: 11.729 s
- peak VRAM: 15,518 MiB
- official ComfyUI API/workflow: PASS

## Key technical conclusion

16GB VRAM is not a simple hard "model size" wall because ComfyUI can offload model weights to host RAM and stream components. But it is also not true that every setting will work if we merely wait longer.

Three separate ceilings matter:

1. Weight residency: usually tradeable for RAM/SSD traffic and time.
2. Attention / latent / activation memory: grows with resolution and frame count; can create real OOM boundaries.
3. VAE decode: can OOM after sampling succeeds; tiling can recover some cases at a large speed cost.

Therefore local optimization must measure the complete pipeline, not only sampler success.

## Recommended model roles

### MiniMax H3 — quality / native-audio path

Use when:
- native video + stereo audio matters;
- dialogue or sound should be generated with the clip;
- subject/reference conditioning quality matters;
- 5-second hero shots justify several minutes of render time.

Do not assume 10 s costs 2× 5 s. Temporal token growth and offloading can make long clips non-linear.

### Wan 2.2 TI2V-5B — default local production path

Use when:
- fast iteration matters;
- T2V and I2V are both needed;
- 720p local generation is the target;
- many candidate clips must be searched before final selection.

On 16GB consumer cards this is the safest primary local model.

### LTX-Video — preview / motion exploration path

Optional. Use only if already available or if a later evidence gate justifies installation.
Primary value is fast motion/layout iteration; not the final identity-consistency path.

## R0 benchmark ladder

Use one prompt family, fixed seed, same output folder, and exact telemetry for every run.

### Gate 0 — inventory only

Record:
- ComfyUI git/version
- Python/Torch/CUDA
- driver
- free disk
- exact H3 and Wan weight filenames + sizes
- custom nodes
- current workflows
- idle VRAM/RAM

No downloads or upgrades in Gate 0.

### Gate 1 — existing smoke replay

Re-run the previously passing H3 and Wan smoke workflows unchanged.
PASS only if outputs, API history, and telemetry are reproducible.

### Gate 2 — H3 preview ladder

Increase one variable at a time.

Suggested sequence:
1. 608×352, ~1 s, existing steps
2. 864×480, ~2–3 s, draft steps
3. 864×480, ~5 s, draft steps
4. 1024×576, ~5 s, 12 steps
5. 1024×576, ~5 s, 18 steps

Optional only after Gate 2 passes:
- 1344×768, ~5 s
- 10 s variants

Record separate timings for:
- text/reference encoding
- sampling
- VAE decode
- audio encode/decode if exposed
- total wall time

### Gate 3 — Wan production ladder

Suggested sequence:
1. existing smoke replay
2. 832×480, 49 frames
3. 1024×576, ~3–5 s
4. 1280×704, ~5 s
5. one I2V test with a neutral, non-sensitive keyframe

If VAE decode OOM occurs, test smaller VAE tiles before reducing the model.

### Gate 4 — fixed-seed quality comparison

Produce:
- H3 draft
- H3 final
- Wan draft/final

Compare:
- prompt adherence
- identity consistency
- motion continuity
- hand/face stability
- temporal artifacts
- audio quality for H3
- generation time
- peak VRAM/RAM

Do not declare a winner from timing alone.

## Sample clip brief

Create one neutral 5-second cinematic character shot that is safe to publish in a public repo.

Prompt concept:
"A young adult woman stands by a large apartment window at blue hour, turns toward the camera, takes two slow steps, soft natural expression, subtle hair and fabric movement, realistic indoor lighting, stable face, single continuous camera move."

H3 audio add-on:
"Quiet room tone, distant city ambience, soft footsteps. She says one short Korean line in a natural voice."

Use no copyrighted character, celebrity likeness, proprietary company asset, or private photo.

## Output structure

Local-only outputs:
`ComfyUI/output/video-production-skills/local-gen-r0/<run-id>/`

Per run:
- `request.json`
- `workflow.json`
- `telemetry.csv`
- `run.log`
- `result.mp4`
- `preview.jpg`
- `metrics.json`

Repo stores only:
- workflow/source
- scripts
- metrics
- SHA-256 of large media
- small preview/contact sheet only if license-safe

Do not commit model weights or large MP4 files.

## R0 decision gates

PASS for local workstation if:
- H3 can produce a reproducible 5 s clip without OOM;
- Wan can produce a reproducible 5 s 720p-class clip;
- Codex can submit jobs over the local ComfyUI API and collect outputs/telemetry;
- failed runs recover without corrupting existing workflows;
- all settings are recorded so the run can be repeated.

Completion token:

`LOCAL_VIDEO_GEN_R0_READY`
