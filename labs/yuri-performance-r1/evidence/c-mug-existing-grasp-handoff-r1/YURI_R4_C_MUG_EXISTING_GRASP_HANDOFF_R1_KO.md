# C MUG 기존 Grasp 재사용 handoff — 2026-10-05

새 motion 후보 없이 원본 Grasp 재사용만 완료했다. 활성 손은 hand.L; 오른손 채널/손목은 정지. BODY42 upper/digit bones294채널, HEAD/HAIR transport 두 Action을 기존 Talk native reader schema로 제공한다. R4/source81 OFF signature와 source/candidate bytes 동일, strict guard terminal PASS. 새 render/baseline/6Reaction/contact precision 검사는0.

24fps1..169/7초 key interval: open reach1–51, close52–69, lift closed69–85, exact full pose hold85–101, lower closed102–119, open release119–136, return open136–169. LEFT fingers exact closed plateau69–118. 이벤트는 authored data에서 추론한 integration 후보: attach69(2.833초), hold85(3.5초), release119(4.917초), fully-open136(5.625초). 처음 raw sampler의 release102 제안은 손을 낮추는 시작을 release로 오인했으므로 consumer handoff에서119로 교정했다. 102에서는 손가락이 닫힌 상태다.

Anchor는 hand.L local +Y 반 bone 길이의 provisional palm midpoint 및 해당 손 orientation이다. 실제 MUG handle fitting/penetration/contact/force proof 아님. 제품 writer가 실제 handle socket을 이 지점에 맞추고 attach/release/ownership/resume를 구현한다. 기존 source upper tracks에는 lower/root navigation이 없다. imported rest+basis/H reflection을 기존 consumer 방식으로 한 번 적용하며 parent-local Blender TRS를 Unity local 값으로 직접 복사하지 않는다.

기존 ZIP9d23f40e/librarya2808d19를 재생성하지 않았다. 예전 already_received 표시는 수신 파일 위치를 독립 검증하지 않은 것이었다. 이번 bounded inbox/Downloads/Assets/artifacts exact-name 검사는 없음을 보였고, 기존 zeros/SSH 경로로 새 inbox scope에 닫힌 ZIP 및 JSON만 전달해 각 receiver SHA/bytes 검증했다. 전역 파일 부재 증명은 아니다. 정확한 수신 위치/해시는 scalar JSON 참조; 새 archive/exporter/framework/제품 코드 변경0. Tier-C source-only/TierP0. finger/webbing/thumb/handle contact/fidelity는 PASS2 debt이며 Unity gameplay PASS는 해당 writer의 실제 receipt가 필요하다.
