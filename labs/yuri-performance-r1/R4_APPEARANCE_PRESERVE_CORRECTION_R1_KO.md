# R4 Appearance Preserve Correction R1 — 2026-10-03

R4 외형의 유일한 authority는 `source/Character_Master_NeckSkin_R4.blend`다. 원본 파일 SHA256은 a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa이며 다운로드 원본과 byte-identical이다. 외형 승격이나 새로운 캐릭터 제작을 하지 않았다.

기존 08caad76e6a279d07698cbfaa33d5c50f2aa097d 및 이전 bundle/FBX/GameRig/master는 보존했다. 그 GameRig는 **structural/animation compatibility experiment ONLY**이며 canonical character로 사용하면 안 된다. 이 checkpoint가 원본 외형 보존 규칙을 추가한다.

| Acceptance | 결과 / 증거 |
|---|---|
| neutral geometry / topology / UV / attributes | 동일, append·save/reopen·ON→OFF hash diff={} |
| material slots / shaders / nodes / packed textures | 동일, 19 materials 유지 |
| ShapeKeys / expression drivers | 동일, 원본 head 72 keys 포함 |
| skin weights / modifier settings | 동일, source native DQ·GN·surface corrections 유지 |
| hierarchy / rest pose / bind helper pose | 동일, 원본 4 rigs / 97 objects 유지 |
| original Action curves | 원본 R4 78개 동일; R2 원본 66개 파일은 건드리지 않음 |
| animation OFF neutral pixels | 960×920 source camera + 256×384 full-body QA 모두 unequal RGBA channels=0, max diff=0 |
| ON→OFF neutral pixels | 위 두 구도 모두 exact 동일 |
| Action library | 6 physical + 2 existing QA Actions, geometry/rig/material/image 0개 |
| actual bone motion / loop | 6 clips 전 프레임 검사 PASS, Light/Strong 각각 2 cycles |
| Unity runtime / appearance | 미검증; 외형 승격 없음, AlwaysAnimate 필수 gate 유지 |

신규 GameRig/mesh merge/body substitution/donor geometry append는 0회다. 원본 R4가 이미 가지고 있는 얼굴·헤어 assembly와 gaze/face drivers를 그대로 사용한다. ON에서는 기존 Meshy_Fitted_Rig에 Action만 연결하고, OFF에서는 원래 pose channels, frame, action slot/binding metadata까지 복원한다. Blender Action/NLA 경로를 선택했고 새 캐릭터 FBX/VRM을 만들지 않았다.

정상속도 proof: `sequence_24fps.mp4` (11초: Lift_Start → Light 2 cycles → Release placeholder → Land_Soft → BalanceRecover), `strong_2cycles_24fps.mp4` (4초), `startle_24fps.mp4` (1.5초). 24fps의 실제 authored 시간을 유지하며 endpoint 중복 한 프레임만 encode에서 제외한다. 전체 PNG와 joint checks는 전 구간 기준이고 MP4 전체 decode를 검증한다. 큰 mesh explosion/face detachment/root teleport는 관찰되지 않았다. 낮은 preview sampling noise는 원본과 동일한 QA 렌더 설정이며 shader 수정으로 제거하지 않았다.

원본 source camera/조명/구도는 authoritative neutral PNG에서 유지한다. CPU Cycles 8 samples, seed=0, animated seed OFF, denoise OFF, RGBA8 PNG가 동일하게 적용된 QA overrides다. 별도 전신 camera/resolution 변경은 저장하지 않는 QA process에서만 적용했다. master는 원래 scene/render/camera 설정과 animation OFF 상태로 저장되어 있다. `neutral/authority_source_camera_before.png`를 기준으로 삼고 `metadata/pixels_*.json`의 decoded pixel SHA를 확인한다.

## 사용법

1. Blender 5.2에서 `Character_R4_Animation_OFF_20261003.blend`를 열면 원본 외형과 neutral/driver/binding 상태이고 reaction은 재생되지 않는다. 원본 R4 78 Actions + 추가 8 Actions만 존재한다.
2. 원본 파일에서 시작하려면 `YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend`의 Action datablocks만 Append한다. Object/Collection/Mesh/Armature/Material append나 rig rebuild는 금지한다.
3. Python Console에서 아래 adapter를 사용한다. source rigs/constraints/face/gaze drivers를 clear/reset/mute하지 않는다.

```python
import sys
sys.path.insert(0, r"<bundle>/workflow")
from r4_appearance_adapter import ReactionLane
lane = ReactionLane()
lane.on('YRA_R4_QA_MilestoneA_Sequence')
# Timeline 1..265, 24 fps로 재생. 24fps 설정은 QA session에서만 변경.
lane.off()  # source frame / pose / action slot 상태를 정확히 복원
```

adapter는 원본 hierarchy의 Blender playback용이다. Unity Runtime adapter를 구현했다고 주장하지 않는다. `metadata/clip_mapping.json`은 future IPhysicalAnimationLane 연결을 위한 mapping/data contract이며 Active Ragdoll 구현은 없다. Unity에서는 canonical source / animation-only asset / runtime adapter를 분리하고, state-entered / normalized-time / weight>0 / AlwaysAnimate / 실제 bone motion / mesh/root / loop2cycles를 해당 owner가 검사해야 한다. 제품 repo는 수정하지 않았다.

재현: workflow의 saved bpy scripts와 metadata receipts를 참고한다. authoring build/QA scripts는 이 Desktop 연구 workspace 경로를 기록하고, 휴대 가능한 playback은 위 Action library + adapter 경로다. 기존 foot cleanup·retarget curves를 다시 제작하지 않고 재사용했다. 검사 구현의 실패와 수정은 metadata/failure_correction_log.json에 남겼다.

다음 bounded experiment는 원본 authority와 분리된 Unity native animation-only import가 source shader/face/gaze adapter와 충돌하지 않는지 검증하는 것이다. Unity 외형 동일성이나 Humanoid/VRM 적합성은 이 Blender PASS에 포함되지 않는다.
