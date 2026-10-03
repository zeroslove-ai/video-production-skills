# Original skeleton bind serialization trial R1 — 2026-10-03 KST

One disposable versioned model/motion serialization trial, following ab1409f.
Source a30fc513... and six existing Actions remain read-only inputs. No source
rest=OFF substitution, bone edits, hierarchy changes, new rig, geometry merge,
weight/material/driver changes, consumer rest rewrite or tolerance relaxation.

Feasibility: Blender FBX importer reads Pose/BindPose global matrices before
Cluster TransformLink overrides; no cluster is required to attach a BindPose to
an existing bone Model node. Without either, it falls back to Model defaults.
Exporter already provides raw bone world-rest matrices with rest=True. The
model's Pose/Cluster matrices will be captured from actual serialized elements,
not inferred from evaluated OFF. The same raw skeleton bind matrices can be
carried into meshless motion using one skeleton BindPose with no mesh, skin or
geometry. Unbound FaceBoard bones use the unchanged original rest=True getter.

Model default TRS capture/replay from previous bounded probe is retained as a
separate neutral/default layer, not used as bind/rest. Pose declaration/IDs and
Definitions template count must be internally consistent. Full source state
must restore with component diff0 and exact source SHA unchanged.

Gates: original4rigs/137bones ordered names/parents; model effective Pose/Cluster
bind versus animation Pose exact values; strict imported local rest <1e-5;
full-frame world joint position<0.0001m AND normalized-double-quaternion
rotation<0.001deg; six nonroot motions and Light/Strong2cycles. Gate failures
remain independent. Actual movement does not imply source fidelity, F2 or
Unity PASS. No performance video rerender for a failed numerical candidate.

Source raw rest, evaluated OFF, Model default, BindPose/Cluster and importer
reconstruction are recorded independently. Candidate custody must freeze exact
bytes/SHA before PM decides any Unity intake. CPU factory background only;
shared GUI/product worktrees and old ZIPs untouched.
