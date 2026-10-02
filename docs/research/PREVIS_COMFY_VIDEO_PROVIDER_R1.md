# Previs → ComfyUI / Local Video / External Provider — Research R1

Date: 2026-10-02 · Branch: `research/previs-video-provider-r1` · Base: `origin/main@29f9431`
Scope: research only. No pipeline code, no paid generations, no model downloads. Cursor owns the separate implementation R1 (`work/previs-video-pipeline-r1`); this doc supplies the contract it can be checked against, not code.

## 0. Bottom line (central question)

> Can we nearly finish animation + camera in Blender and let AI handle mainly style/detail/final rendering?

**Yes for "motion/camera/timing are authoritative and AI re-skins"; no for "AI preserves it frame-exactly".** Every route below is a *soft* conditioning of a diffusion model, not a renderer. What survives previs → final depends on the route:

| Route | Camera + composition | Body motion | Identity | Shot timing | Verdict |
|---|---|---|---|---|---|
| Local V2V with depth/pose/canny control (Wan 2.2 Fun Control / VACE, LTX-2 IC-LoRA) | strong (structure locked per frame) | strong | medium; needs ref image/LoRA | exact (frame count = input) | Best fidelity; short clips, 16 GB limits |
| Local I2V w/ first(+last) frame only | weak–medium | model-invented | medium | approximate | Keyframe tool, not a previs tool |
| Provider V2V restyle (Runway Aleph) | strong (edits input video) | strong | medium | exact-ish | Best "style pass over finished animation" |
| Provider motion transfer (Kling Motion Control, Wan Animate) | camera is *re-interpreted* | strong | good (ref image) | matches ref video | Good for character acting; poor for locked camera |
| Provider multimodal reference (Seedance 2.x) | prompt-steered, not locked | medium–strong | medium–good | approximate | Highest "look" quality; least deterministic |

Honest expectation: **~85–95% structural adherence in the locked-structure routes, with drift in fine limbs/hands/faces and texture flicker**, and **a human/automated selection loop (N seeds → pick) is mandatory**. These percentages are my inference, not a measured benchmark (see §1 and §15 experiments to measure them).

**Recommended default: hybrid.** Blender is the source of truth for camera, blocking, timing and a *clean-pass package*; a local ComfyUI depth/pose-conditioned pass makes cheap draft restyles and A/Bs; the best 1–2 candidates per shot go to an external provider (V2V / reference) for the final-quality pass; FFmpeg/Remotion handle editorial. Never let the provider own camera or timing.

## 1. Evidence legend and verification status

Every claim in this document carries one tag:

- **[DOC]** documented fact — official docs/model card/repo read this session (or stated as such).
- **[MKT]** marketing / vendor claim — vendor blog or landing page; capability not independently demonstrated.
- **[COM]** community evidence — workflow sites, forum posts, reseller/aggregator blogs, tutorials. Directional only.
- **[INF]** my inference/engineering judgement; testable.
- **[UNV]** not freshly verified this session (training memory or search snippet only; fetch failed or page was JS shell).

Verification log (what was actually fetched on 2026-10-02):

| Source | Result |
|---|---|
| docs.comfy.org Wan2.2 Fun Control tutorial | fetched OK → Apache-2.0, control types, VRAM figure |
| docs.dev.runwayml.com (index) | fetched OK → model list, input types; per-model pricing page not fetched |
| higgsfield.ai/blog/higgsfield-api | fetched OK (vendor blog [MKT]) |
| en.wikipedia.org Seedance 2.0 | fetched OK (secondary source) |
| kling.ai motion control user guide | fetched OK (vendor doc) |
| docs.ltx.video IC-LoRA | **HTTP 403** — only search snippet seen → [UNV]/[COM] |
| docs.byteplus.com Seedance 2.0 tutorial | **JS shell only** — request schema from search snippets → [UNV]/[COM] |
| Pricing figures from atlascloud/anikuku/openrouter/etc. | search snippets from resellers → [COM], re-check before budgeting |
| Veo 3.1 reference-image API | Google forum thread reports docs/API mismatch → [COM] |

Treat every price in this doc as "order of magnitude as of Sept–Oct 2026, re-verify on the vendor page before spend".

## 2. Facts by tier

### 2.1 Documented facts [DOC]
- ComfyUI Wan 2.2 Fun Control is Apache-2.0, supports Canny, Depth, OpenPose, MLSD and trajectory control; core ComfyUI ships only Canny preprocessing, other preprocessors come from `comfyui_controlnet_aux`; requires current/nightly ComfyUI (docs.comfy.org). FP8 scaled variant used ~24 GB VRAM on an RTX 4090D at 640×640 (docs.comfy.org). A 4-step LoRA cut a ~524 s run to ~138 s.
- Wan 2.2 Animate 14B (character animation + replacement from performer video) is Apache-2.0 open weights; ComfyUI has a template workflow (HF model card, comfy.org workflow page).
- Runway developer docs list Seedance 2.5, Gen 4.5 (image→video), Aleph 2.0 (video→video), GPT Image 2; inputs include text, reference images, video (V2V), first/last frame, aspect ratio, duration; billing is credits per second.
- Higgsfield API (vendor blog): async submit/poll/webhook, API key unlocks 20 concurrent requests, pay-as-you-go USD, failed requests refunded, outputs retained ≥7 days, funds expire after 1 year, states generated content may be used commercially.
- Kling Motion Control (vendor guide): inputs = character image + motion video (+ optional element binding); motion reference 3–30 s; "orientation matches image" mode allows independent camera moves by prompt, "matches video" follows the reference.
- Seedance timeline (Wikipedia, secondary): 2.0 released 2026-02-12 (≤15 s, 1080p); 2.5 on 2026-07-31 (≤30 s, up to 30 image / 10 video / 10 audio references, joint audio-video generation, timestamp editing). CapCut international rollout excludes US and **does not generate from images/videos containing real faces**.
- Existing local baseline from this repo's `research/local-video-gen-r0` inventory: RTX 4080 SUPER 16 GB, 64 GB RAM, ComfyUI 0.34.6 (likely too old for current Fun Control/Animate/LTX-2 templates), PyTorch 2.10+cu130. Measured: Wan 2.2 TI2V-5B 320×192 ×9 frames in 11.7 s at 15.5 GB peak; MiniMax H3 608×352 ×22 frames at 15.5/16.4 GB peak.

### 2.2 Marketing claims [MKT] — do not plan on them
- "Frame-accurate", "perfect character consistency", "cinematic physics" for Seedance 2.x/2.5, Kling 3.0, Higgsfield DoP, Runway Aleph.
- Seedance 2.5 "30 s with reference budget" — spec is documented, *quality over 30 s* is unproven for our shots.
- Higgsfield "50+ models" is a catalog aggregation; model parity with first-party APIs is unverified.

### 2.3 Community evidence [COM]
- Wan VACE / Fun Control workflows for pose/depth-driven character animation are widely reproduced on RunComfy, comfyui-wiki, neurocanvas, stable-diffusion-art; consistently reported: good motion following, identity drift without a reference image/LoRA, 81-frame (~5 s @16 fps) practical clip length, seams between chained clips.
- Wan open-weights line ends at 2.2; 2.5/2.6/2.7 are API-only (invideo, localaimaster, wan27.org, flowjam). I could not verify via an Alibaba primary source. A "Wan 3.0" claim exists on a third-party site — **treated as unverified**.
- LTX-2 / 2.3 IC-LoRAs for depth/pose/canny exist; "memory intensive because the whole reference video is encoded" (search snippet quoting docs; official page 403). 8–16 GB GPUs advised 540p ×4 s.
- Blender+ComfyUI workflows exporting mask/depth/outline sequences into ControlNet-style pipelines are common (RunComfy "Blender + ComfyUI").
- Seedance 2.0 API pricing on BytePlus ≈ $0.07/s @480p, $0.15/s @720p, $0.37/s @1080p, lower with video input (e.g. 720p with video input ≈ $0.089 vs $0.144/s); Higgsfield lists Seedance 2.0 up to ≈ $0.93/s, Seedance 2.5 ≈ $0.074/s, Kling 3.0 ≈ $0.112/s; Runway Aleph 2.0 ≈ 28 credits/s at $0.01/credit = **$0.28/s**, 56-credit minimum. Resellers disagree by up to 10× — see §6.
- Veo 3.1: up to 3 reference images; Gemini API docs vs actual API behavior disagreed in a forum report.

### 2.4 Inference [INF]
Marked inline as `[INF]` below. All numeric adherence estimates are INF.

## 3. Pipeline anatomy: what Blender can emit

Blender (Cycles/EEVEE) passes → ControlNet-like conditioning. All of these are exported from one saved scene via bpy (Z, Normal, Cryptomatte/IndexOB, Mist, Freestyle/Line) per Blender manual pass list [DOC for pass existence; mappings below are INF].

| Blender output | Provider-neutral name | Feeds | Gotchas |
|---|---|---|---|
| Combined (EEVEE/Workbench, flat-lit grey or lookdev) | `rgb_previs` | V2V structure input (Aleph, VACE source, Seedance reference_video) | Style leakage: grey-clay previs encourages grey outputs; use light, neutral lookdev, not final PBR |
| Z / Mist | `depth` | Depth control (Fun Control, VACE, LTX IC-LoRA) | Z is metres, models expect relative inverse-depth 0–1 ("near=white" convention varies). Normalize **per shot** with fixed near/far, never per frame (flicker). Store raw EXR plus normalized 16-bit PNG. Preprocessors like Depth-Anything produce *estimated* depth; true Z usually cleaner but different distribution → needs a calibration test |
| Normal | `normal` | Normal control; relighting hints | Blender normals are world/camera-space with different axes than the common ControlNet "bae/midas" tangent-ish convention; ComfyUI normal models expect camera-space RGB with specific Y/Z flips — verify empirically |
| Cryptomatte / Object Index | `mask_<role>` | Region prompting, character replacement masks (Animate), inpaint masks, per-character identity routing | Anti-aliased edges; threshold + dilate 2–4 px |
| Armature → OpenPose-18/COCO or DWPose | `pose` | OpenPose control, Kling/Animate-style motion references | Render 2D skeleton from projected bones, **in the shot camera**, with confidence = 1; stylised/non-human rigs need mapping table; hands/face optional |
| Freestyle / Canny of silhouette | `lineart` | Canny/MLSD control | Cheap, robust for camera layout |
| Camera object | `camera.json` | **Not consumed by any open model reliably**; used for provenance + provider prompts + re-projection | Camera path conditioning (e.g. camera-control LoRAs) exists [UNV], quality unproven; depth+rgb already encode most of it |
| Motion vectors/Vector pass | `flow` | Optional temporal-consistency guidance/evaluation, not input | Use mainly for QA (warp error) |

[INF] Key principle: **camera is conditioned implicitly via per-frame depth/edges/RGB**, not via camera parameters. Explicit camera parameters are provenance only.

## 4. Model / provider matrix

Columns: control inputs, ref/identity, first/last, duration, access, automation, cost, commercial, evidence, fit.

| Model / provider | Previs-relevant control | Identity | First/last | Typical duration | Access / automation | Cost (indicative, [COM] unless stated) | Commercial caveats | Evidence | Fit |
|---|---|---|---|---|---|---|---|---|---|
| **Wan 2.2 Fun Control 14B** (local) | Depth/OpenPose/Canny/MLSD/trajectory [DOC] | ref image start frame, LoRA [COM] | start frame | ~5 s @16 fps [COM] | ComfyUI API (`/prompt`) [DOC for API existence; repo validated it earlier] | GPU time; ~24 GB FP8 at 640² on 4090D [DOC] → **does not fit 16 GB at that res without offload/GGUF** [INF] | Apache-2.0 [DOC] | DOC + COM | **Local structural restyle, short clips** |
| **Wan 2.2 VACE / Wan 2.1 VACE** (local) | Pose/depth/edge, masks, inpaint/outpaint, ref images, first-last [COM] | ref image [COM] | yes | 81 frames | ComfyUI | same class; GGUF quants reported for 12–16 GB [COM] | Check VACE license separately [UNV] | COM | Strong all-rounder for mask/ref combos |
| **Wan 2.2 Animate 14B** (local) | Pose + face from performer video, replacement with masks [DOC/COM] | ref image | – | ~5–10 s windows [COM] | ComfyUI template | 14B class | Apache-2.0 [DOC] | DOC+COM | Previs rendered pose/face-driven acting → stylised character |
| **Wan 2.2 TI2V-5B** (local) | none (T2V/I2V) | start frame | start | short | ComfyUI; **measured on this PC** | Fits 16 GB at tiny res [DOC-local] | Apache-2.0 [UNV] | local measurement | Draft/keyframe only |
| **LTX-2 / LTX-2.3 + IC-LoRA** (local) | Depth, pose, canny IC-LoRAs [COM; official page 403] | image conditioning | yes | ~4–10 s | ComfyUI-LTXVideo nodes | 720p needs ≥24 GB; 16 GB → 540p ×4 s [COM] | LTX-2 Community License (revenue-threshold style terms — **read before commercial use**) [UNV] | COM | Fast drafts, joint audio; check IC-LoRA quality |
| HunyuanVideo / others (local) | partial controls [UNV] | – | – | – | – | – | – | – | Not evaluated this round |
| **Runway Aleph 2.0** (API) | Video-to-video edit of *the actual previs video* [DOC list; COM price] | Reference image [UNV] | – | seconds-scale; input clip limits [UNV] | REST + SDK, async; credits | ≈ $0.28/s, 56-credit min [COM] | ToS + moderation; commercial on paid plans [UNV] | DOC+COM | **Best final "style pass" on finished animation** |
| **Runway Gen 4.5 / Seedance 2.5 on Runway** (API) | I2V, first/last, refs [DOC] | ref images | yes | up to 30 s (Seedance 2.5) [DOC listing] | same API | credits/s, model-dependent [UNV] | same | DOC | Candidate single-vendor gateway |
| **Seedance 2.0 / 2.5 (BytePlus ModelArk)** | `reference_video` (motion/camera ref), `reference_image`, `reference_audio`, first/last frame [COM; official page JS-only] | ref images (≤30 in 2.5 [DOC-secondary]) | yes | ≤15 s (2.0), ≤30 s (2.5) [DOC-secondary] | REST async task API [COM] | ≈ $0.07–0.37/s (480–1080p), cheaper with video input [COM] | **Real-face input restrictions** (CapCut documented; BytePlus API behavior [UNV]); region availability; IP filters | DOC-secondary + COM | Best look/audio; camera/motion follows reference *loosely* |
| **Kling 3.0 Motion Control** (Kuaishou API/resellers) | Character image + motion video, 3–30 s, orientation mode [DOC] | image-bound; element binding [DOC] | – | 10 s (image orient.) / 30 s (video orient.) [COM] | Official + many resellers; async/webhook | ≈ $0.11/s [COM, Higgsfield] | Reseller terms vary | DOC+COM | Character acting from Blender pose/RGB; camera conditions weaker |
| **Higgsfield API** | Aggregator: Seedance, Kling, Wan, LTX etc. [MKT] | per model | per model | per model | REST/SDK/CLI, 20 concurrent, webhooks [MKT] | $0.042–$0.93/s by model [MKT] | States commercial use allowed [MKT]; funds expire 1 yr | MKT | Convenient multiplexer; adds dependency & margin |
| **Veo 3.1** (Gemini/Vertex) | ≤3 reference images, first/last [COM] | ref images | yes | ≤8 s typ. [UNV] | Gemini API | [UNV] | SynthID/watermarks, policy | COM (mismatch bug reported) | I2V/reference with audio; no V2V control |
| Wan 2.5/2.6/2.7 (API-only) | I2V/ref/audio [COM] | ref | – | – | Alibaba Cloud / resellers | $/s [COM] | closed | COM | Provider alternative; no local path |
| Others to monitor [UNV] | Luma Ray, Pika, Hailuo/MiniMax (local H3 exists), Sora 2 | – | – | – | – | – | – | – | Out of scope this round |

[INF] Selection rule: **if the shot needs locked camera/composition → V2V (Aleph or local control); if it needs acting transfer onto a new character → Kling Motion Control / Wan Animate; if it needs best look and audio with looser structure → Seedance reference mode.**

## 5. Capability-by-requirement analysis

### 5.1 Depth / normals / masks / pose / camera
- Depth: first-class in open models (Fun Control, VACE, LTX IC-LoRA). Providers rarely expose it — they take the RGB video and re-derive structure internally [INF]. So a clean *RGB* previs matters more for providers; clean *depth/pose* matters more locally.
- Normals: poorly supported for video; use for relighting/QA only [INF].
- Masks: first-class for VACE/Animate; Seedance/Aleph have prompt-based local edit only [INF].
- Pose/skeleton: first-class locally (OpenPose/DWPose); Kling/Animate use pose extracted from video. Rendering skeleton video from rig is optional if the previs RGB is human-readable.
- Camera controls: Provider "camera presets" are prompt-level; none accept a camera path file [UNV]. Treat camera as locked by video/depth input.

### 5.2 First/last frame
Supported by Wan (FLF template [DOC per ComfyUI templates mentions]), LTX, Seedance, Runway, Veo. Use for **shot-boundary anchoring and chaining** (last frame of clip N = first of N+1), not as a motion constraint (middle motion is invented) [INF].

### 5.3 Identity & temporal consistency [INF unless noted]
Tools in descending reliability: (1) identity-bearing first frame produced by a still model from character sheet, (2) LoRA trained on the character (local; needs 15–40 stills; license of base respected), (3) multi-reference images (Seedance/Veo/Kling element binding), (4) text description (weakest). Temporal: short clips + overlapping windows with shared seed; keep camera/lighting consistent; evaluate with face-embedding similarity and optical-flow warp error rather than eyeballing.
Known failure modes [COM]: face drift past ~3–5 s, hand deformation during fast motion, clothing pattern flicker, cut-seams when chaining local clips.

### 5.4 Motion fidelity previs → final [INF]
- Gross trajectory/timing: high when structure control (depth/pose/V2V).
- Contact (feet/ground, hand-object): the common loss. Mitigate with depth+mask of props and short clips.
- Fine speed profile (ease in/out): models smooth/regularize; assume ±2–4 frame timing drift per beat and verify with pose-tracking comparison (§15 E1).
- Extreme stylised proportions (non-human, chibi): control nets trained on humans degrade; expect re-fitting prompts and lower adherence.

## 6. Cost, usage, commercial caveats

Indicative cost for a 10 s shot at 720p, 4 candidates [COM-derived, INF arithmetic]:
- Local Wan/LTX: electricity + wall time (hours of 4080 SUPER time at 14B quality; minutes at 5B/540p).
- Aleph 2.0: 10 s × $0.28 = **$2.8/candidate → ~$11** (before re-roll).
- Seedance 2.0 720p w/ video input: ≈ $0.09/s → ~$0.9/candidate (BytePlus list per [COM]); via aggregators up to several × more.
- Kling 3.0 MC: ≈ $1.1/candidate.

Caveats [mixed]:
- Reseller prices diverge up to ~10× for the same model; always bind to the first-party price page in the experiment record.
- Real-person/face input policies: Seedance consumer variants block real faces [DOC-secondary]; API may differ [UNV]. Applies to Avatar use with real talent likenesses → **requires explicit consent records and per-provider policy check**.
- Commercial rights: Apache-2.0 models (Wan 2.2) are the cleanest [DOC]; LTX-2 community license has conditions [UNV]; provider outputs usually allowed on paid tiers [MKT/UNV]. Record the ToS version/date per generated asset.
- Data handling: previs frames and character refs leave the machine in provider routes. For unreleased IP (Yuri Room) this is a business decision [INF].
- Retention: Higgsfield outputs ≥7 days [MKT] → download immediately; hash and store.

## 7. Local-first route

```
Blender (saved bpy) ─► passes: rgb/depth/pose/lineart/mask/ camera.json
                 └──► ComfyUI API (/prompt) ─► Fun Control or VACE V2V (+ref image/LoRA)
                                     └─► 81-frame windows, shared seed, overlap
                 └──► FFmpeg/Remotion: stitch, upscale/interp, grade, audio
```
- Fit: 16 GB → run GGUF/FP8 + block-swap/offload, ≤ ~480–540p, 4–5 s windows, then upscale (e.g. SeedVR/ESRGAN-class, [UNV]) — measured data to date only covers TI2V-5B tiny res and MiniMax H3 (see §2.1); **Fun Control/VACE/LTX IC-LoRA on this machine are unmeasured**.
- Prereq: upgrade ComfyUI (0.34.6 is old; Fun Control/Animate need current build [DOC]) in a **separate portable install** to avoid disturbing the existing one (repo rule: additive).
- Strength: deterministic, zero marginal cost, no data egress, Apache-2.0 base. Weakness: resolution/length, "AI look" at low-res, temporal seams, VRAM juggling.
- Automation difficulty: **medium** — ComfyUI API workflow JSON is scriptable (already validated `/prompt`+history); custom-node dependency pinning is the cost.

## 8. External-provider route

```
Blender ─► rgb_previs.mp4 (+ref images, prompt, seed) ─► Runway Aleph 2.0 / Seedance ref / Kling MC
        ─► download + hash + provenance ─► QA gate ─► edit
```
- Strength: quality, resolution, duration (≤15–30 s), audio (Seedance/Veo). Weakness: soft structure, filters, price × rerolls, API/regional drift, face policies, no depth/mask inputs.
- Automation difficulty: **low–medium** — async REST everywhere; hard part is not code but ToS, moderation rejects and reproducibility (providers may change model weights silently; seeds not always honored [INF]).
- Rule: pin model ID + version/date, store request JSON and response ID.

## 9. Hybrid route (recommended)

1. Blender: finish animation + camera + timing; export package (§10) at draft (480p) and final res.
2. Local ComfyUI: depth/pose-conditioned drafts with 2–4 style prompts → select style + verify structural adherence cheaply.
3. Provider: final pass on selected shots with Aleph V2V (locked structure) or Seedance/Kling (acting/look), using the *same* package + chosen style frames.
4. Post: FFmpeg/Remotion; color match across providers; audio.
5. QA gates (video-production-qa skill): pose-track error vs previs, face-embedding sim vs sheet, camera-path IoU (silhouette/mask overlap), flicker metric, frame-count/fps exact match.

[INF] This reduces provider spend to ~1–2 calls per shot while the local pass kills bad prompts/styles early.

## 10. Recommended shot package contract (provider-neutral)

Directory per shot; all arrays are frame-indexed from 0 at shot-local frame 0 at `fps`. Adapters (Comfy / Runway / Seedance / Kling) *read* this and never mutate it.

```
shots/<shot_id>/
  shot.json                 # manifest (below)
  rgb/%04d.png | rgb.mp4    # lookdev previs, sRGB, even-sized, fps-locked
  depth/%04d.exr            # raw Z metres (camera-space)
  depth_norm/%04d.png       # 16-bit, near/far fixed in shot.json
  normal/%04d.png           # camera-space; axis convention in shot.json
  mask/<role>/%04d.png      # 8-bit; roles: char_<id>, prop_<id>, bg
  pose/%04d.json + pose.mp4 # OpenPose-18/DWPose, 2D px + confidence; rig mapping id
  lineart/%04d.png          # optional
  flow/%04d.exr             # optional, QA only
  camera.json               # per-frame matrix, lens mm, sensor, shift, DoF
  keyframes/first.png last.png mid_<n>.png
  refs/<char_id>/*.png      # character sheet views + face crop + license/consent file
  prompts.json              # positive/negative, style, per-provider overrides
  provenance.json
```

`shot.json` required fields:
```json
{
  "contract_version": "1",
  "shot_id": "yr_s010_c03",
  "fps": 24, "frame_start": 1001, "frame_count": 96,
  "resolution": {"draft":[854,480], "final":[1920,1080]},
  "color": {"rgb":"sRGB", "view_transform":"Standard"},
  "depth": {"units":"m","near":0.5,"far":12.0,"encoding":"inverse_16bit","convention":"near_white"},
  "normal": {"space":"camera","y_up":true,"z_toward_camera":true},
  "characters": [{"id":"yuri","mask":"mask/char_yuri","pose_rig":"humanoid_coco18","ref_dir":"refs/yuri","identity_lora":null}],
  "locks": {"camera":"hard","timing":"hard","composition":"hard","identity":"hard","style":"free","lighting":"soft"},
  "prompts": "prompts.json",
  "seeds": {"global":12345, "per_provider":{}},
  "provenance": "provenance.json"
}
```
`provenance.json`: blend file path + git SHA + SHA256 of `.blend` and bpy script, Blender version, render engine/samples, per-asset SHA256, exporter version, date; then per generation record: provider/model ID/version, endpoint, full request JSON (redact keys), response/task ID, seed (and whether honored), ComfyUI workflow JSON + custom-node commit pins + model file SHA256, cost, output SHA256, ToS/policy snapshot date, consent record ID for any real-person likeness, human QA verdict.

[INF] Rationale: store *raw* (EXR depth) and *derived* (normalized) separately so conversions are reproducible; `locks` tells adapters/QA what a failure means; no field is provider-specific except `per_provider` overrides.

Overlap with Cursor's R1: commit `81c7007 "R1 previs shot manifest and provider dry-run handoff"` exists on another branch; I did not read it for code. **Reconcile field names against it before either contract is adopted** (unresolved, §17).

## 11. Automation difficulty summary

| Route | API | Difficulty | Main fragility |
|---|---|---|---|
| Local ComfyUI | HTTP `/prompt`, WS progress | Medium | custom-node/version pinning, VRAM OOM, workflow JSON drift |
| Runway | REST+SDK, async | Low | credits, moderation, model deprecations |
| BytePlus Seedance | REST async task [COM] | Low–Med | region/face policy, schema (docs JS-gated) |
| Kling | REST/webhook; resellers | Low–Med | multiple resellers, terms |
| Higgsfield | REST/SDK/CLI | Low | single-vendor aggregator risk |
| Blender export | bpy script | Medium | pass normalization/axis conventions, pose rig mapping |

## 12. Tradeoff table

| Axis | Local Wan/LTX V2V | Aleph V2V | Seedance ref | Kling MC |
|---|---|---|---|---|
| Control fidelity | ★★★★ | ★★★ | ★★ | ★★★ (acting) |
| Camera lock | ★★★★ | ★★★ | ★★ | ★★ |
| Identity | ★★★ (+LoRA ★★★★) | ★★★ | ★★★ | ★★★★ |
| Final quality/res | ★★ | ★★★★ | ★★★★★ | ★★★★ |
| Marginal cost | ~0 | $$ | $ | $ |
| Privacy | best | egress | egress | egress |
| Determinism | high | low | low | low |
(All ratings [INF]; to be replaced by §15 E1–E5 results.)

## 13. Application: Yuri Room

[INF] — I did not read Yuri Room assets (not in this worktree; the earlier inventory states the workspace must not be modified).
- Fixed interior + one recurring character → the **ideal** case: locked camera + static background ⇒ depth/line/mask conditioning is stable; identity LoRA is worth training; background can even be a *rendered plate* with only the character region AI-restyled (mask route) to remove background flicker.
- Recommended: local-first (Fun Control/VACE at 480–540p drafts) → Aleph or Seedance final on 1–2 hero shots; keep IP local for unreleased content unless explicitly approved.
- Risks: stylised (anime/non-realistic) proportions vs human-trained pose models; use lineart+depth rather than pose if rig is non-human.

## 14. Application: Avatar promotional/video production

[INF] — "Avatar" interpreted as the user's own avatar product/brand promos, not the film; confirm.
- Shots are shorter, brand-critical, often with real-person likeness or product UI → **provider face-policy and consent are the gating issue**, not quality.
- Recommended: Blender previs defines product/camera moves; **provider route for final** (Seedance for look+audio, Kling MC if acting from a performer's reference video), local route for storyboards/animatics. Pre-clear likeness rights; keep consent records in `refs/<id>/`.
- Commercial: pin provider ToS date; prefer providers stating commercial usage (Higgsfield says so [MKT]; verify in contract).

## 15. Top 5 experiments (ordered by information gain per cost)

All must stay free/cheap unless noted; each is one small, scripted, logged run; no more than the stated spend.

1. **E1 — Measure adherence on existing local TI2V/ playground with a 2-s Blender test clip using existing pose-tracking** (cost: $0, ~1 h). Render a 48-frame grey-clay previs with a known motion (walking + camera dolly) and *extract pose + depth from the previs itself*. Score metrics harness (pose error, camera-path mask IoU, timing offset). **Info gain: builds the evaluator every later experiment needs and calibrates what "85–95%" really means.**
2. **E2 — Depth convention calibration** (cost: $0): feed Blender Z (normalized per-shot, near_white vs near_black, inverse vs linear) vs Depth-Anything estimates into Fun Control/VACE 480p 33 frames; pick the encoding that gives best adherence. Prevents the most common silent failure.
3. **E3 — Local 16 GB feasibility of Fun Control / VACE (GGUF/FP8) and LTX-2 IC-LoRA at 480–540p** in a fresh ComfyUI install (cost: downloads + GPU hours): record peak VRAM, wall time, max frames, OOM boundary. Fills the biggest unknown in §7.
4. **E4 — One paid Aleph 2.0 V2V call on 5 s previs (~$1.4, cap $5)** vs local result on same shot: structure adherence, identity drift, timing offset, cost/time. Confirms/refutes "AI re-skins finished animation" for a provider.
5. **E5 — Seedance 2.0 720p reference_video call with the same previs + 1 ref image (~$0.5–1, cap $3)**, plus verify first-party API schema, face-policy behavior with a *non-real* stylised character, and seed reproducibility (2 runs same seed). Settles API/policy unknowns.
(Kling MC and Higgsfield multiplexing deferred until E4/E5 show the structure-lock gap.)

## 16. DO-NOT-REPEAT

- Do not treat first/last-frame I2V as motion control; middle motion is invented.
- Do not normalize depth per frame; fix near/far per shot.
- Do not feed final-PBR, high-contrast lit previs when you want stylistic freedom; use neutral lookdev.
- Do not use reseller prices/specs as authoritative; bind to first-party page + date.
- Do not assume Wan 2.5+ open weights exist; the open line ends at 2.2 [COM, unverified at the primary source].
- Do not run Fun Control/VACE/LTX-2 on the existing ComfyUI 0.34.6 install; use a separate install (repo rule: additive).
- Do not substitute the community `uvx blender-mcp` for the official Blender Lab MCP (already in repo brief).
- Do not train/identify real-person likeness on a provider without consent records.
- Do not conclude success from screenshots; use numeric adherence metrics (matches repo QA rule).
- Do not run paid generations without a cap and a prior local control.
- Do not re-research: model list in §4 and primary-source fetch failures (LTX docs 403; BytePlus docs JS shell) — next pass should use a real browser session or the vendors' OpenAPI/SDK repos directly.

## 17. Unresolved unknowns

1. Official BytePlus Seedance 2.x request schema, limits, face policy — page was JS-gated.
2. Official LTX-2 IC-LoRA docs/license text — HTTP 403.
3. Aleph 2.0 max input duration, resolution, reference-image support, per-model credit table — not fetched.
4. Real VRAM/time of Fun Control / VACE / LTX IC-LoRA on RTX 4080 SUPER 16 GB — unmeasured.
5. Normal-pass axis convention compatibility with available ComfyUI normal models.
6. Whether any provider honors explicit seeds and camera paths.
7. Cursor R1 manifest (`81c7007`) field compatibility.
8. Yuri Room and "Avatar" specifics (asset style, real-person likeness) — assumptions in §13/§14.
9. Wan >2.2 and "Wan 3.0" status at a primary source.
10. Veo 3.1 reference-image API behavior (docs/API mismatch reported).

## Sources (fetched this session unless marked)

- https://docs.comfy.org/tutorials/video/wan/wan2-2-fun-control
- https://docs.dev.runwayml.com/
- https://higgsfield.ai/blog/higgsfield-api (vendor)
- https://en.wikipedia.org/wiki/Seedance_2.0 (secondary)
- https://kling.ai/quickstart/motion-control-user-guide (vendor)
- Search snippets only [COM/UNV]: runcomfy.com Wan 2.2 VACE; stable-diffusion-art.com Wan VACE V2V; huggingface.co Wan2.2-Animate-14B and comfy.org Animate workflow; docs.ltx.video IC-LoRA (403); github.com/Lightricks/ComfyUI-LTXVideo; docs.byteplus.com/docs/ModelArk/2291680 (JS shell); openrouter.ai/bytedance/seedance-2.0; atlascloud.ai Seedance/Aleph pricing blogs; discuss.ai.google.dev Veo 3.1 reference-images thread; runcomfy Blender+ComfyUI; docs.blender.org render passes manual; wan27.org / localaimaster Wan open-source status.
- Repo-local: `README.md`, `skills/*/SKILL.md`, `R1_CODEX_WORKSTATION_BRIEF.md`, `origin/research/local-video-gen-r0` (`LOCAL_VIDEO_GEN_R0.md`, inventory).
