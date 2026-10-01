# R3 Codex Brief — H3 Photoreal T2V Gate

## Root cause

The R1 batch was not a photorealistic text-to-video test.

The reused API graph hard-wired:
`LoadImage(example.png) -> MiniMaxH3ImageToVideo.first_frame`

Therefore the flat cartoon source image dominated every output.

The graph also used 4 sampler steps without a Turbo LoRA.

Do not generate another batch from that graph.

## Authority

Use:
- `workflows/local_gen/h3_t2v_photoreal_4step.json`
- official ComfyUI MiniMax H3 T2V behavior: `MiniMaxH3ImageToVideo` with no first/last frame connected = T2V
- official 4-step Turbo LoRA:
  `minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors`

## Gate A — inventory only

Before downloading anything, check:
`ComfyUI/models/loras/minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors`

If already present, reuse it.

If missing, download only that official Comfy-Org LoRA. Do not upgrade ComfyUI, Torch, CUDA, Python, or other nodes.

Verify file exists and record size/hash.

## Gate B — graph audit

Open/parse `h3_t2v_photoreal_4step.json` and prove:

- no `LoadImage` node
- no `first_frame`
- no `last_frame`
- UNET = `minimax_h3_fl2va_pruned_int8_convrot.safetensors`
- text encoder = `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`
- Turbo LoRA = official 4-step file
- LoRA strength = 1.0
- scheduler = simple
- steps = 4
- sampler = res_multistep
- width = 864
- height = 480
- length = 124
- audio output disconnected for this visual gate

If any condition fails, STOP. Do not render.

## Gate C — one-frame/style proof, not a batch

Render exactly ONE clip first.

Seed: 101
Duration: 124 frames (~5.17 s)
Resolution: 864x480
Steps: 4
Audio: off

Prompt:
Realistic live-action cinematic footage of a cheerful six-year-old girl performing an energetic, age-appropriate K-pop-inspired dance on a bright family-friendly stage. Natural human skin texture, realistic child facial proportions, realistic hair strands, real fabric, real stage lighting, photographic live-action look. Full-body framing, stable face and limbs, crisp rhythmic footwork, coordinated arm movements, one quick spin and a joyful final pose. The camera makes a gentle professional dolly move while keeping her entire body visible. No illustration, no animation, no cartoon, no CGI, no doll-like rendering, no stylized drawing.

Do not run P02-P08.

## Gate D — visual acceptance

Extract first/middle/last frames.

PASS only if:
- clearly photorealistic / live-action
- human photographic skin and hair
- not illustration, cartoon, 3D doll, anime, painted image
- full-body child dance is recognizable
- no major duplicate limbs or catastrophic face distortion

If it is cartoon/stylized:
STOP immediately. Do not waste another render.

Diagnose workflow/model/LoRA/prompt conditioning before any second clip.

If it is photorealistic but motion quality is weak:
run ONE comparison only:
same seed/prompt/resolution at 6 steps if the active Turbo setup supports it correctly.
Do not start a wide batch yet.

## Gate E — only after visual PASS

Once the single photoreal clip passes, run 3 prompts only:
- stage
- dance studio
- outdoor festival

One seed each.

After those three are visually checked, then and only then expand to the full prompt pack.

## Memory safety

Keep the validated recovery settings:
- `--fast-disk --preview-method none`
- available RAM warning <8 GiB
- stop <5 GiB for 3 consecutive samples
- VRAM telemetry only; no external VRAM kill

## Reporting

VERDICT: PASS / PARTIAL / FAIL

GRAPH AUDIT:
- no image conditioning: yes/no
- turbo LoRA present: yes/no
- exact LoRA filename
- steps
- resolution/frames

PHOTOREAL GATE:
- PASS/FAIL
- output path
- wall time
- peak VRAM
- minimum available RAM
- first/middle/last preview paths
- visual classification: photoreal / stylized / cartoon / broken

NEXT ACTION:
one narrow action only

Do not call technical render success a PASS if the requested visual style is not met.
