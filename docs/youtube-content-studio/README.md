# YouTube Content Studio

## 현재 결정 — 2026-10-18

사용자가 선택한 세 트랙을 병렬 준비한다.

| 트랙 | 준비 대상 | 작업 이슈 |
|---|---|---|
| A | 타인 인기 롱폼의 실제 컷 편집 숏츠 | [#8](https://github.com/zeroslove-ai/video-production-skills/issues/8) |
| B | 인기 주제의 자체 해설·영상 숏츠 | [#9](https://github.com/zeroslove-ai/video-production-skills/issues/9) |
| C | 자체 동화·애니메이션의 밝은/잠자리 본편 및 숏츠 | [#10](https://github.com/zeroslove-ai/video-production-skills/issues/10) |

총괄: [#7](https://github.com/zeroslove-ai/video-production-skills/issues/7)
설계 변경: [PR #6](https://github.com/zeroslove-ai/video-production-skills/pull/6)

## 먼저 읽을 문서

- **[로컬 실행 인수인계 R1](LOCAL_HANDOFF_SHORTS_FACTORY_R1_KO.md)** (2026-10-22): Windows 소스 설치·설정·실기동, 수동 초안/모의 발행, 카드 MP4 검증, 장애 복구와 완료 보고. 로컬 실행 담당자의 시작 문서.
- [R1 병렬 준비 지시서](PARALLEL_TRACKS_R1_KO.md): 현재 사용자 선택, 각 트랙 첫 산출물, 공통 엔진, 비교 기준.
- [딸깍 v1.11.7 정적 검토](references/DDALKKAK_THREADS_V1_11_7_REVIEW_KO.md): 관리/발행 참고 기능과 카드 영상의 범위. 실제 설치·실행 완료 보고서는 아님.
- [지정 Shorts 스타일 후보](references/YOUTUBE_3HyqObwYn0c_STYLE_CANDIDATE_KO.md): 사용자 참고 링크와 확인 범위. 실제 영상 재생·청취 분석은 미완료.
- [지정 Threads 영상 확보·분석 기록](references/THREADS_Den_D5qErNf_REVIEW_KO.md): **다운로드 실패 / 영상 미검토**. 접근 장애와 검토 항목만 기록했으며 영상 내용 분석이 아니다.

## 이전 검토 기록

- [R0 전략](STRATEGY_R0_2026-10-18_KO.md)
- [R0 기술 설계](SHORTS_FACTORY_TECH_R0_KO.md)

R0의 트랙 우선순위와 A 전면 제외 제안은 R1로 대체한다. 공통 기술 아이디어는 참고하되 R1의 연구/편집/공개 구분을 적용한다.

2026-10-22 정정: R0의 '2027-02-01 YPP 기준 강화' 주장은 이번 공식 문서 확인으로 뒷받침되지 않았으므로 확정 정책이나 수익 계산 입력으로 사용하지 않는다. 이전 대화의 Shorts 조회 집계 변경일도 공식 안내의 2025-03-31과 구분해야 한다. 근거와 정정 범위는 로컬 실행 인수인계 10절에 기록했다.

## 실제 상태

- 문서와 작업 이슈 준비 완료. 2026-10-22에 로컬 실행 인수인계 추가.
- 이번 대화에서 작업 에이전트·GPU 렌더·유튜브 업로드를 실행하지 않음.
- 인수인계에 포함된 실행 명령은 소스 기준으로 작성했으며, 사용자 Windows PC에서 실제 설치·기동한 기록이 아니다.
- 제작·게시 단계가 실행되면 실제 로그와 산출물로 상태를 변경한다. 이슈 존재만으로 RUNNING/PASS 처리하지 않는다.
- main과 기존 동작 코드는 변경하지 않았으며, 별도 모션그래픽 저장소는 유지한다.
