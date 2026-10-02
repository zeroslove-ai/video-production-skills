# Native body timing R3 — 진행 중 checkpoint

R2 실제 비율에서 첫 세 semantic recipe의 body/head/hand 전달을 확인하는 private 연구 후보다. Yuri animation 납품, retargeting, physics/product integration은 하지 않는다. Face는 neutral이다. Actual A/O readability 실패로 고급 face recipe를 추가하지 않았다.

후보는 `local/native-body-r3/R2_NATIVE_BODY_TIMING_R3.blend`. User-supplied R2 original을 열었다. `evidence/native-body-r3/preservation.json`에서 원본 66 actions의 curves/handles/interpolation, mesh/shape geometry, skin weights, rest rigs fingerprints 동일성을 assert했다. Source binary SHA도 전후 동일하다. 연구 action 세 개를 추가했으며 완료된 작품 수가 아니다.

greeting: 얼굴 옆 wrist goal, anticipation, wave, hold, recovery. please: chest 앞 비대칭 wrist goals와 tilt/forward attention. shy: head/neck/chest 지연과 복귀. Face/gaze neutral이므로 native source 영상은 eye-lead 실증이 아니다. Eye-lead score/영상은 proxy에서 비교한다.

실패와 수정:

1. Angle 측정에서 q/-q 동등성을 빠뜨려 359° false alarm이 생겼다. 최소 물리 회전각으로 수정. 이전 JSON 보존.
2. 이후에도 please에 실제 half-frame 180° spin이 있었다. Quaternion key 부호 연속성 고정으로 제거.
3. greeting half-frame 36.38° elbow step. 대각선 pole을 바깥으로 변경 후 13.85°. Wrist 경로에 .07m 바깥 호 추가 후 12.06°.
4. Parent의 현재 orientation을 따라 회전을 누적하는 대신 bend-plane normal과 고정 roll로 bone basis 구성. greeting 최종 8.39°. Threshold 완화 없음. 이전 failure JSON에 candidate SHA 보존.

구조 gate: 241 samples/clip (24fps keys + half frames), 세 clip PASS. Max step greeting 8.39°/half-frame, shy 1.04°, please 5.16°. Root/foot drift=0, endpoint matrix difference=0. Max IK wrist error 약 1.38e-7m. **Mesh break, hand/contact, 자연스러운 1x 연기, silhouette 승인은 PENDING**.

먼저 3 clips × 3 cameras(full/waist 3/4/hand+face) × 6 frames를 CPU 렌더한다. 구조 PASS가 미학 PASS를 대신하지 않는다. 이후 결함 하나씩 수정하고 normal-speed video를 만든다. 다섯 camera의 lens/transform/target/resolution metadata도 저장했다.

재현: Blender factory-startup / CPU / threads4, `scripts/build_native_body_r3.py` → `scripts/render_native_body_r3.py -- qa` → `-- contacts`. 후보 변경 전 기존 렌더를 SHA별로 보존해야 한다. Video job은 구조 PASS와 SHA 일치 시만 시작한다.
