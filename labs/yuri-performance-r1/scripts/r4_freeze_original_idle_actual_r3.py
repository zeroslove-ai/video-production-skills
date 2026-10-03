"""File-only data custody, separated from failed strict whole guard; never retry."""
from pathlib import Path
import gzip,hashlib,json,shutil,zipfile
LAB=Path(__file__).resolve().parent.parent
OUT=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-original-idle-sampling-r3')
E=LAB/'evidence/o1-original-idle-sampling-result-r3'
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):
    with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
def main():
    assert not E.exists()
    job=load(OUT/'OWNED_JOB_RESULT_R1.json');result=load(OUT/'IDLE_SAMPLING_RESULT_R3.json')
    assert job['pid']==124580 and job['guard_status']=='FAIL' and job['cleanup_owned_handle_exit_code']==0
    assert 'missing executable image while owned handle genuinely LIVE' in job['error']
    last=job['resource_samples'][-1]
    assert last['image_error']==5 and not last['owned_handle_signaled_before_image'] and not last['owned_handle_signaled_after_image']
    assert job['retry_count']==0 and job['cleanup_job_accounting_before_close']['active']==0 and job['cleanup_job_pids_before_close']==[] and not job['cleanup_errors']
    assert job['job_close_success'] and job['owned_process_signaled_after_job_close']
    assert job['inputs_before']==job['inputs_after'] and all(sha(p)==s for p,s in job['inputs_after'].items())
    custody=load(OUT/'TERMINAL_FILE_CUSTODY_R3.json')
    assert custody['status']=='FINAL_CLOSED_LOG_AND_JOB_RECEIPT'
    for name,row in custody['files'].items():assert sha(OUT/name)==row['sha256'] and (OUT/name).stat().st_size==row['bytes']
    for name,row in result['files'].items():assert sha(OUT/name)==row['sha256'] and (OUT/name).stat().st_size==row['bytes']
    scene=load(OUT/'SCENE_SIGNATURE_BEFORE_AFTER.json');on=load(OUT/'ON_SOURCE_SIGNATURE_R1.json')
    assert scene['before']==scene['after'] and scene['differences']=={}
    for c in ['meshes_shape_keys_weights','rest_rigs','actions','rest_pose_settings','materials','node_groups','textures','worlds']:assert scene['before'][c]==on[c]
    raw={}
    for phase,sig in [('BEFORE',scene['before']),('ON',on),('AFTER',scene['after'])]:
        with gzip.open(OUT/f'RAW_FINGERPRINT_INPUTS_{phase}_PRIVATE_R3.json.gz','rt') as f:raw[phase]=json.load(f)
        for category in ['objects','mesh_attributes']:
            assert {n:hashlib.sha256(json.dumps(v,separators=(',',':')).encode()).hexdigest() for n,v in raw[phase][category].items()}==sig[category]
    assert raw['BEFORE']==raw['AFTER'];raw.clear()
    verdict=load(OUT/'FORENSIC_RESTORATION_VERDICT_R3.json')
    assert verdict['raw_difference_count']==0 and not verdict['ledger_error_indices'] and verdict['driver_NLA_same'] and not verdict['full_signature_differences']
    struct=load(OUT/'STRUCTURAL_OFF_ON_OFF_R1.json');after=load(OUT/'STRUCTURAL_RESTORED_R1.json')
    assert struct['before']==struct['on']==after['after']
    with gzip.open(OUT/'RAW_FIELD_DIFF_PRIVATE_R3.json.gz','rt') as f:assert json.load(f)==[]
    ledger=load(OUT/'RESTORATION_LEDGER_PRIVATE_R3.json')
    restored_slot_fields=[{'owner':r['owner'],'field':r['field'],'assignment':r.get('assignment'),'exact':r.get('exact')} for r in ledger if r.get('field') in {'last_slot_identifier','action_slot_handle'}]
    assert len(restored_slot_fields)==16 and all(r['exact'] for r in restored_slot_fields)
    before_process=load(OUT/'PROCESS_RESOURCE_RECONCILIATION_BEFORE.json');after_process=load(OUT/'PROCESS_RECONCILIATION_AFTER.json')
    assert before_process['gpu_lease_sha256']==after_process['gpu_lease_sha256'] and after_process['owned_124580_absent']
    assert len(after_process['blender'])==1 and after_process['blender'][0]['ProcessId']==129152
    count=0;offset=0;geometry_records=0;endpoints={};domain_metrics={};static={};first={}
    with gzip.open(OUT/'FRAMES_PRIVATE_R1.jsonl.gz','rt') as jf,gzip.open(OUT/'ALL_MESH_NATIVE_LOCAL_F32_PRIVATE_R1.bin.gz','rb') as gf:
        for line in jf:
            row=json.loads(line);count+=1;assert row['frame']==count
            assert [len(d['channels']) for d in row['domains']]==[364,16,2,4]
            assert sum(len(r['bones']) for r in row['rigs'])==137
            assert len(next(r for r in row['rigs'] if r['object']=='Meshy_Fitted_Rig')['bones'])==57
            assert len(next(r for r in row['rigs'] if r['object']=='Hair_Rig_R4')['bones'])==10
            assert sum(d['owner']=='Hair_Rig_R4' for d in row['drivers'])==14 and sum(bool(d['mute']) for d in row['drivers'])==13
            assert len(next(k for k in row['Keys'] if k['Key']=='FaceControls_TEST_Jaw_Smile.001')['values'])==72
            for domain in row['domains']:
                name=domain['Action'];values=[c['evaluated_RNA'] for c in domain['channels']]
                if count==1:first[name]=values;static[name]=[True]*len(values);domain_metrics[name]={'max_native_curve_vs_evaluated_RNA':0}
                for i,(c,v) in enumerate(zip(domain['channels'],values)):
                    static[name][i]=static[name][i] and v==first[name][i]
                    domain_metrics[name]['max_native_curve_vs_evaluated_RNA']=max(domain_metrics[name]['max_native_curve_vs_evaluated_RNA'],abs(c['native_FCurve_evaluate']-v))
            if count in {1,2,72,73,74,144,145}:endpoints[count]=row
            for g in row['geometry']:
                assert g['offset_uncompressed_bytes']==offset and g['bytes']==g['vertices']*12
                data=gf.read(g['bytes']);assert len(data)==g['bytes'] and hashlib.sha256(data).hexdigest()==g['sha256']
                offset+=len(data);geometry_records+=1
        assert gf.read(1)==b''
    assert count==145 and offset==result['geometry_uncompressed_bytes']==331863240 and geometry_records==6525
    for name in domain_metrics:domain_metrics[name]['static_evaluated_channel_indices']=[i for i,s in enumerate(static[name]) if s]
    private_measurements={'status':'NO_LOOP_VISUAL_PASS; endpoints/raw orientation/geometry retained for downstream whole-domain analysis','domain_metrics':domain_metrics,'endpoint_frames':sorted(endpoints)}
    write(OUT/'INDEPENDENT_DOMAIN_MEASUREMENTS_PRIVATE_R3.json',private_measurements)
    files=sorted(p for p in OUT.iterdir() if p.is_file())
    packet=OUT/'YURI_ORIGINAL_IDLE_ACTUAL_R3_GUARD_FAIL_DATA_RESTORED.zip'
    with zipfile.ZipFile(packet,'x',zipfile.ZIP_STORED) as z:
        for p in files:z.write(p,p.name)
    with zipfile.ZipFile(packet) as z:
        assert z.testzip() is None
        for p in files:
            h=hashlib.sha256()
            with z.open(p.name) as f:
                for b in iter(lambda:f.read(1048576),b''):h.update(b)
            assert h.hexdigest()==sha(p)
    report={'player_visible_delta':'새 사용자 기능 없음; strict LIVE image guard 실패로 전체 공급 승인 HOLD. 원본 Idle145 및 정확한 OFF 복원 데이터는 독립 검증 완료.', 'status':'INDEPENDENT_DATA_AND_RAW_OFF_RESTORE_PASS_WHOLE_GUARD_FAIL_HOLD','guard_status':'FAIL','frozen_whole_auditor_actual_status':'FAIL at required guard PASS assertion; prior raw/signature comparisons passed; not weakened','actual_command':job['argv'],'pid':job['pid'],'creation_FILETIME':job['creation_FILETIME'],'guard_parent_pid':job['guard_parent_pid'],'native_process_handle':job['native_process_handle'],'native_job_handle':job['native_job_handle'],'terminal_owned_exit_field':'NOT_RECORDED due LIVE assertion; cleanup exact owned exit0','cleanup_owned_exit_code':0,'cleanup_accounting':job['cleanup_job_accounting_before_close'],'cleanup_pids':[],'cleanup_errors':[],'wall_seconds':job['wall_seconds'],'strict_LIVE_failure':{'image_error':5,'owned_handle_before_signaled':False,'owned_handle_after_signaled':False,'exit_FILETIME_not_terminal_substitute':True},'source_SHA':result['source_sha256'],'inputs_SHA_unchanged':True,'original_GUI_product_GPU_unchanged':True,'frames':145,'native_curve_counts':[364,16,2,4],'all_bones':137,'head_Key_outputs':72,'hair_drivers':14,'muted_drivers_per_frame':13,'geometry_records_verified':geometry_records,'geometry_bytes_verified':offset,'raw_before_after_exact':True,'raw_original_hash_recomputation_exact':True,'all_original_scene_signatures_exact_OFF_restored':True,'driver_NLA_structure_before_ON_after_exact':True,'restored_slot_field_readbacks':restored_slot_fields,'R2_cause':'Not retroactively proven without R2 AFTER raw fields; R3 explicit bookkeeping restoration exact and full raw0 differences demonstrated','loop_orientation_velocity_geometry_silhouette_visual':'NOT_ACCEPTED; no render; full145 actual raw evidence retained','retry_count':0,'private_packet':{'path':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'CRC_all_member_SHA_verified':True,'members':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in files}},'explicit_alternative_after_repeated_failure':'Separate file-only verified canonical-source/curve/fingerprint/failed-guard native data custody from whole-execution/product acceptance. Continue PM-reviewed O1-I1 adapter/loop/driver analysis using correctly labelled source evidence; no native retry, no weaker guard or transport PASS. Strict FAIL/HOLD remains; product writer owns actual scene.','next_one_task':'PM independent private custody/domain review for original BODY/FACE/Blink/GAZE/HAIR mapping and loop/driver analysis under guard-FAIL label, without duplicating export or waiting on unrelated normals/tessellation/PBR research.'}
    E.mkdir(parents=True);write(E/'INDEPENDENT_DATA_CUSTODY_R3.json',report)
    for name in ['OWNED_JOB_RESULT_R1.json','TERMINAL_FILE_CUSTODY_R3.json','SCENE_SIGNATURE_BEFORE_AFTER.json','FORENSIC_RESTORATION_VERDICT_R3.json','RAW_FIELD_DIFF_PATHS_R3.json','PROCESS_RESOURCE_RECONCILIATION_BEFORE.json','PROCESS_RECONCILIATION_AFTER.json','fixed-capture.log']:
        shutil.copyfile(OUT/name,E/name);assert sha(OUT/name)==sha(E/name)
    print(json.dumps({'status':report['status'],'packet_bytes':packet.stat().st_size,'packet_sha256':sha(packet),'domain_max_errors':{n:m['max_native_curve_vs_evaluated_RNA'] for n,m in domain_metrics.items()}}))
if __name__=='__main__':main()
