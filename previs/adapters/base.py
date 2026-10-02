from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class ProviderAdapter(ABC):
    """Contract for packaging a shot handoff for an external generator (R1: dry-run only)."""

    provider_id: str

    @abstractmethod
    def build_request(self, package_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
        """Return a provider-specific request document (no paid API calls in R1)."""

    @abstractmethod
    def stage_inputs(self, package_dir: Path, staging_dir: Path, request: dict[str, Any]) -> Path:
        """Copy/link inputs into a staging folder; return staging root."""

    @abstractmethod
    def dry_run_validate(
        self, package_dir: Path, staging_dir: Path, request: dict[str, Any]
    ) -> dict[str, Any]:
        """Validate bindings and emit expected output manifest without generation."""

    def run_dry_run(self, package_dir: Path, work_dir: Path) -> dict[str, Any]:
        manifest_path = package_dir / "shot-manifest.json"
        import json

        with manifest_path.open(encoding="utf-8") as f:
            manifest = json.load(f)
        request = self.build_request(package_dir, manifest)
        staging = self.stage_inputs(package_dir, work_dir / "staging", request)
        validation = self.dry_run_validate(package_dir, staging, request)
        return {
            "provider_id": self.provider_id,
            "request": request,
            "staging_dir": str(staging),
            "dry_run": validation,
        }
