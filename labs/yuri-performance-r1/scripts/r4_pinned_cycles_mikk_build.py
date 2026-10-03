"""Build unmodified pinned algorithms in a NEW research workspace.

Usage: python this.py <packet download_receipt.json> <new build directory>
No Blender, product repository, GPU, render or existing frozen file writes.
"""
from pathlib import Path
import hashlib,json,sys,urllib.request,subprocess,shutil
receipt=Path(sys.argv[1]);work=Path(sys.argv[2]);assert not work.exists()
work.mkdir(parents=True)
files=json.loads(receipt.read_text())
for name,v in files.items():
    assert v['url'].startswith('https://raw.githubusercontent.com/blender/blender/9e2066aef7ef/')
    data=urllib.request.urlopen(v['url'],timeout=30).read()
    assert len(data)==v['bytes'] and hashlib.sha256(data).hexdigest()==v['sha256']
    p=work/'upstream'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
scene=(work/'upstream/intern/cycles/scene/mesh.cpp').read_bytes().decode()
wrapper=scene[scene.index('struct MikkMeshWrapper {'):scene.index('\nstatic void mikk_compute_tangents')]
tri=scene[scene.index('float3 Mesh::Triangle::compute_normal('):scene.index('\nbool Mesh::Triangle::valid')]
(work/'pinned_wrapper.inc').write_bytes((wrapper+'\n'+tri).encode())
shutil.copyfile(Path(__file__).with_name('r4_pinned_cycles_mikk_harness.cpp'),work/'harness.cpp')
cmd='''@echo off
call "C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\VC\\Auxiliary\\Build\\vcvars64.bat"
cl /nologo /std:c++20 /EHsc /O2 /fp:precise /LD /I"upstream\\intern\\cycles" /I"upstream\\intern\\mikktspace" harness.cpp /link /OUT:harness.dll
'''
(work/'compile.cmd').write_text(cmd)
r=subprocess.run(['cmd.exe','/c','compile.cmd'],cwd=work,capture_output=True)
(work/'compile.log').write_bytes(r.stdout+r.stderr)
assert r.returncode==0 and (work/'harness.dll').exists()
print('PINNED_ALGORITHM_REFERENCE build only; actual renderer buffer HOLD',work)
