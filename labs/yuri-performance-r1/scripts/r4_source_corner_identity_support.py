"""Read frozen source/FBX and Unity inventory; preserve ambiguous consumer IDs.

Plain Python, no bpy, scene load, geometry edits, or exporter execution.
"""
import gzip, hashlib, json, subprocess, sys, types
from pathlib import Path
import numpy as np

LAB = Path(__file__).resolve().parent.parent
BASE = Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
SOURCE = BASE/'o1-source-fidelity-recovery-r1'
FBX = BASE/'o1-original-bind-serialization-r1/YURI_O1_R4_NATIVE_CARRIER_20261003_R1.fbx'
OUT = BASE/'o1-source-corner-identity-support-r1'
E = LAB/'evidence/o1-source-corner-identity-support-r1'
assert not (OUT/'SOURCE_CORNER_IDENTITY_RECEIPT.json').exists(), 'Do not overwrite frozen receipt'
OUT.mkdir(exist_ok=True); E.mkdir(exist_ok=True)
inputs = {}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def record(p):
    inputs[str(p)] = {'sha256': sha(p), 'bytes': p.stat().st_size}
    return p
def read(p): return json.loads(record(p).read_text(encoding='utf8'))
def array(p): return np.load(record(p), allow_pickle=False)
addon = Path(r'C:/Program Files/Blender Foundation/Blender 5.2/5.2/scripts/addons_core/io_scene_fbx')
pkg = types.ModuleType('io_scene_fbx'); pkg.__path__ = [str(addon)]; sys.modules['io_scene_fbx'] = pkg
from io_scene_fbx.parse_fbx import parse
record(FBX)
assert sha(FBX) == '3b37f3570742617b42215e980a70260490ffe92c7480c33a5de5060dd38c90c1'
root, version = parse(str(FBX))
sections = {x.id: x for x in root.elems}
objects = {o.props[0]: o for o in sections[b'Objects'].elems}
cons = [tuple(c.props) for c in sections[b'Connections'].elems if c.props[0] == b'OO']
def name(o): return o.props[1].decode(errors='replace').split('\x00')[0]
def field(o, key): return next(c.props[0] for c in o.elems if c.id == key)
models = {uid:name(o) for uid,o in objects.items() if o.id == b'Model' and o.props[-1] == b'Mesh'}
geometry = {models[parent]:(child,objects[child]) for _,child,parent,*_ in cons if parent in models and child in objects and objects[child].id == b'Geometry' and objects[child].props[-1] == b'Mesh'}
metadata = read(SOURCE/'metadata/mesh_slot_UV_attributes_shape_deltas.json')
all_meshes = []; head = None
for meta in metadata:
    renderer = meta['renderer']; original = array(SOURCE/'data'/f'{renderer}_original_mesh.npz')
    gid, geo = geometry[renderer]
    points = np.asarray(field(geo,b'Vertices')).reshape(-1,3)
    encoded = np.asarray(field(geo,b'PolygonVertexIndex'))
    cp = np.where(encoded < 0, -encoded-1, encoded)
    ends = np.flatnonzero(encoded < 0)+1
    starts = np.r_[0, ends[:-1]]
    layers = [x for x in geo.elems if x.id == b'LayerElementUV']
    uv_checks = []
    for layer, source_uv in zip(layers,meta['UV']):
        assert field(layer,b'MappingInformationType') == b'ByPolygonVertex'
        assert field(layer,b'ReferenceInformationType') == b'IndexToDirect'
        uv_idx = np.asarray(field(layer,b'UVIndex'))
        uv_direct = np.asarray(field(layer,b'UV')).reshape(-1,2)
        uv_values = uv_direct[uv_idx]
        uv_checks.append({'source_layer':source_uv['name'], 'FBX_layer':field(layer,b'Name').decode(),
            'loop_values_exact':bool(np.array_equal(uv_values,original[source_uv['array']]))})
    material = next(x for x in geo.elems if x.id == b'LayerElementMaterial')
    material_mapping = field(material,b'MappingInformationType')
    assert material_mapping in (b'ByPolygon',b'AllSame')
    mat = np.asarray(field(material,b'Materials'))
    if material_mapping == b'AllSame': mat = np.repeat(mat,len(starts))
    model_id = next(uid for uid,n in models.items() if n==renderer)
    materials = [name(objects[child]) for _,child,parent,*_ in cons if parent==model_id and child in objects and objects[child].id==b'Material']
    source_materials = meta['material_slots']
    semantic_materials_equal = all(materials[int(f)]==source_materials[int(s)] for f,s in zip(mat,original['polygon_material_slot']))
    result = {'renderer':renderer,'FBX_geometry_id':gid,'control_points':len(points),
        'source_loose_vertices':int(len(points)-len(np.unique(cp))),
        'positions_exact':bool(np.array_equal(points,original['positions'])),
        'polygon_corner_controlpoints_exact':bool(np.array_equal(cp,original['loop_vertex_indices'])),
        'polygon_starts_exact':bool(np.array_equal(starts,original['polygon_loop_start'])),
        'polygon_sizes_exact':bool(np.array_equal(np.diff(np.r_[0,ends]),original['polygon_loop_total'])),
        'polygon_material_slots_exact':bool(np.array_equal(mat,original['polygon_material_slot'])),
        'polygon_material_names_exact':semantic_materials_equal,
        'FBX_material_slots':materials,'source_material_slots':source_materials,
        'UV_layer_count_exact':len(layers)==len(meta['UV']), 'UV':uv_checks}
    assert all(result[k] for k in ('positions_exact','polygon_corner_controlpoints_exact','polygon_starts_exact','polygon_sizes_exact','polygon_material_names_exact','UV_layer_count_exact')), result
    assert all(x['loop_values_exact'] for x in uv_checks)
    all_meshes.append(result)
    if renderer == 'Character_Body_Head': head = (meta, original, gid, geo, cp, starts, uv_idx, uv_values)
    else: original.close()

meta, original, gid, geo, cp, starts, uv_idx, uv_values = head
corners = array(SOURCE/'data/Character_Body_Head_corner_basis.npz')
candidate = array(BASE/'o1-renderer-basis-diagnostic-r1/R4_Renderer_Position_Basis_Candidates_And_Source_Index_Sets.npz')
offsets = candidate['Character_Body_Head_candidate_offsets']; ids = candidate['Character_Body_Head_candidate_source_vertices']
ambiguous = [int(i) for i in np.flatnonzero(np.diff(offsets)>1)]
assert ambiguous == [9859,9865,12926,12929,12977,12980]
# Resolve actual FBX shape -> channel -> blendshape -> mesh, without assuming names alone identify geometry.
children = {}
for _,child,parent,*_ in cons: children.setdefault(parent,[]).append(child)
shape_deltas = {}
for bid in children.get(gid,[]):
    if objects[bid].props[-1] != b'BlendShape': continue
    for channel in children.get(bid,[]):
        if objects[channel].props[-1] != b'BlendShapeChannel': continue
        for sid in children.get(channel,[]):
            if objects[sid].id != b'Geometry' or objects[sid].props[-1] != b'Shape': continue
            shape = objects[sid]
            shape_deltas[name(objects[channel])] = {
                'FBX_shape_id':sid, 'FBX_channel_id':channel,
                'rows':dict(zip(map(int,field(shape,b'Indexes')),np.asarray(field(shape,b'Vertices')).reshape(-1,3)))}
source_keys = meta['ShapeKeys']
records = []
for vi in sorted(set(int(v) for i in ambiguous for v in ids[offsets[i]:offsets[i+1]])):
    loops = []
    for li in np.flatnonzero(cp==vi):
        pi = int(np.searchsorted(starts,li,side='right')-1)
        tris = np.flatnonzero(np.any(corners['loop_triangle_loops']==li,axis=1))
        loops.append({'source_loop':int(li),'source_polygon':pi,'polygon_corner_ordinal':int(li-starts[pi]),
            'material_slot':int(original['polygon_material_slot'][pi]),'UV_layer':'UVMap',
            'UV':uv_values[li].tolist(),'FBX_UV_direct_index':int(uv_idx[li]),
            'source_corner_normal':corners['corner_normals'][li].tolist(),
            'source_tangent_uv0':corners['tangent_uv0'][li].tolist(),
            'source_bitangent_sign':float(corners['bitangent_sign_uv0'][li]),
            'source_triangle_ids':tris.tolist()})
    deltas = []
    for key in source_keys:
        delta = original[key['array']][vi]
        exported = shape_deltas.get(key['name'])
        fb = np.asarray(exported['rows'].get(vi,[0.,0.,0.])) if exported else None
        deltas.append({'name':key['name'],'relative_key':key['relative_key'],'source_relative_delta':delta.tolist(),
            'FBX_channel_present':exported is not None,'FBX_sparse_delta':None if fb is None else fb.tolist(),
            'FBX_delta_exact':None if fb is None else bool(np.array_equal(fb,delta))})
    records.append({'renderer':'Character_Body_Head','source_vertex':vi,'FBX_controlpoint':vi,
        'position':original['positions'][vi].tolist(),'corners':loops,'ShapeKeys':deltas})
by_id = {r['source_vertex']:r for r in records}
pairs = []
for pair in sorted(set(tuple(map(int,ids[offsets[i]:offsets[i+1]])) for i in ambiguous)):
    a,b = map(by_id.get,pair)
    differences = [x['name'] for x,y in zip(a['ShapeKeys'],b['ShapeKeys']) if x['source_relative_delta']!=y['source_relative_delta']]
    pairs.append({'source_candidates':list(pair),'UV_sets_equal': sorted(x['UV'] for x in a['corners'])==sorted(x['UV'] for x in b['corners']),
        'different_source_relative_shape_deltas':differences,
        'consumer_identity_resolved':False})
ref = 'fd19f8d6cd4efa897ec5338afacfd7939c25b10d'
path = 'docs/evidence/root-pm-o1-original-bind/raw-inventory.json.gz'
blob = subprocess.check_output(['git','show',ref+':'+path],cwd=r'C:/Users/JAEWAN/projects/yuri-root-pm-r1')
raw = json.loads(gzip.decompress(blob))
unity_head = next(r for r in raw['carrier']['renderers'] if r['name']=='Character_Body_Head')
request = {'carrier_sha256':sha(FBX),'renderer':'Character_Body_Head','split_vertex_ids':ambiguous,
    'required_fields':['Actual isolated-clone Unity mesh UV0 for the six split vertices',
        'Actual triangles/submesh and corner ordinals touching the six split vertices; winding/axis conversion documented',
        'Actual per-frame named blendshape delta vertices for these vertices, if UV/topology leaves ambiguity',
        'Actual normals/tangents and importer triangulation provenance if preceding fields still tie',
        'Clone/mesh identity, carrier hash, capture commit and blob SHA'],
    'existing_Unity_renderer_fields':sorted(unity_head),
    'existing_Unity_shape_fields':sorted(unity_head['shapes'][0]),
    'no_nearest_position_assignment':True}
receipt = {'task_id':'YURI_O1_SOURCE_CORNER_IDENTITY_SUPPORT_R1','status':'DONE_SOURCE_SUPPORT_CONSUMER_MAPPING_PENDING',
    'scope':'Frozen source/actual FBX data only. No bpy, source binary write, mesh edit, Blender export or renderer transform change.',
    'FBX_version':version,'all21_meshes':all_meshes,'head_candidate_semantics':records,'candidate_pair_comparison':pairs,
    'retained_Unity_candidates':[{'Unity_split_vertex':i,'source_candidates':ids[offsets[i]:offsets[i+1]].tolist()} for i in ambiguous],
    'semantic_key':['renderer','source_vertex/FBX_controlpoint','source_polygon','source_loop/polygon_corner_ordinal','UV_layer/UV_value','material_slot','ShapeKey_name/relative_key/delta'],
    'triangulation_limit':'Frozen source loop triangulation available; actual FBX polygons retained. Unity importer diagonal/order is not proven without consumer triangles.',
    'source_head_loose_vertices_preserved':835,'request':request,'inputs':inputs,
    'Unity_inventory':{'commit':ref,'path':path,'compressed_blob_sha256':hashlib.sha256(blob).hexdigest()},
    'source_writes':0,'consumer_assignments':0,'files':[]}
assert next(x for x in all_meshes if x['renderer']=='Character_Body_Head')['source_loose_vertices']==835
for p in (OUT,E): (p/'SOURCE_CORNER_IDENTITY_RECEIPT.json').write_text(json.dumps(receipt,indent=2),encoding='utf8')
print(json.dumps({'all21_source_FBX_exact':True,'ambiguities_retained':len(ambiguous),'pairs':pairs,'shape_channels':len(shape_deltas),'out':str(OUT)},indent=2))
