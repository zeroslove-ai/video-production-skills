# Video Production Skills

Codex/ChatGPT 계열 에이전트에서 영상 제작 작업을 반복 가능하게 운영하기 위한 **Skill + MCP production stack**의 정본 저장소다.

Canonical repository: `zeroslove-ai/video-production-skills`

## Core pattern

1. Research first — 레퍼런스, 기술 제약, 에셋, 렌더 방식을 먼저 조사한다.
2. Production brief — 바로 제작하지 않고 shot/style/asset/quality gate를 짧은 brief로 고정한다.
3. Fresh build context — 조사 컨텍스트와 실제 제작 컨텍스트를 분리한다.
4. Hybrid Blender control — MCP는 live inspect/correction, 저장된 bpy Python은 반복 가능한 scene construction에 사용한다.
5. Inspect → mutate → verify — 수정 전에 구조 상태를 읽고, 수정 후 상태 + 렌더/스크린샷으로 검증한다.
6. Checkpoint + evidence — 장시간 작업은 blend/script/render/log를 단계별로 남긴다.
7. Post pipeline — 필요 시 Remotion/FFmpeg로 편집, 자막, 오디오, 최종 인코딩을 수행한다.

## Repository layout

- `skills/video-production-director/` — 전체 영상 제작 라우팅 및 gate 관리
- `skills/video-blender-production/` — Blender 제작 workflow
- `skills/video-production-qa/` — 구조 상태 + visual evidence 기반 QA
- `mcp/blender/SETUP.md` — Blender 5.1+ 공식 Lab MCP를 Codex에 연결하는 기준
- `INSTALL.md` — Codex skill 설치/활성화 절차
- `UPSTREAM.md` — 채택/검토할 외부 skill 및 MCP 출처
- `R1_CODEX_WORKSTATION_BRIEF.md` — 실제 workstation 검증 실행 지시서
- `CHANGELOG.md` — 변경 이력
- `EXPERIMENT_LOG.md` — 실제 제작 테스트 결과 누적

## Operating rules

- 외부 Skill을 무더기로 vendoring하지 않는다. source/version/license를 확인한 뒤 필요한 부분만 채택한다.
- live Blender scene의 writer는 한 번에 하나만 둔다.
- 반복 가능한 geometry/camera/material/animation 생성은 가능한 한 파일로 저장되는 Python source를 남긴다.
- screenshots만 보고 성공 처리하지 않는다. scene/object/transform/frame/render state를 먼저 검사한다.
- renderer/MCP 장애 시 기존 작업을 파괴하지 말고 마지막 checkpoint에서 복구한다.
- machine-local MCP 설정은 이 repo가 자동으로 변경하지 않는다. `mcp/blender/SETUP.md`의 pinned 절차를 사용한다.

## Status

R0 source extracted from the Project OS incubator on 2026-09-16.

Next gate: real Codex skill discovery + official Blender Lab MCP smoke test + first reproducible 10–15s demo.

Only after that gate passes should this stack be considered production-ready.
