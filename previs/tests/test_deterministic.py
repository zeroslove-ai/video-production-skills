from __future__ import annotations

import copy
from pathlib import Path

from previs_pipeline.hash_util import sha256_canonical_json
from previs_pipeline.synthetic import build_demo_r1_package

MINIMAL_FIXTURE = Path("previs/fixtures/demo_r1/minimal_scene.json")


def _stable_manifest_view(manifest: dict) -> dict:
    m = copy.deepcopy(manifest)
    m["provenance"].pop("exported_at", None)
    for pass_ in m.get("render_passes", []):
        pass_.pop("sha256", None)
    for pass_ in m.get("control_passes", []):
        pass_.pop("sha256", None)
    kcs = m.get("keyframes_contact_sheet")
    if kcs:
        kcs.pop("sha256", None)
    return m


def test_manifest_core_fields_are_deterministic(tmp_path: Path) -> None:
    a = build_demo_r1_package(tmp_path / "a", fixture_path=MINIMAL_FIXTURE)["manifest"]
    b = build_demo_r1_package(tmp_path / "b", fixture_path=MINIMAL_FIXTURE)["manifest"]
    assert sha256_canonical_json(_stable_manifest_view(a)) == sha256_canonical_json(
        _stable_manifest_view(b)
    )


def test_fixture_hash_stable() -> None:
    h1 = build_demo_r1_package(Path("previs/out/det_a"), fixture_path=MINIMAL_FIXTURE)["fixture_hash"]
    h2 = build_demo_r1_package(Path("previs/out/det_b"), fixture_path=MINIMAL_FIXTURE)["fixture_hash"]
    assert h1 == h2
