#!/usr/bin/env python3
"""Run one local LTX-2.5 I2V job and capture reproducible evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT))

from previs.adapters.comfyui.client import ComfyUIClient, ComfyUIError
from previs.adapters.comfyui.ltx25 import build_ltx25_i2v_workflow


PROMPT = (
    "Preserve the exact character identity, face, hairstyle, outfit, accessories, pose and background from the source image. "
    "In a single continuous 3-second portrait shot, she gives a gentle friendly greeting: one small relaxed hand wave, "
    "a natural blink, a soft warm smile, subtle breathing in the shoulders, a very slight head tilt, and restrained secondary hair sway. "
    "Keep the camera locked. Preserve the original illustrated style, clean line art, colors and proportions. "
    "The motion is calm, human-like and physically coherent, with a stable face and stable clothing. No scene cut."
)
NEGATIVE_PROMPT = (
    "identity drift, unstable face, warped anatomy, extra fingers, extra arms, extra limbs, morphing, flicker, jitter, "
    "clothing distortion, outfit deformation, exaggerated body change, blur, low quality, text, watermark, subtitles, "
    "camera shake, sudden motion, scene change, broken hands, broken eyes, broken mouth, framing drift, zoom drift"
)


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def dimensions(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    if not data.startswith(b"\xff\xd8"):
        return None
    index = 2
    while index + 9 < len(data):
        if data[index] != 0xFF:
            index += 1
            continue
        while index < len(data) and data[index] == 0xFF:
            index += 1
        if index >= len(data):
            break
        marker = data[index]
        index += 1
        if marker in {0xD8, 0xD9} or 0xD0 <= marker <= 0xD7:
            continue
        if index + 2 > len(data):
            break
        length = int.from_bytes(data[index:index + 2], "big")
        if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
            if index + 7 <= len(data):
                return int.from_bytes(data[index + 5:index + 7], "big"), int.from_bytes(data[index + 3:index + 5], "big")
            break
        index += max(length, 2)
    return None


def gpu_sample(nvidia_smi: str) -> dict[str, Any] | None:
    command = [nvidia_smi, "--query-gpu=name,utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=5, check=True)
        row = result.stdout.strip().splitlines()[0].split(",")
        return {"name": row[0].strip(), "utilization_percent": int(row[1]), "memory_used_mib": int(row[2]), "memory_total_mib": int(row[3]), "sampled_at": iso_now()}
    except (OSError, subprocess.SubprocessError, IndexError, ValueError):
        return None


def saved_mp4s(history: dict[str, Any]) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    for node_output in history.get("outputs", {}).values():
        if not isinstance(node_output, dict):
            continue
        for output_value in node_output.values():
            if not isinstance(output_value, list):
                continue
            for item in output_value:
                if isinstance(item, dict) and str(item.get("filename", "")).lower().endswith(".mp4"):
                    found.append({key: str(item.get(key, "")) for key in ("filename", "subfolder", "type")})
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", default="http://127.0.0.1:8190")
    parser.add_argument("--input", required=True, type=Path, help="Existing image file already visible in the ComfyUI input directory")
    parser.add_argument("--image-name", required=True, help="Filename as seen by ComfyUI LoadImage")
    parser.add_argument("--comfy-output", required=True, type=Path)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--nvidia-smi", default="nvidia-smi")
    parser.add_argument("--comfy-pid", type=int)
    parser.add_argument("--seed", type=int, default=20261015)
    parser.add_argument("--width", type=int, default=512)
    parser.add_argument("--height", type=int, default=768)
    parser.add_argument("--frames", type=int, default=73)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--prefix", default="greeting_wave_r2")
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(f"input image does not exist: {args.input}")
    if not args.run_dir.parent.is_dir():
        raise SystemExit(f"run directory parent must already exist: {args.run_dir.parent}")
    if args.run_dir.exists():
        raise SystemExit(f"refusing to overwrite existing run: {args.run_dir}")
    if not re.fullmatch(r"[A-Za-z0-9._-]+", args.prefix):
        raise SystemExit("prefix may contain only letters, numbers, dot, underscore and hyphen")
    args.run_dir.mkdir(parents=False)

    image_size = dimensions(args.input)
    image_hash = sha256(args.input)
    workflow = build_ltx25_i2v_workflow(
        image_name=args.image_name,
        positive_prompt=PROMPT,
        negative_prompt=NEGATIVE_PROMPT,
        seed=args.seed,
        width=args.width,
        height=args.height,
        frames=args.frames,
        filename_prefix=args.prefix,
    )
    client = ComfyUIClient(args.api)
    started_at = iso_now()
    gpu_samples: list[dict[str, Any]] = []
    status: dict[str, Any] = {
        "run_id": args.run_dir.name,
        "status": "RUNNING",
        "started_at": started_at,
        "comfyui_api": args.api,
        "comfyui_pid": args.comfy_pid,
        "input_image_name": args.image_name,
        "input_image_sha256": image_hash,
        "input_image_dimensions": image_size,
        "workflow_sha256": hashlib.sha256(json.dumps(workflow, sort_keys=True).encode("utf-8")).hexdigest(),
        "model": "ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors",
        "text_encoder": "gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors",
        "vae": ["ltx-2.5-video-vae-conv-bf16.safetensors", "ltx-2.5-audio-vae-bf16.safetensors"],
        "lora": None,
        "resolution": [args.width, args.height],
        "fps": 24,
        "frames": args.frames,
        "duration_seconds": args.frames / 24,
        "steps": 8,
        "cfg": 1.0,
        "seed": args.seed,
        "prompt": PROMPT,
        "negative_prompt": NEGATIVE_PROMPT,
    }
    write_json(args.run_dir / "workflow.json", workflow)
    write_json(args.run_dir / "metrics.json", status)

    try:
        system_stats = client.system_stats()
        node_types = client.node_types()
        required = {node["class_type"] for node in workflow.values()}
        missing = sorted(required - node_types)
        if missing:
            raise ComfyUIError(f"ComfyUI is missing required node types: {missing}")
        status["comfyui_system_stats"] = system_stats
        status["required_node_types_available"] = True
        write_json(args.run_dir / "metrics.json", status)

        prompt_id = client.submit(workflow, client_id=f"video-studio-r2-{args.run_dir.name}")
        status["prompt_id"] = prompt_id
        write_json(args.run_dir / "metrics.json", status)
        t0 = time.monotonic()
        history: dict[str, Any] | None = None
        while time.monotonic() - t0 < args.timeout_seconds:
            sample = gpu_sample(args.nvidia_smi)
            if sample:
                gpu_samples.append(sample)
            try:
                history = client.wait(prompt_id, timeout_s=3, poll_s=1)
                break
            except ComfyUIError as exc:
                if "Timed out waiting" not in str(exc):
                    raise
        if history is None:
            raise ComfyUIError(f"Timed out after {args.timeout_seconds}s; last ComfyUI status was not complete")
        status["generation_seconds"] = round(time.monotonic() - t0, 2)
        status["comfyui_history_status"] = history.get("status", {})
        saved = saved_mp4s(history)
        if not saved:
            raise ComfyUIError(f"ComfyUI completed but history did not report an MP4: {json.dumps(history.get('outputs', {}))}")
        source_mp4 = args.comfy_output / saved[-1]["subfolder"] / saved[-1]["filename"]
        if not source_mp4.is_file():
            raise ComfyUIError(f"ComfyUI history output file is missing: {source_mp4}")
        destination = args.run_dir / "greeting_wave.mp4"
        shutil.copy2(source_mp4, destination)
        status.update({
            "status": "PASS",
            "finished_at": iso_now(),
            "output": "greeting_wave.mp4",
            "output_bytes": destination.stat().st_size,
            "output_sha256": sha256(destination),
            "comfyui_saved_result": saved[-1],
            "gpu_sample_count": len(gpu_samples),
            "gpu_memory_peak_mib": max((item["memory_used_mib"] for item in gpu_samples), default=None),
            "gpu_samples": gpu_samples,
        })
        write_json(args.run_dir / "history.json", history)
        write_json(args.run_dir / "metrics.json", status)
        print(json.dumps(status, indent=2, ensure_ascii=False))
        return 0
    except Exception as exc:
        status.update({"status": "FAIL", "finished_at": iso_now(), "failure": str(exc), "gpu_samples": gpu_samples})
        write_json(args.run_dir / "metrics.json", status)
        print(json.dumps(status, indent=2, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
