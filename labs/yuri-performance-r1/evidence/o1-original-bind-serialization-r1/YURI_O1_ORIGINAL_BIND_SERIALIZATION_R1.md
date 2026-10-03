# Original skeleton bind serialization R1 — 2026-10-03 KST

**One trial completed. Bind transport and strict model↔animation rest PASS; source rotation fidelity remains HOLD. No Unity/product/F2 promotion.** Prior source/Actions/rig/weights/materials/drivers/helper poses/ZIPs unchanged; CPU factory jobs, no GUI or product edits.

## Exact representation

Raw native rest, evaluated OFF, FBX Model default TRS and effective Pose/Cluster bind are separate. Original source OFF Model defaults are captured/replayed only for serializer consistency, never substituted for rest. The original model's actual raw BindPose matrices are emitted in meshless animation as one skeleton BindPose.143Pose nodes =137original bones +4rig objects +2existing ancestry empties. No Geometry, Mesh, Skin or Cluster is added to animation. Unbound FaceBoard13/ancestry matrices use original rest=True global getter; no new rig or rest reset. Definitions/Pose count added consistently.

Actual wire audit:1150model Cluster.TransformLink records across124bound bones are exactly equal to corresponding model Pose matrices. Every existing effective model bone bind is byte-value identical to animation Pose; source rest conversion checked independently, max coefficient residual1.192092896e-7 from float32 matrix operations. Column-major float64 wire storage and declared source→FBX axis/unit convention are retained. Trial wrapper recorded0Cluster captures because its orientation filter selected Model→Cluster; actual source edges are Cluster→Model. This is disclosed, not hidden: transported Pose equals all actual overriding Cluster matrices by independent binary audit. No second export performed.

Source SHA `a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa` unchanged, component diff={},78original Actions preserved. Bone order/parents/counts identical across paired files, all57body including nondeform helpers preserved. Both loops sampled2cycles. No source scale/height ratio reapplied.

## Strict gates

- Model↔animation local rest: body0, face0, hair0, FaceBoard2.384185791e-7, all<1e-5 **PASS**. This repairs the prior bind/default representation gap.
- Source full-frame position max 1.51406816e-06m<0.0001m **PASS**.
- Source full-frame normalized-double quaternion rotation max 0.00212100607° versus<0.001° **FAIL** (face J_Bip_L_Index3, Startle frame17). Combined position+rotation **FAIL**; no threshold relaxation.
-276unique source frames and384endpoint-inclusive motion frames tested;6actual nonroot movements **PASS**, Light/Strong2cycles **PASS**. All-frame data, not action-name existence.
- Blender/Unity visual fidelity and F2 **HOLD**. No repeated performance video; previous complete normal-speed references retain their own failures. New bytes are not authorized Unity input until PM custody/disposition.

## Remaining reconstructed-bone gap

Source and imported bones now receive the same raw FBX bind representation, but source→Blender importer reconstructed bone matrix remains measurably different. Diagnostic world-rest rotation J_Bip_L_Index3≈0.002089307°, Index2≈0.001650977°. Source/import head/tail/length/local matrices/orthogonality/determinant/singular values are recorded for all137bones, together with raw source rest and evaluated OFF references. Importer uses bind matrices, localizes hierarchy, computes correction matrices, then creates normalized Blender bones. We have isolated the residual reconstruction stage; no claim that a single float operation is the sole cause and no importer rewrite. Zero skin influence on a finger bone does not waive the all-bone gate.

Original bind can be transported with meshless FBX; that missing representation is resolved. Remaining limitation is reconstructed source-pose equivalence in this Blender roundtrip. Source-preserving fallback is canonical original .blend + existing Action/NLA + exact native evaluated matrix payload. Future consumer must independently measure its own importer raw bind/default/Transform against these references after exact custody. Blender failure is not automatic Unity failure or PASS. Do not rewrite consumer rest, offset bones, prune helpers or enlarge tolerance to hide it.

## Custody/reproduction

Versioned model: `YURI_O1_R4_NATIVE_CARRIER_20261003_R1.fbx`, 23537068bytes, SHA `3b37f3570742617b42215e980a70260490ffe92c7480c33a5de5060dd38c90c1`.
Meshless animation: `YURI_O1_R4_NATIVE_ANIMATION_ONLY_20261003_R1.fbx`, 7071276bytes, SHA `ea3f93f8fe7f59b171a67dd4be5c893bca6cbd238a82d1f68c080e861c30e67c`.
Expanded exact bind/source/rest/import/fullframe/error receipts are packaged. Original source/action/reference data reused via exact REUSE_POINTERS.json to frozen ZIP4ec5c10... and recovery ZIP080352.... No duplicated canonical master or normals/material rebake.

Run r4_original_bind_serialization.py once on fresh Blender5.2.1LTS factory background; then wire_verify and reconstruction_diagnostic are read-only checks; package freezes bytes. Runtime exporter functions are patched only inside this disposable process and restored; installed module files remain unchanged. PM dispatch blob dc5d8b09dd402382f10041c9d8540ca3022dfb45. No next trial or production work started.
