"""Independent CPU file-only freeze of the one failed approved invocation. No retry."""
from pathlib import Path
import hashlib, json, shutil, zipfile

LAB=Path(__file__).resolve().parent.parent
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-exact-source-local-stage-capture-r1'
E=LAB/'evidence/o1-exact-local-stage-capture-result-r1'

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def write(p,v):
    with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2)

def main():
    assert not E.exists(), 'Frozen failure cannot be overwritten'
    raw=[OUT/n for n in ['PM_APPROVAL_EXACT_LOCAL_CAPTURE_R1.json','fixed-capture.log','OWNED_JOB_RESULT_R1.json']]
    receipt=json.loads(raw[0].read_bytes());row=json.loads(raw[2].read_bytes())
    assert sha(raw[0])=='cb1acd61177ad0130e29b24876cced75b220f661fe33d2be43e3f6aca0baeed5'
    assert row['pid']==114608 and row['guard_status']=='FAIL' and row['data_result']=='NOT_READ'
    assert row['cleanup_owned_handle_signaled'] is True and row['cleanup_owned_handle_exit_code']==93
    assert row['cleanup_job_accounting_before_close']['active']==0 and row['cleanup_job_pids_before_close']==[]
    assert row['cleanup_job_accounting_before_close']['total']==1 and row['cleanup_job_accounting_before_close']['limit_terminated']==0
    assert row['owned_process_signaled_after_job_close'] is True and row['cleanup_errors']==[]
    assert not list(OUT.glob('*.npz')) and not (OUT/'CAPTURE_RESULT_R1.json').exists()
    assert all(row['inputs_before'][p]==s==sha(Path(p)) for p,s in row['inputs_after'].items())
    proposal=LAB/'evidence/o1-exact-local-stage-preparation-r1/CAPTURE_PROPOSAL_R1.json'
    config=LAB/'evidence/o1-exact-local-stage-launcher-preparation-r1/FIXED_ROUTE_CONFIG_R1.json'
    launcher=LAB/'scripts/r4_exact_local_stage_launcher_r1.py'
    collector=LAB/'scripts/r4_exact_local_stage_collector_r1.py'
    for k,p in [('launcher_sha256',launcher),('collector_sha256',collector),('proposal_sha256',proposal),('config_sha256',config)]:assert sha(p)==receipt[k]==row.get(k,receipt[k])
    text=raw[1].read_text(errors='replace')
    assert 'AssertionError: factory addon inventory must be empty' in text
    assert 'EXACT_LOCAL_STAGE_READ' not in text
    sample=row['resource_samples'][-1]
    assert sample['image_query_success'] is False and sample['image_error']==5
    assert sample['owned_handle_signaled_before_image'] is False and sample['owned_handle_signaled_after_image'] is False
    facts={
        'status':'FAILED_SINGLE_APPROVED_CAPTURE_NO_RETRY',
        'approved_attempts':1,'actual_child_launches':1,'pid':row['pid'],'creation_FILETIME':row['creation_FILETIME'],'guard_parent_pid':row['guard_parent_pid'],
        'guard_status':row['guard_status'],'data_result':row['data_result'],
        'collector_failure':'Factory preferences addon collection was nonempty; strict empty-inventory assertion failed before snapshot/recipe identity/Action activation/clone/stage capture.',
        'addon_ids':'NOT_CAPTURED; cannot infer built-in versus user addons from collection nonempty alone',
        'addon_log_marker_check':{x:(x in text) for x in ['BlenderMCP','Higgsfield','MPFB','account-balance']},
        'guard_failure':'Missing executable image error5 on exact owned handle that remained unsignaled before/after lookup. Exit FILETIME was populated; it was not used as substitute for handle signaling. Whole guard FAIL preserved.',
        'terminal_cleanup':{k:row[k] for k in ['cleanup_terminate_owned_job_if_live','cleanup_owned_handle_signaled','cleanup_owned_handle_exit_code','cleanup_owned_times','cleanup_job_accounting_before_close','cleanup_job_pids_before_close','job_close_success','owned_process_signaled_after_job_close','cleanup_errors']},
        'native_job_limit_readback':row['native_job_limit_readback'],
        'resource_minima_bytes':{k:min(s[k] for s in row['resource_samples']) for k in ['free_RAM_bytes','free_C_bytes']},
        'source_action_recipe_and_all_dependencies_pre_post_sha_identical':True,
        'full_scene_signature':'NOT_RUN; failure was earlier. File hash preservation is not scene signature acceptance.',
        'stage6_reference_comparison':'NOT_RUN','perarray_metadata':[],'local_world_stage_arrays':0,
        'native_cache_operator_branch':'UNKNOWN_NOT_READ','first_comparative_divergence':'NOT_PROVEN',
        'raw_files':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in raw},
        'source_inputs_current_hashes':row['inputs_after'],
        'wall_seconds_owned_job':row['wall_seconds'],'renders_exports_saves_GPU_download_build':0,
        'R5_whole_guard_status':'FAIL_PRESERVED','gui_observation':'Separate read-only process query before/after saw PID129152 with unchanged start2026-10-02 23:17:57; no attach/kill/control',
        'GPU_lease':'PRODUCT_EXCLUSIVE/product-observed58248 untouched',
        'next_bounded_review':'Review the overly strict empty factory-addon assumption from this actual failure; identify bundled factory addon inventory by static files or separately approved diagnostic. No new execution or guard relaxation authorized.',
    }
    E.mkdir(parents=True)
    write(E/'FAILED_CAPTURE_FINDINGS_R1.json',facts)
    for p in raw:shutil.copyfile(p,E/p.name);assert sha(E/p.name)==sha(p)
    packet=OUT/'YURI_O1_EXACT_LOCAL_SINGLE_CAPTURE_FAILED_R1.zip'
    items=raw+[E/'FAILED_CAPTURE_FINDINGS_R1.json',launcher,collector,proposal,config]
    with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
        for p in items:z.write(p,p.name)
    with zipfile.ZipFile(packet) as z:
        assert z.testzip() is None
        for p in items:assert hashlib.sha256(z.read(p.name)).hexdigest()==sha(p)
    custody={'status':facts['status'],'private_transfer_packet':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'contains_motion_arrays':False,'zip_CRC_and_all_member_hashes_verified':True,'members':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in items}}
    write(E/'PACKET_CUSTODY_R1.json',custody)
    write(OUT/'FAILURE_PACKET_CUSTODY_R1.json',custody)
    outbox=Path('C:/YuriTransfer/outbox')/('YURI_O1_EXACT_LOCAL_SINGLE_CAPTURE_FAILED_R1_'+sha(packet)[:12])
    assert not outbox.exists();outbox.mkdir(parents=True)
    shutil.copyfile(packet,outbox/packet.name)
    assert sha(outbox/packet.name)==sha(packet)
    write(E/'PRIVATE_TRANSFER_OUTBOX_R1.json',{'path':str(outbox/packet.name),'sha256':sha(packet),'bytes':packet.stat().st_size})
    print(json.dumps({'status':facts['status'],'packet_sha256':sha(packet),'packet_bytes':packet.stat().st_size,'outbox':str(outbox/packet.name),'data_arrays':0}))

if __name__=='__main__':main()
