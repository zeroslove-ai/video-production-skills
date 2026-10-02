# Production modes and benchmark sequences R1

2026-10-02 · 설계 fixture, 실제 제작 아님. 24fps, 1280×720, square pixels, shot source origin1/edit origin0. Frame 표는 **edit 반개구간**이다. lens는 sensor36mm/HORIZONTAL 기준 시작값이고 height/angle/movement는 camera preset에 기록한다. 이전 CS01/WD01/GC01 fixture를 이번 SEQ_A/B/C로 대체했다.

## Mode별 계약

| Mode | 목표 / coverage | Camera / editorial / lighting / references |
|---|---|---|
| CHARACTER_SHORT | 5–30s, establish→medium→action→CU→reaction→eye-contact→end | eye-height portrait, slow motivated motion, smile settle hold; soft/window/cozy; cute/romantic/daily |
| WEB_DRAMA | 30s–수분, establish/master/two-shot/A-B medium/OTS/CU/reaction/insert/ending | same-axis matched gaze, locked dialogue; semantic-turn/J/L-cut; warm/cozy; dialogue/relationship/negative-space |
| GAME_CUTSCENE | geography→entrance→hero medium→dialogue/reaction→action→heroCU→gameplay | destination/axis/root policy, readable action, explicit return anchor; hero/rim; hero/action/silhouette |

완성된 character/environment/prop 및 compatible body/facial clip을 입력받는다. body/facial clip의 reference/binding/range를 별도로 pin하며 retarget/viseme/rig/animation 생성은 하지 않는다. feet/hand contact와 mouth/voice mismatch는 upstream 입력 QA다. GP proxy frame은 blocked asset을 숨기는 final 결과가 아니다.

## Stage A: script → beat → shooting intention

“Yuri가 침대에서 휴대폰을 본다. 메시지를 확인하고 작게 웃는다. 카메라를 바라본다.”를 action 목록으로만 쪼개지 않는다. Beat01 평범한 일상(공간/phone relation), Beat02 메시지 발견(정보), Beat03 감정 변화(반응 onset), Beat04 미소(peak/settle), Beat05 관객과 eye contact(대상 전환/ending hold)로 기록한다. supplied clip에서 이 event frame을 고른 뒤 shot/cut 길이를 결정한다.

## SEQ_A — CUTE_ROOM / 12s / 5 shots

Required assets: adult Yuri `CHAR_A`, finished `BODY_A_PHONE`와 compatible `FACE_A_PHONE`, `SET_ROOM_BED`, `PROP_PHONE`와 approved message display, eye/hand/head anchors. 288-frame/24fps inputs, root locked. reference pack `REF_SEQ_A_R1`은 draft; [soft portrait card](../references/cinematography/cute/REF_PORTRAIT_SOFT_01.md)의 composition 원리와 owned Yuri atlas를 적용한다. phone readable text 권한/문구는 upstream 입력.

| Shot / frames / seconds | Beat | Camera / lens / composition | Look / cut intent |
|---|---|---|---|
| SH010 / [0,48) / 2s | ordinary room/phone | room_candid_35 / 35mm / left-third, hands/bed 포함 | window_morning; 정보의 원인 관계 |
| SH020 / [48,96) / 2s | message discovery | INSERT85_LOCKED / 85mm / phone center | 동일 light; text readable hold |
| SH030 / [96,168) / 3s | smile reaction | cute_closeup_soft / 75mm / near-center eyes | eye/face gates; smile onset→peak |
| SH040 / [168,240) / 3s | emotion→lens gaze | romantic_push_in / 75mm / near-third→target | .03m/s push, fit 유지/settle |
| SH050 / [240,288) / 2s | eye-contact end | ending_hold / 75mm / centered | direct-camera gaze, final48f hold |

GP/storyboard 수작업 그림은 필수 아님: 공급 clip sample과 proxy layout/camera frame을 자동 캡처하고 eye/hand/axis/beat annotation을 얹는다. R2 첫 prototype은 start/mid/end panels+small animatic만으로 appeal/eye light/pacing을 비교한다.

## SEQ_B — DIALOGUE / 30s / 12 planned coverage shots

Required assets: `CHAR_A/CHAR_B`, `BODY_A_DIALOGUE/BODY_B_DIALOGUE`, `FACE_A_DIALOGUE/FACE_B_DIALOGUE` 각720f/24fps, `SET_CAFE`, `PROP_NOTE`, external `A_VOICE/B_VOICE` 48kHz wav+script/cue sheet. root locked. floorplan A=(-1,0,0), B=(1,0,0), axis worldX, camera side worldY<0; A screen-left/gaze-right, B screen-right/gaze-left. actor facing/eye targets는 upstream compatible clip와 anchor로 확인한다.

| Shot / edit frames / sec | Coverage / intent | Camera / lens / composition |
|---|---|---|
| SH010 / [0,48) / 2 | Establish | environment_establishing / 24 / geography |
| SH020 / [48,120) / 3 | Master | dialogue_master / 35 / whole acting space |
| SH030 / [120,168) / 2 | Two shot | dialogue_master / 35 / relationship spacing |
| SH040 / [168,240) / 3 | A medium | MS50_LOCKED / 50 / A left-third/hand-safe |
| SH050 / [240,312) / 3 | B medium | MS50_LOCKED / 50 / B right-third/listener |
| SH060 / [312,384) / 3 | OTS A | dialogue_ots_right / 65 / A left, B foreground |
| SH070 / [384,456) / 3 | OTS B | dialogue_ots_left / 65 / B right, A foreground |
| SH080 / [456,504) / 2 | A close-up | reaction_closeup / 80 / A left/decision |
| SH090 / [504,552) / 2 | B close-up | reaction_closeup / 80 / B right |
| SH100 / [552,600) / 2 | Listener reaction | reaction_medium / 60 / response hold |
| SH110 / [600,648) / 2 | Insert | INSERT85_LOCKED / 85 / note OPEN, hand clip required |
| SH120 / [648,720) / 3 | Ending two-shot | dialogue_master / 35 / relationship resolved |

warm_window_evening look을 통일한다. Synthetic cues A=[156,336), B=[336,492): A voice가 SH040 picture보다12f 앞서 시작하고(J-cut) B voice가 SH070 picture보다48f 앞서 시작한다. A voice는 SH060의 시작을 넘어24f 계속되어 L-cut placement도 검토 가능. supplied face/voice의 실제 sync는 별도 R2 gate. 12 coverage cuts는 검증용 계획이며 좋은 연출이 항상 많은 컷을 뜻하지 않는다. reference는 approved axis/OTS floorplan, A/B portrait look key, reaction timing card가 필요하다.

## SEQ_C — GAME_REVEAL / 18s / 8 shots

Required assets: `CHAR_A`, finished `BODY_A_GAME` authored-root clip 및 `FACE_A_GAME` 432f/24fps, `SET_GATE`, `PROP_BEACON`, warning voice/event cue (optional upstream), cinematic-start/gameplay-return anchor, target engine camera samples/unit/axis/FOV convention. reference `REF_SEQ_C_R1` draft, [symmetry/depth](../references/composition/symmetry/REF_ROOM_DEPTH_01.md)를 geography 원리로만 사용한다.

| Shot / frames / sec | Beat | Camera / lens / composition |
|---|---|---|
| SH010 / [0,48) / 2 | Environment reveal | environment_establishing / 24 / destination visible |
| SH020 / [48,108) / 2.5 | Entrance | character_entrance / 40 / travel into right-third |
| SH030 / [108,156) / 2 | Hero medium | hero_medium / 50 / centered silhouette |
| SH040 / [156,204) / 2 | Dialogue warning | dialogue_ots_right / 65 / source-of-warning target |
| SH050 / [204,252) / 2 | Reaction | reaction_medium / 60 / readable face+gesture |
| SH060 / [252,324) / 3 | Action beat | action_tracking / 35 / lead room/action lane |
| SH070 / [324,372) / 2 | Hero close-up | hero_closeup / 75 / short push→settle |
| SH080 / [372,432) / 2.5 | Gameplay transition | WS35_LOCKED / 35 / matched return anchor |

hero_rim look을 사용하며 beacon cue는 환경 이벤트다. clip root motion은 한 번만 평가해 이중 이동을 막는다. SH080은 linear benchmark timeline의 고정 camera placeholder이며 target camera blend는 R2 sidecar/rehearsal로 구현한다. frame431의 gameplay pose/orientation/camera/focus/exposure를 입력 조건으로 검증한다. skip 시 return-state는 engine 측 책임이다.

## Design vs runtime acceptance

`examples/previz/SEQ_*.sequence.json`와25 Shot manifests는 위 range/preset/asset intake를 formalize한다. zero hash/placeholder revision/draft review는 의도된 값이며 실재 asset이나 승인을 뜻하지 않는다. schema1.1.0은 composition, optional facial input, planned outputs, audio role/subtitle cues를 기록한다. `.blend` 자동 생성과 완전한 benchmark 제작은 R2다. PM은 beat/coverage/length, art reviewer는 appeal/look/edit rhythm, asset owner는 compatible clip/event/voice/anchor를 승인한다.
