from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from previs.adapters.base import ProviderAdapter

WORKFLOW_TEMPLATE = (
    Path(__file__).resolve().parent / "workflows" / "previs_handoff_v1.api.json"
)


class ComfyUIAdapter(ProviderAdapter):
    provider_id = "comfyui"

    def build_request(self, package_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
        workflow = json.loads(WORKFLOW_TEMPLATE.read_text(encoding="utf-8"))
        bindings = self._bindings_for_manifest(manifest)
        return {
            "provider": self.provider_id,
            "mode": "dry_run",
            "workflow_template": WORKFLOW_TEMPLATE.as_posix(),
            "workflow_template_sha256": self._sha256_file(WORKFLOW_TEMPLATE),
            "bindings": bindings,
            "workflow": self._apply_bindings(workflow, bindings),
            "shot_id": manifest["shot_id"],
            "seed": manifest["seed"]["value"],
            "prompts": manifest["prompts"],
            "image": manifest["image"],
            "timeline": manifest["timeline"],
        }

    def stage_inputs(self, package_dir: Path, staging_dir: Path, request: dict[str, Any]) -> Path:
        staging_dir.mkdir(parents=True, exist_ok=True)
        bindings = request["bindings"]
        beauty_glob = package_dir / "passes" / "beauty"
        if beauty_glob.is_dir():
            dest = staging_dir / "inputs" / "beauty"
            shutil.copytree(beauty_glob, dest, dirs_exist_ok=True)
            bindings["staged_beauty_dir"] = dest.as_posix()
        contact = package_dir / "meta" / "contact_sheet.png"
        if contact.is_file():
            dest = staging_dir / "inputs" / "contact_sheet.png"
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(contact, dest)
            bindings["staged_contact_sheet"] = dest.as_posix()
        manifest_copy = staging_dir / "shot-manifest.json"
        shutil.copy2(package_dir / "shot-manifest.json", manifest_copy)
        request_path = staging_dir / "comfyui_request.json"
        request_path.write_text(json.dumps(request, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return staging_dir

    def dry_run_validate(
        self, package_dir: Path, staging_dir: Path, request: dict[str, Any]
    ) -> dict[str, Any]:
        errors: list[str] = []
        bindings = request.get("bindings", {})
        required_nodes = ("load_image_beauty", "prompt_encode", "seed")
        for key in required_nodes:
            if key not in bindings:
                errors.append(f"missing binding: {key}")

        wf = request.get("workflow", {})
        if not wf.get("nodes"):
            errors.append("workflow has no nodes")

        expected = self._expected_output_manifest(request)
        out_path = staging_dir / "expected_output_manifest.json"
        out_path.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        return {
            "valid": not errors,
            "errors": errors,
            "expected_output_manifest_path": out_path.as_posix(),
            "expected_output_manifest": expected,
            "comfyui_server_required": False,
            "generation_executed": False,
        }

    def _bindings_for_manifest(self, manifest: dict[str, Any]) -> dict[str, Any]:
        beauty = next((p for p in manifest["render_passes"] if p["id"] == "beauty"), None)
        beauty_pattern = beauty["relative_path"] if beauty else "passes/beauty/beauty_%04d.png"
        return {
            "load_image_beauty": {
                "node_id": "1",
                "input_key": "image",
                "source_glob": beauty_pattern,
            },
            "prompt_encode": {
                "node_id": "2",
                "input_key": "text",
                "value": manifest["prompts"]["prompt"],
            },
            "negative_prompt_encode": {
                "node_id": "3",
                "input_key": "text",
                "value": manifest["prompts"].get("negative_prompt", ""),
            },
            "seed": {
                "node_id": "4",
                "input_key": "seed",
                "value": manifest["seed"]["value"],
            },
            "width": manifest["image"]["width"],
            "height": manifest["image"]["height"],
            "frame_count": manifest["timeline"]["frame_end"] - manifest["timeline"]["frame_start"] + 1,
            "fps": manifest["timeline"]["fps"],
        }

    def _apply_bindings(self, workflow: dict[str, Any], bindings: dict[str, Any]) -> dict[str, Any]:
        wf = json.loads(json.dumps(workflow))
        nodes = {n["id"]: n for n in wf.get("nodes", [])}
        if "2" in nodes:
            nodes["2"]["inputs"]["text"] = bindings["prompt_encode"]["value"]
        if "3" in nodes:
            nodes["3"]["inputs"]["text"] = bindings["negative_prompt_encode"]["value"]
        if "4" in nodes:
            nodes["4"]["inputs"]["seed"] = bindings["seed"]["value"]
        wf["nodes"] = list(nodes.values())
        wf["meta"]["bound_shot"] = True
        return wf

    def _expected_output_manifest(self, request: dict[str, Any]) -> dict[str, Any]:
        tl = request["timeline"]
        return {
            "provider": self.provider_id,
            "mode": "dry_run_expected",
            "shot_id": request["shot_id"],
            "outputs": [
                {
                    "id": "generated_preview",
                    "type": "video",
                    "relative_path": "outputs/generated_preview.mp4",
                    "fps": tl["fps"],
                    "frame_start": tl["frame_start"],
                    "frame_end": tl["frame_end"],
                }
            ],
            "notes": "R1 dry-run only; no ComfyUI server invocation.",
        }

    @staticmethod
    def _sha256_file(path: Path) -> str:
        from previs_pipeline.hash_util import sha256_file

        return sha256_file(path)
