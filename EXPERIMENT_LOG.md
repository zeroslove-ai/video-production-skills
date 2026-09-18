# Experiment Log

실제 제작 작업에서 이 skillstack을 사용한 결과를 누적한다. 성공 사례뿐 아니라 실패/우회/비용/시간 병목도 기록한다.

## Entry template

### YYYY-MM-DD — <experiment name>
- Task:
- Repo / source revision:
- Codex surface/version:
- Blender version:
- MCP revision:
- Skills enabled:
- Input assets:
- Output target:
- Result: PASS / PARTIAL / FAIL
- Evidence:
- Failure mode / friction:
- Manual intervention required:
- Reusable learning:
- Skill/MCP change proposed:
- Follow-up issue/PR:

---

## 2026-09-16 — Canonical repo migration
- Task: Extract R0 video-production Skill + Blender MCP package from Project OS incubator into the dedicated canonical repository.
- Repo: `zeroslove-ai/video-production-skills`
- Skills enabled: source migrated; workstation discovery not yet tested
- Blender MCP: official Blender Lab MCP remains preferred base
- Result: PARTIAL
- Evidence: canonical README, skills, setup/install/upstream/changelog/log committed to `main`
- Remaining gate: real workstation Codex discovery + Blender read/write/verify smoke test + first end-to-end render
- Reusable learning: Keep process knowledge in Skills, live application control in MCP, and deterministic production logic in saved source/scripts.

## 2026-09-18 — Local H3 smoke replay blocked by RAM watchdog
- Task: Reconnect the existing ComfyUI installation and replay the known MiniMax H3 smoke before scaling the child-safe draft batch.
- Repo / source revision: `zeroslove-ai/video-production-skills`, `research/local-video-gen-r0`, `e082ac7b7c5260cbfae3e111a2c001d9b7a81664`
- Codex surface/version: local Windows shell; existing ComfyUI `0.34.6`
- Skills enabled: local API runner added under `tools/local_gen/`
- Input assets: existing ComfyUI `input/example.png`; no new source media committed
- Output target: existing ComfyUI local output root under `video-production-skills/local-gen-r0/`
- Environment: Python `3.12.10` embedded, PyTorch `2.10.0+cu130`, RTX 4080 SUPER, driver `595.97`
- Workflow used: recovered prior API payload from the existing smoke MP4 metadata; 608×352, 22 frames @ 24 fps, 4 steps, seed `20260908`, H3 VAE/audio nodes, `VHS_VideoCombine`
- Safety thresholds: RAM soft/hard `52/56 GiB`; VRAM soft/hard `15.2/15.6 GiB`; timeout `600 s`
- Result: FAIL — watchdog stopped at `17.137 s` for `OOM_RAM`; peak VRAM `15,047 MiB`, peak RAM `60,672,122,880 bytes`; no output MP4
- Evidence: `evidence/local-gen-r0/inventory.md`, `evidence/local-gen-r0/smoke-replay-20260918.md`, local run metrics/telemetry/run log under the ComfyUI output root
- Failure mode / friction: ComfyUI H3 dynamic staging pushed the process to ~`33.48 GiB` working set / ~`44.37 GiB` private memory while other workstation processes were active; ComfyUI itself interrupted cleanly
- Manual intervention required: started the existing ComfyUI installation; no upgrades, model changes, workflow overwrite, or unrelated process termination
- Reusable learning: the API payload can be recovered from MP4 metadata, and the watchdog correctly prevents a second job when host RAM crosses the hard limit
- Skill/MCP change proposed: none until the exact smoke replay passes in a fresh memory state
- Best prompt(s): none evaluated because Gate B failed
- Next narrow recommendation: restart/settle the existing ComfyUI workstation state, rerun this exact smoke payload under the same watchdog, and only then resume the draft batch

## 2026-09-18 — Local H3 recovery R1 and child-safe draft batch
- Task: Recover the existing ComfyUI/H3 installation with a memory-safe watchdog, replay the known smoke, and run the eight-prompt child-safe draft batch sequentially.
- Repo / source revision: `zeroslove-ai/video-production-skills`, `research/local-video-gen-r0`
- Environment: Windows 10 Pro; embedded Python `3.12.10`; PyTorch `2.10.0+cu130`; RTX 4080 SUPER 16 GiB; driver `595.97`; ComfyUI `0.34.6`
- ComfyUI startup: existing installation only, `--windows-standalone-build --fast-disk --preview-method none`; no upgrades or model changes.
- Workflow used: copied `workflows/local_gen/h3_draft_base.json`, MiniMax H3 I2V; smoke `608x352`, `22` frames, seed `20260908`; draft `864x480`, `124` frames, 4 steps, audio off.
- Draft batch settings: prompts P01–P08, fixed seeds `101, 202, 303, 404, 505, 606, 707, 808`, strict one-job-at-a-time execution, CPU H.264 output after the installed NVENC API mismatch was observed.
- Safety thresholds: available-RAM soft warning `<8 GiB`; hard stop `<5 GiB` for 3 consecutive one-second samples; VRAM `>=15,872 MiB` warning only; timeout `600 s`.
- Result: PARTIAL — smoke PASS, real draft P01 PASS, full batch `8/8` technical PASS; visual target is not met because the reused source image is a flat cartoon reference, so outputs are stable cartoon motion rather than photorealistic live-action clips.
- Performance: smoke `14.11 s`, peak VRAM `15,560 MiB`; draft batch `58.691–65.750 s` per run, peak VRAM `14,563–15,286 MiB`, lowest available RAM `27.12–30.69 GiB`, peak ComfyUI RSS up to `16.54 GiB`.
- Evidence: `evidence/local-gen-r0/recovery-r1-20260918.md`, `evidence/local-gen-r0/draft-batch-summary.md`, `evidence/local-gen-r0/draft-batch-summary.json`, and per-run telemetry/metrics under the existing ComfyUI output root.
- Failure modes / friction: old used-RAM watchdog produced a false-positive stop; NVENC encode failed because driver API `13.0` was below required `13.1`; both were handled with narrow changes only. No CUDA OOM, RAM hard-stop, timeout, or queue concurrency occurred in the recovery batch.
- Manual intervention required: restart of the existing ComfyUI process only; no unrelated process termination.
- Reusable learning: available physical RAM is the correct primary host guard; the H3 workflow's `LoadImage(example.png)` source dominates prompt style, so prompt-only changes cannot turn that cartoon reference into live action.
- Best prompt(s): P04 and P06 produced the most useful stage-light/background variation; P01 had the clearest simple full-body composition. This is a visual observation, not a photorealism pass.
- Next narrow recommendation: keep the validated runner and replace only the I2V `LoadImage` source with a child-safe realistic reference image, then rerun P04 at seed `404` before any wider batch.
