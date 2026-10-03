"""File-only frozen execution packet builder. Does not execute collector/launcher."""
from pathlib import Path
import ast,hashlib,json,zipfile
LAB=Path(__file__).resolve().parent.parent
S=LAB/'scripts';E=LAB/'evidence/o1-original-idle-sampling-preparation-r1'
OLD=LAB/'evidence/o1-original-idle-slot-graph-preparation-r2'
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-original-idle-sampling-r1'
COL=S/'r4_original_idle_sample_r1.py';LAUNCH=S/'r4_original_idle_sample_launcher_r1.py'
SCOPE='ORIGINAL_IDLE_EXPLICIT_FOUR_QA_BINDING_145_FRAME_SAMPLING'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(n,v):
    with (E/n).open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
def main():
    assert not E.exists() and not LAUNCH.exists()
    oldlaunch=S/'r4_original_idle_slot_graph_launcher_r2.py'
    assert sha(oldlaunch)=='5212f0bf5c3f2ea20112afb0484bd728d78d60ab152f94b50a0048e0c477575a'
    code=oldlaunch.read_text(encoding='utf8')
    replacements={
      'o1-original-idle-slot-graph-inspection-r2':'o1-original-idle-sampling-r1',
      'evidence/o1-original-idle-slot-graph-preparation-r2/FIXED_ROUTE_CONFIG_R2.json':'evidence/o1-original-idle-sampling-preparation-r1/FIXED_ROUTE_CONFIG_R1.json',
      'evidence/o1-original-idle-slot-graph-preparation-r2/INSPECTION_PROPOSAL_R2.json':'evidence/o1-original-idle-sampling-preparation-r1/SAMPLING_PROPOSAL_R1.json',
      'r4_original_idle_slot_graph_inspect_r2.py':'r4_original_idle_sample_r1.py',
      'PM_APPROVAL_ORIGINAL_IDLE_GRAPH_R2.json':'PM_APPROVAL_ORIGINAL_IDLE_SAMPLE_R1.json',
      'ORIGINAL_LIVING_IDLE_SLOT_GRAPH_READ_ONLY':SCOPE,
      'IDLE_SLOT_GRAPH_RESULT_R1.json':'IDLE_SAMPLING_RESULT_R1.json',
    }
    for a,b in replacements.items():code=code.replace(a,b)
    start=code.index("                row['graph_schema_validated_separately']")
    end=code.index('\n            except Exception:',start)
    oldblock=code[start:end]
    newblock="                row['sampling_schema_validated_separately'] = (data['sample_count'] == 145 and data['original137bones'] is True and data['original78Actions'] is True and len(data['original13muted_bridges']) == 13 and data['original_scene_signature_differences'] == {})\n                row['target_binding_and_playback_acceptance'] = 'EXPLICIT_PM_QA_BINDINGS; NOT_VISUAL_OR_PRODUCT_ACCEPTANCE'"
    code=code[:start]+newblock+code[end:]
    reverse=code.replace(newblock,oldblock)
    for a,b in reversed(list(replacements.items())):reverse=reverse.replace(b,a)
    assert reverse==oldlaunch.read_text(encoding='utf8'), 'Guard semantics changed'
    # Strict Job/LIVE/identity/resource/watchdog/cleanup implementation untouched.
    with LAUNCH.open('x',encoding='utf8',newline='\n') as f:f.write(code)
    for p in [COL,LAUNCH,S/'r4_audit_original_idle_sample_r1.py',Path(__file__)]:compile(ast.parse(p.read_text(encoding='utf8')),str(p),'exec')
    E.mkdir(parents=True)
    graph=json.loads((LAB/'evidence/o1-original-idle-slot-graph-result-r2/INDEPENDENT_IDLE_GRAPH_BINDING_SUMMARY_R2.json').read_bytes())
    config=json.loads((OLD/'FIXED_ROUTE_CONFIG_R2.json').read_bytes())
    proposal=json.loads((OLD/'INSPECTION_PROPOSAL_R2.json').read_bytes())
    proposal={k:proposal[k] for k in ['argv','blender_sha256','inputs']}
    proposal['inputs'].pop(str(S/'r4_original_idle_slot_graph_inspect_r2.py'))
    proposal['inputs'][str(COL)]={'sha256':sha(COL),'bytes':COL.stat().st_size}
    proposal['argv'][-1]=str(COL)
    proposal.update(status='FROZEN_EXECUTABLE_PREPARATION_NOT_RUN_NOT_APPROVAL',scope=SCOPE,source_sha256='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa',new_output_directory=str(OUT),bindings=[{'exact_Action':r['exact_Action'],'target_name':r['unique_RNA_compatible_candidate']['ID_name'],'target_id_type':r['target_id_type'],'slot_identifier':r['slot_identifier'],'slot_handle':r['slot_handle'],'curve_count':r['complete_attributed_curves'],'curve_fingerprint':r['curve_fingerprint']} for r in graph['Action_slot_candidate_table']],mapping_authority='ROOT_PM_TECHNICAL_QA_CHOICE; ORIGINAL_AUTHOR_INTENT_UNKNOWN',evaluation={'frames':[1,145],'samples':145,'fps':24,'fps_base':1,'continuous_original_modifiers':True,'manual_modulo_clamp_normalize':False},readback='All386 native curve values vs original/evaluated RNA; all137 native bones/57BODY including5unanimated helpers, all Key outputs/all original drivers incl13mutes, GAZE/HAIR UI ranges/default metadata and driver variable dependencies,10hair bones14drivers; all scene object transforms and all native evaluated meshes lossless f32 eachframe',rollback='Original Action/slot/animation-data existence, object/pose transform channels, animated custom properties, all Key values and frame restored; full independent OFF->ON->OFF hashes including exact NLA tracks/strips; original curves/modifiers and sourceSHA retained',exports_saves_aliases_unmutes=0,resource_estimate={'source_mesh_vertices':190726,'geometry_raw_bytes_estimate':190726*3*4*145,'geometry_estimate_excludes_evaluated_vertex_growth':True,'private_output_upper_target_bytes':1024**3,'wall_seconds_estimate_unmeasured':[45,120],'runtime_fit_status':'UNMEASURED; full145may exceed120s and must fail retained partial, no automatic subset/retry','memory_strategy':'Stream native f32 geometry to gzip1, stream perframe JSONL; keep only386channel+137head vectors for measurements. No full-scene snapshots perframe.','sparse_semantics':'None; allframes/allchannels/fullnativegeometry retained. Any later sparse alternative needs explicit separate scope.'},budget=config['limits'],gpu_render_network_build_download=False,max_attempts=1,approval_pending=True,source_eye_attribution='Cached mesh inventory has no separately named eye meshes. Record all native evaluated meshes and transforms plus topology/material metadata, actual driver dependencies; do not invent an eye-only subset or claim eyeball attribution from names.',actual_native_validation='NOT_RUN; ID evaluated_get/driver API, modifier metadata and restoration require actual approved execution; errors fail and retain partial outputs')
    assert all(sha(p)==r['sha256'] for p,r in proposal['inputs'].items())
    write('SAMPLING_PROPOSAL_R1.json',proposal)
    config.update(status='FROZEN_PREPARATION_ONLY_NOT_RUN',scope=SCOPE,launcher_sha256=sha(LAUNCH),collector_sha256=sha(COL),proposal_sha256=sha(E/'SAMPLING_PROPOSAL_R1.json'),argv=proposal['argv'],output_directory=str(OUT),receipt_path=str(OUT/'PM_APPROVAL_ORIGINAL_IDLE_SAMPLE_R1.json'),remaining_review='Exact new sampling receipt required; prior graph receipt is not activation approval')
    config['launch_command_argv'][2]=str(LAUNCH)
    write('FIXED_ROUTE_CONFIG_R1.json',config)
    write('APPROVAL_RECEIPT_TEMPLATE_NOT_APPROVAL_R1.json',{'scope':SCOPE,'approved':False,'reviewed_owned_job_terminal_behavior':False,'launcher_sha256':sha(LAUNCH),'config_sha256':sha(E/'FIXED_ROUTE_CONFIG_R1.json'),'proposal_sha256':sha(E/'SAMPLING_PROPOSAL_R1.json'),'collector_sha256':sha(COL),'blender_sha256':config['blender_sha256'],'argv':proposal['argv'],'max_attempts':1,'custom_native_build_trace_capture_approved':False,'large_resource_acquisition_approved':False,'note':'Template only; not installed in runtime output'})
    write('STATIC_VALIDATION_R1.json',{'status':'AST_COMPILE_INPUT_HASH_AND_LAUNCHER_REVERSE_DIFF_PASS','native_runs':0,'guard_logic_unchanged':True,'guard_reference_sha256':sha(oldlaunch),'changes_only':'Fixed paths/scope/result schema; no Job/LIVE/resource/cleanup change','original_r4_source_sha256':proposal['source_sha256'],'rollback_native_validation':'NOT_RUN','independent_auditor':str(S/'r4_audit_original_idle_sample_r1.py')})
    packet=E/'YURI_ORIGINAL_IDLE_SAMPLING_PREPARATION_R1.zip'
    files=[COL,LAUNCH,S/'r4_audit_original_idle_sample_r1.py',Path(__file__)]+[S/n for n in ['r4_appearance_signature.py','native_preservation.py','r4_installed_addon_origin_gate_r2.py']]+list(E.glob('*.json'))
    with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,p.name)
    with zipfile.ZipFile(packet) as z:
        assert z.testzip() is None
        for p in files:assert hashlib.sha256(z.read(p.name)).hexdigest()==sha(p)
    write('PACKET_CUSTODY_R1.json',{'status':'PREPARATION_ONLY_NOT_NATIVE_APPROVAL','packet':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'members':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in files},'CRC_all_member_SHA_verified':True,'model_geometry_original_key_values_in_packet':False})
    print((E/'PACKET_CUSTODY_R1.json').read_text())
if __name__=='__main__':main()
