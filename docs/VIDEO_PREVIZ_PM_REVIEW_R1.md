# VIDEO_PREVIZ_CINEMATOGRAPHY_R1 — PM review

2026-10-02 · design checkpoint · base `29f9431` · branch `research/previz-cinematography-r1`.

## 전달 결과

제안된 5개 문서, Shot/Sequence JSON Schema 2개, preset library 3개를 추가했다. 검토 가능한 3개 sequence/15개 shot fixture와 offline design validator도 추가했다. 기존 README, production skill, `.agents` snapshot, workstation/MCP 설정은 수정하지 않았다. video provider 실행/결제/통합, model 다운로드, Blender render, character modelling/rigging/body/facial animation 구현은 수행하지 않았다.

| 산출물 | 검토 내용 |
|---|---|
| [Architecture](VIDEO_PREPRODUCTION_ARCHITECTURE_R1.md) | native Blender 조사, skill 소유권, storyboard 자동화, OTIO mapping, R2 backlog |
| [Cinematography bible](CINEMATOGRAPHY_BIBLE_STYLIZED_FEMALE_R1.md) | shot-size/lens/composition/motion, look/eye/mood, 예외 정책 |
| [Reference system](VISUAL_REFERENCE_SYSTEM_R1.md) | identity 권한·provenance·revision·approved panel 규칙 |
| [Mode blueprints](WEB_DRAMA_CUTSCENE_BLUEPRINT_R1.md) | CHARACTER_SHORT / WEB_DRAMA / GAME_CUTSCENE의 asset와 shot list |
| [Previz/Comfy handoff](COMFY_PREVIZ_HANDOFF_R1.md) | beauty/clay/depth/mask/pose/first/last/camera contract, local workflow 비교 |
| [Fixtures](../examples/previz/README.md) | 3 sequences / 15 shots, upstream placeholder 입력 |
| [Validation](VIDEO_PREVIZ_VALIDATION_R1.md) | 수행한 검사와 runtime 미검증 경계 |

## 기존 skill에 추가 / 별도 skill

director에는 mode 선택·reference/manifest freeze·preproduction gate를 추가한다. blender-production에는 manifest builder/export entry point와 read-back를 추가한다. QA에는 continuity·pass alignment·OTIO loss·character fidelity 검사를 추가한다. 공통 research/brief/checkpoint/single-writer/QA 흐름은 기존 내용을 재사용한다.

별도 `video-preproduction`, `video-visual-reference`를 제안한다. `video-editorial-interchange`는 초기에 preproduction reference module로 구현하고 반복 운영 필요가 확인되면 분리한다. Comfy는 optional adapter로 유지한다. INSTALL의 중앙 skill 정본 `zeroslove-ai/agent-skills` 정책을 먼저 따라 R2 변경 후 compatibility snapshots를 동기화한다.

## 자동화와 art judgment

자동화 가능: schema/ID/range/asset intake, camera 후보와 framing fit, scene/GP/VSE 구성, representative panels, proxy/cache, pass export index, camera/pose projection, OTIO straight-cut bridge, QA evidence pack.

Human artistic judgment 필요: emotional subtext, supplied performance 선택, 얼굴/눈에 맞는 각도, lighting/color key, cut rhythm, deliberate continuity break. 이를 agent에 전달하는 방법은 approved positive/negative panel, character angle/eye atlas, beat별 pause/hold range, measurable framing tolerance, 좁은 shot/frame 예외와 reviewer decision log다. 자동 미적 점수만으로 final 승인하지 않는다.

## 세 기준 sequence

| ID / mode | 길이 / shot list | 필요한 입력 |
|---|---|---|
| CS01 CHARACTER_SHORT | 12s / MS establish → MCU push → CU hold | A finished asset, 288-frame greeting/face clip, window set |
| WD01 WEB_DRAMA | 30s / master → OTS A → B reaction → note insert → A CU → two-shot | A/B finished assets, 각 720-frame synced talk/listen clip, café, note states, A/B voice cues |
| GC01 GAME_CUTSCENE | 24s / geography → tracking → orbit reveal → beacon insert → CU → gameplay return | A finished asset, 576-frame root-motion clip, gate/beacon, gameplay return anchor |

asset revision/hash/clip binding과 reference pack은 모두 placeholder. 실제 파일이 있는 것처럼 보고하지 않는다. shot별 frame/lens/preset/gate 목록은 blueprint와 fixture에 있다.

## 구현 우선순위 / PM 판단

1. P0: 기존 workstation gate 증거와 exact Blender/MCP pin → finished asset intake/semantic validation → CS01 idempotent builder/GP/VSE → cheap pass alignment proof.
2. P1: approved look/eye atlas → WD01 dialogue/coverage → OTIO round-trip와 target editor relink → GC01 engine convention/return-state proof.
3. P2: 이미 설치된 local weights가 있을 때만 optional single-shot Comfy A/B. 필수 경로에 추가하지 않는다.

PM은 skill 정본 정책, mode별 스토리/길이, incoming asset 담당자, reference art reviewer, P0 우선순위를 검토한다. **이번 checkpoint는 설계 검증 완료이며 실제 제작 준비 완료 판정은 아니다.** R2 runtime evidence가 남아 있다.
