# Editorial language R1

2026-10-02 · 촬영 계획과 컷 의사결정 지침. 기술적 VSE/OTIO 계약은 [editorial pipeline](EDITORIAL_PIPELINE_R1.md)을 따른다. 길이는 calibration 전 시작 범위이며 실제 공급 clip/audio 이벤트가 우선한다.

## Coverage의 목적

| Shot | 전달 정보 | Yuri/stylized 적용 / 컷 사용 |
|---|---|---|
| Establishing | 공간·동선·관계 | wide에서 얼굴 감정 대신 목적지/인물 위치 읽기 |
| Master | 전체 scene의 acting continuity | dialogue fallback, prop/action 기준 |
| Medium | 몸 gesture와 관계 | cute laugh/phone/손; CU 전에 정보 확보 |
| Close-up | 감정 변화 | supplied smile/hesitation의 onset/hold 포함 |
| Extreme close-up | 눈/상징 detail | 짧은 강조, 앞뒤 context 필요 |
| Two shot | 거리/관계 변화 | 대화 끝 관계 회복/긴장 유지 비교 |
| OTS | interlocutor와 depth | 상대 shoulder는 foreground cue; face/eye 가리지 않기 |
| Insert | phone/message/prop 정보 | reaction의 원인, text readable duration 별도 |
| Reaction | listener의 subtext | speaker 음성 지속 중에도 listener로 cut 가능 |
| Cutaway | 주변 의미/시간/숨길 edit | 임의 continuity 수리로 남발하지 않음 |
| POV | character가 본 정보 | preceding gaze와 height/direction 일치; actor camera와 구별 |
| Reveal | 감춘 정보의 공개 | 움직임·occluder 해제·cut 중 하나를 동기로 선택 |
| Ending hold | 감정 정착/return-state | end pose 뒤 24–48f를 시작값으로 검토 |

모든 coverage를 매번 final edit에 사용할 필요는 없다. benchmark B는 다양한 coverage를 검사하기 위해 12 shot을 계획하지만 실제 dramatic scene은 beat 목적이 중복되는 cut을 줄일 수 있다.

## Continuity와 rhythm recipe

| Rule | 설계 / cheap 검증 | Artistic exception |
|---|---|---|
| 180 degree | A→B action axis와 camera side를 모든 shot에 저장 | neutral on-axis bridge/re-establish 또는 화면 안에서 crossing 공개 |
| Screen direction | actor/prop travel vector를 projected frame로 비교 | 새로운 geography를 보여준 뒤 방향 변경 |
| Eyeline match | looking shot→target/reverse의 gaze height/side 확인 | lens eye contact는 audience-address beat로 명시 |
| Matching action | 동일 event/clip sample을 cut 양쪽에 표시 | 시간 생략은 ellipsis note; trim으로 performance 재제작 금지 |
| Shot/reverse shot | A/B foreground·look 방향·크기 균형, same axis | 관계 power 변화는 asymmetry reference로 승인 |
| Reaction cut | listener response onset과 information reveal 순서 | surprise를 먼저 보일 때 narrative reason 기록 |
| J-cut | 다음 shot의 audio가 picture cut보다 먼저 시작 | 다음 공간/화자 정보 먼저 전달; 독립 audio placement |
| L-cut | 이전 shot audio가 다음 picture까지 계속 | 상대의 듣는 감정 유지; voice/facial sync 검사 |
| Pacing | beat의 information→response→settle 기간 측정 | comedy quick cut / melancholy long hold의 목적별 rule |
| Rhythm | camera motion과 cut 둘 다 동시에 강조하지 않기 | action peak cut은 subject silhouette/event 보존 |

같은 axis 한쪽에서 shot/reverse/eyeline coverage를 잡는 이유는 관객의 공간 모델을 유지하기 위해서다. 반응/insert는 대사 외의 의미를 전달한다. [StudioBinder axis](https://www.studiobinder.com/blog/what-is-the-180-degree-rule-film/), [coverage](https://www.studiobinder.com/blog/shot-reverse-shot-cutaways-coverage/). 위 수치/예외·캐릭터 적용은 이 repo의 설계 판단이다.

## Mode별 언어

- CHARACTER_SHORT: MS 상황→insert 원인→MCU/CU 반응→lens eye-contact→ending hold. 컷 수보다 한 감정 변화의 가독성을 우선. 눈 contact 전 다른 gaze target이 있었다는 정보가 필요하다.
- WEB_DRAMA: establishing/master→A/B medium/OTS→emotion CU/reaction→insert→two-shot ending. camera는 locked가 기본, semantic turn에서만 push 후보. J/L-cut은 speaker 교체보다 관계/반응 전달에 사용한다.
- GAME_CUTSCENE: geography→entrance→hero medium→dialogue/reaction→action→hero CU→gameplay. action axis와 destination/return camera anchor가 이어져야 한다. engine handback frame은 ending beauty frame과 동일 시점으로 매핑한다.

## Timing을 agent rule로 만드는 방법

cue sheet에 `information_visible`, `response_onset`, `expression_peak`, `settle`, `next_intent` frame을 upstream annotation/clip sample로 기록한다. phone insert는 글을 읽을 시간을, CU는 표정 변화를 읽을 시간을, game action은 contact/recovery 정보를 확보한다. 초기 eye-contact hold 24–48f, smile settle hold 12–24f, shy reaction 24–48f는 draft 범위이며 실제 performance와 voice가 우선한다. silence가 empty content라는 이유로 자동 삭제하지 않는다.

Cut candidate는 event frame 주변 여러 후보를 animatic로 비교하고 “무엇을 새로 알게 되는 컷인가”를 설명한다. adjacent framing/angle이 거의 같으면 jump-cut 후보로 경고한다. 두 컷 사이 frame의 동일성을 요구하는 action QA와 dramatic pacing QA는 별도로 기록한다. 관객 감정 효과는 cheap animatic art review로 검증한다.
