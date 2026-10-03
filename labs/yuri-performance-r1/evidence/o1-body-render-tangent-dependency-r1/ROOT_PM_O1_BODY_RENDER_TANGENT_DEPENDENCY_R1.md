# Original R4 Body render tangent dependency — 2026-10-03

**Runtime tangent/PBR proof remains HOLD.** Source graph/dependency and pinned renderer code are identified without another Blender job, render, export, source save, triangulation edit, normal regeneration, static-normal substitution or threshold change. Immutable R4 and the existing native-carrier adapter remain authority; no product/PM writes.

## Actual Body shader

All three original Body material slots reference `R4_Meshy_OriginalDetail_FaceMatched`. Its active `ALL` Material Output Surface is connected to Principled BSDF; there are exactly these normal-related links:

`Original Meshy Normal - safe derived 4K.Color → Normal Map.Color → Principled BSDF.Normal`.

| Setting | Exact source value |
|---|---|
| Normal Map space | TANGENT |
| Strength | 0.3499999940395355, unlinked, not muted |
| Convention / base | OPENGL / DISPLACED |
| UV name | empty node name selects default; Body's sole active/render UV is UVMap |
| Texture | R4_Meshy_Normal_Safe_4K, 4096×4096, Non-Color / is_data=true |
| Image Texture | Linear interpolation, FLAT projection, REPEAT; Vector unlinked |
| Packed image | `textures/08_00.png`, 3,808,709bytes; SHA256 aa1ca76133eb9774fad2add96e72504821488e95dd51bd2544eddfa8221f6430 |
| Bump/displacement | No connected ShaderNodeBump; Material Output Displacement unlinked |
| Principled anisotropy | 0, unlinked; tangent input unlinked |

The material property `displacement_method=BUMP` does not establish a connected Bump node. The connected Normal Map is a real tangent-space dependency. Do not set strength to0, remove the image or substitute static normals to get a superficial pass. Normal strength must be matched semantically by the consumer shader; assigning the same number to a differently defined normal-scale operation is not proof.

## Corrected canonical render path

Frozen source render engine is **CYCLES**; Body has only seven deform-only modifiers, no subdivision modifier. Pinned [Cycles Blender mesh exporter](https://github.com/blender/blender/blob/9e2066aef7ef/intern/cycles/blender/mesh.cpp) obtains the evaluated mesh's `corner_tris`, maps source CORNER UV/normals to triangle corners, and builds Cycles triangles. Thus the400 Body ngons are tessellated for rendering without changing canonical source topology.

[Cycles scene mesh](https://github.com/blender/blender/blob/9e2066aef7ef/intern/cycles/scene/mesh.cpp) calls its own Mikk wrapper through `Mesh::update_tangents`. That wrapper presents **three vertices per face**. It does not reconstruct source quads. Smooth triangles use decoded packed CORNER normals when available; flat triangles use their geometric triangle normal. This is distinct from **BKE general `calc_uv_tangents` with quad reconstruction**, and from **RNA `Mesh.calc_tangents` restricted to tris/quads**. Do not call the BKE quad path the actual canonical Cycles render path. All use Mikk, but their supplied faces/normal precision can differ.

Pinned [Cycles packed normal](https://github.com/blender/blender/blob/9e2066aef7ef/intern/cycles/util/types_normal.h) encodes unit normals octahedrally into a32-bit value with two16-bit components; the wrapper decodes before Mikk. This renderer representation is **different from original Blender fan-space `custom_normal` short2** and from the frozen float32 BKE CORNER reference. Compare matching stages/domains; keep the BKE normal accuracy gate separate from renderer packing/tangent/PBR comparison. No precision waiver is inferred.

Pinned [NormalMapNode compiler](https://github.com/blender/blender/blob/9e2066aef7ef/intern/cycles/scene/shader_nodes.cpp) requests standard UV tangent/sign for the source's empty UV name + DISPLACED base. OPENGL sets compiler `invert_green=0`. The shader strength/image remain source values. These code/graph checks establish the requested dependency, **not an observed renderer tangent buffer or final normal-map output**.

## Scope across21 meshes

The machine receipt walks all active ALL/CYCLES output graphs backwards for the12 materials assigned to the21 source meshes. It lists each original material slot, connected NormalMap/Bump/Tangent nodes, texture metadata, UV availability and polygon sizes. There are no unresolved nested shader groups in this set. Shared-material repeats do not collapse source slot identity.

- Body: 399 pentagons + one heptagon; original RNA tangent calculation explicitly unsupported, with no Body tangent array. Its connected normal texture makes renderer tangents necessary.
- LowerLashesClean.L/R:24/26 hexagons; **no source UV**, material `Face_LowerLash_Pigment` contains only Principled/Output and no NormalMap/Bump/Tangent nodes. No UV tangent call was attempted, so do not label them a recorded RNA failure. Their geometric/CORNER normal and transparency/material gates remain.
- Other meshes: original tri/quad UV tangent references exist where UV is present; actual assigned connected dependencies are itemized. Existing head/eye evaluated gaze-corner/tangent references remain their source authority, not a full Cycles/Unity PBR proof.

## Minimum missing evidence / next consumer input

The source metadata proves actual material settings, links, texture bytes, UV defaults and non-subdivision render path. It does **not** capture dynamic Cycles triangle tessellation, packed-normal/tangent buffers or shader-applied normal output for animated Body frames. Frozen original triangulation is not an all-frame render tessellation claim. Do not start another probe without separate authorization.

Laptop can first provide actual clone normals/tangent4/UV0/triangle-corner correspondence, source-local/world K matrices and winding/mirror/UV-V-flip conventions. Confirm texture SHA, Non-Color sampling, OpenGL green convention, applied strength and shader negative-scale sign behavior. If exact canonical Cycles tangent proof is required, the smallest additional source capture is those actual dynamic render triangle/packed normal/tangent/sign buffers at the selected QA frame, with compiler/backend settings and source-loop mapping. Preserve runtime tangent/PBR **HOLD** until that capture/comparison is authorized and passes.

The receipt rehashes the original normal texture and references existing material/source/corner receipts. Official pinned Cycles files are unmodified Apache-2.0, with license and URL/hash provenance included. Guessed `mesh_tangent.cpp`/`normal_map.h` paths returned404; investigation found the actual implementation in scene/mesh.cpp without replacing the task with a render. Saved plain-Python inventory and packet hash/CRC checks are reproducible; no competing shader implementation was created.
