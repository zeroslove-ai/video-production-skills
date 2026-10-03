# R4 source fidelity recovery data R1 — 2026-10-03 KST

**Bounded source-data packet complete. Product/appearance promotion remains HOLD.** Parent research commit d204379b and immutable probe ZIP4ec5c10... remain unchanged. No canonical geometry/material/rig/driver/rest/Action changes, no Unity product edits or shared GUI edits; all jobs CPU-only.

## Coverage and immutable reuse

Prior frozen ZIP SHA256 `4ec5c10ce90d7d25c06721b7dcd3832be4b7672190c975d42912be876a5a0843` is required. REUSE_COVERAGE_POINTERS.json contains exact internal paths/bytes/hashes; extract it once and use pointers. This packet adds missing executable data, not another source master or rebuilt GameRig.

| Requirement | Disposition | Exact data paths |
|---|---|---|
| Material slot→polygon/UV/texture bytes/math | PROVIDED | mesh_slot_UV_attributes_shape_deltas.json; executable_material_graphs.json; exact_texture_receipt.json; data/*_original_mesh.npz; textures/* |
| Neutral albedo/opacity/normal/masks | PROVIDED_WITH_LIMITS | NEUTRAL_BAKE_RECEIPT.json; neutral_bakes/*.exr; CORNER_BASIS_RECEIPT.json; data/*_corner_basis.npz |
| Camera/lights/color/driver state | PROVIDED | neutral_camera_light_color_driver_state.json |
| FaceBoard13/face/gaze/hair executable dependencies | PROVIDED_WITH_OWNERSHIP_HOLD | controls_contract.json; executable_driver_dependencies.json; executable_geometry_node_graphs.json; evaluated_driver_geometry_references.json; CONTROL_CAUSAL_RECEIPT.json; MATERIAL_SHADER_DRIVER_RECEIPT.json; MANUAL_MORPH_RECEIPT.json |
| ShapeKey basis/delta/default correspondence | PROVIDED | mesh_slot_UV_attributes_shape_deltas.json; data/*_original_mesh.npz |
| DQ/maskedLBS/GN/surface masks/order/normals | PROVIDED | DEFORMATION_LAYER_RECEIPT.json; exact_mask_coverage.json; data/Strong_1_49_deformation_layer_ablation.npz; data/motion_*.npz; data/gaze_*.npz |
| Bind/rest transport and influence support | PROVIDED_GATE_FAILS | *_bind_and_OFF_LBS.json; LBS_bind_motion_transport_metrics.json; worst_rest_bone_skin_support.json; full_deformation_RMS_percentiles.json; STATIC_CAUSAL_SEPARATION.json; static-correction/* |
| F0/F1/F2/F3 and promotion | HOLD | RECOVERY_DISPOSITION.json; manual_morph_proof/Existing_Blink_Smile_Jaw_24fps_3s.mp4 |

Texture15 files are original packed bytes without re-encoding, with image dimensions/channels/space/alpha.19 source material graphs include types/operations/socket defaults/links/image/attribute names and mapping/interpolation. Slot/polygon/loopUV/basis/relative morph deltas/attributes and corner normals/tangents have stable source indices in float32 NPZ; NPZ array names and JSON paths define correspondence. Current FBX roundtrip counts/index positions match; if a consumer splits vertices, it must retain explicit polygon-loop→source index mapping, never assume Unity vertex order.

Neutral CPU bake references are diagnostic Base Color/Alpha-input/Tangent Normal in unchanged UVs,512px32bit linear EXR, not replacement source textures or full PBR shader equivalence. Alpha is stored in RGB; A is atlas coverage. All roughness/IOR/transmission/emission/metallic/normal strengths and masks remain exact graph inputs. Where compatible scalar roughness is converted, smoothness=1-roughness reversibly, no visual retuning. Combined slot UV overlaps can limit atlas references; original polygon/UV/node/attribute semantics outrank a bake. Hair has no UV; its original constant shader and geometric normals/tangents policy are explicit rather than inventing UVs.

## Source expression ownership recovered without unmuting

Source13 head FaceBoard bridge Fcurves are muted but valid; factory `--disable-autoexec/use_scripts=False` has no autoexec error, missing custom namespace or invalid drivers. Read-only GUI confirms same13mute flags, clean/frame1.872 object/Key/GN/material-ID drivers +8material-owned ShaderNodeTree drivers =880 total,13muted. Shader-owned drivers are included separately because they are not in bpy.data.node_groups.

Board sliders LOCAL Y0..0.055m target geometry shape-key values (not shader-only controls); their head bridges remain0 in current source. Runtime DriverVariable values have no public RNA accessor; evaluated bone channels/matrices, declared variables/paths/spaces, downstream Key/GN/shader outputs are provided without pretending to access the private evaluator.

Existing direct head morph input works: Blink max16.0845mm including attached lashes; Smile2.39016mm; Jaw5.45469mm; Brow2.59992mm. Peak/RMS/affected vertices/defaults/connected shader output measured; OFF geometry0m and diagnostic first/last pixels0difference. Existing_Blink_Smile_Jaw_24fps_3s.mp4 is a72frame1x triangular control fixture (not performance design). Source driver definition/mute policy untouched. Body-only ReactionLane does not own face. No author declaration explaining original13mute policy found in relevant adapter/build/evidence reads; PM must choose manual-morph versus board-driven runtime ownership explicitly. No automatic unmute or face redesign.

## Deformation causality and bind are distinct

Frozen native versus FBX Strong1 max3.928654mm, RMS0.415242mm, p95 0.844805mm, p99 2.121519mm; worst original body vertex47693. Float64 first-armature pure LBS transport mismatch max1.231315µm across6clips×4samples×21renderers, so this transport shadow cannot explain the millimeter-scale native procedure deficit. True source native deformation remains authority; pure LBS is not promoted.

Staged read-only source-mesh object-copy ablation Strong1: DQ↔LBS max3.928732mm, DQ versus DQ+maskedLBS1.435946mm, surface stack addition1.454683mm.49 end behaves similarly. These component effects are not additive scalar allowances. Copy removed; source fingerprint diff={}. Exact masks/order/settings and dense layer arrays provided. Affected thigh.L descendants influence18161body vertices, Hair_Pony_03 influences1025hair vertices; face J_Bip_L_Index3 has0positive skin influences, but strict rest gate remains independent of that count.

## One bounded static correction — not promoted

Exporter input unchanged and source fingerprints0difference. Blender Model serializer uses evaluated pose (`fbx_object_tx(rest=False)`), while skin BindPose/Cluster uses raw rest; NLA animation gathering precedes Model writing. One disposable exporter correction caches original OFF Model default TRS from model and replays exactly those defaults only in animation Model serialization. Animation curve evaluation remains unchanged. Original effective default mismatch9.156722356e-5 component (Euler degrees/scale/translation depending property) becomes0. Raw wire omission-versus-explicit identity still differs, but effective defaults match exactly.

Importer uses Pose/Cluster bind matrices in model (34Pose objects/1150Cluster records), but animation-only has0Pose/0Cluster and falls back to Model default matrix. Source raw rest and evaluated neutral are not interchangeable. Bind/default paths and float decomposed/normalized bone construction are therefore separately evidenced; not every coefficient is attributed solely to precision.

Corrected candidate still FAILS strict rest: body1.050531864e-5, face4.563480616e-5, hair2.384185791e-6, board0. Rotation-inclusive pose gate still FAILS (~0.002111216° versus<0.001°). Six actual motions/2loop cycles continue PASS, which does not waive fidelity. Candidate files/versioned SHA receipts stay diagnostic. No consumer rest rewrite or tolerance relaxation. Next narrow serializer feasibility would transport original skeleton bind/rest matrices consistently into meshless motion, not change source rig; no second export trial launched.

## Quality layers and next consumer boundary

F0: native/Blender import functionality and direct existing morph references. Unity functional gate pending. F1: physical contact/root/transition acceptance unverified. F2: not certified—combined pose/timing/hands/head/gaze/face/secondary and normal1x multiple product-camera review still required. F3: not claimed. The owner anime performance North Star was read and does not authorize new dance or character redesign here.

Consumer owns exact texture/UV/slot/node restoration on isolated Unity candidate and separate driver/morph/DQ/GN/surface adapter feasibility. PM must disposition manual face ownership and strict bind/rest serialization first. Existing full normal-speed6clip video is reused by hash pointer and remains HOLD; this packet has not re-rendered or passed corrected-carrier appearance/normal-speed source fidelity. No material recoloring, approximate local-control head, shader compensation or newGameRig is authorized.

## Reproduction

Scripts preserved in research branch and scripts/; existing project paths are explicit. Order inspect→source_data→neutral_bake→static_correction(one trial)→static_analysis→bind_analysis→control_causal→corner_basis→deform_layers→manual_morph→shader_drivers→package. Fresh Blender5.2.1 LTS factory background CPU and Python313/PIL/NumPy/FFmpeg. Source originals and prior packet remain input-only; GUI only inspected.
