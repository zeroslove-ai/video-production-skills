#!/usr/bin/env python3
"""Decode a generated MP4 and save start/middle/end frames plus a contact sheet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import cv2
from PIL import Image, ImageDraw, ImageFont


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    if not args.video.is_file():
        raise SystemExit(f"video does not exist: {args.video}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    capture = cv2.VideoCapture(str(args.video))
    if not capture.isOpened():
        raise SystemExit(f"OpenCV could not open video: {args.video}")

    fps = float(capture.get(cv2.CAP_PROP_FPS))
    declared_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    targets = {
        "start": 0,
        "middle": max(0, (declared_frames - 1) // 2),
        "end": max(0, declared_frames - 1),
    }
    grid_indices = sorted({round(i * max(0, declared_frames - 1) / 8) for i in range(9)})
    selected: dict[str, Image.Image] = {}
    grid_frames: dict[int, Image.Image] = {}
    decoded_frames = 0
    first_dimensions: tuple[int, int] | None = None
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        if first_dimensions is None:
            first_dimensions = (int(frame.shape[1]), int(frame.shape[0]))
        for label, target_index in targets.items():
            if decoded_frames == target_index:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                selected[label] = Image.fromarray(rgb)
        if decoded_frames in grid_indices:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            grid_frames[decoded_frames] = Image.fromarray(rgb)
        decoded_frames += 1
    capture.release()

    for label, image in selected.items():
        image.save(args.output_dir / f"{label}.png")

    sheet_width = 3 * 480
    sheet_height = 300 + 32
    sheet = Image.new("RGB", (sheet_width, sheet_height), "#20242b")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for column, label in enumerate(("start", "middle", "end")):
        image = selected.get(label)
        x = column * 480
        draw.text((x + 8, 8), f"{label.upper()}  frame {targets[label]}", fill="white", font=font)
        if image is not None:
            image.thumbnail((464, 268), Image.Resampling.LANCZOS)
            sheet.paste(image, (x + (480 - image.width) // 2, 32 + (268 - image.height) // 2))
    sheet.save(args.output_dir / "contact_sheet.png")

    grid_cell = (320, 220)
    grid = Image.new("RGB", (3 * grid_cell[0], 3 * (grid_cell[1] + 24)), "#20242b")
    grid_draw = ImageDraw.Draw(grid)
    for index, frame_index in enumerate(grid_indices):
        image = grid_frames.get(frame_index)
        column, row = index % 3, index // 3
        x, y = column * grid_cell[0], row * (grid_cell[1] + 24)
        grid_draw.text((x + 6, y + 4), f"frame {frame_index}", fill="white", font=font)
        if image is not None:
            image.thumbnail((grid_cell[0] - 12, grid_cell[1] - 8), Image.Resampling.LANCZOS)
            grid.paste(image, (x + (grid_cell[0] - image.width) // 2, y + 24 + (grid_cell[1] - image.height) // 2))
    grid.save(args.output_dir / "review_9frames.png")

    report = {
        "video": str(args.video.resolve()),
        "sha256": sha256(args.video),
        "bytes": args.video.stat().st_size,
        "fps": fps,
        "declared_frames": declared_frames,
        "decoded_frames": decoded_frames,
        "resolution": list(first_dimensions) if first_dimensions else None,
        "duration_seconds": decoded_frames / fps if fps > 0 else None,
        "selected_frame_indices": targets,
        "review_grid_frame_indices": grid_indices,
        "decode_ok": decoded_frames > 0 and decoded_frames == declared_frames and len(selected) == 3,
        "audio_checked": False,
    }
    (args.output_dir / "decode_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["decode_ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
