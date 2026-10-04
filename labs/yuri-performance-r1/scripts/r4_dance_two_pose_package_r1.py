"""Close one private failed-control packet; never repack historical ZIPs."""
import json,hashlib,zipfile
from pathlib import Path
LAB=Path(__file__).resolve().parents[1];B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'dance-two-pose-delivery-r1';PUB=LAB/'evidence/dance-two-pose-native-r1';PUB.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
V=json.loads((B/'dance-two-pose-off-verify-r1/OFF_READONLY_VERIFY_RECEIPT_R1.json').read_bytes());P=json.loads((O/'OFF_PIXEL_ORACLE_R1.json').read_bytes());Q=json.loads((O/'OBSERVED_NATIVE_QA_FROM_FAILED_JOB_R1.json').read_bytes())
assert P['changed_RGBA_pixels']==0 and V['action_only_library_source_OFF_full_snapshot_equal']
src=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/target-reference/Character_Master_NeckSkin_R4.blend');cand=B/'dance-two-pose-native-r1/Character_R4_DanceStatic03_16_EXPERIMENT_OFF_R1_20261005.blend';lib=B/'dance-two-pose-native-r1/YURI_R4_DANCE_STATIC03_16_ACTIONS_ONLY_R1.blend'
d={'task':'ROOT_PM_DANCE_TWO_POSE_NATIVE_QA_R1','date':'2026-10-05','verdict':'FAIL_HOLD_STATIC_SOURCE_EXPERIMENT_ONLY','source':{'file':str(src),'sha256':sha(src),'bytes':src.stat().st_size},'candidate':{'file':str(cand),'sha256':sha(cand),'bytes':cand.stat().st_size},'action_only_library':{'file':str(lib),'sha256':sha(lib),'bytes':lib.stat().st_size,'actions':2,'objects':0,'meshes':0,'armatures':0},'rows':Q['rows'],'OFF_pixel':P,'OFF_source_Action_library_snapshot_equal':True,'candidate_raw_OFF_texture_path_string_diffs':6,'packed_texture_bytes_identical':all(x['source']['packed']==x['candidate']['packed'] for x in V['image_filepath_SaveAs_differences'].values()),'candidate_other_snapshot_categories_equal':all(V['geometry_rest_material_weights_morph_drivers_category_equality'].values()),'candidate_raw_path_signature_PASS':False,'guard_statuses':{},'static_only':True,'06_14':'PENDING','TierP':0}
for n in ['inspect','native','off-verify']:
 g=B/('o1-dance-two-pose-'+n+'-r1')/'NATIVE_GUARD_RESULT.json';v=json.loads(g.read_bytes());d['guard_statuses'][n]={'status':v['status'] if 'status' in v else v.get('guard_status'),'sha256':sha(g),'terminal_exit_code':v.get('terminal_exit_code'),'active_after_cleanup':v.get('cleanup_job_before_close',{}).get('active')}
# Actual broker status key is inspected explicitly, do not infer successful terminal from exit code alone.
for n,v in d['guard_statuses'].items():
 g=json.loads((B/('o1-dance-two-pose-'+n+'-r1')/'NATIVE_GUARD_RESULT.json').read_bytes())
 if v['status'] is None:v['status']=g.get('overall_status',g.get('result',g.get('verdict')))
(O/'DANCE_TWO_POSE_HANDOFF_MANIFEST_R1.json').write_text(json.dumps(d,indent=2),encoding='utf8')
files={}
def add(p,name):
 assert name not in files;files[name]=p
add(src,'authority/Character_Master_NeckSkin_R4.blend')
for folder in ['dance-two-pose-native-r1','dance-two-pose-off-verify-r1','dance-two-pose-delivery-r1','dance-two-pose-inspect-r1']:
 for p in sorted((B/folder).glob('*')):
  if p.is_file():add(p,folder+'/'+p.name)
for n in ['inspect','native','off-verify']:
 folder=B/('o1-dance-two-pose-'+n+'-r1')
 for p in sorted(folder.rglob('*')):
  if p.is_file():add(p,folder.name+'/'+p.relative_to(folder).as_posix())
for n in ['r4_dance_two_pose_owned_prepare_r1.py','r4_dance_two_pose_inspect_r1.py','r4_dance_two_pose_native_r1.py','r4_dance_two_pose_off_verify_r1.py','r4_dance_two_pose_package_r1.py','r4_appearance_signature.py','r4_appearance_adapter.py','native_preservation.py']:add(LAB/'scripts'/n,'workflow/'+n)
report=LAB/'YURI_DANCE_TWO_POSE_NATIVE_QA_R1_TEMP.md';add(report,'YURI_DANCE_TWO_POSE_NATIVE_QA_R1.md')
index={n:{'sha256':sha(p),'bytes':p.stat().st_size} for n,p in files.items()}
z=B/'YURI_R4_DANCE_STATIC03_16_FAIL_CONTROL_R1_20261005.zip';assert not z.exists()
with zipfile.ZipFile(z,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for n,p in files.items():f.write(p,n)
 f.writestr('FILE_INDEX_SHA256.json',json.dumps(index,indent=2))
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None
 for n,v in index.items():raw=f.read(n);assert len(raw)==v['bytes'] and hashlib.sha256(raw).hexdigest()==v['sha256']
receipt={'packet':str(z),'sha256':sha(z),'bytes':z.stat().st_size,'members':len(index)+1,'indexed_members':len(index),'all_CRC_SHA_size_verified':True,'closed_once':True,'verdict':d['verdict']}
(PUB/'PRIVATE_PACKET_RECEIPT_R1.json').write_text(json.dumps(receipt,indent=2),encoding='utf8');(PUB/'DANCE_TWO_POSE_SCALAR_QA_R1.json').write_text(json.dumps(d,indent=2),encoding='utf8');(PUB/'YURI_DANCE_TWO_POSE_NATIVE_QA_R1.md').write_bytes(report.read_bytes())
print(json.dumps(receipt,indent=2))
