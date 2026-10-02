# 유리룸 연기·프리비즈 병행 작업 지시

## 목표
영상 파일만 늘리지 말고 몸·손·얼굴·시선·호흡·카메라·소품 접촉을 분리한 연기 라이브러리를 만든다. 최종 목표는 자연스러운 애니메이션 주인공 같은 반응이며, 52개 키 존재만으로 완료 처리하지 않는다.

## 작업 순서
1. 현재 product/Avatar canonical 문서와 검증된 대상 아바타 해시를 확인한다. 기존 실행은 중지하지 않는다. proxy를 최종 아바타로 대체했다고 보고하지 않는다.
2. 이미 있는 UAL 클립/VRM retarget/AnimationMixer/접촉/손가락 프리셋을 읽고 재사용한다. 엔진 변경 금지.
3. 승인된 대상의 neutral, blink L/R, gaze, A/O를 정면·3/4·측면에서 검증한다. 눈꺼풀 접힘, 입꼬리 찢김, 치아/혀 관통, 눈 시선 writer 충돌을 먼저 해결한다.
4. 인사/수줍게 시선 피하기/고개 기울여 부탁하기 3개를 실제 대상에 연출한다. 준비→동작→감정 정점→여운→복귀를 별도 타이밍으로 만든다. 시선이 머리보다 먼저 이동하도록 소량의 lead를 시험하고, 모든 클립에 같은 지연을 강제하지 않는다.
5. 각 동작 3강도, 정면/3/4/클로즈업 검수. 완성된 3개가 통과하면 signature 12개로 확장, 이후 전체 계획 48개로 확장한다. 강도/속도 조합 수를 제작 완료 수로 세지 않는다.
6. 손-볼/손-컵/발-바닥 접촉과 중단/복귀를 확인한다. 기존 스켈레톤 매핑/초기 자세를 기록한다.
7. .blend 원본, glTF bone/morph 또는 개별 face curves, adapter별 런타임 테스트를 남긴다. FBX의 shape animation은 별도 검증한다. 단순 GLB 파일명 변경을 VRMA라고 부르지 않는다.
8. 동일 shot manifest로 beauty/previz/first-last/depth/pose/mask/camera 패키지를 준비한다. 생성영상과 리깅 데이터는 별개 산출물이다.
9. GPU 승인이 확인된 후 기존 Wan 5B smoke를 재현한다. Fun Control/Animate는 별도 weight/노드/VRAM 검증 과제이며 현재 5B 설치를 그 기능 완료로 간주하지 않는다.
10. H3는 과거 1인→3인 증식 문제가 남아 있다. 새 얼굴 reference와 1인 구도를 고정한 1샷을 먼저 검증하고, 기존 실패를 무시한 대량 T2V를 하지 않는다.

## 영상 공부를 남길 형식
매 실험마다 질문/가설, 고정 변수, 하나의 변경 변수, first-middle-last 프레임, MP4, 손·얼굴·인원·구도·시간 일관성 판정, 비용/VRAM/RAM, 다음 결정 1개를 기록한다. 렌즈, 시선축, 포즈 silhouette, anticipation/hold/follow-through, 컷 연결, 자막·오디오·libx264 인코딩을 차례로 검증한다.

## 외부 도구
Higgsfield: motion/camera/표현 참고 또는 최종 픽셀 제작 후보. 사용 전 현재 MCP 모델/입력 역할/비용을 다시 확인한다. 이번 준비에서 유료/무료 quota 모두 소비하지 않는다.
Tripo/Meshy/AccuRIG: 기존 몸/리깅 자산 재사용. facial topology와 expression system의 자동 완성으로 가정하지 않는다.
Audio-to-face: 입모양 보조 후보일 뿐 감정/시선/제스처 전체의 연출자가 아니다. 새로운 대형 설치보다 현재 rig mapping 우선.
