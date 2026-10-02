from __future__ import annotations

from pathlib import Path

from previs.adapters.comfyui.adapter import ComfyUIAdapter
from previs.adapters.external.adapter import ExternalVideoProviderAdapter
from previs_pipeline.synthetic import build_demo_r1_package

MINIMAL_FIXTURE = Path("previs/fixtures/demo_r1/minimal_scene.json")


def test_comfyui_dry_run(tmp_path: Path) -> None:
    result = build_demo_r1_package(tmp_path / "demo", fixture_path=MINIMAL_FIXTURE)
    adapter = ComfyUIAdapter()
    out = adapter.run_dry_run(result["package_dir"], tmp_path / "comfy_work")
    assert out["dry_run"]["valid"]
    assert out["dry_run"]["generation_executed"] is False
    expected = Path(out["dry_run"]["expected_output_manifest_path"])
    assert expected.is_file()


def test_external_provider_dry_run(tmp_path: Path) -> None:
    result = build_demo_r1_package(tmp_path / "demo", fixture_path=MINIMAL_FIXTURE)
    adapter = ExternalVideoProviderAdapter("example_provider")
    out = adapter.run_dry_run(result["package_dir"], tmp_path / "ext_work")
    assert out["dry_run"]["valid"]
    assert out["dry_run"]["network_called"] is False
