# Changelog

## 2026-10-02 — Previs → AI video handoff (R1)

### Added
- Provider-neutral `previs/schema/shot-manifest.schema.json`
- `previs_pipeline` Python package (validate, synthetic demo, CLI)
- Blender export script `previs/blender/export_previs_package.py` (live gate pending)
- ComfyUI and external provider adapters (dry-run only)
- `docs/PREVIS_VIDEO_PIPELINE_R1.md`, pytest suite under `previs/tests/`

### Validation status
- Synthetic handoff demo CLI: TESTED (worker)
- Live Blender bpy export: NOT_TESTED
- Live ComfyUI / external generation: NOT_TESTED

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
