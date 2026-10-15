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
- Repo / source revision: `zeroslove-ai/video-production-skills` @ `230625f` (branch `work/previs-video-pipeline-r1`)
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

---

## 2026-10-15 — R2 workstation I2V + Blender wave guide

- Task: Restore a real local I2V path, create an editable Blender greeting-wave motion guide, and make one free Genjutsu motion-transfer comparison.
- Repo / source revision: zeroslove-ai/video-production-skills, branch work/video-studio-r2 (isolated from the Yuri Unity checkout).
- Runtime: ComfyUI 0.34.6, embedded Python 3.12.10, PyTorch 2.10.0+cu130, CUDA 13.0, RTX 4080 SUPER 16 GB; Blender 5.2.1 LTS.
- Local I2V result: PASS. LTX 2.5 distilled INT8, 448×768, 24 FPS, 73 frames / 3.0417 s, H.264 MP4, 602,495 bytes, seed 20261015, 8 steps, no LoRA. Actual generation completed in 416.07 s including cold model initialization. Workflow, history, metrics and frame review are stored beside the MP4 under D:\AI\LTX25-R3\output\video-studio-r2\greeting_wave_20261015\.
- GPU/RAM evidence: 135 nvidia-smi samples; peak VRAM 15,676/16,376 MiB, observed utilization reached 98%. At peak memory pressure, the ComfyUI process used about 39 GiB working set, Windows had about 4.9 GiB RAM available and 82.6/133.1 GiB committed. The captured Task Manager row showed about 37,060 MB for the app group and GPU 0 - 3D; that engine label is not CUDA evidence. After the isolated server stopped, free RAM returned to about 43.6 GiB, committed memory to 29.7 GiB, and GPU memory to 656 MiB.
- Visual result: PARTIAL. The face, outfit and background mostly stay recognizable; there is a blink, soft smile and raised hand. The hand barely waves for much of the clip and picks up a bright fringe near the last frame.
- Blender result: PASS as previs only. Blender produced an editable 448×768, 24 FPS, 73-frame proxy animation with keyed shoulder/elbow pivots and start/peak/end frames. It is not a Yuri rig or humanoid Action. Files and metrics are under D:\AI\LTX25-R3\output\video-studio-r2\blender_previs\.
- Higgsfield: Workspace had one free hf_mult_motion_control run. Four-second 512×878 driver and avatar reference image uploaded; estimate returned 0 credits and both media roles present. One 720p request was submitted with use_free_gens=true (job bec37c97-a9b6-41a5-a2d0-a4eb41efc5eb). Status: completed. The output is stored under D:\AI\LTX25-R3\output\video-studio-r2\higgsfield_genjutsu\. Review: one character and face/outfit stay recognizable, but the arm raises and holds without a clear wrist-wave cycle or return to idle. Balance remained 8.6 credits; no paid credits or trial were used. Result: 720x1280, 24 FPS, 97 frames/4.0417s H.264 MP4; metrics and review frames are in higgsfield_metrics.json.
- Failure mode / friction: No IC-LoRA/Layout-to-Render model or upscaler is installed, and the IC-LoRA source is access-gated. This run was still image-to-video, not Blender-to-ComfyUI V2V. No humanoid rig exists in this repository for motion retargeting.
- Manual intervention required: Review the terminal Higgsfield job and likeness/motion result; later supply the actual Yuri rig before FBX/BVH or Action validation.
- Reusable learning: Task Manager's 3D engine column can under-report model inference; nvidia-smi recorded GPU compute while the 22B stack offloaded most weights into system RAM. Keep RAM and VRAM samples together.
- Skill/MCP change proposed: The actual-run conventions are appended to previs/adapters/comfyui/CONVENTIONS.md; see docs/VIDEO_STUDIO_R2_RUNBOOK.md.
- Follow-up issue/PR: Gate local Blender-video conditioning on approved access to LTX IC-LoRA plus the matching upscaler; then compare local Layout-to-Render with the free cloud motion-transfer result and validate retargeting on the real avatar rig.
