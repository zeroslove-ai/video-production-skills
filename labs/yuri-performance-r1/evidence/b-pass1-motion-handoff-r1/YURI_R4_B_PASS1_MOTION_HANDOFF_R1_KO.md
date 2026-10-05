# R4 외형 보존 / B motion handoff — 2026-10-05

R4 visual authority는 a30fc513 원본이다. 기존 appearance corrective checkpoint 820a237과 08caad7을 보존한다. 6 Reaction의 원본 geometry/material/ShapeKey/weights/rest/drivers/OFF pixel 동일성과 정상속도 증거는 기존 R4_APPEARANCE_PRESERVE_CORRECTION_R1_KO.md에 유지하며 재제작하지 않았다. 외형 승격 및 Unity runtime PASS 없음.

PASS1 B는 기존 Idle/Walk/Talk/Look/Wave/Grasp/Reaction을 재사용한다. 이번에 추가한 motion은 Walk cycle boundary97 → native Idle1 한 전환뿐이다. 25samples@24fps, key interval1초/container1.041667초, 3 Action-only library934825B SHA916d0ecb7a643907142b64f88ae38a0edf274353a3d119f906ba8ceebd4a5050. 원본78 Actions 및 original scene 전체signature/save-reopen 동일, neutral decodedRGBA 차이0. 전체25 PNG SHA 및 MP4 전체decode/실제UI ended/rate1/errornull 확인.

Tier-C placeholder / TierP0다. 임의 Walk phase interruption, floor/contact/foot sliding/velocity 및 손·목·헤어 정밀도는 PASS2 HOLD다. 실제 world locomotion/turn/Unity/AlwaysAnimate를 검증했다고 세지 않는다. HEAD transport와 native FACE root를 중복 소유하지 않는다. 같은 clock의 기존 provider와 runtime owner가 선택·복원한다.

닫힌 Walk ZIP6f88434a/63291879B를 Root가 알려준 기존 zeros/SSH 경로로 inbox에 전달하고 receiver SHA/size를 확인했다. 이후 Root도 별도 경로 전달 완료를 통지하여 같은 packet이 두 경로에 존재한다. 추가전송/삭제/overwrite 없음. 첫 jaewan 인증 실패는 copy 전 종료. 새 exporter/Walk 재생성 없음.

위 JSON들은 실제 경로·SHA·소유권·한계를 제공한다. review: http://127.0.0.1:18949/REVIEW_B_WALKSTOP_TIERC_R1.html . Blender/MP4/캐릭터 데이터는 private local outputs에만 존재한다. GPU/GUI/product/main 수정0. 다음은 기존 product writer의 Generic/native binding과 state/time/weight/AlwaysAnimate/actual bones/restore receipt; Desktop precision micro-chain은 추가하지 않는다.

추가 coordination closure: 원본 Walk97 consumer samples는 guard terminal PASS/source81 OFF 동일로 로컬 완료됐으나, 직후 Laptop의 기존 Talk reader exit0 확인 통지를 받아 전송·중복 적용하지 않았다. 새 sampler/framework 확장 종료. MUG 기존 Grasp9d23f40e/Action library a2808d19를 CRC member SHA 확인하여 재사용 입력으로 지정했다. 실제 부족한 motion이 아직 입증되지 않아 새 Grasp를 만들지 않았다.
