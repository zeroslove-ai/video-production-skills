#!/usr/bin/env python3
"""Run exactly one R3 H3 photoreal T2V gate clip."""

from __future__ import annotations

import subprocess
import sys
import argparse
from pathlib import Path


PROMPT = """Realistic live-action cinematic footage, genuine photographic video, not an illustration and not animation.

A cheerful six-year-old Korean girl performs an energetic but age-appropriate K-pop-inspired dance on a professionally lit, family-friendly music stage. She looks like a real child filmed by a professional cinema camera.

Natural human skin with subtle skin texture and realistic subsurface detail, natural child facial proportions, individual realistic hair strands, real fabric texture, physically plausible stage lighting, authentic photographic exposure, realistic depth of field, natural motion blur, genuine live-action television performance appearance.

She wears a colorful child-appropriate performance outfit: a bright lightweight jacket, comfortable layered skirt over leggings, and clean sneakers. No mature styling.

Full-body shot. Her entire body and feet remain visible.

She begins in a confident ready pose, immediately enters rhythmic coordinated choreography, performs crisp arm movements, quick side steps, light footwork, a small energetic jump, one fast clean spin, then continues dancing with strong musical timing and finishes in a joyful confident pose.

Her movement is impressive and skilled for her age, lively and energetic, with natural body weight transfer and physically believable balance.

The camera performs a subtle professional dolly movement while primarily maintaining a clear full-body view. Modern concert lighting and soft LED stage lights in the background, realistic reflections on the floor, cinematic but natural lighting.

Maintain consistent facial identity, realistic hands, realistic legs and feet, stable anatomy and natural human motion throughout.

Absolutely no cartoon, no anime, no drawing, no illustration, no painting, no 3D character, no doll, no plastic skin, no game-render appearance, no stylized character rendering, no exaggerated proportions, no text, no logo, no watermark.

Child-safe and age-appropriate performance throughout."""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--comfy-pid", type=int, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    run_id = "r3-t2v-photoreal-seed101-20260918"
    output_root = Path(r"C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI\output")
    run_dir = output_root / "video-production-skills" / "local-gen-r0" / run_id
    if run_dir.exists():
        raise SystemExit(f"refusing duplicate gate run: {run_dir}")

    command = [
        sys.executable,
        str(repo / "tools/local_gen/run_h3_batch.py"),
        "--workflow", str(repo / "workflows/local_gen/h3_t2v_photoreal_4step.json"),
        "--run-id", run_id,
        "--comfy-pid", str(args.comfy_pid),
        "--prompt", PROMPT,
        "--seed", "101",
        "--width", "864",
        "--height", "480",
        "--length", "124",
        "--steps", "4",
        "--audio-off",
        "--output-format", "video/h264-mp4",
        "--timeout-sec", "600",
    ]
    completed = subprocess.run(command, cwd=repo)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
