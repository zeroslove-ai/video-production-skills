#!/usr/bin/env python3
"""Run the configured H3 prompt pack strictly one process/job at a time."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def queue_empty(api: str) -> bool:
    with urllib.request.urlopen(api.rstrip("/") + "/queue", timeout=10) as response:
        queue = json.loads(response.read().decode("utf-8"))
    return not queue.get("queue_running") and not queue.get("queue_pending")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="tools/local_gen/config_h3_draft.json")
    parser.add_argument("--workflow", default="workflows/local_gen/h3_draft_base.json")
    parser.add_argument("--start-id", default="P01")
    parser.add_argument("--comfy-pid", type=int, required=True)
    parser.add_argument("--api", default="http://127.0.0.1:8188")
    parser.add_argument("--comfy-output", default=r"C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI\output")
    parser.add_argument("--settle-sec", type=int, default=10)
    parser.add_argument("--summary", default="evidence/local-gen-r0/draft-batch-summary.json")
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[2]
    config = json.loads((repo / args.config).read_text(encoding="utf-8"))
    prompts = config["prompts"]
    start_index = next((i for i, item in enumerate(prompts) if item["id"] == args.start_id), None)
    if start_index is None:
        raise SystemExit(f"unknown start id: {args.start_id}")

    summary_path = repo / args.summary
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    results = []
    started_at = iso_now()
    for item in prompts[start_index:]:
        run_id = f"batch-{item['id'].lower()}-seed{item['seed']}-864x480-r1-20260918"
        command = [
            sys.executable,
            str(repo / "tools/local_gen/run_h3_batch.py"),
            "--workflow", str(repo / args.workflow),
            "--run-id", run_id,
            "--comfy-pid", str(args.comfy_pid),
            "--api", args.api,
            "--comfy-output", args.comfy_output,
            "--prompt", item["prompt"],
            "--seed", str(item["seed"]),
            "--width", str(config["width"]),
            "--height", str(config["height"]),
            "--length", str(config["length"]),
            "--steps", str(config["steps"]),
            "--output-format", config["output_format"],
            "--timeout-sec", "600",
        ]
        if config.get("audio_off"):
            command.append("--audio-off")
        launched = iso_now()
        print(f"[{launched}] START {item['id']} seed={item['seed']}", flush=True)
        process = subprocess.Popen(command, cwd=repo)
        return_code = process.wait()
        run_dir = Path(args.comfy_output) / "video-production-skills" / "local-gen-r0" / run_id
        metrics_path = run_dir / "metrics.json"
        metrics = json.loads(metrics_path.read_text(encoding="utf-8")) if metrics_path.exists() else {
            "run_id": run_id,
            "status": "FAIL",
            "failure_reason": "RUNNER_EXIT_WITHOUT_METRICS",
        }
        record = {
            "prompt_id": item["id"],
            "seed": item["seed"],
            "run_id": run_id,
            "return_code": return_code,
            "metrics": metrics,
            "metrics_path": str(metrics_path),
            "finished_at": iso_now(),
        }
        results.append(record)
        summary_path.write_text(json.dumps({"started_at": started_at, "updated_at": iso_now(), "results": results}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[{iso_now()}] END {item['id']} status={metrics.get('status')} reason={metrics.get('failure_reason')}", flush=True)
        if metrics.get("status") != "PASS":
            print(f"[{iso_now()}] STOP after {item['id']}", flush=True)
            return 1
        for _ in range(args.settle_sec):
            if queue_empty(args.api):
                break
            time.sleep(1)
        time.sleep(args.settle_sec)

    summary_path.write_text(json.dumps({"started_at": started_at, "updated_at": iso_now(), "results": results}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
