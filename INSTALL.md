# Install / activate in Codex

## 1. Project-local skills — 우선 권장

대상 repo의 `.agents/skills`에 아래 3개 skill folder를 복사한다.

```text
.agents/skills/
  video-production-director/SKILL.md
  video-blender-production/SKILL.md
  video-production-qa/SKILL.md
```

source:

```text
skills/
```

R1에서는 symlink보다 실제 file copy를 권장한다. Codex를 재시작/재로드한 뒤 skill catalog에서 3개 이름이 실제로 발견되는지 확인한다.

## 2. User-global skills

여러 repo에서 공통 사용하려면 현재 공용 convention인 `~/.agents/skills/`에 같은 폴더를 복사한다.

설치 후 반드시 현재 Codex의 skill catalog에서 discovery를 확인한다.

## 3. Blender MCP

`mcp/blender/SETUP.md`를 따른다.

기준:
- Blender 5.1+
- official Blender Lab MCP extension
- official `projects.blender.org/lab/blender_mcp` source checkout
- reviewed tag/commit pin
- Codex stdio registration
- actual scene read/write/read/visual smoke test

## 4. Optional upstream skills

필요한 경우에만 추가한다.

```bash
npx skills add remotion-dev/skills
npx skills add https://github.com/affaan-m/ecc --skill blender-motion-state-inspection
```

설치 후 실제 설치 위치와 skill catalog를 확인한다. upstream을 vendoring할 경우 source revision/license를 `UPSTREAM.md`와 `CHANGELOG.md`에 기록한다.

## 5. First invocation

첫 실전 작업은 10~15초짜리 저위험 demo를 권장한다.

```text
$video-production-director
10초 16:9 Blender 테스트 영상을 만든다. 먼저 production brief를 고정하고,
Blender MCP는 scene inspect/correction에, 저장된 bpy script는 반복 가능한 scene construction에 사용한다.
최종 전에 $video-production-qa로 state + representative frames + output metadata를 검증한다.
```

## 6. Record learning

실행 후 `EXPERIMENT_LOG.md`에 환경, tool revision, 성공/실패, 수동개입, 개선점을 남긴다. Skill 수정은 실제 evidence가 생겼을 때 좁게 반영한다.
