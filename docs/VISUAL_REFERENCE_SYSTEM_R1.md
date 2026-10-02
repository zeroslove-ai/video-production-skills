# Visual reference system R1

상태: 설계, 2026-10-02. canonical character identity는 incoming asset owner가 제공한다. reference는 이를 대체하는 새 캐릭터 생성 지시가 아니다.

## Reference pack

pack 유형: `identity`, `cinematography`, `lighting_color`, `set_prop`, `editorial_rhythm`. identity는 upstream의 character turnaround/승인 render와 hash. cinematography는 lens/shot-size/angle/composition 예시, lighting은 mood/palette/eye atlas, editorial은 cut/beat timing 예시를 제공한다. 각 shot은 pack ID/revision과 해당 panel ID를 pin한다.

R2 reference index 필드: `reference_id`, `pack_id`, `revision`, `role`, `source_url_or_uri`, `creator`, `license_or_permission`, `usage_scope`, `content_sha256`, `crop_region`, `timecode_or_frame_range`, `asset_revision`, `positive_rules`, `negative_rules`, `approved_by`, `approved_at`, `status`, `supersedes`. status는 draft/approved/rejected/expired. source URL만으로 license나 permission을 추정하지 않는다. 연구용 링크와 production conditioning에 넣을 이미지의 usage_scope를 구분한다. 미확인 권한은 research-only이며 proof layer 입력으로 자동 승격하지 않는다.

pack directory 제안: `index.json`, `identity/`, `camera/`, `look/`, `edit/`, `contact_sheets/`, `decisions.json`. 내용이 바뀌면 revision/hash를 변경하고 affected shot을 stale로 표시. URI는 project root 기준 상대 경로나 approved external resource, local machine의 개인 경로를 공유 manifest에 넣지 않는다. 캐시만 바뀌면 provenance를 덮어쓰지 않는다.

## 검색 → agent 적용

1. brief의 beat intention과 mode로 필요한 reference role을 정한다.
2. 공식 기술 문서 / incoming owned asset / 이용 범위가 확인된 visual sample을 분리하여 기록한다.
3. positive 2개, negative 1개로 선택 이유를 설명한다. 인터넷 이미지 한 장의 style을 전체 캐릭터 정본으로 사용하지 않는다.
4. art reviewer가 기준 panel을 승인한 뒤 measurable rule로 옮긴다.
5. agent는 candidate framing/look과 panel의 차이를 보고한다. identity/reference 충돌 시 identity를 우선하고 art review를 요청한다.

| 사람이 선택할 요소 | agent에게 전달할 규칙 | 증거 / 실패 처리 |
|---|---|---|
| 얼굴 silhouette | yaw/pitch allowed range, hair visibility panel | face atlas와 start/mid/end 비교 |
| 감정과 시선 | beat intention, gaze target ID, hold frames | supplied clip sample; mismatch upstream 요청 |
| 조명과 눈 | mood preset, baked/live catchlight policy | eye crop + unclipped RGB reference |
| framing | composition target, allowed intentional crop | normalized landmark overlay |
| 편집 리듬 | dialogue cue와 pause min/max, reveal frame | waveform/beat timeline + animatic review |
| 특수 예외 | exact shot/frame/rule + reason + approver | narrow override; global preset 변경 금지 |

룰은 score 하나로 합격 판정을 하지 않는다. agent가 예외를 추천할 수 있지만 approved pack과 모순되는 새 미적 기준은 draft로 기록한다. 자동 분석이 불가능한 그림/표정은 reviewer description을 남기며 false precision을 피한다.

## 세 기준 sequence의 reference 요구

| Sequence | identity | camera/look | edit |
|---|---|---|---|
| CS01 | A neutral/turn/greeting asset frames | MS→MCU→CU, SOFT_DAY | 3-shot 12s emotion turn, hold 2s |
| WD01 | A/B seated, talk/listen finished clip frames | axis floorplan, OTS/reverse, WARM_CONFESSION | 6-shot 30s cue/pause sheet |
| GC01 | A walk/stop/look supplied clip frames | geography→reveal→reaction→return, HERO_RIM | 6-shot 24s beat/gameplay return diagram |

Fixtures의 `REF_CS01_R1`, `REF_WD01_R1`, `REF_GC01_R1`은 설계 placeholder이며 승인 reference pack이 아니다. 실제 R2 gate는 approved pack, 권한, upstream revision, approver가 채워져야 통과한다.
