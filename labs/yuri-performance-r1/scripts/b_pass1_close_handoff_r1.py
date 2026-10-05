"""Publish scalar custody only; never embed character geometry or motion arrays."""
from pathlib import Path
import json, hashlib
L=Path(__file__).resolve().parents[1]
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
E=L/'evidence/b-pass1-motion-handoff-r1'; E.mkdir(exist_ok=False)
read=lambda p:json.loads(Path(p).read_bytes())
write=lambda p,v:Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
m=read(B/'b-pass1-walkstop-idle-tierc-r1/B_WALKSTOP_IDLE_TIERC_PRIVATE_R1.json')
d=read(B/'b-pass1-walkstop-delivery-r1/DELIVERY_RECEIPT_R1.json')
ui=read(B/'b-pass1-walkstop-delivery-r1/WHOLE_NORMAL1X_UI_R1.json')
assert ui['ended'] and ui['rate']==1 and ui['error'] is None
assert d['OFF_pixels']['unequal_RGBA_channels']==0
contract={k:v for k,v in m.items() if k!='rows_private'}
contract.update({'loop':False,'default_animation':'OFF','ownership':'BODY: Meshy_Fitted_Rig. HEAD: Armature/Root. HAIR: Hair_Rig_R4/Hair_HeadRoot; all one clock. Single owner per channel; never simultaneously apply native FACE root and HEAD transport.', 'world_root':'External product controller; in-place only; no navigation/turn certification','arbitrary_interrupt':'Runtime owner crossfade; this source starts ONLY at Walk phase97','consumer':'Append Action datablocks only through existing ReactionLane. Never append geometry, materials, rigs or rebuild GameRig. Restore original state with lane.off().','product_import_gate':'UNTESTED: state/time/weight/AlwaysAnimate/non-root bone movement/root teleport/mesh and OFF restore require product-owner receipt.'})
write(E/'B_WALKSTOP_IDLE_TIERC_CONSUMER_R1.json',contract)
write(E/'B_WALKSTOP_DELIVERY_SCALAR_R1.json',{'delivery':d,'UI':ui,'source_preservation':m['original78_OFF_signature_exact'],'source_precision_PASS':False})
t=read(B/'b-pass1-walk-transfer-r2/WALK_EXACT_PACKET_TRANSFER_RECEIPT_R1.json')
t['concurrent_root_delivery_notice']='Root separately reported C:/YuriTransfer/inbox/ROOT_PM_EXISTING_WALK_6f88434a/ same ZIP SHA/bytes after this transfer finished; no further transfer. This receipt independently verifies our destination only.'
t['failed_attempt']='R1 jaewan account authentication denied before remote writes; R2 used Root-verified zeros account and unchanged key/knownhost.'
write(E/'EXISTING_WALK_RECEIVER_RECEIPT_R1.json',t)
items=[]
for name,fn,limit in [
 ('Idle','YURI_R4_A1_FEMALE_IDLE_BODY_CANDIDATE_R3_20261004.zip','Reuse existing accepted product Idle. Native Idle also exists in unchanged master.'),
 ('Walk','YURI_R4_NATIVE_WALK_SOURCE_ONLY_R1_20261005.zip','1..97@24fps; sample97 duplicates1; 96 unique samples,4sec loop. Root XYZ range0. Foot drift/contact/seam HOLD; world movement owned externally.'),
 ('Talk','YURI_R4_NATIVE_TALK_SOURCE_ONLY_R1_20261004.zip','Existing native BODY/head/hair same-clock provider; key interval5sec@24fps. Already received; no resend.'),
 ('Look','YURI_R4_LOOK_LISTEN_SOURCE_ONLY_R1_20261004.zip','Already received; gaze ownership remains provisional.'),
 ('Wave','YURI_R4_SOCIAL_GREETING_SOURCE_ONLY_R1_20261004.zip','Already received. Keys1..91@30fps,3sec interval. Hand framing supplement only; BODY contact59 HOLD.'),
 ('Grasp','YURI_R4_NATIVE_GRASP_SOURCE_ONLY_R1_20261005.zip','Already received; native169 samples@24fps; prop/physical grasp not certified.')]:
 p=B/fn;assert p.exists();items.append({'family':name,'existing_packet':str(p),'SHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'contract_limit':limit})
items.extend([{'family':'Reaction6','reuse_checkpoint':'820a23791d17838b101296b50c87fd7564db791f','report':str(L/'R4_APPEARANCE_PRESERVE_CORRECTION_R1_KO.md'),'contract_limit':'Reuse six existing Action-only reactions. Original appearance OFF exact; Light/Strong2cycles; Unity untested.'},{'family':'Autonomous/interrupt/resume','owner':'Existing product writer','contract_limit':'State selection/crossfade/pause/resume/root navigation are runtime ownership, not additional source motions.'}])
write(E/'B_REUSABLE_MOTION_INPUTS_R1.json',{'policy':'OWNER_TWO_PASS_POLICY_R1_DESKTOP','TierP':0,'reused':items,'only_new_missing_motion':contract['library'],'quality':'Tier-C PASS1 placeholder only; PASS2 precision deferred','new_export_framework':False,'product_repo_changed':False})
report='''# R4 외형 보존 / B motion handoff — 2026-10-05

R4 visual authority는 a30fc513 원본이다. 기존 appearance corrective checkpoint 820a237과 08caad7을 보존한다. 6 Reaction의 원본 geometry/material/ShapeKey/weights/rest/drivers/OFF pixel 동일성과 정상속도 증거는 기존 R4_APPEARANCE_PRESERVE_CORRECTION_R1_KO.md에 유지하며 재제작하지 않았다. 외형 승격 및 Unity runtime PASS 없음.

PASS1 B는 기존 Idle/Walk/Talk/Look/Wave/Grasp/Reaction을 재사용한다. 이번에 추가한 motion은 Walk cycle boundary97 → native Idle1 한 전환뿐이다. 25samples@24fps, key interval1초/container1.041667초, 3 Action-only library934825B SHA916d0ecb7a643907142b64f88ae38a0edf274353a3d119f906ba8ceebd4a5050. 원본78 Actions 및 original scene 전체signature/save-reopen 동일, neutral decodedRGBA 차이0. 전체25 PNG SHA 및 MP4 전체decode/실제UI ended/rate1/errornull 확인.

Tier-C placeholder / TierP0다. 임의 Walk phase interruption, floor/contact/foot sliding/velocity 및 손·목·헤어 정밀도는 PASS2 HOLD다. 실제 world locomotion/turn/Unity/AlwaysAnimate를 검증했다고 세지 않는다. HEAD transport와 native FACE root를 중복 소유하지 않는다. 같은 clock의 기존 provider와 runtime owner가 선택·복원한다.

닫힌 Walk ZIP6f88434a/63291879B를 Root가 알려준 기존 zeros/SSH 경로로 inbox에 전달하고 receiver SHA/size를 확인했다. 이후 Root도 별도 경로 전달 완료를 통지하여 같은 packet이 두 경로에 존재한다. 추가전송/삭제/overwrite 없음. 첫 jaewan 인증 실패는 copy 전 종료. 새 exporter/Walk 재생성 없음.

위 JSON들은 실제 경로·SHA·소유권·한계를 제공한다. review: http://127.0.0.1:18949/REVIEW_B_WALKSTOP_TIERC_R1.html . Blender/MP4/캐릭터 데이터는 private local outputs에만 존재한다. GPU/GUI/product/main 수정0. 다음은 기존 product writer의 Generic/native binding과 state/time/weight/AlwaysAnimate/actual bones/restore receipt; Desktop precision micro-chain은 추가하지 않는다.
'''
(E/'YURI_R4_B_PASS1_MOTION_HANDOFF_R1_KO.md').write_text(report,encoding='utf8')
latest=read(L/'LATEST_RUN.json');latest['b_pass1_motion_handoff_r1']={'report':str(E/'YURI_R4_B_PASS1_MOTION_HANDOFF_R1_KO.md'),'only_new_motion':contract['library'],'candidate_SHA':m['candidate_SHA'],'library_SHA':m['library_SHA'],'OFF_pixel_diff':0,'TierP':0,'precision':'PASS2 HOLD','review':'http://127.0.0.1:18949/REVIEW_B_WALKSTOP_TIERC_R1.html','walk_receiver':t['receiver']};write(L/'LATEST_RUN.json',latest)
p=L/'CODEX_HANDOFF_KO.md';p.write_text('# 2026-10-05 B PASS1 reuse / R4 appearance preserved\n\n기존 외형 correction820a237/08caad7 보존. 새 motion 하나: Walk97→Idle1 Tier-C3Actions, OFFpixel0/original78 동일/25@24fps 전체1x. 기존 Walk packet exact receiver SHA 확인; Root와 동시 전달로 inbox 두 사본, 추가 전송 금지. Idle/Talk/Look/Wave/Grasp/Reaction 재사용. Precision PASS2 HOLD/TierP0/Unity미검증. report evidence/b-pass1-motion-handoff-r1/YURI_R4_B_PASS1_MOTION_HANDOFF_R1_KO.md 및 consumer JSON 참조.\n\n'+p.read_text(encoding='utf8'),encoding='utf8')
print('B_PASS1_HANDOFF_CLOSED_SOURCE_APPEARANCE_PRESERVED')
