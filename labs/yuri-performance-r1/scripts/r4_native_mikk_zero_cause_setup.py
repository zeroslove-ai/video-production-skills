"""Instrument a separate copy of frozen CPU harness; source originals untouched."""
from pathlib import Path
import difflib,shutil,subprocess,hashlib,json,sys
LAB=Path(__file__).resolve().parent.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
ORIG=BASE/'o1-pinned-cycles-triangle-mikk-cpu-reference-r1'
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else BASE/'o1-native-mikk-zero-cause-trace-r1'
OUT.mkdir(exist_ok=True)
if not (OUT/'upstream').exists():
    shutil.copytree(ORIG/'upstream',OUT/'upstream')
    for n in ('harness.cpp','pinned_wrapper.inc','compile.cmd'):shutil.copyfile(ORIG/n,OUT/n)
assert not (OUT/'instrumentation.diff').exists()
shutil.copyfile(Path(__file__).with_name('r4_native_mikk_diagnostic_hooks.h'),OUT/'diagnostic_hooks.h')
h=OUT/'upstream/intern/mikktspace/mikktspace.hh'
original=h.read_text();s=original
edits=[
 ('    });\n\n    // force otherwise healthy quads',
  '      diag::init(triangle.faceIdx,triangle.groupWithAny,triangle.orientPreserving,signedAreaSTx2,vOs,vOt,triangle.tangent);\n    });\n\n    // force otherwise healthy quads'),
 ('  void generateTSpaces()\n  {\n',
  '  void generateTSpaces()\n  {\n    for (const Triangle &dt : triangles) for (uint dj=0;dj<3;dj++)\n      diag::assign(dt.faceIdx,dt.faceVertex[dj],dt.group[dj],dt.groupWithAny,dt.markDegenerate,dt.tangent);\n'),
 ('        if constexpr (atomic) {\n',
  '        diag::contribution(triangle.faceIdx,triangle.faceVertex[i],groupId,fCos[i],fast_acosf(std::clamp(fCos[i],-1.0f,1.0f)),n[i],triangle.tangent,project(n[i],triangle.tangent),triangle.tangent-n[i]*dot(n[i],triangle.tangent),tangent,groups[groupId].tangent);\n        if constexpr (atomic) {\n'),
 ('          groups[groupId].accumulateTSpace(tangent);\n',
  '          groups[groupId].accumulateTSpace(tangent);\n          diag::group("sum_after",groupId,groups[groupId].tangent);\n'),
 ('      group.normalizeTSpace();\n',
  '      diag::group("pre_normalize",uint(&group-groups.data()),group.tangent);\n      group.normalizeTSpace();\n      diag::group("post_normalize",uint(&group-groups.data()),group.tangent);\n')]
for old,new in edits:
    assert s.count(old)==1,(old,s.count(old));s=s.replace(old,new)
h.write_text(s)
(OUT/'instrumentation.diff').write_text(''.join(difflib.unified_diff(original.splitlines(True),s.splitlines(True),fromfile='original_pinned/mikktspace.hh',tofile='diagnostic_fork/mikktspace.hh')))
p=OUT/'harness.cpp';s=p.read_text();assert s.count('#include "mikktspace.hh"')==1
p.write_text(s.replace('#include "mikktspace.hh"','#include "diagnostic_hooks.h"\n#include "mikktspace.hh"'))
r=subprocess.run(['cmd.exe','/c','compile.cmd'],cwd=OUT,capture_output=True)
(OUT/'compile.log').write_bytes(r.stdout+r.stderr)
assert r.returncode==0 and (OUT/'harness.dll').exists(),r.stdout[-2000:]
print('DIAGNOSTIC_FORK_COMPILED',hashlib.sha256((OUT/'harness.dll').read_bytes()).hexdigest())
