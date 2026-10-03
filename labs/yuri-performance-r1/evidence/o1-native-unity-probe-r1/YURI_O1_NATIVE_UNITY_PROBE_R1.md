# O1 R4 native export compatibility probe R1

**Completed bounded experiment; appearance/Unity promotion HOLD.** Source R4 remains the immutable visual authority. This carrier is a compatibility test, never a canonical character or replacement GameRig. No product repo, shared Blender GUI, old artifacts, source mesh/material/weights/rest/driver changes.

## Accepted source evidence

Source SHA256 `a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa` unchanged. Before/after exporter component diff={}; all78 original Actions retained. No new rig or geometry, no merge/prune/donor substitution. Original4rigs:57body +57face +10hair +13board.51 consumer semantic paths match native paths as metadata only. Source scale0.535 applied once, no second height normalization.

Native OFF→ON→OFF geometry delta0m for21 meshes. Fresh source neutral render versus frozen authority:0 unequal pixel channels (960×920). Shader, material slots, ShapeKeys, weights, rest and drivers preserved in native authoring. Existing action-only library reused, not regenerated.

## Motion and rest gates

All6 clips actually move nonroot bones; Light/Strong sampled2cycles. Root excursions remain original authored compression (0–0.033m), no gravity trajectory. Six FBX stacks,24fps, durations1.5/1.25/2.5/2/1.75/2.25s. Export uses original source OBJECT slot OBMeshy_Fitted_Rig; Blender import creates generic OBSlot bound explicitly by exported object+take. QA Release/sequence not exported.

Position error max 1.36459575e-06m; rotation error max 0.00211248101° using normalized quaternion dot in Python double. Combined position<1e-4m AND rotation<0.001° **FAIL**, independently of actual motion PASS. Earlier Quaternion.angle reported0° due float resolution; this has been corrected, tolerance not loosened.

Ordered names/parents/counts match model and motion. Local-rest matrix gate1e-5 **FAIL**: body thigh.L max1.138448715e-5 (scale delta1.132488251e-5); face J_Bip_L_Index3 max4.565156996e-5, translation2.504889911e-7m, rotation0.003331253°. Worst animation rotation also that face index bone. Full source/model/animation world/local TRS differences perbone in rest_matrix_decomposed_by_bone.json. Small neutral bind effect is measured below; this does not waive static contract. Serialized default properties themselves differ, not merely importer reconstruction; identical settings/axis/unit/parents do not imply identical floating defaults. Some missing versus explicit identity properties also differ harmlessly and are shown unfiltered in wire evidence.

## Exact carrier defects

Neutral geometry max corresponding vertex error ~2.81e-7m, all21 mesh counts equal. Numeric skin bone influence error0; omitted zero entries and procedural mask groups declared separately. Mesh/ShapeKey/material slot counts retained (see permesh report); FBX material graphs are not native graphs.

Same camera/lights/world, actual FBX materials and deformation: 1032207 unequal RGBA8 channels, mean error 2.32548856/255. Visible eye iris/gaze material loss, washed face/hair shading. **Visual FAIL.** No source shader/modifier was copied into the imported carrier to hide this failure.

Motion mesh worst 0.00392865436m on Meshy_Body_NeutralCovered in YRA_R4_Struggle_Strong_Loop frame1. Native DQ + masked second LBS + corrective/smooth stack becomes conventional FBX skinning. Gaze Geometry Nodes, expression/hair driver logic, board-driven morph behavior and arbitrary shader graphs are not executable FBX content. Bone follower motion is evaluated/baked for these6 takes only; this does not recreate future constraints/driver behavior. Deformation difference is a combined measured effect; individual causal contributions have not been isolated.

## Playback evidence and boundary

visual/source_vs_actual_FBX_24fps.mp4: left native / right actual FBX,15.75s,378frames24fps. Full interval rendered for6 clips and2 loop cycles each, no speed remap/interpolation. Perclip hard cuts are intentional diagnostic segmentation; no smooth sequence or runtime state graph acceptance claimed. Both full native/imported videos included. Contact sheet supplements complete videos and all-frame bone checks. CPU only; GPU PRODUCT_EXCLUSIVE untouched. Unity state entered/normalizedTime/weight/AlwaysAnimate/actual mesh playback **PENDING consumer test**, never Unity PASS.

## Narrow next adapter requirement

Consumer/PM should decide a source-preserving runtime adapter contract before another export: resolve exact rest/default matrix and bind representation, keep4native hierarchy/137bones/nondeform helpers, evaluate future face/gaze/hair board logic, preserve source material appearance and DQ/masked skin behavior. No new GameRig/geometry, source rig edits or silent shader replacement. If Unity cannot execute these original procedures faithfully, remain HOLD and retain Blender Action/NLA as canonical animation path. This worker stops at this bounded probe; no next production task.

## Reproduction

Fresh Blender5.2.1 LTS `--factory-startup --background --disable-autoexec --python-exit-code 1`; run export, roundtrip, wire, matrix_analysis, visual(native), visual(imported), package scripts in order. Scripts are in scripts/; original immutable source and action library are in source/. Adjust script absolute OUT path on another host. Native source never saved. Consumer intake refs8a1bba98/825a7f87 and PM reporting037b1f40 recorded; latest reporting addendum2d828a81 used for structured checkpoint. Failures: initial importer exact source Action-slot expectation rejected because imported slot is generic OBSlot; explicit target+slot fixed in scratch data only. Static/rotation/procedural failures retained, no threshold relaxation or corrective character rebuild.
