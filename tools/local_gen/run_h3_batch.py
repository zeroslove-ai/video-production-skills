#!/usr/bin/env python3
"""Sequential MiniMax H3 runner for the existing local ComfyUI API."""

from __future__ import annotations

import argparse
import ctypes
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_API = "http://127.0.0.1:8188"
DEFAULT_COMFY_OUTPUT = Path(r"C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI\output")
SOFT_RAM_BYTES = 52 * 1024**3
HARD_RAM_BYTES = 56 * 1024**3
SOFT_VRAM_MIB = 15565  # 15.2 GiB expressed as MiB
HARD_VRAM_MIB = 15975  # 15.6 GiB expressed as MiB


class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]


def memory_status() -> tuple[int, int]:
    status = MEMORYSTATUSEX()
    status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
        return 0, 0
    return status.ullTotalPhys - status.ullAvailPhys, status.ullTotalPhys


def nvidia_memory() -> tuple[int, int]:
    command = [
        "nvidia-smi",
        "--query-gpu=memory.used,memory.total",
        "--format=csv,noheader,nounits",
    ]
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        row = result.stdout.strip().splitlines()[0]
        used, total = [int(re.sub(r"[^0-9]", "", value)) for value in row.split(",")[:2]]
        return used, total
    except (OSError, IndexError, ValueError, subprocess.CalledProcessError):
        return 0, 0


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def http_json(api: str, method: str, path: str, payload: Any | None = None, timeout: float = 30) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        api.rstrip("/") + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"} if data is not None else {},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read()
        return json.loads(raw.decode("utf-8")) if raw else None


def queue_empty(api: str) -> bool:
    queue = http_json(api, "GET", "/queue", timeout=5)
    return not queue.get("queue_running") and not queue.get("queue_pending")


def classify_failure(text: str) -> str:
    lower = text.lower()
    if "out of memory" in lower or "cuda out of memory" in lower:
        return "OOM_VRAM"
    if "memoryerror" in lower or "cannot allocate memory" in lower:
        return "OOM_RAM"
    if "timed out" in lower or "timeout" in lower:
        return "TIMEOUT"
    if "workflow" in lower or "node errors" in lower or "prompt validation" in lower:
        return "WORKFLOW_PATCH_FAIL"
    return "OTHER"


def find_mp4s(value: Any, comfy_output: Path) -> list[Path]:
    found: list[Path] = []
    if isinstance(value, dict):
        filename = value.get("filename")
        if isinstance(filename, str) and filename.lower().endswith(".mp4"):
            subfolder = value.get("subfolder", "")
            candidate = (comfy_output / subfolder / filename).resolve()
            if candidate.exists():
                found.append(candidate)
        for child in value.values():
            found.extend(find_mp4s(child, comfy_output))
    elif isinstance(value, list):
        for child in value:
            found.extend(find_mp4s(child, comfy_output))
    return list(dict.fromkeys(found))


def patch_workflow(
    workflow: dict[str, Any],
    run_id: str,
    comfy_output: Path,
    prompt: str | None,
    seed: int | None,
    width: int | None,
    height: int | None,
    length: int | None,
    steps: int | None,
    audio_off: bool,
) -> dict[str, Any]:
    patched = json.loads(json.dumps(workflow))
    prefix = f"video-production-skills/local-gen-r0/{run_id}/result"
    h3_nodes = [node for node in patched.values() if node.get("class_type") == "MiniMaxH3ImageToVideo"]
    if not h3_nodes:
        raise ValueError("MiniMaxH3ImageToVideo node not found")
    for node in h3_nodes:
        inputs = node["inputs"]
        if prompt is not None:
            inputs["prompt"] = prompt
        if width is not None:
            inputs["width"] = width
        if height is not None:
            inputs["height"] = height
        if length is not None:
            inputs["length"] = length
    if seed is not None:
        noise_nodes = [node for node in patched.values() if node.get("class_type") == "RandomNoise"]
        if not noise_nodes:
            raise ValueError("RandomNoise node not found")
        for node in noise_nodes:
            node["inputs"]["noise_seed"] = seed
    if steps is not None:
        scheduler_nodes = [node for node in patched.values() if node.get("class_type") == "BasicScheduler"]
        if not scheduler_nodes:
            raise ValueError("BasicScheduler node not found")
        for node in scheduler_nodes:
            node["inputs"]["steps"] = steps
    output_nodes = [
        node for node in patched.values() if node.get("class_type") in {"VHS_VideoCombine", "SaveVideo"}
    ]
    if not output_nodes:
        raise ValueError("No supported video output node found")
    for node in output_nodes:
        node["inputs"]["filename_prefix"] = prefix
        if audio_off and node.get("class_type") == "VHS_VideoCombine":
            node["inputs"].pop("audio", None)
    return patched


def write_metrics(path: Path, metrics: dict[str, Any]) -> None:
    path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--prompt")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--length", type=int)
    parser.add_argument("--steps", type=int)
    parser.add_argument("--audio-off", action="store_true")
    parser.add_argument("--api", default=DEFAULT_API)
    parser.add_argument("--comfy-output", type=Path, default=DEFAULT_COMFY_OUTPUT)
    parser.add_argument("--timeout-sec", type=int, default=600)
    args = parser.parse_args()

    comfy_output = args.comfy_output.resolve()
    run_dir = comfy_output / "video-production-skills" / "local-gen-r0" / args.run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "run.log"
    telemetry_path = run_dir / "telemetry.csv"
    metrics_path = run_dir / "metrics.json"
    started = time.monotonic()
    metrics: dict[str, Any] = {
        "run_id": args.run_id,
        "started_at": iso_now(),
        "status": "RUNNING",
        "failure_reason": None,
        "api": args.api,
        "workflow_source": str(Path(args.workflow).resolve()),
        "watchdog": {
            "timeout_sec": args.timeout_sec,
            "soft_ram_bytes": SOFT_RAM_BYTES,
            "hard_ram_bytes": HARD_RAM_BYTES,
            "soft_vram_mib": SOFT_VRAM_MIB,
            "hard_vram_mib": HARD_VRAM_MIB,
        },
        "peak_vram_mib": 0,
        "peak_ram_bytes": 0,
        "output_path": None,
        "sha256": None,
    }
    soft_ram_logged = False
    soft_vram_logged = False

    def log(message: str) -> None:
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(f"[{iso_now()}] {message}\n")

    try:
        workflow_source = Path(args.workflow)
        workflow = json.loads(workflow_source.read_text(encoding="utf-8"))
        patched = patch_workflow(
            workflow,
            args.run_id,
            comfy_output,
            args.prompt,
            args.seed,
            args.width,
            args.height,
            args.length,
            args.steps,
            args.audio_off,
        )
        (run_dir / "request.json").write_text(
            json.dumps(
                {
                    "run_id": args.run_id,
                    "prompt": args.prompt,
                    "seed": args.seed,
                    "width": args.width,
                    "height": args.height,
                    "length": args.length,
                    "steps": args.steps,
                    "audio_off": args.audio_off,
                    "created_at": iso_now(),
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        (run_dir / "workflow.json").write_text(json.dumps(patched, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        log("workflow patched; output is routed into the run folder")
    except Exception as exc:
        metrics.update(status="FAIL", failure_reason="WORKFLOW_PATCH_FAIL", error=str(exc), finished_at=iso_now())
        log(f"WORKFLOW_PATCH_FAIL: {exc}")
        write_metrics(metrics_path, metrics)
        return 1

    try:
        health = http_json(args.api, "GET", "/system_stats", timeout=10)
        metrics["comfyui_version"] = health.get("system", {}).get("comfyui_version")
        log("API health PASS")
        if not queue_empty(args.api):
            metrics.update(status="FAIL", failure_reason="API_FAIL", error="queue was not empty before submit", finished_at=iso_now())
            log("API_FAIL: queue was not empty before submit")
            write_metrics(metrics_path, metrics)
            return 1
    except Exception as exc:
        metrics.update(status="FAIL", failure_reason="API_FAIL", error=str(exc), finished_at=iso_now())
        log(f"API_FAIL: health or queue check failed: {exc}")
        write_metrics(metrics_path, metrics)
        return 1

    telemetry_file = telemetry_path.open("w", newline="", encoding="utf-8")
    telemetry = csv.writer(telemetry_file)
    telemetry.writerow(["timestamp", "elapsed_sec", "vram_used_mib", "vram_total_mib", "ram_used_bytes", "ram_total_bytes", "queue_running", "queue_pending"])
    telemetry_file.flush()
    prompt_id = None
    failure_reason = None
    error_text = ""
    try:
        response = http_json(args.api, "POST", "/prompt", {"prompt": patched, "client_id": f"local-gen-r0-{args.run_id}"}, timeout=30)
        if response.get("error") or response.get("node_errors"):
            raise RuntimeError(json.dumps(response, ensure_ascii=False))
        prompt_id = response.get("prompt_id")
        if not prompt_id:
            raise RuntimeError(f"missing prompt_id: {response}")
        metrics["prompt_id"] = prompt_id
        log(f"submitted prompt_id={prompt_id}")
        while True:
            elapsed = time.monotonic() - started
            vram_used, vram_total = nvidia_memory()
            ram_used, ram_total = memory_status()
            metrics["peak_vram_mib"] = max(metrics["peak_vram_mib"], vram_used)
            metrics["peak_ram_bytes"] = max(metrics["peak_ram_bytes"], ram_used)
            try:
                queue = http_json(args.api, "GET", "/queue", timeout=5)
                running_count = len(queue.get("queue_running", []))
                pending_count = len(queue.get("queue_pending", []))
            except Exception:
                running_count = pending_count = -1
            telemetry.writerow([iso_now(), round(elapsed, 3), vram_used, vram_total, ram_used, ram_total, running_count, pending_count])
            telemetry_file.flush()
            if vram_used >= SOFT_VRAM_MIB and not soft_vram_logged:
                log(f"WATCHDOG WARNING: VRAM soft limit exceeded: {vram_used} MiB")
                soft_vram_logged = True
            if ram_used >= SOFT_RAM_BYTES and not soft_ram_logged:
                log(f"WATCHDOG WARNING: RAM soft limit exceeded: {ram_used} bytes")
                soft_ram_logged = True
            if vram_used >= HARD_VRAM_MIB:
                failure_reason = "OOM_VRAM"
                error_text = f"hard VRAM limit exceeded: {vram_used} MiB"
                log(f"WATCHDOG HARD STOP: {error_text}")
                try:
                    http_json(args.api, "POST", "/interrupt", {}, timeout=10)
                except Exception as interrupt_exc:
                    log(f"interrupt request failed: {interrupt_exc}")
                break
            if ram_used >= HARD_RAM_BYTES:
                failure_reason = "OOM_RAM"
                error_text = f"hard RAM limit exceeded: {ram_used} bytes"
                log(f"WATCHDOG HARD STOP: {error_text}")
                try:
                    http_json(args.api, "POST", "/interrupt", {}, timeout=10)
                except Exception as interrupt_exc:
                    log(f"interrupt request failed: {interrupt_exc}")
                break
            if elapsed >= args.timeout_sec:
                failure_reason = "TIMEOUT"
                error_text = f"run exceeded {args.timeout_sec} seconds"
                log(f"WATCHDOG TIMEOUT: {error_text}")
                try:
                    http_json(args.api, "POST", "/interrupt", {}, timeout=10)
                except Exception as interrupt_exc:
                    log(f"interrupt request failed: {interrupt_exc}")
                break
            try:
                history = http_json(args.api, "GET", f"/history/{prompt_id}", timeout=10)
                entry = history.get(prompt_id)
                if entry:
                    status = entry.get("status", {})
                    if status.get("status_str") == "error" or status.get("completed") is False and status.get("messages"):
                        error_text = json.dumps(status, ensure_ascii=False)
                        failure_reason = classify_failure(error_text)
                        log(f"ComfyUI history failure: {error_text}")
                        break
                    if status.get("completed") is True or entry.get("outputs"):
                        mp4s = find_mp4s(entry, comfy_output)
                        if mp4s:
                            source = mp4s[0]
                            destination = run_dir / "result.mp4"
                            if source.resolve() != destination.resolve():
                                shutil.copy2(source, destination)
                            metrics["output_path"] = str(destination)
                            digest = hashlib.sha256(destination.read_bytes()).hexdigest()
                            metrics["sha256"] = digest
                            metrics["source_output_path"] = str(source)
                            log(f"completed output={source}")
                            ffmpeg = shutil.which("ffmpeg")
                            if ffmpeg:
                                subprocess.run([ffmpeg, "-y", "-i", str(destination), "-frames:v", "1", str(run_dir / "preview.jpg")], capture_output=True, text=True)
                            break
            except urllib.error.HTTPError as history_exc:
                error_text = str(history_exc)
            time.sleep(1.0)
    except Exception as exc:
        error_text = traceback.format_exc()
        failure_reason = "API_FAIL" if prompt_id is None else classify_failure(str(exc))
        log(f"{failure_reason}: {exc}")
    finally:
        telemetry_file.close()

    if failure_reason:
        metrics["status"] = "FAIL"
        metrics["failure_reason"] = failure_reason
        metrics["error"] = error_text
        log(f"result FAIL reason={failure_reason}")
    elif metrics.get("output_path"):
        metrics["status"] = "PASS"
        log("result PASS")
    else:
        metrics["status"] = "FAIL"
        metrics["failure_reason"] = "OUTPUT_NOT_FOUND"
        metrics["error"] = error_text or "history completed without an MP4 output"
        log("OUTPUT_NOT_FOUND: history completed without an MP4 output")
    metrics["wall_time_sec"] = round(time.monotonic() - started, 3)
    metrics["finished_at"] = iso_now()
    write_metrics(metrics_path, metrics)
    try:
        for _ in range(30):
            if queue_empty(args.api):
                break
            time.sleep(1)
    except Exception:
        pass
    return 0 if metrics["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
