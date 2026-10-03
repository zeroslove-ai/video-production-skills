# Full recipe custody and conditional read-only preflight

Status: exact recipe file custody PASS; live Blender identity comparison NOT_RUN.

The existing PM local copy was independently hashed, compared against the pinned Git blob metadata, and copied byte-for-byte to the Desktop output directory. The 18,390,792-byte recipe SHA256 is `0cd0bdd70e5a6c0670846dab74e295b0a637a79f1c6d57d503611d5cf50aafe0`. It retains 63,561 positions, 57 bone slots, 304,799 ordered CSR entries, 58 groups and mask group 52, including all 37,310 zero-weight entries. Both requested file-arming rows pass file/hash and declared-route checks. These are file checks, not runtime action or native arithmetic checks. See RECIPE_CUSTODY_R1.json for exact provenance and counts.

The subsequent conditional read-only Blender task requires an existing compatible owned-process guard. Neither existing guard satisfies that condition:

- `scripts/native_readback_proposal/owned_windows_capture_supervisor_v5.py` SHA256 `86d62b17bdbd0b03de7f33c52a2def11688b70a1050110b1f465ea52887143ac` unconditionally asserts `human_large_resource_acquisition_approved is True`, including command overrides. Its acquisition/capture root must already exist; `C:/YuriTransfer/native-cycles-readback-r1` is absent. Actual acquisition approval remains false.
- `scripts/r4_owned_windows_job_preflight.py` SHA256 `70d5beae93f0c702596c8c669e619bf4d60e7ffe221f73b093ffdf4a7973a913` accepts only its fixed Python print/sleep child, with a 256 MiB job/process limit. It has no Blender command interface or the requested conservative free-memory gate.

As instructed for an incompatible existing guard, no Blender process was launched. No argv was executed, no source was opened, and no live comparison or first-mismatch result exists. A separately scoped read-only guard is needed before the live verifier can run; the existing acquisition/native guards and false approvals were not altered or bypassed.

Read-only observations on 2026-10-03: GUI Blender PID 129152/start 2026-10-02 23:17:57 remains present; GPU lease remains PRODUCT_EXCLUSIVE/product-observed PID 58248. Installed Blender executable SHA256 is `284f4041f98e113f3dc10654a7193ffaaa9bfdfec8b87fa116620a48b5f6d4cb`; no fresh executable version invocation was performed.

R4 source SHA256 remains `a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa`; exact recipe remains `0cd0bdd70e5a6c0670846dab74e295b0a637a79f1c6d57d503611d5cf50aafe0`. Source, GUI, actions, frozen R6/R7 packets and historical 08caad7 remain unchanged. Raw recipe/source files stay outside public Git. This checkpoint does not claim source live identity, native numeric acceptance, Unity/PBR acceptance, or appearance promotion.
