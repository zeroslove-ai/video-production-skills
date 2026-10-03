# Original Idle graph completeness correction — R2 prepared only

Frozen R1 checkpointce76347/packet c706fc8e is preserved unchanged. This additive R2 implements PM's completeness review. No Blender/probe/launcher/native build/export/activation or source/preferences mutation occurred. Current Living plan and bodyWorld f32 precision correction remain840ac26.

Only four exact original Idle Actions are read, with real Object/Key IDs/mesh owners, slot handles/channelbags/fcurve paths and existing direct/NLA references. Targets are never guessed or assigned. Original137bones/78Actions/rest/fullweights/materials/ShapeKeys/drivers and muted13 preservation remain mandatory. Original KEY curves are not substituted with face rig pose. Sampling/playback/export/material quality remain separate future scopes.

## Explicit completeness versus partial compatibility

Every slot now records matched_channelbag_count, attributed_curve_count, unresolved_bag_count, missing_API_records, complete_original_curve_attribution, graph_completeness_status and incomplete_reasons. Missing `channelbags`/`fcurves` API, UNKNOWN slot_handle, orphan handle not in real Action slots, no matched bags, or no attributed curves yields **UNKNOWN_INCOMPLETE_GRAPH**. Unknown bags are counted, not silently skipped as irrelevant. Slot uncertainty propagates to its Action and overall data status; no fallback target selection.

Candidate `compatible_all_recorded_RNA_paths` remains explicitly a known-subset observation. `compatible_all_original_curves` is **null** when attribution is incomplete, and compatibility_status is UNKNOWN_INCOMPLETE_GRAPH. Only completely enumerated known-handle/curve graphs may record complete-curve compatibility; even then compatible RNA is not authoring intent or playback acceptance. Existing binding references are recorded separately and ambiguity is retained. An intentionally empty action still has no compatibility proof from this inspection.

The guard records graph_completeness_status and all_original_curves_attributed separately from whole guard. Successful owned exit0/Active0/PIDs[] cannot promote an UNKNOWN graph to complete. No identity/resource/strictLIVE rule changed. File-only reverse comparison confirms launcher differences from R1 are fixed R2 paths and those data-completeness fields only.

## Exact final review packet

Inspector `../../scripts/r4_original_idle_slot_graph_inspect_r2.py`; launcher `../../scripts/r4_original_idle_slot_graph_launcher_r2.py`. INSPECTION_PROPOSAL_R2.json/FIXED_ROUTE_CONFIG_R2.json contain exact argv/import/input SHA bindings and new private output `outputs/o1-original-idle-slot-graph-inspection-r2`. A new external one-attempt receipt under ORIGINAL_LIVING_IDLE_SLOT_GRAPH_READ_ONLY must match inspector/launcher/config/proposal/Blender SHA and argv; approval template remains FALSE and is not installed at execution path.

Reviewed R2 installed-origin helper/315-file manifest and immutable R4 source are unchanged. Same single owned Job/suspended detached assign-before-resume/active1/two threads/affinity3/8GiB/120s/resource floors/kill-on-close/strict LIVE missing-image failure/independent cleanup remain. No preference surgery/GPU/source-model re-export is introduced. Prior R1/R5 guard FAIL stays historical evidence.

Actual API completeness/target graph/owner resolution/native before-after preservation and Job runtime are **NOT_RUN** here. Saved AST/compile, source/dependency hashes, reverse launcher diff, ZIP CRC and all member SHA passed. No source geometry/model/raw weights are in the packet.

Packet24869bytes SHA256**2848fcabb2065bc53b9ef0dd662cb131fd4f57c080e1a2d698e2e11ec8c3568a**. Inspector4841fcf66a849f5ad8403ca4f33a0edca5e67a8c01e22ddcad000d281b514ad2; launcher5212f0bf5c3f2ea20112afb0484bd728d78d60ab152f94b50a0048e0c477575a; config4393f3414b5400825068c98bcaf2c4fa0c950a366268cf9a16b44a65cc049708; proposalf4854fa003a2f30b16dbf1eee3c48614e93edd55adccfe9713087e5dcc94d300. This note is outside the frozen ZIP. Next step is PM's exact-byte review before any native launch; complete Living transport and normal-speed validation are not claimed.
