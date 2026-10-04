# R4 pose03 constrained native correction C1 · FAIL/HOLD / method stopped

ONE candidate, 2026-10-05. Immutable R4, original78Actions/rest/weights/geometry/materials/ShapeKeys/face-gaze drivers unchanged. Existing R2 and failed92c74b7 batch retained. No06/14/16 expansion, rig/exporter/framework/product/Unity changes, angle sweeps or second correction candidate. Static source experiment only; PhysX/F2/TierP/StageA not approved.

Source SHA256: a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa.
Candidate OFF SHA256: edfe9975aa89db3c8df28382b6c4df9a9737244660710bed1039cbdbcb2c3ab1.
One-Action / zero-object-mesh-armature library SHA256: 65bd438a7a32f27c8b1721f6859e35cf14eaea3150309bc18df0db7a215004b6 (148,293bytes).

Existing native solutions inspected before authoring: original WalkInPlace, QA_HipStress, Reach and TalkGesture keyframes. Reused exact WalkInPlace39 LEFT thigh/shin/foot quaternions, with pelvis/root/RIGHT leg unchanged. Local quaternion delta25.048° /52.001° /26.996°. Reused Reach77 native elbow axis for LEFT arm, existing chain lengths141.476mm/119.626mm, explicit outward pole, analytical two-segment reach. Axial twist applied-16.942° within±35° cap, elbow bend72.256° within±85° cap; actual wrist target error2.300mm. Caps are conservative experiment bounds, not source-rig certified anatomical ROM. Previous RIGHT diagonal arm quaternion curves retained exactly.

| Measurement | Failed original03 | Constrained C1 |
|---|---:|---:|
| LEFT leg weak-weight inclusive NEW nonadjacent pairs |16|0|
| LEFT arm inclusive NEW nonadjacent pairs |64|68|
| RIGHT arm / tested head / hair pairs |0|0|
| RIGHT full foot2430vertices /109sole patch drift |0|0|
| RIGHT minimum actual floor gap |0.19985mm|0.19985mm|
| LEFT minimum actual floor gap |88.325mm|58.969mm|
| Finite / topology |PASS|PASS|
| Edge ratio p01 /p99 |0.59909/1.46235|0.64650/1.40214|
| Edge ratio maximum |21.31683|21.31683|
| Overall pose acceptance |FAIL/HOLD|FAIL/HOLD, stop method|

Actual read-only localization of residual68 pairs: shoulder/armpit, dominant upper_arm.L/chest deformation and R3_Shoulder_PoseRelax.L /CorrectiveSmooth masks. Bounds X66.85–103.27mm/Y-134.39–-30.58mm/Z692.25–735.09mm. The remaining failure is not established as palm/chest penetration merely from screen overlap. Inclusive collision oracle proves nonadjacent triangle intersection and its vertex-weight region, not volumetric/PhysX collision.

Largest stretch remains on unchanged RIGHT neck/clavicle neighborhood: source edge0.194139mm→4.138428mm (21.31683×). Strongest collapse is also RIGHT clavicle/neck region:35.525324mm→1.952244mm (0.054954×). This was not repaired by the LEFT-only correction. The source rig and weights were preserved; these metrics must not be called an acceptable mesh merely because coordinates are finite or overview silhouette appears readable.

One measured cause: native pole/hinge positional constraints control bone endpoints but do not constrain the original shoulder tissue surface. The wrist target fits, yet immutable shoulder/chest deformation still intersects; retained RIGHT shoulder pose also retains extreme local strain. **Stop this local method.** One alternative, proposed only: reuse a complete existing native Reach shoulder/clavicle/elbow posture and accept a lower/outward hand placement, then gate actual shoulder surfaces before seeking closer03 silhouette. No additional candidate executed.

Original OFF acceptance:
- Source plus one imported Action: complete original78 snapshot equal on import and after ON/OFF.
- Candidate reopened raw snapshot equal to source, including original texture filepath strings; no normalization needed.
- SaveAs relative_remap=False preserved strings without rewriting shader/texture data.
- Neutral960×920RGBA: changed pixels0, maximum channel error0.
- Strict guard inspection PASS72c2ace3; single correction/render PASS8a14b0eb; read-only verifier C1 initially failed during diagnostic serialization after reopening source object reference, preserved; fresh C1b fixed only the read-only collector, no pose/candidate rerender/rewrite, PASS3fa8675e.
- Earlier92c74b7 raw SaveAs path limits/failure remain unchanged.

Sole measurements: actual evaluated foot/toe sum weights>0.5 and source bottom-Z+2mm cohorts, original Contact_Ground Z. Geometric unchanged soles do not certify force/COM/support/PhysX. Collision cohort triangles include ANY vertex with summed relevant bone/digit weights>0.01 vs ALL actual body triangles and all actual head/hair. No weak-weight, palm or webbing exception. Cohorts overlap; do not sum counts. Shared-vertex adjacency/identical triangles separate from nonadjacent source-baseline comparison. No containment/adjacent deformation/physical certification. Matched original-light front/anatomical LEFT768×1024 CPU8sample renders provided; noise unchanged experiment settings, no visual authority promotion.

User-visible comparison: outputs/dance03-constrained-delivery-c1/OFF_R1_C1_MATCHED_FRONT_LEFT.jpg. Exact scalar custody and private packet receipt alongside this report. Public Git contains scripts/scalars/SHA pointers only; original source, raw quaternion arrays, native renders and contact triangle records remain private. Protected GUI/GPU unchanged, all owned jobs drained.
