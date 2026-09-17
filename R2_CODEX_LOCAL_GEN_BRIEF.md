# R2 Codex Brief — Local AI Video Sample + Limit Sweep

## Mission

On the real Windows workstation, validate the practical limit of the existing RTX 4080 SUPER 16GB ComfyUI video stack and produce reproducible sample clips.

Canonical repo:
`zeroslove-ai/video-production-skills`

Research branch:
`research/local-video-gen-r0`

Read first:
- `LOCAL_VIDEO_GEN_R0.md`
- `EXPERIMENT_LOG.md`

## Hard constraints

- Do not reinstall ComfyUI if the existing installation works.
- Do not upgrade Python, Torch, CUDA, GPU driver, or custom nodes before inventory and smoke replay.
- Do not overwrite existing workflows.
- Do not delete model weights.
- Do not touch Unity, Blender, ARDY/Kimodo, Yuri product worktrees, or unrelated Codex configuration.
- One GPU generation job at a time.
- No production app integration in R0.
- Large generated videos remain local; repo gets metadata/evidence only.
- Stop before any change that needs a reboot or broad environment migration.

## Existing path

`C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI`

Known working API:
- `GET /system_stats`
- `POST /prompt`
- history endpoint

## Gate A — read-only inventory

Capture:
- `nvidia-smi`
- ComfyUI version/HEAD
- Python
- Torch/CUDA
- exact model files
- H3 workflow(s)
- Wan 2.2 workflow(s)
- custom nodes
- free RAM/disk
- idle VRAM

Write inventory to:
`evidence/local-gen-r0/inventory.md`

## Gate B — replay known passes

Re-run unchanged:

H3:
- 608×352
- 22 frames @ 24 fps
- expected prior wall time ~24.759 s
- prior peak VRAM 15,484 MiB
- prior output family `h3_i2v_smoke`

Wan:
- 320×192
- 9 frames @ 24 fps
- 4 steps
- expected prior wall time ~11.729 s
- prior peak VRAM 15,518 MiB

Do not require exact timing equality. Require successful completion, playable MP4, API history PASS, and no OOM.

If either replay fails, stop the scaling ladder and diagnose the environment delta first.

## Gate C — build a reusable local runner

Create a small script under this repository, not inside ComfyUI core, that:

1. checks ComfyUI health;
2. loads an API workflow JSON;
3. applies a small config patch for prompt/seed/resolution/frames/steps where node IDs are known;
4. submits `/prompt`;
5. waits for history completion;
6. records wall time;
7. samples `nvidia-smi` once per second to CSV;
8. copies or references the output path;
9. writes `metrics.json`;
10. computes SHA-256.

Use only standard library unless an already-installed package is required.

## Gate D — MiniMax H3 sweep

Use a fixed seed and one neutral public-safe prompt.

Run sequentially:
- H3-P0: 608×352, known smoke
- H3-P1: 864×480, ~2–3 s, low/draft steps
- H3-P2: 864×480, ~5 s, low/draft steps
- H3-B1: 1024×576, ~5 s, 12 steps
- H3-F1: 1024×576, ~5 s, 18 steps

Only if F1 is stable:
- H3-X1: 1344×768, ~5 s
- H3-X2: 1024×576 or 864×480, ~10 s

Increase one variable at a time.

If OOM:
- identify phase: TE / sampler / VAE / audio;
- release model memory through supported ComfyUI mechanisms;
- retry once with the narrowest memory mitigation;
- never silently lower settings and call it the same test.

## Gate E — Wan 2.2 sweep

Run:
- WAN-P0: known smoke
- WAN-P1: 832×480, 49 frames
- WAN-B1: 1024×576, ~3–5 s
- WAN-F1: 1280×704, ~5 s
- WAN-I1: one 5 s I2V test from a generated/non-sensitive keyframe

Prefer native ComfyUI offloading.
Do not add experimental 14B quant workflows during this R0 unless the 5B path is fully characterized first.

## Gate F — sample deliverables

Produce at least:
1. one H3 5 s clip with native audio;
2. one Wan 5 s clip;
3. one still/contact sheet showing beginning / middle / end frames;
4. metrics table.

Sample concept:
A young adult woman by an apartment window at blue hour, turns toward camera and takes two slow steps. Stable face, subtle cloth/hair motion, one continuous camera move.

For H3 add:
Quiet room tone, distant city ambience, footsteps, and one short Korean spoken line.

No copyrighted character, celebrity, company asset, or private photo.

## Gate G — evidence and repo hygiene

Append to `EXPERIMENT_LOG.md`:
- environment
- workflow IDs
- exact settings
- wall time
- peak VRAM
- peak host RAM if measurable
- result
- output local path
- SHA-256
- failure phase if any
- manual intervention

Do not commit generated MP4 files unless tiny and intentionally approved.
Commit scripts/workflows/metrics/docs only.

## Verdict format

Return first:

`VERDICT: PASS | PARTIAL | FAIL`

Then:
- fastest usable H3 preset
- highest stable H3 preset
- fastest usable Wan preset
- highest stable Wan preset
- exact sample output paths
- measured bottleneck
- next narrow optimization only

Completion token only if Gates A–G pass:

`LOCAL_VIDEO_GEN_R0_READY`
