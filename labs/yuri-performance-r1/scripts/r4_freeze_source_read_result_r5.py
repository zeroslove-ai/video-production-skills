"""Freeze exact one-shot R5 result; no guard repair, restart or promotion."""
from pathlib import Path
import hashlib,json,shutil,zipfile
LAB=Path(__file__).resolve().parents[1]
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-readonly-source-job-r5-final')
E=LAB/'evidence/o1-readonly-source-identity-result-r5'
GUARD=LAB/'scripts/r4_readonly_source_job_guard_r5.py';VERIFIER=LAB/'scripts/r4_readonly_recipe_verifier_r5.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert not E.exists();E.mkdir()
r=json.loads((OUT/'source-read.json').read_bytes());identity=json.loads((OUT/'source-identity.json').read_bytes());log=(OUT/'source-read.log').read_text()
assert sha(GUARD)==r['guard_sha256']=='c6912b0378d9b1f626de33b4f819efb898d49432e035576e240764559fe8566c'
assert sha(VERIFIER)=='822e032882b9f4c5f0df012a60083d72abe217679c5f2e881c7a4af241866b9c'
assert sha(OUT/'PM_REVIEW_SOURCE_READ_APPROVED_R5.json')=='f9d7ab8df572869833288c9ab371aad24bf94b3184d84809e96239ee6c6426d4'
assert r['status']=='FAIL' and r['error']=="AssertionError('missing image on LIVE owned process is failure')"
assert r['inputs_before']==r['inputs_after'] and identity['status']=='LIVE_ORIGINAL_FULL_RECIPE_BYTE_IDENTICAL'
assert r['cleanup_owned_handle_terminal'] and r['cleanup_owned_handle_exit_code']==0
assert r['cleanup_terminal_job_accounting']=={'active':0,'total':1,'limit_terminated':0} and r['cleanup_final_job_pids']==[]
last=r['resources_samples'][-1];end=last['PID_identities'][0]
assert end['pid']==r['pid'] and end['creation_FILETIME']==r['creation_FILETIME'] and end['image_error']==5
assert end['exit_code_query']==0 and end['exit_FILETIME']>end['creation_FILETIME']
assert last['owned_handle_terminal_after_missing_image'] is False
markers={name:name.lower() in log.lower() for name in ['BlenderMCP','MPFB','Higgsfield','account lookup','get_balance','Request failed']}
assert not any(markers.values())
for name in ['PM_REVIEW_SOURCE_READ_APPROVED_R5.json','source-read.json','source-read.log','source-identity.json']:shutil.copyfile(OUT/name,E/name)
shutil.copyfile(GUARD,E/GUARD.name);shutil.copyfile(VERIFIER,E/VERIFIER.name)
result={'status':'R5_SOURCE_VERIFIER_PASS_GUARD_FAIL_EXIT_TEARDOWN_IMAGE_QUERY','scope':'FULL_ORIGINAL_SOURCE_RECIPE_DATA_IDENTITY_ONLY','source_attempts':1,'restarted':False,'source_verifier':identity,'guard_status':'FAIL','guard_error':r['error'],'owned_provenance':{k:r[k] for k in ['pid','creation_FILETIME','native_process_handle','native_job_handle','guard_parent_pid']},'last_identity_snapshot':end,'last_observation_owned_handle_signaled':last['owned_handle_terminal_after_missing_image'],'actual_terminal_cleanup':{k:r[k] for k in ['cleanup_owned_handle_terminal','cleanup_owned_handle_exit_code','cleanup_terminal_job_accounting','cleanup_final_job_pids','failure_cleanup_terminated_owned_job','owned_process_signaled_after_job_close']},'immutable_prepost_input_SHA':r['inputs_after'],'wall_seconds':r['wall_seconds'],'resource_sample_count':len(r['resources_samples'])-1,'startup_stdout_markers':markers,'startup_scope_limit':'Previous addon/account lookup markers absent in actual source stdout; fixed factory/offline argv used. No packet-level network trace or exhaustive addon inventory; do not claim an OS network sandbox.','whole_guard_acceptance':False,'native_numeric_acceptance':False,'PBR_Unity_primary_or_appearance_promotion':False,'human_large_resource_acquisition_approved':False,'custom_native_build_trace_capture_approved':False,'approval_receipt_sha256':sha(OUT/'PM_REVIEW_SOURCE_READ_APPROVED_R5.json'),'next_bounded_review':'PM review exact failed R5 guard and terminal cleanup; no rerun or guard mutation under this approval','files':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(E.iterdir())}}
(E/'SOURCE_READ_RESULT_R5.json').write_text(json.dumps(result,indent=2),encoding='utf8')
(E/'SOURCE_READ_LIMITATIONS_R5.md').write_text(f'''# R5 one-shot source-data result and guard failure

Exact scoped PM receipt SHA `{sha(OUT/'PM_REVIEW_SOURCE_READ_APPROVED_R5.json')}` was copied byte-for-byte and checked against guard/verifier/executable/argv/probe/help SHA. The approved tool ran once unchanged. Owned live child PID{r['pid']}, creation FILETIME{r['creation_FILETIME']}, process handle{r['native_process_handle']}/Job handle{r['native_job_handle']} in guard PID{r['guard_parent_pid']} were emitted as OWNED_CHILD_RESUMED and recorded. Handles are meaningful in that guard process only.

Read-only verifier reports original57rest/world/63561 basis positions/all304799 ordered CSR/groups58/mask52/37310 zero weights byte-identical. Original source/actions/recipe pre/post hashes are unchanged. Factory/offline/disable-autoexec source startup stdout contains none of the former BlenderMCP/MPFB/Higgsfield/account lookup markers; no render/export/save/Action/pose operations were requested. This stdout check is not an exhaustive addon inventory or packet-level network trace.

Whole guard remains FAIL. Last identity query reports image_error5, matching original creation FILETIME, exit FILETIME{end['exit_FILETIME']} and queried exit code0, while the actual owned process handle is not yet signaled. R5's exact safety rule therefore rejects the missing image; it was not weakened or retried. Finally cleanup requested owned Job termination and then captured the authoritative handle signaled/exit0, Job Active0/Total1/LimitTerminated0 and empty PID list before closing handles. The guard is not retroactively PASS. Raw snapshots are sequential and preserve the exit-teardown observation gap.

R4 failed tool/log/result, R5 reviewed tool/probes and all prior attempts remain immutable. Original GUI129152 remains present; no product repo or preferences edits. Source-data identity alone does not imply rendered fidelity, native arithmetic, Unity/PBR or PRIMARY/appearance promotion. Large acquisition/custom native approval remain false. Next bounded task is PM review of this result and, if authorized separately, a new shutdown-observation tool; no restart under R5 approval.
''',encoding='utf8')
packet=E/'YURI_O1_SOURCE_READ_RESULT_R5.zip'
with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(E.iterdir()):
        if p.is_file() and p!=packet:z.write(p,p.name)
with zipfile.ZipFile(packet) as z:assert z.testzip() is None
receipt={'status':result['status'],'zip':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'result_manifest_sha256':sha(E/'SOURCE_READ_RESULT_R5.json')}
(E/'PACKET_RECEIPT_R5.json').write_text(json.dumps(receipt,indent=2),encoding='utf8');print(json.dumps(receipt))
