# Changelog

## 2026-09-16 — Canonical repo bootstrap

### Added
- `video-production-director`
- `video-blender-production`
- `video-production-qa`
- official Blender Lab MCP → Codex setup guide
- Codex installation guide
- upstream registry and adoption policy
- experiment log
- workstation R1 execution brief

### Migration
- Canonical source moved from `zeroslove-ai/project-os/incubators/video-production-skillstack/` to `zeroslove-ai/video-production-skills`.
- `project-os` remains only as historical/incubation context and must not become a second editable source.

### Design decisions
- Skill = reusable production procedure.
- MCP = live Blender inspection/correction/tool access.
- saved bpy/Remotion/FFmpeg source = reproducible production logic.
- research/planning context is separated from heavy build context for long tasks.
- state-first + visual QA is required for non-trivial Blender work.

### Validation status
- Canonical repository: CREATED
- Skill source: MIGRATED
- Codex skill discovery on user workstation: NOT YET SMOKE-TESTED
- Blender Lab MCP end-to-end connection: NOT YET SMOKE-TESTED
- First reproducible 10–15s demo: NOT YET TESTED
