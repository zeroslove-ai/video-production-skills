# Dance reprojection R2 — 같은6초의 손 궤적 보정

R1의3개 실제 extraction 비교에서 이어졌다. 새 extractor가 아니다. MediaPipe2D+MotionBERT 결과의 normalized target arm positions만 보정했다. Body/root/legs/head는 기존360frames와 동일하며 source SHA를 고정했다. 정확한 world dance acceptance는 계속 FAIL이다.

목표는 target upper/lower arm 길이를 유지하면서 source 화면의 elbow/wrist 궤적을 재현하는 것이다. R1의 모든 shoulder/hip frames에서 얻은 하나의 orthographic camera fit을 고정했다. per-frame alignment를 하지 않는다. 실제 camera intrinsics/world depth가 확인됐다는 뜻은 아니다.

팔은 spherical directions와 실제 target lengths로 표현했다. residual 가중치는 wrist XY1.8, elbow XY.8, depth prior.35, original direction.04, previous direction.025다. 첫 unconstrained least-squares는 detector 대비 mean wrist error를 좌30.71→2.08px, 우64.13→1.24px로 줄였다. 그러나 direction step94.5/117.4deg와 baked quaternion step158.91deg를 만들어 폐기했다. 화면 오차만 줄이면3D depth branch를 넘나들 수 있다는 실패 증거를 보존했다.

두 번째는 SLSQP로 upper/lower directions의 프레임 간 변화를20deg 이하로 제한했다. target 길이를 유지해 positional bake하고 roll parallel transport와 quaternion hemisphere continuity를 적용했다.

| Fixed camera 비교 | Before | Constrained after |
|---|---:|---:|
| detector 대비 왼손 mean px |30.71|2.29|
| detector 대비 오른손 mean px |64.13|6.82|
| 독립 수동 wrist11labels mean px |62.17|16.73|
| 수동 wrist p95 px |157.54|35.27|
| 전체 bone 최대60fps step deg |20.07|20.08|
| actual target mesh 대 model source-mask 평균 IoU |.5905|.6169|
| target mesh ROI boundary clipping frames /360 |41|3|

새 수동 labels는20.5/21.5/22.5/23.5/24.5/25.5초 source-only unmarked grids를 보고 기록했다. uncertainty20px이고 가려진 wrist 하나는 제외했다. 이 frames의 detector observations는 solver 입력이므로 held-out motion input이 아니라 independent manual-label audit이다. 24.5초 수동 label이 옆 performer의 팔을 따라간 오류를 enlarged source-only crop에서 발견했다. 원래 실패 label을 보존하고 선택 dancer의 waist wrist로 수정했다. 추출값에 맞춰 label을 대체하지 않았다.

6초360motion frames를 검사하고180frame30fps 비교에 source audio를 time-sync했다. reference, detector/before/after wrist overlay, original3D, rejected3D, constrained3D 전체1x playback을 확인했다. rejected candidate의 큰 pop을 숨기거나 좋은 still만으로 판정하지 않는다.

reference detector wrist speed 대 target 전체 curve 상관 lag는 after 좌/우0ms다. 개별 reference speed peak의 가장 가까운 target peak 차이는 평균 좌5.26ms, 우42.86ms다. before69.30/86.51ms에서 개선됐다. audio transient proximity도 기록했지만 music/choreography beat label이 아니므로 beat accuracy PASS를 선언하지 않는다. 20deg 제한이 빠른 true direction change를 약화할 수 있어 오른손 일부 peak는 추가 검사해야 한다.

silhouette는 capsule 대신 실제 skinned Blender proxy mesh를 CPU Cycles alpha로 모든360frames 렌더했다. floor를 숨기고 fixed camera를 유지했다. source mask는 MediaPipe segmentation이므로 수동 GT가 아니며 skirt, head/body proportions, neighbouring overlap 차이가 남는다. IoU 개선은 해당2D fit의 개선이며 원본 performer silhouette를 동일하게 재현했다는 뜻은 아니다.

root/world depth/floor/contact 정확도는 이 실험에서 해결하지 않았다. wrist orientation/fingers/head yaw·pitch/face도 새로 추출하지 않았다. finite/mesh 검사가 안무 accuracy를 대신하지 않는다.

## 재현

1. `dance_reprojection_solve_r2.py` 또는 `... stable`로 실패/제약 후보를 분리한다.
2. Blender `dance_reprojection_bake_r2.py` 또는 `... -- stable`로 private candidate를 저장한다.
3. `dance_render_r1.py -- motionbert_reprojection_stable`로360frame QA/180frame preview를 만든다.
4. `dance_reprojection_qa_r2.py`로 frozen camera/manual labels/time-domain QA를 수행한다.
5. `dance_silhouette_render_r2.py -- METHOD`와 `dance_silhouette_qa_r2.py`로 actual mesh를 검사한다.
6. `dance_reprojection_package_r2.py`로 source-audio time-synced1x 비교를 만든다.

candidate .blend/GLB, baked joint positions, optimizer target/실패, manual audit/수정, all-frame QA, silhouette scores와 영상은 local package에 포함한다. 원본 source video/model weights는 Git/package에서 제외한다. source pixels를 포함한 비교 영상도 Git에서 제외한다.

다음은 independent shoe-contact strike/lift annotation과 perspective-aware full-body optimization이다. torso/root/knee까지 jointly constrain하고 metric depth ambiguity를 별도 표시한다. GVHMR는 product owner의 GPU lease 해제와 licensed SMPL setup 후 비교한다. accuracy gate를 통과하기 전 후렴/전체 dance로 늘리지 않는다.
