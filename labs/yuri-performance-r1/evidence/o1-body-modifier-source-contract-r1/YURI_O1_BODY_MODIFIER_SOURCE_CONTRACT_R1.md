# R4 original body modifier source contract — 2026-10-03

`3b37f357…` is the **native original-bind carrier**, preserving original control points and 1,150 stored bind rows. It is distinct from the earlier rebuilt GameRig compatibility experiment. The preceding agent final's generic “GameRig FBX” wording must not conflate them. Native duplicate Body material slots (three references to one material) remain source authority; existing carrier serialization connects that material once. This does not abandon/reset the current source-equivalent adapter. Preserve source slot identity when reconstructing clone topology. No visual promotion is granted.

This support contract reads existing receipts/NPZ only. No Blender process/load/render/export/bake, source binary write, rig/rest/weight/material/driver edit or product repository write occurred. Installed build hash `9e2066aef7ef` resolved on the official Blender repository; its five original algorithm source files and COPYING are frozen with hashes in the packet. Upstream files remain unmodified, GPL-2.0-or-later.

## Exact stages

| Order | Source modifier | Essential settings |
|---|---|---|
| 0 | Armature | Meshy_Fitted_Rig; vertex groups; preserve volume DQ; multi=false; no overall mask/envelopes |
| 1 | R3 neck and joints - local linear blend | same rig; LBS; multi=true; mask R3_Surface_LinearBlend; invert=false |
| 2 | R3 local joint surface relaxation | CORRECTIVE_SMOOTH; LENGTH_WEIGHTED; 24 iterations; scale=1; ORCO; is_bind=false; pin boundary; only_smooth=false; mask R3_Joint_CorrectiveSmooth |
| 3, 4 | R3 raised shoulder surface L, R | SMOOTH; 60 iterations each; XYZ; respective shoulder masks |
| 5, 6 | R3 bent hip surface L, R | SMOOTH; 220 iterations each; XYZ; respective hip masks |

There is **no SurfaceDeform** modifier/cage/bind cache in this seven-stage stack. “Surface corrections” means stage 2 plus stages 3–6. CorrectiveSmooth ORCO reads original object-mesh positions, not evaluated OFF geometry. `R4_Body_Original_Modifier_Support.npz` freezes those original local coordinates, all ordered edges/polygons/corners and both 57-row original Armature bind sets (identical). Body object and rig matrices are separate; apply the object world transform once.

## Algorithm semantics

The pinned [Armature modifier](https://github.com/blender/blender/blob/9e2066aef7ef/source/blender/modifiers/intern/MOD_armature.cc), [multi-modifier cache](https://github.com/blender/blender/blob/9e2066aef7ef/source/blender/modifiers/intern/MOD_util.cc) and [deformation code](https://github.com/blender/blender/blob/9e2066aef7ef/source/blender/blenkernel/intern/armature_deform.cc) preserve pre-first-Armature coordinates for stage 1. In mesh-local coordinates, its un-inverted mask gives `(1-mask)*DQ(original) + mask*LBS(original)`. Do not apply LBS to already DQ-deformed vertices. Keep literal bone influences separately from nonbone masks. The upstream accumulated contribution threshold is 0.0001, not authorization to prune small individual influences.

[CorrectiveSmooth](https://github.com/blender/blender/blob/9e2066aef7ef/source/blender/modifiers/intern/MOD_correctivesmooth.cc) length-weighted iteration accumulates `edge_vector * edge_length`; its divisor is `sum_incident_lengths * edge_degree`, and multiplier is `2*factor*effective_mask`. Use original edge order/float operations. Pin-boundary zeros the mask at endpoints of edges with exactly one face-corner use; frozen support marks 84 vertices. Smooth original ORCO using the same settings, compute per-corner tangent-space rest deltas, smooth incoming stage-1 coordinates, then restore transported deltas with per-corner angle weights normalized per vertex and scale 1. These are geometric polygon-corner frames, **not UV shading tangents**. Preserve pinned degeneracy tests, inverse fallback and `safe_acos_approx`. A driver factor change invalidates rest-delta settings/cache; a fixed OFF cache is insufficient. Mask-zero vertices remain neighbor inputs.

[Smooth](https://github.com/blender/blender/blob/9e2066aef7ef/source/blender/modifiers/intern/MOD_smooth.cc) averages incident **edge midpoints**, not neighboring vertices alone. Each iteration accumulates before writing positions, then interpolates with `factor*vertex_mask` on XYZ. Keep every source edge and full neighbor coordinates; apply stages L shoulder → R shoulder → L hip → R hip sequentially. Rebuilding adjacency from triangulated/split Unity mesh changes this algorithm.

## Drivers and support indices

`BODY_MODIFIER_PARAMETERS_AND_DRIVERS.json` contains exact expressions, SINGLE_PROP target paths, mute/curve modifier settings, ordered source settings, seven mask columns, both original bind rows and nine frozen evaluated cases. Inputs use raw pose-bone quaternion properties **wxyz**, not world rotation, Euler rotation or assumed evaluated-parent-local TRS. Define `s(x)=clamp(x,0,1)^2*(3-2*clamp(x,0,1))`:

- Corrective factor: `.65*s((max(1-a²,1-b²,1-c²,1-d²)-.03)/.15)`, with w of upper_arm.L/R and thigh.L/R.
- Shoulder factor per side: `.75*s((1-w²-.2132)/.1488)`.
- Hip factor L/R: `.9*s((max(0,sign*z*w)^2-.003)/.122)`, sign L=-1, R=+1; thigh quaternion w/z.

Mask columns use original source IDs. Positive supports: LinearBlend 29,081; Corrective 28,291; shoulders L/R 6,102/6,117; hips L/R 8,037/8,025. The seventh nonbone group `Joint_Smoothing_Mask` (9,245 positive vertices) is retained but unused by these modifiers. No extra stage or bone-weight renormalization is inferred from it. Dense masks were checked bit-for-bit against both existing original row data and CSR. Full original topology is retained for neighbors, including mask-zero vertices.

## Bounded numerical next step and limits

Reuse original full-stack Strong frame 6 from the existing 18-volume deformation packet; the manifest gives its exact chunk, SHA and source-frame offset. The PM-reported 1.77mm DQ+secondary prototype residual is not runtime PASS or a proven single-stage cause. Existing Strong frame 1/49 ablations give surface-stack effect ≈1.45469mm maximum and masked-secondary effect ≈1.43595mm; these are **different frames**, not an explanation of the frame-6 residual.

Nine frozen cases include Strong frames 1/25/49 Corrective factors `.2226823866 / .1280768365 / .2226823866`; all four ordinary Smooth factors are zero in those cases. First implement/verify CorrectiveSmooth at those exact case factors against the already frozen ablation arrays, then compare full-stack Strong6 using verified raw driver values. No all-frame raw quaternion-property/factor capture or individually separated surface-stage Strong6 capture exists in the current receipts. A matrix-derived factor remains a candidate until checked. If needed, the precise missing source evidence is raw wxyz inputs plus evaluated five factor outputs at Strong frame6, not another character export or new geometry. This checkpoint respects the no-new-Blender-load restriction and leaves that gap explicit.

The CPU script read back all 16 support arrays exactly and checked finite values, original mask rows and the two 57-row bind sets. Packet freeze checks every hash/member/CRC. No numerical adapter implementation or full Unity deformation/normal/material/AlwaysAnimate acceptance is claimed. Master, source Actions and earlier checkpoints are preserved.
