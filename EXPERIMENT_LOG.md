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
