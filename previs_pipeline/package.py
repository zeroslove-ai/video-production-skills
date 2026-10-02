from __future__ import annotations

import json
import zipfile
from pathlib import Path
from typing import Any

from previs_pipeline.hash_util import sha256_file
from previs_pipeline.validate import validate_manifest


class PackageError(Exception):
    pass


def write_manifest(package_dir: Path, manifest: dict[str, Any]) -> Path:
    package_dir.mkdir(parents=True, exist_ok=True)
    path = package_dir / "shot-manifest.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")
    return path


def attach_pass_hashes(manifest: dict[str, Any], package_dir: Path) -> dict[str, Any]:
    manifest = json.loads(json.dumps(manifest))
    for pass_ in manifest.get("render_passes", []):
        rel = pass_.get("relative_path", "")
        if "%" in rel:
            continue
        fp = package_dir / rel
        if fp.is_file():
            pass_["sha256"] = sha256_file(fp)
    for pass_ in manifest.get("control_passes", []):
        rel = pass_.get("relative_path", "")
        fp = package_dir / rel
        if fp.is_file():
            pass_["sha256"] = sha256_file(fp)
    kcs = manifest.get("keyframes_contact_sheet")
    if kcs and kcs.get("contact_sheet_relative_path"):
        fp = package_dir / kcs["contact_sheet_relative_path"]
        if fp.is_file():
            kcs["sha256"] = sha256_file(fp)
    return manifest


def verify_package_assets(package_dir: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for pass_ in manifest.get("render_passes", []):
        rel = pass_.get("relative_path", "")
        if "%" in rel:
            template_dir = package_dir / Path(rel).parent
            if not template_dir.is_dir():
                errors.append(f"missing pass directory: {template_dir}")
                continue
            pfs = pass_.get("frame_start")
            pfe = pass_.get("frame_end")
            if pfs is not None and pfe is not None:
                for frame in (pfs, pfe):
                    concrete = rel.replace("%04d", f"{frame:04d}")
                    fp = package_dir / concrete
                    if not fp.is_file():
                        errors.append(f"missing render pass frame: {concrete}")
            continue
        fp = package_dir / rel
        if not fp.is_file():
            errors.append(f"missing render pass asset: {rel}")
        elif pass_.get("sha256") and sha256_file(fp) != pass_["sha256"]:
            errors.append(f"hash mismatch for render pass: {rel}")

    for pass_ in manifest.get("control_passes", []):
        if pass_.get("optional"):
            continue
        rel = pass_.get("relative_path", "")
        fp = package_dir / rel
        if not fp.is_file():
            errors.append(f"missing required control pass: {rel}")

    kcs = manifest.get("keyframes_contact_sheet") or {}
    rel = kcs.get("contact_sheet_relative_path")
    if rel:
        fp = package_dir / rel
        if not fp.is_file():
            errors.append(f"missing contact sheet: {rel}")
    return errors


def validate_package(package_dir: Path) -> dict[str, Any]:
    manifest_path = package_dir / "shot-manifest.json"
    if not manifest_path.is_file():
        raise PackageError(f"missing shot-manifest.json in {package_dir}")
    with manifest_path.open(encoding="utf-8") as f:
        manifest = json.load(f)
    schema_errors = validate_manifest(manifest)
    asset_errors = verify_package_assets(package_dir, manifest)
    return {
        "valid": not schema_errors and not asset_errors,
        "schema_errors": schema_errors,
        "asset_errors": asset_errors,
        "manifest": manifest,
    }


def create_zip_archive(package_dir: Path, zip_path: Path) -> Path:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for fp in sorted(package_dir.rglob("*")):
            if fp.is_file():
                zf.write(fp, fp.relative_to(package_dir).as_posix())
    return zip_path
