#!/usr/bin/env python3
"""Build a compact Video Studio index from recorded shot evaluations."""

from __future__ import annotations

import argparse
import html
import json
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


RANK = {"PASS": 3, "PARTIAL": 2, "FAIL": 1}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def collect(root: Path) -> list[dict]:
    records: list[dict] = []
    for evaluation_path in sorted(root.glob("**/evaluation.json")):
        try:
            evaluation = load_json(evaluation_path)
        except (OSError, json.JSONDecodeError):
            continue
        attempt_dir = evaluation_path.parent
        shot_dir = attempt_dir.parents[1]
        metrics_path = attempt_dir / "metrics.json"
        decode_path = shot_dir / "previews" / f"v{evaluation.get('attempts', 1)}" / "decode_report.json"
        metrics = load_json(metrics_path) if metrics_path.exists() else {}
        decode = load_json(decode_path) if decode_path.exists() else {}
        preview_dir = decode_path.parent
        video = next(iter(sorted(attempt_dir.glob("*.mp4"))), None)
        if video is None:
            continue
        records.append(
            {
                "shot_id": evaluation.get("shot_id", shot_dir.name),
                "action": evaluation.get("action", ""),
                "category": shot_dir.parent.name,
                "attempt": evaluation.get("attempts", 1),
                "content_verdict": evaluation.get("content_verdict", "PARTIAL"),
                "mocap_suitability": evaluation.get("mocap_suitability", "UNKNOWN"),
                "visual_review": evaluation.get("visual_review", ""),
                "input_reference": evaluation.get("input_reference", ""),
                "character_id": evaluation.get("character_id", ""),
                "canon_status": evaluation.get("canon_status", ""),
                "game_import": evaluation.get("game_import", ""),
                "video": str(video.relative_to(root)).replace("\\", "/"),
                "preview": str((preview_dir / "contact_sheet.png").relative_to(root)).replace("\\", "/")
                if (preview_dir / "contact_sheet.png").exists()
                else "",
                "review_grid": str((preview_dir / "review_9frames.png").relative_to(root)).replace("\\", "/")
                if (preview_dir / "review_9frames.png").exists()
                else "",
                "decode_ok": decode.get("decode_ok", False),
                "resolution": evaluation.get("resolution", ""),
                "fps": evaluation.get("fps", ""),
                "frames": evaluation.get("frames", ""),
                "duration_seconds": evaluation.get("duration_seconds", ""),
                "generation_seconds": evaluation.get("generation_seconds", ""),
                "peak_gpu_memory_mib": evaluation.get("peak_gpu_memory_mib", ""),
                "seed": evaluation.get("seed", ""),
                "model": evaluation.get("model", metrics.get("model", "")),
                "lora": evaluation.get("lora", metrics.get("lora")),
                "prompt": metrics.get("prompt", ""),
                "sha256": decode.get("sha256", ""),
                "notes": evaluation.get("notes", ""),
                "attempt_dir": str(attempt_dir),
            }
        )
    return records


def best_attempts(records: list[dict]) -> list[dict]:
    chosen: dict[str, dict] = {}
    for record in records:
        current = chosen.get(record["shot_id"])
        candidate_key = (RANK.get(record["content_verdict"], 0), record["attempt"])
        current_key = (RANK.get(current["content_verdict"], 0), current["attempt"]) if current else (-1, -1)
        if candidate_key > current_key:
            chosen[record["shot_id"]] = record
    return sorted(chosen.values(), key=lambda item: (item["category"], item["shot_id"]))


def make_contact_sheet(root: Path, records: list[dict], output: Path) -> None:
    tile_w, tile_h, label_h = 300, 300, 54
    cols = 4
    rows = max(1, (len(records) + cols - 1) // cols)
    canvas = Image.new("RGB", (cols * tile_w, rows * (tile_h + label_h)), "#20242b")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    for index, record in enumerate(records):
        x, y = (index % cols) * tile_w, (index // cols) * (tile_h + label_h)
        preview = root / record["preview"] if record["preview"] else None
        frame_path = (preview.parent / "middle.png") if preview else None
        if frame_path and frame_path.exists():
            frame = Image.open(frame_path).convert("RGB")
            frame.thumbnail((tile_w - 16, tile_h - 16), Image.Resampling.LANCZOS)
            canvas.paste(frame, (x + (tile_w - frame.width) // 2, y + (tile_h - frame.height) // 2))
        draw.text((x + 8, y + tile_h + 5), f"{record['shot_id']} · {record['action'][:30]}", font=font, fill="white")
        draw.text((x + 8, y + tile_h + 24), f"{record['content_verdict']} / mocap {record['mocap_suitability']}", font=font, fill="#cbd5e1")
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, format="WEBP", quality=76, method=6)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path, help="D:\\AI\\LTX25-R3\\output\\video-studio-r2")
    args = parser.parse_args()
    root = args.root.resolve()
    records = collect(root)
    selected = best_attempts(records)
    counts = Counter(record["content_verdict"] for record in selected)
    index = {
        "generated_at": __import__("datetime").datetime.now().astimezone().isoformat(timespec="seconds"),
        "root": str(root),
        "unique_shots": len(selected),
        "attempts": len(records),
        "verdict_counts": dict(counts),
        "shots": selected,
        "attempt_records": records,
    }
    manifest_path = root / "manifests" / "shot_index.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    preview_dir = root / "previews"
    contact_path = preview_dir / "contact_sheet.webp"
    make_contact_sheet(root, selected, contact_path)

    rows = []
    for record in selected:
        video_href = html.escape(record["video"])
        review_href = html.escape(record["review_grid"])
        thumbnail = f'<img src="../{html.escape(record["preview"])}" alt="{html.escape(record["shot_id"])} contact sheet">' if record["preview"] else ""
        rows.append(
            f'<article><h2>{html.escape(record["shot_id"])} | {html.escape(record["action"])}</h2>'
            f'<p><b>{html.escape(record["content_verdict"])}</b> | mocap {html.escape(record["mocap_suitability"])}</p>'
            f'{thumbnail}<p>{html.escape(record["visual_review"])}</p>'
            f'<p>{record["resolution"]} | {record["fps"]} fps | {record["duration_seconds"]} s | seed {record["seed"]}</p>'
            f'<p><a href="../{video_href}">MP4</a> | <a href="../{review_href}">9-frame review</a></p>'
            f'<details><summary>Prompt / provenance</summary><p>{html.escape(record["input_reference"])}</p><pre>{html.escape(record["prompt"])}</pre><code>{html.escape(record["model"])}</code></details></article>'
        )
    report = f"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Video Studio R2 Index</title>
<style>body{{font:15px system-ui;margin:24px auto;max-width:1200px;padding:0 16px;background:#10151b;color:#edf2f7}}a{{color:#86c5ff}}.summary{{display:flex;gap:18px;flex-wrap:wrap}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:16px}}article{{padding:14px;border:1px solid #35404b;border-radius:10px;background:#1a222c}}article img{{width:100%;height:auto;background:#20242b}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}</style>
<h1>VIDEO STUDIO R2 | shot index</h1><div class="summary"><span>Unique shots: {len(selected)}</span><span>Attempts: {len(records)}</span><span>PASS: {counts.get('PASS',0)}</span><span>PARTIAL: {counts.get('PARTIAL',0)}</span><span>FAIL: {counts.get('FAIL',0)}</span></div>
<p>Thumbnails link to local deliverables. Generated AI motion is not skeleton data; mocap suitability is recorded separately.</p><img style="max-width:100%" src="contact_sheet.webp" alt="Shot contact sheet"><div class="grid">{''.join(rows)}</div></html>"""
    (preview_dir / "index.html").write_text(report, encoding="utf-8")

    md = ["# Video Studio R2 | current delivery", "", f"Unique shots: {len(selected)} | attempts: {len(records)} | PASS: {counts.get('PASS',0)} | PARTIAL: {counts.get('PARTIAL',0)} | FAIL: {counts.get('FAIL',0)}", "", "| Shot | Action | Verdict | Mocap suitability | Duration | Output |", "|---|---|---|---|---:|---|"]
    for record in selected:
        md.append(f"| {record['shot_id']} | {record['action']} | {record['content_verdict']} | {record['mocap_suitability']} | {record['duration_seconds']}s | `{record['video']}` |")
    (root / "reports" / "current_delivery.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({"unique_shots": len(selected), "attempts": len(records), "verdict_counts": dict(counts), "manifest": str(manifest_path), "contact_sheet": str(contact_path), "html": str(preview_dir / 'index.html')}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
