from __future__ import annotations

from typing import Any


SIGMAS_8_STEP = "1.0, 0.99375, 0.9875, 0.98125, 0.975, 0.909375, 0.725, 0.421875, 0.0"


def build_ltx25_i2v_workflow(
    *,
    image_name: str,
    positive_prompt: str,
    negative_prompt: str,
    seed: int,
    width: int,
    height: int,
    frames: int,
    filename_prefix: str,
) -> dict[str, dict[str, Any]]:
    """Build the proven native LTX-2.5 single-stage distilled I2V API graph."""
    if width < 256 or height < 256 or width % 32 or height % 32:
        raise ValueError("LTX width and height must be at least 256 and multiples of 32")
    if frames < 9 or (frames - 1) % 8:
        raise ValueError("LTX frame count must follow 8k+1 (for example 73 or 121)")
    if not image_name or "/" in image_name or "\\" in image_name:
        raise ValueError("image_name must be a filename inside ComfyUI's input directory")

    return {
        "1": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "2": {
            "class_type": "ImageScale",
            "inputs": {"image": ["1", 0], "upscale_method": "lanczos", "width": width, "height": height, "crop": "center"},
        },
        "3": {"class_type": "CLIPLoader", "inputs": {"clip_name": "gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors", "type": "ltxv"}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["3", 0], "text": positive_prompt}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["3", 0], "text": negative_prompt}},
        "6": {"class_type": "LTXVConditioning", "inputs": {"positive": ["4", 0], "negative": ["5", 0], "frame_rate": 24.0}},
        "7": {"class_type": "VAELoader", "inputs": {"vae_name": "ltx-2.5-audio-vae-bf16.safetensors"}},
        "8": {"class_type": "VAELoader", "inputs": {"vae_name": "ltx-2.5-video-vae-conv-bf16.safetensors"}},
        "9": {"class_type": "UNETLoader", "inputs": {"unet_name": "ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors", "weight_dtype": "default"}},
        "10": {"class_type": "LTXVPreprocess", "inputs": {"image": ["2", 0], "img_compression": 18}},
        "11": {"class_type": "EmptyLTXVLatentVideo", "inputs": {"width": width, "height": height, "length": frames, "batch_size": 1}},
        "12": {"class_type": "LTXVImgToVideoInplace", "inputs": {"vae": ["8", 0], "image": ["10", 0], "latent": ["11", 0], "strength": 0.7, "bypass": False}},
        "13": {"class_type": "LTXVEmptyLatentAudio", "inputs": {"frames_number": frames, "frame_rate": 24.0, "batch_size": 1, "audio_vae": ["7", 0]}},
        "14": {"class_type": "LTXVConcatAVLatent", "inputs": {"video_latent": ["12", 0], "audio_latent": ["13", 0]}},
        "15": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "16": {"class_type": "CFGGuider", "inputs": {"model": ["9", 0], "positive": ["6", 0], "negative": ["6", 1], "cfg": 1.0}},
        "17": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler_ancestral"}},
        "18": {"class_type": "ManualSigmas", "inputs": {"sigmas": SIGMAS_8_STEP}},
        "19": {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["15", 0], "guider": ["16", 0], "sampler": ["17", 0], "sigmas": ["18", 0], "latent_image": ["14", 0]}},
        "20": {"class_type": "LTXVSeparateAVLatent", "inputs": {"av_latent": ["19", 0]}},
        "21": {"class_type": "VAEDecodeTiled", "inputs": {"samples": ["20", 0], "vae": ["8", 0], "tile_size": 512, "overlap": 64, "temporal_size": 64, "temporal_overlap": 8}},
        "22": {"class_type": "LTXVAudioVAEDecode", "inputs": {"samples": ["20", 1], "audio_vae": ["7", 0]}},
        "23": {"class_type": "CreateVideo", "inputs": {"images": ["21", 0], "audio": ["22", 0], "fps": 24.0, "bit_depth": "auto"}},
        "24": {"class_type": "SaveVideo", "inputs": {"video": ["23", 0], "filename_prefix": filename_prefix, "format": "mp4", "codec": "h264"}},
    }
