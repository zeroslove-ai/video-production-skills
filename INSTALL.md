# Install / activate in Codex

The canonical source for shared skills is the private repository `zeroslove-ai/agent-skills`.

The copies under this repository's `skills/` and `.agents/skills/` are deployed compatibility snapshots. Update the central canonical copy first, then propagate.

## Project-local discovery

This repository carries:

```text
.agents/skills/
  video-production-director/SKILL.md
  video-blender-production/SKILL.md
  video-production-qa/SKILL.md
```

Fresh local/cloud Codex project sessions should discover these project copies.

## User-global discovery

On a workstation with the canonical repo cloned, run:

```powershell
pwsh ./scripts/install-global.ps1
```

from `agent-skills`. This installs globally scoped canonical skills under `~/.agents/skills/`.

## Verification

Repository files alone are not proof of runtime discovery. After a material skill update, reload/start a fresh Codex session, confirm expected skill discovery, and run a bounded replay when practical.

## Blender MCP

Use the reviewed Blender MCP setup for live inspect/correction/verification and durable `bpy` source for reproducible structural changes.
