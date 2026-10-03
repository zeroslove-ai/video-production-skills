"""Static fixture checks and immutable research packet. Never build/run Blender."""
from pathlib import Path
import ast, hashlib, json, re, shutil, subprocess, zipfile
ROOT=Path(__file__).resolve().parents[1]
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
E=ROOT/'evidence/o1-native-armature-instrumentation-draft-r3'
OUT=BASE/'o1-native-armature-instrumentation-draft-r3'
assert not OUT.exists();OUT.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((E/'PATCH_APPLY_AND_SCOPE.json').read_text(encoding='utf8'))
fixture=Path(manifest['apply_check']['fixture'])
result=subprocess.run(['git','apply',str(E/'native_armature_typed_r3.patch')],cwd=fixture,capture_output=True,text=True)
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
for script in ('r4_armature_instrumentation_draft_r1.py','r4_armature_instrumentation_draft_r2.py','r4_armature_instrumentation_draft_r3.py','r4_armature_draft_finalize_r3.py','native_readback_proposal/armature_trace_unpack_r1.py'):
    ast.parse((ROOT/'scripts'/script).read_text(encoding='utf8'))
test=subprocess.run([r'C:/Program Files/Python313/python.exe',str(ROOT/'scripts/native_readback_proposal/armature_trace_unpack_r1.py'),'--self-test'],capture_output=True,text=True)
assert test.returncode==0
checks['raw_format_parser']=json.loads(test.stdout)
checks['DEG_get_ctime']='EXACT_PINNED_DECLARATION_FOUND; full ModifierEvalContext/matrix API compilation pending'
checks['actual_compile_runtime']='NOT_ATTEMPTED'
(E/'STATIC_VALIDATION_R3.json').write_text(json.dumps(checks,indent=2),encoding='utf8')
for name in ('TEXT_SOURCE_RECEIPT.json','CMAKE_TEXT_RECEIPT.json'):
    shutil.copyfile(upstream/name,E/name)
request=BASE/'o1-guarded-native-resource-sizing-r2/dependencies/NATIVE_ARITHMETIC_INTERMEDIATE_REQUEST_R1_3b8383a6.md'
shutil.copyfile(request,E/request.name)
for p in E.iterdir():shutil.copyfile(p,OUT/p.name)
for name in ('native_readback_proposal/armature_trace_r1.hh.in','native_readback_proposal/armature_trace_unpack_r1.py','r4_armature_instrumentation_draft_r3.py','r4_armature_draft_finalize_r3.py'):
    target=OUT/'workflow'/Path(name).name;target.parent.mkdir(exist_ok=True);shutil.copyfile(ROOT/'scripts'/name,target)
for name,row in manifest['sources'].items():
    target=OUT/'upstream'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(row['cached_path'],target)
for name in ('math_matrix_c.cc','DEG_depsgraph_query.hh','CMakeLists.txt'):
    target=OUT/'upstream-reference'/name;target.parent.mkdir(exist_ok=True);shutil.copyfile(upstream/'upstream'/name,target)
rows=[{'path':p.relative_to(OUT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(OUT.rglob('*')) if p.is_file()]
packet={'status':'TYPED_SOURCE_DRAFT_STATIC_CHECKED_NOT_COMPILED_CAPTURE_PENDING','files':rows,'source_commit':manifest['source_commit'],'patch_sha256':sha(E/'native_armature_typed_r3.patch')}
(OUT/'PACKET_MANIFEST.json').write_text(json.dumps(packet,indent=2),encoding='utf8')
shutil.copyfile(OUT/'PACKET_MANIFEST.json',E/'PACKET_MANIFEST.json')
digest=sha(OUT/'PACKET_MANIFEST.json');outbox=Path(r'C:/YuriTransfer/outbox')/('YURI_O1_ARMATURE_TYPED_DRAFT_R3_20261003_'+digest[:12]);assert not outbox.exists();outbox.mkdir()
archive=outbox/'YURI_O1_ARMATURE_TYPED_DRAFT_R3_20261003.zip'
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(OUT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for row in rows:assert hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
custody={'archive':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive),'member_hash_and_CRC':'PASS','manifest_sha256':digest}
(E/'PACKET_CUSTODY.json').write_text(json.dumps(custody,indent=2),encoding='utf8');print(json.dumps(custody))
