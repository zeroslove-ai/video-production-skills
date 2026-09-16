# Blender MCP → Codex setup

기준일: 2026-09-16

## 권장 기준

Blender 5.1+의 공식 Blender Lab MCP add-on + 공식 `blender-mcp` stdio server 조합을 우선한다.

공식 안내:
- https://www.blender.org/lab/mcp-server/
- source: https://projects.blender.org/lab/blender_mcp

주의: Blender 공식 MCP는 LLM이 생성한 Python을 Blender 프로세스 안에서 실행하며 sandbox guard가 없다. 민감 데이터가 없는 별도 작업 환경 또는 VM을 권장한다.

## Architecture

```text
Codex
  │ MCP stdio
  ▼
official blender-mcp process
  │ local TCP (default localhost:9876)
  ▼
Blender 5.1+ Lab MCP add-on
  │
  ▼
bpy / scene / render
```

## Blender side

1. Blender 5.1+를 사용한다.
2. 공식 Blender Lab 페이지를 통해 MCP extension을 설치/활성화한다.
3. add-on preferences에서 MCP server/bridge를 시작한다.
4. endpoint는 localhost에 유지하고 외부 네트워크에 노출하지 않는다.

## Official MCP server source

동일한 `blender-mcp` 이름을 사용하는 별도 community package가 있으므로 `uvx blender-mcp`만 실행해 어느 구현인지 모호하게 만들지 않는다.

공식 source를 별도 폴더에 clone하고 확인된 tag/commit을 pin한다.

```bash
git clone https://projects.blender.org/lab/blender_mcp.git
git -C blender_mcp fetch --tags
# 설치 시점의 최신 공식 release/tag와 보안 수정 여부를 검토한 뒤 checkout
# git -C blender_mcp checkout <VERIFIED_TAG_OR_COMMIT>
```

`uv`가 있는 환경의 실행 형태:

```bash
uv --directory /ABSOLUTE/PATH/blender_mcp/mcp run blender-mcp
```

## Codex registration

CLI 예시:

```bash
codex mcp add blender -- \
  uv --directory /ABSOLUTE/PATH/blender_mcp/mcp run blender-mcp
codex mcp list
```

동등한 `~/.codex/config.toml` 예시:

```toml
[mcp_servers.blender]
command = "uv"
args = ["--directory", "/ABSOLUTE/PATH/blender_mcp/mcp", "run", "blender-mcp"]

[mcp_servers.blender.env]
BLENDER_MCP_HOST = "localhost"
BLENDER_MCP_PORT = "9876"
```

Windows에서는 실제 절대 경로를 사용한다. `uv`가 PATH에 없으면 실행 파일의 절대 경로를 사용한다.

`codex mcp list` 성공은 Codex에 server가 등록됐다는 뜻이지 Blender-side socket까지 정상이라는 증거는 아니다. 실제 scene read를 수행해 end-to-end 연결을 확인한다.

## Smoke test

1. Blender가 열려 있고 Lab MCP endpoint가 running인지 확인.
2. `codex mcp list`에서 Blender server 등록을 확인.
3. 실제 현재 scene/object의 read-only 상태를 조회.
4. test collection/object 하나를 만들고 즉시 상태 재조회.
5. viewport 또는 low-cost render evidence 생성.
6. test object 삭제 후 scene이 원상 복구됐는지 재조회.

read → bounded write → read → visual verify가 모두 통과해야 production에 사용한다.

## Do not

- 공식 Lab add-on과 protocol이 다른 community/legacy client를 이름만 같다고 섞지 않는다.
- `uvx blender-mcp`가 자동으로 Blender Lab 공식 구현이라고 가정하지 않는다.
- MCP가 등록됐다는 이유만으로 대규모 scene mutation을 바로 실행하지 않는다.
- workstation의 unrelated folders를 광범위하게 workspace로 노출하지 않는다.
- visual screenshot만으로 animation/transform correctness를 판정하지 않는다.
