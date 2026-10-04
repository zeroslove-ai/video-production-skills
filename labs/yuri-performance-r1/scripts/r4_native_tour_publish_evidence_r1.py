"""Publish scalar source QA and custody pointers only; no failed source packet."""
from pathlib import Path
import json,hashlib
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
L=Path(__file__).resolve().parents[1];E=L/'evidence/native-tour-source-r1';E.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
m=json.loads((B/'alpha-native-tour-recovery-r2/NATIVE_TOUR_RECOVERY_PRIVATE_R2.json').read_bytes())
keys=['source_SHA','source_Action_SHA','candidate_SHA','candidate_bytes','fps','frames','endpoint_span_seconds','container_seconds','source_body_curves','all_original_keys_handles_modifiers_exact_fresh_candidate','all769_full_head_hair_root_goal_matrix_max_error','root_turn_look','whole_sole_oracle_replay_all769','support_patch_only_SHA','support_patch_only_bytes','large_original_feet_npz_truncated_preserved_not_trusted','all769_saved_actual_contact_ledger_complete','all_surface_peak_new','first_BODY_new_frame','worst_BODY_new_frame','first_worst_BODY_localization','all_source78_OFF_and_serialized_candidate_equal','original_data_guard_resource_FAIL_retained','guard_failure_SHA','full_motion_authoring_or_full769_contact_rerun','all769_transform_replay_only','scoped_gate_pass','TierP']
q={k:m[k] for k in keys};q['support']={s:{k:v for k,v in m['support'][s].items() if 'private' not in k} for s in ['L','R']}
q.update(verdict='FAIL_HOLD_NATIVE_TOUR_SURFACE',source_packet='NOT_CREATED_SCOPED_GATE_FAIL',runtime_Unity_F2_StageB='UNTESTED',usable_scope='exact native in-place showcase research/reference only; no root walk/turn',next_minimum_correction='ONE Action-only elbow flexion trajectory adjustment at first failing frame302 and neighboring transition; compare exact new pair IDs and native timing; preserve immutable skin/rest and keep wrist472 as independent HOLD. Not executed.')
guards=[]
for name in ['source-r1','intake-r1','source-r2','source-r3','source-r4','recovery-r1','recovery-r2','capture-front-r1','capture-front-r2','capture-quarter-r2','capture-side-r2','close-defects-r1']:
 p=B/f'o1-native-tour-{name}/NATIVE_GUARD_RESULT.json'
 if p.exists():
  g=json.loads(p.read_bytes());guards.append({'name':name,'status':g['guard_status'],'SHA':sha(p),'private_path':str(p)})
q['guard_custody']=guards
private=[B/'alpha-native-tour-recovery-r2/NATIVE_TOUR_RECOVERY_PRIVATE_R2.json',B/'alpha-native-tour-source-r4/NATIVE_TOUR_SURFACE_IDENTITIES_PRIVATE_R1.json.gz',B/'alpha-native-tour-foot-oracle-verified-r2/LOSSLESS_ORACLE_READBACK_RECEIPT_R2.json',B/'alpha-native-tour-foot-oracle-verified-r2/NATIVE_TOUR_SUPPORT_PATCH_VERIFIED_ATOMIC_R2.npz',B/'alpha-native-tour-delivery-r1/VIDEO_CUSTODY_R1.json',B/'alpha-native-tour-delivery-r1/OFF_PIXEL_QA_R1.json',B/'alpha-native-tour-delivery-r1/WHOLE_NORMAL1X_UI_R1.json',B/'alpha-native-tour-close-defects-r1/MATCHED_DEFECT_CAPTURE_PRIVATE_R1.json']
q['private_evidence']=[{'path':str(p),'SHA':sha(p),'bytes':p.stat().st_size} for p in private]
(E/'NATIVE_TOUR_SCALAR_QA_R1.json').write_text(json.dumps(q,indent=2),encoding='utf8')
v=json.loads((B/'alpha-native-tour-delivery-r1/VIDEO_CUSTODY_R1.json').read_bytes())
(E/'VIDEO_CUSTODY_PUBLIC_R1.json').write_text(json.dumps({'movies':[{k:x[k] for k in ['file','SHA','bytes','view','frames','fps','duration_seconds','native_time_scale','whole_frame_decode']} for x in v['movies']],'captures':v['captures']},indent=2),encoding='utf8')
print('NATIVE_TOUR_SCALAR_EVIDENCE_PUBLISHED_NO_SOURCE_PACKET')
