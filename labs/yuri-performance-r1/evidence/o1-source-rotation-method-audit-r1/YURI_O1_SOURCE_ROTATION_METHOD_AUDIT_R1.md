# R4 source rotation method audit R1

결론: Blender source↔imported pose 회전 gate는 **FAIL 유지**다. 기존 float32 matrix→quaternion 변환을 float64 polar/SVD로 바꿔도 Index3 / Startle frame 17 오차가 남는다. 이 감사는 외형 승격이나 Unity 결과의 대체 판정이 아니다.

| 동일 sample의 방법 | 회전 오차 (degree) |
|---|---:|
| 기존 mathutils quaternion → normalized double dot | 0.0021210060720103056 |
| float64 polar/SVD → normalized double quaternion 2acos | 0.0021221062229851797 |
| float64 polar/SVD → relative matrix atan2 | 0.002122107853806262 |
| object × bone 곱셈도 float64로 수행한 diagnostic | 0.002121928285954439 |
| 기존 gate | < 0.001 |

6 Actions, 137 bones, 384 endpoint-inclusive frame samples = **52,608 bone samples**를 측정했다. Light 121 / Strong 97 samples는 각 2 cycles이며, unique authored frames는 276이다. helpers와 zero-weight bones도 포함한다. 6 clips 모두 같은 고정 회전 gate에서 FAIL이고 위치는 모두 PASS, 전체 최대 **1.5140681553463275e-6 m**다. clip별/per-bone worst는 `ALL_137_BONES_384_SAMPLES.json`에 기록했다.

저장 rest matrices에서도 Index3 오차 **0.0020957303287018622°**가 남는다. 기존 legacy rest 값 0.002089306749°와의 차이는 측정법 영향이지만, 둘 다 gate를 넘는다. 따라서 float32 quaternion 변환만으로 FAIL을 설명할 수 없다. 저장된 Blender reconstructed/evaluated transform의 회전 residual이 실제로 존재한다. FBX 원본 bind/Pose/Cluster 동일성은 이전 `EXACT_BIND_WIRE_RECEIPT.json`의 독립 wire 검사 결과이며 이번에는 exporter를 실행하지 않았다. 특정 importer 내부 연산 하나를 원인으로 확정하지 않는다.

모든 SVD 입력은 원래 evaluated float32 matrices를 float64 container로 보존한 값이다. 이미 소실된 source 정밀도를 복원했다고 주장하지 않는다. 기존 scale/hierarchy를 world matrix에 반영한 뒤 SVD `U diag(1,1,det(UVt)) Vt`로 SO(3) 성분만 추출한다. 모든 basis parity는 positive이고 최소 singular value는 약 0.33이다. translation, scale, handedness, serialized bytes를 보정하지 않았다. 직접 matrix-angle과 stable quaternion 4atan2 교차검증 최대 차이는 **1.64634e-13°**다. 2acos는 극소각에서 precision floor가 있어 matrix-angle과 최대 약 3.10930e-6° 차이가 있지만 gate 결론에는 영향이 없다.

NumPy-only 독립 재계산은 같은 worst **0.002122107853804401°**를 얻었다. 명시된 orthogonal P/H (reflection 포함)를 양쪽 입력에 동일 적용한 invariance check도 최대 **3.08399e-13°** 차이다. 이는 실제 Unity P/H를 추정한 값이 아니다. 현재 audit에는 consumer의 실제 Unity quaternion buffers/P/H가 없으므로 PM이 보고한 Unity maximum 0.00044220529964394403° 및 동일 case 0.00004220786122274481°를 재계산하거나 인증하지 않는다. Blender와 Unity importer 경로를 구분하고, 다음 비교에는 동일 Index3 frame 17의 consumer matrices/xyzw/P/H를 사용한다.

## 보존과 재현

R4 source, model/motion FBX, frozen ZIP, scratch importer blend, source matrices와 이전 FAIL evidence의 SHA256/size를 실행 전후 대조해 **모두 동일**함을 확인했다. source .blend는 열거나 저장하지 않았다. 두 차례 CPU factory read-only capture (첫 motion audit, 두 번째 기존 rest evidence 및 stable-angle 교차검증 추가)와 NumPy-only recheck만 수행했다. render/bake/export, 새 rig, mesh merge, donor geometry, shader/material/driver 수정은 없다. 08caad7 및 모든 기존 checkpoint를 보존했다.

`ROTATION_METHOD_AUDIT_RECEIPT.json`에 exact input hashes와 원래 mismatch matrix/quaternion buffer lineage를 기록했다. `INDEX3_STARTLE_FRAME17_METHOD_COMPARISON.json`에 같은 case의 full matrices, legacy/polar quaternions, singular values를 저장했다. 전체 frozen NPZ는 별도 audit packet에 있으며 원본 reference video/model ZIP을 Git에 재등록하지 않았다.

재현:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --factory-startup --background --disable-autoexec --python-exit-code 1 --python labs/yuri-performance-r1/scripts/r4_o1_source_rotation_method_audit.py
& 'C:\Program Files\Python313\python.exe' labs/yuri-performance-r1/scripts/r4_o1_rotation_buffer_recheck.py '<audit packet directory>/frozen_evaluated_matrix_buffers.npz'
```

첫 명령은 local frozen inputs가 필요하다. 두 번째는 packet의 NPZ와 NumPy만 필요하며 Blender/source 없이 재계산한다. immutable source appearance acceptance와 기존 animation Action/NLA 경로는 유지한다. 이번 packet은 structural/animation 측정 감사용이며 canonical character, runtime appearance, F2/F3, face/gaze, physics 인증이 아니다.
