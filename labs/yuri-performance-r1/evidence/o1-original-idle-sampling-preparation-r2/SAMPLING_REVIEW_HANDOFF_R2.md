# Original Idle sampler R2: closed-log custody correction

**File-only preparation; no Blender launch/probe/activation.** Frozen R1 checkpoint2e8672e and packet51b29af0 remain unchanged. R2 requires its own exact review receipt; R1 receipt cannot authorize this route.

The R1 collector could hash fixed-capture.log while Blender stdout was still open. Blender exit/footer could then change its SHA and make a successful capture fail the independent payload audit. R2 collector explicitly excludes the live log, external Job receipt, terminal custody and result manifest itself. It records hashes only for closed collector payloads and labels final log custody deferred.

After the exact owned child signals, Job drains and closes, log context closes, and OWNED_JOB_RESULT_R1.json closes, the R2 launcher writes **TERMINAL_FILE_CUSTODY_R2.json** with final fixed-capture.log, closed Job receipt and collector result byte counts/SHA. No manifest self-hash or circular Job receipt hash exists. If terminal/drain/cleanup conditions are absent, custody is explicitly pending and makes no final-log hash claim. Final custody does not override guard_status; the independent auditor still requires the original strict whole-Job PASS and all145frame geometry/channel/appearance/NLA validations.

Corrected executable paths and exact input/argv/hash bindings: FIXED_ROUTE_CONFIG_R2.json and SAMPLING_PROPOSAL_R2.json. Receipt destination is the fresh outputs/o1-original-idle-sampling-r2/PM_APPROVAL_ORIGINAL_IDLE_SAMPLE_R2.json. The template remains approved=false and is not installed.

| Artifact | SHA256 |
|---|---|
| Collector R2 | fb44ed96ebb07ad1c2b55cd2619828a97ca6ecdaa1bf366b24f9f2d79334f416 |
| Launcher R2 | b6890cb38139340a7c2693d001708ecf68125a2a6e48d2a7fd89224de237564b |
| Auditor R2 | 1a6c2ddaf92becf2d2b2043958ac660f9907dbe4733290780446b2bea7b0b94d |
| ZIP,28331bytes | 5f4562b1bcf14aee3e9f83e43fefea4ff119e76266abe2446e25805e47cf7f1b |

Validation: AST compile and pinned input hashes; reverse-diff proves only path/result/receipt revision and log custody changes against frozen R1; synthetic file-only regression appends a Blender-like footer after the early log hash and verifies final custody includes it; ZIP CRC and every member SHA verified. All three frozen R1 script hashes remain exact. Native APIs, output growth and120second runtime fit remain NOT_RUN.

Full145continuousframes1..145/fps24/base1/originalCYCLES,386curves vs native evaluated outputs, all137bones, complete native meshes, source property/Key metadata,13mutes, exact NLA graph and OFF→ON→OFF restoration requirements are unchanged. One owned CPU process/2threads/affinity3/8GiB/120s/RAM12GiB/C100GiB, strict LIVE identity and cleanup remain unchanged. No geometry/channel dilution, resource expansion, alias, export, source save or automatic retry. GUI/productGPU lease untouched. Approximately332MB source-point geometry plus evaluated growth/JSON is still an estimate. Public packet contains scripts/metadata; actual native numeric outputs remain private.

Ready for PM exact-byte packet review; no native or product/playback acceptance claimed.
