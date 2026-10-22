# 숏츠 공장 — 로컬 실행 인수인계 R1

작성일: 2026-10-22 (KST)  
대상: Windows에서 작업하는 Codex / Claude Code / T3 Code의 로컬 실행 담당자  
목적: **딸깍 Threads Community v1.11.7을 실제로 실행하고, 기존 숏츠 공장 A/B/C에 쓸 부분을 증거로 판단한다.**

> 현재 완료된 것은 기획·소스 검토·이슈 등록이다. 딸깍 설치/실행, 숏츠 시제품, 자동 업로드, 수익 검증은 아직 완료되지 않았다. 이 문서를 받은 담당자는 기획 문서만 다시 쓰지 말고, 아래 로컬 시험을 실행하고 결과 화면과 산출물을 남긴다.

## 1. 첫 작업과 완료 목표

첫 작업은 새 서비스를 통째로 개발하는 것이 아니다. **별도 시험 폴더에서 앱을 켜고 → 수동 초안·승인·예약·모의 발행을 확인하고 → 카드 모션 MP4 한 개를 만들어 보는 것**이다.

| 단계 | 할 일 | 완료 증거 |
|---|---|---|
| G0 환경 | 작업 경로·Git·Node/npm·사용 포트·기존 세션 확인 | 환경 기록, 충돌하지 않는 시험 폴더 |
| G1 기동 | v1.11.7 고정, 설치·빌드, SQLite/이미지 모듈 검사, 서버 시작 | 커밋·버전, 로그, `/api/health`, 실제 화면 |
| G2 운영 | 테스트 초안 → 승인 → 예약 → DRY_RUN 완료 | 초안 ID, 상태 전환, 모의 발행 로그, 중복 여부 |
| G3 영상 | 자체 테스트 이미지로 카드 모션 MP4 한 개 | 실제 MP4, ffprobe, 대표 프레임, 재생 검수 |
| G4 인수인계 | 무엇을 재사용할지, A/B/C 다음 작업을 분리 | 실행 보고서, 한계·수정 내역·재시작 방법 |

G2/G3의 실패가 다른 독립 작업까지 막아서는 안 된다. 실패한 항목만 원인과 다음 조치를 남긴다. 전체를 PASS라고 뭉뚱그리지 않는다.

## 2. 사용자 결정 — 바꾸지 말아야 할 방향

**A/B/C 세 트랙을 모두 병렬로 준비한다.**

| 트랙 | 사용자 의도 | 첫 콘텐츠 목표 |
|---|---|---|
| A | 타인의 인기 롱폼을 실제로 잘라 숏츠 제작 | 후보 10개, 우선 원본의 컷 후보 5개, 사용할 수 있는 원본으로 20~45초 시제품 3개 |
| B | 인기 주제를 발굴해 자체 해설·영상 제작 | 주제 10개, 한 주제의 30~60초 대본 3종, 시제품 1개 |
| C | 자체 동화·애니메이션을 본편과 숏츠로 제작 | 신데렐라 한 장면의 밝은/잠자리 대본·스토리보드 각 45~60초, 파생 숏츠 2개 계획 |

숫자와 길이는 내부 파일럿 목표다. 세 트랙을 한 세션에서 모두 완성하라는 지시가 아니다. **이번 세션의 우선 결과는 G1~G3 실기동 증거**이며, A/B/C 조사·대본은 병렬로 준비할 수 있다.

A를 일방적으로 제외하거나 B로 바꾸지 않는다. 대신 연구용 참고 자료, 편집 가능한 원본, 공개 가능한 결과물을 구분한다. 원본 이용 근거가 부족하면 해당 영상의 공개만 보류하고 조사·템플릿 준비는 계속한다. 다운로드 성공이나 자막 추가가 재배포 권리 또는 YouTube 수익화 승인을 뜻하지 않는다.

C의 잠자리 버전은 밝은 버전의 배속·색상만 바꾸지 않고 낭독, 쉼, 이야기 전개를 다르게 설계한다. 일반 시청자용과 아동용의 브랜드·검수 기준은 분리한다. 기존 캐릭터/노래 참고 영상의 이용 권한은 별도로 확인한다.

## 3. 저장소·현재 지점·읽을 순서

### 우리 프로젝트

- 통합 저장소: https://github.com/zeroslove-ai/video-production-skills
- 작업 브랜치: `proposal/youtube-content-studio-r0-20261018`
- 설계 PR: https://github.com/zeroslove-ai/video-production-skills/pull/6
- 총괄 이슈: https://github.com/zeroslove-ai/video-production-skills/issues/7
- A/B/C 이슈: 같은 저장소의 `#8 / #9 / #10`
- 인수인계 작성 전 확인한 HEAD: `ed2442b202cc4355ae23d15df559e19ed07c49f6`
- PR은 **Draft / 미병합** 상태다. 이후 문서 커밋이 더해질 수 있으므로 시작할 때 최신 HEAD와 차이를 기록한다.
- 모션그래픽 전용: https://github.com/zeroslove-ai/video-motion-production-skills

먼저 다음 순서로 읽는다. 인수인계 이후의 사용자 지시가 있으면 그것을 우선한다.

1. 작업 폴더의 실제 `AGENTS.md` 및 해당 경로에 적용되는 규칙. 파일이 없는 경우 만들어 놓았다고 가정하지 않는다.
2. `docs/youtube-content-studio/PARALLEL_TRACKS_R1_KO.md`
3. `docs/youtube-content-studio/references/DDALKKAK_THREADS_V1_11_7_REVIEW_KO.md`
4. 이 문서와 저장소 `README.md`, `EXPERIMENT_LOG.md`
5. 모션 작업을 할 때만 별도 motion 저장소의 `AGENTS.md`, `README.md`, 실험 기록

R0의 “A 제외”와 일렬 우선순위는 R1에서 대체됐다. 오래된 R0를 현재 결정으로 복원하지 않는다. 두 영상 저장소는 합치지 않는다.

### 이번에 실행할 외부 프로젝트

- 저장소: https://github.com/apache3563-bit/ddalkkak-threads-community
- 지정 릴리스: https://github.com/apache3563-bit/ddalkkak-threads-community/releases/tag/v1.11.7
- 태그: `v1.11.7`
- 태그가 가리키는 커밋: `bef76fa476dac941a06e212fe306a075a3e2c864`
- 기술: Node.js / TypeScript / Express / SQLite / sharp
- `package.json`: Node.js `>=22.0.0`; 실제 스크립트는 `build`, `start`, `dev`
- 기본 UI: `http://localhost:3970`; 서버는 IPv4/IPv6 loopback에 바인딩
- 라이선스 표기: `AGPL-3.0`

최신 버전 자동 교체보다 위 버전으로 재현을 먼저 한다. 태그 커밋이 다르면 원인을 확인하고 변경을 기록한다. EXE 경로도 있지만, 이번 기본 경로는 설정과 오류를 추적하기 쉬운 **소스 실행**이다. EXE와 소스 서버를 같은 포트로 동시에 띄우지 않는다.

## 4. 이 도구가 하는 일 / 아직 없는 일

딸깍은 소재 수집, Claude Code 기반 글 생성, 초안 검토, 승인, 예약, Threads 발행을 관리하는 앱이다. 설치만으로 YouTube 롱폼 탐색·ASR·하이라이트 추출·YouTube 업로드가 완성되지는 않는다.

확인한 카드 영상 경로는 **렌더된 PNG 1~3장 → 확대/이동 효과 → 1080×1350, 30fps, 10/12/15초 무음 MP4**다. 이는 세로 4:5이며 우리가 목표로 하는 9:16과 다르다. 기본 렌더 검증 후 별도 9:16 어댑터를 검토한다. 출력 설정을 먼저 덮어써 원본 시험과 커스텀 시험을 섞지 않는다.

| 구분 | 역할 |
|---|---|
| 딸깍 평가본 | 소재·초안·승인·예약·발행 기록, 카드 모션 구현 참고 |
| video-production-skills | 전체 제작 계획·편집·합성·QA·결과 기록 |
| video-motion-production-skills | Remotion/SVG 기반 모션그래픽·자막·도형·2.5D |
| 기존 ComfyUI | 필요한 새로운 그림·짧은 생성 장면. 현재 설치·워크플로 상태는 로컬에서 재확인 |
| 추후 구현 | YouTube 인기 후보 탐색, 실제 롱폼 구간 분석, 플랫폼별 게시 어댑터 |

별도 앱으로 활용, 조건을 확인한 포크, 운영 방식만 참고한 자체 구현 중 무엇이 맞는지는 실기동 뒤 결정한다. 이번 작업에서 통합·대규모 재개발을 먼저 하지 않는다.

## 5. 이번 로컬 실행의 범위

**진행할 수 있는 일:** 별도 폴더에 clone, 기존 도구를 활용한 의존성 설치·빌드, 시험 폴더 내 작은 수정, localhost 서버 실행, 테스트 데이터 생성, 모의 발행, 로컬 카드 렌더, 로그·스크린샷·실행 보고서 작성.

**별도 확인할 일:** 실제 Threads/YouTube 게시, 계정·채널 생성, 유료 API/신규 구독, 외부 클라우드 배포, 공개 터널, 기존 프로젝트의 전역 설정 변경. 해당 일이 없어도 G1~G3 시험은 진행한다.

기존 ComfyUI/Unity/Blender/Node 프로세스를 일괄 종료하지 않는다. 전체 Node/npm 업그레이드나 `npm audit fix --force`로 시작하지 않는다. 전역 정책을 풀기보다 프로젝트 범위에서 문제를 해결한다.

기존 담당 세션이 있으면 먼저 재개한다. 공통 파일 writer는 하나로 두고, QA는 독립 읽기 전용으로 수행한다. 새 작업자를 실제 실행하지 않았다면 RUNNING으로 보고하지 않는다. 중간에는 완료한 결과와 장애를 짧게 보고한다.

## 6. Windows PowerShell — 소스 실행 절차

아래는 **실행 담당자가 로컬에서 수행할 명령**이다. 작성자가 사용자 PC에서 실행해 본 명령으로 오인하지 않는다. 블록을 순서대로 실행하며 실패한 명령을 무시하고 다음으로 넘어가지 않는다.

### 6.1 환경 확인과 새 폴더

기존 프로젝트 밖에서 새 PowerShell 창을 연다. 관리자 권한은 기본 전제가 아니다. `npm.cmd`를 사용해 `npm.ps1` 실행 정책 문제를 피한다.

```powershell
$ErrorActionPreference = 'Stop'
Get-Command git, node, npm.cmd -ErrorAction Stop | Select-Object Name, Source
& git --version
& node --version
& npm.cmd --version
$major = [int]((& node -p "process.versions.node.split('.')[0]").Trim())
if ($major -lt 22) { throw 'Node.js 22 이상이 필요합니다. 기존 전역 환경을 덮어쓰지 말고 별도 런타임을 검토하세요.' }

$Root = Join-Path $env:USERPROFILE ('Projects\shorts-factory-lab-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
if (Test-Path $Root) { throw "이미 있는 폴더입니다: $Root" }
New-Item -ItemType Directory -Path $Root | Out-Null
$App = Join-Path $Root 'ddalkkak-v1.11.7'
$Evidence = Join-Path $Root 'evidence'
New-Item -ItemType Directory -Path $Evidence | Out-Null
$Root | Set-Content (Join-Path $Evidence 'workspace.txt') -Encoding UTF8

& git clone --depth 1 --single-branch --branch v1.11.7 `
  https://github.com/apache3563-bit/ddalkkak-threads-community.git $App
if ($LASTEXITCODE -ne 0) { throw 'clone 실패' }
Set-Location $App
$Head = (& git rev-parse HEAD).Trim()
if ($Head -ne 'bef76fa476dac941a06e212fe306a075a3e2c864') {
  throw "검토한 커밋과 다릅니다: $Head"
}
& git switch -c local/shorts-eval
if ($LASTEXITCODE -ne 0) { throw '시험 브랜치 생성 실패' }
$Head | Set-Content (Join-Path $Evidence 'upstream-commit.txt') -Encoding UTF8
```

`$Root`는 이번에 새로 만드는 예시 작업 경로다. 기존 설치 위치를 찾았다고 주장하지 않는다. 담당자는 자신의 실제 경로를 보고서에 남긴다. 원격 `origin`은 외부 제작자 저장소이므로 그곳에 push하지 않는다.

### 6.2 사용할 포트와 격리 설정

포트가 사용 중이면 다른 프로세스를 종료하지 않고 다음 비어 있는 포트를 고른다. 선택한 포트를 이후 브라우저/API 검사에도 동일하게 사용한다.

```powershell
$Port = 3970
while (Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue) {
  $Port++
  if ($Port -gt 3980) { throw '3970~3980 사용 중. 별도 포트를 확인하세요.' }
}
$Port | Set-Content (Join-Path $Evidence 'port.txt') -Encoding ASCII
if (Test-Path '.env') { throw '예상하지 못한 .env가 있습니다. 내용을 로그로 출력하지 말고 확인하세요.' }

@"
PORT=$Port
TZ=Asia/Seoul
DRY_RUN=true
DISABLE_SCHEDULER=true
DOCS_MODE=false
DAILY_MAX_PUBLISH=1
DB_PATH=./data/local-eval.db
LOG_DIR=./logs/local-eval
UPLOAD_DIR=./data/local-eval-uploads
THREADS_ACCESS_TOKEN=
THREADS_USER_ID=
THREADS_MEDIA_GATEWAY_PORT=
THREADS_MEDIA_PUBLIC_BASE_URL=
THREADS_MEDIA_RELAY_BASE_URL=
THREADS_OAUTH_RELAY_URL=
THREADS_RELAY_CLIENT_KEY=
"@ | Set-Content '.env' -Encoding ASCII

# 이 PowerShell 프로세스가 기존 환경변수를 상속했을 수 있으므로 안전 설정을 명시한다.
$env:PORT = [string]$Port
$env:TZ = 'Asia/Seoul'
$env:DRY_RUN = 'true'
$env:DISABLE_SCHEDULER = 'true'
$env:DOCS_MODE = 'false'
$env:DAILY_MAX_PUBLISH = '1'
$env:DB_PATH = './data/local-eval.db'
$env:LOG_DIR = './logs/local-eval'
$env:UPLOAD_DIR = './data/local-eval-uploads'
$BlankKeys = @('THREADS_ACCESS_TOKEN','THREADS_USER_ID','THREADS_MEDIA_GATEWAY_PORT',
  'THREADS_MEDIA_PUBLIC_BASE_URL','THREADS_MEDIA_RELAY_BASE_URL',
  'THREADS_OAUTH_RELAY_URL','THREADS_RELAY_CLIENT_KEY','CLAUDE_ARGS_PREFIX')
foreach ($key in $BlankKeys) { [Environment]::SetEnvironmentVariable($key, '', 'Process') }
New-Item -ItemType Directory -Force -Path '.\logs\local-eval', '.\data\local-eval-uploads' | Out-Null
```

첫 실행은 빈 시험 DB를 사용한다. 기존 DB를 복사하면 저장된 Threads 인증 정보가 서버 시작 때 복원될 수 있다. 환경변수만 비웠다고 기존 DB의 연결 정보까지 제거됐다고 생각하지 않는다. `DOCS_MODE=true`는 가상 연결 상태를 돌려주는 문서 촬영용 기능이므로 실제 성공 증거에 사용하지 않는다.

### 6.3 설치·빌드·네이티브 모듈 검사

설치 전에 `package.json`, lockfile, `install.bat`을 읽는다. 설치 스크립트가 실제로 사용한 방식대로 `--ignore-scripts`로 시작하되, 이것만으로 네이티브 모듈의 실행이 보장되지는 않는다.

```powershell
& npm.cmd ci --ignore-scripts
if ($LASTEXITCODE -ne 0) { throw '의존성 설치 실패. 오류를 기록하고 원인을 확인하세요.' }
& npm.cmd run build
if ($LASTEXITCODE -ne 0) { throw 'TypeScript 빌드 실패' }

# PowerShell 5.1에서도 인용부호 문제가 없도록 JavaScript는 파일로 실행한다.
$Smoke = Join-Path $Evidence 'runtime-smoke.cjs'
@'
const path = require('node:path');
const { createRequire } = require('node:module');
const req = createRequire(path.join(process.cwd(), 'package.json'));
(async () => {
  const DB = req('better-sqlite3');
  const db = new DB(':memory:');
  try { console.log('sqlite', db.prepare('select 1 as ok').get()); }
  finally { db.close(); }
  const png = await req('sharp')({create:{width:16,height:16,channels:3,background:'white'}})
    .png().toBuffer();
  console.log('sharp-ok', png.length);
  const c = req('./dist/env').config;
  const summary = {port:c.PORT,dryRun:c.DRY_RUN,schedulerDisabled:c.DISABLE_SCHEDULER,
    docsMode:c.DOCS_MODE,hasToken:!!c.THREADS_ACCESS_TOKEN,hasUser:!!c.THREADS_USER_ID};
  console.log(JSON.stringify(summary));
  if (!c.DRY_RUN || !c.DISABLE_SCHEDULER || c.DOCS_MODE ||
      c.THREADS_ACCESS_TOKEN || c.THREADS_USER_ID) {
    throw new Error('Unsafe initial test configuration');
  }
})().catch(e => { console.error(e.message); process.exit(1); });
'@ | Set-Content $Smoke -Encoding ASCII
& node $Smoke
if ($LASTEXITCODE -ne 0) { throw '모듈/설정 검사 실패. 아래 복구 지침을 확인하세요.' }
& npm.cmd start
```

`npm start`는 이 창에서 전경 실행한다. 창을 유지하고 다른 PowerShell/브라우저에서 검사한다. 실제 로그는 비밀을 가린 뒤 `evidence`에 보관한다. 시작 로그에서 `DRY_RUN = true`, 스케줄러 비활성, 선택한 주소를 확인한다.

**SQLite native binding 오류:** `--ignore-scripts` 때문에 네이티브 설치 단계가 생략됐는지 확인한다. 해당 패키지의 정확한 버전·install script·출처와 사용 중인 npm 정책을 먼저 읽고, 필요한 패키지에 한해서 재빌드한다. 검토 후의 예시는 다음과 같다.

```powershell
# 필요한 설치 스크립트를 검토한 뒤에만, 시험 폴더 안에서 실행
& npm.cmd rebuild better-sqlite3 --ignore-scripts=false --foreground-scripts
if ($LASTEXITCODE -ne 0) { throw '네이티브 모듈 재빌드 실패' }
```

npm 버전에 따라 개별 설치 스크립트 승인 절차가 추가로 필요할 수 있다. 전체 패키지 허용이나 전역 보안 설정 해제로 해결하지 않는다. Node ABI/사전 빌드 바이너리/빌드 도구 문제가 남으면 별도 런타임 또는 해당 모듈의 공식 설치 절차를 확인한다. sharp 실패 역시 실제 오류를 보고 처리한다. `npm ci`를 다시 돌리면 앞서 재빌드한 모듈이 교체될 수 있으므로 재검사한다.

### 6.4 실제 화면·상태 확인

다른 PowerShell 창에서 선택한 포트를 넣어 실행한다. 첫 창의 `$Port` 변수는 자동 공유되지 않는다.

```powershell
$Port = 3970  # evidence/port.txt에 기록한 실제 값으로 변경
$Base = "http://127.0.0.1:$Port"
Invoke-RestMethod "$Base/api/health"
Invoke-RestMethod "$Base/api/status"
Start-Process $Base
Get-NetTCPConnection -State Listen -LocalPort $Port |
  Select-Object LocalAddress, LocalPort, OwningProcess
```

`/api/health`의 `ok=true`만으로 G1 전체를 PASS 처리하지 않는다. 대시보드가 실제 렌더되는지, 버전이 맞는지, DB/정적 리소스/브라우저 오류가 없는지 함께 본다. 상태 응답 전체를 공개 저장소에 그대로 올리지 말고 민감한 값이 없는지 검사한다. localhost가 IPv6 문제로 실패하면 명시적인 `127.0.0.1` 주소로 확인한다. 정상 바인딩은 loopback이며, 메인 UI 포트를 공개 터널에 연결하지 않는다.

## 7. G2 — 모델·계정 없이 운영 흐름 시험

테스트 문구 예시: **“로컬 시험용 초안입니다. 외부에 게시하지 않습니다.”** 실제 고객 정보나 타인의 글을 넣지 않는다.

1. 화면의 직접 작성/수동 초안 경로로 테스트 초안 1개를 저장한다. 정확한 UI/요청 필드는 실행 화면과 `src/routes/drafts.ts`에서 확인한다. 존재하지 않는 API를 추측해 호출하지 않는다.
2. 초안의 내용 변경, 승인, 예약 화면 진입을 확인한다. 예약 시간은 서울 기준이며 최소 사전 예약 제한이 있으면 그 값을 따른다.
3. 스케줄러를 시험할 때만 서버를 `Ctrl+C`로 종료한다. `.env`와 서버를 시작할 PowerShell 양쪽에서 `DISABLE_SCHEDULER=false`로 변경한다. **DRY_RUN=true와 빈 자격정보는 그대로 둔다.**
4. 서버를 재시작하고 화면의 자동 발행을 켠다. 이 토글이 꺼져 있으면 모의 발행도 진행되지 않는다. 초안 1개를 가까운 미래로 예약한다.
5. 예약 시각 이후 스케줄러 확인에서 `dry_run_done`과 모의 발행 기록을 확인한다. README는 매분 점검한다고 설명하지만 실제 로그와 상태로 판정한다. 예정 시간보다 먼저 성공 처리하지 않는다.
6. 추가 점검 주기와 재시작 후 같은 초안이 다시 처리되는지 확인한다. 중복 기록/재발행 여부를 보고한다.
7. 시험이 끝나면 자동 발행을 끄고, `.env`와 PowerShell의 `DISABLE_SCHEDULER=true`로 복귀시킨다. 사용자에게 화면을 남길 때도 **DRY_RUN=true / 자동 발행 꺼짐**을 유지한다.

로컬 테스트 코드가 필요하면 실제 라우트/DB 함수의 시그니처를 읽고 가장 작은 시험용 스크립트를 만든다. 기존 데이터베이스에 직접 임의 INSERT를 하지 않는다. 시험용 생성물에는 `TEST`를 표시한다.

**Claude 글 생성은 별도 검사다.** `claude --version`은 설치 확인이지 로그인·생성 성공의 증거가 아니다. 기존 로그인된 CLI와 사용 조건을 확인한 경우에만 테스트 소재 1개로 최소 생성 1회를 시험하고 호출 횟수를 기록한다. 새 API 결제/구독은 만들지 않는다. CLI가 없거나 한도에 막혀도 수동 초안으로 G2를 계속한다. `DOCS_MODE`나 가짜 CLI로 실제 생성 PASS를 만들지 않는다.

## 8. G3 — 실제 카드 모션 영상 한 개

목적은 숏츠 전체 자동화 완료가 아니라 **이 앱의 실제 영상 출력과 한계를 확인하는 것**이다.

먼저 읽을 소스:
- `src/productRadar/motionPresets.ts`
- `src/productRadar/motionOrchestration.ts`
- `src/productRadar/ffmpegRuntime.ts`
- 실제 카드 생성·영상 렌더 라우트 및 입력 형식

자체 테스트 이미지 1~3장을 준비해 앱의 카드/캐러셀 경로에서 렌더한다. 상품 수집 확장 프로그램이나 외부 계정이 막히면, 확인한 함수·입력 계약을 이용한 최소 로컬 시험으로 분리한다. 단순히 다른 FFmpeg 명령으로 만든 영상을 “딸깍 렌더 PASS”로 바꾸어 보고하지 않는다.

FFmpeg/ffprobe 존재와 실제 탐색 경로를 확인한다. 앱이 번들 런타임을 요구하면 코드에 맞춰 해결하고, 시스템 전체 PATH나 다른 프로젝트의 바이너리를 덮어쓰지 않는다. 첫 출력은 원래 프리셋 그대로 시험한다.

완료 증거는 다음과 같다.
- 실제 MP4 파일, 입력 이미지 출처, 사용 프리셋, 실행 로그, 소요 시간
- ffprobe로 해상도·코덱·프레임률·길이·오디오 유무 확인
- 시작/중간/끝 및 전환 지점 프레임 확인, 실제 재생 검수
- 텍스트 깨짐, 검은 프레임, 구도 잘림, 움직임, 원치 않는 외부 호출 확인

기본 무음 출력에 소리가 없다는 사실은 결함이 아니라 기능 범위다. 음성·자막·9:16 합성은 별도 어댑터 실험으로 이름을 나누고, 원본 시험과 구분해 기록한다. 영상 한 개 성공을 하루 생산량이나 수익성의 증거로 해석하지 않는다.

## 9. 장애 대응 — 멈추지 말고 실패 범위를 좁힌다

| 관찰한 문제 | 먼저 할 조치 | 피할 조치 |
|---|---|---|
| Node <22 / 네이티브 바인딩 오류 | 버전·ABI·모듈 설치 로그 확인, 격리 런타임/선택 재빌드 | 전체 PC Node 환경 교체, 무차별 재설치 |
| npm 실행 정책 오류 | `npm.cmd` 사용 | 시스템 ExecutionPolicy 전체 해제 |
| 포트 사용 중 | 점유 프로세스 확인, 다른 시험 포트 선택 | 모든 node.exe 종료 |
| Claude 없음/로그인 오류/한도 | 수동 초안으로 UI/예약 시험 계속 | 새 유료 API로 몰래 전환, 무한 재시도 |
| 모의 발행이 진행되지 않음 | DRY_RUN, cron 비활성 여부, 자동 발행 토글, 승인·예약 시각 확인 | 문제 해결을 위해 DRY_RUN=false로 변경 |
| 이미지/영상 발행에 공개 URL 요구 | 로컬 렌더와 발행 시험을 분리 | 메인 대시보드 공개 터널 개방 |
| FFmpeg 또는 수집 도구 없음 | 영상 기능만 PARTIAL, 파일 탐색·입력 계약 확인 | 앱 전체가 쓸모없다고 결론 |
| `test.bat` / `npm test` 없음 | 태그 실제 파일과 scripts 확인, 작은 시험 스크립트 작성 | README의 미존재 테스트를 실행했다고 보고 |

서버 중지는 해당 전경 창에서 `Ctrl+C`가 기본이다. 강제 종료가 필요하면 방금 실행한 시험 프로세스의 경로·포트·PID를 확인하고 그 프로세스만 종료한다. 기존 DB·미디어는 삭제하지 않는다. 재현을 위해 새 시험 DB가 필요하면 기존 것을 보존하고 다른 이름을 사용한다.

## 10. 참고 영상과 기존 문서의 정확도

- Threads: https://www.threads.com/@auto_make_vid/post/Den_D5qErNf/media?hl=ko
  - 이전 세션에서 다운로드 실패. 실제 영상·음성 내용은 분석되지 않았다.
- Shorts: https://www.youtube.com/shorts/3HyqObwYn0c
  - 이전 기록은 외부 색인의 제목 식별 수준이며 원본 재생·청취 분석이 아니다.
- 두 영상은 로컬에서 정상 접근 가능할 때 장면·자막·소리·편집 구조를 확인한다. 접근 통제 우회 없이 분석하고, 원본을 공개 저장소에 올리지 않는다. 확보에 실패해도 앱 실행과 다른 트랙 준비는 계속한다.

**이전 정책 수치의 정정/격리:** R0에 적힌 “2027-02-01 수익화 기준 강화”는 이번에 확인한 공식 YPP 안내에서 뒷받침되지 않았다. 확정 정책이나 사업 계산의 입력으로 사용하지 않는다. 현재 공식 안내는 구독자 1,000명 + 최근 12개월 적격 공개 시청 4,000시간 또는 최근 90일 적격 Shorts 조회수 1,000만 회이며, 기타 심사가 필요하다. 또한 공개 Shorts 조회 집계 변경일은 공식 안내상 **2025-03-31**이다. 앞선 대화의 2026년 변경일 표기를 이어받지 않는다. 공개·수익 신청 시 공식 안내와 실제 계정 상태를 다시 확인한다.[S8][S9]

AGPL 표기를 상업 사용 금지로 단정하지 않는다. 반대로 코드를 비공개 상품에 자유롭게 합쳐도 된다고 가정하지 않는다. 별도 실행 평가와 수정본 배포·서비스 제공는 구분하고 도입 방식 확정 때 라이선스 조건을 검토한다. 이 앱의 라이선스와 영상·음악·캐릭터의 권리는 별도다.

## 11. 산출물·완료 보고 형식

이번 시험의 실제 폴더 아래에 다음을 남긴다. 비밀값·원본 DB·제3자 원본 영상은 공개 GitHub에 올리지 않는다.

```text
<실제 시험 루트>/
  ddalkkak-v1.11.7/          # 고정 버전의 별도 clone
  evidence/
    workspace.txt
    upstream-commit.txt
    port.txt
    environment.md
    startup-redacted.log
    workflow-test.md
    screenshots/
    card-motion-smoke.mp4   # 실제 성공했을 때만
    ffprobe.json            # 실제 출력이 있을 때만
    LOCAL_EXECUTION_REPORT_KO.md
```

보고서에는 다음을 포함한다.

```text
전체 판정: PASS / PARTIAL / FAIL
기준: G0 __ / G1 __ / G2 __ / G3 __ / G4 __
실행 PC·OS / Node·npm / source commit:
실제 작업 폴더 / 접속 URL / 재시작 명령:
서버 현재 상태: RUNNING(확인 시각) 또는 STOPPED
DRY_RUN / 스케줄러 / 자동 발행 / 실제 게시 건수:
Claude 실제 호출 수 / 다른 유료 호출 수:
수동 초안→예약→모의 처리 결과 및 ID:
MP4·스크린샷·로그 경로:
코드 변경 파일 / 이유 / diff / 복구 방법:
확인된 장애 / 시도한 해결 / 남은 항목:
재사용 권장 기능 / 별도 구현이 필요한 기능:
A/B/C 다음 작업 각 1개:
```

첫 시험의 기대값은 실제 게시 0건이다. 실행 상태는 보고 시점의 관찰값이지 이후에도 계속 실행된다는 보장이 아니다. 서버를 켜 둔 경우에는 화면 주소와 해당 프로세스만 중지하는 방법을 함께 남긴다.

가능하면 독립 QA가 화면·산출물·증거를 읽기 전용으로 확인한다. QA가 없으면 “작성자 자체 검수”라고 표시한다. 문서만 작성한 상태를 실기동 완료로 바꾸지 않는다. GitHub 보고가 필요하면 우리 저장소의 관련 이슈와 `EXPERIMENT_LOG.md`에 비밀을 제거한 결과를 남기고, 실제 코드 수정은 별도 작은 브랜치/PR로 제안한다. 기존 Draft PR과 main을 임의 병합하지 않는다.

## 12. 근거와 검증 범위

아래는 2026-10-22에 확인한 원출처다. `[S1]~[S7]`은 소스·문서 열람 근거이며 사용자 PC 실행 증거가 아니다.

- [S1] 태그의 커밋 확인: https://api.github.com/repos/apache3563-bit/ddalkkak-threads-community/git/tags/56a0287b6f2a17e048fb2ba9a6b26b2ee771eaea
- [S2] 설명서: https://github.com/apache3563-bit/ddalkkak-threads-community/blob/v1.11.7/README_KO.md
- [S3] 패키지·명령: https://github.com/apache3563-bit/ddalkkak-threads-community/blob/v1.11.7/package.json
- [S4] 설치 스크립트: https://github.com/apache3563-bit/ddalkkak-threads-community/blob/v1.11.7/install.bat
- [S5] 환경 설정: https://github.com/apache3563-bit/ddalkkak-threads-community/blob/v1.11.7/.env.example
- [S6] 실제 설정 로더: https://github.com/apache3563-bit/ddalkkak-threads-community/blob/v1.11.7/src/env.ts
- [S7] 서버·상태 확인·기동: https://github.com/apache3563-bit/ddalkkak-threads-community/blob/v1.11.7/src/server.ts
- [S8] YouTube YPP: https://support.google.com/youtube/answer/72851?hl=en
- [S9] Shorts 조회수 변경: https://support.google.com/youtube/answer/10059070?hl=en
- [S10] npm 설치 스크립트 정책: https://docs.npmjs.com/cli/v11/using-npm/config/
- [S11] 현재 사용자 결정: https://github.com/zeroslove-ai/video-production-skills/blob/ed2442b202cc4355ae23d15df559e19ed07c49f6/docs/youtube-content-studio/PARALLEL_TRACKS_R1_KO.md
- [S12] 이전 카드 모션 소스 검토: https://github.com/zeroslove-ai/video-production-skills/blob/ed2442b202cc4355ae23d15df559e19ed07c49f6/docs/youtube-content-studio/references/DDALKKAK_THREADS_V1_11_7_REVIEW_KO.md

**이 인수인계 문서의 명령은 소스 계약에 맞춰 작성했지만 Windows 실기동 검증은 아직 하지 않았다. 실제 성공/실패는 담당자가 남긴 결과로 갱신한다.**
