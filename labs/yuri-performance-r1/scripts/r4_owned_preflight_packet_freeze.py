"""Freeze actual harmless-child receipts + additive V5 helpers; never launch anything."""
from pathlib import Path
import ast,hashlib,importlib.util,json,shutil,subprocess,sys,zipfile
LAB=Path(__file__).resolve().parent.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-owned-job-and-acquisition-v5-r1';E=LAB/'evidence'/OUT.name
assert not OUT.exists(),'immutable new packet only'
OUT.mkdir();E.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf8'))
def copy(p,name):
    target=OUT/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
def write(n,v):
    p=OUT/n;p.write_text(json.dumps(v,indent=2),encoding='utf8');return p
failed=BASE/'o1-owned-windows-job-preflight-r1';success=BASE/'o1-owned-windows-job-preflight-r2'
for root,label in ((failed,'failed-attempt-r1'),(success,'actual-attempt-r2')):
    for p in root.iterdir():
        if p.is_file():copy(p,'preflight/'+label+'/'+p.name)
preflight=load(success/'OWNED_WINDOWS_JOB_PREFLIGHT_MANIFEST.json')
assert preflight['status']=='PASS_SUCCESS_AND_TIMEOUT_OWNED_JOB'
assert sha(success/'used_script.py')==preflight['source']['SHA256']
for row in preflight['cases']:
    assert row==load(success/(row['case']+'.json')) and row['status']=='PASS' and row['active_after_exit']==0
    assert row['large_download_approval_flag_used'] is False and row['unrelated_process_handles']==0
source=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
actions=BASE/'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'
assert sha(source)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
assert sha(actions)=='6874ec69d5721f385d31edaa06ef0d58c89a543b98bacd961f8f575ff57eef4d'
workflow=LAB/'scripts/native_readback_proposal'
names=('owned_windows_capture_supervisor_v5.py','staged_native_acquisition_v5.py','validate_owned_native_capture.py')
checks=[]
for name in names:
    p=workflow/name;ast.parse(p.read_text(encoding='utf8'));copy(p,'workflow/'+name)
    spec=importlib.util.spec_from_file_location('nonexecuting_'+p.stem,p)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    result=subprocess.run([sys.executable,str(p)],capture_output=True,text=True,encoding='utf8') if 'v5' in name else None
    if result:assert result.returncode==0
    checks.append({'path':name,'sha256':sha(p),'AST':'PASS','safe_import':'PASS',
                   'dry_exit_code':result.returncode if result else None,'dry_stdout':result.stdout if result else None})
plan=BASE/'o1-guarded-native-resource-sizing-r1/ACQUISITION_PLAN.json'
deps=BASE/'o1-guarded-native-resource-sizing-r1/WINDOWS_DEPS_EXACT_PAYLOAD_MANIFEST.json'
tools=load(LAB/'evidence/o1-guarded-native-resource-sizing-r2/EXISTING_STAGING_TOOLS.json')
template={'status':'REQUIRES_REAL_OWNER_APPROVAL_NOT_GRANTED','human_large_resource_acquisition_approved':False,
 'approved_known_payload_bytes':7054121984,'Git_transport_overhead_acknowledged':False,
 'acquisition_plan_sha256':sha(plan),'Windows_deps_manifest_sha256':sha(deps),
 'acquisition_script_sha256':sha(workflow/'staged_native_acquisition_v5.py'),
 'allowed_tools':{p:row['sha256'] for p,row in tools.items()},
 'scope':'isolated download/verify/unpack only; no source/GUI/product/global install/build/capture',
 'note':'Template is deliberately non-executable until actual human approval is evidenced; no fake approval flag used by preflight.'}
write('ACQUISITION_REVIEW_TEMPLATE_NOT_APPROVED.json',template)
write('V5_DRY_SYNTAX_IMPORT.json',{'checks':checks,'OS_job_scope':'Only harmless child preflight R2 is actual; V5 acquisition/capture supervisor itself unrun'})
report='''# Owned Windows Job preflight + acquisition helper V5

Actual separate harmless-child preflight used existing Python only, no acquisition approval flag. Success PID131604 exited0: Job Active was1 immediately after process wait, then0 after25.21ms bounded drain. Timeout PID49028 was terminated only through its owned Job, exit88/Active0. Original failed R1 attempt/log/helper are preserved; its receipt did not distinguish which conjunct failed, so that failure's cause is not retrospectively claimed proved.

This accepts only Windows SDK suspended creation→assignment→resume, normal and timeout owned-child cleanup. RAM cap enforcement/child-limit negative tests/kill-on-close-trigger experiment, actual acquisition/build/native pipeline remain untested. No Blender or GPU process was launched or attached; GUI129152 stayed present. Source and Action library hashes remain immutable.

Additive V5 supervisor now polls actual Job accounting for up to1sec after process wait while retaining strict Active==0 and wall/free-resource rejection. Actual exit/accounting/drain values are logged before completion assertion. Old V4/R2 packet/diff/helpers are preserved. V5 acquisition uses this supervisor and explicit UTF-8 JSON/source read/write; helper identity is pinned by SHA in the separate approval template. AST/safe imports/default dry CLI passed; proposed resource root still absent.

Concrete next command after the real human approves the known7,054,121,984bytes + unknown Git pack/protocol:

```powershell
& 'C:\\Program Files\\Python313\\python.exe' '<packet>\\workflow\\staged_native_acquisition_v5.py' --execute --approval '<owner-reviewed-acquisition-receipt.json>'
```

`ACQUISITION_REVIEW_TEMPLATE_NOT_APPROVED.json` contains exact plan/dependency/helper/tool hashes and approval=false. It is a review template, not consent. Execution only creates C:/YuriTransfer/native-cycles-readback-r1 and downloads/verifies/unpacks there. No compiler installer execution/global PATH/registry changes; no build or capture follows acquisition automatically. Native arithmetic hook remains unimplemented and actual Cycles/Unity/PBR remain HOLD. R4 appearance correction/6-reaction native playback proof is unchanged.
'''
for root in (OUT,E):(root/'OWNED_JOB_PREFLIGHT_AND_V5_ACTION.md').write_text(report,encoding='utf8')
manifest={'status':'DONE_SCOPED_ACTUAL_OWNED_CHILD_PREFLIGHT_V5_ACTION_EXECUTION_HOLD',
 'preflight':preflight,'source_R4_SHA256':sha(source),'Action_library_SHA256':sha(actions),
 'GUI_PID_preserved':129152,'harmless_child_processes':2,'failed_initial_harmless_attempts':1,
 'large_download_build_Blender_GPU_capture_jobs':0,'actual_native_Cycles_PBR':'HOLD',
 'V4_R2_packet_unchanged_SHA256':sha(BASE/'o1-guarded-native-resource-sizing-r2/GUARDED_NATIVE_RESOURCE_MANIFEST.json'),
 'files':[{'path':str(p.relative_to(OUT)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]}
for root in (OUT,E):(root/'OWNED_PREFLIGHT_V5_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
for n in ('ACQUISITION_REVIEW_TEMPLATE_NOT_APPROVED.json','V5_DRY_SYNTAX_IMPORT.json'):
    shutil.copyfile(OUT/n,E/n)
target=Path(r'C:/YuriTransfer/outbox')/('YURI_O1_OWNED_JOB_V5_20261003_'+sha(OUT/'OWNED_PREFLIGHT_V5_MANIFEST.json')[:12])
target.mkdir();archive=target/'YURI_O1_OWNED_JOB_V5_20261003.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_STORED) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file():z.write(p,str(p.relative_to(OUT)))
    z.write(Path(__file__),'scripts/'+Path(__file__).name)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for row in manifest['files']:
        assert hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
custody={'archive':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive),'zip_CRC_and_member_hashes':'PASS'}
for root in (OUT,E,target):(root/'PACKET_CUSTODY.json').write_text(json.dumps(custody,indent=2),encoding='utf8')
print(json.dumps(custody))
