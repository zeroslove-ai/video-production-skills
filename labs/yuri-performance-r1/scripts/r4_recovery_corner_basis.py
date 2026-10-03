"""Original source UV/corner tangent basis on disposable mesh copies only."""
import bpy,json,hashlib
import numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent;E=ROOT/'evidence/o1-source-fidelity-recovery-r1';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-source-fidelity-recovery-r1')
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'),use_scripts=False)
meta=json.loads((E/'mesh_slot_UV_attributes_shape_deltas.json').read_text(encoding='utf8'));rows=[]
for r in meta:
    o=bpy.data.objects[r['renderer']];m=o.data.copy();a={};m.calc_loop_triangles()
    def arr(c,field,width,dtype):
        v=np.empty(len(c)*width,dtype=dtype);c.foreach_get(field,v);return v.reshape(-1,width) if width>1 else v
    a['loop_triangle_vertices']=arr(m.loop_triangles,'vertices',3,np.int32);a['loop_triangle_loops']=arr(m.loop_triangles,'loops',3,np.int32);a['triangle_polygon_index']=arr(m.loop_triangles,'polygon_index',1,np.int32)
    a['corner_normals']=arr(m.corner_normals,'vector',3,np.float32)
    uv=[]
    for i,u in enumerate(m.uv_layers):
        try:
            m.calc_tangents(uvmap=u.name);a[f'tangent_uv{i}']=arr(m.loops,'tangent',3,np.float32);a[f'bitangent_sign_uv{i}']=arr(m.loops,'bitangent_sign',1,np.float32);uv.append({'name':u.name,'tangent_array':f'tangent_uv{i}','bitangent_sign_array':f'bitangent_sign_uv{i}'})
        except RuntimeError as error:uv.append({'name':u.name,'unsupported':str(error)})
    p=OUT/'data'/f'{o.name}_corner_basis.npz';np.savez_compressed(p,**a);rows.append({'renderer':o.name,'file':p.relative_to(OUT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'UV':uv,'corner_normals':'source local-space evaluated original mesh normals before runtime modifiers','tangent_convention':'bitangent=sign*cross(normal,tangent); corner order original loop indices; no Y flip','triangulation':'Blender native calc_loop_triangles on copy; original polygon/slot indices retained; no source triangulation edit'});bpy.data.meshes.remove(m)
for p in (E/'CORNER_BASIS_RECEIPT.json',OUT/'metadata/CORNER_BASIS_RECEIPT.json'):p.write_text(json.dumps(rows,indent=2),encoding='utf8')
print('CORNER_BASIS_COMPLETE',len(rows))
