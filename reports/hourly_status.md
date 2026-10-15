# VIDEO STUDIO R2 — 시간대별 제작 상태

시간은 ComfyUI 기록의 KST 시각과 실제 보고서 저장 시각을 사용했다. 시도/샷 수는 해당 시각까지의 누적치다. 중간 시점의 아직 생성·검수가 끝나지 않은 샷은 PASS/PARTIAL 집계에 넣지 않고 pending으로 표시했다.

| KST checkpoint | 누적 시도 / 고유 샷 | Avatar / Arcane 고유 샷 | 해당 시점 QA 상태 | 누적 최대 VRAM | 성공 예시 | 다음 작업 |
|---|---:|---:|---|---:|---|---|
| 10/15 22:46 | 13 / 12 | 8 / 4 | PASS 4 · PARTIAL 8 · FAIL 0 | 15,797 MiB | A07 sit_stand | batch02의 나머지 Avatar 표정·동작과 Arcane 동작 생성 |
| 10/15 23:46 | 33 / 32 | 22 / 10 | 첫 30개 검수 완료: PASS 14 · PARTIAL 16 · FAIL 0; 신규 2개 pending | 15,832 MiB | T02 cleric_recovery | batch03 생성 이어가기; 전체 프레임 디코드와 시각 검수 |
| 10/16 00:46 | 55 / 54 | 40 / 14 | 첫 30개 PASS 14 · PARTIAL 16 · FAIL 0; 추가 24개 pending | 15,854 MiB | T02 cleric_recovery | 남은 Arcane 6개 생성 후 30개 전체 최종 검수·연락 시트 제작 |
| 10/16 01:04 | 61 / 60 | 40 / 20 | 최종 PASS 31 · PARTIAL 29 · FAIL 0; 등록된 시도 MP4 61개 전부 디코드 PASS | 15,854 MiB | A34 polite_bow · T17 cleric_heal_cast | 모캡 입력 후보 4개에서 3D 포즈 추출·리타게팅을 후속 수행 |

## 실패 원인과 GPU/디스크

완전 실패 판정은 없었다. PARTIAL은 주로 손 흔들기/윙크처럼 작은 동작이 흐린 경우, 카메라가 점차 줌인해 발이 잘린 경우, 무기 발사·베기 표현이 충분히 읽히지 않는 경우에 해당한다. 반복 생성으로 PASS를 부풀리지 않았다.

LTX 생성은 GPU 직렬 실행했다. 샷별 metrics의 GPU 샘플에서 최대 15,854/16,376 MiB를 기록했고 OOM은 없었다. D: 여유 공간의 시간별 스냅샷은 실행 metrics에 기록되지 않았다. 최종 점검에서 2.74 TB 여유를 확인했다. ComfyUI가 대기 중에도 모델 VRAM을 유지해 종료 직전 유휴 상태에서 13,313 MiB 사용, GPU 이용률 2%로 표시됐다.

첫 12개 시점의 세부 표: first12_report.md. 전체 최종 집계: current_delivery.md 및 ../manifests/shot_index.json.
## 자가 검수 마감 — 2026-10-16 01:45 KST

선택적 재시도 11개까지 인덱스에 반영했다. 누적 72회 생성 시도·60개 고유 샷, 최종 선택 PASS 37 / PARTIAL 23 / FAIL 0. 이번 재시도 6개가 PASS로 개선됐고 A23은 표정 레퍼런스 PARTIAL, A01/T01/T03/T13 재시도는 원래 PARTIAL 버전을 유지했다. 전 시도 디코드 PASS, 누적 VRAM 최고 15,868 MiB. 마감 자원 확인: GPU 유휴 13,350/16,376 MiB, D: 여유 2.74 TB.
