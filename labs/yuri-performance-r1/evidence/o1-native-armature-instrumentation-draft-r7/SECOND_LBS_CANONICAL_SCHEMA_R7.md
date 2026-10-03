# R7 second masked LBS canonical fields

R6/e0b6abe and ZIPb6979... remain byte-identical. Original Laptop3b8383a6 request specifically includes ordered native accumulation, masked LBS blend where applicable, actual stageLOCAL+WORLD and source transport. R6 raw events carried computed second-modifier state, but canonical pack visibly omitted those second-LBS primitives. R7 exposes them directly, and adds one default-OFF native hook for the actual LinearMixer.finalize `const float scale_factor = armature_weight / total` local. It does not recompute that quotient in the consumer.

| Canonical field | Storage / native scope |
|---|---|
| lbs_computed_vertex_indices | [N,2] int32 [case,sample index]; actual computed rows0/1 only, N=4 across two cases |
| lbs_computed_csr_indices | [L,4] int32 [case,sample,local original CSR,concatenated original CSR]; all original rows including zero/helpers/masks for computed vertices |
| lbs_running_delta_values, lbs_running_total_values | [L,3], [L] raw float32; actual modifier1 per-entry running_lbs_delta/running_total, no normalization or post-output inversion |
| lbs_mapped_bone_values, lbs_eligibility_values | [L] exact native float32 diagnostic values; unmapped/zero entries remain and running state unchanged |
| lbs_co_armature_values | [N,3] actual input co after second premat; includes use of previous cached original coordinates |
| lbs_previous_co_weight_values, lbs_armature_weight_values | [N] actual native interpolation/finalize weights |
| lbs_finalize_scale_factor_values, lbs_finalize_total_values | [N] actual newly logged LinearMixer quotient; actual last running_total passed unchanged to finalize |
| lbs_finalize_delta_armature_values | [N,3] actual native finalize delta in ARMATURE coordinates |
| lbs_co_before_finalize_update_values, lbs_co_after_finalize_update_values | [N,3] actual native armature co before/after delta update |
| lbs_pre_mask_local_values, lbs_vertex_output_local_values | [N,3] actual BODY LOCAL before previous-coordinate blend and after blend |
| lbs_mask_weight, lbs_previous_cached_local | [2,5], [2,5,3] actual native mask/cache also present on genuine skip branch |
| lbs_caller_input_local/world | [2,5,3] actual second caller input; links to first-DQ actual output |
| lbs_object_world, lbs_rig_world, lbs_premat, lbs_postmat | [2,4,4] actual SECOND modifier matrices, not reused first-modifier inputs |
| stage01_local/world, stage01_intermediates_computed_valid | actual second caller output and [2,5] validity;0 means genuine native skip |

Vertices21485/22227/40817 have mask0 and take native previous-mask-one return. Their caller/mask/cache fields remain actual, but running/finalize/co intermediates are absent, explicitly NOT_COMPUTED. They are excluded from sparse index/value arrays; no fabricated zeros/identity. Ordinary nullopt/full_deform=false has no meaningful computed LBS deformation matrix; it is not represented as an invented matrix. Native source operations remain unchanged when macro OFF.

Raw alternative route: each field maps to `(tag,(case,modifier=1,bone=-1,original_vertex,original_CSR_entry))`; finalize/co tags use entry=-1. Original CSR definitions/weights are request metadata verified against every actual raw row; untouched full63561/all304799 arming checks remain mandatory. All values are raw little-endian float32 bytes and each uncompressed array hash is recorded. The canonical request consumer must explicitly accept sparse helper/DQ and skip-branch schema; Laptop agreement is NOT CONFIRMED and original dense acceptance is pending. No message was sent to the product/Laptop task.

R6 packet also had a packaging error: after testing correct JSON, a reused `request` variable copied Markdown bytes under `request-inputs-exact.json`. R7 uses a dedicated request_json variable, verifies SHAa46c693c28e09a93729bbe433a522d47c7a452c740a6af6ceb8868ddec370b17 before/after copy, and parses packaged JSON. R6's CRC/member custody was valid but did not prove that file's semantic identity. Earlier immutable packet stays unchanged.

Validation: copied pinned-source apply/default-OFF token identity,2106-record complete SYNTHETIC fixture,15 single-defect intended-gate rejections, new second-LBS byte/index checks including absence of skipped rows, NPZ per-array SHA/CRC and packaged exact JSON identity. Synthetic example is test-only; no native numeric evidence. New patch/binding adapter digest is b2ba72354e36d96f87ef98f7f7c2b1dba39a95338bff2a91f4cdeb48d64989e2. Build/native capture/real full recipe/world numeric/shader/Unity/PBR and Laptop schema agreement remain pending. Acquisition approval stays false; no resources, source blends, product files or GUI changed.
