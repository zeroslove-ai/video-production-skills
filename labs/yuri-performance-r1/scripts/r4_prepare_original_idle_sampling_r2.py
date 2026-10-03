"""Additive file-only fix for collector-live-log hashing; frozen R1 untouched."""
from pathlib import Path
import ast,hashlib,json,tempfile,zipfile
LAB=Path(__file__).resolve().parent.parent;S=LAB/'scripts'
R1=LAB/'evidence/o1-original-idle-sampling-preparation-r1'
E=LAB/'evidence/o1-original-idle-sampling-preparation-r2'
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-original-idle-sampling-r2'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(n,v):
    with (E/n).open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
def main():
    assert not E.exists()
    old=[S/n for n in ['r4_original_idle_sample_r1.py','r4_original_idle_sample_launcher_r1.py','r4_audit_original_idle_sample_r1.py']]
    expected=['1aa569ddb12bc7111daf819a8955b5f77d364a43bab744fc4b5f6b4216bec21f','eca41b95d66dfa175a566f27934a7b6e901aa41f64d3dd7b319eca13f8590279','711e401365518a88888d9574c382bb1fee2756b1238847f9aa5c92881ba51227']
    assert [sha(p) for p in old]==expected
    new=[p.with_name(p.name.replace('_r1.py','_r2.py')) for p in old]
    assert not any(p.exists() for p in new)
    changes={
      'o1-original-idle-sampling-r1':'o1-original-idle-sampling-r2',
      'o1-original-idle-sampling-preparation-r1':'o1-original-idle-sampling-preparation-r2',
      'r4_original_idle_sample_r1.py':'r4_original_idle_sample_r2.py',
      'PM_APPROVAL_ORIGINAL_IDLE_SAMPLE_R1.json':'PM_APPROVAL_ORIGINAL_IDLE_SAMPLE_R2.json',
      'SAMPLING_PROPOSAL_R1.json':'SAMPLING_PROPOSAL_R2.json',
      'FIXED_ROUTE_CONFIG_R1.json':'FIXED_ROUTE_CONFIG_R2.json',
      'IDLE_SAMPLING_RESULT_R1.json':'IDLE_SAMPLING_RESULT_R2.json',
    }
    codes=[]
    for p in old:
        code=p.read_text(encoding='utf8')
        for a,b in changes.items():code=code.replace(a,b)
        codes.append(code)
    live_filter="p.name!='PM_APPROVAL_ORIGINAL_IDLE_SAMPLE_R2.json'"
    stable_filter="p.name not in {'PM_APPROVAL_ORIGINAL_IDLE_SAMPLE_R2.json','fixed-capture.log','OWNED_JOB_RESULT_R1.json','TERMINAL_FILE_CUSTODY_R2.json','IDLE_SAMPLING_RESULT_R2.json'}"
    assert codes[0].count(live_filter)==1
    codes[0]=codes[0].replace(live_filter,stable_filter)
    marker="'exports_saves_aliases':0,'files':"
    added="'exports_saves_aliases':0,'collector_manifest_scope':'CLOSED_COLLECTOR_PAYLOAD_ONLY; live fixed-capture.log excluded; final log and Job receipt custody deferred until owned terminal/drain/close','files':"
    assert marker in codes[0];codes[0]=codes[0].replace(marker,added)
    helper='''def finalize_terminal_custody(out, row):
    # Called after log context exit and owned process/Job cleanup, after Job receipt closes.
    finalized = (row.get('cleanup_owned_handle_signaled') is True and
        row.get('owned_process_signaled_after_job_close') is True and
        row.get('cleanup_job_accounting_before_close', {}).get('active') == 0 and
        row.get('cleanup_job_pids_before_close') == [] and row.get('job_close_success') is True)
    files = {}
    for name in ['OWNED_JOB_RESULT_R1.json','IDLE_SAMPLING_RESULT_R2.json']:
        p = out/name
        if p.exists(): files[name] = {'bytes': p.stat().st_size, 'sha256': sha(p)}
    if finalized and (out/'fixed-capture.log').exists():
        p = out/'fixed-capture.log'
        files[p.name] = {'bytes': p.stat().st_size, 'sha256': sha(p)}
    custody = {'status': 'FINAL_CLOSED_LOG_AND_JOB_RECEIPT' if finalized and 'fixed-capture.log' in files else 'PENDING_OR_UNFINALIZED_NO_LOG_HASH_CLAIM',
        'guard_status_separate': row['guard_status'], 'files': files,
        'self_hash': 'NOT_INCLUDED', 'ordering': 'child signaled; Job drained and closed; log context closed; Job receipt closed; then custody written'}
    with (out/'TERMINAL_FILE_CUSTODY_R2.json').open('x', encoding='utf8') as f: json.dump(custody, f, indent=2)
    return custody


'''
    codes[1]=codes[1].replace('def run():\n',helper+'def run():\n')
    finalize="        finalize_terminal_custody(OUT, row)\n"
    marker2="        print(json.dumps({'guard_status': row['guard_status'], 'data_result': row['data_result'], 'pid': row.get('pid'), 'retry_count': 0}), flush=True)"
    assert codes[1].count(marker2)==1;codes[1]=codes[1].replace(marker2,finalize+marker2)
    audit='''    custody=load('TERMINAL_FILE_CUSTODY_R2.json')
    assert custody['status']=='FINAL_CLOSED_LOG_AND_JOB_RECEIPT'
    assert {'fixed-capture.log','OWNED_JOB_RESULT_R1.json','IDLE_SAMPLING_RESULT_R2.json'} <= set(custody['files'])
    assert 'TERMINAL_FILE_CUSTODY_R2.json' not in custody['files']
    for name,receipt in custody['files'].items():
        p=OUT/name
        assert p.stat().st_size==receipt['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==receipt['sha256']
    assert 'fixed-capture.log' not in result['files'] and 'OWNED_JOB_RESULT_R1.json' not in result['files']
    assert 'TERMINAL_FILE_CUSTODY_R2.json' not in result['files']
'''
    marker3="    for name,row in result['files'].items():"
    assert marker3 in codes[2];codes[2]=codes[2].replace(marker3,audit+marker3)
    # Reverse all additions and fixed path substitutions: original guard/readback checks unchanged.
    reverse=[codes[0].replace(stable_filter,live_filter).replace(added,marker),codes[1].replace(helper,'').replace(finalize,''),codes[2].replace(audit,'')]
    for i in range(3):
        for a,b in reversed(list(changes.items())):reverse[i]=reverse[i].replace(b,a)
        assert reverse[i]==old[i].read_text(encoding='utf8'), ('Unexpected semantic change',i)
        compile(ast.parse(codes[i]),str(new[i]),'exec')
        with new[i].open('x',encoding='utf8',newline='\n') as f:f.write(codes[i])
    # Synthetic file-only regression: footer changes log after collector phase; hash only at terminal.
    ns={'sha':sha,'json':json};exec(compile(ast.parse(helper),'<pure custody helper>','exec'),ns)
    with tempfile.TemporaryDirectory(prefix='yuri-idle-log-r2-') as t:
        d=Path(t);log=d/'fixed-capture.log';log.write_bytes(b'collector output\n');early=sha(log)
        with log.open('ab') as f:f.write(b'Blender quit footer\n')
        (d/'OWNED_JOB_RESULT_R1.json').write_text('{}');(d/'IDLE_SAMPLING_RESULT_R2.json').write_text('{}')
        row={'cleanup_owned_handle_signaled':True,'owned_process_signaled_after_job_close':True,'cleanup_job_accounting_before_close':{'active':0},'cleanup_job_pids_before_close':[],'job_close_success':True,'guard_status':'PASS_OWNED_JOB_EXIT_ZERO_DRAINED'}
        custody=ns['finalize_terminal_custody'](d,row)
        assert custody['files']['fixed-capture.log']['sha256']==sha(log)!=early
        assert 'TERMINAL_FILE_CUSTODY_R2.json' not in custody['files']
    E.mkdir(parents=True)
    proposal=json.loads((R1/'SAMPLING_PROPOSAL_R1.json').read_bytes())
    proposal['inputs'].pop(str(old[0]));proposal['inputs'][str(new[0])]={'bytes':new[0].stat().st_size,'sha256':sha(new[0])}
    proposal['argv'][-1]=str(new[0]);proposal['new_output_directory']=str(OUT)
    proposal.update(status='ADDITIVE_R2_LOG_FINALIZATION_FIX_PREPARATION_ONLY',log_custody='Collector manifest excludes live stdout log and external Job receipt. Launcher final custody records closed log after exact child signal/Job drain+close and closed Job receipt; neither manifest self-hashes.',prior_frozen_packet_sha256=sha(R1/'YURI_ORIGINAL_IDLE_SAMPLING_PREPARATION_R1.zip'))
    assert all(sha(p)==r['sha256'] for p,r in proposal['inputs'].items())
    write('SAMPLING_PROPOSAL_R2.json',proposal)
    config=json.loads((R1/'FIXED_ROUTE_CONFIG_R1.json').read_bytes())
    config.update(status='ADDITIVE_R2_PREPARATION_ONLY_NEW_EXACT_REVIEW_REQUIRED',launcher_sha256=sha(new[1]),collector_sha256=sha(new[0]),proposal_sha256=sha(E/'SAMPLING_PROPOSAL_R2.json'),argv=proposal['argv'],output_directory=str(OUT),receipt_path=str(OUT/'PM_APPROVAL_ORIGINAL_IDLE_SAMPLE_R2.json'),remaining_review='Exact R2 sampling receipt required; frozen R1 receipt/packet cannot authorize R2')
    config['launch_command_argv'][2]=str(new[1]);write('FIXED_ROUTE_CONFIG_R2.json',config)
    receipt=json.loads((R1/'APPROVAL_RECEIPT_TEMPLATE_NOT_APPROVAL_R1.json').read_bytes())
    receipt.update(launcher_sha256=sha(new[1]),collector_sha256=sha(new[0]),config_sha256=sha(E/'FIXED_ROUTE_CONFIG_R2.json'),proposal_sha256=sha(E/'SAMPLING_PROPOSAL_R2.json'),argv=proposal['argv'],note='R2 template false; not installed; no R1 receipt reuse')
    write('APPROVAL_RECEIPT_TEMPLATE_NOT_APPROVAL_R2.json',receipt)
    write('STATIC_VALIDATION_R2.json',{'status':'AST_INPUT_HASH_REVERSE_DIFF_AND_SYNTHETIC_LOG_FOOTER_REGRESSION_PASS','native_runs':0,'guard_scope_resources_LIVE_cleanup_145frame_requirements_unchanged':True,'R1_scripts_SHA_unchanged':[sha(p) for p in old]==expected,'synthetic_closed_log_includes_footer':True,'custody_no_self_hash':True})
    packet=E/'YURI_ORIGINAL_IDLE_SAMPLING_PREPARATION_R2.zip'
    files=new+[Path(__file__)]+[S/n for n in ['r4_appearance_signature.py','native_preservation.py','r4_installed_addon_origin_gate_r2.py']]+list(E.glob('*.json'))
    with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,p.name)
    with zipfile.ZipFile(packet) as z:
        assert z.testzip() is None
        for p in files:assert hashlib.sha256(z.read(p.name)).hexdigest()==sha(p)
    write('PACKET_CUSTODY_R2.json',{'status':'PREPARATION_ONLY_NEW_R2_REVIEW_PENDING','packet':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'members':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in files},'CRC_all_member_SHA_verified':True,'private_numeric_source_data_in_packet':False})
    print(json.dumps({'bytes':packet.stat().st_size,'sha256':sha(packet),'collector_sha256':sha(new[0]),'launcher_sha256':sha(new[1]),'auditor_sha256':sha(new[2])}))
if __name__=='__main__':main()
