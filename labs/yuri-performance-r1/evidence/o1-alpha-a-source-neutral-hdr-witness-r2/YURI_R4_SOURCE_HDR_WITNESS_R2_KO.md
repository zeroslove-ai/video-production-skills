# R4 immutable source neutral HDR witness R2

새 Windows 기능 없음. 외형 승격 없음. R4 source, product Unity, GUI Blender, GPU lease를 변경하지 않았다.

## DONE

- Canonical source SHA256: `a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa`. Source byte clone으로 frame 1 / Assembly_Review_Camera / 960×920를 CPU 렌더했다. 원본 파일 저장·geometry·material·pose·light 조정 없이 한 Render Result에서 EXR32 RGBA ZIP 및 PNG를 저장했다.
- 원래 camera/world/area lights/compositor/color operands의 실행 전후 동일성을 확인했다. 원본 compositor node group은 null이다. AgX / Medium High Contrast / exposure +0.25EV / gamma 1 / sRGB display를 유지했다. Render I/O와 CPU resource overrides만 별도 기록했다.
- 기존 authoritative neutral PNG와 이번 PNG의 decoded RGBA 전체 배열이 **동일**, 최대 차이 **0**, changed pixels **0**이다. 파일 SHA는 PNG 저장 metadata 때문에 서로 다르다; decoded pixel equality와 file equality를 구분한다.
- HDR global RGB maximum **9.130925**. EXR에서 읽은 float32 RGBA NPZ와 5개 hair/face patch 통계를 재계산하고 exact mean/count를 검증했다. Top-left 기준 xyxy이며 NPZ의 shape는 `(920,960,4)`다. 모든 값이 finite다.
- Native PID **124432**, before/after live identity barriers PASS, owned process exit **0**, terminal Job active **0**, cleanup errors 없음. Wall **11.7799s**, combined bounded output **12,459,789 bytes**. 이는 이번 실행의 receipt이며 과거 native 실패를 변경하지 않는다.
- Private packet **13,964,358 bytes / 30 members**, ZIP 내부 29개 evidence/workflow 파일을 SHA256로 재검증했다. Source model/mesh는 포함하지 않는다.

## FAILED / HOLD

- R1은 Blender 5.2의 `Scene.node_tree` 접근 오류로 **render 전 실패**했다. 실패 collector/config/approval/guard/traceback을 packet에 그대로 보존했다. R2는 `compositing_node_group` read-only 접근으로 수정한 별도 collector와 새 실행 receipt다.
- `Render Result.pixels`의 direct float access는 이 실행에서 unavailable이다. Raw Render Result → EXR exact pixel equality를 주장하지 않는다. NPZ는 실제 저장 EXR의 Blender float-image decode이다. Generic RNA serializer가 loader colorspace 이름을 기록하지 못했으므로 해당 이름의 직접 관찰을 주장하지 않는다.
- 8 samples / seed 0 / denoising OFF의 preview witness다. Noise/specular outlier를 제거하지 않았다. Patch는 수동 image rectangle이며 object-ID mask가 아니다.
- Source area-light의 absolute response와 Unity의 절대 조명 일치, appearance/PBR promotion은 **HOLD**. RGB peak나 PNG 일치만으로 다른 renderer의 조명 calibration을 PASS할 수 없다.

## Receiver operands / next bounded comparison

Packet `witness/SOURCE_RENDER_OPERANDS_PRIVATE_R1.json`에 camera transform/projection, light transform/type/energy/color/shape, world nodes, original view/display/compositor operands, render overrides를 담았다. Source area geometry와 위치를 유지한 비교가 필요하다. Source watts를 directional light 값으로 임의 치환하지 않는다.

`witness/SOURCE_NEUTRAL_SCENE_LINEAR_20261004_R2.exr` 또는 `SOURCE_NEUTRAL_LINEAR_RGBA_TOP_LEFT_PRIVATE_R1.npz`의 선형 RGB를 먼저 비교한다. `HDR_WITNESS_NATIVE_RECEIPT_PRIVATE_R1.json`의 동일 ROI를 사용한다. Display 비교에는 원본 AgX look과 exposure를 한 번 적용한다; 이미 표시 변환된 PNG에 재적용하지 않는다. 표시 변환과 scene-linear 수치의 역할은 [Blender color-management 문서](https://docs.staging.blender.org/manual/en/latest/render/color_management/displays_views.html)에 따른다.

Receiver는 원본 SHA, frame, camera/world/light operands 및 색상 경로를 먼저 대조하고 선형 patch response를 보고 다음 한 변수를 선택한다. 이 packet은 원본 밝기 headroom을 제공하며 제품 변경이나 새로운 exporter를 요구하지 않는다.

## Immutable correction continuity

기존 `08caad7`을 삭제/덮어쓰지 않는다. Corrective checkpoint `820a237`의 geometry/material slots/ShapeKeys/skin weights/rest pose/drivers/OFF pixel 보존 결과와 6개 reaction Blender-native 정상속도 재생 증거를 그대로 재사용한다. 이번 작업은 해당 neutral authority의 HDR 증거를 추가한 것이다. Unity AlwaysAnimate regression gate는 여전히 REQUIRED/PENDING이며 Unity 검증으로 승격하지 않는다.

## VISUAL_EVIDENCE / receiver packet

- Private packet: `C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/YURI_R4_SOURCE_NEUTRAL_HDR_WITNESS_R2_20261004.zip`
- Packet SHA256: `cd47090a80f6fece8be8dc2672ab2ebd1ccba0e74e2344e13ae0e6144d975198`
- PNG: `C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-alpha-a-source-neutral-hdr-witness-r2/SOURCE_NEUTRAL_AGX_DISPLAY_20261004_R2.png`
- Exact guard receipt SHA256: `513ced886cbb8a13536a54fb1849d3346f0d97370eb6aab25c6abf4ef2c3d835`
- Public receipt: `HDR_PACKET_RECEIPT_R2.json`; complete numerical source operands remain private.

Source/clone input hashes and source SHA were unchanged through execution and packaging. GUI Blender PID 129152 retained creation time 2026-10-02 23:17:57; GPU lease retained PRODUCT_EXCLUSIVE. No provider inference, source save, model export, or Unity write occurred.
