새 Windows 기능 없음 — 기존 source head 내부 lash의 BSDF operands와 실제 slot/domain reference만 공급했다.

DONE: `HEAD_LASH_EXACT_CACHED_OPERANDS_R1.json`에 Face_Lash_Pigment의 기존 private member 기준21개 exact socket pointers와 transparency/render flags를 기록했다. 실제 surface는 Principled BSDF→Material Output 한 연결이며 Normal/Tangent/CoatNormal 등 입력은 전부 unlinked다. Active node Roughness **0.47999998927116394**, IOR **1.5**, Specular IOR Level **0.33000001311302185**. Material viewport `roughness`/`specular_intensity`는 이 active BSDF socket과 다른 필드다. RGB/Metallic inventory는 반복하지 않았다.

Head 실제 owner는 `Armature/Character_Body_Head`, mesh `tripo_mesh_1d697050.001`, DATA-linked zero-based material slot **6**이다. Frozen raw polygon assignments와 기존 NPZ `polygon_material_slot` 전체가 동일하다. Slot6 domain은 **2,634 smooth polygons / 7,902 source corners / 1,410 unique source vertices**, flat polygons0. Polygon/corner IDs는 공개하지 않고 기존 배열 선택식과 SHA를 제공한다. Separate14lash meshes를 숨기는 것은 이 head 내부 slot6 domain을 숨기는 것과 다르다.

Alpha=1, ThinWall=false; Coat/Transmission/Subsurface/Sheen/Emission/Anisotropy/ThinFilm contributions는 weight/strength/thickness0이다. 정확한 coat/specular tint/roughness/normal/tangent socket 값은 기존 [private packet](https://drive.google.com/file/d/12F0Qz_U-c-8pzfNRvEnt9k6TgyGIhpEs/view?usp=drivesdk)의 JSON pointers를 사용한다. DITHERED/HASHED material flags만으로 actual translucency를 주장하지 않는다. BaseColor가 어두워도 dielectric specular는 nonzero이므로 highlight hypothesis는 남지만 원인으로 확정하지 않는다.

Normal/Tangent sockets가 unlinked이고 기본값이 zero-vector인 것은 실제 shading normal이 zero라는 뜻이 아니다. Source head는 `has_custom_normals=true`, CORNER/INT16_2D `custom_normal` 원본 배열 `attribute_19_value`와 전부 smooth인 slot6 polygons를 가진다. Exact original NPZ: `outputs/o1-source-fidelity-recovery-r1/data/Character_Body_Head_original_mesh.npz`, **1,655,757bytes**, SHA256 **1a48cf823cb6cf0c95c7eee6d4b7e7e8a952cbaadd50d1d9ad18d909be34f473**. Source R4 SHA256 **a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa**이며 source/NPZ absolute paths 및 raw BEFORE SHA는 JSON에 있다. 새로운 NPZ/packet/upload를 만들지 않았다.

FAILED-HOLD: 원본 whole guard FAIL과 F2/F3/fullappearance/PBR는 유지한다. 이 결과는 cached source operands이며 runtime shader output이나 samepose Blink~.962 source render가 아니다. 새로운 native sampling/export/mesh edit/Unity 제품 수정 없이 완료했다. 5276592 recipe를 재실행하지 않았다.

CAUSE: PM이 보고한 samepose AB에서 separate14lashes hide 및 ContinuousEyeSkin.black 후에도 bright boundary가 남는 현상은 아직 pixel owner+slot 판정이 필요하다. Internal headlash BSDF/normal/light 또는 다른 owner를 자료만으로 구분하지 못한다. Source 재질을 바꾸거나 hidden guide를 복원할 이유로 쓰지 않는다.

NEXT — Laptop sole writer의 검증3개:

1. 동일 pose/camera/light에서 slot-ID diagnostic으로 bright pixel이 실제 source polygon slot6인지 확인한다.
2. 실제 headslot6 materialID와 Roughness/IOR/SpecularIORLevel/Alpha/Coat/Normal binding을 exact private fields와 대조한다. Blender SpecularIORLevel을 Unity 임의 specular/smoothness 숫자와 직접 동일시하지 않는다.
3. 동일 slot6 source-corner smooth/custom-normal transport를 확인하고, geometry/camera/light 고정 진단의 specular-only/off 비교로 highlight 가설을 분리한다. 진단 결과를 canonical material 변경이나 외형 PASS로 승격하지 않는다.

VISUAL_EVIDENCE: 새 이미지/영상 없음. Bright-boundary AB는 PM 보고이며 Desktop에서 새로 관측하지 않았다. Source/fallback/immutable R4 및08caad7 보존. Missing runtime pixel owner, actual shader uniforms, evaluated samepose corner normals를 JSON에 명시했다.

검증 실행: `& 'C:/Program Files/Python313/python.exe' labs/yuri-performance-r1/scripts/r4_head_lash_cached_operands_r1.py`. Cached source SHA, private ZIP CRC/SHA, frozen NPZ SHA/bytes, raw/NPZ assignments, unlinked operands21개를 확인한다. 새 native process는 실행하지 않는다.
