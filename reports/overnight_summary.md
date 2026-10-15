# VIDEO STUDIO R2 — 납품 및 자가 개선 결과

- 작업일: 2026-10-16 KST
- 로컬 결과 위치: D:\AI\LTX25-R3\output\video-studio-r2
- 모델: LTX 2.5 22B Distilled INT8; ComfyUI 0.34.6; PyTorch 2.10.0+cu130; 추가 LoRA/커스텀 노드 설치 없음
- 장치: RTX 4080 SUPER 16GB; 생성은 GPU 단일 작업 직렬 실행
- 고유 샷: 60 / 60 (Avatar A01–A40, Arcane T01–T20)
- 검수 등록 시도: 72 (원래 A05 두 번째 시도 1개와 이번 자가 개선 재시도 11개 포함; 샷당 최대 2개)
- 선택된 최종 영상: PASS 37 / PARTIAL 23 / FAIL 0; Avatar 24/16, Arcane 13/7
- 인덱스에 등록된 MP4 전 프레임 디코드 오류: 0
- 샷별 생성시간 합계: 183.1분; 최대 샘플 VRAM 15868 MiB, OOM 없음
- 모캡 입력 후보: 6개. 영상→3D 관절 추출과 Blender 리타게팅은 아직 수행하지 않음.

## 자가 품질 검수

기존 PARTIAL 중 수정 가능성이 높은 11개만 한 번씩 재생성했다. A04 balance recovery, A06 walk-stop, A11 surprise, A16 one-clap, A36 idol two-step, A37 walk-turn-stop은 동작이 더 분명해져 선택 결과가 PASS로 개선됐다. A23 wink는 표정이 더 잘 보이지만 점진 줌이 남아 PARTIAL로 유지했다.

A01 wave와 Arcane T01 saber slash, T03 archer release, T13 spear thrust는 수정 프롬프트에서도 요청 동작이 뚜렷하지 않아 재시도를 FAIL로 기록했다. 기존의 더 유용한 PARTIAL 버전을 최종 선택했다. 재시도 11개 모두 MP4 디코드 자체는 통과했다.

아바타는 정본 이미지의 얼굴·체형을 직접 편집하지 않고 회색 마커 슈트를 입힌 추적 프록시로 제작했다. 그 복장은 캐릭터 정본 의상이나 게임 적용 승인이 아니다. Arcane CHAR-002는 후보 참조로만 남기고, 일반 클래스 원형에도 로스터 승인을 부여하지 않았다.

## 산출물

- 전체 선택/시도 인덱스: manifests/shot_index.json
- 작은 연락 시트와 브라우저 인덱스: previews/contact_sheet.webp, previews/index.html
- 프롬프트, 재시도 검수, 선택 워크플로, 보고서: GitHub work/video-studio-r2 브랜치
- 각 시도의 MP4, 대표 프레임, 9프레임 검수판, 메트릭, 워크플로: 로컬 결과 위치의 avatar/ 및 arcane/ 아래에 보존
