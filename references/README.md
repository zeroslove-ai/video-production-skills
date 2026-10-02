# Visual reference knowledge, R1

Reference는 collection 수가 아닌 **촬영 판단을 다시 실행할 수 있는 card**로 관리한다.
아래 세 observed card는 공식 Nikon 자료의 소형 이미지를 직접 확인하고 작성했다.
이미지 파일은 repo에 vendoring하지 않는다. 권한 미확인이라 research-only이며 generation 입력으로 허용하지 않는다.
실제 focal length/camera pose/light placement의 EXIF나 set diagram이 없으므로 estimate와 observation을 분리한다.
still에는 관찰된 motion/duration이 없다. 적힌 motion/duration은 Blender adaptation 제안이다.

- [Portrait / soft smile](cinematography/cute/REF_PORTRAIT_SOFT_01.md)
- [Night / negative space](composition/negative_space/REF_NIGHT_SPACE_01.md)
- [Interior / symmetry depth](composition/symmetry/REF_ROOM_DEPTH_01.md)

Directory taxonomy (필요한 card만 만들며 빈 폴더를 대량 생성하지 않음):

```text
cinematography/{cute,romantic,dialogue,comedy,melancholy,action,hero}
lighting/{morning_window,afternoon_soft,sunset,cozy_room,night_blue,neon,dramatic_backlight}
camera_motion/{static,push_in,pull_out,pan,truck,orbit,crane,handheld_sim}
composition/{centered,thirds,symmetry,negative_space,frame_within_frame,foreground_occlusion,silhouette}
```

한 card는 canonical 위치 하나에 저장하고 tags로 여러 category에 검색된다.
positive/negative frame, asset revision, confidence, license, crop/timecode, reviewer approval와
reference hash를 [reference system](../docs/VISUAL_REFERENCE_SYSTEM_R1.md) 계약에 따라 기록한다.
observed source analysis와 Yuri용 proposed lens/lighting/action clip 선택을 섞지 않는다.
Benchmarks의 REF_SEQ_* pack은 아직 승인된 visual pack이 아니다.
