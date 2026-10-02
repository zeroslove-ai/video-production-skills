# R1 design validation record

2026-10-02. Windows / Python 3.13.3 / jsonschema 4.26.0. No dependencies installed.
Latest fetched main/base: `29f943115c269d64d651bd641a4718b53236be00`.
The designated branch was recreated from main; only our earlier design commit was reapplied.
PR #4 was inspected read-only, including its branch report, and preserved as OPEN/Draft.

## Performed design checks

```powershell
python scripts/validate_previz_design.py
git diff --check
```

Draft 2020-12 meta-schema and local fixture validation:

```text
PASS SEQ_A: 5 shots, 288 frames
PASS SEQ_B: 12 shots, 720 frames
PASS SEQ_C: 8 shots, 432 frames
DESIGN PASS: 3 sequences / 25 shots / 36 cameras / 15 looks / 25 templates
```

Checks cover unique IDs; shot/sequence source, rate, resolution, mode and reference agreement;
asset/preset revisions; required camera metadata, lens/motion/light recommendations; required
lighting components; placements/subjects; character/body/facial binding, rate and availability;
clip handles; panel/depth bounds; exact V1 coverage; audio source/track ranges; subtitle/event bounds.
Planned outputs are design references and do not prove artifact generation.

In-memory negative probes reject undeclared gaps, body/facial range overruns, nonexistent subjects,
stale assets, incompatible character bindings and unapproved production fixtures. Schema probes reject
unknown fields and zero duration. Explicit gap plus 24000/1001 frame semantics pass. Final probes use
copies of SEQ_A and do not modify fixture files. This is not an OTIO runtime round-trip test.

All JSON parses, local Markdown links resolve, and staged whitespace checks pass. Final comparisons
check that main/experimental refs and original README/skills/MCP/workstation sources remain unchanged.
Required documents, all 23 named camera recipes, all 10 named look recipes, and benchmark durations/
coverage are checked separately. Full benchmark production remains out of scope.

## Visual source inspection

Three small portrait/night/interior images linked from the official Nikon article were downloaded
and directly inspected. Total temporary bytes: 509423. Source hashes are recorded in Reference Cards;
research copies were deleted and are not committed. Usage permission is unverified, so they remain
research-only and cannot automatically become conditioning inputs. Observations, parameter estimates
and proposed Yuri adaptations are separate. No camera motion or duration was inferred as an observed
fact from a still image.

## Not performed

Blender runtime/API compatibility, real asset binding, rendered boards/animatic, eye/face calibration,
depth/mask/pose alignment, audio sync, engine camera handback, OTIO/editor round-trip, Comfy model
execution. PR #4's reported runtime evidence is not counted as execution on this branch.

Schema `$id` URLs are design identifiers, not hosted deployments. R2 must pin exact installed builds,
workflow/model versions, asset hashes and OCIO configuration. Missing runtime evidence is R2 work;
it does not make this design checkpoint a production-readiness certification.
