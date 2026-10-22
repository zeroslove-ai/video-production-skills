# 딸깍 Threads 공장 Community v1.11.7 — 숏츠 공장 적용 검토

검토일: 2026-10-21
상태: STATIC_REVIEW_COMPLETED / RUNTIME_NOT_TESTED / ADOPTION_PROPOSED
연결: PR #6, 총괄 #7, A #8, B #9, C #10

## 1. 결론

사용자가 제공한 릴리스는 Windows 로컬 Threads 콘텐츠 제작·예약 발행 프로그램이다. 공개 소스와 설치 파일이 실제 존재한다. 우리 숏츠 공장에서는 **자료→초안→검토→승인→예약→발행→기록이라는 운영 구조와 Threads 배포 연결의 참고 후보**로 가치가 있다.

그러나 이것을 설치하면 인기 유튜브 롱폼 탐색→음성 인식→핵심 구간 추출→9:16 편집→유튜브 업로드가 완성되는 것은 아니다. 확인한 영상 생성 경로는 상품 카드/캐러셀 PNG를 짧은 무음 MP4 또는 GIF로 만드는 기능이다. 음성·캐릭터 연기·스토리 애니메이션 생성기를 대체하지 않는다.

A(타인 롱폼 클립), B(인기 주제 자체 해설), C(자체 동화·애니메이션) 병렬 준비를 유지한다. 새 콘텐츠 트랙을 강제하거나 기존 영상 저장소를 이 프로그램으로 교체하지 않는다.

## 2. 고정한 검토 대상

- 저장소: https://github.com/apache3563-bit/ddalkkak-threads-community
- 사용자 지정 릴리스: https://github.com/apache3563-bit/ddalkkak-threads-community/releases/tag/v1.11.7
- 태그 조회 SHA: `bef76fa476dac941a06e212fe306a075a3e2c864`
- 릴리스 공개일: 2026-09-08 (GitHub published_at: 2026-09-08T13:35:19Z)
- 릴리스 명칭: Ddalkkak Threads 공장 Community v1.11.7
- Windows 설치 파일: `DdalkkakThreadsFactory_Community_Setup_1.11.7.exe`
- 파일 크기: 113,652,939 bytes (릴리스 메타데이터)
- 게시된 SHA-256: `4a55aadf81a1cde0f9b0e60952c81de53a864e9d85c4ff306c3708aea8f972fc`
- 라이선스 표기: AGPL-3.0

위 해시는 릴리스가 제공한 값이다. 설치 파일을 다운로드하여 직접 해시를 대조하거나 바이너리 보안을 검증했다는 뜻이 아니다. 최신 버전 전체 조사가 아니라 사용자가 보낸 v1.11.7을 고정해 검토했다.

## 3. 확인한 기능과 우리에게 남은 작업

| 항목 | v1.11.7에서 확인한 범위 | 우리 시스템에 대한 판단 |
|---|---|---|
| 자료 수집 | README의 RSS, URL, 직접 입력 텍스트, 키워드 | 주제 자료함 참고 가능. 유튜브 인기 탐색과 영상 파일 수집은 별도 |
| 글 생성 | Claude Code CLI를 호출해 구조화된 Threads 글 초안 생성 | 자체 해설 트랙의 주제·문구 생성 참고. 영상 대본·장면·음성 계약은 별도 |
| 페르소나 | 채널 정체성, 독자층, 말투, 금지 표현 등을 공통 프롬프트에 반영 | 일반/아동 채널의 스타일 관리 참고 |
| 검토·승인·예약 | README에 수동 승인, 예약, 자동 발행 토글, DRY_RUN, 발행 기록 명시 | 세 트랙 공통 관리 화면의 참고 후보 |
| 게시 | Meta 공식 Threads API 중심 | YouTube 업로더를 대신하지 않음 |
| 카드 영상 | 상품 카드/캐러셀 1~3장 PNG → MP4/GIF | 카드형 짧은 영상에는 유용. 롱폼 자동 편집과 다름 |
| 저장 | Node.js/TypeScript/Express, SQLite, 로컬 미디어 폴더 | 별도 앱으로 검증하거나 운영 구조만 참고 가능 |

검토는 README·파일 트리와 지정 코드의 정적 열람이다. 파일이 존재한다는 사실을 실제 실행 성공, 자동화 수익, 영상 품질의 증거로 보지 않는다.

## 4. 영상 기능에서 코드로 확인한 구체값

`src/productRadar/motionPresets.ts`:
- MP4: 1080×1350, 30fps, 1/2/3장일 때 총 10/12/15초.
- GIF: 720×900, 12fps, 총 4/6/8초.
- 프리셋: `smooth` / `slide` / `punch` (줌·이동 연출).
- 기본 MP4 비율은 4:5다. 우리 1080×1920 9:16 목표와 다르므로 해상도와 화면 구성을 별도 수정해야 한다. 4:5라는 이유만으로 플랫폼 업로드가 불가능하다는 주장은 하지 않는다.

`src/productRadar/motionOrchestration.ts`:
- 입력은 이미 렌더된 로컬 card/carousel PNG다.
- 임의의 롱폼 MP4를 받아 하이라이트를 추출하는 경로가 아니다.
- 동일 source/output의 렌더 결과 재사용, 세 프리셋 일괄 처리, 실패 시 결과 상태 관리가 구현돼 있다.

`src/productRadar/ffmpegRuntime.ts`:
- MP4 검증 함수는 H.264 영상 스트림 1개와 오디오 스트림 0개를 요구한다.
- 따라서 이 생성 경로에 내레이션/노래/효과음이 이미 통합됐다고 설명하면 안 된다. 외부에서 만든 영상 파일 첨부 기능과는 구분한다.

재사용할 만한 핵심은 '이미지에 줌을 넣는 것'만이 아니라, 입력 출처·작업 ID·재생성 방지·실제 파일 형식 검증까지 관리하는 방식이다.

## 5. 권장 결합 구조 (제안, 미구현)

공통 소재/콘텐츠 관리
→ A 롱폼 구간 편집 / B 자체 해설 / C 자체 동화 제작
→ 현재 영상 스택의 자막·음성·ComfyUI/모션그래픽·FFmpeg
→ 완성 MP4 + 제목/설명 + 썸네일 + 출처/권리 기록
→ 플랫폼별 발행 모듈
   - YouTube: 별도 OAuth/업로드/예약 구현
   - Threads: 이 프로젝트의 발행 방식 또는 별도 앱 연동 후보

우선은 딸깍 앱을 별도 평가 대상으로 두고, 기존 코드에 바로 복사·병합하지 않는다. 기능과 입출력 구조를 검증한 뒤 (1) 수정 없이 별도 사용, (2) AGPL 조건을 준수한 포크, (3) 설계 아이디어만 참고한 자체 구현 중 선택한다. 'API로 분리하면 언제나 라이선스 의무가 사라진다'고 가정하지 않는다.

트랙별 활용:
- A: 클립 목록·검수·예약 관리에 참고. ASR·타임코드·자동 컷/리프레이밍은 별도.
- B: RSS/URL 소재 수집, 말투 설정, 초안 생성은 가장 직접적으로 대응. 영상 대본화·내레이션·9:16 렌더는 별도.
- C: 동화 제작 엔진으로 보지 않고 완성본의 소개글·티저·발행 관리에 활용할 후보. 일반 콘텐츠와 아동 콘텐츠의 채널/검수 기준은 분리 유지.

## 6. 설치·계정·비용에 관한 실제 조건

- README상 Windows 10/11 대상, 소스 실행에는 Node.js 22 이상이 필요하다.
- 글 생성은 로그인된 Claude Code CLI를 사용한다. 앱이 무료라는 사실과 모델 사용량/구독 비용은 별개다. 이 사용자 PC의 설치·로그인·요금제·잔여 한도는 이번 검토에서 조회하지 않았다.
- Community는 제작사의 공용 Threads 중계 서버 설정을 제공하지 않는다. 자신의 Meta Developer 앱/Threads 인증이 필요하다.
- README는 이미지·영상 발행용 Cloudflare Workers/R2, OAuth용 Worker/KV의 self-host 구성을 안내한다. 공개 HTTPS 미디어 경로가 필요한 문제를 로컬 설치만으로 해결했다고 보면 안 된다.
- README 기준 Relay 없이도 직접 발급 토큰으로 텍스트 발행은 가능하다. 미디어용 HTTPS 터널 대안도 문서에 있다. 실제 구성을 선택하거나 배포하지 않았다.
- 로컬 앱이라는 뜻이 데이터가 외부로 절대 전송되지 않는다는 뜻은 아니다. Claude 생성 요청, Meta 게시 요청, 구성한 미디어 중계는 각각 별도 데이터 경로다.
- 초기 검증은 DRY_RUN 유지, 실제 발행 비활성 상태에서 진행하는 것을 제안한다. 이번 문서는 설치·계정 연결·클라우드 비용·게시 승인 자체가 아니다.

## 7. 라이선스 판단

AGPL-3.0은 상업적 사용 금지 라이선스가 아니다. 우리 업무에서 사용해 콘텐츠를 제작한다는 이유만으로 그 콘텐츠가 자동으로 AGPL이 되는 것도 아니다. 다만 출력 자체에 라이선스 적용 대상 프로그램의 보호되는 부분이 포함되는 경우 등은 별도 판단이 필요하며, 이미지·음원·원본 영상 권리는 각각 확인해야 한다.

프로그램 또는 수정본을 배포하거나, 수정본을 네트워크로 사용자에게 제공할 때는 해당 조건에 따른 소스 제공·고지 의무를 확인해야 한다. 따라서 '상업 사용 불가'로 배제하지도, 'MIT처럼 마음대로 비공개 제품에 합치면 된다'고 판단하지도 않는다. 외부 판매/서비스화 시 결합 방식과 의무 범위는 구체적으로 검토한다.

근거: AGPL v3 전문 §2, §4–6, §13 — https://opensource.org/license/agpl-3.0

## 8. 정적 검토에서 발견한 확인 필요 사항

1. README에는 아직 EXE 릴리스가 없다는 문구가 남아 있지만, 사용자가 보낸 릴리스에는 EXE와 SHA256SUMS가 실제 존재한다. 이 부분은 릴리스 메타데이터를 기준으로 삼는다.
2. README는 test.bat/통합 테스트를 안내하지만, 조회한 태그 파일 트리에는 test.bat가 없고 package.json의 scripts는 build/start/dev다. 테스트 재현 방법을 별도 확인해야 한다. 이것만으로 런타임이 실패한다고 단정하지 않는다.
3. Claude 상태 점검 함수의 --version 성공은 실행 파일의 존재·버전을 확인하는 것이며, 유효 로그인과 실제 생성 성공까지 증명하지 않는다. 상태/생성 스모크를 분리하는 것이 좋다.
4. 일부 파일을 읽은 결과이며 완전한 보안 감사·의존성 취약점 검사·악성코드 검사는 수행하지 않았다. EXE 안전 인증으로 사용하지 않는다.

## 9. 후속 검증 제안

다음 구현 담당자가 평가한다면 기존 ComfyUI/실행 세션과 분리된 평가 폴더에서 진행한다.

- 문서/설치 불일치와 의존성 빌드 경로 확인.
- 실제 계정 발행 없이 샘플 자료→초안 저장→승인→예약→DRY_RUN 로그 흐름 검증.
- 사용할 수 있는 테스트 이미지로 카드 MP4 1개 렌더 후 길이·비율·무음 여부 확인.
- 기존 9:16 영상 제작기와 콘텐츠 ID/완성 파일 경로/게시 메타데이터만 연결하는 시제품 설계.
- 사람이 수정한 시간, 생성 호출 수, 실패 복구, 중복 발행 방지, 재실행 결과를 기록.

위 항목은 실행 계획이며 수행 완료 목록이 아니다. 콘텐츠 3트랙 준비는 이 앱의 도입 여부와 독립적으로 유지한다.

## 10. 이번 실제 수행

- 수행: 지정 릴리스, 태그 파일 트리, README, package.json, Claude 초안 코드, 카드 모션 프리셋/배치/검증 코드 열람. 이 검토 문서 추가.
- 미수행: EXE 다운로드/설치/실행, 소스 빌드, 로그인/토큰 등록, 모델 호출, GPU 렌더, 실제 게시, 수익 검증.
- 기존 main, 두 영상 레포의 실행 코드, 로컬 사용자 환경은 변경하지 않았다.

## 원출처

- 릴리스: https://github.com/apache3563-bit/ddalkkak-threads-community/releases/tag/v1.11.7
- 설명서: https://github.com/apache3563-bit/ddalkkak-threads-community/blob/v1.11.7/README_KO.md
- 패키지: https://github.com/apache3563-bit/ddalkkak-threads-community/blob/v1.11.7/package.json
- 초안 생성: https://github.com/apache3563-bit/ddalkkak-threads-community/blob/v1.11.7/src/claude.ts
- 프리셋: https://github.com/apache3563-bit/ddalkkak-threads-community/blob/v1.11.7/src/productRadar/motionPresets.ts
- 영상 배치: https://github.com/apache3563-bit/ddalkkak-threads-community/blob/v1.11.7/src/productRadar/motionOrchestration.ts
- MP4 검증: https://github.com/apache3563-bit/ddalkkak-threads-community/blob/v1.11.7/src/productRadar/ffmpegRuntime.ts
- 라이선스: https://github.com/apache3563-bit/ddalkkak-threads-community/blob/v1.11.7/LICENSE
- AGPL 전문: https://opensource.org/license/agpl-3.0
