"""File-only fixed-route preparation; no launcher/probe/Blender execution."""
from pathlib import Path
import ast, hashlib, json, zipfile

LAB = Path(__file__).resolve().parent.parent
E = LAB/'evidence/o1-exact-local-stage-launcher-preparation-r1'
OLD = LAB/'evidence/o1-exact-local-stage-preparation-r1'
LAUNCHER = LAB/'scripts/r4_exact_local_stage_launcher_r1.py'
COLLECTOR = LAB/'scripts/r4_exact_local_stage_collector_r1.py'
PROPOSAL = OLD/'CAPTURE_PROPOSAL_R1.json'
BASE = Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
R5 = LAB/'scripts/r4_readonly_source_job_guard_r5.py'

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def write(n,v):
    with (E/n).open('x',encoding='utf8') as f:json.dump(v,f,indent=2)

def main():
    assert not E.exists(), 'Do not overwrite frozen preparation'
    assert sha(PROPOSAL)=='210cd30d5c85c44317f4e10d03f0c17d486bb3bf84979238230ffac3098bffe2'
    assert sha(COLLECTOR)=='f8ab4bc7dd77f1ecdeaf843659acd9be6caf290e888f13d59862388b2136d57a'
    assert sha(R5)=='c6912b0378d9b1f626de33b4f819efb898d49432e035576e240764559fe8566c'
    tree=ast.parse(LAUNCHER.read_text(encoding='utf8'))
    compile(tree,str(LAUNCHER),'exec')
    calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='CreateProcess']
    assert len(calls)==1
    assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('Popen','run','system','OpenProcess') for n in ast.walk(tree))
    proposal=json.loads(PROPOSAL.read_bytes())
    assert all(sha(Path(p))==row['sha256'] for p,row in proposal['inputs'].items())
    E.mkdir(parents=True)
    config={
        'status':'PREPARED_FIXED_ROUTE_ONLY_NOT_RUN',
        'scope':'EXACT_TWO_FRAME_SOURCE_LOCAL_STAGE_READ_ONLY',
        'launcher_sha256':sha(LAUNCHER),'collector_sha256':sha(COLLECTOR),'proposal_sha256':sha(PROPOSAL),
        'blender_sha256':proposal['blender_sha256'],'argv':proposal['argv'],
        'output_directory':str(BASE/'o1-exact-source-local-stage-capture-r1'),
        'limits':{'affinity_mask':3,'process_memory_bytes':8*1024**3,'job_memory_bytes':8*1024**3,'active_process_limit':1,'watchdog_seconds':120,'kill_on_close':True,'creation_flags':12},
        'launch_command_argv':['C:/Program Files/Python313/python.exe','-I',str(LAUNCHER),'--run-approved-fixed-capture'],
        'python_sha256':'d87063e5597f257004c731b66c59c56c91038861c6877b1a3dca6b8c4e919125',
        'R5_logic_reference':{'path':str(R5),'sha256':sha(R5),'actual_whole_guard_status':'FAIL_PRESERVED','reuse':'Native ctypes ABI/layout, detached suspended owned Job assignment, limit flags/readback, affinity/memory/active1/resource floors and owned-only cleanup; no probe/help routes'},
        'receipt_path':str(BASE/'o1-exact-source-local-stage-capture-r1/PM_APPROVAL_EXACT_LOCAL_CAPTURE_R1.json'),
        'receipt_exists_or_created_by_preparation':False,
        'terminal_contract':{'before_image':'If exact owned handle signaled, classify terminal by exit code then drain Job','after_image':'If same owned handle became signaled, classify terminal independent of image availability; raw image error retained','LIVE_missing_image':'FAIL even if GetProcessTimes exit FILETIME or exit-code query looks terminal','normal_terminal':'exit0, total1, limit_terminated0, Active0, PIDs[] before close','failure':'No retry; terminate only assigned owned Job or own unassigned suspended child; independent cleanup queries, close guaranteed by cleanup path, retain raw receipts/partial files','separate_statuses':'guard_status separate from data_result and file hashes; neither certifies native/PBR/Unity'},
        'network':'No packet-level network sandbox claim; exact factory/offline CLI and collector empty addon gate, no account/plugin/network calls',
        'remaining_review':'Exact launcher/config/collector/proposal/argv/receipt and terminal behavior need PM approval; no runtime test/Blender/probe launched',
    }
    write('FIXED_ROUTE_CONFIG_R1.json',config)
    write('APPROVAL_RECEIPT_TEMPLATE_NOT_APPROVAL.json',{
        'scope':config['scope'],'approved':False,'reviewed_owned_job_terminal_behavior':False,
        'launcher_sha256':sha(LAUNCHER),'config_sha256':sha(E/'FIXED_ROUTE_CONFIG_R1.json'),'proposal_sha256':sha(PROPOSAL),'collector_sha256':sha(COLLECTOR),'blender_sha256':config['blender_sha256'],'argv':config['argv'],
        'custom_native_build_trace_capture_approved':False,'large_resource_acquisition_approved':False,
        'note':'Schema example only; not installed at receipt path, not launch authorization',
    })
    write('STATIC_PREPARATION_VALIDATION_R1.json',{'status':'FILE_ONLY_AST_COMPILE_AND_HASH_BINDINGS_PASS','launcher_ast_compile':True,'fixed_CreateProcess_call_count':len(calls),'probes_or_native_jobs_executed':0,'Blender_launched':False,'launcher_executed':False,'collector_executed':False,'runtime_owned_handle_image_race':'NOT_RUN','runtime_native_ABI_limit_readback':'NOT_RUN','input_dependency_hashes_verified':True,'source_proposal_unchanged':True,'R5_file_unchanged':True,'config_sha256':sha(E/'FIXED_ROUTE_CONFIG_R1.json'),'launcher_sha256':sha(LAUNCHER)})
    packet=E/'YURI_O1_EXACT_LOCAL_FIXED_ROUTE_PREPARATION_R1.zip'
    with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
        for p in [LAUNCHER,Path(__file__),COLLECTOR,PROPOSAL,E/'FIXED_ROUTE_CONFIG_R1.json',E/'APPROVAL_RECEIPT_TEMPLATE_NOT_APPROVAL.json',E/'STATIC_PREPARATION_VALIDATION_R1.json']:z.write(p,p.name)
    with zipfile.ZipFile(packet) as z:assert z.testzip() is None
    write('PACKET_CUSTODY_R1.json',{'packet':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'launcher_sha256':sha(LAUNCHER),'config_sha256':sha(E/'FIXED_ROUTE_CONFIG_R1.json'),'collector_sha256':sha(COLLECTOR),'proposal_sha256':sha(PROPOSAL),'status':'PREPARATION_ONLY_PM_REVIEW_PENDING','no_native_launch_or_probe':True})
    print((E/'PACKET_CUSTODY_R1.json').read_text())

if __name__=='__main__':main()
