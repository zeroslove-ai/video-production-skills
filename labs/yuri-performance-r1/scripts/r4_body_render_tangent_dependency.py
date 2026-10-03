"""Source metadata/upstream receipt; no Blender or shader execution."""
import hashlib,json
from pathlib import Path
LAB=Path(__file__).resolve().parent.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
R=BASE/'o1-source-fidelity-recovery-r1'
OUT=BASE/'o1-body-render-tangent-dependency-r1';E=LAB/'evidence/o1-body-render-tangent-dependency-r1'
OUT.mkdir(exist_ok=True);E.mkdir(exist_ok=True)
assert not (OUT/'BODY_RENDER_TANGENT_DEPENDENCY_RECEIPT.json').exists(),'Preserve frozen receipt'
inputs={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(p):inputs[str(p)]={'sha256':sha(p),'bytes':p.stat().st_size};return p
def load(p):return json.loads(record(p).read_text(encoding='utf8'))
materials=load(R/'metadata/executable_material_graphs.json')
meshes=load(R/'metadata/mesh_slot_UV_attributes_shape_deltas.json')
images=load(R/'metadata/exact_texture_receipt.json');image_by_name={v['image']:v for v in images}
source_scene=load(R/'metadata/neutral_camera_light_color_driver_state.json')
normal_contract=load(BASE/'o1-corner-normal-tangent-semantics-r1/CORNER_NORMAL_TANGENT_SEMANTIC_RECEIPT.json')
material_rows={}
for mat in set(name for m in meshes for name in m['material_slots']):
    g=materials[mat]['node_graph'];nodes={n[0]:n for n in g['nodes']}
    outputs=[n[0] for n in g['nodes'] if n[1].get('type')=='OUTPUT_MATERIAL' and n[1].get('is_active_output') and n[1].get('target') in ('ALL','CYCLES')]
    assert outputs,mat
    seen=set(outputs);changed=True
    while changed:
        changed=False
        for src,ss,dest,ds in g['links']:
            if dest in seen and src not in seen:seen.add(src);changed=True
    maps=[];bumps=[];tangents=[];texture_rows=[]
    for name in seen:
        n=nodes[name];prop=n[1];type_=prop.get('type');sockets={s[0]:s[1] for s in n[5]}
        if type_=='NORMAL_MAP':
            maps.append({'name':name,'space':prop.get('space'),'uv_map':prop.get('uv_map'),
                'convention':prop.get('convention'),'base':prop.get('base'),'mute':prop.get('mute'),
                'Strength':sockets.get('Strength'),'Color':sockets.get('Color'),
                'incoming_links':[l for l in g['links'] if l[2]==name],
                'outgoing_links':[l for l in g['links'] if l[0]==name]})
        if type_=='BUMP':bumps.append({'name':name,'properties':prop,'inputs':n[5]})
        if type_=='TANGENT':tangents.append({'name':name,'properties':prop})
        if type_=='TEX_IMAGE':
            image=prop.get('image');tex=image_by_name.get(image[1]) if image else None
            texture_rows.append({'node':name,'image':image,'vector_linked':sockets.get('Vector',{}).get('is_linked'),
                'interpolation':prop.get('interpolation'),'projection':prop.get('projection'),'extension':prop.get('extension'),
                'image_receipt':tex})
    unknown=[name for name in seen if nodes[name][1].get('type')=='GROUP']
    assert not unknown,(mat,'Nested group analysis needs exact group graph')
    material_rows[mat]={'active_output_nodes':outputs,'reachable_node_names':sorted(seen),
        'surface_links':g['links'],'NormalMap':maps,'Bump':bumps,'Tangent':tangents,
        'textures':texture_rows,'material_properties':materials[mat]['properties'],
        'material_driver_binding':g.get('animation'),
        'graph_sha256':hashlib.sha256(json.dumps(g,sort_keys=True,separators=(',',':')).encode()).hexdigest()}
mesh_rows=[]
for m in meshes:
    norm=next(r for r in normal_contract['original_meshes'] if r['renderer']==m['renderer'])
    used=[]
    for mat in m['material_slots']:
        v=material_rows[mat]
        used.append({'material':mat,'connected_NormalMap_count':len(v['NormalMap']),
            'connected_Bump_count':len(v['Bump']),'connected_Tangent_node_count':len(v['Tangent']),
            'NormalMap_spaces':[n['space'] for n in v['NormalMap']]})
    mesh_rows.append({'renderer':m['renderer'],'original_material_slots':m['material_slots'],
        'slot_dependencies':used,'UV':m['UV'],'polygon_sizes':norm['polygon_sizes'],
        'RNA_original_tangent_arrays':[x['basis_tangent_array'] for x in norm['UV_layers']],
        'has_ngons':any(int(k)>4 for k in norm['polygon_sizes']),
        'original_modifier_types':[x['type'] for x in m['modifiers']]})
body=next(x for x in mesh_rows if x['renderer']=='Meshy_Body_NeutralCovered')
body_mat=material_rows['R4_Meshy_OriginalDetail_FaceMatched']
assert len(body_mat['NormalMap'])==1 and not body_mat['Bump']
assert not any(l[2] in body_mat['active_output_nodes'] and l[3]=='Displacement' for l in body_mat['surface_links'])
node=body_mat['NormalMap'][0]
assert node['space']=='TANGENT' and node['convention']=='OPENGL' and node['base']=='DISPLACED'
assert node['Strength']['default_value']==0.3499999940395355 and not node['Strength']['is_linked']
assert node['uv_map']=='' and body['UV'][0]['name']=='UVMap' and body['UV'][0]['active_render']
normal_image=image_by_name['R4_Meshy_Normal_Safe_4K']
assert normal_image['properties']['colorspace_settings'][1]=='Non-Color' and normal_image['colorspace']['is_data']
for v in normal_image['packed']:
    p=record(R/v['path']);assert sha(p)==v['sha256']
license_source=record(BASE/'o1-corner-normal-tangent-semantics-r1/upstream/Apache-2.0.txt')
target=OUT/'upstream/Apache-2.0.txt';assert not target.exists();target.write_bytes(license_source.read_bytes())
paths={'mesh.cpp':'intern/cycles/blender/mesh.cpp','shader_nodes.cpp':'intern/cycles/scene/shader_nodes.cpp',
    'cycles_scene_mesh.cpp':'intern/cycles/scene/mesh.cpp','cycles_scene_geometry.cpp':'intern/cycles/scene/geometry.cpp',
    'types_normal.h':'intern/cycles/util/types_normal.h','Apache-2.0.txt':None}
files=[]
for name,path in paths.items():
    p=OUT/'upstream'/name;assert p.exists()
    files.append({'path':'upstream/'+name,'sha256':sha(p),'bytes':p.stat().st_size,
        'url':'https://raw.githubusercontent.com/blender/blender/9e2066aef7ef/'+path if path else 'https://www.apache.org/licenses/LICENSE-2.0.txt',
        'license':'Apache-2.0','modified':False})
receipt={'task_id':'ROOT_PM_O1_BODY_RENDER_TANGENT_DEPENDENCY_R1','status':'DONE_SOURCE_DEPENDENCY_RUNTIME_TANGENT_PROOF_HOLD',
    'source_render_engine':source_scene['render']['engine'],'source_build_ref':'9e2066aef7ef','materials':material_rows,'all21_mesh_dependencies':mesh_rows,
    'Body_dependency':{'NormalMap_material':'R4_Meshy_OriginalDetail_FaceMatched','normal_node':node,
        'effective_default_UV':'UVMap','normal_image':normal_image,'material_displacement_connected':False,
        'shader_Bump_nodes':0,'original_slots':'Three source slots refer to same material; do not collapse canonical slots.',
        'normal_map_dependency_active':True},
    'render_route_correction':{'actual_Cycles_nonsubdivision':'Blender corner_tris/current CORNER normals/UV -> Cycles triangles/packed_normal attributes -> Mesh::update_tangents -> Cycles MikkMeshWrapper (three vertices per face).',
        'BKE_general':'BKE calc_uv_tangents corner-tris with quad reconstruction is a separate path. Do not assert it was the canonical Cycles renderer tangent route.',
        'RNA':'RNA calc_tangents remains tri/quad only; Body400 ngons unsupported; LowerLashes have no UV and no connected NormalMap/Bump, no attempted failed UV call.',
        'normal_packing':'Cycles encodes normals octahedrally into uint32 (two16-bit components) and decodes before Mikk; distinct from original fan-space short2 custom_normal and raw float32 reference.',
        'shader_attribute':'Body empty UV name and DISPLACED base request standard UV tangent/sign; OPENGL compile invert_green=0. Material output Displacement is not linked.',
        'proof_limit':'Static graph and pinned-source path verified; actual Cycles packed normal/tangent buffers and dynamic triangle tessellation have not been captured.'},
    'consumer_minimum_inputs':['Actual clone/evaluated normal and tangent4 buffers plus vertex/source-loop/triangle-corner identity',
        'Dynamic rendered triangle corner list and winding/source polygon map at QA frames, UV0 values and V-flip convention',
        'Source-local positions/CORNER normals with coordinate basis K and object-world matrices, mirror/negative-scale sign handling',
        'Imported normal image SHA/color-space/OpenGL convention/normal-strength0.349999994 and actual applied shader normal result',
        'If exact Cycles equivalence is required: actual packed_normal attribute/tangent input and renderer normal-map output, obtained only by separately authorized probe'],
    'failure_log':['Initial guessed mesh_tangent.cpp and normal_map.h upstream paths were404; actual tangent implementation was found in Cycles scene/mesh.cpp. No render/probe was substituted.'],
    'source_geometry_or_material_changes':0,'Blender_jobs':0,'runtime_tangent_or_PBR_verdict':'HOLD',
    'files':files,'inputs':inputs}
assert receipt['source_render_engine']=='CYCLES'
for p in (OUT,E):(p/'BODY_RENDER_TANGENT_DEPENDENCY_RECEIPT.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False),encoding='utf8')
print('BODY_RENDER_DEPENDENCY_COMPLETE',len(mesh_rows),len(material_rows),node['Strength']['default_value'])
