"""Additive file-only raw forensic/exact AnimData restoration packet builder."""
from pathlib import Path
import ast,hashlib,json,zipfile
LAB=Path(__file__).resolve().parent.parent;S=LAB/'scripts'
R2=LAB/'evidence/o1-original-idle-sampling-preparation-r2'
E=LAB/'evidence/o1-original-idle-sampling-preparation-r3'
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-original-idle-sampling-r3'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(n,v):
    with (E/n).open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
def main():
    assert not E.exists()
    old=[S/n for n in ['r4_original_idle_sample_r2.py','r4_original_idle_sample_launcher_r2.py','r4_audit_original_idle_sample_r2.py']]
    expected=['fb44ed96ebb07ad1c2b55cd2619828a97ca6ecdaa1bf366b24f9f2d79334f416','b6890cb38139340a7c2693d001708ecf68125a2a6e48d2a7fd89224de237564b','1a6c2ddaf92becf2d2b2043958ac660f9907dbe4733290780446b2bea7b0b94d']
    assert [sha(p) for p in old]==expected
    new=[p.with_name(p.name.replace('_r2.py','_r3.py')) for p in old]
    assert not any(p.exists() for p in new)
    changes={a:b for a,b in [
      ('o1-original-idle-sampling-r2','o1-original-idle-sampling-r3'),
      ('o1-original-idle-sampling-preparation-r2','o1-original-idle-sampling-preparation-r3'),
      ('r4_original_idle_sample_r2.py','r4_original_idle_sample_r3.py'),
      ('PM_APPROVAL_ORIGINAL_IDLE_SAMPLE_R2.json','PM_APPROVAL_ORIGINAL_IDLE_SAMPLE_R3.json'),
      ('SAMPLING_PROPOSAL_R2.json','SAMPLING_PROPOSAL_R3.json'),
      ('FIXED_ROUTE_CONFIG_R2.json','FIXED_ROUTE_CONFIG_R3.json'),
      ('IDLE_SAMPLING_RESULT_R2.json','IDLE_SAMPLING_RESULT_R3.json'),
      ('TERMINAL_FILE_CUSTODY_R2.json','TERMINAL_FILE_CUSTODY_R3.json')]}
    codes=[]
    for p in old:
        code=p.read_text(encoding='utf8')
        for a,b in changes.items():code=code.replace(a,b)
        codes.append(code)
    base_collector=codes[0];base_auditor=codes[2]
    importline='from r4_idle_raw_forensics_r3 import capture,raw_diff,save_ad,restore_all\n'
    codes[0]=codes[0].replace('LAB=HERE.parent\n',importline+'LAB=HERE.parent\n')
    codes[0]=codes[0].replace('    before=snapshot(actions)\n',"    before=snapshot(actions)\n    capture('BEFORE',before,OUT)\n")
    codes[0]=codes[0].replace("'had_ad':ad is not None,'original_action'","'had_ad':ad is not None,'original_ad_fields':save_ad(ad),'original_action'")
    codes[0]=codes[0].replace("        write('ON_SOURCE_SIGNATURE_R1.json',on_snapshot)\n","        write('ON_SOURCE_SIGNATURE_R1.json',on_snapshot)\n        capture('ON',on_snapshot,OUT)\n")
    begin=codes[0].index('    finally:\n        for r in resolved:')
    end=codes[0].index("        assert modifier_fingerprint==",begin)
    old_finally=codes[0][begin:end]
    new_finally='''    finally:
        # Evidence precedes every restoration verdict; no original error is discarded.
        write('PRIMARY_SAMPLING_ERROR_R3.json',{'error':error,'frames_recorded':len(records)})
        ledger=restore_all(resolved,object_state,pose_state,key_state,saved_frame,restore_channels,OUT)
        after=snapshot(actions)
        diff=difference(before,after)
        write('SCENE_SIGNATURE_BEFORE_AFTER.json',{'before':before,'after':after,'differences':diff})
        capture('AFTER',after,OUT)
        fields=raw_diff(OUT)
        structural_after=structural_graph(owners)
        write('STRUCTURAL_RESTORED_R1.json',{'after':structural_after,'same_before_after':structural_before==structural_after})
        ledger_errors=[i for i,r in enumerate(ledger) if 'error' in r or r.get('exact') is False or r.get('success') is False or r.get('readback_none') is False]
        write('FORENSIC_RESTORATION_VERDICT_R3.json',{'full_signature_differences':diff,'raw_difference_count':len(fields),'ledger_error_indices':ledger_errors,'driver_NLA_same':structural_before==structural_after,'primary_sampling_error_preserved':error is not None,'no_exclusions_or_epsilon':True})
        origin_after=inspect_and_require(bpy,origin_manifest,OUT,'after')
        assert origin_before['preferences_module_names']==origin_after['preferences_module_names'] and origin_before['loaded_enabled_module_names']==origin_after['loaded_enabled_module_names']
        assert not diff,diff
        assert not fields,'Exact raw Object/Key/UI/fingerprint inputs differ; see private raw diff'
        assert not ledger_errors,ledger_errors
        assert structural_before==structural_after,'Driver/NLA structure restore mismatch'
'''
    codes[0]=codes[0][:begin]+new_finally+codes[0][end:]
    # Independent auditor recomputes exact original object/mesh hashes from durable raw inputs.
    addition='''    raw_phases={}
    for phase,sig in [('BEFORE',scene['before']),('ON',on),('AFTER',scene['after'])]:
        with gzip.open(OUT/f'RAW_FINGERPRINT_INPUTS_{phase}_PRIVATE_R3.json.gz','rt') as f:raw_phases[phase]=json.load(f)
        raw=raw_phases[phase]
        for category in ['objects','mesh_attributes']:
            hashes={name:hashlib.sha256(json.dumps(payload,separators=(',',':')).encode()).hexdigest() for name,payload in raw[category].items()}
            assert hashes==sig[category],('raw recomputation',phase,category)
        proof=load(f'RAW_RECOMPUTED_HASHES_{phase}_R3.json')
        assert all(proof['exact_original_signature_matches'].values())
    assert raw_phases['BEFORE']==raw_phases['AFTER']
    raw_phases.clear()
    verdict=load('FORENSIC_RESTORATION_VERDICT_R3.json')
    assert not verdict['full_signature_differences'] and verdict['raw_difference_count']==0 and not verdict['ledger_error_indices'] and verdict['driver_NLA_same']
    assert load('RAW_FIELD_DIFF_PATHS_R3.json')['difference_count']==0
    with gzip.open(OUT/'RAW_FIELD_DIFF_PRIVATE_R3.json.gz','rt') as f:assert json.load(f)==[]
'''
    marker="    structural=load('STRUCTURAL_OFF_ON_OFF_R1.json');restored=load('STRUCTURAL_RESTORED_R1.json')"
    assert marker in codes[2];codes[2]=codes[2].replace(marker,addition+marker)
    reverse_col=codes[0].replace(importline,'').replace("    capture('BEFORE',before,OUT)\n",'').replace("'had_ad':ad is not None,'original_ad_fields':save_ad(ad),'original_action'","'had_ad':ad is not None,'original_action'").replace("        capture('ON',on_snapshot,OUT)\n",'').replace(new_finally,old_finally)
    assert reverse_col==base_collector and codes[2].replace(addition,'')==base_auditor
    # Launcher has only fixed revision paths/names; strict guard and terminal custody unchanged.
    reverse_launch=codes[1]
    for a,b in reversed(list(changes.items())):reverse_launch=reverse_launch.replace(b,a)
    assert reverse_launch==old[1].read_text(encoding='utf8')
    helper=S/'r4_idle_raw_forensics_r3.py'
    for p,code in zip(new,codes):
        compile(ast.parse(code),str(p),'exec')
        with p.open('x',encoding='utf8',newline='\n') as f:f.write(code)
    compile(ast.parse(helper.read_text()),str(helper),'exec')
    # Serializer source expressions copied exactly from immutable original signature helper.
    original=ast.parse((S/'r4_appearance_signature.py').read_text())
    snap=next(n for n in original.body if isinstance(n,ast.FunctionDef) and n.name=='snapshot')
    helper_tree=ast.parse(helper.read_text())
    for category,function in [('objects','object_payload'),('mesh_attributes','mesh_payload')]:
        assignment=next(n for n in snap.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Subscript) and isinstance(n.targets[0].slice,ast.Constant) and n.targets[0].slice.value==category)
        expression=assignment.value.value.args[0]
        fn=next(n for n in helper_tree.body if isinstance(n,ast.FunctionDef) and n.name==function)
        assert ast.dump(expression)==ast.dump(fn.body[0].value),('Original hash input expression changed',category)
    E.mkdir(parents=True)
    proposal=json.loads((R2/'SAMPLING_PROPOSAL_R2.json').read_bytes())
    proposal['inputs'].pop(str(old[0]))
    for p in [new[0],helper]:proposal['inputs'][str(p)]={'bytes':p.stat().st_size,'sha256':sha(p)}
    proposal['argv'][-1]=str(new[0]);proposal['new_output_directory']=str(OUT)
    proposal.update(status='ADDITIVE_R3_EXACT_RAW_FORENSICS_RESTORATION_PREPARATION_ONLY',prior_frozen_packet_sha256=sha(R2/'YURI_ORIGINAL_IDLE_SAMPLING_PREPARATION_R2.zip'),forensics='Complete original Object/mesh hash input expressions AST-identical; all native Object/Key raw props/custom/anim before/ON/after; exact hash recomputation; private raw field diff without omissions/epsilon; UI and readonly schema separately captured; original sampling error and restoration ledger durable before assert',rollback='Original Action/slot and full captured AnimData props ledger, explicit slot_handle and last_slot_identifier if writable; readonly mismatch fails and records; all original transform/Key/custom values/frame restored; no existing AnimData reconstruction; exact post-frame readback; full Object/Key raw equality and complete original signature equality required',runtime_API_status='NOT_RUN: writability/order of original no-action slot metadata must be proven, no guarantee of R2 root cause or fix',scope_and_resources='Full145/four domains/all137/allKeys+drivers/allnativegeometry unchanged; guard gates unchanged; no native launch/probe',approval_pending=True)
    proposal['resource_estimate']['R3_extra_raw_phases']='Three private full Object/mesh/Key raw phase files and in-memory field diff; additional time/output/RAM unmeasured. Fixed8GiB/120s unchanged; budget failure legitimate, no reduction/retry.'
    assert all(sha(p)==r['sha256'] for p,r in proposal['inputs'].items())
    write('SAMPLING_PROPOSAL_R3.json',proposal)
    config=json.loads((R2/'FIXED_ROUTE_CONFIG_R2.json').read_bytes())
    config.update(status='R3_FORENSIC_PREPARATION_ONLY_NEW_EXACT_REVIEW_REQUIRED',launcher_sha256=sha(new[1]),collector_sha256=sha(new[0]),proposal_sha256=sha(E/'SAMPLING_PROPOSAL_R3.json'),argv=proposal['argv'],output_directory=str(OUT),receipt_path=str(OUT/'PM_APPROVAL_ORIGINAL_IDLE_SAMPLE_R3.json'),remaining_review='R3 full raw forensic packet needs exact review; consumed R2 receipt cannot authorize R3')
    config['launch_command_argv'][2]=str(new[1]);write('FIXED_ROUTE_CONFIG_R3.json',config)
    receipt=json.loads((R2/'APPROVAL_RECEIPT_TEMPLATE_NOT_APPROVAL_R2.json').read_bytes())
    receipt.update(launcher_sha256=sha(new[1]),collector_sha256=sha(new[0]),config_sha256=sha(E/'FIXED_ROUTE_CONFIG_R3.json'),proposal_sha256=sha(E/'SAMPLING_PROPOSAL_R3.json'),argv=proposal['argv'],note='R3 false template only; not installed; no native authorization')
    write('APPROVAL_RECEIPT_TEMPLATE_NOT_APPROVAL_R3.json',receipt)
    write('STATIC_VALIDATION_R3.json',{'status':'AST_COMPILE_EXACT_OBJECT_MESH_HASH_EXPRESSION_AND_REVERSE_DIFF_PASS','native_runs':0,'raw_input_expressions_AST_identical':True,'launcher_guard_terminal_custody_unchanged':True,'collector_full145_loop_unchanged':True,'R2_scripts_SHA_unchanged':[sha(p) for p in old]==expected,'rollback_native_writability_and_readbacks':'NOT_RUN','prior_root_cause':'UNPROVEN'})
    files=new+[helper,Path(__file__)]+[S/n for n in ['r4_appearance_signature.py','native_preservation.py','r4_installed_addon_origin_gate_r2.py']]+list(E.glob('*.json'))
    packet=E/'YURI_ORIGINAL_IDLE_SAMPLING_PREPARATION_R3.zip'
    with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,p.name)
    with zipfile.ZipFile(packet) as z:
        assert z.testzip() is None
        for p in files:assert hashlib.sha256(z.read(p.name)).hexdigest()==sha(p)
    write('PACKET_CUSTODY_R3.json',{'status':'PREPARATION_ONLY_NEW_R3_REVIEW_PENDING','packet':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'members':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in files},'CRC_all_member_SHA_verified':True,'original_numeric_private_data_in_packet':False})
    print(json.dumps({'bytes':packet.stat().st_size,'sha256':sha(packet),'collector_sha256':sha(new[0]),'launcher_sha256':sha(new[1]),'auditor_sha256':sha(new[2]),'forensics_helper_sha256':sha(helper)}))
if __name__=='__main__':main()
