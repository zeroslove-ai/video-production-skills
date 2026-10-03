"""Independent CPU-only file validation/freeze; never invokes bpy or a process."""
from pathlib import Path
import hashlib, json, shutil, zipfile
import numpy as np

LAB=Path(__file__).resolve().parent.parent
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-exact-source-local-stage-capture-r2'
E=LAB/'evidence/o1-exact-local-stage-capture-result-r2'
PREP=LAB/'evidence/o1-exact-local-stage-factory-addon-preparation-r2'

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def ah(a):return hashlib.sha256(a.tobytes(order='C')).hexdigest()
def load(p):return json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2)

def main():
    assert not E.exists(),'Never overwrite frozen evidence'
    raw_files=sorted(p for p in OUT.iterdir() if p.is_file())
    guard=load(OUT/'OWNED_JOB_RESULT_R1.json');data=load(OUT/'CAPTURE_RESULT_R1.json')
    proposal=load(PREP/'CAPTURE_PROPOSAL_R2.json')
    assert sha(OUT/'PM_APPROVAL_EXACT_LOCAL_CAPTURE_R2.json')=='97680145bec890e2b79cd875559e6758358f34e125dc1693047d405f3b64dfd3'
    assert guard['guard_status']=='PASS_OWNED_JOB_EXIT_ZERO_DRAINED' and guard['pid']==48516
    assert guard['terminal_owned_handle_exit_code']==guard['cleanup_owned_handle_exit_code']==0
    assert guard['terminal_job_accounting']['active']==guard['cleanup_job_accounting_before_close']['active']==0
    assert guard['terminal_job_accounting']['total']==1 and guard['terminal_job_accounting']['limit_terminated']==0
    assert guard['terminal_job_pids']==guard['cleanup_job_pids_before_close']==[]
    assert guard['job_close_success'] and guard['cleanup_owned_handle_signaled'] and guard['owned_process_signaled_after_job_close'] and not guard['cleanup_errors']
    assert guard['retry_count']==0 and data['pid']==48516
    assert guard['inputs_before']==guard['inputs_after']
    assert all(sha(Path(p))==s for p,s in guard['inputs_after'].items())
    assert data['source_pre_post_identical'] and data['full_CSR_original_identity']=={'entries':304799,'zero_entries':37310,'recipe_sha256':'0cd0bdd70e5a6c0670846dab74e295b0a637a79f1c6d57d503611d5cf50aafe0'}
    scene=load(OUT/'SCENE_SIGNATURE_BEFORE_AFTER.json')
    assert scene['differences']=={} and scene['before']==scene['after']
    inv_before=load(OUT/'ADDON_ORIGIN_INVENTORY_BEFORE_R2.json');inv_after=load(OUT/'ADDON_ORIGIN_INVENTORY_AFTER_R2.json')
    assert inv_before['status']==inv_after['status']=='PASS_PINNED_INSTALLED_ORIGINS_ONLY'
    assert inv_before['preferences_module_names']==inv_after['preferences_module_names'] and inv_before['loaded_enabled_module_names']==inv_after['loaded_enabled_module_names']
    for inventory in (inv_before,inv_after):
        assert inventory['installed_python_files_checked']==315 and inventory['factory_startup'] and not inventory['errors']
        for m in inventory['modules']:assert m['classification']=='PINNED_INSTALLED_BUNDLED_MODULE' and sha(Path(m['resolved_origin']))==m['origin_sha256']
    install_manifest=load(PREP/'INSTALLED_BUNDLED_ADDON_ORIGIN_MANIFEST_R2.json')
    for package in install_manifest['installed_bundled_allowlist'].values():
        assert all(sha(Path(p))==s for p,s in package['python_files'].items())
    recipe=load(BASE/'o1-native-armature-full-recipe-custody-r1/SourceBodyArmatureInput_0cd0bdd7_EXACT.json')
    contract_path=LAB/'evidence/o1-normal-tess-domain-contract-r1/NORMAL_TESS_DOMAIN_CONTRACT_R1.json'
    assert sha(contract_path)=='0e6e0e6693639e93fafe0647ff104dbd44b3ad11e5ca49ded671997b1fae9552'
    contract=load(contract_path)
    validations=[]
    assert [(r['clip'],r['frame']) for r in data['rows']]==[('YRA_R4_Startle_Short',11),('YRA_R4_Struggle_Strong_Loop',6)]
    for row in data['rows']:
        p=OUT/row['file'];assert sha(p)==row['sha256'] and p.stat().st_size==row['bytes']
        with zipfile.ZipFile(p) as nz:assert nz.testzip() is None
        z=np.load(p,allow_pickle=False)
        assert set(z.files)==set(row['arrays'])
        for k,meta in row['arrays'].items():
            a=z[k];assert list(a.shape)==meta['shape'] and str(a.dtype)==meta['dtype'] and ah(a)==meta['sha256'] and np.isfinite(a).all()
        assert z['rest_local_f64'].shape==(57,4,4)
        assert z['rest_local_f64'].astype('<f4').tobytes()==np.asarray(recipe['rest'],dtype='<f4').reshape(57,4,4).tobytes()
        assert z['body_world_f64'].astype('<f4').tobytes()==np.asarray(recipe['sourceWorld'],dtype='<f4').reshape(4,4).tobytes()
        assert row['bone_names']==recipe['boneNames']
        reference_path=Path(proposal['final_reference_by_clip'][row['clip']])
        final_equal={}
        with np.load(reference_path,allow_pickle=False) as ref:
            for k in ['local_position','local_corner_normal','world_position','world_corner_normal']:
                final_equal[k]=z['stage_06_'+k].tobytes()==ref['current_'+k].tobytes()
        assert all(final_equal.values())
        old_path=BASE/'o1-raw-pose-driver-stage-reference-r1'/f"{row['clip']}_frame{row['frame']:03d}_seven_stages.npz"
        old=np.load(old_path,allow_pickle=False)
        old_equal={}
        world_transport=[]
        for stage in range(7):
            prefix=f'stage_{stage:02d}_'
            for k in ['world_position','world_corner_normal']:old_equal[prefix+k]=z[prefix+k].tobytes()==old[prefix+k].tobytes()
            local=z[prefix+'local_position'];normal=z[prefix+'local_corner_normal'];mw=z[prefix+'evaluated_body_world']
            assert local.shape==(63561,3) and normal.shape==(254602,3) and local.dtype==normal.dtype==np.float32
            w=(local.astype(np.float64)@mw[:3,:3].T+mw[:3,3]).astype(np.float32)
            wn=normal.astype(np.float64)@np.linalg.inv(mw[:3,:3]);wn/=np.linalg.norm(wn,axis=1)[:,None]
            assert w.tobytes()==z[prefix+'world_position'].tobytes() and wn.astype(np.float32).tobytes()==z[prefix+'world_corner_normal'].tobytes()
            world_transport.append({'stage':stage,'independent_world_transform_bits_equal':True})
        case=next(c for c in contract['four_actual_runtime_failures'] if c['clip']==row['clip'] and c['source_frame']==row['frame'])
        corners=np.concatenate([np.arange(x['source_corner_start'],x['source_corner_start']+5) for x in case['PM_trace_polygon_instances']])
        points=np.unique(z['original_corner_vertex'][corners])
        focused=[]
        for stage in range(1,7):
            focused.append({'from':stage-1,'to':stage,'local_position_changed_focused_points':int(np.any(z[f'stage_{stage-1:02d}_local_position'][points].view(np.uint32)!=z[f'stage_{stage:02d}_local_position'][points].view(np.uint32),axis=1).sum()),'local_normal_changed_focused_CORNERs':int(np.any(z[f'stage_{stage-1:02d}_local_corner_normal'][corners].view(np.uint32)!=z[f'stage_{stage:02d}_local_corner_normal'][corners].view(np.uint32),axis=1).sum())})
        pose_path=OUT/f"{row['clip']}_frame{row['frame']:03d}_all_rig_pose_rest.json"
        pose=load(pose_path)
        assert hashlib.sha256(json.dumps(pose['rigs'],separators=(',',':')).encode()).hexdigest()==pose['fingerprint']==row['all_rig_pose_rest_fingerprint']
        validations.append({'clip':row['clip'],'frame':row['frame'],'file':row['file'],'sha256':sha(p),'bytes':p.stat().st_size,'arrays':row['arrays'],'stage6_frozen_final_reference_bits_equal':final_equal,'prior_seven_stage_WORLD_arrays_equal':old_equal,'prior_stage_file_sha256':sha(old_path),'world_transforms':world_transport,'focused_source_points':points.tolist(),'focused_source_CORNERs':corners.tolist(),'focused_local_changes':focused,'all_rig_pose_rest_file_sha256':sha(pose_path),'all_rig_pose_rest_fingerprint':pose['fingerprint'],'all_rig_bone_count':sum(len(r['bones']) for r in pose['rigs'].values())})
        z.close();old.close()
    facts={'status':'ACTUAL_NATIVE_SOURCE_LOCAL_TWO_FRAME_DATA_VALIDATED_GUARD_PASS_SEPARATE','pid':48516,'creation_FILETIME':guard['creation_FILETIME'],'guard_parent_pid':guard['guard_parent_pid'],'guard_status':guard['guard_status'],'data_status':data['status'],'independent_file_array_hash_shape_dtype_finite_readback':True,'scene_signature_before_after_exact':True,'scene_signature_categories':list(scene['before']),'source_action_recipe_rest_fullCSR_weights_material_driver_preservation':'Collector exact original CSR/rest checks plus identical whole-scene hashes and immutable file SHA. Raw CSR is not republished.','native_local_provenance':'Original-index evaluated mesh.vertices.co and native mesh.corner_normals.vector; no averaging/reconstructed local data.','world_provenance':data['world_data_policy'],'evaluation_scope':data['limitation'],'native_cache_operator_branch':'UNKNOWN_NOT_READ','first_comparative_divergence':'NOT_PROVEN_NO_ACTUAL_CONSUMER_STAGE_ARRAYS','frames':validations,'actual_enabled_modules_before_after':inv_before['loaded_enabled_module_names'],'prior_failed_run_factory_inventory':'UNKNOWN; R2 actual inventory does not retroactively identify R1','installed_origin_fingerprint_status':'315 Python files/13 candidate package origins pinned; eight modules actually enabled and resolved in R2','guard_terminal':{k:guard[k] for k in ['terminal_owned_handle_exit_code','terminal_job_accounting','terminal_job_pids','cleanup_owned_handle_signaled','cleanup_owned_handle_exit_code','cleanup_job_accounting_before_close','cleanup_job_pids_before_close','job_close_success','owned_process_signaled_after_job_close','cleanup_errors']},'native_job_limit_readback':guard['native_job_limit_readback'],'resource_minima_bytes':{k:min(r[k] for r in guard['resource_samples']) for k in ['free_RAM_bytes','free_C_bytes']},'wall_seconds_guard':guard['wall_seconds'],'wall_seconds_collector':data['seconds'],'R1_and_R5_whole_guard_FAIL':'PRESERVED','raw_file_custody':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in raw_files},'retry_count':0,'renders_exports_saves_GPU_download_build':0,'next_bounded_task':'Compare actual consumer local stages0/1/2 with these source local f32 arrays at original IDs; no extra source/native job is needed for this pair.'}
    E.mkdir(parents=True)
    write(E/'INDEPENDENT_SOURCE_LOCAL_VALIDATION_R2.json',facts)
    for p in raw_files:
        if p.suffix=='.npz' or p.name.endswith('_all_rig_pose_rest.json'):continue
        shutil.copyfile(p,E/p.name);assert sha(E/p.name)==sha(p)
    write(OUT/'INDEPENDENT_SOURCE_LOCAL_VALIDATION_R2.json',facts)
    packet=OUT/'YURI_O1_EXACT_SOURCE_LOCAL_TWO_FRAME_R2.zip'
    packet_files=raw_files+[OUT/'INDEPENDENT_SOURCE_LOCAL_VALIDATION_R2.json']+[PREP/n for n in ['CAPTURE_PROPOSAL_R2.json','FIXED_ROUTE_CONFIG_R2.json','INSTALLED_BUNDLED_ADDON_ORIGIN_MANIFEST_R2.json']]+[LAB/'scripts'/n for n in ['r4_exact_local_stage_collector_r2.py','r4_exact_local_stage_launcher_r2.py','r4_installed_addon_origin_gate_r2.py']]
    with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
        for p in packet_files:z.write(p,p.name)
    with zipfile.ZipFile(packet) as z:
        assert z.testzip() is None
        for p in packet_files:assert hashlib.sha256(z.read(p.name)).hexdigest()==sha(p)
    custody={'status':facts['status'],'private_transfer_packet':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'ZIP_CRC_and_member_SHA_verified':True,'source_model_Action_library_full_recipe_in_packet':False,'private_native_stage_arrays_and_pose_rest_in_packet':True,'members':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in packet_files}}
    write(E/'PACKET_CUSTODY_R2.json',custody)
    write(OUT/'PACKET_CUSTODY_R2.json',custody)
    outbox=Path('C:/YuriTransfer/outbox')/('YURI_O1_EXACT_SOURCE_LOCAL_TWO_FRAME_R2_'+sha(packet)[:12])
    assert not outbox.exists();outbox.mkdir(parents=True)
    shutil.copyfile(packet,outbox/packet.name);assert sha(outbox/packet.name)==sha(packet)
    write(E/'PRIVATE_TRANSFER_OUTBOX_R2.json',{'path':str(outbox/packet.name),'bytes':packet.stat().st_size,'sha256':sha(packet)})
    print(json.dumps({'status':facts['status'],'packet_bytes':packet.stat().st_size,'packet_sha256':sha(packet),'outbox':str(outbox/packet.name),'prior_WORLD_all_equal':all(all(r['prior_seven_stage_WORLD_arrays_equal'].values()) for r in validations),'focused_local_all_unchanged':all(not(x['local_position_changed_focused_points'] or x['local_normal_changed_focused_CORNERs']) for r in validations for x in r['focused_local_changes'])}))

if __name__=='__main__':main()
