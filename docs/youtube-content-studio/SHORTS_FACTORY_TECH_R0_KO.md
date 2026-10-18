# Shorts Factory — R0 기술 설계 / 첫 구현 지시서
작성: 2026-10-18 KST | Status: SPEC ONLY (실행/검증 없음)
관련 전략: STRATEGY_R0_2026-10-18_KO.md

## A. 범위
목표는 허가받은 롱폼 원본으로 9:16 Shorts 3개를 **재현 가능한 방식으로 만드는 것**이다. 외부 바이럴 영상 검색은 '제작 주제 탐색'을 위한 메타데이터 작업이다. 자동 다운로드, 무단 리업로드, 승인 없는 공개를 MVP에 넣지 않는다.

R0에서 절대 하지 말 것:
- 다른 영상 레포(main)의 기존 코드/의존성 대량 변경
- 기존 ComfyUI/Blender 구동 세션 침범, 별도 승인 없는 유료 생성 API 사용
- 제3자 원본 파일의 무단 다운로드/자막 추출
- 비공개 테스트 없이 실제 채널 공개 및 계정·토큰 기록

## B. 시스템 분할
1. trend-scout (신규, 메타데이터만): 주제 검색/영상 기본정보/랭킹/출처 로그.
2. rights-ledger (신규, 필수): 원본 ID, 권리 종류, 증빙, 상업적/파생 권한, 승인자, 유효기간.
3. media-ingest (신규, 허가된 로컬 파일만): ffprobe로 형식 검증/파일 해시/길이/오디오 상태.
4. media-understand (신규): ASR/타임스탬프 + 장면전환/감정/핵심 발언 후보. 선택적 faster-whisper·PySceneDetect.
5. clip-planner (신규): 인트로-핵심-결말 구조를 갖춘 독립 쇼츠 후보, 출처 타임코드와 추가 제작 대본.
6. render-adapter (기존 재사용): FFmpeg 컷/리프레임/믹스, 별도 motion repo의 Remotion·SVG caption/2.5D composition 모듈; ComfyUI는 새 장면/배경을 필요한 경우에만.
7. QA + provenance (신규): 시각·음향·자막·사실·중복·권리·연령 분류를 검수하고 manifest/thumbnail/MP4/hash를 저장.
8. publish-gate (미연결): 승인 전에는 로컬 산출물 저장만. 추후 YouTube OAuth로 private 업로드 → 승인 → schedule. YouTube Data API의 publishAt, selfDeclaredMadeForKids, containsSyntheticMedia 등 확인.
9. analytics-loop (미연결): 우리가 운영하는 채널 Analytics 권한에서만 성과 취득. 타인의 retention/수익은 알 수 없음.

## C. 상태 머신
DISCOVERED → RESEARCHED → RIGHTS_PENDING → RIGHTS_CLEARED → INGESTED → TRANSCRIBED → PLANNED → RENDERED → QA_PASS → HUMAN_APPROVED → PRIVATE_UPLOADED → SCHEDULED → PUBLISHED → MEASURED

차단/실패 분기: RIGHTS_REJECTED, CONTEXT_FAIL, QA_FAIL, REWORK, EXPIRED.
- RESEARCHED 영상은 RIGHTS_CLEARED 전까지 INGESTED로 갈 수 없다.
- PUBLIC 업로드는 HUMAN_APPROVED와 채널 인증, 적절한 아동용/AI 공개 플래그 확인 없이는 불가능.
- '자체 제작 영상'도 상업적 이용이 불가능한 음원/외부 에셋이 포함됐으면 RIGHTS_PENDING.

## D. 최소 manifest 필드
~~~yaml
candidate_id: video-001
workflow: OWN_SHORTS # or LICENSED_CREATOR_SHORTS / ORIGINAL_TREND_EXPLAINER
source:
  reference_url: null
  original_filename: example-owned-longform.mp4
  sha256: null
  source_owner: OUR_CHANNEL
rights:
  class: OWNED
  commercial_use: true
  derivative_shorts: true
  music_cleared: null
  evidence_uri: null
  reviewer: null
  checked_at: null
research:
  topic: example
  reason: original source smoke test
  external_references: []
clip:
  start_sec: null
  end_sec: null
  original_context_summary: null
  transformed_narrative: null
  destination_duration_sec: null
  caption_language: ko
  aspect_ratio: "9:16"
  target_resolution: "1080x1920"
  edits: []
publishing:
  channel_class: GENERAL
  made_for_kids: null
  synthetic_media_disclosure: null
  human_approval: false
  youtube_video_id: null
qa:
  rights: NOT_TESTED
  caption_accuracy: NOT_TESTED
  video_audio: NOT_TESTED
  context_and_facts: NOT_TESTED
  output_sha256: null
status: RIGHTS_PENDING
~~~
※ 이 예시는 자료 구조 설명용이다. 실제 원본/승인/해시가 확보되지 않았으므로 테스트 파일인 것처럼 표시하지 않는다.

## E. Viral Discovery R0 점수 실험
- 탐색 입력: topic, country/lang, publish window, duration, intended audience.
- 후보 필드: video_id, title, channel_id, publishedAt, publicViewCount, duration, retrieved_at.
- 파생: 공개 데이터로 계산한 (조회수 / 경과 시간), 채널 최근 공개 영상 대비 상대 조회수(데이터가 충분할 때만), 주제 관련성/서사 재창작 가치.
- 동영상 조회수는 검색 API 정렬 및 색인 특성에 따라 표본 편향이 있다. viewVelocity는 예측 지표가 아니라 후보 정렬용 휴리스틱이다.
- 1차 선정은 20개 참고 영상의 주제를 관찰하는 방식으로 제한하며, 제3자 영상 파일을 저장하지 않는다.
- 재조회 주기/데이터 보존기간/사용량은 공식 API 개발자 약관을 준수하여 별도 확정한다.

## F. Own-source → Shorts 품질 체크
1. 원본 파일 권리·ffprobe 분석 PASS.
2. 타임스탬프 기반 3개 다른 하이라이트. 단순 중복/미완성 문맥 금지.
3. 자체 가치: 필요하면 새 내레이션, 설명, 순서 재배치, 직접 생성한 그래픽.
4. 세로 리프레임 1080x1920 목표, 얼굴/주요 피사체 크롭 방지, 모바일 UI 안전 영역 확인.
5. 자막: 한국어 문장 자연스러움/동기화/한 줄 길이/이름 일관성 직접 검수.
6. 오디오: clipping/무음/음량 급변/라이선스 미확인 음악 없음.
7. 숏츠별 원본 타임코드와 편집 diff 기록. 렌더 MP4·원본·manifest SHA-256 저장.
8. 아동용 시 폭력·공포·빛 번쩍임·음량·오인 연출 추가 QA.
9. 공개 전 썸네일, 제목/설명, 제작자 정보, Made for Kids, AI 공개 요건 개별 확인.
10. 오류 발생 시 문제 장면만 다시 렌더. 전체 길이 재생성 최소화.

## G. 추천 구현 순서 / 병렬화 경계
P0 (1명 writer): README/AGENTS/EXPERIMENT_LOG 재확인. 워크스테이션 환경·ComfyUI/MCP/FFmpeg·오디오 툴 **읽기 전용 조사**. 실제 준비 여부 검증. 설치/업데이트 무단 진행 금지.
P1 (독립 worker A): trend-scout 메타데이터 로직 + 20개 후보 샘플. 타인 영상 파일 취득 금지.
P1 (독립 worker B): rights-ledger + import gate + 샘플 테스트, PUBLIC_DOMAIN/OWNED/LICENSED 등 권리 상태 검증.
P1 (독립 worker C): 실제 소유/허락된 fixture 1편 기준 ASR + 장면분석 + 컷 후보 3개; 변경·렌더는 소유 자산만.
P2 (1명 writer): Remotion/FFmpeg 템플릿 연동; 3개 후보 → MP4, caption, manifest, storyboard.
P2 (독립 read-only QA): file/hash/provenance/rights/context/audio/9:16 별도 검수. 코드 수정은 writer만.
P3: 명시적 채널 승인 뒤 OAuth 및 private 업로드 스모크. 공개 자동화는 별도 승인/검증 후.

## H. 검수 판정
- G0 (연결 점검): 현재 워크스테이션, 기존 두 레포/ComfyUI/렌더 산출 경로 확인 = READ-ONLY PASS 여부.
- G1 (데이터): 20개 참조 후보/출처/조회 시각 + 1개 자체/허가 원본 통과. 미검증 타인 원본 ingest 0건.
- G2 (제작): 같은 원본 1개에서 차별화된 숏츠 3개, 정확한 시점과 9:16 MP4/자막/편집 manifest 재현 가능.
- G3 (품질): 권리·자막·오디오·문맥·표시검수 PASS, 실패하면 해당 원인 및 재렌더 비용 기재.
- G4 (게시): 사용자 채널 연결 및 공개 승인 전에는 **미실행**; 승인돼도 private 스모크 선행.
- 실험 후에는 기존 EXPERIMENT_LOG에 증거와 PASS/PARTIAL/FAIL, 변경된 컴포넌트, 사용 리소스를 기록한다.

## I. 도입 후보 (검증/선택 전)
- YouTube Data API: 영상 메타데이터 검색/통계, OAuth 업로드(타 콘텐츠 자동 다운로드에 쓰지 않음).
- FFmpeg/ffprobe: 고정밀 컷/리프레임/음량·미디어 메타데이터/인코딩.
- PySceneDetect: 샷 전환 탐지 — https://www.scenedetect.com/docs/latest/
- faster-whisper or equivalent local ASR: 본인 소유 원본 오디오 타임코드 추출(실제 가용성 검증 전).
- Remotion/@remotion/captions: 영상 자막 및 템플릿 — https://www.remotion.dev/docs/captions/
- ComfyUI + 기존 로컬 비디오 생성: 숏츠의 부족한 시각 장면을 자체 생성(기존 컴퓨팅 비용 측정 후).
- OpusClip: 상용 제품의 편집 UX·캡션·리프레이밍 벤치마크만, 수익성 사례로 해석 금지 — https://www.opus.pro/

## J. 외부 근거
- https://support.google.com/youtube/answer/1311392
- https://support.google.com/youtube/answer/12843009
- https://support.google.com/youtube/answer/14328491
- https://developers.google.com/youtube/terms/developer-policies
- https://developers.google.com/youtube/v3/docs/search/list
- https://developers.google.com/youtube/v3/docs/videos/insert
