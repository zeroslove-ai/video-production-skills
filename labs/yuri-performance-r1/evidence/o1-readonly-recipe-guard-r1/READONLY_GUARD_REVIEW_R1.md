# Installed Blender source-read guard review candidate

Prepared only. Blender was not launched. No approval receipt exists. V5/R2, large acquisition approval=false, custom native build/trace approval=false, source/actions/recipe and GUI PID129152 remain unchanged.

Actual command tested: installed Python313 runs `scripts/r4_readonly_owned_job_guard_r1.py --prove-fixed-probes`. The fixed owned children use `-I -S -c` with print/sleep only. Normal PID134120 exited0; watchdog PID121188 exited88. Both have final Job ActiveProcesses0, empty Job PID list and signaled owned process handles. Pre/post immutable file hashes match. Resource samples and combined stdout/stderr are preserved. Actual Job limit readback confirms affinity3, active limit1 and 8GiB process/job memory. Source job timeout is fixed120sec; probes use3sec/0.3sec to exercise cleanup.

**Unresolved review item:** both probes report cumulative TotalProcesses2 and TotalTerminatedProcesses0; an additional associated PID can appear transiently. Its origin and admission status were not identified. Do not claim a proven single admitted process throughout execution. The configured limit is verified, and final zero children is verified. Four earlier failed attempts and their exact source/logs/receipts are preserved. Assertions that cumulative count must equal1 or that the transient PID list must contain only the root were unsuitable as unqualified proof. Microsoft documents that failed associations can increment both total and transient active counts, but this alone does not explain the observed TerminatedProcesses0: [official accounting documentation](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_accounting_information). The guard requires PM review of this anomaly before the source route can run.

Frozen source-read argv is in REVIEW_MANIFEST.json. `--disable-autoexec` precedes the canonical blend filename so the disable flag applies before loading. `--python-exit-code 93` makes verifier exceptions fail the process. The source verifier reads original bone rest matrices, body world/basis vertices, original ordered groups/CSR weights and mask contract, comparing float32 bytes; it does not import Actions, update pose, invoke operators, render, export, save or repair. It stops at the first mismatch. It has no local helper imports to leave mutable dependency hashes unreviewed.

The source route requires a separate exact approval receipt with guard/verifier/executable/probe hashes, fixed argv, scoped PM review and both review booleans=true, while human_large_resource_acquisition_approved remains false. No arbitrary command/executable/timeout overrides exist. Fixed scripts contain no download/network route; Windows Job is not a network security sandbox.

Review ZIP: `YURI_O1_READONLY_GUARD_REVIEW_R1.zip`, 37,676 bytes, SHA256 `20fc9ecc269396810e1b40313d67adc74ffc04845c1e55d9404fc61f34bceb5c`.
Manifest SHA256 `2f112515796f8c2cc453ce9ef639479afaf3ae60eb21ede53cdff08c84603cec`.
Guard SHA256 `35d7c08503759c0be1f6e3e99b78e45309d84061659aab5f590cb0d01c7c21eb`.
Verifier SHA256 `4c84215c6a61addf220b1a8cf408ae8e675cbb8aceca35158452d8869a8cd763`.
Probe manifest SHA256 `2c33e8c04dbfb8f61f9d45fb8e8d9b281832d8551b08ae168a8fb2a385224b77`.

Exact-byte frozen copies are in the ZIP and `frozen/`; Git line-ending conversion must not replace approved bytes. Public packet contains tool/evidence only, no blend, full numeric recipe, product source or media. Live source identity, native arithmetic, visual/PBR/Unity acceptance remain NOT_RUN/NOT_CLAIMED. Next bounded task: PM review of fixed guard/verifier/argv and accounting anomaly; no Blender run in this preparation checkpoint.
