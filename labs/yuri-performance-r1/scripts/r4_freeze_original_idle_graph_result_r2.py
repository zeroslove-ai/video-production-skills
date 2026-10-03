"""Independent file-only graph/terminal/identity audit and immutable packet."""
from pathlib import Path
import hashlib,json,shutil,zipfile
LAB=Path(__file__).resolve().parent.parent
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-original-idle-slot-graph-inspection-r2'
E=LAB/'evidence/o1-original-idle-slot-graph-result-r2'
PREP=LAB/'evidence/o1-original-idle-slot-graph-preparation-r2'

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def load(p):return json.loads(p.read_bytes())
def write(p,v):
    with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2)

def main():
    assert not E.exists(),'No overwrite'
    originals=sorted(p for p in OUT.iterdir() if p.is_file())
    data=load(OUT/'IDLE_SLOT_GRAPH_RESULT_R1.json');guard=load(OUT/'OWNED_JOB_RESULT_R1.json');scene=load(OUT/'SCENE_SIGNATURE_BEFORE_AFTER.json')
    proposal=load(PREP/'INSPECTION_PROPOSAL_R2.json');review=load(OUT/'PM_APPROVAL_ORIGINAL_IDLE_GRAPH_R2.json')
    assert guard['pid']==128164 and guard['guard_status']=='PASS_OWNED_JOB_EXIT_ZERO_DRAINED'
    assert guard['terminal_owned_handle_exit_code']==guard['cleanup_owned_handle_exit_code']==0
    assert guard['terminal_job_accounting']['active']==guard['cleanup_job_accounting_before_close']['active']==0
    assert guard['terminal_job_accounting']['total']==1 and guard['terminal_job_accounting']['limit_terminated']==0
    assert guard['terminal_job_pids']==guard['cleanup_job_pids_before_close']==[] and guard['cleanup_errors']==[]
    assert guard['cleanup_owned_handle_signaled'] and guard['job_close_success'] and guard['owned_process_signaled_after_job_close']
    assert guard['retry_count']==0 and guard['inputs_before']==guard['inputs_after']
    assert all(sha(Path(p))==s for p,s in guard['inputs_after'].items())
    assert scene['before']==scene['after'] and scene['differences']=={}
    assert data['original137bones'] and data['original78Actions'] and len(data['original13muted_bridges'])==13
    assert sum(r['bones'] for r in data['original_rigs'])==137 and len(data['original_rigs'])==4
    assert data['source_pre_post_sha256']=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
    assert data['graph_completeness_status']=='COMPLETE_ENUMERATED_CURVE_GRAPH' and data['all_original_curves_attributed']
    assert data['exports_activations_saves']==0 and data['fps']==24 and data['fps_base']==1
    original_inventory=load(LAB/'evidence/model-handoff-r4/R4.json')
    names=['MESHY_R2_BODY_Idle','MESHY_R2_FACE_Idle','MESHY_R2_GAZE_Idle','MESHY_R2_HAIR_Idle']
    assert [a['exact_Action'] for a in data['Actions']]==names
    table=[]
    for a in data['Actions']:
        assert a['curve_fingerprint']==original_inventory['fingerprints']['actions'][a['exact_Action']]==scene['before']['actions'][a['exact_Action']]
        assert a['complete_original_curve_attribution'] and a['graph_completeness_status']=='COMPLETE_ENUMERATED_CURVE_GRAPH'
        assert a['frame_range']==[1,73] and len(a['slots'])==1
        s=a['slots'][0];assert s['complete_original_curve_attribution'] and s['unresolved_bag_count']==0 and not s['missing_API_records']
        curves=[f for b in s['channelbags'] for f in b.get('fcurves',[])]
        assert len(curves)==s['attributed_curve_count']>0
        assert sum(1 for b in s['channelbags'] if b.get('slot_handle')==s['actual_handle'])==s['matched_channelbag_count']==1
        for c in s['candidate_compatibility']:
            assert c['complete_original_curve_attribution'] and c['curves_checked']==len(curves)
            assert c['compatible_all_original_curves']==(not c['failed_paths'])
        compatible=[c for c in s['candidate_compatibility'] if c['compatible_all_original_curves']]
        assert len(compatible)==1
        match=compatible[0]
        table.append({'exact_Action':a['exact_Action'],'slot_identifier':s['identifier'],'slot_handle':s['actual_handle'],'target_id_type':s['target_id_type'],'complete_attributed_curves':len(curves),'complete_channelbags':1,'unresolved_bags':0,'existing_owner_references':a['actual_owner_references'],'unique_RNA_compatible_candidate':match['target'],'KEY_mesh_owner_IDs':match['mesh_owner_Object_IDs'],'actual_target_intent':'UNBOUND_NO_ASSIGNMENT; candidate compatibility only','curve_fingerprint':a['curve_fingerprint'],'source_range':[1,73],'fps':24,'fps_base':1,'endpoint_closure':'NOT_RUN','RNA_paths':[{'path':c['RNA_path'],'array_index':c['array_index'],'keyframe_count':c['keyframe_count'],'curve_fingerprint':c['original_curve_fingerprint']} for c in curves]})
    origins=[load(OUT/f'ADDON_ORIGIN_INVENTORY_{phase}_R2.json') for phase in ['BEFORE','AFTER']]
    for o in origins:
        assert o['status']=='PASS_PINNED_INSTALLED_ORIGINS_ONLY' and not o['errors'] and o['installed_python_files_checked']==315
        for m in o['modules']:assert sha(Path(m['resolved_origin']))==m['origin_sha256']
    assert origins[0]['preferences_module_names']==origins[1]['preferences_module_names'] and origins[0]['loaded_enabled_module_names']==origins[1]['loaded_enabled_module_names']
    canonical_names={k:review[k] for k in ['launcher_sha256','collector_sha256','config_sha256','proposal_sha256','blender_sha256']}
    assert canonical_names['collector_sha256']==sha(LAB/'scripts/r4_original_idle_slot_graph_inspect_r2.py')
    assert canonical_names['launcher_sha256']==sha(LAB/'scripts/r4_original_idle_slot_graph_launcher_r2.py')
    assert canonical_names['config_sha256']==sha(PREP/'FIXED_ROUTE_CONFIG_R2.json') and canonical_names['proposal_sha256']==sha(PREP/'INSPECTION_PROPOSAL_R2.json')
    summary={'status':'ACTUAL_COMPLETE_ENUMERATED_IDLE_GRAPH_UNBOUND_UNIQUE_COMPATIBLE_CANDIDATES','guard_status':guard['guard_status'],'data_status':data['status'],'pid':guard['pid'],'creation_FILETIME':guard['creation_FILETIME'],'guard_parent_pid':guard['guard_parent_pid'],'original137bones78Actions13muted':True,'source_scene_before_after_exact':True,'source_and_all_six_input_SHA_prepost_exact':True,'six_inputs':proposal['inputs'],'exact_review_bindings':canonical_names,'review_receipt_sha256':sha(OUT/'PM_APPROVAL_ORIGINAL_IDLE_GRAPH_R2.json'),'fps':24,'fps_base':1,'source_range':[1,73],'Action_slot_candidate_table':table,'target_assignment':'NONE','original_KEY_vs_pose':'FACE remains native Key curves on actual Key ID; no face rig pose substitute','playback_export_loop_visual_quality':'NOT_RUN_NOT_ACCEPTED','whole_guard_terminal':{k:guard[k] for k in ['terminal_owned_handle_exit_code','terminal_job_accounting','terminal_job_pids','cleanup_owned_handle_signaled','cleanup_owned_handle_exit_code','cleanup_job_accounting_before_close','cleanup_job_pids_before_close','job_close_success','owned_process_signaled_after_job_close','cleanup_errors']},'resource_minima_bytes':{k:min(x[k] for x in guard['resource_samples']) for k in ['free_RAM_bytes','free_C_bytes']},'native_job_limit_readback':guard['native_job_limit_readback'],'wall_seconds':guard['wall_seconds'],'raw_file_custody':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in originals},'next_bounded_prep':'Exact-target original four Idle activation/sampling approval using these candidates and real slot handles, preserving13mutes; first native endpoint2cycle/actual Key-gaze-hair output receipts, then separate compatible transport/export review. No activation authorized by this result.'}
    E.mkdir(parents=True);write(E/'INDEPENDENT_IDLE_GRAPH_BINDING_SUMMARY_R2.json',summary)
    # Full candidate failure/driver graph stays private; public summary is metadata.
    for p in originals:
        if p.name=='IDLE_SLOT_GRAPH_RESULT_R1.json':continue
        shutil.copyfile(p,E/p.name);assert sha(E/p.name)==sha(p)
    write(OUT/'INDEPENDENT_IDLE_GRAPH_BINDING_SUMMARY_R2.json',summary)
    packet=OUT/'YURI_O1_ORIGINAL_IDLE_GRAPH_ACTUAL_R2.zip'
    files=originals+[OUT/'INDEPENDENT_IDLE_GRAPH_BINDING_SUMMARY_R2.json']+[PREP/'INSPECTION_PROPOSAL_R2.json',PREP/'FIXED_ROUTE_CONFIG_R2.json']+[LAB/'scripts/r4_original_idle_slot_graph_inspect_r2.py',LAB/'scripts/r4_original_idle_slot_graph_launcher_r2.py']
    with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,p.name)
    with zipfile.ZipFile(packet) as z:
        assert z.testzip() is None
        for p in files:assert hashlib.sha256(z.read(p.name)).hexdigest()==sha(p)
    custody={'status':summary['status'],'private_packet':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'CRC_and_member_SHA_verified':True,'members':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in files},'raw_graph_private_not_geometry':True,'source_model_or_export_in_packet':False}
    write(E/'PACKET_CUSTODY_R2.json',custody);write(OUT/'PACKET_CUSTODY_R2.json',custody)
    print(json.dumps({'status':summary['status'],'packet_bytes':packet.stat().st_size,'packet_sha256':sha(packet),'candidates':[r['unique_RNA_compatible_candidate']['ID_name'] for r in table],'reference_counts':[len(r['existing_owner_references']) for r in table]}))

if __name__=='__main__':main()
