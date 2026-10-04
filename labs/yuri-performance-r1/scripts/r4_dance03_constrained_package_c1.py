"""Close ONE constrained03 FAIL packet with original source authority and diagnostic limits."""
import json,hashlib,zipfile
from pathlib import Path
LAB=Path(__file__).resolve().parents[1];B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');R=B/'dance03-constrained-native-c1';O=B/'dance03-constrained-delivery-c1';PUB=LAB/'evidence/dance03-constrained-native-c1';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
d=json.loads((R/'DANCE03_CONSTRAINED_PRIVATE_MANIFEST_C1.json').read_bytes());loc=json.loads((B/'dance03-constrained-readonly-c1b/READONLY_LOCALIZATION_OFF_PRIVATE_C1.json').read_bytes());pixel=json.loads((O/'OFF_PIXEL_ORACLE_C1.json').read_bytes())
assert loc['candidate_raw_reopened_OFF_snapshot_equal'] and pixel['changed_RGBA_pixels']==0
public={k:d[k] for k in ['task','source','source_SHA','candidate','candidate_SHA','original78Actions_preserved','action_names','action_only_library','rows','floor_z_m','views','collision_scope','limits']}
public.update(date='2026-10-05',verdict='FAIL_HOLD_ONE_CONSTRAINED03_CANDIDATE_METHOD_STOP',source_action_ON_OFF_full_snapshot_equal=True,raw_candidate_reopened_OFF_equal=True,raw_texture_filepath_differences=[],OFF_pixel=pixel,left_arm_residual_dominant_groups=loc['left_arm_contact_dominant_groups'],left_arm_residual_bounds_m=loc['left_arm_contact_bounds_world_m'],edge_extremes=loc['edge_extremes'],single_constraint_scalar={k:d['native_constraint_private'][k] for k in ['native_two_bone_lengths_m','target_distance_m','actual_wrist_target_error_m','requested_upper_axial_twist_degrees','applied_upper_axial_twist_degrees','upper_axial_twist_bound_degrees','requested_elbow_bend_degrees','applied_elbow_bend_degrees','elbow_bend_bound_degrees','existing_leg_source','existing_leg_delta_degrees','right_arm_previous03_quaternions_exact','one_candidate_no_sweep']},TierP=0)
public['source_bytes']=Path(d['source']).stat().st_size;public['candidate_bytes']=Path(d['candidate']).stat().st_size
guards=['o1-dance03-existing-inspect-c1','o1-dance03-constrained-native-c1','o1-dance03-constrained-readonly-c1','o1-dance03-constrained-readonly-c1b']
public['guards']={}
for n in guards:
 p=B/n/'NATIVE_GUARD_RESULT.json';g=json.loads(p.read_bytes());public['guards'][n]={'status':g['guard_status'],'sha256':sha(p),'exit':g['terminal_exit_code'],'cleanup_active':g['cleanup_job_before_close']['active']};assert g['cleanup_job_before_close']['active']==0
old=B/'YURI_R4_DANCE_STATIC03_16_FAIL_CONTROL_R1_20261005.zip';assert sha(old)=='6b8d18971087eb200bfd85235c3670cf1d27f1e46757013d639059f1a0c421dd';public['prior_FAIL_packet_unchanged_SHA']=sha(old)
(O/'CONSTRAINED03_HANDOFF_MANIFEST_C1.json').write_text(json.dumps(public,indent=2),encoding='utf8')
files={}
def add(p,n):assert n not in files;files[n]=p
add(Path(d['source']),'authority/Character_Master_NeckSkin_R4.blend')
for folder in ['dance03-existing-solutions-inspect-c1','dance03-constrained-native-c1','dance03-constrained-readonly-c1','dance03-constrained-readonly-c1b','dance03-constrained-delivery-c1',*guards]:
 for p in sorted((B/folder).rglob('*')):
  if p.is_file():add(p,folder+'/'+p.relative_to(B/folder).as_posix())
for n in ['03_front.png','03_left.png']:add(B/'dance-two-pose-native-r1'/n,'prior_FAIL03/'+n)
add(B/'dance-two-pose-native-r1/YURI_R4_DANCE_STATIC03_16_ACTIONS_ONLY_R1.blend','prior_FAIL03/ORIGINAL_R1_RIGHT_ARM_REFERENCE_ACTIONS.blend')
for n in ['r4_dance03_owned_prepare_c1.py','r4_dance03_existing_solutions_inspect_c1.py','r4_dance03_constrained_pose_fragment_c1.py','r4_dance03_constrained_native_c1.py','r4_dance03_constrained_readonly_c1.py','r4_dance03_constrained_readonly_c1b.py','r4_dance03_constrained_package_c1.py','r4_appearance_signature.py','r4_appearance_adapter.py','native_preservation.py']:add(LAB/'scripts'/n,'workflow/'+n)
add(PUB/'YURI_DANCE03_CONSTRAINED_NATIVE_QA_C1.md','YURI_DANCE03_CONSTRAINED_NATIVE_QA_C1.md')
index={n:{'sha256':sha(p),'bytes':p.stat().st_size} for n,p in files.items()}
z=B/'YURI_R4_DANCE03_CONSTRAINED_FAIL_CONTROL_C1_20261005.zip';assert not z.exists()
with zipfile.ZipFile(z,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for n,p in files.items():f.write(p,n)
 f.writestr('FILE_INDEX_SHA256.json',json.dumps(index,indent=2))
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None
 for n,v in index.items():raw=f.read(n);assert len(raw)==v['bytes'] and hashlib.sha256(raw).hexdigest()==v['sha256']
receipt={'packet':str(z),'sha256':sha(z),'bytes':z.stat().st_size,'members':len(index)+1,'indexed_members':len(index),'CRC_SHA_size_all_verified':True,'closed_once':True,'verdict':public['verdict']}
(PUB/'CONSTRAINED03_SCALAR_CUSTODY_QA_C1.json').write_text(json.dumps(public,indent=2),encoding='utf8');(PUB/'PRIVATE_PACKET_RECEIPT_C1.json').write_text(json.dumps(receipt,indent=2),encoding='utf8')
print(json.dumps(receipt,indent=2))
