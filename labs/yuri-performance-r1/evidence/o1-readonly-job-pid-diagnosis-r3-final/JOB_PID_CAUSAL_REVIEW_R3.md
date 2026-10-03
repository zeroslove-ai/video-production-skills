# Owned Job extra PID: bounded causal findings

Blender source-read remains NOT_RUN. No approval receipt was written; large acquisition/native build/trace/capture remain unapproved. Frozen R1/R2/V5 and all failed attempts are preserved. Earlier cleanup PASS proves final drain only; the earlier interpretation of an extra PID as merely cumulative accounting is withdrawn.

| Variant | Probe | Owned Python PID | Extra observed PID | Actual Job observation | Final |
| --- | --- | --- | --- | --- | --- |
| CREATE_NO_WINDOW R2 | normal | 136840 | 121016 | Active2, Total2, Terminated0 | exit0; Active0; PID list empty |
| CREATE_NO_WINDOW R2 | timeout | 71808 | 117768 | Active2, Total2, Terminated0 | exit88; Active0; PID list empty |
| DETACHED_PROCESS R3 | normal | 112736 | none | Active<=1, Total1, Terminated0 | exit0; Active0; PID list empty |
| DETACHED_PROCESS R3 | timeout | 126136 | none | Active<=1, Total1, Terminated0 | exit88; Active0; PID list empty |

Both extra PIDs are **C:\Windows\System32\conhost.exe**, with parent PID equal to their owned Python PID, later creation FILETIME, IsProcessInJob(this exact Job)=true and observed STILL_ACTIVE259. Repeated accounting before/after identity lookup reports Active2. This is an actual live console-host process, not a cumulative-count inference. Read-only identity handles were opened only for PIDs returned by this owned Job; no unrelated process handles or PID-based termination were used. Root ownership is recorded by created process handle, GetProcessId and creation FILETIME.

R3 changes the process creation flag from CREATE_SUSPENDED|CREATE_NO_WINDOW (0x08000004) to CREATE_SUSPENDED|DETACHED_PROCESS (0x0000000c). The same fixed Python executable SHA, argv (`-I -S`, print/sleep), logs and limits are used. Console detachment removes the extra host in both measured cases. [Microsoft documents DETACHED_PROCESS as creating a console process without attachment to a console](https://learn.microsoft.com/en-us/windows/console/creation-of-a-console). The observed conhost behavior under the active limit is not generalized as an undocumented OS exemption.

Native layout assertions and actual limit readback pass: Basic64, Extended144, Accounting48; Basic LimitFlags offset16/ActiveProcessLimit offset40; Accounting ActiveProcesses offset40; Job PID list array offset8; PROCESSENTRY32W568/parent offset32. Each diagnostic sample records actual accounting around PID-list/identity queries, timestamps, executable, Toolhelp parent, process creation/exit FILETIME, exit code and IsProcessInJob. API queries are sequential snapshots rather than an atomic snapshot; raw results are preserved. [Microsoft accounting semantics](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_accounting_information) and [PID-list layout](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_process_id_list) were checked.

Limits remain affinity3/two cores, 8GiB process/job, active process limit1, kill-on-close. Pre/during free RAM>=12GiB and free C>=100GiB pass; source/actions/recipe pre/post hashes remain identical. R3 confirms total lifetime association count1 and all sampled identities are the one owned Python PID, then zero drain for normal and watchdog termination. Heavy memory negative tests were not run. **R3 is Python-probe-only and explicitly has no Blender launch route.** A future source-read guard must incorporate the detached mechanism and undergo its own frozen guard/verifier/argv/SHA review; these probe receipts are not Blender authorization.

Exact-byte R2/R3 guards and full corrected receipts are in `YURI_O1_JOB_PID_DIAGNOSIS_R3.zip` (27,617 bytes), SHA256 `53b6ce6fc1c35886990cdce648433c0d394292d3825f64b970280544d5ea0479`.
Findings SHA256 `b90b3400a9c5da20f1e9659dbe30fc8fbba8e3fd17deb1a587f5fdf7cef3ccb6`.
R2 guard SHA256 `dfa8b60ea29e4c269f33f3f251174ce54be06935b7b4e5757ae29ca006c43cba`.
R3 guard SHA256 `e21b9ceed80a65ca60ba98c71b8a394b84f0287c10a0bc5717a9b6dd265f7aed`.

Next bounded task: PM review of causal findings/corrected detached receipts and preparation of a separately frozen detached source-read guard. No source-open/live recipe or native numeric acceptance is claimed.
