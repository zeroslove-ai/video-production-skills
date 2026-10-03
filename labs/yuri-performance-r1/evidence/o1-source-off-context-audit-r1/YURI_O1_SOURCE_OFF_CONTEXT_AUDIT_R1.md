# Source OFF context contract R1

기존 frozen metadata만으로 baseline 계약을 확정했다. **새 Blender job, source open/save, render/bake/export 0회**다. `SOURCE_OFF_CONTEXT_CONTRACT.json`에 전체 137 bone matrix pointers, 21 renderer matrix/vertex/stack/bind pointers, 사용한 metadata/arrays/scripts SHA256를 기록했다.

Source-authoritative neutral은 **frame 1, 4 rigs 모두 active Action=null**, source evaluated OFF다. body Reaction Action 첫 frame, identity pose, raw rest와 혼용하면 안 된다. `source_expanded_rigs.json` 각 bone의 `local_rest`/`armature_rest`/`world_rest`는 raw rest, `neutral_pose_channels`/`neutral_evaluated_armature`/`neutral_evaluated_world`는 기존 default channels와 constraints/drivers가 적용된 OFF다. renderer bind metadata에도 raw rest와 evaluated neutral inverse가 각각 있다.

Source 5개 R3 bind helpers (Head, Neck, Shoulder L/R, UpperChest)는 scale 약 **1.869159**를 가지고 있다. body object world scale 약 **0.5350000262**와 함께 원본에 존재하는 값이다. helper를 identity로 reset하거나 bind/rest를 고쳐 비교를 통과시키지 않는다. body parent/path, 얼굴 COPY_TRANSFORMS, hair follower/drivers, source ordered modifiers와 ShapeKeys를 모두 보존한다.

Recovery neutral reference의 3 rigs / 124 bones world matrices와 native expanded OFF matrices는 최대 matrix element delta **0**이다. FaceBoard 13 bones는 recovery reference `rig_pose`에 빠져 있으나 native expanded metadata에 전부 있으므로 해당 exact hash/pointer를 사용한다. 21 renderer의 world matrices와 ordered stack은 `source_renderers_bind.json`, 상세 GN/masks/ShapeKeys는 `mesh_slot_UV_attributes_shape_deltas.json`에 있다.

Manual-morph zero/half/peak 생성 코드는 immutable source를 열고 기존 input key 값만 임시 변경하며 `frame_set(1)`한다. body Action/pose reset 코드는 없다. dense half는 같은 `setinput`/`evaluate` 함수의 AST를 그대로 재사용했다. 기존 receipts의 source component diff=0이며 half summary가 기존 half summary와 모두 정확히 일치한다. half/peak 각각의 별도 rig matrix snapshot은 없다. 동일 body context는 생성 코드/보존 receipts로 뒷받침하되 별도 per-case 측정이 있었다고 주장하지 않는다.

Recovery `neutral.npz` world array는 explicit float64 object matrix 곱셈 뒤 float32 저장, manual/half 함수는 matrix buffer float32 곱셈 뒤 float32 저장이다. 기존 zero reference 간 residual 최대 약 **1.666e-8 m**는 정밀도 차이이며 37 cm 오차의 설명이 아니다. 모든 `*_world_position`은 해당 object world transform/scale이 이미 반영된 meters다. 다시 0.535를 곱하지 않는다. local 배열에는 정확한 renderer object matrix를 한 번만 적용하고 world 배열은 그대로 coordinate conversion에 넣는다.

PM이 전달한 immutable Unity body A/B 결과는 `useScale=false` max **0.369968202 m** / RMS **0.235387318 m**, `useScale=true` max **7.3214657505e-7 m** / RMS **2.9152165e-7 m**다. 이 결과는 consumer의 measurement scale semantics를 분리한다. 이전 posed baseline 가설은 확정되지 않았으며 그 가설을 근거로 source reset/new capture를 수행하지 않았다. worker가 실제 consumer A/B buffers를 재계산한 것은 아니다. Unity `BakeMesh`는 renderer 기준 좌표를 반환하고 `useScale`에 따라 Transform scale 보상 방식이 달라지므로 flag와 world conversion을 함께 기록해야 한다. [Unity 공식 API](https://docs.unity3d.com/ScriptReference/SkinnedMeshRenderer.BakeMesh.html).

독립 consumer A/B 재검증에 필요한 것은 **A/B baked vertex buffers + useScale flag + actual renderer localToWorldMatrix/lossyScale + coordinate conversion P/H + correspondence hash**다. source OFF 측의 all137/21 pointers는 이미 제공됐다. half/peak per-case rig snapshot은 필요한 경우 명시된 별도 누락 필드지만, 현재 scale A/B로 분리된 37 cm discrepancy를 이유로 재추출하지 않는다.

Blender importer rotation FAIL, 실제 DQ/7weights deformation HOLD, gaze/GN HOLD, material/PBR visual HOLD는 유지한다. 이 source-context receipt가 runtime 구현/appearance acceptance를 대신하지 않는다. 기존 source/FBX/frozen ZIP/08caad7과 연구 checkpoint를 삭제하거나 덮어쓰지 않았다.

재현 (Python + NumPy, 기존 frozen local metadata 필요):

```powershell
& 'C:\Program Files\Python313\python.exe' labs/yuri-performance-r1/scripts/r4_o1_source_off_context_audit.py
```
