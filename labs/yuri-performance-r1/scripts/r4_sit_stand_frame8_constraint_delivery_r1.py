"""Publish scalar-only source discriminator closure; private assets remain outside Git."""
from pathlib import Path
import json,hashlib,zipfile
import numpy as np
from PIL import Image
LAB=Path(__file__).resolve().parents[1];B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-sit-stand-frame8-constraint-r1';R=B/'alpha-sit-stand-frame8-capture-repair-r1b';RG=B/'o1-sit-stand-frame8-capture-repair-r1b';G=B/'o1-sit-stand-frame8-constraint-r1';E=LAB/'evidence/sit-stand-frame8-constraint-r1';E.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();m=json.loads((O/'FRAME8_NATIVE_CONSTRAINT_PRIVATE_R1.json').read_bytes());g=json.loads((G/'NATIVE_GUARD_RESULT.json').read_bytes());assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN'
assert sha(m['candidate'])==m['candidate_SHA'] and sha(m['library'])==m['library_SHA']
a=np.array(Image.open(B/'alpha-a1-contact-qa-r3/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png').convert('RGBA'));b=np.array(Image.open(R/'OFF_SOURCE_CAMERA_NEUTRAL.png').convert('RGBA'));assert a.shape==b.shape;off={'dimensions':list(a.shape),'unequal_pixels':int(np.any(a!=b,axis=2).sum()),'max_channel_delta':int(np.abs(a.astype(int)-b.astype(int)).max())};assert off['unequal_pixels']==0
public={k:m[k] for k in ['task','source_SHA','old_candidate_SHA','candidate','candidate_SHA','library','library_SHA','frame8_only','solve_iteration_history','solve_seconds','variables','whole_original_sole_anchor_vertices','corridor_definition','old_actual','constraint_actual','constraints_all_residuals_within_declared_tolerance','exact_old18_retained','exact_old18_removed','all_crossings_counts','source78_fullraw_OFF_and_serialized_candidate_equal','pose_pass','TierP','next']};public['OFF_pixel_QA']=off;repair=json.loads((RG/'NATIVE_GUARD_RESULT.json').read_bytes());assert repair['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN';public['capture_repair_guard_SHA']=sha(RG/'NATIVE_GUARD_RESULT.json');public['initial_matched_capture_invalid_decoded_pixels_identical']=True;public['guard_SHA']=sha(G/'NATIVE_GUARD_RESULT.json');public['finite_bounded_optimizer_not_global_infeasibility_proof']=True;public['verdict']='PASS_SOURCE_POSE_ONLY' if m['pose_pass'] else 'FAIL_HOLD_CONSTRAINT_RESIDUALS_OR_NEW_SURFACE_CROSSINGS'
(E/'FRAME8_NATIVE_CONSTRAINT_SCALAR_QA_R1.json').write_text(json.dumps(public,indent=2),encoding='utf8')
rows=[]
for q in ['L','R']:
 old=m['old_actual'][q];new=m['constraint_actual'][q];rows.append(f"| {q} | {old['knee_flexion_degrees']:.6f} → {new['knee_flexion_degrees']:.6f} / donor {new['desired_donor_knee_degrees']:.6f} | {new['knee_angle_error_degrees']:+.6f} | {old['whole_original_patch_max_anchor_error_m']*1000:.6f} → {new['whole_original_patch_max_anchor_error_m']*1000:.6f} | {new['knee_forward_m']*1000:+.6f} / {new['knee_lateral_m']*1000:+.6f} |")
cross='\n'.join(f"- {k}: old {v['old_new_vs_OFF']} → constrained {v['constraint_new_vs_OFF']}; introduced relative old {v['introduced_vs_old']}." for k,v in m['all_crossings_counts'].items())
report=f'''USER_CAN_NOW_SEE_OR_DO: 첫 실패 frame8의 기존/관절제약 pose를 정면·3/4·측면에서 비교할 수 있다. 판정 {public['verdict']}; 전체 Sit/Stand/물리 접촉 승격 없음.

# R4 Sit/Stand frame8 원본 rig 관절 제약 discriminator

원본 mesh/재질/weights/modifiers/rest/bind/rig hierarchy 및78 Actions를 보존했다. 이전 실패후보8bc13115 및 packet1103147f는 그대로 남겼다. 새 rig/geometry/바인딩/충돌기/런타임을 만들지 않고 원본 R4의 추가 Action3개만 만들었다. Upper local pose reference는 이전 frame8 값으로 고정; pelvis orientation도 고정. Pelvis local translation3 + 양쪽 thigh/shin/foot exponential-map rotation18로 ONE bounded least-squares solve. Toe local rotation은 원본 OFF를 사용했다. 각 iteration은 같은 제약식의 수치해법이며 후보 강도군이 아니다.

목표는 원본 OFF whole-sole patch L218/R223 모든 vertices의 world anchors, donor 실제 관절의 anatomical knee flexion, 원본 foot→toe forward half-plane 및 sagittal lateral15mm corridor. Anchor maximum1mm/knee0.5deg를 declared tolerance로 사용했다. 관절 pose 조건이며 실제 force/지지/seat contact 증거가 아니다.

| Side | actual knee old→new / donor(deg) | new error(deg) | whole patch max anchor residual old→new(mm) | knee forward / lateral(mm) |
|---|---|---|---|---|
{chr(10).join(rows)}

저장된 첫18 actual nonadjacent BODY pair identities를 다시 검사했다: retained{m['exact_old18_retained']}, removed{m['exact_old18_removed']}. 기존 pair count만 줄이는 것으로 통과시키지 않고 모든 weak/unweighted BODY/HEAD/HAIR triangles의 source OFF 대비 새 self/cross identities도 검사했다.

{cross}

조건 residual tolerance 통과: {m['constraints_all_residuals_within_declared_tolerance']}. Surface/pose 종합 PASS: {m['pose_pass']}. 유한 iteration/180sec 내부 solve budget에서 feasible solution을 얻었는지에 대한 실험이다. 수학적 전역 infeasibility나 immutable source skin weights의 단독 원인을 증명하지 않는다. Residual이 남으면 이번 donor-angle + original whole-sole anchors + fixed upper/pelvis orientation 조합을 production 후보로 거절한다. Exact donor 체형이나 물리적 foot support를 주장하지 않는다.

원본 OFF/fresh serialized full signature 동일, source camera960×920 decoded RGBA unequal pixels0/maxdelta0. Candidate defaults OFF. 3 pose Actions-only library에 mesh/rig/objects를 넣지 않았다. Head/hair는 기존 root에 head rigid transport로 부착하고 gaze/face drivers를 유지했다. 첫 capture repair는 저장된 pose-only 후보에 old4Actions가 없어서 bind 전 KeyError로 실패했다. 보존 후 suffixR1b에서 immutable old Action library를 append하여 완료했다. 처음 manual assignment 렌더는 Action 재평가로 old/new decoded RGBA가 동일해 비교 증거에서 제외/보존했다. 별도 동일SHA candidate capture-only guard로 두 Action을 명시적으로 바인딩, exact actual triangle identities 및 mesh SHA before/after 각 렌더를 재확인한 6장을 사용한다. Solve/새candidate/121frame 재실행 없음. Native guard CPU2threads/4GiB/600sec unchanged, strict LIVE/terminal/drain PASS. SOURCE/이전candidate SHA unchanged. GPU/protectedGUI/Product/Laptop/Unity/main 변경0; TierP0/F2/StageB 미승격.

실패 시 연구 분리: donor anatomical angle을 그대로 고정하는 방식 대신, 원본 R4에서 무릎-forward와 표면 clearance를 먼저 만족하는 native seated pose/feet-contact schedule을 설계하고 donor는 phrase timing/hip-height reference로 사용한다. 이는 별도 접근 제안이며 이 checkpoint에서 추가 pose/전체121frame sweep은 실행하지 않았다. 전달용 첫 batch는 기존 NativeTalk packet135fdc26/libraryeae83ac3를 재사용할 수 있으나 Sit capability로 세지 않는다.

Candidate SHA {m['candidate_SHA']}.
Action-only SHA {m['library_SHA']}.
Guard SHA {public['guard_SHA']}.
원본 a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa와08caad7/R2/R3d/6Reaction/닫힌 ZIP은 보존했다.
'''
(E/'YURI_R4_SIT_STAND_FRAME8_CONSTRAINT_R1_KO.md').write_text(report,encoding='utf8')
html='<html><meta charset="utf-8"><title>R4 frame8 constraint discriminator</title><body style="background:#191923;color:white;font-family:sans-serif"><h1>R4 native frame8: old vs constrained</h1><p>'+public['verdict']+'; still-pose evidence only, no sequence/physics PASS.</p><table><tr><th></th><th>Front</th><th>Quarter</th><th>Side</th></tr>'
for label in ['old','constraint']:html+='<tr><th>'+label+'</th>'+''.join('<td><img width="384" src="'+label+'_'+v+'.png"></td>' for v in ['front','quarter','side'])+'</tr>'
html+='</table><pre>'+json.dumps({'old':m['old_actual'],'constraint':m['constraint_actual'],'counts':m['all_crossings_counts']},indent=2)+'</pre></body></html>';(R/'REVIEW_FRAME8_CONSTRAINT_R1.html').write_text(html,encoding='utf8')
entries={}
def add(p,a):
 p=Path(p);assert p.is_file() and a not in entries;entries[a]=p
source=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/target-reference/Character_Master_NeckSkin_R4.blend');assert sha(source)==m['source_SHA'];add(source,'source/Character_Master_NeckSkin_R4.blend')
add(B/'alpha-sit-stand-source-candidate-r1/YURI_R4_SIT_STAND_ACTIONS_ONLY_R1.blend','old-reference/YURI_R4_SIT_STAND_ACTIONS_ONLY_R1.blend')
for folder,prefix in [(O,'native-pose-qa-with-preserved-invalid-initial-images'),(G,'owned-native-guard'),(R,'correct-Action-bound-matched-capture'),(RG,'capture-repair-guard'),(B/'o1-sit-stand-frame8-capture-repair-r1','preserved-first-capture-repair-missing-old-library-failure'),(E,'scalar-qa')]:
 for p in folder.rglob('*'):
  if p.is_file():add(p,prefix+'/'+p.relative_to(folder).as_posix())
for n in ['r4_sit_stand_frame8_constraint_r1.py','r4_sit_stand_frame8_constraint_owned_prepare_r1.py','r4_sit_stand_frame8_constraint_delivery_r1.py','r4_sit_stand_frame8_capture_repair_r1.py','r4_sit_stand_frame8_capture_repair_r1b.py','r4_sit_stand_frame8_capture_owned_prepare_r1.py','r4_appearance_adapter.py','r4_appearance_signature.py','r4_sit_stand_adapter_r1.py','r4_native_walk_source_supply_r1.py','r4_existing_reach_contact_closure_r1.py']:add(LAB/'scripts'/n,'workflow/'+n)
index={'source_SHA':m['source_SHA'],'candidate_SHA':m['candidate_SHA'],'library_SHA':m['library_SHA'],'verdict':public['verdict'],'members':[{'path':a,'bytes':p.stat().st_size,'sha256':sha(p)} for a,p in sorted(entries.items())]};ip=O/'PACKET_INDEX_R1.json';ip.write_text(json.dumps(index,indent=2),encoding='utf8');add(ip,'PACKET_INDEX_R1.json');z=B/'YURI_R4_SIT_STAND_FRAME8_CONSTRAINT_R1_20261005.zip'
with zipfile.ZipFile(z,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for a,p in sorted(entries.items()):f.write(p,a)
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None
 for row in index['members']:
  v=f.read(row['path']);assert len(v)==row['bytes'] and hashlib.sha256(v).hexdigest()==row['sha256']
receipt={'packet':str(z),'sha256':sha(z),'bytes':z.stat().st_size,'members':len(entries),'indexed_members':len(index['members']),'CRC_SHA_size_all_verified':True,'closed_once':True,'source_SHA':m['source_SHA'],'candidate_SHA':m['candidate_SHA'],'library_SHA':m['library_SHA'],'verdict':public['verdict'],'TierP':0};(E/'PRIVATE_PACKET_RECEIPT_R1.json').write_text(json.dumps(receipt,indent=2),encoding='utf8');print(json.dumps(public,indent=2));print(json.dumps(receipt,indent=2))
