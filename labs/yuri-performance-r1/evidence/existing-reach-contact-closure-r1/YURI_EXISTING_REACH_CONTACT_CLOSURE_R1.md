# Existing C1 Reach contact gate closure R1

Verdict: **FAIL / HOLD**, source-only. This closes a missing gate; the old candidate and its sealed packet are unchanged.

61 samples at 30fps were evaluated against actual body/head/hair triangles. Relevant arm/hand/digit triangles include any vertex whose summed relevant bone weights exceed 0.01. Identical/shared-vertex triangle pairs are separated; new nonadjacent pair identities are compared against the original R4 OFF mesh, evaluated at all 61 samples. Source geometry has one unique fingerprint. L/R cohorts overlap: summed rankings are not distinct penetration counts. Surface intersections do not measure penetration depth, containment or physics.

All 61 mapped samples have new intersections. Worst count is frame53 /1.733333s: LEFT485 and RIGHT4, chiefly left hand/fingers against left thigh during entry/return. RIGHT clavicle/neck contributes a minority. Frame23 at the reach peak has LEFT0 /RIGHT6. The source original native Reach, separately phase-normalized from native frames1–97, has zero contacts across all61 samples; it is a different motion/target, not same-path ground truth.

Shoulder/clavicle/elbow deformation was measured in six weak-weight regions. Maximum edge ratio19.09862 is clavicle.L at frame43: source0.279476mm to posed5.337613mm. Percentiles and extrema are retained per sample; finite coordinates and matching topology do not certify acceptable skin deformation.

Original78Actions, geometry, rest, weights, keys, materials/nodes, packed textures and drivers remain unchanged. The old candidate retains six SaveAs-remapped raw texture locator strings: this raw difference is not waived. Its own ON→OFF signature is identical; transient original-path restoration yields strict source equality, then the old strings are restored without saving.

Existing three matched 1× full61-frame videos were reused and SHA/full decoding rechecked; no old frames rerendered. Unity/AlwaysAnimate/state/time/weight, physics, props, MUG/F2/F3 and TierP remain unverified (TierP0).

One separate source-upper reuse correction is authorized by the measured defect. It must retain old lower/root and all source appearance; this is not another dance03/16 angle or IK iteration.
