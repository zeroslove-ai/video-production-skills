# Gate B — H3 smoke replay

Date: 2026-09-18 KST
Branch: `research/local-video-gen-r0`
Workflow: `workflows/local_gen/h3_draft_base.json`
Prompt ID: `652e0afe-4e16-40a6-8968-e915e387c008`

## Result

`FAIL` — watchdog stopped the unchanged known H3 API graph before an MP4 was produced.

The graph settings and prompt were preserved from the prior passing MP4 metadata:

- `example.png` first frame
- 608×352
- 22 frames @ 24 fps (~0.92 s)
- 4 steps, `simple` scheduler, `res_multistep` sampler
- seed `20260908`
- MiniMax H3 video + audio VAE nodes and `VHS_VideoCombine`

Only the output filename prefix was routed to the local run folder so the prior output was not overwritten.

## Watchdog evidence

- Wall time: `17.137 s`
- Peak VRAM: `15,047 MiB` / `16,376 MiB`
- Peak host RAM observed: `60,672,122,880 bytes` (~56.52 GiB)
- RAM soft warning: `58,189,639,680 bytes` (~54.20 GiB)
- RAM hard stop: `56 GiB` configured; crossed
- VRAM soft/hard limits: not crossed
- Timeout: not reached
- Failure reason: `OOM_RAM`
- MP4 output: none

Telemetry: `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI\output\video-production-skills\local-gen-r0\smoke-replay-20260918\telemetry.csv`
Metrics: `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI\output\video-production-skills\local-gen-r0\smoke-replay-20260918\metrics.json`
Run log: `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI\output\video-production-skills\local-gen-r0\smoke-replay-20260918\run.log`

## ComfyUI state after stop

- `/queue`: empty
- `/history/<prompt_id>`: empty after interrupt cleanup
- `comfyui.log`: `Global interrupt` → `Processing interrupted` → `Prompt executed in 17.17 seconds`
- Existing ComfyUI server remained healthy after the interrupt.

## Root-cause evidence

The existing ComfyUI process reached approximately `33.48 GiB` working set and `44.37 GiB` private memory. ComfyUI logged dynamic staging of approximately `14,956 MB` for the H3 text encoder, `4,965 MB` for the video VAE, and `19,995 MB` for the H3 model. This explains the host-RAM pressure while VRAM remained below its hard limit. No environment upgrade or unrelated process termination was attempted.

## Gate decision

Per the execution brief, no 8-prompt batch or larger H3 ladder was started after the smoke replay failed. The next run requires a fresh, lower-memory workstation state and the same smoke replay to pass before scaling.
