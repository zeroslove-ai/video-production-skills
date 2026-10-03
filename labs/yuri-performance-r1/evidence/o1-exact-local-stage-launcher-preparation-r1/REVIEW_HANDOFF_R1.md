# Exact source-local fixed route — preparation only

2026-10-03 KST. Collector/proposal at checkpoint7ebeeb3 are unchanged. New files provide a single fixed-purpose launcher and hash-bound configuration. No launcher execution, probe, Blender/GPU/render/export/bake/download or custom native build occurred. R5 file and actual whole-guard FAIL remain unchanged.

`../../scripts/r4_exact_local_stage_launcher_r1.py` is dry by default. Its only execution argument is `--run-approved-fixed-capture`; no command override, help/probe or retry route exists. The config gives the exact host-Python launch argv and exact Blender argv. The future external receipt must bind **launcher/config/collector/proposal/Blender SHA256 and exact argv**, with scoped approval and explicit terminal-behavior review. The supplied template has approval FALSE, resides only in this evidence directory and is not installed as an approval receipt. No new launch approval is inferred from this preparation.

## Terminal and ownership review

- The child is created suspended with DETACHED_PROCESS flags12 and assigned to the newly owned Job before resume. Native readback must match active1, affinity3, process+Job8GiB and kill-on-close flags. Existing R5 ctypes ABI/layout assertions are reused. Fixed argv supplies two Blender threads; resource floors are12GiB free RAM/100GiB free C:, watchdog120s.
- Image lookup uses the **original owned CreateProcess handle**, rather than reopening a PID with a new query handle. PID/creation identity and Job PID list remain checked. No unrelated PID is opened or killed.
- If the owned handle is signaled before image query, classify terminal by its exit code. If it becomes signaled during image query, retain raw image result/error and classify by the owned exit code. Missing executable image while the same owned handle remains genuinely LIVE is FAIL. Exit FILETIME alone does not replace handle signaling. This does not retroactively make R5 PASS.
- Normal completion requires owned exit0, Job total1/limit-terminated0, Active0 and empty Job PID list before close. Failure cleanup terminates only the owned Job, or the own newly created unassigned suspended child if assignment failed. Cleanup operations individually catch/log errors so an assertion cannot skip Job close. Terminal signaling, raw exit code/times, Job accounting/PIDs before close and signaling after close are recorded independently. Any missing terminal proof keeps guard FAIL.
- Data manifest availability/file hashes are reported independently from whole `guard_status`, including on guard failure. Partial files/logs are retained; no deletion or automatic retry. Collector exit93, timeout/resource failure or LIVE image failure cannot become a guard PASS merely because data files exist.

Preflight denies a missing/mismatched review receipt or immutable input/hash drift **before any process creation**. Native Job creation/assignment failures retain failure where the owned Job exists; a preflight failure has no child and no successful execution record. All postlaunch source/dependency hashes must remain equal.

Windows Job is not network isolation. Exact factory/offline CLI and the unchanged collector's empty addon gate are required; neither script performs account/network/plugin calls. This is not packet-level network proof.

## Actual validation and review boundary

Only saved-file AST/compile, one fixed CreateProcess call/static route inspection, original collector/proposal/R5 and input dependency hashes, and ZIP CRC were verified. The launcher was **not executed**, including its dry branch. Native ABI readback, resource enforcement, image race, timeout and cleanup paths are **NOT_RUN** for this route. No synthetic probe is substituted for those facts. Prior R5 logic provenance is reuse evidence only, not a new guard PASS.

The20,115-byte preparation ZIP is additive to the earlier collector packet; it contains launcher/config/template/validation and exact collector/proposal copies, without character geometry or private arrays. Exact packet/file custody is in `PACKET_CUSTODY_R1.json`. This note is outside the frozen ZIP. PM's next step is review of these exact files/receipt/terminal behavior before authorizing the single two-frame native source read. No Unity/native numeric/PBR/AlwaysAnimate acceptance is claimed.
