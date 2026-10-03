"""Freeze actual small-read guard/probe evidence; never execute Blender."""
from pathlib import Path
import hashlib,json,zipfile,shutil,importlib.util,ast
LAB=Path(__file__).resolve().parents[1]
E=LAB/'evidence/o1-readonly-recipe-guard-r1'
GUARD=LAB/'scripts/r4_readonly_owned_job_guard_r1.py'
VERIFIER=LAB/'scripts/r4_readonly_recipe_verifier_r1.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('guard',GUARD);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
assert not (E/'REVIEW_MANIFEST.json').exists()
probe=json.loads((g.OUT/'PROBE_MANIFEST.json').read_bytes())
assert probe['status']=='PASS_NORMAL_TIMEOUT_ZERO_CHILDREN' and probe['guard_sha256']==sha(GUARD)
for case in probe['cases']:
    assert case['status']=='PASS' and case['active_after_exit']==0 and case['final_job_pids']==[]
    assert case['job_limit_readback_verified'] and case['owned_process_signaled_after_job_close']
ast.parse(GUARD.read_text());ast.parse(VERIFIER.read_text())
FROZEN=E/'frozen';FROZEN.mkdir()
for source in [GUARD,VERIFIER,*g.OUT.glob('*.json'),*g.OUT.glob('*.log')]:
    shutil.copyfile(source,FROZEN/source.name)
assert not (g.OUT/'PM_REVIEW_SOURCE_READ_APPROVED.json').exists()
review={'status':'PREPARED_NOT_APPROVED_BLENDER_NOT_RUN','scope':'INSTALLED_BLENDER_SOURCE_DATA_READ_ONLY',
 'guard_sha256':sha(GUARD),'verifier_sha256':sha(VERIFIER),'blender_sha256':g.BLENDER_SHA,
 'python_sha256':g.PYTHON_SHA,'probe_manifest_sha256':sha(g.OUT/'PROBE_MANIFEST.json'),
 'argv':g.source_argv(),'output_root':str(g.OUT),'source_identity_output':str(g.OUT/'source-identity.json'),
 'approval_receipt_required_but_absent':str(g.OUT/'PM_REVIEW_SOURCE_READ_APPROVED.json'),
 'PM_reviewed_frozen_guard_verifier_argv_and_actual_probe_receipts':False,
 'PM_reviewed_raw_job_accounting_and_PID_list_anomaly':False,
 'human_large_resource_acquisition_approved':False,'custom_native_build_trace_capture_approved':False,
 'source_action_recipe_current_sha256':g.hashes(),
 'limits':{'CPU_affinity':3,'Blender_threads':2,'process_and_job_RAM_bytes':8*1024**3,'active_process_limit':1,'source_watchdog_seconds':120,'min_free_RAM_bytes':12*1024**3,'min_free_C_bytes':100*1024**3,'kill_on_close':True},
 'probes':[{'case':r['case'],'pid':r['pid'],'exit_code':r['exit_code'],'active_after':r['active_after_exit'],'final_job_pids':r['final_job_pids'],'total_processes':r['total_job_processes'],'limit_terminated':r['limit_terminated_processes']} for r in probe['cases']],
 'accounting_caveat':'Raw total association count and transient additional PID observations retained. Cause/admission status unresolved. Readback verifies configured limit1; no claim of identified extra executable. PM must review before source route.',
 'no_network_routes':'Fixed scripts have no network/download code. Job object is not a network security sandbox.',
 'Blender_launches':0,'live_source_identity':'NOT_RUN','native_numeric_acceptance':False,
 'frozen_files':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(FROZEN.iterdir())}}
(E/'REVIEW_MANIFEST.json').write_text(json.dumps(review,indent=2),encoding='utf8')
packet=E/'YURI_O1_READONLY_GUARD_REVIEW_R1.zip'
with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(E.rglob('*')):
        if p.is_file() and p!=packet:z.write(p,p.relative_to(E).as_posix())
with zipfile.ZipFile(packet) as z:assert z.testzip() is None
receipt={'zip':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'review_manifest_sha256':sha(E/'REVIEW_MANIFEST.json'),'status':'FROZEN_REVIEW_ONLY_NOT_APPROVED'}
(E/'PACKET_RECEIPT.json').write_text(json.dumps(receipt,indent=2),encoding='utf8')
print(json.dumps(receipt))
