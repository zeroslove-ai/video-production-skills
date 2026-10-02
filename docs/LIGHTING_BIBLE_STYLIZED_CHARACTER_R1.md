# Stylized character lighting bible R1

2026-10-02 · design, 렌더 검증 전. 목적은 Yuri/stylized female의 얼굴·눈·연기 가독성이다. 캐릭터 material, face rig, eye texture를 제작하거나 수정하지 않는다. 공급 asset의 toon/PBR/자체 catchlight 지원을 intake에 기록한다.

## 구성 요소와 실행 계약

각 preset은 key, fill, rim, background_light, environment, eye_catchlight, face_readability, skin_toon_readability, hair_rim, background_separation을 독립 필드로 가진다. energy는 key=1에 대한 **광원 에너지 비율**이며 픽셀 노출 비율이 아니다. 색 hex는 sRGB design swatch; bpy light RGB로 넘길 때 working-space 변환이 필요하다. 광원 크기는 subject height의 배수, 배치 azimuth는 subject forward 기준, elevation은 수평 위로 양수다. 절대 watts/distance는 set-scale calibration 후 pin한다.

| Preset ID | Key / fill / rim | Background / environment | 눈·얼굴·toon 판단 |
|---|---|---|---|
| soft_beauty_key | large frontal 20°/25°, 1/.55/.2 | 낮은 neutral BG, soft ambient | cute/lovely; 밝은 피부에 nose/cheek plane 유지 |
| window_morning | large window side 35°/30°, 1/.5/.25 | cool room BG, soft daylight | comfortable/playful; 양 눈 확인, 창쪽 catchlight |
| warm_window_evening | broad warm 40°/20°, 1/.35/.3 | muted violet BG, 낮은 warm ambient | romantic/shy; iris hue와 blush 보존 |
| cozy_room | lamp-motivated broad 25°/20°, 1/.45/.15 | warm practical BG, gentle ambient | comfortable; 얼굴에 orange cast 과다 금지 |
| sunset_rim | soft key 30°/15°, 1/.3/.7 | warm back horizon, cool fill | lovely/romantic; hair halo가 silhouette를 키우지 않게 |
| night_blue | soft neutral-cool 35°/25°, 1/.3/.35 | blue BG, 낮은 environment | lonely/mysterious; sclera/pupil 분리 유지 |
| neon_city | broad neutral face key 30°/25°, 1/.25/.5 | violet/cyan BG lights | confident/playful; neon을 eye hue 변경으로 처리하지 않음 |
| dramatic_backlight | subtle face key 45°/25°, 1/.2/.8 | motivated backlight, low ambient | mysterious/surprised; deliberate silhouette와 unreadable face 구별 |
| hero_rim | broad key 30°/30°, 1/.3/.7 | separated dark BG, warm rim | heroic/confident; hair/skin highlight clip 경고 |
| melancholy_side_light | soft side 60°/20°, 1/.25/.25 | cool quiet BG, low ambient | melancholy/lonely; shadow eye가 감정 의도를 충족하는지 |

기존 SOFT_DAY 등 generic look은 호환용으로 유지하고 위 10개 preset을 shot 목적별로 추가한다. 신규 ID를 참조하는 camera preset은 모두 실제 lighting preset ID로 resolve된다. Standard NPR baseline과 AgX PBR variant를 같은 이름으로 몰래 바꾸지 않는다. [Blender displays/views](https://docs.blender.org/manual/sr/5.0/render/color_management/displays_views.html).

## 독립 QA: eye catchlight

1. incoming eye capability: baked/live/hybrid/unknown 기록. baked는 `preserve_asset`; live는 asset interface와 key 방향이 확인된 경우만 사용한다.
2. 좌우 iris crop을 start/mid/end/head-turn/blink-event에서 비교한다. pupil 분리, catchlight 위치/크기, 복수 highlight, 프레임간 flicker를 별도 gate로 기록한다.
3. supplied blink/눈 감음은 event annotation으로 제외한다. 털/앞머리 occlusion은 character appeal 의도에 따라 승인 사례와 비교한다.
4. 눈 texture를 임의 밝게 하거나 새 표정을 만들지 않는다. material support 부족은 upstream 요청으로 반환한다.

## 독립 QA: face readability

face ROI의 눈썹/눈/코/입 edge와 silhouette를 approved neutral atlas에 대조한다. shadow side 정보 소실, skin/toon band collapse, hair rim clipping, background와 face hue 혼합을 경고한다. automatic score는 실패 후보 순위에만 사용하고 art 승인과 분리한다. score 기록에는 ROI, exposure/view transform, 참조 frame/hash, blink/occlusion 예외를 함께 보존한다.

Background separation은 rim만으로 해결하지 않는다: face와 BG의 value/hue contrast, depth layering, foreground occupancy를 함께 검토한다. 초기 rule은 silhouette 대부분이 배경에 읽히는지, 눈 앞 foreground가 없는지, rim edge가 의도한 폭인지이며 asset별 tolerance는 golden frames로 calibration한다.

## Golden look 검증 / R2

one finished Yuri asset + neutral/turn/smile facial clip을 입력받아 10 looks × 정면/three-quarter/profile의 저비용 still을 비교한다. 렌더 budget을 작게 단계화하고 처음에는 soft_beauty_key/window_morning/hero_rim 3개만 검증한다. 카메라/view transform과 reference revision을 고정하고 key/fill/rim/BG를 한 번에 하나씩 비교한다. 선택 결과를 Reference Card와 preset calibration revision에 저장한다. 이번 R1에는 이미지·blend·실측 light 값이 없다.
