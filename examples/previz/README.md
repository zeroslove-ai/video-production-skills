# R1 design fixtures

`CS01` CHARACTER_SHORT = 3 shots / 288 frames / 12s.
`WD01` WEB_DRAMA = 6 shots / 720 frames / 30s, two planned audio cues.
`GC01` GAME_CUTSCENE = 6 shots / 576 frames / 24s, last-frame return marker.

All use 24/1 fps, 1280×720, square pixels, source start 1 and edit origin 0.
All ranges are start+duration with an exclusive end. Clip samples continue across cuts; handles are zero.

These are design fixtures, not produced media. Zero SHA256 values, PLACEHOLDER revisions,
pending landmarks/anchors/joint maps and draft reviews deliberately prevent production acceptance.
The proposed validator rejects them under `--production`.

Run from any directory with Python 3.10+ / jsonschema 4.x:

```powershell
python scripts/validate_previz_design.py
```

The validator uses local schemas and makes no network requests. Dependencies are not installed
by this command. Checks cover schema syntax, required fields, IDs, asset consistency,
mode/fps/resolution/reference/preset matching, clip/handle availability, frame coverage,
panel bounds, depth bounds and audio/event ranges. It does not inspect incoming files,
evaluate Blender, approve references, produce OTIO or test artistic quality.

See [architecture](../../docs/VIDEO_PREPRODUCTION_ARCHITECTURE_R1.md),
[blueprints](../../docs/WEB_DRAMA_CUTSCENE_BLUEPRINT_R1.md) and
[handoff](../../docs/COMFY_PREVIZ_HANDOFF_R1.md) before implementing R2.
