"""File-only trusted installation inspection and new immutable R2 proposal.

Does not import installation scripts, bpy, addon modules or launch anything.
"""
from pathlib import Path
import ast, copy, hashlib, json, zipfile

LAB=Path(__file__).resolve().parent.parent
S=LAB/'scripts'
E=LAB/'evidence/o1-exact-local-stage-factory-addon-preparation-r2'
OLD=LAB/'evidence/o1-exact-local-stage-preparation-r1'
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
INSTALL=Path('C:/Program Files/Blender Foundation/Blender 5.2/5.2/scripts')
ROOT=INSTALL/'addons_core'

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def write(n,v):
    with (E/n).open('x',encoding='utf8') as f:json.dump(v,f,indent=2)

def main():
    assert not E.exists(),'Frozen preparation cannot be overwritten'
    old_collector=S/'r4_exact_local_stage_collector_r1.py'
    old_launcher=S/'r4_exact_local_stage_launcher_r1.py'
    assert sha(old_collector)=='f8ab4bc7dd77f1ecdeaf843659acd9be6caf290e888f13d59862388b2136d57a'
    assert sha(old_launcher)=='a861300f4bff07813799958d8c6400a874360a61023b095e72b9917c36926eb8'
    module_control=INSTALL/'modules/addon_utils.py'
    source=module_control.read_text(encoding='utf8')
    tree=ast.parse(source)
    hidden=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_addons_hidden_core' for t in n.targets))
    assert hidden=={'bl_pkg','io_anim_bvh','io_curve_svg','io_mesh_uv_layout','io_scene_fbx'}
    assert 'these add-ons will *not* be included' in source and 'reason we can\'t include "cycles"' in source
    allow={}
    for directory in sorted(ROOT.iterdir()):
        if not directory.is_dir() or not (directory/'__init__.py').is_file():continue
        entry=directory/'__init__.py'
        ast_tree=ast.parse(entry.read_text(encoding='utf8'))
        info=None
        for node in ast_tree.body:
            if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='bl_info' for t in node.targets):
                try:info=ast.literal_eval(node.value)
                except (ValueError,TypeError):info={'static_literal':'UNKNOWN'}
        py_files={str(p.resolve()):sha(p) for p in sorted(directory.rglob('*.py'))}
        allow[directory.name]={'entry_path':str(entry.resolve()),'entry_sha256':sha(entry),'python_files':py_files,'python_tree_fingerprint':hashlib.sha256(json.dumps(py_files,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'static_bl_info':info,'factory_membership':'HIDDEN_CORE_EXPLICITLY_ENABLED_AT_STARTUP' if directory.name in hidden else 'UNKNOWN; installed bundled candidate only'}
    assert len(allow)==13 and set(hidden)<=set(allow)
    control_files={str(p.resolve()):sha(p) for p in [module_control,INSTALL/'modules/bpy/utils/__init__.py']}
    E.mkdir(parents=True)
    manifest={'status':'STATIC_INSTALLED_ORIGIN_CANDIDATE_ALLOWLIST_PM_REVIEW_PENDING','installed_root':str(ROOT.resolve()),'installed_bundled_allowlist':allow,'startup_control_files':control_files,'explicit_hidden_core':sorted(hidden),'exact_prior_failed_run_enabled_inventory':'UNKNOWN_NOT_LOGGED','compiled_factory_preference_default_list':'UNKNOWN_NOT_PRESENT_IN_INSPECTED_PYTHON_FILES','cycles_evidence':'Installed addon_utils comment says Cycles cannot be hidden because it needs saved preferences. Installed cycles entry identifies official renderer integration. Does not prove prior actual preference membership.','policy':'Exact13 existing installed-bundle package origins and full Python-tree hashes are proposed, not all names called factory-enabled. Other origins/names/unknown modules fail before pose capture. No enabling/disabling/preference edits/importing addons.'}
    write('INSTALLED_BUNDLED_ADDON_ORIGIN_MANIFEST_R2.json',manifest)
    collector=S/'r4_exact_local_stage_collector_r2.py'
    launcher=S/'r4_exact_local_stage_launcher_r2.py'
    assert not collector.exists() and not launcher.exists()
    code=old_collector.read_text(encoding='utf8')
    code=code.replace("o1-exact-source-local-stage-capture-r1","o1-exact-source-local-stage-capture-r2")
    code=code.replace("evidence/o1-exact-local-stage-preparation-r1/CAPTURE_PROPOSAL_R1.json","evidence/o1-exact-local-stage-factory-addon-preparation-r2/CAPTURE_PROPOSAL_R2.json")
    code=code.replace("PM_APPROVAL_EXACT_LOCAL_CAPTURE_R1.json","PM_APPROVAL_EXACT_LOCAL_CAPTURE_R2.json")
    old_assert="    assert list(bpy.context.preferences.addons.keys()) == [], 'factory addon inventory must be empty'"
    assert old_assert in code
    code=code.replace(old_assert,"    from r4_installed_addon_origin_gate_r2 import inspect_and_require\n    addon_manifest = LAB / 'evidence/o1-exact-local-stage-factory-addon-preparation-r2/INSTALLED_BUNDLED_ADDON_ORIGIN_MANIFEST_R2.json'\n    addon_before = inspect_and_require(bpy, addon_manifest, OUT, 'before')")
    code=code.replace("    after = snapshot(original_actions)","    addon_after = inspect_and_require(bpy, addon_manifest, OUT, 'after')\n    assert addon_before['preferences_module_names'] == addon_after['preferences_module_names'] and addon_before['loaded_enabled_module_names'] == addon_after['loaded_enabled_module_names']\n    after = snapshot(original_actions)")
    with collector.open('x',encoding='utf8',newline='\n') as f:f.write(code)
    code=old_launcher.read_text(encoding='utf8').replace('o1-exact-source-local-stage-capture-r1','o1-exact-source-local-stage-capture-r2').replace('evidence/o1-exact-local-stage-launcher-preparation-r1/FIXED_ROUTE_CONFIG_R1.json','evidence/o1-exact-local-stage-factory-addon-preparation-r2/FIXED_ROUTE_CONFIG_R2.json').replace('evidence/o1-exact-local-stage-preparation-r1/CAPTURE_PROPOSAL_R1.json','evidence/o1-exact-local-stage-factory-addon-preparation-r2/CAPTURE_PROPOSAL_R2.json').replace('r4_exact_local_stage_collector_r1.py','r4_exact_local_stage_collector_r2.py').replace('PM_APPROVAL_EXACT_LOCAL_CAPTURE_R1.json','PM_APPROVAL_EXACT_LOCAL_CAPTURE_R2.json')
    with launcher.open('x',encoding='utf8',newline='\n') as f:f.write(code)
    helper=S/'r4_installed_addon_origin_gate_r2.py'
    for p in [collector,launcher,helper]:compile(ast.parse(p.read_text(encoding='utf8')),str(p),'exec')
    proposal=copy.deepcopy(json.loads((OLD/'CAPTURE_PROPOSAL_R1.json').read_bytes()))
    proposal['status']='R2_PREPARED_ONLY_NOT_RUN_NEW_APPROVAL_REQUIRED'
    proposal['argv'][-1]=str(collector)
    proposal['output_private_directory']=str(BASE/'o1-exact-source-local-stage-capture-r2')
    proposal['inputs'].pop(str(old_collector))
    for p in [collector,helper,E/'INSTALLED_BUNDLED_ADDON_ORIGIN_MANIFEST_R2.json']:proposal['inputs'][str(p)]={'sha256':sha(p),'bytes':p.stat().st_size}
    assert all(sha(Path(p))==row['sha256'] for p,row in proposal['inputs'].items())
    proposal['addon_policy']={'manifest_sha256':sha(E/'INSTALLED_BUNDLED_ADDON_ORIGIN_MANIFEST_R2.json'),'exact_installed_candidates':sorted(allow),'actual_factory_default_membership':'UNKNOWN','capture':'Preferences union already-loaded enabled addon modules; no new addon import. Resolve file/spec origins and SHA; pin all package Python/control files. Before and after inventory JSON retained even when gate rejects.', 'external_user_unknown_policy':'FAIL; no surgery or preference edits','network':'Not a sandbox or proof of no startup side effects'}
    proposal['guard_proposal']['existing_R5_route_executable_for_this_collector']=False
    proposal['guard_proposal']['pending_review']='Exact R2 route/config now included for new PM receipt review. R1 approval consumed; no probes/launch performed.'
    proposal['guard_proposal']['network']='Factory/offline; installed-origin gate instead of incorrect empty-addon gate; no global edits or account/plugin calls. Windows Job is not network isolation.'
    proposal['output_schema']['addon_inventory_before_after']='Preferences and loaded enabled modules, exact resolved origins/file SHA, trusted-installed classification/errors. Defaults membership remains unknown unless actual inventory read.'
    proposal['prior_failed_capture']={'checkpoint':'026a581','PID':114608,'collector':'empty factory-addon assertion before capture','guard':'strict LIVE image error5; FAIL independently','cleanup':'exit93/Active0/PIDs[]','retry_authorization':'NONE; new proposal only'}
    write('CAPTURE_PROPOSAL_R2.json',proposal)
    oldconfig=json.loads((LAB/'evidence/o1-exact-local-stage-launcher-preparation-r1/FIXED_ROUTE_CONFIG_R1.json').read_bytes())
    config=copy.deepcopy(oldconfig)
    config.update(status='R2_PREPARED_ONLY_NOT_RUN',launcher_sha256=sha(launcher),collector_sha256=sha(collector),proposal_sha256=sha(E/'CAPTURE_PROPOSAL_R2.json'),argv=proposal['argv'],output_directory=proposal['output_private_directory'])
    config['launch_command_argv'][2]=str(launcher)
    config['receipt_path']=str(BASE/'o1-exact-source-local-stage-capture-r2/PM_APPROVAL_EXACT_LOCAL_CAPTURE_R2.json')
    config['network']='Exact factory/offline CLI, pinned installed addon origin gate. No network/account operations; no packet isolation claim.'
    config['remaining_review']='New receipt bound to R2 launcher/config/script/proposal required; no probes or runtime launch performed.'
    write('FIXED_ROUTE_CONFIG_R2.json',config)
    template={'scope':config['scope'],'approved':False,'reviewed_owned_job_terminal_behavior':False,'launcher_sha256':sha(launcher),'config_sha256':sha(E/'FIXED_ROUTE_CONFIG_R2.json'),'proposal_sha256':sha(E/'CAPTURE_PROPOSAL_R2.json'),'collector_sha256':sha(collector),'blender_sha256':config['blender_sha256'],'argv':config['argv'],'custom_native_build_trace_capture_approved':False,'large_resource_acquisition_approved':False,'note':'NOT_APPROVAL; not installed at actual receipt path'}
    write('APPROVAL_RECEIPT_TEMPLATE_NOT_APPROVAL_R2.json',template)
    # Resource/identity/terminal executable logic identical to R1 except fixed paths.
    reverse=launcher.read_text().replace('o1-exact-source-local-stage-capture-r2','o1-exact-source-local-stage-capture-r1').replace('evidence/o1-exact-local-stage-factory-addon-preparation-r2/FIXED_ROUTE_CONFIG_R2.json','evidence/o1-exact-local-stage-launcher-preparation-r1/FIXED_ROUTE_CONFIG_R1.json').replace('evidence/o1-exact-local-stage-factory-addon-preparation-r2/CAPTURE_PROPOSAL_R2.json','evidence/o1-exact-local-stage-preparation-r1/CAPTURE_PROPOSAL_R1.json').replace('r4_exact_local_stage_collector_r2.py','r4_exact_local_stage_collector_r1.py').replace('PM_APPROVAL_EXACT_LOCAL_CAPTURE_R2.json','PM_APPROVAL_EXACT_LOCAL_CAPTURE_R1.json')
    assert reverse==old_launcher.read_text()
    write('STATIC_VALIDATION_R2.json',{'status':'FILE_ONLY_STATIC_REVIEW_PASS_NATIVE_NOT_RUN','collector_launcher_helper_AST_compile':True,'installed_packages':len(allow),'installed_Python_files_hashed':sum(len(x['python_files']) for x in allow.values()),'hidden_core_from_installed_AST':sorted(hidden),'launcher_logic_same_as_R1_except_fixed_paths':True,'source_action_recipe_existing_reference_hashes_unchanged':True,'enabled_inventory_actual':'UNKNOWN_NOT_CAPTURED','addon_origin_gate_runtime':'NOT_RUN','Blender_or_probe_launches':0,'global_preferences_edits':0,'R1_R5_guard_FAIL_preserved':True})
    packet=E/'YURI_O1_FACTORY_ADDON_EXACT_LOCAL_PREPARATION_R2.zip'
    files=[collector,launcher,helper,Path(__file__)]+list(E.glob('*.json'))
    with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,p.name)
    with zipfile.ZipFile(packet) as z:assert z.testzip() is None
    write('PACKET_CUSTODY_R2.json',{'packet':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'collector_sha256':sha(collector),'launcher_sha256':sha(launcher),'config_sha256':sha(E/'FIXED_ROUTE_CONFIG_R2.json'),'proposal_sha256':sha(E/'CAPTURE_PROPOSAL_R2.json'),'installed_manifest_sha256':sha(E/'INSTALLED_BUNDLED_ADDON_ORIGIN_MANIFEST_R2.json'),'status':'PREPARATION_ONLY_NEW_PM_REVIEW_PENDING'})
    print((E/'PACKET_CUSTODY_R2.json').read_text())

if __name__=='__main__':main()
