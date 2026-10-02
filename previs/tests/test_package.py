from __future__ import annotations

from pathlib import Path

from previs_pipeline.package import validate_package
from previs_pipeline.synthetic import build_demo_r1_package

MINIMAL_FIXTURE = Path("previs/fixtures/demo_r1/minimal_scene.json")


def test_package_asset_validation_passes() -> None:
    result = build_demo_r1_package(Path("previs/out/test_pkg"), fixture_path=MINIMAL_FIXTURE)
    report = validate_package(result["package_dir"])
    assert report["valid"]
    assert report["schema_errors"] == []
    assert report["asset_errors"] == []


def test_missing_asset_detected(tmp_path: Path) -> None:
    result = build_demo_r1_package(tmp_path / "pkg", fixture_path=MINIMAL_FIXTURE)
    beauty_dir = result["package_dir"] / "passes" / "beauty"
    first = next(beauty_dir.glob("*.png"))
    first.unlink()
    report = validate_package(result["package_dir"])
    assert not report["valid"]
    assert report["asset_errors"]
