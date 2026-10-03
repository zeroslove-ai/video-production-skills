# ROOT_PM_O1_DYNAMIC_BODY_CYCLES_INPUT_REFERENCE_R1

Status: DONE_EVALUATED_INPUT_REFERENCE_METADATA_RECOVERED. Actual Cycles buffer / runtime tangent PBR: HOLD.

## Actual read-only capture

Pristine immutable R4 master + existing Action library, one CPU-only Blender 5.2.1 LTS job (9e2066aef7ef, 4 threads, exec session 12455). No render, GPU work, save, export, rig rebuild or GUI edit. Source job PID 135608 was independently observed by Root PM; GUI PID 129152 remained. Source job exited. Wall duration is unknown and is not fabricated.

Four NPZ files preserve actual evaluated local/world positions, local/world CORNER normals, current UVMap and dynamic triangle→source corner/vertex/polygon/material routes. Each contains 13 arrays, 63,561 source vertices, 254,602 original corners and 127,040 triangles. Total NPZ bytes: 24,413,014. SOURCE_COMPONENT_DIFF.json records identical before/after component fingerprints (diff {}). Original 78 Actions, 137 rest/hierarchy contracts and 13 original muted face bridge drivers are preserved. Master/library SHA256 and 16 provenance inputs are in DYNAMIC_BODY_CYCLES_INPUT_MANIFEST.json.

All four position and CORNER-normal fields match prior full-body reference bit-for-bit. UV, source corner/polygon routes, source packed short2 custom normals and source sharp-edge state are unchanged. This does not mean triangulation is unchanged:

| Case | Different triangle rows | Changed polygons | Quads | Ngons | Order-only |
|---|---:|---:|---:|---:|---:|
| Startle 1 | 11 | 5 | 0 | 5 | 0 |
| Startle 11 | 25 | 12 | 0 | 12 | 0 |
| Strong 6 | 42 | 21 | 9 | 12 | 0 |
| Strong 44 | 41 | 20 | 7 | 13 | 0 |

Original topology IDs remain valid, but frozen rest triangles are not dynamic runtime authority. Full changed polygon IDs and array hashes are recorded in the manifest.

## Failure and recovery

The sole source job completed four NPZ files and SOURCE_COMPONENT_DIFF, then final JSON serialization failed with `TypeError: Object of type int64 is not JSON serializable`. NumPy boolean sums returned np.int64. Blender's process exit code was 0 despite the Python exception; this is not reported as an entirely successful job.

Saved capture script now casts counts to Python int. No second Blender job was launched. Plain-Python r4_dynamic_body_cycles_input_recover.py independently verified saved data/hash/routes/reference fields and repaired only metadata. Prior 424517b raw pose/factor rows are explicitly prior-reference provenance, not newly captured raw property rows. The source job checked all 137 evaluated world matrices against frozen native references before each NPZ write; those current-job matrices were not persisted.

## Cycles boundary and next experiment

These are actual Blender-evaluated Cycles input references, not actual Cycles packed normal / Mikk tangent buffers. Blender's original short2 fan custom normals are distinct from Cycles uint32 octahedral packed normals.

Pinned Cycles mesh.cpp uses actual dynamic triangles, smooth flags, packed corner normals and UVs; scene/mesh.cpp runs triangle Mikk (three vertices per face). Body NormalMap is active, OpenGL, Displaced tangent base, Strength 0.3499999940395355 and active UVMap. Runtime PBR acceptance remains HOLD.

MSVC 14.44.35207 is installed (exact executable/hash in manifest), though absent from initial PATH. A native pinned algorithm reference is feasible conditionally: assemble unmodified util/defines.h, math_float3.h, math_int4.h with all transitive headers, compiler/SDK environment and exact triangle wrapper/FP definitions. No handport or substitute output was generated in this checkpoint. Blender Python inspection does not expose actual Cycles Mesh::update_tangents attribute buffers; true renderer proof requires a native hook/export path.

Next bounded experiment may compile pinned source against these frozen four inputs, beginning with Strong 6. Label outputs PINNED_ALGORITHM_REFERENCE; actual Cycles renderer buffer remains a separate HOLD. No full 384-frame scope or tolerance waiver is granted by this input packet.

## Custody

DYNAMIC_BODY_CYCLES_INPUT_MANIFEST.json contains four full NPZ SHA256/byte receipts, all array shapes, immutable input hashes, failure correction and job provenance. PACKET_CUSTODY.json supplies independently extractable ZIP location, full hash and member CRC/hash readback. Source master, videos and raw binary assets are not committed into Git. Historical 08caad7 is retained. Product repositories are untouched.
