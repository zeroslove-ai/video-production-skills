"""Additive V4/R2 preparation freeze. No acquisition, compiler or Blender launch."""
from pathlib import Path
import ast,hashlib,importlib.util,json,shutil,subprocess
LAB=Path(__file__).resolve().parent.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
R1=BASE/'o1-guarded-native-resource-sizing-r1';OUT=BASE/'o1-guarded-native-resource-sizing-r2'
E=LAB/'evidence'/OUT.name;E.mkdir(exist_ok=True)
assert not (OUT/'GUARDED_NATIVE_RESOURCE_MANIFEST.json').exists(), 'frozen R2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):
    p=OUT/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2));return p
shutil.copytree(R1/'upstream',OUT/'upstream',dirs_exist_ok=True)
for n in ('WINDOWS_DEPS_EXACT_PAYLOAD_MANIFEST.json','ACQUISITION_PLAN.json','BUILD_CAPTURE_STAGED_PLAN.json'):
    shutil.copyfile(R1/n,OUT/n)
shutil.copytree(R1/'expected-Strong6-v3',OUT/'expected-Strong6-v3',dirs_exist_ok=True)
# Reuse the source-pinned V3 generator, redirect ONLY this new packet's outputs.
code=(LAB/'scripts/r4_guarded_native_proposal_v3.py').read_text()
code=code.replace('o1-guarded-native-resource-sizing-r1','o1-guarded-native-resource-sizing-r2')
needle="code=(LAB/'scripts/r4_guarded_native_proposal_v2.py').read_text()"
code=code.replace(needle,needle+".replace('o1-guarded-native-resource-sizing-r1','o1-guarded-native-resource-sizing-r2')")
code=code.replace('PROPOSED_GUARDED_NATIVE_V3.diff','PROPOSED_GUARDED_NATIVE_V4.diff').replace('NATIVE_V3_REVIEW_RECEIPT.json','NATIVE_V4_REVIEW_RECEIPT.json')
extra=r'''
changes['intern/cycles/blender/host_guard_probe.cpp']=('',(LAB/'scripts/native_readback_proposal/host_guard_probe.cpp').read_text())
a,b=changes['intern/cycles/blender/CMakeLists.txt']
b=b.replace('  host_readback.cpp','  host_guard_probe.cpp\n  host_readback.cpp',1)
changes['intern/cycles/blender/CMakeLists.txt']=(a,b)
a,b=changes['intern/cycles/blender/python.cpp']
b=b.replace('    {"host_mesh_readback",', '    {"host_mesh_guard_probe", host_guard_probe_func, METH_VARARGS, "Owned actual entry denial probe"},\n    {"host_mesh_readback",',1)
changes['intern/cycles/blender/python.cpp']=(a,b)
'''
code=code.replace("exec(compile(code,'additive-v3-proposal','exec'))",
    "code=code.replace(\"diff=''.join(\", "+repr(extra)+"+\"\\ndiff=''.join(\",1)\nexec(compile(code,'additive-v4-proposal','exec'))")
if not (OUT/'PROPOSED_GUARDED_NATIVE_V4.diff').exists():
    exec(compile(code,'v4-source-diff-only','exec'))
diff=OUT/'PROPOSED_GUARDED_NATIVE_V4.diff'
diff.write_bytes(diff.read_text().encode())  # Canonical LF for actual git apply check.
review=json.loads((OUT/'NATIVE_V4_REVIEW_RECEIPT.json').read_text())
review.update({'revision':'V4_ADDITIVE_R2_NO_PRIOR_REVIEW_INHERITANCE','diff_sha256':sha(diff),
 'all_vector_sizes_before_reads':'corner_tris381120/corner_vertices254602/triangle_polygons127040/material_slots127040/smooth127040/object_world16/actualtri381120/shader127040/smooth127040; polygon span length/range and material/sharp span sizes guarded',
 'types':'Native TypePoint/TypeNormal/TypeFloat2/TypeVector/TypeFloat and std/domain/stride/count/no-motion enforced',
 'probe_coverage':'13 proposed actual native entry calls; remaining7 hooks require compiled source/control-flow/guard coverage review. No fake helper-only test is counted. All probes uncompiled/unrun.',
 'caller_receipt_alignment':'finally OFF restore even on failure; OFF_restore_exact/source_temporal_settings_unchanged emitted after assertions; standard_name emitted by native provenance writer for external schema',
 'supervisor':'Concrete Windows suspended creation + owned Job kill-on-close, RAM/CPU/activechildren/wall-time/free-disk guards. Exact allowed exe/helper SHA and review gate; sanitized failure receipt; process exit0/activechildren0/data validator mandatory. UNRUN.',
 'acquisition':'Executable dry-default stager, per-object published SHA/size checks, Range resume+quarantine, pinned shallow Git checkout and raw blob/LFS validation, owned LLVM7z unpack only, no PATH/registry/compiler install. No payload acquired.'})
write('NATIVE_V4_REVIEW_RECEIPT.json',review)
for p in (LAB/'scripts/native_readback_proposal').iterdir():
    target=OUT/'proposal-v4'/p.name;target.parent.mkdir(exist_ok=True);shutil.copyfile(p,target)
# Source-applicability test in a tiny copied text fixture, not real/source/build repo.
fixture=OUT/'apply-check-fixture';fixture.mkdir(exist_ok=True)
for name,row in review['original_source'].items():
    text=(OUT/'upstream'/name).read_text()
    assert hashlib.sha256(text.encode()).hexdigest()==row['sha256']
    p=fixture/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(text.encode())
check=subprocess.run(['git','apply','--check',str(diff)],cwd=fixture,capture_output=True,text=True)
assert check.returncode==0,check.stderr
write('SOURCE_APPLY_CHECK.json',{'scope':'git apply --check on copied pinned source text only; no patch applied/no compile',
 'exit_code':check.returncode,'diff_sha256':sha(diff),'base_files':review['original_source'],'stdout':check.stdout,'stderr':check.stderr})
# Parse every Python helper, then import only helpers that cannot execute on import.
syntax=[]
for p in (OUT/'proposal-v4').glob('*.py'):
    ast.parse(p.read_text(encoding='utf8'),filename=str(p));syntax.append({'path':p.name,'sha256':sha(p),'AST_parse':'PASS'})
for name in ('owned_windows_capture_supervisor','staged_native_acquisition','validate_owned_native_capture'):
    p=OUT/'proposal-v4'/f'{name}.py';spec=importlib.util.spec_from_file_location('review_'+name,p)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    syntax.append({'path':p.name,'import_without_network_process_root_creation':'PASS'})
write('DRY_SYNTAX_IMPORT_RECEIPT.json',{'scope':'No Blender import, no WinDLL/job execution, no acquisition/build/probe/capture','files':syntax})
source_inventory=BASE/'o1-source-fidelity-recovery-r1/metadata/mesh_slot_UV_attributes_shape_deltas.json'
assert sha(source_inventory)=='e76524048e1168a84b7a98aead4404f6b5cea76fe33f317234dcc21facc8de0c'
body=next(row for row in json.loads(source_inventory.read_text()) if row['renderer']=='Meshy_Body_NeutralCovered')
assert 'sharp_face' not in [a['name'] for a in body['attributes']]
write('SMOOTH_EXPECTATION_PROVENANCE.json',{'source_inventory_path':str(source_inventory),'source_inventory_sha256':sha(source_inventory),
 'field':'renderer=Meshy_Body_NeutralCovered.attributes[*].name; sharp_face absent',
 'source_attribute_names':[a['name'] for a in body['attributes']],
 'pinned_policy_source':'intern/cycles/blender/mesh.cpp; absent sharp_faces => smooth true',
 'expected_smooth_SHA256':sha(OUT/'expected-Strong6-v3/smooth.u8'),
 'classification':'DERIVED_SOURCE_POLICY_EXPECTATION_NOT_A_CAPTURED_EVALUATED_SMOOTH_BYTE_ARRAY',
 'actual_evaluated_smooth_authority':'PENDING native routes reads actual sharp_face; exact expected comparison rejects drift; not an actual Cycles buffer claim'})
tools={}
for p in (Path(r'C:/Program Files/Git/cmd/git.exe'),Path(r'C:/Program Files/7-Zip/7z.exe')):
    assert p.is_file();tools[str(p.resolve())]={'bytes':p.stat().st_size,'sha256':sha(p)}
write('EXISTING_STAGING_TOOLS.json',tools)
expected=json.loads((OUT/'expected-Strong6-v3/EXPECTED_INPUTS.json').read_text())
for r in expected['files']:assert sha(OUT/'expected-Strong6-v3'/r['path'])==r['sha256']
route='''# Native arithmetic dependency decision — 3b8383a6

The exact request was read from the committed product documentation through GitHub API only; product/Laptop worktree was not opened or changed. The contract requires Startle11/Strong6,57 native bone inverse/pose/deform/quaternion intermediates, five ordered original CSR samples11189/14918/21485/22227/40817, lossless little-endian float32 arrays and stage00/01 native LOCAL plus WORLD. Final WORLD inverse must never fill missing LOCAL.

Resource acquisition/build infrastructure can be shared with the pinned Cycles research build: same9e2066aef7ef source and owned Clang/Eigen/SDK, independent read-only instrumentation macro in MOD_armature ordinary nullopt no-deform-matrices caller and actual armature_deform/math_matrix/math_rotation primitives. Its native diagnostics must log source/compiler/FMA/SSE/Eigen path and exact original recipe/CSR/pose custody. The code hook/capture for that arithmetic request is **not implemented or executed here**; current library/reference values are not relabeled native intermediates. A standalone native primitive harness with existing MSVC is also feasible as a separate classification, but cannot certify installed Blender arithmetic. Exact installed flags remain unavailable.

The chosen next route after resources are approved is typed source instrumentation of the owned full native build, not installed-GUI pointer hooks or donor geometry. Preserve all57 slots/helpers and ordinary caller operation order; source `.blend` and Action library remain byte-identical. Cycles host-center tangent capture and native armature arithmetic are separate evidence requirements; neither proves the other's PASS. No new model/export/product implementation is authorized by this dependency.
'''
(OUT/'NATIVE_ARITHMETIC_ROUTE_DECISION.md').write_text(route,encoding='utf8')
coverage={'real_entry_probes':['factory','session','scene-upload','scene-kernel','alloc','upload','copy-from','zero','subptr','const','global','kernel','kernel-globals'],
 'other_hooks':['Session.start','Session.run_main_render_loop','BlenderSession.render','BlenderSession.synchronize','BVH.create','CPUDevice.image_alloc','CPUDevice.build_bvh'],
 'acceptance':'Runtime exit86 + exact expected entry and before_original_body log for13 proposed cases; remaining7 compiled-hook/control-flow closure or expanded valid-context tests must be reviewed before capture. All uncompiled/unrun.',
 'additional_negative_cases':'wrong RNA type, expired RNA, wrong source frame/scene/input bytes/route counts/type/domain/size, existing output path, source/action hash drift, exception OFF restore, job timeout/RAM/disk abort -> partial rejection; not falsely counted as native-entry probes.'}
write('GUARD_TEST_COVERAGE.json',coverage)
action='''# Reviewable next action — isolated acquisition only

Known binary payload **7,054,121,984bytes** plus unknown Git pack/protocol/metadata. Official URLs/digests and1263 individual LFS objects are in ACQUISITION_PLAN/WINDOWS_DEPS_EXACT_PAYLOAD_MANIFEST. Existing Git/7z hashes are recorded; no new unpacker install is needed. Full source/compiler/deps downloads have **not** occurred.

Concrete command, after human approval and an owner receipt with this packet's exact plan/manifest/stager/tool SHA values:

```powershell
& 'C:\\Program Files\\Python313\\python.exe' '<packet>\\proposal-v4\\staged_native_acquisition.py' --execute --approval '<owner-reviewed-acquisition-receipt.json>'
```

The command creates only C:/YuriTransfer/native-cycles-readback-r1 after approval. It streams published assets with size/digest validation; exact-identity partial files resume with Range+full hash, unsupported Range or wrong digest moves the checked owned partial to quarantine. Tar extraction uses data filter; pinned shallow Git tree bypasses smudge, then LFS batch responses are validated and each object/working-tree path rehashed. LLVM NSIS installer is **unpacked by existing7z, never executed**; safe member paths checked, compiler file manifest recorded. No global PATH/registry/ComfyUI update. Original master/Action hashes are checked by every owned tool supervisor job.

This acquisition does not build or capture. Review staged-resource receipts first, then execute the isolated CMake/Ninja profile from BUILD_CAPTURE_STAGED_PLAN with a reviewed exact argv/tool manifest. Generic tool jobs are suspended before assignment to owned Windows Job, bounded8 processes/8GiB/2cores/15–20min; proposed build can use16GiB/2tasks. Capture is1process/8GiB/4cores/TBB4/120sec. Stop below12GiB freeRAM or100GiB freeC;80GiB workspace budget. Kill-on-job-close, SHA-validated reviewed helpers, failed/partial receipts and exit0+zero active job children+full data validator are implemented but **Windows actual job tests are unrun**. Existing GUI129152 is never attached/stopped. GPU PRODUCT_EXCLUSIVE remains unchanged.

V4 native diff source applies in a small copied-source fixture (`git apply --check` only), helper syntax/nonexecuting import checks pass. Compile/link/private/protected/API compatibility cannot be proven without acquisition.13 actual-entry probe calls are proposed;7 other hooks need compiled closure review. Source/Action OFF restore and temporal receipt schema align. Derived smooth policy is anchored to original inventory absence of sharp_face, not falsely called captured evaluated bytes. Custom local MOTION_NONE snapshot is not shaded installed renderer equivalence. Numerical PBR/Unity acceptance remains HOLD.

Human boundary retained: “명백한 유료결제/대규모 신규 다운로드/제품 repo 변경만 사용자 승인 대상으로 남긴다.” Approval is required for the concrete large acquisition; no automatic transfer, build, capture or product edit follows this preparation. No routine small-experiment question is introduced. Preparation has reached the executable acquisition action; next execution waits for owner approval/review rather than more metadata enumeration.
'''
for root in (OUT,E):(root/'ROOT_PM_GUARDED_NATIVE_RESOURCE_SIZING_R2.md').write_text(action,encoding='utf8')
manifest={'task_id':'ROOT_PM_GUARDED_NATIVE_PREPARATION_REVIEW_AND_RESOURCE_SIZING_R2','status':'DONE_REVIEWABLE_ISOLATED_ACQUISITION_AND_V4_PREPARATION_EXECUTION_HOLD',
 'V4_diff_SHA256':sha(diff),'prior_R1_manifest_SHA256':sha(R1/'GUARDED_NATIVE_RESOURCE_MANIFEST.json'),
 'prior_R1_packet_custody':json.loads((R1/'PACKET_CUSTODY.json').read_text()),
 'source_apply_check':'PASS_COPIED_TEXT_ONLY','Python_AST_and_safe_import':'PASS','known_payload_bytes':7054121984,
 'large_transfer_build_Blender_GPU_capture_jobs':0,'GUI_PID_preserved':129152,'appearance_promoted':False,
 'actual_Cycles_buffers':'HOLD','native_armature_intermediates':'HOLD_ROUTE_DECIDED_NO_HOOK_IMPLEMENTED','runtime_PBR':'HOLD',
 'negative_entry_probes_proposed':13,'other_denial_hooks_compiled_closure_pending':7,
 'files':[{'path':str(p.relative_to(OUT)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)}
          for p in sorted(OUT.rglob('*')) if p.is_file() and not p.is_relative_to(fixture)]}
for root in (OUT,E):(root/'GUARDED_NATIVE_RESOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
for name in ('NATIVE_V4_REVIEW_RECEIPT.json','SOURCE_APPLY_CHECK.json','DRY_SYNTAX_IMPORT_RECEIPT.json','GUARD_TEST_COVERAGE.json',
 'EXISTING_STAGING_TOOLS.json','SMOOTH_EXPECTATION_PROVENANCE.json'):
    shutil.copyfile(OUT/name,E/name)
print(json.dumps({'status':manifest['status'],'files':len(manifest['files']),'bytes':sum(r['bytes'] for r in manifest['files']),'V4_diff_SHA256':sha(diff)}))
