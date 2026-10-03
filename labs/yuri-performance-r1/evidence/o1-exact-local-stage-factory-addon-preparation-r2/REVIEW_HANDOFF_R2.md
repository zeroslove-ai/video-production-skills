# Factory-addon assertion correction: file-only R2 preparation

2026-10-03 KST. Failed one-attempt capture is frozen at026a581, PID114608. Both collector empty-inventory failure and independent strict LIVE image error5 remain FAIL; cleanup exit93/Active0/PIDs[] and file hashes are separate scoped evidence. No additional Blender/probe/inventory-only process, preferences edit or addon surgery occurred.

## What installed files actually establish

Installed `5.2/scripts/modules/addon_utils.py` lines41–53 explicitly says hidden core addons do not appear in `bpy.context.preferences.addons`, and Cycles cannot be hidden because it needs preferences. Its `_initialize_once()` lines56–83 enables the five hidden core modules first, then iterates preference addons. The exact AST set is **bl_pkg, io_anim_bvh, io_curve_svg, io_mesh_uv_layout, io_scene_fbx**. `bpy/utils/__init__.py` records `bpy.app.factory_startup` and chooses `use_user = not _is_factory_startup` for script loading. These installed control files are SHA-pinned in the manifest, not imported/executed in this investigation.

This proves the prior blanket “empty preference addons” criterion is not a sound identity criterion. It **does not recover** PID114608's actual enabled names. Exact compiled factory preference membership is absent from the inspected Python sources and remains **UNKNOWN**. No third-party/account/plugin cause is attributed to the failed assertion. The failed log's missing third-party markers is only a log check.

## Proposed trust gate, not a claimed factory-default list

The candidate allowlist is the13 existing installed `addons_core` package roots, each with exact entry path/SHA and complete Python-source tree hashes: **bl_pkg, cycles, hydra_storm, io_anim_bvh, io_curve_svg, io_mesh_uv_layout, io_scene_fbx, io_scene_gltf2, node_wrangler, pose_library, rigify, ui_translate, viewport_vr_preview**. They were enumerated and entry AST metadata read from the existing installation, not downloaded. All13 are **installed bundled origin candidates**; only the five hidden core names have explicit always-startup-enable evidence in the inspected code. The other eight are not asserted enabled or factory-default. Package/source hashes prove custody of this inspected installation, not a separately obtained vendor signature. PM must review this exact allowlist scope before execution.

New helper inspects the union of preferences names and already-loaded modules with `__addon_enabled__ is True`. It never imports a missing addon, calls register/unregister, or changes preferences. For each name it records loaded/enabled state, resolved `__file__`, `__spec__.origin`, origin SHA and classification. Allowed names must resolve exactly to their pinned installed entry with matching SHA and enabled flag. External/user/extension/unknown names or origins fail. All pinned package Python/control files are checked. Before/after inventory JSON is written even when a gate rejects; no missing module is silently accepted. Factory flag must be true.

This is a post-startup origin gate; it cannot undo startup behavior or prove absence of earlier network side effects. The helper's complete Python-tree pins do not claim full native-binary dependency attestation. Factory/offline CLI and no account/network operations remain. No global preferences modification is proposed.

## Minimal bounded collector change and fixed route

R2 collector changes fixed output/proposal/receipt paths and replaces the empty assertion with the read-only inventory/origin gate. It adds a second gate after restoring the source scene; enabled/preferences names must match before/after. Existing native local position/CORNER getters, original63561/254602 topology IDs, full304799 ordered CSR/37310 zeros, rest/pose/bodyWorld, disposable-copy cumulative seven-stage evaluation, original stack/factors/drivers, exact stage6 frozen reference and full scene/input preservation requirements remain.

The separate R2 launcher changes **fixed paths only**. File-only reverse comparison proves its executable resource/identity/terminal logic equals R1. Missing image on an unsignaled genuinely LIVE owned handle remains FAIL; authoritative signaled exit then Active0/PIDs[] remains required. No retry path or relaxed gate is introduced. R1/R5 guard failure history is unchanged.

New immutable output directory is `outputs/o1-exact-source-local-stage-capture-r2`. Exact R2 proposal/config/launcher/collector/helper/manifest hashes and argv are in this packet. Receipt template is approval FALSE and not placed at the executable receipt path. Consumed R1 approval cannot run R2. A new exact receipt and PM review are required before any native capture; this turn does not request or infer launch approval.

## Validation actually performed

Saved collector/launcher/helper AST/compile, installed entry AST/control-set inspection, pinned file hashes, source/action/recipe/final-reference identity, launcher reverse-diff and ZIP CRC passed. Actual enabled inventory, origin gate inside Blender, native stage captures/full-scene restoration, guard race/resource/terminal behavior for R2 are **NOT_RUN**. Exact factory membership remains unknown. No motion arrays or numeric/runtime/PBR acceptance are claimed.

Frozen R2 packet43242bytes SHA256597afc3192cf720e605c56a0c654e410fda79ab66c5cc48f09a9c7ed07e0d290 includes hashes/metadata and saved code only; source model/full weights/native arrays are excluded. This additive review note sits beside the frozen ZIP. Next bounded task is PM review of the exact installed-origin candidate scope and new receipt-bound route before a single native capture.
