# Upstream registry

기준일: 2026-09-16

외부 코드/Skill을 가져오기 전에 source, license, revision/tag/commit, Blender/Codex 호환성을 확인한다. 무조건 latest를 설치하지 않는다.

## Tier A — 우선 검토/사용

### OpenAI skill format / tooling
- https://github.com/openai/skills
- `skill-creator`, `skill-installer`, `migrate-to-codex` 참고

### Blender official MCP
- https://www.blender.org/lab/mcp-server/
- https://projects.blender.org/lab/blender_mcp
- Blender 5.1+ first-party MCP integration
- generated Python execution is not sandboxed

### Remotion Agent Skills
- https://github.com/remotion-dev/skills
- motion graphics, composition, render/preview 계열 영상 작업의 우선 upstream

## Tier B — Blender production 보강

### Motion state inspection
- https://github.com/affaan-m/ecc
- skill: `blender-motion-state-inspection`
- screenshot-only 판정 대신 Blender scene/armature/transform/frame state를 구조적으로 읽고 visual evidence와 함께 검증

예시:
```bash
npx skills add https://github.com/affaan-m/ecc --skill blender-motion-state-inspection
npx skills add remotion-dev/skills
```

## Tier C — 아이디어/패턴 참고, 자동 채택 금지

- https://github.com/qiuranke99/codex-skills
- https://github.com/RobLe3/cc-blender-skill
- https://github.com/arjun988/blender-skills

## Source video pattern

User reference video:
- https://youtu.be/lQJDbmJSo_s

참고할 운영 패턴:
- research → compact PRD/brief → fresh build context
- Skills로 작업법 재사용
- Blender MCP live inspection/correction + saved Python source
- screenshot/render QA + structured state QA
- long-running autonomous iteration with checkpoints

## Adoption rule

새 upstream을 추가할 때 `CHANGELOG.md`에 다음을 남긴다.
- source URL
- observed revision/tag/commit
- license
- why adopted
- exact files/ideas adopted
- local validation evidence
- rollback path
