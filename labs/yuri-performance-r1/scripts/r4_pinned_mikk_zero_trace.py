"""Metadata-only localization of existing canonical/raw/rest zero tangents."""
from pathlib import Path
import json,hashlib,numpy as np
LAB=Path(__file__).resolve().parent.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
ALG=BASE/'o1-pinned-cycles-triangle-mikk-cpu-reference-r1'
IN=BASE/'o1-dynamic-body-cycles-input-reference-r1'
OUT=BASE/'o1-pinned-mikk-zero-trace-r1';OUT.mkdir(exist_ok=True)
E=LAB/'evidence/o1-pinned-mikk-zero-trace-r1';E.mkdir(exist_ok=True)
assert not (OUT/'PINNED_MIKK_ZERO_TRACE.json').exists()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((ALG/'PINNED_CYCLES_TRIANGLE_MIKK_CPU_MANIFEST.json').read_text())
inputs=json.loads((IN/'DYNAMIC_BODY_CYCLES_INPUT_MANIFEST.json').read_text())
for v in m['files']:assert sha(ALG/v['path'])==v['sha256']
for v in inputs['files']:assert sha(IN/v['path'])==v['sha256']
restpath=BASE/'o1-source-fidelity-recovery-r1/data/Meshy_Body_NeutralCovered_corner_basis.npz'
topopath=BASE/'o1-source-fidelity-recovery-r1/data/Meshy_Body_NeutralCovered_original_mesh.npz'
for p in (restpath,topopath):assert sha(p)==inputs['inputs'][str(p)]['sha256']
rest=np.load(restpath,allow_pickle=False);topo=np.load(topopath,allow_pickle=False)
records=[];counts=[]
def areas(pos,uv,dtype):
    p=pos.astype(dtype);u=uv.astype(dtype)
    p1=p[1]-p[0];p2=p[2]-p[0];u1=u[1]-u[0];u2=u[2]-u[0]
    return {'geom_cross_length':float(np.linalg.norm(np.cross(p1,p2))),
            'UV_signed_double_area':float(u1[0]*u2[1]-u1[1]*u2[0])}
for row in m['frames']:
    f=next(v['path'] for v in m['files'] if row['clip'] in v['path'] and ('frame%03d'%row['frame']) in v['path'])
    orig=next(v['file']['path'] for v in inputs['frames'] if v['clip']==row['clip'] and v['frame']==row['frame'])
    d=np.load(ALG/f,allow_pickle=False);src=np.load(IN/orig,allow_pickle=False)
    packed=np.zeros(len(src['current_local_corner_normal']),np.uint32)
    decoded=np.zeros_like(src['current_local_corner_normal'])
    packed[d['triangle_source_corners']]=d['packed_normal_uint32']
    decoded[d['triangle_source_corners']]=d['decoded_normal']
    for variant in ('canonical','raw','rest'):
        prefix='' if variant=='canonical' else 'raw_normal_' if variant=='raw' else 'rest_triangle_'
        tangent=d[prefix+'tangent'];sign=d[prefix+'sign']
        corners=d['rest_triangle_source_corners' if variant=='rest' else 'triangle_source_corners']
        vertices=d['rest_triangle_source_vertices' if variant=='rest' else 'triangle_source_vertices']
        polys=rest['triangle_polygon_index'] if variant=='rest' else d['triangle_source_polygon']
        zeros=np.argwhere(np.linalg.norm(tangent.astype(float),axis=-1)==0)
        counts.append({'clip':row['clip'],'frame':row['frame'],'variant':variant,'zero_count':len(zeros)})
        for t,j in zeros:
            c=int(corners[t,j]);poly=int(polys[t]);vs=vertices[t];cs=corners[t]
            pos=src['current_local_position'][vs];uv=src['current_corner_UVMap'][cs]
            records.append({'clip':row['clip'],'frame':row['frame'],'variant':variant,
                'triangle_row':int(t),'local_corner':int(j),'source_corner':c,'source_vertex':int(vs[j]),
                'source_polygon':poly,'source_material_slot':int(topo['polygon_material_slot'][poly]),
                'triangle_source_corners':cs.tolist(),'triangle_source_vertices':vs.tolist(),
                'triangle_UV':uv.tolist(),'float32':areas(pos,uv,np.float32),'float64':areas(pos,uv,np.float64),
                'source_raw_corner_normal':src['current_local_corner_normal'][c].tolist(),
                'Cycles_packed_normal_uint32':int(packed[c]),'Cycles_decoded_corner_normal':decoded[c].tolist(),
                'source_fan_custom_normal_short2':src['original_custom_normal_short2'][c].tolist(),
                'tangent':tangent[t,j].tolist(),'sign':float(sign[t,j])})
receipt={'task_id':'ROOT_PM_PINNED_MIKK_ZERO_TRACE_R1','classification':'METADATA_ONLY_ON_PINNED_ALGORITHM_REFERENCE',
    'Blender_render_GPU_native_execution_source_writes':0,'all_tangent_unit_gate':'FAIL_NO_EXCLUSION_OR_FILL',
    'actual_Cycles_buffer':'HOLD','original_CORNER_normal_0_001_degree_gate':'UNCHANGED_NO_PACKING_WAIVER',
    'algorithm_manifest_sha256':sha(ALG/'PINNED_CYCLES_TRIANGLE_MIKK_CPU_MANIFEST.json'),
    'counts':counts,'zero_records':records,'files':[]}
for root in (OUT,E):(root/'PINNED_MIKK_ZERO_TRACE.json').write_text(json.dumps(receipt,indent=2),encoding='utf8')
print(json.dumps(counts),len(records))
