"""CPU-light existing FBX binary/metadata inspection only. No bpy/source/import.
Run in factory Blender for io_scene_fbx.parse_fbx dependency; no scene changes.
"""
import json,gzip,hashlib,sys,collections
from pathlib import Path
import numpy as np
from io_scene_fbx.parse_fbx import parse
LAB=Path(__file__).resolve().parent.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
N=BASE/'o1-native-unity-probe-r1';B=BASE/'o1-original-bind-serialization-r1';R=BASE/'o1-source-fidelity-recovery-r1'
E=LAB/'evidence/o1-all-bind-and-weight-diagnostic-r1';OUT=BASE/'o1-all-bind-and-weight-diagnostic-r1'
E.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf8'))
def write(n,v):
    for p in (E/n,OUT/n):p.write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf8')
inputs=[N/'reference/source_original_vertex_weights.json.gz',N/'metadata/source_expanded_rigs.json',
    N/'metadata/source_renderers_bind.json',B/'metadata/imported_renderer_bind.json',B/'metadata/EXACT_BIND_WIRE_RECEIPT.json',
    B/'YURI_O1_R4_NATIVE_CARRIER_20261003_R1.fbx',B/'YURI_O1_R4_NATIVE_ANIMATION_ONLY_20261003_R1.fbx',
    R/'metadata/mesh_slot_UV_attributes_shape_deltas.json',R/'metadata/neutral_camera_light_color_driver_state.json',
    N/'metadata/skin_weight_roundtrip_comparison.json',
    Path(r'C:/Program Files/Blender Foundation/Blender 5.2/5.2/scripts/addons_core/io_scene_fbx/export_fbx_bin.py'),
    Path(r'C:/Users/JAEWAN/projects/yuri-root-pm-r1/docs/evidence/root-pm-o1/LAPTOP_ORIGINAL_BIND_bind-rest-summary.json')]
hashes={str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in inputs}
with gzip.open(inputs[0],'rt',encoding='utf8') as f:weights=json.load(f)
rigs=load(inputs[1]);renderers=load(inputs[2]);imported={r['name']:r for r in load(inputs[3])};wire=load(inputs[4]);meta=load(inputs[7])
bodyname='Meshy_Body_NeutralCovered';w=weights[bodyname];groups=w['groups'];bone_map={b['name']:b for b in rigs['Meshy_Fitted_Rig']['bones']}
identity=[{'group_index':i,'group_name':n,'domain':'BONE' if n in bone_map else 'PROCEDURAL_MASK',
    'original_rig':'Meshy_Fitted_Rig' if n in bone_map else None,'bone_index':bone_map[n]['index'] if n in bone_map else None,
    'bone_path':bone_map[n]['path'] if n in bone_map else None,'bone_deform':bone_map[n]['deform'] if n in bone_map else None} for i,n in enumerate(groups)]
offset=[0];gid=[];value=[];skin_count=[];raw_count=[];seventh=[];eighth=[];sums=[];examples=[]
for vi,row in enumerate(w['influences']):
    for g,v in row:gid.append(g);value.append(v)
    offset.append(len(gid));skin=[(g,v) for g,v in row if v>0 and groups[g] in bone_map]
    skin_count.append(len(skin));raw_count.append(sum(v>0 for g,v in row));sums.append(sum(v for g,v in skin))
    ordered=sorted(skin,key=lambda x:x[1],reverse=True)
    if len(skin)>=7:
        seventh.append(ordered[6][1]);examples.append({'vertex':vi,'bone_positive_count':len(skin),'raw_source_row':row,
            'bone_rows':[{'group_index':g,'bone':groups[g],'weight':v} for g,v in skin]})
    if len(skin)>=8:eighth.append(ordered[7][1])
normalized=[]
for row,total in zip(w['influences'],sums):
    normalized.extend(v/total if v>0 and groups[g] in bone_map and total>0 else 0. for g,v in row)
npz=OUT/'R4_Body_All_Original_Group_Weights_CSR.npz'
np.savez_compressed(npz,vertex_offsets=np.array(offset,np.int32),group_index=np.array(gid,np.int32),weight=np.array(value,np.float32),
    group_is_bone=np.array([n in bone_map for n in groups],np.uint8),positive_bone_count=np.array(skin_count,np.uint8),
    positive_all_group_count=np.array(raw_count,np.uint8),vertices_with_at_least7_bone_weights=np.flatnonzero(np.array(skin_count)>=7).astype(np.int32),
    derived_bone_weight_sum=np.array(sums,np.float64),derived_normalized_bone_weight=np.array(normalized,np.float64))
assert np.array_equal(np.array(value,np.float32).astype(np.float64),np.array(value,np.float64))
# Frozen seven-plus rows are data, not a Git-expanded bulk receipt.
rowsfile=OUT/'R4_Body_Seven_Plus_Bone_Rows.json.gz'
with gzip.open(rowsfile,'wt',encoding='utf8') as f:json.dump(examples,f,separators=(',',':'))
def normrows(m):
    u,_,v=np.linalg.svd(m[:3,:3]);fix=np.diag([1,1,np.linalg.det(u@v)]);return u@fix@v
def delta(a,b):
    a=np.array(a,dtype=np.float64);b=np.array(b,dtype=np.float64);r=normrows(a).T@normrows(b)
    skew=np.array([r[2,1]-r[1,2],r[0,2]-r[2,0],r[1,0]-r[0,1]])/2
    return {'position_m':float(np.linalg.norm(a[:3,3]-b[:3,3])),
        'rotation_polar_matrix_deg':float(np.degrees(np.arctan2(np.linalg.norm(skew),(np.trace(r)-1)/2))),
        'max_matrix_element_delta':float(np.max(np.abs(a-b)))}
bindrows=[]
for renderer in renderers:
    target=imported[renderer['name']]
    for binding in renderer['armature_bindings']:
        ib=next(v for v in target['armature_bindings'] if v['target']==binding['target'])
        ibones={v['name']:v for v in ib['bone_indices']};native={v['name']:v for v in rigs[binding['target']]['bones']}
        for bone in binding['bone_indices']:
            n=bone['name'];recovered=np.array(target['matrix_world'])@np.linalg.inv(np.array(ibones[n]['inverse_bind_rest_mesh_to_bone']))
            source=np.array(native[n]['world_rest']);wr=next(v for v in wire['bones'] if v['rig']==binding['target'] and v['bone']==n)
            names=weights[renderer['name']]['groups'];positive=sum(any(names[g]==n and v>0 for g,v in row) for row in weights[renderer['name']]['influences'])
            bindrows.append({'renderer':renderer['name'],'rig':binding['target'],'bone':n,'bone_index':bone['index'],
                'source_modifier':binding['modifier'],'import_binding_selection':'same target rig; serialized/imported carrier has one Armature skin, not source layered modifiers',
                'positive_source_vertices':positive,'source_raw_rest_vs_Blender_import_recovered_bind':delta(source,recovered),
                'source_raw_rest_vs_source_evaluated_OFF':delta(source,native[n]['neutral_evaluated_world']),
                'source_inverse_bind_rest':bone['inverse_bind_rest_mesh_to_bone'],'source_inverse_evaluated_OFF':bone['inverse_bind_evaluated_neutral_mesh_to_bone'],
                'Blender_import_inverse_bind_rest':ibones[n]['inverse_bind_rest_mesh_to_bone'],
                'wire_original_model_equals_animation_exact':wr['model_effective_bind_equals_animation_Pose_exact'],
                'wire_converted_source_raw_rest_matrix_delta':wr['converted_source_raw_rest_max_matrix_element_delta']})
write('ALL_RENDERER_BIND_ROWS.json',{'rows':bindrows,'count':len(bindrows),'source_bones':137,
    'zero_positive_weight_rows_included':True,'thresholds_unchanged':True,'scope':'Existing Blender importer reconstructed bind diagnostics, not actual Unity matrices.'})
# Actual frozen FBX cluster wire weights and bind matrices, no importer/exporter.
root,_=parse(str(inputs[5]));sections={v.id:v for v in root.elems};objects={v.props[0]:v for v in sections[b'Objects'].elems}
connections=[tuple(v.props) for v in sections[b'Connections'].elems if v.props[0]==b'OO']
def named(uid):return objects[uid].props[1].decode(errors='replace').split('\x00')[0]
def childfield(element,name,default=None):return next((v.props[0] for v in element.elems if v.id==name),default)
meshes={uid:named(uid) for uid,o in objects.items() if o.id==b'Model' and o.props[-1]==b'Mesh'}
geometries={child:meshes[parent] for _,child,parent,*_ in connections if child in objects and objects[child].id==b'Geometry' and parent in meshes}
skins={child:parent for _,child,parent,*_ in connections if child in objects and objects[child].id==b'Deformer' and objects[child].props[-1]==b'Skin' and parent in geometries}
cluster_bone={parent:child for _,child,parent,*_ in connections if child in objects and objects[child].id==b'Model' and parent in objects and objects[parent].id==b'Deformer' and objects[parent].props[-1]==b'Cluster'}
wireweights={};wirebind=[]
for _,cluster,skin,*_ in connections:
    if skin not in skins or cluster not in cluster_bone:continue
    geometry=skins[skin];renderer=geometries[geometry];bone=named(cluster_bone[cluster]);elem=objects[cluster]
    indices=list(childfield(elem,b'Indexes',[]));vals=list(childfield(elem,b'Weights',[]));assert len(indices)==len(vals)
    wirebind.append({'renderer':renderer,'bone':bone,'cluster_uid':cluster,'entries':len(indices),'positive_entries':sum(v>0 for v in vals),
        'Transform_column_major':list(childfield(elem,b'Transform')),'TransformLink_column_major':list(childfield(elem,b'TransformLink'))})
    if renderer==bodyname:
        for vi,v in zip(indices,vals):
            key=(int(vi),bone)
            if key in wireweights:assert wireweights[key]==v
            wireweights[key]=v
expected={(vi,groups[g]):v for vi,row in enumerate(w['influences']) for g,v in row if groups[g] in bone_map and v>0}
differences=[{'vertex':vi,'bone':b,'source':v,'FBX':wireweights.get((vi,b),0.)} for (vi,b),v in expected.items() if wireweights.get((vi,b),0.)!=v]
extra=[(vi,b) for vi,b in wireweights if wireweights[(vi,b)]>0 and (vi,b) not in expected]
headcase=next(v for v in bindrows if v['renderer']=='Character_Body_Head' and v['bone']=='J_Bip_R_Middle3')
headwire=[v for v in wirebind if v['renderer']=='Character_Body_Head' and v['bone']=='J_Bip_R_Middle3']
consumer=load(inputs[11]);P=np.array(consumer['basis']['P'],dtype=np.float64);H=np.array(consumer['basis']['H'],dtype=np.float64)
hb=next(b for b in rigs['Armature']['bones'] if b['name']=='J_Bip_R_Middle3')
case_expected={'basis_source_pointer':str(inputs[11]),'P':P.tolist(),'H':H.tolist(),
    'expected_Unity_bone_world_raw_rest':(P@np.array(hb['world_rest'])@H).tolist(),
    'expected_Unity_bone_world_evaluated_OFF':(P@np.array(hb['neutral_evaluated_world'])@H).tolist(),
    'expected_Unity_renderer_world_source_OFF':(P@np.array(next(r for r in renderers if r['name']=='Character_Body_Head')['matrix_world'])@H).tolist(),
    'expected_Unity_inverse_raw_rest_bind_from_same_source_frames':(H@np.array(headcase['source_inverse_bind_rest'])@H).tolist(),
    'meaning':'Source-derived expected matrices under actual consumer declared basis. Actual consumer bindpose row not available; does not fit or alter bone/rest/renderer to observed error.'}
write('R_MIDDLE3_HEAD_CASE.json',{'source_and_Blender_import_case':headcase,'actual_frozen_FBX_clusters':headwire,
    'consumer_expected_source_matrices':case_expected,
    'PM_reported_Unity_bind_error':{'position_m':.010416765,'rotation_deg':.675783,'independently_rederived':False},
    'verdict':'Source/rest/OFF and actual wire/Blender reconstructed bind are distinct domains. This source-side result does not silently waive zero-weight row. Need actual Unity bindpose and matched renderer/bone matrices/P/H to explain consumer10.416765mm/.675783deg; no consumer matrices supplied here.'})
bodymeta=next(v for v in meta if v['renderer']==bodyname)
receipt={'task_id':'YURI_O1_ALL_BIND_AND_7_INFLUENCE_SOURCE_DIAGNOSTIC_R1','inputs':hashes,
    'source_preservation':'No source .blend load/save, no scene mutation/import, no new render/bake/export. Existing binary FBX parsed read-only; frozen weights and metadata only.',
    'source_component_mutations':0,'inputs_unchanged':all(sha(p)==hashes[str(p)]['sha256'] for p in inputs),
    'group_identity':identity,'vertices':len(w['influences']),'raw_all_positive_group_max':max(raw_count),
    'strict_positive_bone_weight_count_histogram':dict(sorted(collections.Counter(skin_count).items())),
    'diagnostic_threshold_counts_NOT_pruning_policy':{str(t):max(sum(v>t and groups[g] in bone_map for g,v in row) for row in w['influences']) for t in (0,1e-30,1e-20,1e-12,1e-8,1e-6,1e-4)},
    'seventh_weight_max':max(seventh),'eighth_weight_max':max(eighth),'bone_sum_min':min(sums),'bone_sum_max':max(sums),
    'source_to_FBX_body_raw_bone_weights':{'source_positive_entries':len(expected),'wire_entries':len(wireweights),'differences':differences,'extra_positive_entries':extra,
        'all_source_positive_bone_weights_exact':not differences and not extra},
    'prior_native_Blender_import_weight_receipt':load(inputs[9]),
    'body_modifier_order_settings':bodymeta['modifiers'],
    'normalization_contract':'Raw source weights unchanged. Bone groups are matched by original rig/name/deform identity; seven procedural masks are not bone normalization contributions. Blender armature LBS uses accumulated bone contribution normalization; DQ accumulates weighted transform and normalizes DQ. Secondary LBS mask and subsequent corrective/smooth masks/order are separate. Official current upstream code explains semantics; not asserted binary-identical to installed5.2.1 C++ without matched-build code.',
    'normalization_primary_source':'https://github.com/blender/blender/blob/main/source/blender/blenkernel/intern/armature_deform.cc',
    'files':[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in (npz,rowsfile)],
    'CSR_derivation_policy':'Raw original group_index/weight entries including zero preserved exactly. derived_bone_weight_sum/derived_normalized_bone_weight float64 arrays are independent bone-only normalization diagnostics, not edited source or substitute for DQ/corrective stack. Mask CSR entries derived normalized bone weight=0 but raw masks fully preserved.',
    'all_bind_rows_included':len(bindrows),'all137_original_wire_contract_retained':True,
    'gates':'No influence-count tolerance/zero-row waiver. Original Blender source/import rotation FAIL unchanged; actual Unity all-bind row and DQ/weight restoration remain consumer gate.',
    'missing_consumer_case_fields':['actual head renderer bindpose row matched to J_Bip_R_Middle3 identity/index','actual renderer localToWorldMatrix','actual bone raw-rest and evaluated OFF matrices','source-to-Unity P/H conversion and scale compensation used in bind comparison'],
    'next_useful_source_task':'Consumer all-bind exact case receipt comparison; no redundant source extraction needed. Fullstack276deformation and evaluated gaze corner authorities already frozen.'}
assert receipt['inputs_unchanged'];write('ALL_BIND_AND_WEIGHT_DIAGNOSTIC_RECEIPT.json',receipt)
print('DIAGNOSTIC_COMPLETE',headcase['source_raw_rest_vs_Blender_import_recovered_bind'],len(headwire),max(skin_count),len(differences),len(extra),flush=True)
