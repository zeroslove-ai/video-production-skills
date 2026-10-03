"""Frozen-array semantic inventory only: no bpy or normal implementation."""
import hashlib,json
from pathlib import Path
import numpy as np
LAB=Path(__file__).resolve().parent.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
R=BASE/'o1-source-fidelity-recovery-r1';S=BASE/'o1-raw-pose-driver-stage-reference-r1'
OUT=BASE/'o1-corner-normal-tangent-semantics-r1';E=LAB/'evidence/o1-corner-normal-tangent-semantics-r1'
E.mkdir(exist_ok=True);OUT.mkdir(exist_ok=True)
assert not (OUT/'CORNER_NORMAL_TANGENT_SEMANTIC_RECEIPT.json').exists(),'Do not overwrite frozen receipt'
inputs={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(p):inputs[str(p)]={'sha256':sha(p),'bytes':p.stat().st_size};return p
def load(p):return json.loads(record(p).read_text(encoding='utf8'))
meta=load(R/'metadata/mesh_slot_UV_attributes_shape_deltas.json')
basis=load(R/'metadata/CORNER_BASIS_RECEIPT.json')
rows=[]
for m in meta:
    n=m['renderer'];p=record(R/'data'/f'{n}_original_mesh.npz');b=record(R/'data'/f'{n}_corner_basis.npz')
    with np.load(p,allow_pickle=False) as original,np.load(b,allow_pickle=False) as corners:
        attributes={a['name']:a for a in m['attributes']}
        entries={}
        for attr in ('custom_normal','sharp_edge','sharp_face','.corner_edge'):
            a=attributes.get(attr)
            if a is None:
                entries[attr]={'present':False,'absent_semantics':'false for all elements' if attr.startswith('sharp_') else 'no packed custom normal override'}
                continue
            key=a['fields'][0]['array'];v=original[key]
            info={'present':True,'source_domain':a['domain'],'source_data_type':a['data_type'],'array':key,
                'serialized_dtype':str(v.dtype),'shape':list(v.shape),'min':int(v.min()),'max':int(v.max())}
            if attr=='custom_normal':
                assert a['data_type']=='INT16_2D' and a['domain']=='CORNER' and v.shape==(len(original['loop_vertex_indices']),2)
                assert np.array_equal(v.astype(np.int16).astype(v.dtype),v)
                info.update({'int16_roundtrip_lossless':True,'nonzero_alpha_corners':int(np.count_nonzero(v[:,0])),
                    'alpha_zero_corners':int(np.count_nonzero(v[:,0]==0)),
                    'packed_payload_sha256':hashlib.sha256(v.astype('<i2').tobytes()).hexdigest()})
            elif attr.startswith('sharp_'):info['true_elements']=int(np.count_nonzero(v))
            entries[attr]=info
        ce=original[entries['.corner_edge']['array']];cv=original['loop_vertex_indices'];edges=original['edge_vertex_indices']
        next_corner=np.arange(len(cv),dtype=np.int32)+1
        starts=original['polygon_loop_start'];sizes=original['polygon_loop_total']
        next_corner[starts+sizes-1]=starts
        wanted=np.sort(np.stack((cv,cv[next_corner]),axis=1),axis=1)
        assert np.array_equal(np.sort(edges[ce],axis=1),wanted),'Original corner-edge relation'
        assert corners['corner_normals'].shape==(len(cv),3)
        uv=[]
        for i,layer in enumerate(m['UV']):
            tkey=f'tangent_uv{i}';skey=f'bitangent_sign_uv{i}'
            has=tkey in corners.files
            uv.append({'name':layer['name'],'source_array':layer['array'],'corner_count':len(original[layer['array']]),
                'basis_tangent_array':tkey if has else None,'basis_sign_array':skey if has else None,
                'basis_sign_values':np.unique(corners[skey]).tolist() if has else None})
        sizes_unique,counts=np.unique(sizes,return_counts=True)
        rows.append({'renderer':n,'original_mesh_path':str(p),'original_mesh_sha256':sha(p),
            'original_corner_basis_path':str(b),'original_corner_basis_sha256':sha(b),
            'vertices':len(original['positions']),'corners':len(cv),'polygons':len(starts),
            'loose_vertices':int(len(original['positions'])-len(np.unique(cv))),
            'polygon_sizes':{str(int(k)):int(v) for k,v in zip(sizes_unique,counts)},
            'attributes':entries,'UV_layers':uv,'corner_edge_endpoint_relation_exact':True,
            'triangulation_pointers':{'vertices':'loop_triangle_vertices','corners':'loop_triangle_loops','polygon':'triangle_polygon_index'},
            'triangulation_scope':'Frozen original mesh basis, not guaranteed all-frame deformed triangulation or Unity importer diagonals.'})
stage=load(S/'RAW_POSE_DRIVER_STAGE_MANIFEST.json')
stage_diagnostics=[]
for f in stage['files']:
    if 'seven_stages' not in f['path']:continue
    p=record(S/f['path']);assert sha(p)==f['sha256']
    with np.load(p,allow_pickle=False) as z:
        for i in range(1,7):
            a=z[f'stage_{i-1:02d}_world_corner_normal'].astype(np.float64)
            b=z[f'stage_{i:02d}_world_corner_normal'].astype(np.float64)
            a/=np.linalg.norm(a,axis=1)[:,None];b/=np.linalg.norm(b,axis=1)[:,None]
            angle=np.degrees(np.arctan2(np.linalg.norm(np.cross(a,b),axis=1),np.sum(a*b,axis=1)))
            ci=int(angle.argmax())
            stage_diagnostics.append({'file':f['path'],'sha256':f['sha256'],'previous_stage':i-1,'current_stage':i,
                'corner_normal_array':f'stage_{i:02d}_world_corner_normal','max_normal_angle_degrees':float(angle[ci]),
                'worst_source_corner':ci,'worst_source_vertex':None,
                'corners_over_0_001_degrees':int(np.count_nonzero(angle>0.001))})
with np.load(R/'data/Meshy_Body_NeutralCovered_original_mesh.npz',allow_pickle=False) as body:
    for d in stage_diagnostics:d['worst_source_vertex']=int(body['loop_vertex_indices'][d['worst_source_corner']])
gaze=load(BASE/'o1-gaze-evaluated-corner-reference-r1/GAZE_EVALUATED_CORNER_MANIFEST.json')
gaze_file_list=gaze.get('files',gaze.get('chunks',[]))
upstream=[]
for p in sorted((OUT/'upstream').iterdir()):
    if p.name=='Apache-2.0.txt':url='https://www.apache.org/licenses/LICENSE-2.0.txt';license='Apache-2.0 license text'
    else:
        suffix=('intern/mikktspace/'+p.name if p.suffix=='.hh' else
            'source/blender/makesrna/intern/'+p.name if p.name=='rna_mesh_api.cc' else
            p.name if p.name=='COPYING' else 'source/blender/blenkernel/intern/'+p.name)
        url='https://raw.githubusercontent.com/blender/blender/9e2066aef7ef/'+suffix
        license='Apache-2.0' if p.suffix=='.hh' else 'GPL-2.0-or-later' if p.suffix=='.cc' else 'Blender COPYING'
    upstream.append({'path':'upstream/'+p.name,'sha256':sha(p),'bytes':p.stat().st_size,'url':url,'license':license,'modified':False})
receipt={'task_id':'YURI_O1_CORNER_NORMAL_TANGENT_SEMANTICS_R1','status':'DONE_SOURCE_SEMANTIC_SUPPORT_CONSUMER_GATE_PENDING',
    'upstream_build_ref':'9e2066aef7ef','original_meshes':rows,'all21_original_corner_edge_relations_verified':True,
    'normal_algorithm':{'entry':'Mesh::corner_normals -> normals_calc_corners for CORNER short2 custom_normal',
        'geometry':'Current mesh-local deformed positions, original polygon/corner-edge adjacency, sharp_edge and sharp_face. Face normals true, smooth fan angle weights, fan-local frame.',
        'packed':'Signed short2 alpha/beta semantic data, not xyz. Within each smooth fan, integer-average packed values before decoding in freshly built fan space. Alpha zero/invalid space returns fan normal.',
        'fan_order':'Retain pinned fan traversal/cyclic first-corner ordering and float normalization/approximate acos/degeneracy handling.',
        'cache':'Positions changed dirties face/point/CORNER normal caches; no cached rest normal reuse. These original deform-only stages do not intentionally author packed normal data.',
        'domain':'Absent sharp attributes default false; custom float3 direct attribute path differs from short2 source format. Head/face GN outputs must use existing evaluated gaze authority.'},
    'tangent_algorithm':{'benchmark_entry':'RNA Mesh.calc_tangents -> calc_uv_tangent_tris_quads -> pinned Mikk; frozen original/gaze references used this route.',
        'unsupported_original_basis':[{'renderer':r['renderer'],'UV':uv} for r in basis for uv in r['UV'] if 'unsupported' in uv],
        'inputs':'Final current local position + final source CORNER normal + UVMap per original corner + original tri/quad polygons.',
        'quad_diagonal':'Mikk chooses shortest UV diagonal; tie chooses shortest geometric diagonal, tie prefers 0-2. Unity triangulation-only input may choose differently.',
        'general_route':'calc_uv_tangents supports corner-tris with quad reconstruction; do not conflate with the RNA benchmark route or PBR renderer acceptance.',
        'output':'Corner tangent xyz + orientation sign (+1/-1), B=sign*cross(N,T). Recalculate for deformed normals/geometry; preserve UV seams.',
        'world_transport':'n=normalize(n_local inverse(A)) row-vector; t=normalize(project(t_local A^T perpendicular to n)); bitangent sign gains sign(det(A)). Further consumer mirror/UV flips need explicit verified transport, no double flip.'},
    'reference_pointers':{'raw_pose_stage_manifest':str(S/'RAW_POSE_DRIVER_STAGE_MANIFEST.json'),
        'full_body_manifest':str(BASE/'o1-full-body-deformation-reference-r1/FULL_BODY_DEFORMATION_MANIFEST.json'),
        'gaze_evaluated_manifest':str(BASE/'o1-gaze-evaluated-corner-reference-r1/GAZE_EVALUATED_CORNER_MANIFEST.json'),
        'gaze_evaluated_files':gaze_file_list},'stage_normal_diagnostics':stage_diagnostics,
    'consumer_fields_if_exact_mapping_is_missing':['Actual cloned mesh normal/tangent4/UV0 buffers and vertex/corner counts, normal/tangent import settings',
        'Original source controlpoint and loop/corner correspondence plus actual consumer triangle/submesh corner IDs/winding',
        'Verified geometry basis K, local-to-world matrices, UV V-flip and tangent handedness/sign policy',
        'Normal texture color-space, green-channel convention and shader negative-scale handling for separate PBR gate'],
    'scope':'Specification/evidence only; no competing runtime implementation, no source evaluation/export/render or PM/product writes.',
    'source_or_consumer_writes':0,'Blender_jobs':0,'files':upstream,'inputs':inputs}
for p in (OUT,E):(p/'CORNER_NORMAL_TANGENT_SEMANTIC_RECEIPT.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps({'meshes':len(rows),'custom_normal_meshes':[r['renderer'] for r in rows if r['attributes']['custom_normal']['present']],
    'stage_max_angles':[(d['file'],d['current_stage'],d['max_normal_angle_degrees']) for d in stage_diagnostics]},indent=2))
