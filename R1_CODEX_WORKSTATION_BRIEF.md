# R1 Codex Workstation Execution Brief

Purpose: make this repo's video-production skills discoverable in Codex and connect Codex to the official Blender Lab MCP on one real workstation without changing unrelated system/project state.

## Stop conditions

Stop and report instead of guessing if:
- Blender is below 5.1 and upgrading it would affect existing production work;
- the official Blender Lab MCP source/tag cannot be verified;
- `uv`, Git, or Codex config cannot be changed safely;
- the Blender add-on requires a human UI approval/installation step that is not available;
- the target workspace contains unrelated sensitive data that would be exposed to unsandboxed Blender Python execution.

Do not substitute the similarly named community `uvx blender-mcp` package for the official Blender Lab source.

## Gate A — environment inventory

Read only first. Record:
- OS
- `codex --version`
- `uv --version`
- Git version
- installed Blender version/path
- current Codex MCP registrations
- current skill discovery paths/catalog

Do not modify config during inventory.

## Gate B — skill discovery

Use this repository as the canonical source:

`zeroslove-ai/video-production-skills`

For the first test, copy all three skill folders into a real project-local directory:

`<TEST_PROJECT>/.agents/skills/`

Required:
- `video-production-director`
- `video-blender-production`
- `video-production-qa`

Do not use symlinks for R1. Restart/reload Codex as required and verify the three skills actually appear in the skill catalog. A successful file copy without discovery is FAIL.

## Gate C — official Blender Lab MCP

Follow `mcp/blender/SETUP.md`.

1. Verify Blender 5.1+.
2. Install/enable the official Blender Lab MCP extension from the official Blender Lab distribution. If UI action is required and unavailable, stop at HUMAN_GATE.
3. Clone `https://projects.blender.org/lab/blender_mcp.git` to a dedicated tools directory, not inside an unrelated project.
4. Fetch tags and inspect the current official release/recent security fixes.
5. Pin a reviewed official tag/commit.
6. Register the official source checkout with Codex using `uv --directory <checkout>/mcp run blender-mcp`.
7. Keep host on localhost/default local port unless there is an explicit reason not to.

Do not claim success from `codex mcp list` alone.

## Gate D — end-to-end smoke test

Use a disposable empty `.blend` file, not an active production scene.

1. Read-only: ask MCP for scene/object summary and verify the returned names against Blender.
2. Bounded mutation: create one clearly named temporary object/collection.
3. Read-back: query exact object/type/transform state.
4. Visual: capture viewport or low-cost render evidence.
5. Cleanup: delete only the temporary object/collection created by this test.
6. Read-back again and prove the scene returned to the original object set.

PASS requires all six steps.

## Gate E — first production demo

Create a 10–15 second 16:9 test clip with no proprietary/sensitive assets.

Use:
- `video-production-director` for brief/tool routing;
- MCP for live inspect/correction/verification;
- saved `bpy` script(s) for repeatable scene construction/animation/render settings;
- `video-production-qa` before completion.

Prefer a simple scene that still exercises camera, light, material, one animated object, render, and output metadata.

## Gate F — record evidence

Append one entry to `EXPERIMENT_LOG.md` containing:
- exact versions and pinned MCP revision;
- skill discovery result;
- smoke-test evidence paths;
- demo source/render paths;
- PASS/PARTIAL/FAIL;
- manual intervention required;
- friction/failure mode;
- proposed narrow skill/setup change.

Update `CHANGELOG.md` only if source/instructions actually changed because of evidence.

## Completion token

Only when Gates A–F pass:

`VIDEO_PRODUCTION_SKILLSTACK_R1_READY`
