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

## 2026-10-02 — Blender previz provider PoC
- Task: Blender RGB/depth → ComfyUI control / Seedance first-last and video-reference adapters.
- Source: main `29f9431`; new branch `research/blender-previz-provider-poc-20261002`; isolated clone.
- Blender: 5.2.1 LTS `9e2066aef7ef`; CPU Cycles; disposable generated scene.
- Skills: repository director, Blender production, QA instructions applied; discovery/MCP gate not run.
- Inputs: authored orange cube scene and shot manifest; no user production scene loaded.
- Result: PARTIAL overall; local render/package/dry-run PASS; generative inference NOT RUN.
- Evidence: `evidence/previz/VALIDATION.md`, scene state, contact sheet, hashes, ffprobe metadata.
- Limits: ComfyUI API inactive and Fun Control weights missing; FAL_KEY absent; pose/identity untested.
- Learning: provider reference-video fps/dimensions differ from local conditioning; separate encodes required.
- Follow-up: model/VRAM gate, humanoid pose/identity shot, live provider A/B; no existing research branch changes.

## 2026-09-16 — Canonical repo migration
- Task: Extract R0 video-production Skill + Blender MCP package from Project OS incubator into the dedicated canonical repository.
- Repo: `zeroslove-ai/video-production-skills`
- Skills enabled: source migrated; workstation discovery not yet tested
- Blender MCP: official Blender Lab MCP remains preferred base
- Result: PARTIAL
- Evidence: canonical README, skills, setup/install/upstream/changelog/log committed to `main`
- Remaining gate: real workstation Codex discovery + Blender read/write/verify smoke test + first end-to-end render
- Reusable learning: Keep process knowledge in Skills, live application control in MCP, and deterministic production logic in saved source/scripts.
