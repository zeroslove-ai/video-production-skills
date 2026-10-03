"""Bounded official source/license TEXT receipts only; never archive or LFS payload fetch."""
from pathlib import Path
import urllib.request, hashlib, json, concurrent.futures
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-guarded-native-resource-sizing-r1')
COMMIT='9e2066aef7ef7e20c142ad7bd3303138a4304c93'
paths=['intern/cycles/blender/object.cpp','intern/cycles/blender/CMakeLists.txt',
       'intern/cycles/scene/mesh.h','intern/cycles/device/device.h',
       'intern/cycles/device/cpu/device_impl.h','intern/cycles/device/device.cpp',
       'intern/cycles/session/session.cpp','intern/cycles/bvh/bvh.cpp',
       'intern/cycles/util/task.h','COPYING','CMakeLists.txt',
       'build_files/cmake/platform/platform_win32.cmake',
       'source/blender/python/intern/bpy_rna.hh',
       'source/blender/render/RE_engine.h',
       'source/blender/render/intern/engine.cc',
       'source/blender/blenkernel/BKE_context.hh']
requests=[('upstream/'+p,f'https://raw.githubusercontent.com/blender/blender/{COMMIT}/{p}') for p in paths]
requests.append(('licenses/LLVM_LICENSE.txt','https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-20.1.8/llvm/LICENSE.TXT'))
def fetch(item):
    name,url=item;p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    if not p.exists():
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40) as r:
            data=r.read(1024*1024+1)
        assert len(data)<=1024*1024, name
        data.decode('utf8');p.write_bytes(data)
    return {'path':name,'url':url,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(fetch,requests))
(OUT/'TEXT_FETCH_RECEIPT.json').write_text(json.dumps({'scope':'official UTF-8 text only; no binaries','files':rows},indent=2))
print(json.dumps({'files':len(rows),'bytes':sum(r['bytes'] for r in rows),'binary_payload_bytes':0}))
