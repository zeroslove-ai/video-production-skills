# R4 static dance03/16 · bounded native QA R1 · FAIL/HOLD

2026-10-05. ONE two-pose batch, existing immutable R4 hierarchy only. 06/14 remain pending. No rig, mesh, rest, weight, ShapeKey, material, shader, texture pixel, face/gaze driver or source Action edits. No product/Unity changes, exporter, new character, motion sequence, timing, PhysX, F2 or TierP promotion. Original78 Actions (including66) and08caad7 preserved.

Actual source SHA256: a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa.
Candidate OFF SHA256: 4b618baf6086b6e2ed77492945942c7da07fd5fff06c2793795eb5f86c62faae.
Separate two-Action / zero-object-mesh-armature library SHA256: 47ba39607a241eda004950c637087792c002f984745955b420f1dba7363456d1.
Private render/candidate folder: C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/dance-two-pose-native-r1.
User-visible matched OFF/03/16 front/LEFT grid: outputs/dance-two-pose-delivery-r1/OFF_03_16_MATCHED_FRONT_LEFT_R1.jpg.

| Test | 03 modest LEFT lift | 16 explicit RIGHT-front cross attempt |
|---|---|---|
| Native local quaternion delta | thigh.L35°, shin.L65°, foot.L30°; right upper arm110.38°, left forearm110.77° | right upper arm32.00°/forearm116.40°, left upper arm13.75°/forearm140.59° |
| Actual supporting sole | RIGHT full foot2430 vertices +109 bottom-patch points drift0 | Both full feet and original bottom patches drift0 |
| Floor gap | RIGHT minimum0.19985mm, patch0.19985–2.19059mm. Raised LEFT minimum88.3254mm | Original LEFT minimum0.31701mm, RIGHT0.19985mm retained |
| Finite / topology | finite PASS, unchanged topology | finite PASS, unchanged topology |
| Evaluated edge deformation | ratio extrema0.04965–21.31683; p01/p99 0.59909/1.46235 | extrema0.11630–3.70582; p01/p99 0.92469/1.22939 |
| NEW nonadjacent inclusive body intersections | LEFT arm cohort64, RIGHT0, left-leg cohort16 | LEFT533, RIGHT278, left-leg cohort38 |
| Head / hair intersection | All tested cohorts0 | All tested cohorts0 |
| Crossing | Not applicable | RIGHT centerline69.99mm camera-nearer at extended projected lines, but parameters1.156/1.340 lie beyond BOTH forearm segments: actual forearm X requirement FAIL |
| Native visual | Knee modestly lifted and right foot retained; hand/chest and local tissue crease not approved | Reads as close chest hands rather than valid crossed forearms; left elbow extreme bend/roll and body clearance not approved |
| Verdict | FAIL/HOLD | FAIL/HOLD |

Angles above are actual quaternion basis deltas from original native pose, not calibrated anatomical joint limits. Source rig has no bone constraints that certify ROM. Finite coordinates do not certify acceptable deformation. Sole-floor measurements use actual evaluated body foot/toe weights>0.5 and original minimum-Z+2mm patches, against Contact_Ground Z=-0.19986mm. Stationary geometric soles are not force/COM/support-polygon/PhysX certification.

Collision scope includes triangles if ANY vertex has summed relevant arm/hand/digit or left-leg weights>0.01, versus ALL actual body triangles, plus all actual head/hair triangles. Weak weights/palm/webbing remain included. Cohorts overlap, so counts must not be added or treated as isolated anatomical locations. Shared-vertex adjacency and identical triangles are separate raw counts; newly intersecting nonadjacent identities are compared against original source. Tiny/adjacent deformation, volumetric containment and physical collision are not certified. Supplementary vertex-to-triangle distances exclude same-cohort triangles for remote targets and are diagnostics, not full surface-distance PASS.

One failure cause: direction-only quaternion targeting did not constrain the native elbow bend plane/twist and achievable two-segment reach. It produced adverse local deformation/triangle intersections and moved the proposed16 crossing beyond the native forearm lengths. This batch stops at FAIL; no rig expansion, no second pose candidate. One future alternative, not executed: fit the same native two-segment chains with explicit elbow pole/twist and surface-clearance constraints before testing another static pose.

OFF preservation:
- Original source + imported Action-only library: complete original78-Action snapshot equal before/after import and each ON/OFF.
- Candidate OFF geometry/rest/weights/morphs/drivers/materials/nodes/world/camera/light/scene/evaluated geometry equal source.
- SaveAs changed six texture filepath strings, packed texture SHA bytes unchanged. Raw candidate full signature therefore differs in textures and is NOT waived as an exact raw-path PASS. Transiently restoring original image path strings in read-only verification leaves zero categories different; candidate bytes were not rewritten.
- Existing authoritative960×920 RGBA neutral vs produced OFF: changed pixels0, maximum channel error0.
- First full native job returned FAIL after renders at strict post-SaveAs snapshot assertion; logs and candidate preserved. Separate no-rerender/no-new-pose source Action-only and raw candidate diagnostic verification passed a NEW strict guard. This does not convert first failed job or pose quality to PASS.

Protected GUI and PRODUCT_EXCLUSIVE GPU lease retained; guarded CPU-only jobs closed. Inspection guard PASS c8326fdd...; original pose/render guard FAIL840eb37c...; independent OFF verifier guard PASS51d2ca85.... Exact receipts and original pinned scripts packaged privately. Public Git includes only scripts/scalar diagnostics and SHA pointers, no source geometry or raw pose quaternion arrays/render images.
