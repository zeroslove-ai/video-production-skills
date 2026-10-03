"""File-only failed-run custody audit. Does not retry or modify frozen sampler."""
from pathlib import Path
import gzip,hashlib,json,shutil,zipfile
LAB=Path(__file__).resolve().parent.parent
OUT=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-original-idle-sampling-r2')
E=LAB/'evidence/o1-original-idle-sampling-result-r2'
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
    job=load(OUT/'OWNED_JOB_RESULT_R1.json');custody=load(OUT/'TERMINAL_FILE_CUSTODY_R2.json')
    scene=load(OUT/'SCENE_SIGNATURE_BEFORE_AFTER.json');on=load(OUT/'ON_SOURCE_SIGNATURE_R1.json')
    assert job['pid']==112528 and job['guard_status']=='FAIL' and job['cleanup_owned_handle_exit_code']==93
    assert job['retry_count']==0 and job['cleanup_job_accounting_before_close']['active']==0 and job['cleanup_job_pids_before_close']==[] and not job['cleanup_errors']
    assert job['job_close_success'] and job['owned_process_signaled_after_job_close']
    assert job['inputs_before']==job['inputs_after']
    assert all(sha(p)==s for p,s in job['inputs_after'].items())
    assert custody['status']=='FINAL_CLOSED_LOG_AND_JOB_RECEIPT'
    for n,r in custody['files'].items():assert sha(OUT/n)==r['sha256'] and (OUT/n).stat().st_size==r['bytes']
    categories=['meshes_shape_keys_weights','rest_rigs','actions','rest_pose_settings','materials','node_groups','textures','worlds']
    assert all(on[c]==scene['before'][c]==scene['after'][c] for c in categories)
    assert scene['before']['evaluated_geometry_world']==scene['after']['evaluated_geometry_world']
    struct=load(OUT/'STRUCTURAL_OFF_ON_OFF_R1.json');assert struct['before']==struct['on']
    before_process=load(OUT/'PROCESS_RESOURCE_RECONCILIATION_BEFORE.json');after_process=load(OUT/'PROCESS_RECONCILIATION_AFTER.json')
    assert before_process['gpu_lease_sha256']==after_process['gpu_lease_sha256'] and after_process['owned_112528_absent']
    assert len(after_process['blender'])==1 and after_process['blender'][0]['ProcessId']==129152
    count=0;offset=0;frames=[]
    with gzip.open(OUT/'FRAMES_PRIVATE_R1.jsonl.gz','rt') as jf,gzip.open(OUT/'ALL_MESH_NATIVE_LOCAL_F32_PRIVATE_R1.bin.gz','rb') as gf:
        for line in jf:
            row=json.loads(line);count+=1;frames.append(row['frame'])
            assert row['frame']==count and [len(d['channels']) for d in row['domains']]==[364,16,2,4]
            assert sum(len(r['bones']) for r in row['rigs'])==137
            assert len(next(r for r in row['rigs'] if r['object']=='Meshy_Fitted_Rig')['bones'])==57
            assert len(next(r for r in row['rigs'] if r['object']=='Hair_Rig_R4')['bones'])==10
            assert sum(d['owner']=='Hair_Rig_R4' for d in row['drivers'])==14
            assert sum(bool(d['mute']) for d in row['drivers'])==13
            assert len(next(k for k in row['Keys'] if k['Key']=='FaceControls_TEST_Jaw_Smile.001')['values'])==72
            for g in row['geometry']:
                assert g['offset_uncompressed_bytes']==offset
                data=gf.read(g['bytes']);assert len(data)==g['bytes'] and hashlib.sha256(data).hexdigest()==g['sha256']
                offset+=len(data)
        assert gf.read(1)==b''
    assert count==145
    files=sorted(p for p in OUT.iterdir() if p.is_file())
    packet=OUT/'YURI_ORIGINAL_IDLE_SAMPLING_FAILED_CAPTURE_R2.zip'
    with zipfile.ZipFile(packet,'x',zipfile.ZIP_STORED) as z:
        for p in files:z.write(p,p.name)
    with zipfile.ZipFile(packet) as z:
        assert z.testzip() is None
        for p in files:
            h=hashlib.sha256()
            with z.open(p.name) as f:
                for b in iter(lambda:f.read(1048576),b''):h.update(b)
            assert h.hexdigest()==sha(p)
    report={'status':'FAILED_OFF_RESTORATION_CAPTURE_145_COMPLETE_PRIVATE_CUSTODY_ONLY','guard_status':job['guard_status'],'collector_manifest_status':'NOT_WRITTEN; restoration assertion before final result','frozen_auditor_actual_status':'FAIL at before==after preservation assertion; no weakening','actual_command':job['argv'],'pid':job['pid'],'creation_FILETIME':job['creation_FILETIME'],'guard_parent_pid':job['guard_parent_pid'],'native_process_handle':job['native_process_handle'],'native_job_handle':job['native_job_handle'],'owned_exit_code':93,'job_drained':True,'cleanup_errors':job['cleanup_errors'],'wall_seconds':job['wall_seconds'],'resource_minima_bytes':{k:min(s[k] for s in job['resource_samples']) for k in ['free_RAM_bytes','free_C_bytes']},'source_and_inputs_SHA_unchanged':True,'GUI_129152_and_product_GPU_lease_unchanged':True,'full_frames_native_capture':145,'native_domain_curve_counts':[364,16,2,4],'all_bones':137,'head_Key_outputs':72,'hair_drivers':14,'muted_drivers_every_frame':13,'native_geometry_bytes_verified':offset,'closed_log_terminal_custody_SHA_verified':True,'OFF_ON_static_invariants_exact':categories,'OFF_restored_evaluated_world_geometry_exact':True,'OFF_full_signature_differences':scene['differences'],'complete_driver_NLA_structure_before_ON_exact':True,'restored_driver_NLA_structure_status':'NOT_WRITTEN; failed full OFF assertion first','seam_velocity_orientation_geometry_visual_verdict':'NOT_ACCEPTED; final measurements/result not written; raw145 supports downstream analysis','restoration_cause':'NOT_YET_PROVEN: before metadata records last_slot_identifier empty on all four IDs; frozen restore clears action but does not explicitly restore this field. After per-ID raw RNA not saved, so cannot attribute hash difference conclusively. Source on-disk immutable.','next_one_task':'File-only isolate AnimData bookkeeping restoration (including last_slot_identifier/slot handle) and prepare an additive exact-state diagnostic/restore proposal; no retry or native launch until separate review.','private_packet':{'path':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'CRC_all_member_SHA_verified':True,'members':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in files}},'product_visual_playback_acceptance':'NOT_CLAIMED','retry_count':0}
    E.mkdir(parents=True);write(E/'FAILED_CAPTURE_CUSTODY_R2.json',report)
    for n in ['OWNED_JOB_RESULT_R1.json','TERMINAL_FILE_CUSTODY_R2.json','SCENE_SIGNATURE_BEFORE_AFTER.json','PROCESS_RESOURCE_RECONCILIATION_BEFORE.json','PROCESS_RECONCILIATION_AFTER.json','fixed-capture.log']:
        shutil.copyfile(OUT/n,E/n);assert sha(OUT/n)==sha(E/n)
    print(json.dumps({'status':report['status'],'frames':count,'geometry_bytes':offset,'packet_bytes':packet.stat().st_size,'packet_sha256':sha(packet)}))
if __name__=='__main__':main()
