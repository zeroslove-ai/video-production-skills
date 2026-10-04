"""Close failed native seated pose, scalar-only public report and immutable private packet."""
from pathlib import Path
import json,hashlib,zipfile
from PIL import Image
import numpy as np
LAB=Path(__file__).resolve().parents[1];B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-target-native-seated-pose-r1';G=B/'o1-target-native-seated-pose-r1';E=LAB/'evidence/target-native-seated-pose-r1';E.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();m=json.loads((O/'TARGET_NATIVE_SEATED_POSE_PRIVATE_R1.json').read_bytes());g=json.loads((G/'NATIVE_GUARD_RESULT.json').read_bytes());assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN' and not m['pose_pass'];assert sha(m['candidate'])==m['candidate_SHA'] and sha(m['library'])==m['library_SHA']
a=np.array(Image.open(B/'alpha-a1-contact-qa-r3/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png').convert('RGBA'));b=np.array(Image.open(O/'OFF_SOURCE_CAMERA_NEUTRAL.png').convert('RGBA'));assert a.shape==b.shape;off={'dimensions':list(a.shape),'unequal_pixels':int(np.any(a!=b,axis=2).sum()),'max_channel_delta':int(np.abs(a.astype(int)-b.astype(int)).max())};assert off['unequal_pixels']==0
public={k:m[k] for k in ['task','source_SHA','candidate','candidate_SHA','library','library_SHA','original78_fullraw_OFF_serialized_equal','one_native_high_seat_pose_only','donor_contribution','native_leg_length_m','pelvis_delta_world_m','pelvis_goal_world_m','seat_witness','actual_joint_and_whole_sole_metrics','surface_counts','new_BODY_pair_regions_from_original_weights','head_hair_translation_goal_max_matrix_error','capture','pose_pass','verdict','TierP']};public['OFF_pixel_QA']=off;public['guard_SHA']=sha(G/'NATIVE_GUARD_RESULT.json');public['seated_family_closed_without_phrase_expansion']=True;public['new_crossing_depth_or_volume_not_measured']=True;public['no_skin_weights_only_or_all_native_seated_infeasibility_claim']=True;public['next_selected_existing_independent_motion']={'Action':'MESHY_R2_BODY_Tour','original_Action_SHA':m['original78_signature_private']['actions']['MESHY_R2_BODY_Tour'],'intent':'Living room-orientation / turn-and-look reference; existing original Action source supply lacks dedicated native whole-playback QA checkpoint in this lab.','not_executed_or_promoted':True,'source_only_next_scope':'Original-native Action/neck-head-hair transport with original geometry and defaultOFF; inspect exact source tracks, actual foot/root/contact trajectory and whole1x before any Unity use. No new corpus/framework or donor candidate.'};public['provisional_Wave_followup_superseded']='Existing authored social greeting full1x evidence was found in current lab; avoid duplicate greeting supply. No Wave job launched.'
(E/'TARGET_NATIVE_SEATED_SCALAR_QA_R1.json').write_text(json.dumps(public,indent=2),encoding='utf8')
rows=[]
for q,x in m['actual_joint_and_whole_sole_metrics'].items():rows.append(f"| {q} | {x['native_anatomical_knee_degrees']:.6f} | {x['ankle_goal_error_m']*1000:.6f} | {x['whole_original_patch_max_anchor_error_m']*1000:.6f} | {x['patch_XY_max_drift_m']*1000:.6f} | {x['whole_foot_min_gap_m']*1000:+.6f} |")
report=f'''USER_CAN_NOW_SEE_OR_DO: 원본 standing OFF와 target-native 높은 좌면 pose를 정면·3/4·측면에서 비교할 수 있다. 단일 pose FAIL/HOLD이며 enter/hold/exit 또는 Sit 완료를 주장하지 않는다.

# Target-native seated source discriminator R1

Donor angle/stance/floorfit family를 중단하고 원본 R4 neutral/world joint anatomy에서 새 single native pose를 만들었다. Source78 Actions/4rig/rest/bind/hierarchy/weights/ShapeKeys/materials/textures/shader/modifiers/face-gaze drivers 그대로이며3 추가 Action만 존재한다. Source/model merge/geometry substitution0, product/Unity/main/Laptop 변경0.

Native hip→knee→ankle leg length 평균 {m['native_leg_length_m']:.9f}m 기준 posterior10%/lower20%: pelvis world delta {m['pelvis_delta_world_m']}m. 각 native thigh/shin2bone analytical IK는 원본 ankle world position과 forward pole을 유지하고 foot world orientation/toe local pose는 original OFF 사용. Donor는 timing/intent만 참고한다. 이번에는 pose 하나만 평가했으므로 실제 donor sequence/timing 적용은0이다. Fixed high-seat witness plane worldZ {m['seat_witness']['plane_z_world_m']:.9f}m, source floor 위 {m['seat_witness']['height_above_floor_m']:.9f}m, pelvis clearance design35mm; actual pelvis goal error {m['seat_witness']['actual_pelvis_goal_error_m']*1000:.9f}mm. 실제 chair geometry/force support/contact certification은 없다.

| side | actual knee flexion(deg) | ankle goal error(mm) | whole original sole anchor max residual(mm) | patch XY max drift(mm) | actual lowest sole gap(mm) |
|---|---|---|---|---|---|
{chr(10).join(rows)}

Ankle joint는 원래 world 위치로 거의 정확하게 되지만, 실제 unchanged skin surface는 L3.185/R3.231mm 이동했다. Original whole patch L218/R223vertices 고정1mm gate 실패다. 원본 joint가 맞는다는 사실은 실제 sole shape/contact의 일치를 보장하지 않는다. Knee-forward offset 양쪽138.542mm, lateral ±.328mm로 joint tracking corridor는 만족했다. 양쪽72.641deg actual anatomical flexion에서 source BODYself0→71 new nonadjacent triangle pairs: shin.L/thigh.L27, shin.R/thigh.R24, thigh.R/thigh.R11, thigh.L/thigh.L9. 손/hip/thigh clearance보다 먼저 양쪽 무릎/허벅지 접힘 surface가 실패한다. Actual full weak/unweighted BODY/HEAD/HAIR 및 cross pair identities를 private report에 보존했다. Signed penetration depth/volume는 미측정이므로 숫자로 주장하지 않는다.

HEAD new self0; HAIR newself7; BODY↔HEAD new0, BODY↔HAIR0, HEAD↔HAIR0. Original baseline absolute intersections HEAD1993/HAIR1858/BODY↔HEAD44/HEAD↔HAIR20도 공개 scalar에 보존했다. Baseline 자체가 intersection-free character라는 주장은 없다.

Head translation goal matrix error Armature {m['head_hair_translation_goal_max_matrix_error']['Armature']:.12g}; Hair_Rig_R4 {m['head_hair_translation_goal_max_matrix_error']['Hair_Rig_R4']:.12g} (translation94.121mm mismatch). 이 additive translation 구현은 hair attachment goal을 제대로 만족하지 못한 별도 adapter 결함이다. 정면/3/4/측면상 머리/목이 크게 떨어져 보이지 않더라도 attachment PASS로 처리하지 않는다. 이 문제는 BODY knee71/sole3.2mm 실패와 독립이며 원본 weights만 원인으로 단정하지 않는다. 원본 hierarchy dependency가 있는 hair root에 단순 translation 적용을 다음 자산으로 재사용하지 않는다. 기존 validated full-world native head transport 경로가 별도로 남아 있다.

실측 pose를 keyframe Action에 저장 후 다시 평가했고 capture 전후 actual BODY/HEAD/HAIR vertex buffers가 모두 정확히 같다. Neutral OFF before/after/fresh serialized original78 signature 동일,960×920RGBA unequal pixels0/maxdelta0. Source SHA a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa 그대로. Strict owned native guard {public['guard_SHA']} PASS; CPU2threads/4GiB/600sec/보호된 GUI/GPUlease 기준 유지. 기존08caad7/R2/R3d/6Reaction 및 failed Sit/Stand/frame8 후보/닫힌ZIP 보존.

판정은 {m['verdict']}, TierP0/StageB/F2 미승격. ONE pose 실패 뒤 full121frame/contact sweep/1x sequence0, 같은 seated family 추가 strength/height/angle tune0. 이 ONE selected high-seat pose의 실패이며 모든 native seated pose가 불가능하다는 증거는 아니다.

다음 독립 첫 batch source 후보로 original `MESHY_R2_BODY_Tour`를 선택한다. 현재 lab에 이 Action의 dedicated native full-motion source QA 공급 checkpoint가 없어 Living room-orientation/turn-look 활동을 검증할 수 있다. Already accepted Talk를 대체하지 않으며 existing authored greeting 공급도 중복하지 않는다. 원본 source Action SHA {public['next_selected_existing_independent_motion']['original_Action_SHA']}. 정확한 native tracks/foot-root/contact/full1x 검증은 다음 범위이며 이번 checkpoint에서 Tour job을 실행하거나 통과했다고 세지 않았다.

Candidate SHA {m['candidate_SHA']}.
Action-only library SHA {m['library_SHA']}.
Closed private packet receipt는 PRIVATE_PACKET_RECEIPT_R1.json. 최종 adoption/Unity/StageB/F2는 owner gate다.
'''
(E/'YURI_R4_TARGET_NATIVE_SEATED_FAILURE_R1_KO.md').write_text(report,encoding='utf8')
html='<html><meta charset="utf-8"><title>R4 target native seated failure</title><body style="background:#191923;color:white;font-family:sans-serif"><h1>Original standing / native high-seat pose</h1><p>FAIL/HOLD: knee71 new crossings, whole soles3.2mm residual, HairRoot goal mismatch. Pose-only; no sequence/physics PASS.</p><table><tr><th></th><th>Front</th><th>Quarter</th><th>Side</th></tr>'
for label in ['standing_OFF','seated']:html+='<tr><th>'+label+'</th>'+''.join('<td><img width="384" src="'+label+'_'+v+'.png"></td>' for v in ['front','quarter','side'])+'</tr>'
(O/'REVIEW_TARGET_NATIVE_HIGH_SEAT_R1.html').write_text(html+'</table></body></html>',encoding='utf8');entries={}
def add(p,a):
 p=Path(p);assert p.is_file() and a not in entries;entries[a]=p
source=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/target-reference/Character_Master_NeckSkin_R4.blend');assert sha(source)==m['source_SHA'];add(source,'source/Character_Master_NeckSkin_R4.blend')
for folder,prefix in [(O,'native-pose-qa'),(G,'owned-native-guard'),(E,'scalar-qa')]:
 for p in folder.rglob('*'):
  if p.is_file():add(p,prefix+'/'+p.relative_to(folder).as_posix())
for n in ['r4_target_native_seated_pose_r1.py','r4_target_native_seated_owned_prepare_r1.py','r4_target_native_seated_delivery_r1.py','r4_appearance_adapter.py','r4_appearance_signature.py','r4_native_walk_source_supply_r1.py','r4_existing_reach_contact_closure_r1.py']:add(LAB/'scripts'/n,'workflow/'+n)
index={'source_SHA':m['source_SHA'],'candidate_SHA':m['candidate_SHA'],'library_SHA':m['library_SHA'],'status':m['verdict'],'members':[{'path':a,'bytes':p.stat().st_size,'sha256':sha(p)} for a,p in sorted(entries.items())]};ip=O/'PACKET_INDEX_R1.json';ip.write_text(json.dumps(index,indent=2),encoding='utf8');add(ip,'PACKET_INDEX_R1.json');z=B/'YURI_R4_TARGET_NATIVE_HIGH_SEAT_FAILURE_R1_20261005.zip'
with zipfile.ZipFile(z,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for a,p in sorted(entries.items()):f.write(p,a)
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None
 for row in index['members']:
  v=f.read(row['path']);assert len(v)==row['bytes'] and hashlib.sha256(v).hexdigest()==row['sha256']
receipt={'packet':str(z),'sha256':sha(z),'bytes':z.stat().st_size,'members':len(entries),'indexed_members':len(index['members']),'CRC_SHA_size_all_verified':True,'closed_once':True,'source_SHA':m['source_SHA'],'candidate_SHA':m['candidate_SHA'],'library_SHA':m['library_SHA'],'verdict':m['verdict'],'TierP':0};(E/'PRIVATE_PACKET_RECEIPT_R1.json').write_text(json.dumps(receipt,indent=2),encoding='utf8');print(json.dumps(receipt,indent=2))
