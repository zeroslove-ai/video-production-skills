# Dots exact baseline custody comparison — 2026-10-05

두 기존 Dots baseline을 Aside의 반환 첨부에서 다운로드했다. chat 입력/새 Dots task 변경은 없었다. 각 4개 part는 별도 manifest 순서대로만 결합했다. 8 part SHA/bytes, 2 ZIP SHA/bytes/CRC, 2 recovered native SHA/bytes 모두 독립 검증 PASS. 원본·control·R2 파일은 read-only이며 비교 전후 bytes가 동일하다.

| 파일 | Bytes | SHA256 |
|---|---:|---|
| Dots pristine master | 30045689 | 16440ac619b43f2a9cbc5d0f6660ba1341e08961126d50e19c43493ccf5a646b |
| Dots MUG control | 30207907 | 40fa19e9f276fdc5c6dc08e9e75bda6da90b578a1320443468eb423f580d5374 |
| Existing R2 default OFF | 31630511 | 67fd96b796ea510644c7c65549f410d4e277f04db91b1c57c991b430245904dc |

master는 103 objects/108 Actions, control은 110/111, R2는 110/112다. master→control은 MUG helper 7개와 미연결 study Action 3개를 추가한다. 기존 객체·rig·rest·geometry·weights·ShapeKeys·Action·material·node group·OFF geometry hash는 보존된다. Scene 기록과 image filepath/filepath_raw 6개는 다르다. image packed bytes/colorspace/다른 속성은 동일하며 이 작업에서 경로를 수정하지 않았다.

control→R2 기존 데이터 보존 PASS: 기존 Action 111개 curves, 48 mesh object의 base coordinates/topology/attributes/weights/material slots, 원래 ShapeKeys, rig/rest/bind/constraints/drivers, materials/nodes/textures, scene/cameras, OFF evaluated world geometry가 동일하다. 추가 객체/삭제 객체/삭제 Action은 0개다.

R2는 shared body mesh에 **Basis + MUG_ThumbVolume_VolumeRedistribution_R2_OFF**를 추가한다. Body와 QA inspection 두 객체가 그 mesh를 사용한다. 새 Basis coordinates는 control mesh coordinates와 정확히 같다. body 객체의 유일한 직렬화 속성 차이는 active_shape_key가 null→Basis인 점이다. 전체 ShapeKey 목록은 동일하지 않으므로 whole-asset identical/canonical promotion으로 판정하면 안 된다.

보정 key default=0, Action binding 없음, driver=0. 저장된 nonzero delta는 **164 vertices**, 최대 object-world delta 1.3999989 mm다. upstream authored-support 165와 effective nonzero 164의 차이 원인은 미확정이다. 수정하거나 새 corrective를 만들지 않았다. 별도 **MUG_CORRECTIVE_R2_Envelope_Unassigned_OFF**는 169 keys/0..1, nonzero frames 53..134이며 미연결이다. ON playback/contact acceptance는 이번 범위에 없다.

두 sequential CPU read-only native 작업은 각각 fixed600sec/4GiB/2CPU/64MiB strict live barrier와 terminal/drain PASS다. 두 번째는 첫 비교에서 발견한 body 객체/image 차이 필드만 확인했다. Blender save/render/export, GPU/GUI/Unity/Laptop 변경은 0회다. Pixel render parity는 새로 검사하지 않았다.

**Default OFF / TierP=0 / contact quality HOLD**를 유지한다. Dots pristine master도 canonical immutable R4 `a30fc513…`와 별개의 derived source다. 이 결과가 user의 animation-only R4 acceptance 또는 외형 승격을 대체하지 않는다. 기존 `08caad7`, appearance corrective `820a237`, 이전 custody UNKNOWN checkpoint `5432cc4`는 보존했다. 이전 UNKNOWN은 당시 baseline 부재에 대한 기록이며, 이번 exact comparison receipt가 baseline availability/original-domain parity만 갱신한다.

공개 파일은 scalar QA와 재현 script뿐이다. 다운로드/native 파일/ZIP/geometry arrays는 Git에 넣지 않았다. 실제 paths/SHA/guards/diff 목록은 `DOTS_EXACT_BASELINE_CUSTODY_SCALAR_R1.json`에 있다. 다음 품질 실험은 별도 승인된 범위에서만 수행하며 이번 custody 결과는 접촉 품질 승인이 아니다.
