# ComfyUI core VIDEO 경로 — CPU 연구 결과

기존 설치를 업데이트하지 않았다. Owned CPU process, 127.0.0.1:8192, 격리 input/output/temp/user, custom/API nodes disabled, CUDA/HIP invisible, OMP/MKL threads4. 테스트 후 owned server만 종료했다. 기존 서비스와 shared config는 변경하지 않았다.

Blender proxy greeting MP4 → LoadVideo → GetVideoComponents → CreateVideo → SaveVideo를 두 번 실행했다. 변경 변수는 SaveVideo argument style: legacy `format/codec` vs dynamic `format/format.codec`. 설치된 `nodes_video.py`와 `_io.py`를 읽어 graph를 만들었고 둘 다 성공했다. 동일 5초/24fps/120 frames/SDR8. 파일 hash는 prompt metadata가 달라 다르지만 동일 입력에 대한 decoded frame metrics는 일치한다.

Whole-clip SSIM=0.993819, decoded first/middle/last PSNR=41.72/41.22/41.35dB. Contact에서 얼굴/손/프레임 순서를 확인했다. 재인코딩 fidelity의 기술 PASS다. AI generation, identity preservation, hand continuity 개선의 실증이 아니다.

FFmpeg 9.0.1에서 이전 `-vsync 0` 옵션이 삭제되어 첫 frame-extract command가 실패했다. `-fps_mode passthrough`로 수정해 재현 명령을 저장했다. 실패를 모델 또는 Comfy failure로 오인하지 않는다.

Wan 5B A/B는 이어서 installed `execution.validate_prompt()`를 직접 호출해 검증했다. Queue, HTTP model `/prompt`, PromptExecutor를 실행하지 않았다. UNET/CLIP/VAE loader entrypoints는 호출 시 assertion 실패하도록 guard를 두었다. 실제 loader 호출=0, model inference=0. 두 graph 모두 backend validation PASS. 이것은 weights loading, RAM/VRAM suitability 또는 video quality PASS가 아니다.

GPU lease 재확인: 2026-10-02 10:37:31 UTC, PRODUCT_EXCLUSIVE 그대로. GPU 4080 SUPER 4241/16376MiB, utilization3%. 낮은 사용률과 stale PID로 owner lease를 회수하지 않는다. Owner release 전 모델 추론은 하지 않는다.

재현: system Python으로 `scripts/comfy_video_cpu_r3.py` → `scripts/qa_comfy_roundtrip_r3.py`. 기존 embedded Python으로 `scripts/validate_wan_graph_r3.py`. 구조 evidence는 `evidence/comfy-video-r3/`, 영상/contacts/owned user DB는 ignored `local/comfy-video-r3/`. Original source videos, models, credentials는 Git에 넣지 않는다.

다음 model experiment는 이미 준비된 한 샷 first-frame 유무 A/B다. 동일 model/prompt/seed/steps/size/frames/fps로 한 번씩 실행하고 identity/face/hand/motion/acting/camera를 평가해야 한다. 현 시점 효과는 UNTESTED다.
