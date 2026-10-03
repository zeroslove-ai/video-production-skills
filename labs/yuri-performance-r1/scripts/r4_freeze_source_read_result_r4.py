"""Freeze the one authorized R4 source read without repair/restart or native claims."""
from pathlib import Path
import hashlib,json,shutil,zipfile
LAB=Path(__file__).resolve().parents[1]
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-readonly-source-job-r4')
E=LAB/'evidence/o1-readonly-source-identity-result-r4'
GUARD=LAB/'scripts/r4_readonly_source_job_guard_r4.py'
VERIFIER=LAB/'scripts/r4_readonly_recipe_verifier_r4.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert not E.exists();E.mkdir()
job=json.loads((OUT/'source-read.json').read_bytes());identity=json.loads((OUT/'source-identity.json').read_bytes())
assert sha(GUARD)==job['guard_sha256']=='121f4cadf7eeac0f7508d2f253da3b8533a0b6422b075fb6e249596ef315d4f6'
assert sha(VERIFIER)=='65f06067bfc117e4290cc9520d45db0df2952dd03da9dd063e6a48c1704f54ec'
assert job['status']=='FAIL' and job['error']=="KeyError('executable')" and job['inputs_before']==job['inputs_after']
assert identity['status']=='LIVE_ORIGINAL_FULL_RECIPE_BYTE_IDENTICAL'
assert sha(OUT/'PM_REVIEW_SOURCE_READ_APPROVED_R4.json')=='30b853e5cd97cebc0706e0f1b3d4e701fde9a56d6cd6ee7f6d388dc668e457d8'
samples=job['resources_samples'][1:];last=samples[-1];terminal=last['PID_identities'][0]
assert terminal['pid']==job['pid'] and terminal['creation_FILETIME']==job['creation_FILETIME']
assert terminal['image_error']==31 and terminal['exit_code_query']==0 and terminal['exit_FILETIME']>terminal['creation_FILETIME']
assert last['accounting_after_identity_query']['active']==0 and job['owned_process_signaled_after_job_close']
for s in samples:
    assert s['accounting_before_PID_query']['active']<=1 and s['accounting_before_PID_query']['total']==1
    assert s['associated_job_pids'] in ([job['pid']],[])
files=['PM_REVIEW_SOURCE_READ_APPROVED_R4.json','source-read.json','source-read.log','source-identity.json']
for name in files:shutil.copyfile(OUT/name,E/name)
shutil.copyfile(GUARD,E/GUARD.name);shutil.copyfile(VERIFIER,E/VERIFIER.name)
result={'status':'SOURCE_DATA_VERIFIER_PASS_GUARD_FAIL_TERMINAL_IMAGE_QUERY_RACE','scope':'FULL_ORIGINAL_SOURCE_RECIPE_DATA_IDENTITY_ONLY','actual_attempts':1,'restarted':False,'repair_or_script_change_for_approval':False,'source_verifier':identity,'guard_status':'FAIL','guard_error':job['error'],'owned_child_pid':job['pid'],'owned_child_creation_FILETIME':job['creation_FILETIME'],'live_authoritative_identity':samples[0]['PID_identities'][0],'terminal_identity':terminal,'terminal_accounting_after_identity_query':last['accounting_after_identity_query'],'final_PID_list_in_guard_receipt':'NOT_CAPTURED_AFTER_ASSERTION; no fabrication','owned_handle_signaled_after_job_close':job['owned_process_signaled_after_job_close'],'wall_seconds':job['wall_seconds'],'resource_samples':len(samples),'immutable_input_hashes_before_after':job['inputs_after'],'approval_receipt_sha256':sha(OUT/'PM_REVIEW_SOURCE_READ_APPROVED_R4.json'),'startup_addon_side_effect':'Existing user preference add-ons loaded despite --disable-autoexec. Log shows BlenderMCP registered/unregistered, MPFB initialization, Higgsfield SDK account balance lookup request failedHTTP400. No generation/render/export requested; unintended account lookup means startup isolation is not accepted.','whole_guard_or_isolated_job_acceptance':False,'native_numeric_acceptance':False,'PBR_Unity_canonical_appearance_promotion':False,'human_large_resource_acquisition_approved':False,'custom_native_build_trace_capture_approved':False,'next_bounded_review':'PM review failed guard receipt and actual data PASS; separately reviewed shutdown-race-safe, startup-addon-isolated guard required before any new run','files':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(E.iterdir())}}
(E/'SOURCE_READ_RESULT_R4.json').write_text(json.dumps(result,indent=2),encoding='utf8')
packet=E/'YURI_O1_SOURCE_READ_RESULT_R4.zip'
with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(E.iterdir()):
        if p.is_file() and p!=packet:z.write(p,p.name)
with zipfile.ZipFile(packet) as z:assert z.testzip() is None
receipt={'status':result['status'],'zip':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'result_manifest_sha256':sha(E/'SOURCE_READ_RESULT_R4.json')}
(E/'PACKET_RECEIPT_R4.json').write_text(json.dumps(receipt,indent=2),encoding='utf8');print(json.dumps(receipt))
