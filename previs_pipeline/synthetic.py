from __future__ import annotations

import json
import struct
import zlib
from pathlib import Path
from typing import Any

from previs_pipeline.hash_util import sha256_bytes, sha256_file
from previs_pipeline.manifest import build_manifest_skeleton
from previs_pipeline.package import attach_pass_hashes, write_manifest


def _minimal_png(width: int, height: int, rgb: tuple[int, int, int]) -> bytes:
    """Deterministic solid-color PNG without external deps."""

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)

    raw_rows = b"".join(b"\x00" + bytes(rgb) * width for _ in range(height))
    compressed = zlib.compress(raw_rows, level=9)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", compressed) + chunk(b"IEND", b"")


def _write_frame_sequence(
    out_dir: Path,
    prefix: str,
    frame_start: int,
    frame_end: int,
    width: int,
    height: int,
    base_rgb: tuple[int, int, int],
) -> str:
    out_dir.mkdir(parents=True, exist_ok=True)
    for frame in range(frame_start, frame_end + 1):
        t = (frame - frame_start) / max(1, frame_end - frame_start)
        rgb = (
            min(255, base_rgb[0] + int(40 * t)),
            base_rgb[1],
            min(255, base_rgb[2] + int(30 * (1 - t))),
        )
        path = out_dir / f"{prefix}_{frame:04d}.png"
        path.write_bytes(_minimal_png(width, height, rgb))
    return f"passes/{out_dir.name}/{prefix}_%04d.png"


def build_demo_r1_package(
    output_dir: Path,
    fixture_path: Path | None = None,
) -> dict[str, Any]:
    """
    ~12s @ 24fps synthetic previs package (frames 1–288).
    Blender runtime is explicitly NOT_TESTED.
    """
    repo_root = Path(__file__).resolve().parents[1]
    fixture_path = fixture_path or repo_root / "previs" / "fixtures" / "demo_r1" / "synthetic_scene.json"
    with fixture_path.open(encoding="utf-8") as f:
        scene = json.load(f)

    fixture_path = fixture_path.resolve()
    fixture_bytes = fixture_path.read_bytes()
    fixture_hash = sha256_bytes(fixture_bytes)
    authoritative_sources = [
        {
            "uri": fixture_path.as_uri(),
            "sha256": fixture_hash,
            "role": "synthetic_fixture",
        }
    ]

    shot_id = scene["shot_id"]
    fps = float(scene["fps"])
    frame_start = int(scene["frame_start"])
    frame_end = int(scene["frame_end"])
    width = int(scene["width"])
    height = int(scene["height"])

    manifest = build_manifest_skeleton(
        shot_id,
        fps=fps,
        frame_start=frame_start,
        frame_end=frame_end,
        width=width,
        height=height,
        aspect_ratio=scene["aspect_ratio"],
        prompt=scene["prompt"],
        negative_prompt=scene.get("negative_prompt", ""),
        export_mode="synthetic",
        authoritative_sources=authoritative_sources,
        blender_runtime="NOT_TESTED",
    )
    manifest["provenance"]["notes"] = (
        "R1 synthetic fixture; no live Blender bpy execution in this worker."
    )
    manifest["characters"] = scene.get("characters", [])

    package_dir = output_dir / shot_id
    package_dir.mkdir(parents=True, exist_ok=True)

    pass_specs = [
        ("beauty", "rgb", (180, 140, 120)),
        ("depth", "depth", (80, 80, 200)),
        ("normals", "normals", (120, 180, 120)),
        ("object_mask", "object_mask", (30, 30, 30)),
        ("character_mask", "character_mask", (220, 60, 60)),
    ]
    render_passes: list[dict[str, Any]] = []
    for pass_id, pass_type, rgb in pass_specs:
        rel_pattern = _write_frame_sequence(
            package_dir / "passes" / pass_id,
            pass_id,
            frame_start,
            frame_end,
            width,
            height,
            rgb,
        )
        render_passes.append(
            {
                "id": pass_id,
                "type": pass_type,
                "relative_path": rel_pattern,
                "frame_start": frame_start,
                "frame_end": frame_end,
            }
        )
    manifest["render_passes"] = render_passes

    camera_meta_path = package_dir / "control" / "camera_trajectory.json"
    camera_meta_path.parent.mkdir(parents=True, exist_ok=True)
    camera_payload = {
        "shot_id": shot_id,
        "fps": fps,
        "keyframes": manifest["camera"]["keyframes"],
    }
    camera_meta_path.write_text(json.dumps(camera_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest["control_passes"] = [
        {
            "id": "camera_trajectory",
            "type": "camera_json",
            "relative_path": "control/camera_trajectory.json",
            "optional": False,
        }
    ]

    rep_frames = [frame_start, (frame_start + frame_end) // 2, frame_end]
    sheet_path = package_dir / "meta" / "contact_sheet.png"
    sheet_path.parent.mkdir(parents=True, exist_ok=True)
    sheet_path.write_bytes(_minimal_png(width * 3, height, (90, 90, 110)))
    manifest["keyframes_contact_sheet"] = {
        "representative_frames": rep_frames,
        "contact_sheet_relative_path": "meta/contact_sheet.png",
        "columns": 3,
    }

    manifest = attach_pass_hashes(manifest, package_dir)
    if camera_meta_path.is_file():
        manifest["control_passes"][0]["sha256"] = sha256_file(camera_meta_path)
    if sheet_path.is_file():
        manifest["keyframes_contact_sheet"]["sha256"] = sha256_file(sheet_path)

    write_manifest(package_dir, manifest)
    return {"package_dir": package_dir, "manifest": manifest, "fixture_hash": fixture_hash}
