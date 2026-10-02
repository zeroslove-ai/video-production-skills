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
| SEQ_A CUTE_ROOM | Yuri phone/message/smile/gaze clip frames | MS/insert/CU/push/hold, window_morning | 5-shot 12s emotion turn, hold 2s |
| SEQ_B DIALOGUE | A/B seated, compatible body/facial clips | axis floorplan, master/medium/OTS/CU, warm_window_evening | 12-shot 30s cue/pause sheet |
| SEQ_C GAME_REVEAL | entrance/action/hero finished clip frames | geography→hero→action→return, hero_rim | 8-shot 18s beat/gameplay return diagram |

Fixtures의 `REF_SEQ_A_R1`, `REF_SEQ_B_R1`, `REF_SEQ_C_R1`은 설계 placeholder이며 승인 reference pack이 아니다. 실제 R2 gate는 approved pack, 권한, upstream revision, approver가 채워져야 통과한다.

## Reference Card: 촬영 지식 추출

실제 관찰한 [3개 Reference Card](../references/README.md)를 소량 유지한다. 원본 영상 frame의 EXIF/lens/camera diagram을 얻지 못하면 estimated focal length, pose와 confidence를 명시하고 source로 확인한 사실처럼 적지 않는다. still에는 observed motion/duration 대신 not-observable와 proposed sequence timing을 각각 기록한다.

필수 card 내용: Reference ID/source/creator/permission, scene description/why it works, shot-size/lens-estimate/camera position-height-angle, character screen placement, foreground/midground/background/depth, light direction-softness-rim/eye-highlight, palette, movement/duration, narrative purpose/emotion, Blender reproduction와 Yuri adaptation. identity와 cinematography reference가 충돌하면 authoritative adult Yuri identity를 보존한다.

최소 taxonomy: cinematography(cute/romantic/dialogue/comedy/melancholy/action/hero), lighting(morning_window/afternoon_soft/sunset/cozy_room/night_blue/neon/dramatic_backlight), motion(static/push_in/pull_out/pan/truck/orbit/crane/handheld_sim), composition(centered/thirds/symmetry/negative_space/frame_within_frame/foreground_occlusion/silhouette). canonical card는 한 곳에 저장하고 tags로 검색한다.

재현은 사진을 복제하는 작업이 아니다. source의 foreground/depth/eye/contrast 관계를 proxy scene에서 비교하고 감정 목적에 맞춘 candidate를 만든다. exact pose/light를 알 수 없는 사진은 hypothesis로 표시하며 reference-only 이미지 파일을 conditioning에 자동 투입하지 않는다. 관찰→제안→calibration→approved golden-frame의 네 상태를 분리한다.
