from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from previs_pipeline import __version__
from previs_pipeline.hash_util import sha256_canonical_json


def derive_shot_seed(shot_id: str, authoritative_sources: list[dict[str, str]]) -> int:
    payload = {"shot_id": shot_id, "sources": sorted(authoritative_sources, key=lambda s: s["sha256"])}
    digest = sha256_canonical_json(payload)
    return int(digest[:8], 16)


def build_manifest_skeleton(
    shot_id: str,
    *,
    fps: float,
    frame_start: int,
    frame_end: int,
    width: int,
    height: int,
    aspect_ratio: str,
    prompt: str,
    negative_prompt: str = "",
    export_mode: str,
    authoritative_sources: list[dict[str, str]],
    blender_runtime: str = "NOT_TESTED",
) -> dict[str, Any]:
    seed_value = derive_shot_seed(shot_id, authoritative_sources)
    return {
        "manifest_version": "1.0.0",
        "shot_id": shot_id,
        "timeline": {
            "fps": fps,
            "frame_start": frame_start,
            "frame_end": frame_end,
        },
        "image": {
            "width": width,
            "height": height,
            "aspect_ratio": aspect_ratio,
        },
        "camera": {
            "sensor_width_mm": 36.0,
            "default_focal_length_mm": 50.0,
            "default_fov_deg": 39.6,
            "keyframes": [
                {
                    "frame": frame_start,
                    "location": [0.0, -5.0, 1.5],
                    "rotation_euler_xyz_rad": [1.1, 0.0, 0.0],
                    "focal_length_mm": 50.0,
                },
                {
                    "frame": frame_end,
                    "location": [0.5, -4.5, 1.5],
                    "rotation_euler_xyz_rad": [1.1, 0.0, 0.05],
                    "focal_length_mm": 50.0,
                },
            ],
        },
        "characters": [],
        "render_passes": [],
        "control_passes": [],
        "prompts": {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "style_tags": [],
        },
        "seed": {
            "value": seed_value,
            "policy": "per_shot_derived",
            "derivation": "sha256(shot_id + authoritative source hashes)[:8] as int",
        },
        "optional_hooks": {
            "pose_projection": "skipped_unavailable",
            "motion_vectors": "skipped_unavailable",
        },
        "provenance": {
            "authoritative_sources": authoritative_sources,
            "export_tool": f"previs-pipeline/{__version__}",
            "export_mode": export_mode,
            "blender_runtime": blender_runtime,
            "exported_at": datetime.now(timezone.utc).isoformat(),
        },
    }
