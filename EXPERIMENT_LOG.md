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

---

## 2026-10-02 — R1 previs handoff (synthetic pipeline)
- Task: Provider-neutral shot manifest, synthetic 12s package, ComfyUI/external adapter dry-run (no paid generation).
- Repo / source revision: `zeroslove-ai/video-production-skills` @ `81c7007` (branch `work/previs-video-pipeline-r1`)
- Codex surface/version: CURSOR-1 isolated worktree worker
- Blender version: not invoked
- MCP revision: not invoked
- Skills enabled: `video-production-director`, `video-blender-production`, `video-production-qa` (source extended for manifest handoff)
- Input assets: `previs/fixtures/demo_r1/synthetic_scene.json` (12s @ 24fps, 1280×720)
- Output target: `previs/out/demo_r1/demo_r1_12s/` (gitignored); manifest validates; adapter staging under `previs/out/adapter_dry_run/`
- Result: PASS (synthetic + dry-run only)
- Evidence: `python -m pytest previs/tests -q` (11+ tests); `python -m previs_pipeline.cli demo`; `validate` + `dry-run comfyui`
- Failure mode / friction: Live Blender bpy export and ComfyUI server not available in worker; beauty-only bpy script until compositor pass wiring.
- Manual intervention required: Workstation Blender export + ComfyUI one-frame smoke (next gate).
- Reusable learning: Separate `provenance.blender_runtime` from synthetic `export_mode`; keep adapter contracts on staging + expected output manifest.
- Skill/MCP change proposed: None beyond R1 doc/skill cross-links; live gates recorded in `docs/PREVIS_VIDEO_PIPELINE_R1.md`.
- Follow-up issue/PR: Merge `work/previs-video-pipeline-r1` after review; run Gate D–E from `R1_CODEX_WORKSTATION_BRIEF.md` on workstation.
