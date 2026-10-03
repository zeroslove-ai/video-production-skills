새 Windows 기능 없음 — 원본 visible eyelid BaseColor 재현용 최소 연결식과 기존 private 상수 필드 위치를 정리했다.

DONE: `VISIBLE_LID_MINIMAL_CONSUMER_RECIPE_R1.json`은 ContinuousEyeSkin.L/R 각각의 활성 BaseColor 15 edges, 2 Blink driver targets, neutral/closed 이미지 identity/SHA/color-space/sampler, POINT masks 및 rest-position 연결을 담는다. Cached-only script로 기존 private ZIP SHA/CRC와 양쪽 실제 graph links/연산/driver expression을 확인했다. 새 native 실행·export·NPZ·upload·Unity 변경은 없다. R4 source와 08caad7은 보존한다.

Recipe order (RGB, scene-linear; nominal factors 0..1):

1. Original head Key `FaceControls_TEST_Jaw_Smile.001`의 side-specific Blink에서 `b=min(1,blink*4)`, `d=b*0.60`을 계산한다. 원본에 없는 lower clamp를 추가하지 않는다.
2. Source UV → identity Mapping(TEXTURE) → neutral `N` / closed `D` textures. 두 이미지 모두 sRGB, FLAT/Linear/EXTEND이다. sRGB를 scene-linear로 decode한 후 색을 혼합한다. 상수 socket 색은 이미 scene-linear다.
3. `closed=mix(D,Cskin,p)`; `corrective=mix(N,closed,b)`. `p`는 원본 `R3_LidPigmentMask.side` POINT mask이다.
4. `t=clamp((restZ-a)/(c-a),0,1)`; `s=t³(6t²−15t+10)`; `m=ToMin+s(ToMax−ToMin)`. `neck=mix(corrective,Cneck,m)`. 원본 `neck_rest_position.Z`를 사용하며 움직이는 world-space Z로 대체하지 않는다.
5. `f=q*d`; `BaseColor_RGB=neck*(1+f*(Cwarm−1))`. `q`는 원본 `R3_AnatomicalFold.side` POINT mask이다. 최종 노드는 MULTIPLY MixRGB이며 output clamp=false이다. `mix(A,B,f)=(1−f)A+fB`는 nominal factor 범위의 식이다; 범위 밖 native behavior를 이 자료로 인증하지 않는다.

Unnumbered `Mix (Legacy)` branch는 활성 BaseColor가 아니다. Principled의 흰색 unlinked default를 최종 색으로 쓰지 않는다. Alpha/normal/roughness 전체 shader를 이 RGB recipe로 대체하지 않는다. Source corner/UV 및 POINT attribute interpolation을 유지해야 한다.

Private field authority: 기존 owner-only packet **319cc430201df5db3967c49e06de2d9e4bedc9e5b5400732ec961fc3374957e2**, member `LID_GUIDE_VISIBLE_PIGMENT_INPUTS_PRIVATE_R1.json`. JSON의 `constants`와 `dark_lash_uniform_pointers`는 이 member 기준 exact JSON pointers다. 기존 [private packet](https://drive.google.com/file/d/12F0Qz_U-c-8pzfNRvEnt9k6TgyGIhpEs/view?usp=drivesdk)을 재사용한다. 전체 numeric recipe를 새로 공개하거나 packet을 중복 upload하지 않는다.

Fixed-input algebra: Blink=0 → b=0,d=0 → `mix(N,Cneck,m)`; fold contribution=0. Blink=0.25 또는1 → b=1,d=0.60 → closed corrective가 포화된다. 이는 cached expression의 계산값이며 native node-tree evaluated witness가 아니다. 실제 UV/p/q/restZ 및 해당 fragment의 linear texture samples 없이 최종 RGB/pixel을 만들어내지 않는다.

FAILED-HOLD: Native whole guard FAIL, F2/F3 및 Windows fullappearance/PBR/closed-eye visual gates는 그대로 HOLD다. 원본 145-frame Object/Key sampling은 material node-tree output readback을 포함하지 않는다. 이 연결식은 geometry/pose PASS나 canonical appearance 승격 근거가 아니다.

CAUSE: 흰 경계가 visible lashes인지 eyelid skin인지 실제 renderer+slot 식별이 선행되어야 한다. Lashes면 기존 Face_Lash_Pigment / Face_LowerLash_Pigment의 dark BaseColor/Metallic/Roughness field pointers와 실제 uniforms를 비교한다. Eyelid면 linked texture/mask/Blink driver transport를 비교한다. Missing hidden LidMarginRefine는 이 visible shader를 대체하지 않는다; hide_render=true를 유지한다.

NEXT: 기존 Laptop writer가 같은 geometry/pose/frame/camera에서 visible boundary owner+slot을 기록하고 `N,D,p,q,restZ,b,d,neck,BaseColor_RGB`를 source field mapping과 비교한다. 원본 face shader driver와 skinning closure는 별도 증거로 판정한다. Desktop에는 새 native 실행 승인이 없다.

VISUAL_EVIDENCE: 새 render/screenshot은 없다. 기존 authoritative neutral PNG reference는 유지되며 closed-eye consumer artifact는 PM 보고 범위다. 이 checkpoint는 cached graph contract 검증만 완료했다.

Reproduce: repository root에서 `& 'C:/Program Files/Python313/python.exe' labs/yuri-performance-r1/scripts/r4_visible_lid_minimal_recipe_r1.py`. 실제 기존 private packet이 필요하다. 출력은 JSON 하나이며 native app을 호출하지 않는다.
