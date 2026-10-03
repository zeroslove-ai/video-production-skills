"""Static fixture checks and immutable research packet. Never build/run Blender."""
from pathlib import Path
import ast, hashlib, json, re, shutil, subprocess, zipfile
ROOT=Path(__file__).resolve().parents[1]
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
E=ROOT/'evidence/o1-native-armature-instrumentation-draft-r6'
OUT=BASE/'o1-native-armature-instrumentation-draft-r6'
assert not OUT.exists();OUT.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((E/'PATCH_APPLY_AND_SCOPE.json').read_text(encoding='utf8'))
fixture=Path(manifest['apply_check']['fixture'])
result=subprocess.run(['git','apply',str(E/'native_armature_typed_r6.patch')],cwd=fixture,capture_output=True,text=True)
assert result.returncode==0,result.stderr
checks={}
for name,row in manifest['sources'].items():
    original=Path(row['cached_path']).read_text(encoding='utf8')
    changed=(fixture/name).read_text(encoding='utf8')
    off=re.sub(r'\n#ifdef WITH_YURI_ARMATURE_TRACE_R1\n.*?\n#endif\n','',changed,flags=re.S)
    # Compare default-off C++ token stream modulo whitespace introduced around block removal.
    assert re.sub(r'\s+','',off)==re.sub(r'\s+','',original),name
    checks[name]={'default_off_original_nonwhitespace_bytes':'IDENTICAL','cached_source_sha256':sha(Path(row['cached_path']))}
header=fixture/'source/blender/blenlib/BLI_yuri_armature_trace_r1.hh'
text=header.read_text(encoding='utf8')
assert '@BONES@' not in text and 'bones[57]' in text and 'std::fopen(paths[row],"wbx")' in text
assert '64*1024*1024' in text and 'records>=100000' in text
upstream=BASE/'o1-native-armature-instrumentation-draft-r1'
query=(upstream/'upstream/DEG_depsgraph_query.hh').read_text(encoding='utf8')
assert 'float DEG_get_ctime(const Depsgraph *graph);' in query
for script in ('r4_armature_instrumentation_draft_r1.py','r4_armature_instrumentation_draft_r2.py','r4_armature_instrumentation_draft_r6.py','r4_armature_draft_finalize_r6.py','native_readback_proposal/armature_trace_unpack_r1.py'):
    ast.parse((ROOT/'scripts'/script).read_text(encoding='utf8'))
test=subprocess.run([r'C:/Program Files/Python313/python.exe',str(ROOT/'scripts/native_readback_proposal/armature_trace_unpack_r1.py'),'--self-test'],capture_output=True,text=True)
assert test.returncode==0
checks['raw_format_parser']=json.loads(test.stdout)
checks['DEG_get_ctime']='EXACT_PINNED_DECLARATION_FOUND; full ModifierEvalContext/matrix API compilation pending'
checks['actual_compile_runtime']='NOT_ATTEMPTED'
validation=BASE/'o1-native-armature-canonical-validation-r4'
request=validation/'request-inputs-exact.json'
assert sha(request)=='a46c693c28e09a93729bbe433a522d47c7a452c740a6af6ceb8868ddec370b17'
bones=BASE/'o1-native-unity-probe-r1/metadata/source_expanded_rigs.json'
extra=['armature_canonical_validate_r4.py','armature_validator_fixture_r4.py','armature_owned_invocation_r5.py','armature_live_recipe_r5.py','armature_canonical_pack_r5.py','armature_trace_unpack_r1.py']
for name in extra:ast.parse((ROOT/'scripts/native_readback_proposal'/name).read_text(encoding='utf8'))
test=subprocess.run([r'C:/Program Files/Python313/python.exe',str(ROOT/'scripts/native_readback_proposal/armature_validator_fixture_r4.py'),'--request',str(request),'--bones',str(bones)],capture_output=True,text=True)
assert test.returncode==0,test.stderr
checks['complete_synthetic_fixture_and_single_defect_tests']=json.loads(test.stdout)
invocation=subprocess.run([r'C:/Program Files/Python313/python.exe',str(ROOT/'scripts/native_readback_proposal/armature_owned_invocation_r5.py')],capture_output=True,text=True)
assert invocation.returncode==0 and 'DRY_ONLY' in invocation.stdout
checks['invocation_default_dry']=invocation.stdout.strip()
action_inventory=BASE/'r4-appearance-preserve-correction-r1/metadata/action_library_only.json'
actions=json.loads(action_inventory.read_text(encoding='utf8'))['actions']
assert all(x['clip'] in actions for x in json.loads(request.read_bytes())['pose_inputs'])
checks['actual_Action_identity']={'source_action_inventory_sha256':sha(action_inventory),'request_input_sha256':sha(request),'cases':[(x['clip'],x['frame']) for x in json.loads(request.read_bytes())['pose_inputs']],'runtime_live_gate':'UNEXECUTED; native reads adt->action->id.name in pose/modifier scopes; adapter validates actual slot/pose/files before begin'}
for name in ('DNA_anim_types.h','DNA_object_types.h','DNA_action_types.h','DNA_armature_types.h'):
    p=validation/name;checks[name]={'sha256':sha(p),'static_type_checks_only':True}
checks['full_recipe_gate']='Missing actual full recipe file: arming verification denies; no fabricated consent/token/data'
import sys
sys.path.insert(0,str(ROOT/'scripts/native_readback_proposal'))
from armature_validator_fixture_r4 import fixture
from armature_canonical_pack_r5 import pack
request_data=json.loads(request.read_bytes());bone_data=json.loads(bones.read_bytes())['Meshy_Fitted_Rig']['bones']
synthetic=pack(fixture(request_data,bone_data),request_data,bone_data,OUT/'SYNTHETIC_ONLY_CanonicalSchema_R6.npz','SYNTHETIC_FIXTURE_NOT_NATIVE')
with zipfile.ZipFile(OUT/'SYNTHETIC_ONLY_CanonicalSchema_R6.npz') as z:
    assert z.testzip() is None
    for name,row in synthetic['arrays'].items():
        b=z.read(name+'.npy');length=int.from_bytes(b[8:10],'little');payload=b[10+length:]
        assert hashlib.sha256(payload).hexdigest()==row['uncompressed_array_sha256']
checks['sparse_canonical_pack']={'classification':'SYNTHETIC_SCHEMA_ONLY_NOT_NATIVE_DATA','arrays':len(synthetic['arrays']),'array_bit_hashes_and_npz_CRC':'PASS','helper_DQ':'sparse values, no dense invented helper values','computed_valid_masks':['dq_computed_valid','csr_eligible','stage01_intermediates_computed_valid']}
checks['source_native_binding']='Implemented source built-in _yuri_armature_trace_r5 in patched bpy_interface inittab; unavailable until compile. Exact source/header types still compilation pending.'
checks['joined_RNA_route']='Fixed sync view_layer.update -> pinned rna_ViewLayer_update_tagged -> BKE_scene_graph_update_tagged; actual worker-join/runtime execution NOT TESTED'
(E/'STATIC_VALIDATION_R6.json').write_text(json.dumps(checks,indent=2),encoding='utf8')
for name in ('TEXT_SOURCE_RECEIPT.json','CMAKE_TEXT_RECEIPT.json'):
    shutil.copyfile(upstream/name,E/name)
request=BASE/'o1-guarded-native-resource-sizing-r2/dependencies/NATIVE_ARITHMETIC_INTERMEDIATE_REQUEST_R1_3b8383a6.md'
shutil.copyfile(request,E/request.name)
for p in E.iterdir():shutil.copyfile(p,OUT/p.name)
shutil.copyfile(request,OUT/'request-inputs-exact.json')
for name in extra:
    target=OUT/'workflow'/name;target.parent.mkdir(exist_ok=True);shutil.copyfile(ROOT/'scripts/native_readback_proposal'/name,target)
shutil.copyfile(ROOT/'scripts/native_readback_proposal/bpy_yuri_armature_trace_r5.hh',OUT/'workflow/bpy_yuri_armature_trace_r5.hh')
binding=BASE/'o1-native-armature-binding-r5'
for name in ('O1SourceBodyArmature.cs','O1SourceBodyRenderer.cs','PINNED_BINDING_SOURCE_RECEIPT.json','rna_layer.cc'):
    target=OUT/'upstream-reference'/name;target.parent.mkdir(exist_ok=True);shutil.copyfile(binding/name,target)
for name in ('DNA_anim_types.h','DNA_object_types.h','DNA_action_types.h','DNA_armature_types.h','ACTION_API_TEXT_RECEIPT.json'):
    target=OUT/'upstream-reference'/name;target.parent.mkdir(exist_ok=True);shutil.copyfile(validation/name,target)
for name in ('native_readback_proposal/armature_trace_r4.hh.in','native_readback_proposal/armature_trace_unpack_r1.py','r4_armature_instrumentation_draft_r6.py','r4_armature_draft_finalize_r6.py'):
    target=OUT/'workflow'/Path(name).name;target.parent.mkdir(exist_ok=True);shutil.copyfile(ROOT/'scripts'/name,target)
for name,row in manifest['sources'].items():
    target=OUT/'upstream'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(row['cached_path'],target)
for name in ('math_matrix_c.cc','DEG_depsgraph_query.hh','CMakeLists.txt'):
    target=OUT/'upstream-reference'/name;target.parent.mkdir(exist_ok=True);shutil.copyfile(upstream/'upstream'/name,target)
rows=[{'path':p.relative_to(OUT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
packet={'status':'TYPED_SOURCE_DRAFT_STATIC_CHECKED_NOT_COMPILED_CAPTURE_PENDING','files':rows,'source_commit':manifest['source_commit'],'patch_sha256':sha(E/'native_armature_typed_r6.patch')}
(OUT/'PACKET_MANIFEST.json').write_text(json.dumps(packet,indent=2),encoding='utf8')
shutil.copyfile(OUT/'PACKET_MANIFEST.json',E/'PACKET_MANIFEST.json')
digest=sha(OUT/'PACKET_MANIFEST.json');outbox=Path(r'C:/YuriTransfer/outbox')/('YURI_O1_ARMATURE_TYPED_DRAFT_R6_20261003_'+digest[:12]);assert not outbox.exists();outbox.mkdir()
archive=outbox/'YURI_O1_ARMATURE_TYPED_DRAFT_R6_20261003.zip'
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(OUT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for row in rows:assert hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
custody={'archive':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive),'member_hash_and_CRC':'PASS','manifest_sha256':digest}
(E/'PACKET_CUSTODY.json').write_text(json.dumps(custody,indent=2),encoding='utf8');print(json.dumps(custody))
