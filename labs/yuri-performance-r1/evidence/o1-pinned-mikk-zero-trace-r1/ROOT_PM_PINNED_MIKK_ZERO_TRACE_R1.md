# ROOT_PM_PINNED_MIKK_ZERO_TRACE_R1

Metadata-only supplement to b60d0d1; existing frozen input and algorithm packets unchanged. No Blender, renderer, GPU, native re-execution or source geometry/material changes. Unit tangent gate remains FAIL; actual Cycles buffer / PBR proof HOLD. Original CORNER normal 0.001° gate remains unchanged; packing quantization does not waive it.

All 79 saved zero tangents are localized in PINNED_MIKK_ZERO_TRACE.json: actual triangle row, local corner, original corner/vertex/polygon/material slot, all three UVs, float32/64 signed UV double-area and geometric cross length, source raw CORNER normal, Cycles uint32 packed/decode reference, original fan custom short2 normal, tangent and handedness. Duplications retained; none filled, excluded, merged or replaced.

| Case | Canonical | Raw float ablation | Rest triangle ablation |
|---|---:|---:|---:|
| Strong 6 | 8 | 9 | 6 |
| Startle 1 | 4 | 5 | 9 |
| Startle 11 | 5 | 4 | 5 |
| Strong 44 | 7 | 12 | 5 |
| Total | 24 | 30 | 25 |

For every zero tangent, geometry cross length and UV signed area are nonzero in both float32 and float64. Canonical geometry cross lengths range 5.5763e-11–8.2628e-8 in evaluated mesh local coordinates; absolute UV signed double-areas range 2.7201e-11–1.8922e-9. Thus tiny triangles/UVs are associated with these results, but exact zero triangle area is not established as the cause.

Pinned Mikk source handling: mikk_float3.hh normalize() returns the input when length==0 (line92); project() normalizes the projected vector (line115). mikktspace.hh initializes TSpace tangent to (1,0,0), but first accumulated Group replaces that default (lines107–130). Group normalization preserves zero, and SetTangentSpace writes resulting TSpace without replacing zeros (lines89–92,211). Group projection/angle-weighted accumulation (lines776–825) can yield zero contribution or zero group sum; these source branches permit zero output. The saved arrays alone do not reveal which group path occurred for each row. Do not infer that every zero is source-authored degeneracy, or that the installed Cycles renderer must output these exact zeros. Independent source code is included unchanged under Apache-2.0.

Pinned Cycles svm_node_normal_map is in kernel/svm/tex_coord.h, reached from svm.h NODE_NORMAL_MAP. In tangent mode it falls back to sd->N for absent object/non-triangle or absent tangent/sign attributes. Otherwise it interpolates unnormalized tangent/sign, obtains smooth normal, computes B=sign*cross(normal,tangent), applies strength and safe_normalize(to_global(color,tangent,B,normal)), transforms to world space and handles backfacing. Final zero/nonfinite N falls back to sd->N. There is no per-corner zero-tangent replacement here. With interpolated tangent exactly zero, B also zero; mapped result depends on color.z, normal and barycentric interpolation. A zero at one corner does not imply a whole triangle's interpolated tangent is zero. This is static branch analysis, not a executed shader/render equivalence test.

Canonical/raw/rest zero counts differ with unchanged original source geometry inputs. This demonstrates algorithm-input sensitivity; it does not prove whether packing, projection precision, group cancellation, SIMD/FP flags or wrapper/build context caused a particular zero. Harness compiled with explicit /fp:precise, serial Mikk and x64 pinned SSE headers. Installed Blender/Cycles compiler configuration and actual native renderer buffers are not proven equivalent. Obtain actual buffer readback and, if warranted, group instrumentation before attributing root cause. No rendering tolerance waiver or source cleanup is justified.

First metadata attempt referenced a nonexistent polygon_material_index key; corrected to the frozen archive's polygon_material_slot and reran only metadata analysis. All four algorithm and four input NPZ hashes and original topology/rest basis hashes were verified. Original source files and frozen packets remain unchanged.

Next bounded candidate: review exact 79 source identities and instrument native Mikk group contributions or actual Cycles attribute buffers with matching compiler configuration. Keep R4 immutable and preserve original runtime CORNER-normal gate.
