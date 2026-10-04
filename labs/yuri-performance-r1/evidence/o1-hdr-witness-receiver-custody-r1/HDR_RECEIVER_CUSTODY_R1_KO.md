# HDR witness private receiver custody R1

새 Windows 기능 없음. 기존 `40db3ec` HDR ZIP의 전달만 수행했다. 새로운 source render, modeling, exporter, Unity 변경은 없다.

**DONE:** Desktop private `pc_artifact_read` → Laptop private `fs_write` 경로로 14개 byte chunk를 새 폴더에 전달하고 `CreateNew`로 정확한 ZIP을 조립했다. Desktop/Laptop의 health identity를 먼저 확인했다. 연결된 기존 private 도구만 사용했고 새로운 서버, 공개 링크, credential, 비용, download 서비스를 만들지 않았다.

Laptop actual host: **DESKTOP-11NSABR**. Receiver path:

`C:/YuriTransfer/inbox/YURI_R4_HDR_R2_cd47090a80f6_20261004_0439/YURI_R4_SOURCE_NEUTRAL_HDR_WITNESS_R2_20261004.zip`

- Exact bytes: **13,964,358**
- SHA256: **cd47090a80f6fece8be8dc2672ab2ebd1ccba0e74e2344e13ae0e6144d975198**
- Receiver `zipfile.testzip()` CRC: **PASS**, 30 members, bad member none.
- `FILE_INDEX.json`의 29개 파일은 receiver에서 bytes 및 SHA256 전부 확인했다.
- Receiver receipt SHA256: **9007a99b54f7a5eccb454aac1441d20da5f6dc94f857515f7a08c86d7809eb5d**, **869 bytes**. 실제 receiver 저장본을 readback하여 동일 bytes/SHA로 이 evidence 폴더에 보존했다.
- Receiver receipt path: 같은 새 inbox 폴더의 `RECEIVER_CUSTODY_RECEIPT_R1.json`.
- 원본 source SHA256 **a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa** 및 Desktop sender ZIP SHA/bytes/CRC가 전달 후에도 그대로다.

**FAILED-HOLD:** 전달 실패 없음. Source-fidelity/appearance/PBR/PRIMARY 기존 gate 및 absolute cross-renderer light response HOLD를 유지한다. 이 receipt는 전달 무결성을 검증하며 새로운 visual acceptance가 아니다.

**CAUSE:** 기존 HDR packet을 consumer가 읽을 수 있는 실제 Laptop inbox에 추가 제공할 필요가 있었다. 새 고유 폴더를 먼저 생성하고 이전 파일이 있으면 중지하도록 했다. 기존 inbox/source/control/product 파일은 덮어쓰지 않았다. Consumer를 중단/재시작하거나 메시지를 보내지 않았다. Chunk staging 및 checker는 이번 새 폴더 안에만 남아 있다.

**NEXT:** Receiver가 해당 packet의 source operands 및 5개 ROI를 기존 비교 흐름에서 사용한다. OS80 consumer 통합과 독립적인 지원이며 대기/restart 지시가 아니다.

**VISUAL_EVIDENCE:** 새 render 없음. 기존 packet 내부의 동일 Render Result EXR/PNG 및 authoritative baseline을 그대로 전달했다. 송신 proof는 `SENDER_CUSTODY_RECEIPT_R1.json`, 실제 수신 proof는 `RECEIVER_CUSTODY_RECEIPT_R1.json`이다. Consumer read/사용 완료는 주장하지 않는다.
