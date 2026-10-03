새 Windows 기능 없음 — MORPH67 두 입력의 기존 source normal 증거 부족을 확인하고, 미실행 비교 제안서를 준비했다.

DONE: Laptop commit **c04dda59635d400a6cf174229a196311726c2b75**에서 요청한 WORST/NEUTRAL `source_inputs.json` 두 파일만 읽어 private local cache에 고정했다. SHA256은 각각 **170accdfe80954ae2fe340e1aca3bdef5ac2e7fd25049be2089ab69766bd77a2** / **b775d6252cc4e9c3703d76e5747a7113bfb5d8318f1d1ff5e9b2b73df5d53961**. Numeric vectors/71 morph weights는 공개 복제하지 않는다. JSON contract에 exact original repository/private local paths/bytes를 제공한다.

두 입력 모두 native/applied FACE16 및 GAZE2가 동일하며 ReactionIntent=NONE이다. **NEUTRAL에도 작은 Smile FACE 입력이 있고 source zero-input neutral과 같지 않다.** R3 원본145 samples에서 native FACE16 RNA order를 확인했고 두 exact controls와 일치하는 integer sample은 없다. 가장 가까운 sample의 max FACE/GAZE 차이는 WORST frame31 **0.027257204432098336**, NEUTRAL frame1 **0.009811968**이다. 시간 보간한 normal을 만들거나 tolerance로 같은 입력으로 간주하지 않는다.

기존 증거와 부족한 항목:

- Static head: source **12,928 vertices / 66,861 corners / 21,701 polygons**, `custom_normal` CORNER/INT16_2D는 `attribute_19_value`이다. 정확한 signed short2 fan encoding이며 xyz delta가 아니다. 원본 sharp/smooth/adjacency/UV/relative Keys는 기존 NPZ·semantic receipt에 있다.
- Evaluated gaze: 기존5개 neutral/cardinal cases는 source FACE 모두0, frame1/OFF body 기준의 실제 head local/world CORNER normals와 UV tangents/sign이다. 5개 NPZ SHA를 다시 확인했다. 둘 다 새 입력의 witness가 아니다.
- R3: 145 head binary records는 **POSITION-only**이며 metadata에 normal/tangent buffers가 없다. BEFORE raw original POINT normals는 새 입력의 evaluated CORNER normals가 아니다.
- 실제 부족: exact WORST/NEUTRAL의 shape→GN→Armature stages에서의 evaluated CORNER normals, custom-normal attribute type/domain/payload propagation 및 tangent/sign. Consumer postskin/world 비교에는 actual samepose bones/matrix/corner correspondence도 필요하지만 이 두 input JSON에는 없다.

최소 source contract: original relative ShapeKeys와 원본 driver outputs를 먼저 평가한다. FACE16에 해당하는 기존13 bridge drivers는 muted 상태를 유지하고 나머지37 driver가 EyePath/correctives를 계산하게 둔다. Consumer71 weights를 source에 강제로 쓰지 않는다. Head modifier order는 **Face true gaze before head deformation (GN) → Armature**이다. GN의 geometry chain은 Group Input→Set Position(FaceIris.L)→Set Position.001(FaceIris.R)→Group Output이며 cached graph에는 Set Shade Smooth/Set Mesh Normal node가 없다. 원본 drivers/masks/offsets를 그대로 둔다.

Pinned `mesh_normals.cc`/`mesh_runtime.cc`의 기존 semantic receipt: current positions·original polygon/corner-edge adjacency·sharp/smooth fan으로 normal spaces를 만들고 원본 packed short2를 decode한다. Positions 변경은 normal caches를 invalidate한다. Static normal의 LBS/triangle averaging/vertex averaging, 또는 zero blendshape normal delta를 source-equivalent라고 가정하지 않는다. Exact evaluated attribute propagation은 새 두 입력에서 아직 관측하지 않았고 제안된 capture가 답할 질문이다.

FAILED-HOLD: **새 native 실행 승인 없음.** 과거 sampler 승인은 소진됐으며 whole native guard FAIL/F2/F3/fullappearance는 그대로다. DN0DTkeep 픽셀 감소는 PM의 consumer AB 관측이며 source-equivalent normal correction이 아니다. 새 source rendering/capture/export/build/download/product Unity 수정은 하지 않았다.

Concrete NOT-RUN proposal: `SOURCE_NORMAL_GAP_2INPUT_PROPOSAL_R1.json`에 source/inputs/executable/draft/helper hashes, argv template와 guard/resource contract를 고정했다. `r4_morph67_two_input_normal_collector_DRAFT_R1.py`는 **compile-only 검증**했으며 bpy를 import/execute하지 않았다. 이 draft 자체는 OS guard가 아니고 native 실행 준비 완료를 뜻하지 않는다.

- 새 owned private directory에 source byte-for-byte clone을 만들고 SHA 확인 후 `use_scripts=False`로 load한다. Master/clone save 금지. Original actions78/driver mute13/rig/geometry/material/texture 유지.
- 두 입력만 original native FACE16+GAZE2에 적용한다. Frame1/source unbound body/원래 Armature pose 유지. `SourceFrame`으로 timeline을 seek하지 않으며 전체 runtime pose reconstruction을 주장하지 않는다.
- Head만 **SHAPE_ONLY / SHAPE_GN / FULL_SOURCE** 3 stages에서 capture한다. Private clone RAM에서 head modifier enable flags만 바꾸고 restore한다. Per stage original-loop normal, position, evaluated custom attribute, topology/material/smooth/UV, native triangle corner/polygon, tangent/sign 및 matrix를 수집한다. All72 source Key readback은 runtime71 이름별 weight/100과 별도로 대조한다.
- Native process1, CPU threads2, external watchdog90s, Job memory4GiB, private output64MiB cap. 6stage+2OFF NPZ 최대8개와 작은 private receipt만. Render/export/GPU0. Source arrays는 비교 증거로만 사용한다.
- Finally FACE/gaze/modifier flags를 restore하고 full source-signature diff0, OFF head arrays exact, source/clone/input SHA exact를 요구한다. Exceptions는 quarantine/FAIL이며 기존 artifacts를 덮어쓰지 않는다.

Guard review boundary: 새 broker/approval packet을 별도로 고정하고 Root PM이 검토하기 전에는 launch하지 않는다. Owned handle/PID/creation FILETIME/image/hash/parent, private Job active limit1/KILL_ON_CLOSE, strict BEFORE+AFTER image query, signaled handle+exitcode+JobActive0 custody를 요구한다. 기존 QueryFullProcessImageName error5가 재발하면 FAIL/HOLD로 중지한다. Historical approval/exitFILETIME substitute/waiver/자동 retry는 금지한다. Draft의 approval+before receipt interface는 executable OS guard의 검증을 대신하지 않는다.

NEXT: Root PM이 작은 stage-based source-reference 획득이 필요한지와 **새 strict guard/broker review**를 먼저 판단한다. Consumer writer는 현 상태에서 기존 exact normal semantics와 static corner-domain 계약만 사용하며 source-equivalent 또는 final runtime PASS를 선언하지 않는다.

VISUAL_EVIDENCE: 새 render/이미지 없음. PM 보고 DN0DTkeep7,634 changed pixels vs tangent-only24, neutral2/0 및 baked vertex8.82um covariate는 consumer 진단 범위로만 유지한다. Normal authority/appearance acceptance로 승격하지 않는다. Immutable R4 SHA **a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa** 확인, 기존 source/actions/native guard FAIL 보존.

Cache-only 검증: `& 'C:/Program Files/Python313/python.exe' labs/yuri-performance-r1/scripts/r4_morph67_cached_normal_gap_r1.py`. Draft 파일은 compile만 한다. 기존 shader recipe5276592 또는 native sampler를 재실행하지 않는다.
