# Full original body deformation reference R1

Immutable R4 `a30fc513…` + existing Action library `6874ec69…`를 사용해 **6 clips / 276 unique endpoint-inclusive authored frames**의 full original modifier stack을 실제 CPU job으로 추출했다. body **63,561 vertices / 254,602 original loops / 63,781 polygons**, 7개 source modifiers를 유지한다. 새 rig/FBX/export/render/bake/Unity 구현은 없다.

기존 frozen native pose reference를 재사용하고 **137 bones × 276 frames**의 evaluated world matrices를 매 frame 대조했다. 최대 matrix element delta **0**이며 새 bone buffer를 중복 생성하지 않았다. `.535` body hierarchy와 posed 5 R3 bind helpers, original rest/weights/morphs/drivers/materials/modifier order를 유지했다.

각 frame에서 local/world positions, local/world averaged vertex normals, **별도 local/world split corner normals**를 source index 그대로 저장했다. 모든 frame의 original loop→vertex, polygon loop start/total/material slots, UV를 frozen original mesh NPZ와 정확히 대조했다. split corner normal은 vertex 평균으로 축약하지 않는다. original UV/material/triangulation/corner-basis authority는 manifest input hashes/pointers로 재사용한다.

World position은 float64 object matrix transform을 한 번 적용한 후 float32 저장한다. world normal은 row `normalize(n inverse(A))`, 즉 column inverse-transpose convention이다. Blender Z-up meters, 자동 handedness/Y conversion 없음. 모든 배열은 finite이며 shape/count와 write/read-back exact equality를 chunk별 검사했다. custom normal과 averaged vertex normal 차이가 있는 12 corners도 보존했다 (최대 vector difference 약0.607067).

**72 NPZ chunks**, chunk당 최대 uncompressed **36,645,520 bytes**. 총 NPZ **1,393,561,507 bytes**이며 큰 단일 geometry buffer를 만들지 않았다. 한 CPU factory job, 1 worker / Blender4threads, 약144.56초. shared GUI/GPU 사용 없음. OFF baseline은 기존 `neutral.npz`와 exact equality이며 각 clip 종료 후 position과 모든 normal array OFF return=0, source 전체 component diff=0, 원래78Actions/input bytes unchanged다.

Light 61→121 samples, Strong49→97 samples, 전체 **384 loop-inclusive samples**의 명시적 time/frame mapping을 제공한다. cycle2의 재사용 대상108 samples는 해당 source frame을 다시 full-stack evaluate해 **모든 position/normal 배열 bit-identical**을 확인했다. 단지 이름/주기를 근거로 재사용하지 않았다. 매 clip의 실제 vertex motion>0도 기록했다. `FULL_BODY_DEFORMATION_MANIFEST.json`에 mappings/chunk SHA256/pose correspondence/motion/OFF/CPU receipt, `SOURCE_COMPONENT_DIFF.json`에 before/after source fingerprints가 있다.

Outbox ZIP volumes는 각각 ≤100MiB이며 모두 독립적으로 읽을 수 있다. 전부 같은 destination에 추출한다 (raw-byte split/concatenate 방식 아님). 각 archive SHA256와 aggregate per-file manifest SHA256, CRC 검증은 `PACKET_CUSTODY.json`에 있다. Git에는 compact metadata/receipt/script만 등록한다.

Reference data custody 완료이며 runtime deformation PASS가 아니다. 실제 Unity original DQ + masked LBS + corrective/surface stack + 7-influence 구현/전체 frame 비교가 다음 consumer gate다. 기존 Blender imported rotation FAIL, material/PBR/gaze 및 F2/Player gates를 대체하지 않는다.
