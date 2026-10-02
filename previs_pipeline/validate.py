from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "previs" / "schema" / "shot-manifest.schema.json"


def load_schema() -> dict[str, Any]:
    with _SCHEMA_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    """Return human-readable validation errors (empty if valid)."""
    validator = Draft202012Validator(load_schema())
    errors: list[str] = []
    for err in sorted(validator.iter_errors(manifest), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in err.path) or "(root)"
        errors.append(f"{path}: {err.message}")
    errors.extend(_validate_semantic(manifest))
    return errors


def _validate_semantic(manifest: dict[str, Any]) -> list[str]:
    out: list[str] = []
    tl = manifest.get("timeline", {})
    fs, fe = tl.get("frame_start"), tl.get("frame_end")
    if fs is not None and fe is not None and fe < fs:
        out.append("timeline: frame_end must be >= frame_start")

    cam_kf = manifest.get("camera", {}).get("keyframes", [])
    for i, kf in enumerate(cam_kf):
        frame = kf.get("frame")
        if fs is not None and fe is not None and frame is not None:
            if frame < fs or frame > fe:
                out.append(f"camera.keyframes[{i}]: frame {frame} outside timeline")

    for pi, pass_ in enumerate(manifest.get("render_passes", [])):
        pfs, pfe = pass_.get("frame_start"), pass_.get("frame_end")
        if pfs is not None and pfe is not None and pfe < pfs:
            out.append(f"render_passes[{pi}]: frame_end must be >= frame_start")
        if fs is not None and fe is not None and pfs is not None and pfe is not None:
            if pfs < fs or pfe > fe:
                out.append(f"render_passes[{pi}]: frame range outside timeline")

    return out


def assert_valid_manifest(manifest: dict[str, Any]) -> None:
    errors = validate_manifest(manifest)
    if errors:
        raise ValueError("; ".join(errors))
