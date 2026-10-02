"""
Export a shot handoff package from Blender (bpy).

Usage (inside Blender):
  blender scene.blend --background --python export_previs_package.py -- \
    --output /path/to/package --shot-id shot_001

This script is deterministic when scene/render settings are fixed.
Pose/skeleton projection and motion vectors are optional hooks; if bpy
or required objects are unavailable, those control passes are skipped.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import bpy  # type: ignore
except ImportError:
    bpy = None  # type: ignore


def _parse_args(argv: list[str]) -> argparse.Namespace:
    if "--" in argv:
        argv = argv[argv.index("--") + 1 :]
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--shot-id", required=True)
    parser.add_argument("--beauty-pass-name", default="beauty")
    return parser.parse_args(argv)


def _sha256_file(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _camera_keyframes(scene: object, frame_start: int, frame_end: int) -> list[dict]:
    cam = scene.camera
    if cam is None:
        raise RuntimeError("scene has no active camera")
    keyframes = []
    for frame in (frame_start, frame_end):
        scene.frame_set(frame)
        loc = cam.matrix_world.to_translation()
        rot = cam.matrix_world.to_euler()
        keyframes.append(
            {
                "frame": frame,
                "location": [loc.x, loc.y, loc.z],
                "rotation_euler_xyz_rad": [rot.x, rot.y, rot.z],
                "focal_length_mm": float(cam.data.lens),
            }
        )
    return keyframes


def _configure_pass_output(scene: object, pass_type: str, out_dir: Path) -> None:
    scene.render.filepath = str(out_dir / pass_type / f"{pass_type}_")
    # Beauty RGB uses default Combined; depth/normals/masks require view layers + compositor
    # R1: caller should preconfigure compositor; this script only triggers render writes.


def export_package(args: argparse.Namespace) -> dict:
    if bpy is None:
        raise RuntimeError("bpy not available; run inside Blender")

    scene = bpy.context.scene
    frame_start = int(scene.frame_start)
    frame_end = int(scene.frame_end)
    width = int(scene.render.resolution_x)
    height = int(scene.render.resolution_y)
    fps = float(scene.render.fps / scene.render.fps_base)

    blend_path = Path(bpy.data.filepath) if bpy.data.filepath else Path("untitled.blend")
    blend_hash = _sha256_file(blend_path) if blend_path.is_file() else "0" * 64

    script_path = Path(__file__).resolve()
    script_hash = _sha256_file(script_path)

    manifest: dict = {
        "manifest_version": "1.0.0",
        "shot_id": args.shot_id,
        "timeline": {"fps": fps, "frame_start": frame_start, "frame_end": frame_end},
        "image": {
            "width": width,
            "height": height,
            "aspect_ratio": f"{width}:{height}",
        },
        "camera": {
            "sensor_width_mm": float(scene.camera.data.sensor_width),
            "default_focal_length_mm": float(scene.camera.data.lens),
            "keyframes": _camera_keyframes(scene, frame_start, frame_end),
        },
        "characters": [],
        "render_passes": [],
        "control_passes": [],
        "prompts": {"prompt": "", "negative_prompt": ""},
        "seed": {"value": 0, "policy": "provider_assign"},
        "optional_hooks": {
            "pose_projection": "skipped_unavailable",
            "motion_vectors": "skipped_unavailable",
        },
        "provenance": {
            "authoritative_sources": [
                {"uri": blend_path.as_uri(), "sha256": blend_hash, "role": "blend"},
                {"uri": script_path.as_uri(), "sha256": script_hash, "role": "bpy_script"},
            ],
            "export_tool": "previs/blender/export_previs_package.py",
            "export_mode": "blender",
            "blender_runtime": "PASS",
            "exported_at": datetime.now(timezone.utc).isoformat(),
        },
    }

    out_root = args.output / args.shot_id
    out_root.mkdir(parents=True, exist_ok=True)

    beauty_dir = out_root / "passes" / "beauty"
    beauty_dir.mkdir(parents=True, exist_ok=True)
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(beauty_dir / "beauty_")
    bpy.ops.render.render(animation=True)

    manifest["render_passes"].append(
        {
            "id": "beauty",
            "type": "rgb",
            "relative_path": "passes/beauty/beauty_%04d.png",
            "frame_start": frame_start,
            "frame_end": frame_end,
        }
    )

    cam_json = out_root / "control" / "camera_trajectory.json"
    cam_json.parent.mkdir(parents=True, exist_ok=True)
    cam_json.write_text(
        json.dumps({"keyframes": manifest["camera"]["keyframes"]}, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest["control_passes"].append(
        {
            "id": "camera_trajectory",
            "type": "camera_json",
            "relative_path": "control/camera_trajectory.json",
            "optional": False,
            "sha256": _sha256_file(cam_json),
        }
    )

    manifest_path = out_root / "shot-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    args = _parse_args(sys.argv)
    export_package(args)


if __name__ == "__main__":
    main()
