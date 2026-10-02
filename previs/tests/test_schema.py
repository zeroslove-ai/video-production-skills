from __future__ import annotations

import copy
import json
from pathlib import Path

from previs_pipeline.manifest import build_manifest_skeleton, derive_shot_seed
from previs_pipeline.synthetic import build_demo_r1_package
from previs_pipeline.validate import load_schema, validate_manifest

MINIMAL_FIXTURE = Path("previs/fixtures/demo_r1/minimal_scene.json")


def test_schema_file_loads() -> None:
    schema = load_schema()
    assert schema["title"] == "ShotManifest"


def test_demo_package_validates() -> None:
    result = build_demo_r1_package(Path("previs/out/test_demo"), fixture_path=MINIMAL_FIXTURE)
    errors = validate_manifest(result["manifest"])
    assert errors == []


def test_seed_derivation_is_deterministic() -> None:
    sources = [{"uri": "file:///a", "sha256": "a" * 64, "role": "synthetic_fixture"}]
    assert derive_shot_seed("demo", sources) == derive_shot_seed("demo", sources)
    assert derive_shot_seed("demo", sources) != derive_shot_seed("other", sources)


def test_invalid_frame_range_rejected() -> None:
    result = build_demo_r1_package(Path("previs/out/test_invalid"), fixture_path=MINIMAL_FIXTURE)
    manifest = copy.deepcopy(result["manifest"])
    manifest["timeline"]["frame_end"] = manifest["timeline"]["frame_start"] - 1
    errors = validate_manifest(manifest)
    assert any("frame_end" in e for e in errors)


def test_invalid_camera_frame_rejected() -> None:
    result = build_demo_r1_package(Path("previs/out/test_camera"), fixture_path=MINIMAL_FIXTURE)
    manifest = copy.deepcopy(result["manifest"])
    manifest["camera"]["keyframes"][0]["frame"] = -1
    errors = validate_manifest(manifest)
    assert errors


def test_missing_required_field_rejected() -> None:
    result = build_demo_r1_package(Path("previs/out/test_missing"), fixture_path=MINIMAL_FIXTURE)
    manifest = copy.deepcopy(result["manifest"])
    del manifest["shot_id"]
    errors = validate_manifest(manifest)
    assert errors


def test_manifest_skeleton_rejects_bad_mode() -> None:
    m = build_manifest_skeleton(
        "x",
        fps=24,
        frame_start=1,
        frame_end=10,
        width=640,
        height=360,
        aspect_ratio="16:9",
        prompt="p",
        export_mode="synthetic",
        authoritative_sources=[
            {"uri": "file:///f", "sha256": "b" * 64, "role": "synthetic_fixture"}
        ],
    )
    m["provenance"]["export_mode"] = "invalid"
    assert validate_manifest(m) != []
