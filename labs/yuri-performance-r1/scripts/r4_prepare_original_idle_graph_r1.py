"""File-only precise read-only inspection proposal + fixed owned Job route."""
from pathlib import Path
import ast,hashlib,json,zipfile
LAB=Path(__file__).resolve().parent.parent;S=LAB/'scripts'
E=LAB/'evidence/o1-original-idle-slot-graph-preparation-r1'
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
INSPECT=S/'r4_original_idle_slot_graph_inspect_r1.py'
OLD=S/'r4_exact_local_stage_launcher_r2.py'
LAUNCHER=S/'r4_original_idle_slot_graph_launcher_r1.py'

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def write(n,v):
    with (E/n).open('x',encoding='utf8') as f:json.dump(v,f,indent=2)

def main():
    assert not E.exists() and not LAUNCHER.exists()
    assert sha(OLD)=='bfd084a8f5ce622783811cb877fbb306d4f8f737d7584924077f4ebc80909b3a'
    code=OLD.read_text(encoding='utf8')
    replacements={'o1-exact-source-local-stage-capture-r2':'o1-original-idle-slot-graph-inspection-r1','evidence/o1-exact-local-stage-factory-addon-preparation-r2/FIXED_ROUTE_CONFIG_R2.json':'evidence/o1-original-idle-slot-graph-preparation-r1/FIXED_ROUTE_CONFIG_R1.json','evidence/o1-exact-local-stage-factory-addon-preparation-r2/CAPTURE_PROPOSAL_R2.json':'evidence/o1-original-idle-slot-graph-preparation-r1/INSPECTION_PROPOSAL_R1.json','r4_exact_local_stage_collector_r2.py':'r4_original_idle_slot_graph_inspect_r1.py','PM_APPROVAL_EXACT_LOCAL_CAPTURE_R2.json':'PM_APPROVAL_ORIGINAL_IDLE_GRAPH_R1.json','EXACT_TWO_FRAME_SOURCE_LOCAL_STAGE_READ_ONLY':'ORIGINAL_LIVING_IDLE_SLOT_GRAPH_READ_ONLY','CAPTURE_RESULT_R1.json':'IDLE_SLOT_GRAPH_RESULT_R1.json'}
    for a,b in replacements.items():code=code.replace(a,b)
    original_data="                row['data_files'] = [{'path': x['file'], 'actual_sha256': sha(OUT/x['file']), 'declared_sha256': x['sha256']} for x in data['rows']]\n                row['data_file_hashes_match'] = all(x['actual_sha256'] == x['declared_sha256'] for x in row['data_files'])"
    assert original_data in code
    new_data="                row['data_files'] = [{'path': n, 'actual_sha256': sha(OUT/n)} for n in ['SCENE_SIGNATURE_BEFORE_AFTER.json','ADDON_ORIGIN_INVENTORY_BEFORE_R2.json','ADDON_ORIGIN_INVENTORY_AFTER_R2.json']]\n                row['graph_schema_validated_separately'] = (data['original137bones'] is True and data['original78Actions'] is True and len(data['original13muted_bridges']) == 13 and data['original_scene_signature_differences'] == {} and {a['exact_Action'] for a in data['Actions']} == {'MESHY_R2_BODY_Idle','MESHY_R2_FACE_Idle','MESHY_R2_GAZE_Idle','MESHY_R2_HAIR_Idle'})\n                row['target_binding_and_playback_acceptance'] = 'NOT_CLAIMED; inspection only'"
    code=code.replace(original_data,new_data)
    with LAUNCHER.open('x',encoding='utf8',newline='\n') as f:f.write(code)
    for p in [INSPECT,LAUNCHER]:compile(ast.parse(p.read_text(encoding='utf8')),str(p),'exec')
    # No gate/control/cleanup changes beyond fixed scope/paths and data schema.
    reverse=code.replace(new_data,original_data)
    for a,b in reversed(list(replacements.items())):reverse=reverse.replace(b,a)
    assert reverse==OLD.read_text(encoding='utf8')
    source=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
    assert sha(source)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
    prior_config=json.loads((LAB/'evidence/o1-exact-local-stage-factory-addon-preparation-r2/FIXED_ROUTE_CONFIG_R2.json').read_bytes())
    argv=prior_config['argv'].copy();argv[-1]=str(INSPECT)
    input_files=[source,INSPECT]+[S/n for n in ['r4_appearance_signature.py','native_preservation.py','r4_installed_addon_origin_gate_r2.py']]+[LAB/'evidence/o1-exact-local-stage-factory-addon-preparation-r2/INSTALLED_BUNDLED_ADDON_ORIGIN_MANIFEST_R2.json']
    E.mkdir(parents=True)
    proposal={'status':'PREPARED_ONLY_ORIGINAL_IDLE_GRAPH_NO_LAUNCH_AUTHORIZATION','scope':'ORIGINAL_LIVING_IDLE_SLOT_GRAPH_READ_ONLY','argv':argv,'blender_sha256':prior_config['blender_sha256'],'inputs':{str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in input_files},'new_output_directory':str(BASE/'o1-original-idle-slot-graph-inspection-r1'),'exact_Actions':['MESHY_R2_BODY_Idle','MESHY_R2_FACE_Idle','MESHY_R2_GAZE_Idle','MESHY_R2_HAIR_Idle'],'reads':['Real slot identifier+handle+targetIDtype and channelbags mapped by handle, all original fcurve RNA paths/array component availability/keyframe fingerprints/modifiers','All corresponding Object and Key IDs, direct Action/slot bindings and recursively referenced NLA strips, actual Key mesh owner Object IDs','Read-only RNA-path compatibility for candidate IDs; ambiguous/unbound intent not selected','Actual fps/fps_base/effectivefps/current frame, original4rig137bone graph/rest fingerprints,13muted bridge expressions and unchanged full scene/source hashes','Pinned installed origin before/after and315Python file SHA'], 'mutations':'NONE_TO_SOURCE; no Action assignment/activation, no new NLA, no curve changes, no bridge unmute, no sampling to other frame, no export/save/model rewrite','snapshot_note':'Existing full-scene signature helper reevaluates current source frame for OFF signature; no frame value change or different-action playback. Evaluated mesh caches read only; no GPU/render.','output_schema':{'IDLE_SLOT_GRAPH_RESULT_R1.json':'Exact Action/slot/channelbag/RNA records, candidate compatibility and existing binding references separately, Key mesh-owner IDs, four rig metadata, actual fps/base and original13mutes','SCENE_SIGNATURE_BEFORE_AFTER.json':'All original source components/hashes and differences{} required','ADDON_ORIGIN_INVENTORY_BEFORE_AFTER_R2.json':'Existing pinned installed-origin gate files; no preferences edit','OWNED_JOB_RESULT_R1.json':'Strict whole guard result separate from graph inspection status and target/playback acceptance'},'unknown_API_policy':'Missing channelbag slot_handle is explicitly reported UNKNOWN_API_FIELD and unassigned curves; empty/unattributed channels do not produce compatible target or owner proof','acceptance':'Read-only graph custody only, not target authoring intent/playback/export/KEY transport/PBR acceptance','later_sampling_export':'Separate review after targets resolved; never use generic firstOBJECT fallback or substitute sampled rig pose for original KEY curves','budget':{'active_processes':1,'threads':2,'affinity':3,'job_process_memory_bytes':8*1024**3,'watchdog_seconds':120,'free_RAM_min':12*1024**3,'free_C_min':100*1024**3,'original_frames_read':1,'different_frames_sampled':0,'output_expected_upper_bytes':16*1024**2,'estimates_not_measured':True},'approval_pending':True,'native_build_download_GPU_network_render':False}
    write('INSPECTION_PROPOSAL_R1.json',proposal)
    config=prior_config.copy()
    config.update(status='PREPARED_ONLY_IDLE_GRAPH_FIXED_ROUTE',scope=proposal['scope'],launcher_sha256=sha(LAUNCHER),collector_sha256=sha(INSPECT),proposal_sha256=sha(E/'INSPECTION_PROPOSAL_R1.json'),argv=argv,output_directory=proposal['new_output_directory'],receipt_path=str(BASE/'o1-original-idle-slot-graph-inspection-r1/PM_APPROVAL_ORIGINAL_IDLE_GRAPH_R1.json'))
    config['launch_command_argv']=prior_config['launch_command_argv'].copy();config['launch_command_argv'][2]=str(LAUNCHER)
    config['remaining_review']='New one-attempt exact graph inspection receipt needed. No launch/probe or export authorized by preparation.'
    write('FIXED_ROUTE_CONFIG_R1.json',config)
    write('APPROVAL_RECEIPT_TEMPLATE_NOT_APPROVAL_R1.json',{'scope':proposal['scope'],'approved':False,'reviewed_owned_job_terminal_behavior':False,'launcher_sha256':sha(LAUNCHER),'config_sha256':sha(E/'FIXED_ROUTE_CONFIG_R1.json'),'proposal_sha256':sha(E/'INSPECTION_PROPOSAL_R1.json'),'collector_sha256':sha(INSPECT),'blender_sha256':config['blender_sha256'],'argv':argv,'custom_native_build_trace_capture_approved':False,'large_resource_acquisition_approved':False,'max_attempts':1,'note':'NOT_APPROVAL; not copied to execution receipt path'})
    write('STATIC_VALIDATION_R1.json',{'status':'SAVED_FILE_AST_COMPILE_AND_FIXED_ROUTE_DIFF_ONLY_PASS','Blender_launcher_probes_executed':0,'original_source_hash_verified':True,'inspection_AST_compile':True,'guard_native_job_logic_identical_to_reviewed_R2_except_paths_scope_data_schema':True,'BlenderAPI_slot_handle_recursive_NLA_RNA_resolution':'NOT_RUN','real_target_binding_compatibility':'PENDING_ACTUAL_READ','original_graph_source_signature_rest_mute_preservation':'MANDATORY_NATIVE_RECEIPT_NOT_REPRODUCED_HERE','export_or_assignment':False})
    packet=E/'YURI_O1_ORIGINAL_IDLE_SLOT_GRAPH_PREPARATION_R1.zip'
    files=[INSPECT,LAUNCHER,Path(__file__),S/'r4_appearance_signature.py',S/'native_preservation.py',S/'r4_installed_addon_origin_gate_r2.py']+list(E.glob('*.json'))
    with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,p.name)
    with zipfile.ZipFile(packet) as z:
        assert z.testzip() is None
        for p in files:assert hashlib.sha256(z.read(p.name)).hexdigest()==sha(p)
    write('PACKET_CUSTODY_R1.json',{'status':'FILE_ONLY_INSPECTION_PREPARATION_PM_REVIEW_PENDING','packet':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'inspection_sha256':sha(INSPECT),'launcher_sha256':sha(LAUNCHER),'config_sha256':sha(E/'FIXED_ROUTE_CONFIG_R1.json'),'proposal_sha256':sha(E/'INSPECTION_PROPOSAL_R1.json'),'ZIP_CRC_member_SHA_verified':True,'source_geometry_or_model_in_packet':False})
    print((E/'PACKET_CUSTODY_R1.json').read_text())

if __name__=='__main__':main()
