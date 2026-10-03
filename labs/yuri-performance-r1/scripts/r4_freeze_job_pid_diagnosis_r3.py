"""Freeze bounded console-helper diagnosis, detached probes and exact-byte custody."""
from pathlib import Path
import hashlib,json,shutil,zipfile
LAB=Path(__file__).resolve().parents[1]
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
E=LAB/'evidence/o1-readonly-job-pid-diagnosis-r3-final'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert not E.exists();E.mkdir()
findings=[]
for label,folder,script in [('console-r2','o1-readonly-recipe-guard-diagnose-r2','r4_readonly_owned_job_guard_diagnose_r2.py'),('detached-r3','o1-readonly-recipe-guard-detached-r3','r4_readonly_owned_job_guard_detached_r3.py')]:
    source=BASE/folder;target=E/label;target.mkdir()
    for p in source.iterdir():
        assert p.suffix in ('.json','.log');shutil.copyfile(p,target/p.name)
    guard=LAB/'scripts'/script;shutil.copyfile(guard,target/script)
    q=json.loads((source/'PROBE_MANIFEST.json').read_bytes());assert q['guard_sha256']==sha(guard)
    for r in q['cases']:
        assert r['status']=='PASS' and r['active_after_exit']==0 and r['final_job_pids']==[]
        assert r['inputs_before']==r['inputs_after'] and r['job_limit_readback_verified']
        extra=[i for s in r['resources_samples'] for i in s.get('PID_identities',[]) if i['pid']!=r['pid']]
        unique={i['pid']:i for i in extra}
        if label=='console-r2':
            assert r['total_job_processes']==2 and len(unique)==1
            for i in unique.values():
                assert i['executable'].lower()==r'c:\windows\system32\conhost.exe' and i['parent_pid']==r['pid'] and i['in_this_owned_job'] is True
                assert i['creation_FILETIME']>r['creation_FILETIME']
                assert any(v['pid']==i['pid'] and v['exit_code_query']==259 for v in extra)
            assert any(s.get('accounting_before_PID_query',{}).get('active')==2 for s in r['resources_samples'])
        else:
            assert r['total_job_processes']==1 and r['limit_terminated_processes']==0 and not extra
            for s in r['resources_samples'][1:]:
                assert s['accounting_before_PID_query']['active']<=1 and s['accounting_after_identity_query']['active']<=1
                assert s['associated_job_pids'] in ([r['pid']],[])
        findings.append({'variant':label,'case':r['case'],'root_pid':r['pid'],'root_creation_FILETIME':r['creation_FILETIME'],'extra_identities':list(unique.values()),'total_job_processes':r['total_job_processes'],'limit_terminated_processes':r['limit_terminated_processes'],'active_after_exit':r['active_after_exit'],'exit_code':r['exit_code'],'samples':len(r['resources_samples'])-1,'native_layout':r['native_layout'],'guard_sha256':sha(guard),'actual_probe_receipt_sha256':sha(source/(r['case']+'.json'))})
manifest={'status':'CONHOST_IDENTITY_CONFIRMED_DETACHED_FIXED_PROBES_SINGLE_PROCESS_AND_ZERO_DRAIN','scope':'FIXED_HARMLESS_PYTHON_PROBE_CAUSAL_DIAGNOSIS_ONLY','findings':findings,'change':'CREATE_SUSPENDED|CREATE_NO_WINDOW -> CREATE_SUSPENDED|DETACHED_PROCESS; fixed probe argv/limits/resource floors unchanged between R2 and R3','limits_relaxed':False,'Blender_launches':0,'source_read':'NOT_RUN','approval_receipt_created':False,'human_large_resource_acquisition_approved':False,'native_custom_capture_approved':False,'semantic_limit':'No claim of a general Windows console-host limit exemption; actual conhost identity/Active2 is measured. One flag A/B removes the helper in this environment. R3 has no Blender execution route.','files':{p.relative_to(E).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(E.rglob('*')) if p.is_file()}}
(E/'CAUSAL_FINDINGS_R3.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
packet=E/'YURI_O1_JOB_PID_DIAGNOSIS_R3.zip'
with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(E.rglob('*')):
        if p.is_file() and p!=packet:z.write(p,p.relative_to(E).as_posix())
with zipfile.ZipFile(packet) as z:assert z.testzip() is None
receipt={'zip':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'findings_sha256':sha(E/'CAUSAL_FINDINGS_R3.json'),'status':'REVIEW_ONLY_BLENDER_NOT_RUN'}
(E/'PACKET_RECEIPT_R3.json').write_text(json.dumps(receipt,indent=2),encoding='utf8');print(json.dumps(receipt))
