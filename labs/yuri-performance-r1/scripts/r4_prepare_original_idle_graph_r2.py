"""File-only completeness correction; preserves frozen graph preparation R1."""
from pathlib import Path
import ast,hashlib,json,zipfile
LAB=Path(__file__).resolve().parent.parent;S=LAB/'scripts'
R1=LAB/'evidence/o1-original-idle-slot-graph-preparation-r1'
E=LAB/'evidence/o1-original-idle-slot-graph-preparation-r2'
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
INSPECT=S/'r4_original_idle_slot_graph_inspect_r2.py'
LAUNCHER=S/'r4_original_idle_slot_graph_launcher_r2.py'

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def write(n,v):
    with (E/n).open('x',encoding='utf8') as f:json.dump(v,f,indent=2)

def main():
    assert not E.exists() and not INSPECT.exists() and not LAUNCHER.exists()
    old=S/'r4_original_idle_slot_graph_inspect_r1.py'
    assert sha(old)=='8684933ba08afa14f7e6f329c01983eca7ead079ea70a2b8b1554705b616c027'
    oldlaunch=S/'r4_original_idle_slot_graph_launcher_r1.py'
    assert sha(oldlaunch)=='4a5970c2789d0d2b6c1b30b33f1f667b40b698b08d14a6a1f5c3acb5a7d82e64'
    code=old.read_text(encoding='utf8')
    for a,b in [('o1-original-idle-slot-graph-inspection-r1','o1-original-idle-slot-graph-inspection-r2'),('evidence/o1-original-idle-slot-graph-preparation-r1','evidence/o1-original-idle-slot-graph-preparation-r2'),('PM_APPROVAL_ORIGINAL_IDLE_GRAPH_R1.json','PM_APPROVAL_ORIGINAL_IDLE_GRAPH_R2.json'),('INSPECTION_PROPOSAL_R1.json','INSPECTION_PROPOSAL_R2.json')]:code=code.replace(a,b)
    code=code.replace('            bags=[];curves=[]','            bags=[];curves=[];unresolved_bags=0;missing_apis=[];matched_bags=0\n            known_handles={s.handle for s in a.slots}')
    oldblock="                    for bi,bag in enumerate(getattr(strip,'channelbags',[])):\n                        handle=getattr(bag,'slot_handle',None)\n                        if handle is None:\n                            bags.append({'layer':li,'strip':si,'bag':bi,'slot_handle':'UNKNOWN_API_FIELD','cannot_attribute_curves':True});continue\n                        if handle!=slot.handle:continue\n                        paths=[]"
    newblock="                    if not hasattr(strip,'channelbags'):\n                        missing_apis.append({'layer':li,'strip':si,'reason':'MISSING_CHANNELBAGS_API'});continue\n                    for bi,bag in enumerate(strip.channelbags):\n                        handle=getattr(bag,'slot_handle',None)\n                        if handle is None or handle not in known_handles:\n                            unresolved_bags+=1\n                            bags.append({'layer':li,'strip':si,'bag':bi,'slot_handle':'UNKNOWN_API_FIELD' if handle is None else handle,'cannot_attribute_curves':True,'reason':'UNKNOWN_HANDLE_OR_ORPHAN_BAG'});continue\n                        if handle!=slot.handle:continue\n                        matched_bags+=1\n                        if not hasattr(bag,'fcurves'):\n                            missing_apis.append({'layer':li,'strip':si,'bag':bi,'reason':'MISSING_FCURVES_API'});continue\n                        paths=[]"
    assert oldblock in code;code=code.replace(oldblock,newblock)
    code=code.replace('            candidates=[]',"            complete_attribution=(unresolved_bags==0 and not missing_apis and matched_bags>0 and len(curves)>0)\n            incomplete_reasons=[]\n            if unresolved_bags:incomplete_reasons.append('UNRESOLVED_CHANNELBAG_HANDLES')\n            if missing_apis:incomplete_reasons.append('MISSING_CHANNELBAG_OR_FCURVE_API')\n            if matched_bags==0:incomplete_reasons.append('NO_MATCHED_CHANNELBAGS')\n            if not curves:incomplete_reasons.append('NO_ATTRIBUTED_CURVES')\n            candidates=[]")
    oldcandidate="'compatible_all_recorded_RNA_paths':bool(curves) and not failures,'curves_checked'"
    newcandidate="'compatible_all_recorded_RNA_paths':bool(curves) and not failures,'complete_original_curve_attribution':complete_attribution,'compatible_all_original_curves':(not failures) if complete_attribution else None,'compatibility_status':('COMPATIBLE_COMPLETE_ENUMERATED_CURVES' if not failures else 'INCOMPATIBLE_COMPLETE_ENUMERATED_CURVES') if complete_attribution else 'UNKNOWN_INCOMPLETE_GRAPH','curves_checked'"
    assert oldcandidate in code;code=code.replace(oldcandidate,newcandidate)
    code=code.replace("'channelbags':bags,'candidate_compatibility':candidates", "'channelbags':bags,'matched_channelbag_count':matched_bags,'attributed_curve_count':len(curves),'unresolved_bag_count':unresolved_bags,'missing_API_records':missing_apis,'complete_original_curve_attribution':complete_attribution,'graph_completeness_status':'COMPLETE_ENUMERATED_CURVE_GRAPH' if complete_attribution else 'UNKNOWN_INCOMPLETE_GRAPH','incomplete_reasons':incomplete_reasons,'candidate_compatibility':candidates")
    code=code.replace("'slots':slots,'actual_owner_references':references", "'slots':slots,'complete_original_curve_attribution':bool(slots) and all(s['complete_original_curve_attribution'] for s in slots),'graph_completeness_status':'COMPLETE_ENUMERATED_CURVE_GRAPH' if slots and all(s['complete_original_curve_attribution'] for s in slots) else 'UNKNOWN_INCOMPLETE_GRAPH','actual_owner_references':references")
    code=code.replace("    write('IDLE_SLOT_GRAPH_RESULT_R1.json',{'status':'ORIGINAL_IDLE_GRAPH_READ_ONLY_NOT_TARGET_ASSIGNMENT_OR_PLAYBACK_PASS'", "    all_complete=all(a['complete_original_curve_attribution'] for a in actions)\n    write('IDLE_SLOT_GRAPH_RESULT_R1.json',{'status':'ORIGINAL_IDLE_GRAPH_READ_ONLY_NOT_TARGET_ASSIGNMENT_OR_PLAYBACK_PASS' if all_complete else 'UNKNOWN_INCOMPLETE_GRAPH','graph_completeness_status':'COMPLETE_ENUMERATED_CURVE_GRAPH' if all_complete else 'UNKNOWN_INCOMPLETE_GRAPH','all_original_curves_attributed':all_complete")
    with INSPECT.open('x',encoding='utf8',newline='\n') as f:f.write(code)
    launch=oldlaunch.read_text(encoding='utf8')
    changes={'o1-original-idle-slot-graph-inspection-r1':'o1-original-idle-slot-graph-inspection-r2','evidence/o1-original-idle-slot-graph-preparation-r1/FIXED_ROUTE_CONFIG_R1.json':'evidence/o1-original-idle-slot-graph-preparation-r2/FIXED_ROUTE_CONFIG_R2.json','evidence/o1-original-idle-slot-graph-preparation-r1/INSPECTION_PROPOSAL_R1.json':'evidence/o1-original-idle-slot-graph-preparation-r2/INSPECTION_PROPOSAL_R2.json','r4_original_idle_slot_graph_inspect_r1.py':'r4_original_idle_slot_graph_inspect_r2.py','PM_APPROVAL_ORIGINAL_IDLE_GRAPH_R1.json':'PM_APPROVAL_ORIGINAL_IDLE_GRAPH_R2.json'}
    for a,b in changes.items():launch=launch.replace(a,b)
    marker="                row['target_binding_and_playback_acceptance'] = 'NOT_CLAIMED; inspection only'"
    added="                row['graph_completeness_status'] = data['graph_completeness_status']\n                row['all_original_curves_attributed'] = data['all_original_curves_attributed']\n"
    assert marker in launch;launch=launch.replace(marker,added+marker)
    reverse=launch.replace(added,'')
    for a,b in reversed(list(changes.items())):reverse=reverse.replace(b,a)
    assert reverse==oldlaunch.read_text(encoding='utf8')
    with LAUNCHER.open('x',encoding='utf8',newline='\n') as f:f.write(launch)
    for p in [INSPECT,LAUNCHER]:compile(ast.parse(p.read_text(encoding='utf8')),str(p),'exec')
    E.mkdir(parents=True)
    proposal=json.loads((R1/'INSPECTION_PROPOSAL_R1.json').read_bytes())
    proposal['status']='CORRECTED_R2_PREPARATION_ONLY_NEW_REVIEW_REQUIRED'
    proposal['argv'][-1]=str(INSPECT)
    proposal['new_output_directory']=str(BASE/'o1-original-idle-slot-graph-inspection-r2')
    proposal['inputs'].pop(str(old));proposal['inputs'][str(INSPECT)]={'sha256':sha(INSPECT),'bytes':INSPECT.stat().st_size}
    assert all(sha(Path(p))==r['sha256'] for p,r in proposal['inputs'].items())
    proposal['completeness_policy']={'per_slot_fields':['matched_channelbag_count','attributed_curve_count','unresolved_bag_count','missing_API_records','complete_original_curve_attribution','graph_completeness_status','incomplete_reasons'],'unknown_conditions':'Missing channelbags/fcurves API, UNKNOWN/orphan handle, no matched bags or no attributed curves => UNKNOWN_INCOMPLETE_GRAPH for slot/Action/overall graph. No compatibility fallback.','candidate_relation':'compatible_all_recorded_RNA_paths only the known subset; compatible_all_original_curves is null unless complete attribution. Both are not target intent/playback proof.','complete_definition':'All available strip channelbags enumerated, slot handle attributable, matching bag has curves, no API/handle uncertainty. Not permission to select a candidate or change source.'}
    proposal['output_schema']['IDLE_SLOT_GRAPH_RESULT_R1.json']+='; explicit slot/Action/overall completeness, UNKNOWN_INCOMPLETE_GRAPH propagates'
    write('INSPECTION_PROPOSAL_R2.json',proposal)
    config=json.loads((R1/'FIXED_ROUTE_CONFIG_R1.json').read_bytes())
    config.update(status='CORRECTED_R2_PREPARED_ONLY',launcher_sha256=sha(LAUNCHER),collector_sha256=sha(INSPECT),proposal_sha256=sha(E/'INSPECTION_PROPOSAL_R2.json'),argv=proposal['argv'],output_directory=proposal['new_output_directory'],receipt_path=str(BASE/'o1-original-idle-slot-graph-inspection-r2/PM_APPROVAL_ORIGINAL_IDLE_GRAPH_R2.json'))
    config['launch_command_argv'][2]=str(LAUNCHER)
    config['remaining_review']='New exact R2 receipt required; frozen R1 not overwritten. Strict native guard unchanged, graph completeness is separate data outcome.'
    write('FIXED_ROUTE_CONFIG_R2.json',config)
    write('APPROVAL_RECEIPT_TEMPLATE_NOT_APPROVAL_R2.json',{'scope':proposal['scope'],'approved':False,'reviewed_owned_job_terminal_behavior':False,'launcher_sha256':sha(LAUNCHER),'config_sha256':sha(E/'FIXED_ROUTE_CONFIG_R2.json'),'proposal_sha256':sha(E/'INSPECTION_PROPOSAL_R2.json'),'collector_sha256':sha(INSPECT),'blender_sha256':config['blender_sha256'],'argv':proposal['argv'],'custom_native_build_trace_capture_approved':False,'large_resource_acquisition_approved':False,'max_attempts':1,'note':'R2 schema only, NOT_APPROVAL/not installed'})
    write('STATIC_VALIDATION_R2.json',{'status':'FILE_ONLY_AST_COMPILE_AND_INPUT_HASH_REVERSE_DIFF_PASS','native_job_control_identity_resource_terminal_changes':False,'launcher_changes':'Fixed paths and explicit graph completeness data fields only','per_slot_incomplete_cases_explicit':True,'partial_compatibility_not_exhaustive':True,'actual_API_curve_completeness_target_resolution':'NOT_RUN','native_launches_probes_exports':0,'frozen_R1_source_packet_SHA':sha(R1/'YURI_O1_ORIGINAL_IDLE_SLOT_GRAPH_PREPARATION_R1.zip'),'frozen_R1_scripts_unchanged':sha(old)=='8684933ba08afa14f7e6f329c01983eca7ead079ea70a2b8b1554705b616c027' and sha(oldlaunch)=='4a5970c2789d0d2b6c1b30b33f1f667b40b698b08d14a6a1f5c3acb5a7d82e64'})
    packet=E/'YURI_O1_ORIGINAL_IDLE_SLOT_GRAPH_PREPARATION_R2.zip'
    files=[INSPECT,LAUNCHER,Path(__file__)]+[S/n for n in ['r4_appearance_signature.py','native_preservation.py','r4_installed_addon_origin_gate_r2.py']]+list(E.glob('*.json'))
    with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,p.name)
    with zipfile.ZipFile(packet) as z:
        assert z.testzip() is None
        for p in files:assert hashlib.sha256(z.read(p.name)).hexdigest()==sha(p)
    write('PACKET_CUSTODY_R2.json',{'status':'CORRECTED_R2_PREPARATION_ONLY_FINAL_REVIEW_PENDING','packet':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'inspection_sha256':sha(INSPECT),'launcher_sha256':sha(LAUNCHER),'config_sha256':sha(E/'FIXED_ROUTE_CONFIG_R2.json'),'proposal_sha256':sha(E/'INSPECTION_PROPOSAL_R2.json'),'ZIP_CRC_all_member_SHA_verified':True,'geometry_model_in_packet':False})
    print((E/'PACKET_CUSTODY_R2.json').read_text())

if __name__=='__main__':main()
