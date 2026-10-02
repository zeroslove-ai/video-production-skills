from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from previs.adapters.base import ProviderAdapter


class ExternalVideoProviderAdapter(ProviderAdapter):
    """
    Generic HTTP/API-shaped handoff for external video providers.
    R1: builds `provider_request.json` only; no network calls.
    """

    provider_id = "external_video"

    def __init__(self, provider_name: str = "example_provider") -> None:
        self.provider_name = provider_name

    def build_request(self, package_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
        beauty = next((p for p in manifest["render_passes"] if p["id"] == "beauty"), None)
        depth = next((p for p in manifest["render_passes"] if p["id"] == "depth"), None)
        return {
            "provider": self.provider_name,
            "mode": "dry_run",
            "shot_id": manifest["shot_id"],
            "endpoint": "https://api.example.invalid/v1/video/generate",
            "payload": {
                "prompt": manifest["prompts"]["prompt"],
                "negative_prompt": manifest["prompts"].get("negative_prompt", ""),
                "seed": manifest["seed"]["value"],
                "width": manifest["image"]["width"],
                "height": manifest["image"]["height"],
                "fps": manifest["timeline"]["fps"],
                "frame_start": manifest["timeline"]["frame_start"],
                "frame_end": manifest["timeline"]["frame_end"],
                "control_assets": {
                    "beauty_pattern": beauty["relative_path"] if beauty else None,
                    "depth_pattern": depth["relative_path"] if depth else None,
                    "camera_json": "control/camera_trajectory.json",
                },
            },
            "provenance": manifest["provenance"],
        }

    def stage_inputs(self, package_dir: Path, staging_dir: Path, request: dict[str, Any]) -> Path:
        staging_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(package_dir, staging_dir / "package", dirs_exist_ok=True)
        req_path = staging_dir / "provider_request.json"
        req_path.write_text(json.dumps(request, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return staging_dir

    def dry_run_validate(
        self, package_dir: Path, staging_dir: Path, request: dict[str, Any]
    ) -> dict[str, Any]:
        errors: list[str] = []
        if request.get("mode") != "dry_run":
            errors.append("request mode must be dry_run in R1")
        if not (staging_dir / "package" / "shot-manifest.json").is_file():
            errors.append("staged package missing shot-manifest.json")
        expected = {
            "provider": request["provider"],
            "mode": "dry_run_expected",
            "shot_id": request["shot_id"],
            "outputs": [{"id": "video", "type": "mp4", "relative_path": "outputs/final.mp4"}],
        }
        out = staging_dir / "expected_output_manifest.json"
        out.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return {
            "valid": not errors,
            "errors": errors,
            "network_called": False,
            "expected_output_manifest_path": out.as_posix(),
        }
