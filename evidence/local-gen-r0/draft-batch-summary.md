# H3 Draft Batch Summary — 2026-09-18

Technical result: 8/8 PASS. All outputs were generated sequentially and verified with ffprobe. Visual result: partial, because the reused I2V source is a flat cartoon reference rather than a realistic child-safe reference image.

| Run ID | Prompt | Seed | Status | Wall | Peak VRAM | Peak RAM | Lowest available RAM | Output |
|---|---|---:|---|---:|---:|---:|---:|---|
| `draft-p01-seed101-864x480-r1-20260918` | P01 | 101 | PASS | 61.721 s | 15,286 MiB | 30.87 GiB | 30.69 GiB | `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI\output\video-production-skills\local-gen-r0\draft-p01-seed101-864x480-r1-20260918\result.mp4` |
| `batch-p02-seed202-864x480-r1-20260918` | P02 | 202 | PASS | 65.750 s | 15,072 MiB | 30.91 GiB | 30.65 GiB | `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI\output\video-production-skills\local-gen-r0\batch-p02-seed202-864x480-r1-20260918\result.mp4` |
| `batch-p03-seed303-864x480-r1-20260918` | P03 | 303 | PASS | 59.772 s | 14,563 MiB | 34.43 GiB | 27.12 GiB | `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI\output\video-production-skills\local-gen-r0\batch-p03-seed303-864x480-r1-20260918\result.mp4` |
| `batch-p04-seed404-864x480-r1-20260918` | P04 | 404 | PASS | 59.736 s | 14,632 MiB | 34.41 GiB | 27.14 GiB | `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install\ComfyUI\output\video-production-skills\local-gen-r0\batch-p04-seed404-864x480-r1-20260918\result.mp4` |
| `batch-p05-seed505-864x480-r1-20260918` | P05 | 505 | PASS | 58.691 s | 14,572 MiB | 33.65 GiB | 27.90 GiB | `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI\output\video-production-skills\local-gen-r0\batch-p05-seed505-864x480-r1-20260918\result.mp4` |
| `batch-p06-seed606-864x480-r1-20260918` | P06 | 606 | PASS | 59.818 s | 14,583 MiB | 33.69 GiB | 27.87 GiB | `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI\output\video-production-skills\local-gen-r0\batch-p06-seed606-864x480-r1-20260918\result.mp4` |
| `batch-p07-seed707-864x480-r1-20260918` | P07 | 707 | PASS | 59.901 s | 14,684 MiB | 33.55 GiB | 28.01 GiB | `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI\output\video-production-skills\local-gen-r0\batch-p07-seed707-864x480-r1-20260918\result.mp4` |
| `batch-p08-seed808-864x480-r1-20260918` | P08 | 808 | PASS | 59.684 s | 14,672 MiB | 33.53 GiB | 28.03 GiB | `C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI\output\video-production-skills\local-gen-r0\batch-p08-seed808-864x480-r1-20260918\result.mp4` |

Quick qualitative notes: P04 and P06 show the most useful stage-light/background variation; P01 is the cleanest simple full-body composition. All previews remain child-safe, but all inherit the cartoon style from `ComfyUI/input/example.png`.
