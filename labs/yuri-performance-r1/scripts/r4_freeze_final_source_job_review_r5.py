"""Freeze additive R5 source-job preparation, same-guard probes and local CLI help."""
from pathlib import Path
import ast,hashlib,importlib.util,json,shutil,zipfile
LAB=Path(__file__).resolve().parents[1];E=LAB/'evidence/o1-readonly-source-job-review-r5'
GUARD=LAB/'scripts/r4_readonly_source_job_guard_r5.py';VERIFIER=LAB/'scripts/r4_readonly_recipe_verifier_r5.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('guard_r5',GUARD);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
assert not E.exists();E.mkdir()
q=json.loads((g.OUT/'PROBE_MANIFEST.json').read_bytes())
assert q['guard_sha256']==sha(GUARD) and sha(VERIFIER)==g.VERIFIER_SHA
assert q['Blender_source_reads']==0 and q['Blender_CLI_help_launches']==1
rows=q['cases']+[q['factory_help']]
for r in rows:
    assert r['status']=='PASS' and r['total_job_processes']==1 and r['active_after_exit']==0 and r['final_job_pids']==[]
    assert r['cleanup_owned_handle_terminal'] and r['cleanup_terminal_job_accounting']['active']==0 and r['cleanup_final_job_pids']==[]
    assert r['job_limit_readback_verified'] and r['inputs_before']==r['inputs_after']
    for s in r['resources_samples']:
        assert s['free_RAM_bytes']>=12*1024**3 and s['free_C_bytes']>=100*1024**3
ast.parse(GUARD.read_text());ast.parse(VERIFIER.read_text())
assert not (g.OUT/'PM_REVIEW_SOURCE_READ_APPROVED_R5.json').exists() and not (g.OUT/'source-identity.json').exists()
F=E/'frozen';F.mkdir()
for p in [GUARD,VERIFIER,*g.OUT.glob('*.json'),*g.OUT.glob('*.log')]:shutil.copyfile(p,F/p.name)
manifest={'status':'R5_FACTORY_OFFLINE_TERMINAL_HANDLE_SAFE_PREPARED_NOT_APPROVED','guard_sha256':sha(GUARD),'verifier_sha256':sha(VERIFIER),'blender_sha256':g.BLENDER_SHA,'python_sha256':g.PYTHON_SHA,'same_R5_guard_probe_manifest_sha256':sha(g.OUT/'PROBE_MANIFEST.json'),'factory_help_log_sha256':sha(g.OUT/'factory-help.log'),'source_argv':g.source_argv(),'matching_source_and_verifier_output_path':str(g.OUT/'source-identity.json'),'approval_receipt_required_but_absent':str(g.OUT/'PM_REVIEW_SOURCE_READ_APPROVED_R5.json'),'run_AFTER_exact_PM_review_only':[str(g.PYTHON),str(GUARD),'--run-reviewed-source-read'],'PM_reviewed_exact_final_guard_verifier_argv_and_same_guard_probes':False,'human_large_resource_acquisition_approved':False,'custom_native_build_trace_capture_approved':False,'source_reads_R5':0,'CLI_help_jobs_R5':1,'source_startup_addon_isolation':'NOT_RUN; help confirms supported flags and no addon marker in help job; no claim yet about full source-open startup','terminal_race_rule':'Poll actual owned process handle before querying identity and after unavailable image result. Missing image accepted only if same owned handle terminal; wrong PID/creation/executable always fails. Always collect terminal exit, Job accounting and PID drain before Job close.','strict_limits':{'affinity':3,'process_job_RAM_bytes':8*1024**3,'active_process_limit':1,'source_watchdog_seconds':120,'min_free_RAM_bytes':12*1024**3,'min_free_C_bytes':100*1024**3,'kill_on_close':True},'probes':[{'case':r['case'],'pid':r['pid'],'native_process_handle':r['native_process_handle'],'guard_parent_pid':r['guard_parent_pid'],'exit_code':r['exit_code'],'total':r['total_job_processes'],'final_active':r['active_after_exit'],'cleanup_terminal':r['cleanup_owned_handle_terminal'],'cleanup_exit':r['cleanup_owned_handle_exit_code'],'cleanup_accounting':r['cleanup_terminal_job_accounting'],'cleanup_pids':r['cleanup_final_job_pids']} for r in rows],'source_action_recipe_hashes':g.hashes(),'native_numeric_acceptance':False,'network_boundary':'Supported --offline-mode plus factory startup; no claim of OS-enforced network sandbox','frozen_files':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(F.iterdir())}}
(E/'FINAL_REVIEW_MANIFEST_R5.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
(E/'FINAL_SOURCE_JOB_REVIEW_R5.md').write_text(f'''# R5 additive installed source-read preparation

R4 exact failed guard/source identity/log remain immutable. R5 source was not opened and no approval receipt was written. All source/actions/recipe hashes remain unchanged; user preferences and GUI were not changed. Large acquisition/native capture/build remain false.

Same exact final R5 guard `{sha(GUARD)}` ran normal PID{rows[0]['pid']} exit0, timeout PID{rows[1]['pid']} exit88 and fixed installed CLI-help PID{rows[2]['pid']} exit0. Each has total lifetime processes1, final Active0/PID list empty and authoritative owned-handle terminal/exit and cleanup Job accounting/PID drain before close. Strict native layouts/limit readback/resource floors pass. Help is the only Blender executable job at this preparation stage; no source read, render/export/save/action/pose operations were run.

Installed help output confirms `--factory-startup`, `--offline-mode` and `--disable-autoexec`. Source argv applies these flags before source filename, with two threads; fixed output folder and verifier output match. Factory startup is intended to avoid user preference startup/addons; offline mode overrides the internet-access preference without persistent preference writes. Full source startup isolation remains untested until separately authorized R5 source read. No OS network sandbox is claimed.

R5 polls the real owned process HANDLE before each identity query, and re-polls it if image data is missing. Missing image is tolerated only when that same handle is terminal. Unknown PID, changed creation identity or wrong executable remains failure. It records actual handle exit, Job accounting and empty PID drain before concluding; exception cleanup also records terminal handle/accounting before kill-on-close. Native process/job handles, guard parent PID, child PID and creation FILETIME are printed in the live OWNED_CHILD_RESUMED event for provenance. Handles belong to that guard process only.

Verifier SHA `{sha(VERIFIER)}`, same-guard probes SHA `{sha(g.OUT/'PROBE_MANIFEST.json')}`, local help log SHA `{sha(g.OUT/'factory-help.log')}`. Exact source argv/output/limits/files are in FINAL_REVIEW_MANIFEST_R5.json. Scope is full original57rest/world/63561 basis positions/304799 ordered CSR/groups58/mask52 identity, first mismatch/no repair; no canonical, visual/PBR/Unity or native arithmetic acceptance. Guard requires a new exact scoped R5 approval; R4 approval cannot arm it. Frozen ZIP preserves exact bytes across Git line-ending conversion.

Next bounded task: PM review of frozen R5 guard/verifier/argv and these actual same-guard probe/help receipts, before any R5 source launch.
''',encoding='utf8')
packet=E/'YURI_O1_SOURCE_JOB_REVIEW_R5.zip'
with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(E.rglob('*')):
        if p.is_file() and p!=packet:z.write(p,p.relative_to(E).as_posix())
with zipfile.ZipFile(packet) as z:assert z.testzip() is None
receipt={'status':'R5_REVIEW_ONLY_SOURCE_NOT_RUN','zip':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'manifest_sha256':sha(E/'FINAL_REVIEW_MANIFEST_R5.json'),'guard_sha256':sha(GUARD),'verifier_sha256':sha(VERIFIER),'same_guard_probe_manifest_sha256':sha(g.OUT/'PROBE_MANIFEST.json'),'factory_help_log_sha256':sha(g.OUT/'factory-help.log')}
(E/'PACKET_RECEIPT_R5.json').write_text(json.dumps(receipt,indent=2),encoding='utf8');print(json.dumps(receipt))
