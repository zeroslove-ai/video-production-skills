"""Freeze matching final guard/verifier/argv and actual same-tool probes; no Blender."""
from pathlib import Path
import ast,hashlib,importlib.util,json,shutil,zipfile
LAB=Path(__file__).resolve().parents[1]
E=LAB/'evidence/o1-readonly-source-job-review-r4'
GUARD=LAB/'scripts/r4_readonly_source_job_guard_r4.py'
VERIFIER=LAB/'scripts/r4_readonly_recipe_verifier_r4.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('final_guard',GUARD);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
assert not E.exists();E.mkdir()
probe=json.loads((g.OUT/'PROBE_MANIFEST.json').read_bytes())
assert probe['guard_sha256']==sha(GUARD) and sha(VERIFIER)==g.VERIFIER_SHA
assert len(probe['cases'])==2 and probe['Blender_launches']==0
for r in probe['cases']:
    assert r['status']=='PASS' and r['total_job_processes']==1 and r['limit_terminated_processes']==0
    assert r['active_after_exit']==0 and r['final_job_pids']==[] and r['owned_process_signaled_after_job_close']
    assert r['inputs_before']==r['inputs_after'] and r['job_limit_readback_verified']
    for s in r['resources_samples'][1:]:
        assert s['associated_job_pids'] in ([r['pid']],[]) and s['accounting_before_PID_query']['active']<=1 and s['accounting_after_identity_query']['active']<=1
ast.parse(GUARD.read_text());ast.parse(VERIFIER.read_text())
assert not (g.OUT/'PM_REVIEW_SOURCE_READ_APPROVED_R4.json').exists() and not (g.OUT/'source-identity.json').exists()
FROZEN=E/'frozen';FROZEN.mkdir()
for p in [GUARD,VERIFIER,*g.OUT.glob('*.json'),*g.OUT.glob('*.log')]:shutil.copyfile(p,FROZEN/p.name)
manifest={'status':'FINAL_FIXED_SOURCE_READ_TOOL_PREPARED_NOT_APPROVED_BLENDER_NOT_RUN','scope':'INSTALLED_BLENDER_SOURCE_DATA_READ_ONLY','guard_sha256':sha(GUARD),'verifier_sha256':sha(VERIFIER),'blender_sha256':g.BLENDER_SHA,'python_sha256':g.PYTHON_SHA,'same_final_guard_probe_manifest_sha256':sha(g.OUT/'PROBE_MANIFEST.json'),'argv':g.source_argv(),'source_output_path':str(g.OUT/'source-identity.json'),'verifier_output_path_matches':True,'run_command_AFTER_review_only':[str(g.PYTHON),str(GUARD),'--run-reviewed-source-read'],'approval_receipt_required_but_absent':str(g.OUT/'PM_REVIEW_SOURCE_READ_APPROVED_R4.json'),'PM_reviewed_exact_final_guard_verifier_argv_and_same_guard_probes':False,'human_large_resource_acquisition_approved':False,'custom_native_build_trace_capture_approved':False,'source_action_recipe_prepost_hashes':g.hashes(),'limits':{'creation_flags':12,'creation_sequence':'DETACHED_PROCESS|CREATE_SUSPENDED -> assign own unnamed Job -> identity/accounting -> ResumeThread','two_core_affinity_mask':3,'process_and_job_RAM_bytes':8*1024**3,'active_process_limit':1,'source_watchdog_seconds':120,'min_free_RAM_bytes':12*1024**3,'min_free_C_bytes':100*1024**3,'kill_on_close':True,'strict_per_sample_PID_and_actual_accounting':True},'probes':[{'case':r['case'],'pid':r['pid'],'exit_code':r['exit_code'],'total':r['total_job_processes'],'active_after':r['active_after_exit'],'final_job_pids':r['final_job_pids'],'guard_sha256':r['guard_sha256']} for r in probe['cases']],'Blender_launches':0,'live_source_identity':'NOT_RUN','native_numeric_acceptance':False,'network_security_boundary':'No download/network operations in fixed scripts; Windows Job is not a network sandbox','frozen_files':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(FROZEN.iterdir())}}
(E/'FINAL_REVIEW_MANIFEST_R4.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
(E/'FINAL_SOURCE_JOB_REVIEW_R4.md').write_text(f'''# Final installed source-read Job review R4

Prepared for PM review only. Blender launches0; source identity NOT_RUN. No PM approval receipt was created. Large acquisition/native build/trace/capture false. V5/R2/frozen R1/R3 and failed attempts remain unchanged.

The same final guard SHA256 `{sha(GUARD)}` ran the actual normal and timeout probes. Normal PID{probe['cases'][0]['pid']} exits0; timeout PID{probe['cases'][1]['pid']} exits88. Both report lifetime TotalProcesses1, LimitTerminated0, final Active0, empty Job PID list and signaled process handles. Every sampled actual accounting/PID identity is checked against the owned root. Executable path, creation FILETIME and IsProcessInJob are verified. Strict limits are read back from Windows: affinity3, 8GiB process/job, active limit1. Resource floors and input pre/post hashes pass. No console host appears with DETACHED_PROCESS.

Verifier SHA256 `{sha(VERIFIER)}`; exact same-final-tool probe manifest SHA256 `{sha(g.OUT/'PROBE_MANIFEST.json')}`. Fixed source argv and matching output path are in FINAL_REVIEW_MANIFEST_R4.json. The disable-autoexec flag is before the source filename. Verifier has no imported mutable local helpers; reads full original57 rest f32/body world/63561 positions/all304799 ordered CSR/group58/mask52, first mismatch fails without repair. No action/pose/update/render/export/save calls.

The separate approval gate requires exact guard/verifier/executable/probe hashes, fixed argv, scoped PM review true and large/native approvals false. That gate is absent. There are no arbitrary executable/argv/limit routes. Default CLI is dry. Required resources: free RAM>=12GiB/free C>=100GiB before and each monitoring sample, two-core affinity and Blender threads2, 120sec source watchdog, suspended assignment before resume, kill-on-close. Source/executable/verifier/guard hashes are checked; source/actions/recipe are checked before and after. Fixed output is outside product repos. Jobs are process/resource containment, not a network security sandbox.

Frozen ZIP retains exact bytes despite Git line-ending conversion. Python probes demonstrate the final guard mechanism only; installed Blender compatibility/live source identity remain unrun. Next bounded task: PM review of this exact final packet; no Blender launch until separately authorized.
''',encoding='utf8')
packet=E/'YURI_O1_FINAL_SOURCE_JOB_REVIEW_R4.zip'
with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(E.rglob('*')):
        if p.is_file() and p!=packet:z.write(p,p.relative_to(E).as_posix())
with zipfile.ZipFile(packet) as z:assert z.testzip() is None
receipt={'status':'FINAL_PACKET_FROZEN_REVIEW_ONLY','zip':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'manifest_sha256':sha(E/'FINAL_REVIEW_MANIFEST_R4.json'),'guard_sha256':sha(GUARD),'verifier_sha256':sha(VERIFIER),'same_guard_probe_manifest_sha256':sha(g.OUT/'PROBE_MANIFEST.json')}
(E/'PACKET_RECEIPT_R4.json').write_text(json.dumps(receipt,indent=2),encoding='utf8');print(json.dumps(receipt))
