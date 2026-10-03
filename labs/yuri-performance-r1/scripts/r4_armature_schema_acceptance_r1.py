"""Append PM-relayed scoped Laptop schema agreement; preserve all frozen artifacts."""
from pathlib import Path
import hashlib,json,base64,subprocess
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'evidence/o1-native-armature-schema-acceptance-r1'
assert not (E/'SCHEMA_ACCEPTANCE_STATUS_R1.json').exists(),'new immutable status revision required'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
full=Path(r'C:/YuriTransfer/outbox/YURI_O1_ARMATURE_TYPED_DRAFT_R7_20261003_8c3c1970ddf6/YURI_O1_ARMATURE_TYPED_DRAFT_R7_20261003.zip')
review=ROOT/'evidence/o1-native-armature-instrumentation-draft-r7/YURI_O1_ARMATURE_R7_RECEIVER_REVIEW.zip'
source=ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
actions=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend')
expected={str(full):'1314692aa05bf2d62c4bb54c8fc794104a395d5adfc68b8e0627dc8cb9b638b0',str(review):'a9be2416bba43892686aabd56467daf13ce10c2017be0751ac3cce8066b71607',str(source):'a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa',str(actions):'6874ec69d5721f385d31edaa06ef0d58c89a543b98bacd961f8f575ff57eef4d'}
for path,digest in expected.items():assert sha(Path(path))==digest
approval=ROOT/'evidence/o1-owned-job-and-acquisition-v5-r1/ACQUISITION_REVIEW_TEMPLATE_NOT_APPROVED.json'
assert json.loads(approval.read_text(encoding='utf8'))['human_large_resource_acquisition_approved'] is False
api='repos/zeroslove-ai/yuri-room-mvp/contents/docs/evidence/root-pm-o1/PM_R7_LAPTOP_CONSUMER_ACCEPTANCE_R1.json?ref=b6e5fe09'
response=json.loads(subprocess.check_output(['gh','api',api]))
raw=base64.b64decode(response['content'])
assert len(raw)==response['size'] and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==response['sha']
envelope=json.loads(raw)
assert envelope['decision']=='ACCEPT_BRANCH_AWARE_SPARSE_SCHEMA_ONLY' and envelope['native_numeric_acceptance']=='NOT_AVAILABLE'
assert envelope['product_promotion'] is False and '[YURI_O1_R7_SCHEMA_CONSUMER_ACCEPTED]' in envelope['read_content']
assert envelope['bytes']==4132 and envelope['sha256']=='bc861458f3e10efa70ec4ae021d190d98d0d2105932c7350f3df0bdf47690a9b'
local=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-native-armature-schema-acceptance-r1')
assert not local.exists();local.mkdir()
(local/'PM_R7_LAPTOP_CONSUMER_ACCEPTANCE_R1.json').write_bytes(raw)
state={
 'status':'SCHEMA_AGREEMENT_RESOLVED_SCOPED_ONLY',
 'decision':'ACCEPT_BRANCH_AWARE_SPARSE_SCHEMA_ONLY',
 'decision_marker':'YURI_O1_R7_SCHEMA_CONSUMER_ACCEPTED',
 'provenance':{'kind':'DIRECT_READ_PINNED_PM_ENVELOPE_CONTAINING_LAPTOP_DECISION','PM_thread_id':'01a0ff8a-5bc8-7541-a876-e39fcc7941bf','message_marker':'ROOT_PM_CONSUMER_DECISION_DURABLE_LOCATION_FIX_R1','envelope_URL':'https://github.com/zeroslove-ai/yuri-room-mvp/blob/b6e5fe09/docs/evidence/root-pm-o1/PM_R7_LAPTOP_CONSUMER_ACCEPTANCE_R1.json','envelope_git_blob_SHA1':response['sha'],'envelope_SHA256':hashlib.sha256(raw).hexdigest(),'envelope_bytes':len(raw),'envelope_git_blob_and_content_verified':True,'Laptop_original_file_SHA256_PM_declared':envelope['sha256'],'Laptop_original_file_bytes_PM_declared':envelope['bytes'],'Laptop_original_file_independently_fetched':False,'embedded_decision_text_UTF8_SHA256':hashlib.sha256(envelope['read_content'].encode('utf8')).hexdigest(),'note':'Exact pinned PM envelope read and decision verified. This proves the envelope receipt, not independent original Laptop-file byte custody. Earlier historical-ref404s were expected; original new Laptop source ref pending.'},
 'source_code_commit':'d02ef857e73d8a2b226422a46d9221287f6d686c',
 'receiver_review_commit':'235690ef548e2162d4808ac7beb6d8000d3177ef',
 'accepted_scope':{'branch_aware_sparse_helpers_DQ':True,'original_slots':57,'second_LBS_computed_vertex_rows':4,'second_LBS_ordered_CSR_rows':40,'zero_mask_vertices_NOT_COMPUTED':[21485,22227,40817],'actual_caller_mask_cache_output_retained':True,'separate_second_modifier_transport':True},
 'mandatory_unchanged_gates':{'vertices':63561,'ordered_CSR_entries':304799,'original_helper_flags':'preserve','zero_helpers_masks':'preserve original order and bits','source_pose_and_world':'actual native only; no reverse-WORLD reconstruction'},
 'remaining':{'full_frozen_ZIP_receiver_custody':'PENDING','full_recipe_actual_file_custody':'PENDING','acquisition_approved':False,'native_build_and_API':'NOT_RUN','native_capture_and_numeric':'NOT_AVAILABLE','installed_compiler_equivalence':'NOT_PROVED','world_numeric_and_full_original_gates':'PENDING','shader_Unity_Player_PBR':'PENDING'},
 'native_numeric_acceptance':False,'product_promotion':False,'R4_appearance_promotion':False,
 'frozen_hashes_verified_now':expected,
 'acquisition_template_unchanged_sha256':sha(approval),
 'artifact_update_policy':'Additive acceptance overlay. Original R6/R7 and receiver schema retain PENDING at their freeze time; none rewritten/replaced.',
 'next':'Native resource/build/capture work only after actual owner approval and applicable gates; schema agreement alone authorizes none.'
}
E.mkdir(parents=True,exist_ok=True)
(E/'SCHEMA_ACCEPTANCE_STATUS_R1.json').write_text(json.dumps(state,indent=2),encoding='utf8')
print(json.dumps({'status':state['status'],'sha256':sha(E/'SCHEMA_ACCEPTANCE_STATUS_R1.json'),'model_action_and_packets':'UNCHANGED','acquisition_approved':False}))
