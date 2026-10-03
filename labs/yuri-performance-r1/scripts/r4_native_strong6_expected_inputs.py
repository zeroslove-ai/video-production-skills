"""Prepare only existing frozen local input bytes; no Blender or native execution."""
from pathlib import Path
import json, hashlib
import numpy as np
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-guarded-native-resource-sizing-r1'
assert not (OUT/'GUARDED_NATIVE_RESOURCE_MANIFEST.json').exists(), 'frozen packet'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
current=BASE/'o1-dynamic-body-cycles-input-reference-r1/YRA_R4_Struggle_Strong_Loop_frame006_actual_evaluated_cycles_inputs.npz'
reference=BASE/'o1-pinned-cycles-triangle-mikk-cpu-reference-r1/YRA_R4_Struggle_Strong_Loop_frame006_pinned_algorithm_reference.npz'
assert sha(current)=='156a7c2880bfeedb523196a1572d50943dd53e6780cc5789eced5e5b4ca8cbbd'
original=json.loads((reference.parent/'PINNED_CYCLES_TRIANGLE_MIKK_CPU_MANIFEST.json').read_text())
assert sha(reference)==next(r['sha256'] for r in original['files'] if r['path']==reference.name)
with np.load(current,allow_pickle=False) as d, np.load(reference,allow_pickle=False) as r:
    corners=d['current_triangle_source_corners']
    arrays={'position.f32':d['current_local_position'],
      'packed_normal.u32':r['packed_normal_uint32'],
      'uv.f32':d['current_corner_UVMap'][corners],
      'corner_tris.i32':corners,
      'corner_vertices.i32':d['original_corner_to_source_vertex'],
      'triangles.i32':d['current_triangle_source_vertices']}
    dest=OUT/'expected-Strong6';dest.mkdir(exist_ok=True);files=[]
    for name,array in arrays.items():
        dtype='<f4' if name.endswith('.f32') else '<u4' if name.endswith('.u32') else '<i4'
        array=np.ascontiguousarray(array,dtype=dtype);p=dest/name
        data=array.tobytes()
        if p.exists(): assert p.read_bytes()==data, 'expected data overwrite prohibited'
        else:p.write_bytes(data)
        files.append({'path':name,'dtype':dtype,'shape':list(array.shape),'bytes':len(data),'sha256':sha(p)})
receipt={'classification':'FROZEN_EXPECTED_INPUTS_NOT_NEW_CYCLES_BUFFER','clip':'YRA_R4_Struggle_Strong_Loop','frame':6,
 'source_R4_sha256':'a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa',
 'Action_library_sha256':'6874ec69d5721f385d31edaa06ef0d58c89a543b98bacd961f8f575ff57eef4d',
 'packed_normal_origin':'pinned native algorithm reference, not actual renderer; exact comparison is a reject-on-drift gate, not equivalence proof',
 'inputs':{str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in (current,reference)},'files':files}
(dest/'EXPECTED_INPUTS.json').write_text(json.dumps(receipt,indent=2))
print(json.dumps({'expected_files':len(files),'bytes':sum(r['bytes'] for r in files),'new_native_calls':0}))
