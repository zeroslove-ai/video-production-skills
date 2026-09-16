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
