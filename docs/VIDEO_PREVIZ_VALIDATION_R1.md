# R1 design validation record

2026-10-02. Windows / Python 3.13.3 / jsonschema 4.26.0. 추가 dependency 설치 없음.
base revision `29f9431`. 브랜치 `research/previz-cinematography-r1`.

## 실제 수행

```powershell
python scripts/validate_previz_design.py
git diff --check
```

두 JSON Schema의 draft 2020-12 meta-schema 검사 통과. 로컬 fixture 결과:

```text
PASS CS01: 3 shots, 288 frames
PASS GC01: 6 shots, 576 frames
PASS WD01: 6 shots, 720 frames
DESIGN PASS: 3 sequences / 15 shots / 13 cameras / 5 looks / 15 templates
```

Schema/semantic checks: unique IDs, shot↔sequence source/rate/resolution/mode/reference 일치,
asset revision와 preset ID/revision, placements/subjects, compatible clip binding/root policy,
clip availability/handles, GP panel frame bounds, depth near<far, timeline coverage,
audio ranges/track overlap, event bounds. 모든 fixture JSON은 UTF-8로 parse된다.

In-memory negative probes (fixture 파일은 수정하지 않음):

- undeclared gap, source clip overrun, nonexistent camera subject, stale asset revision 거부.
- unapproved design fixture에 production flag를 적용했을 때 거부.
- schema의 unknown field와 duration 0 거부.
- explicit 12-frame gap과 24000/1001 fps로 변형한 동일 sequence의 semantic 검사 통과.

이 probe들은 현재 세 CS01 shot을 복사하여 해당 필드만 변형하고 validator를 호출한 one-off 검사다.
OTIO runtime round-trip를 수행했다는 의미가 아니다. 반복 가능한 baseline validator는 repo에 포함한다.

기존 `skills`와 `.agents/skills`의 세 SKILL.md 파일을 각각 비교했고 동일했다. 기존 tracked
source를 변경하지 않는다. 새 문서의 repo-relative 링크와 JSON 참조도 최종 commit 전에 확인한다.

## 하지 않은 검증

Blender binary/API compatibility, actual asset URI/hash/binding, rendered panels/animatic,
depth/mask/pose/camera pixel alignment, reference license/approval, audio sync, engine camera
import, OTIO adapter/editor round-trip, Comfy graph/model runtime. R1은 runtime 준비를 인증하지 않는다.

공식 자료의 조사 결과와 custom design을 문서에서 구분했다. 온라인 문서는 변할 수 있으므로
R2 구현 시 exact build, workflow/node/model revision, OCIO와 asset hashes를 다시 pin해야 한다.
스키마 `$id` URL은 안정적인 설계 식별자이며 해당 URL에 배포했다는 의미가 아니다.
