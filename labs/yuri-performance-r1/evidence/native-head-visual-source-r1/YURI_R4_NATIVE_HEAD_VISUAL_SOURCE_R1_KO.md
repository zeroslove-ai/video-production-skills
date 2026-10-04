# Native BODY_HeadGazeHair source visual checkpoint — 2026-10-05

원본 BODY_HeadGazeHair의 좌우 head 동작1..97/24fps를 front/side에서 정상속도로 확인했으며, 큰 새 mouth 얼룩·hair 분리·neck seam 벌어짐은 관찰되지 않았다. 미세 shading은 CPU8sample 노이즈 한계, blink·mouth morph·독립 gaze는 BODY-only take의 미검증 범위다.

원본 SHA: a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa. 정확한 기존 Action: MESHY_R2_BODY_HeadGazeHair, source Action signature SHA 218c7deec182c7a6c1d400ac8c22b2b3943ac44cbaf458e4aa45e4393f6aba92. 364개 원본 curve RNA를 모두 resolve했을 때 호환 Object는 Meshy_Fitted_Rig 하나다. OBLegacy Slot/OBJECT/실제 slot handle은 scalar receipt 참조. 새 Action·transport·mesh·rig·exporter·후보 생성0, 원본 source 저장0. 기존 FACE KEY/GAZE/HAIR native take는 이름만으로 연결하지 않았다.

원본 shader/material/node/texture/driver/weights/rest/72ShapeKeys/78Actions 및 source scene 카메라 설정을 ON→OFF 후 full raw signature exact 복원했다.960×920 source-camera neutral decodedRGBA changed pixels0/max delta0. 동일 원본·08caad7/R2·닫힌 Walk/precision 증거 packet 보존. Walk contact/foot slide/velocity/TierP/F2 HOLD는 이 검사로 변하지 않는다.

실제 head 최대 OFF변위25.837mm(f63),hair38.684mm(f65),body5.256mm(f37). 눈 world pose는 head를 따라 움직이나 head-relative matrix 변화는1.6e-7 미만이다. 원본72 morph values는 전97프레임 모두0이다. **실제 BODY head-motion에서 source 외형 정상 범위이며, 독립 gaze/blink/mouth morph 안정성이나 전체 HeadGazeHair multi-channel 연기 PASS가 아니다.**

은백색/gray-white 헤어는 canonical source에서 이미 관찰된다. 이를 Unity 오류나 donor 교체 증거로 단정하지 않는다. Mouth 주변의 큰 Unity식 blotch/neck 분리 현상을 이 source motion에서 재현하지 못했다. 현재 source 비교 범위는 정상이며 Unity단계 matched 검사 필요다. 실제 Unity scene/shader/normal/tangent/lighting/alpha/material adapter를 여기서 수정·검증하지 않았다.

정상속도 증거는 고정 front/positiveX_side384×384 ortho0.28m, original24fps full97=4.041667s(4.0s endpoint span) 두 MP4와 전체194PNG이다. 두 fullframe grid 검토, 전체 MP4 decode, 실제 UI1x ended/error null 완료. CPU2threads4GiB owned guard1job/정상exit0/drainActive0,elapsed 272.385초. ProtectedGUI/GPU lease/product/Laptop 변경0.

`review/LAPTOP_MATCHED_SOURCE_REFERENCE_PRIVATE_R1.json`에 원본 전체 shader/texture/scene signature, Action·slot, 실제 camera transform/target/ortho/lens/sensor, frame1/13/25/37/49/61/73/85/97의 morph values/actual pose/meshhash/PNG SHA를 연결했다. Full97 raw rows에서는 f63/65도 exact 확인 가능하다. Original source .blend와 기존 ReactionLane도 private reference packet에 포함했다. Source camera와 QA 고정 camera는 구분하며 export용 camera 변경을 저장하지 않았다.

최소 다음 대안 하나: Laptop이 이 BODY-only source 기준과 동일 frame/camera/zero morph를 맞춰 Unity gray-white hair·mouth/neck shading stage를 검사한다. Auxiliary face/morph take 연구나 sampling 증가는 별도 bounded 필요가 생길 때만 한다. 이번에는 Walk precision/epsilon/Idle/wholecorpus/shape-key sweep을 반복하지 않았다.
