"""CPU-only contract from frozen data and pinned upstream source; no bpy."""
import gzip, hashlib, json
from pathlib import Path
import numpy as np
LAB=Path(__file__).resolve().parent.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
R=BASE/'o1-source-fidelity-recovery-r1'; N=BASE/'o1-native-unity-probe-r1'
OUT=BASE/'o1-body-modifier-source-contract-r1'; E=LAB/'evidence/o1-body-modifier-source-contract-r1'
E.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)
assert not (OUT/'BODY_MODIFIER_SOURCE_CONTRACT.json').exists(), 'Preserve frozen contract'
inputs={}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def record(p):
    inputs[str(p)]={'sha256':sha(p),'bytes':p.stat().st_size}; return p
def load(p): return json.loads(record(p).read_text(encoding='utf8'))
def write(n,v):
    for p in (OUT,E): (p/n).write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf8')
body=next(x for x in load(R/'metadata/mesh_slot_UV_attributes_shape_deltas.json') if x['renderer']=='Meshy_Body_NeutralCovered')
bind=next(x for x in load(N/'metadata/source_renderers_bind.json') if x['name']==body['renderer'])
rig=load(N/'metadata/source_expanded_rigs.json')['Meshy_Fitted_Rig']
weights=json.loads(gzip.decompress(record(N/'reference/source_original_vertex_weights.json.gz').read_bytes()))[body['renderer']]
csr=np.load(record(BASE/'o1-all-bind-and-weight-diagnostic-r1/R4_Body_All_Original_Group_Weights_CSR.npz'),allow_pickle=False)
original=np.load(record(R/'data/Meshy_Body_NeutralCovered_original_mesh.npz'),allow_pickle=False)
types=[m['type'] for m in body['modifiers']]
assert types==['ARMATURE','ARMATURE','CORRECTIVE_SMOOTH','SMOOTH','SMOOTH','SMOOTH','SMOOTH']
assert body['modifiers'][2]['settings']['rest_source']=='ORCO' and not body['modifiers'][2]['settings']['is_bind']
count=len(original['positions']);assert count==63561
groups=weights['groups'];nonbone=[i for i,v in enumerate(csr['group_is_bone']) if not v]
assert len(nonbone)==7
row_ids=np.repeat(np.arange(count,dtype=np.int32),np.diff(csr['vertex_offsets']))
mask=np.zeros((count,len(nonbone)),np.float32)
for mi,gi in enumerate(nonbone):
    used=csr['group_index']==gi; mask[row_ids[used],mi]=csr['weight'][used]
    # Independent literal original JSON row check, no thresholds or normalization.
    expected=np.array([dict(v).get(gi,0.) for v in weights['influences']],np.float32)
    assert np.array_equal(mask[:,mi],expected),groups[gi]
corner_edge_name=next(a['fields'][0]['array'] for a in body['attributes'] if a['name']=='.corner_edge')
ce=original[corner_edge_name];edges=original['edge_vertex_indices'];loops=original['loop_vertex_indices']
assert len(ce)==len(loops)==254602
edge_faces=np.bincount(ce,minlength=len(edges)).astype(np.int32)
boundary=np.zeros(count,bool);boundary[edges[edge_faces==1].reshape(-1)]=True
degree=np.bincount(edges.reshape(-1),minlength=count).astype(np.int32)
corrective_index=nonbone.index(groups.index('R3_Joint_CorrectiveSmooth'))
effective_mask=mask[:,corrective_index].copy();effective_mask[boundary]=0
arrays={'source_vertex_id':np.arange(count,dtype=np.int32),'ORCO_rest_local_position':original['positions'],
    'source_edge_vertices':edges,'source_loop_vertex':loops,'source_corner_edge':ce,
    'source_polygon_start':original['polygon_loop_start'],'source_polygon_size':original['polygon_loop_total'],
    'raw_nonbone_group_weights':mask,'edge_polygon_corner_use_count':edge_faces,
    'corrective_boundary_vertex':boundary,'derived_corrective_effective_mask':effective_mask,'edge_degree':degree,
    'body_object_world':np.array(bind['matrix_world'],np.float64),'rig_object_world':np.array(rig['object_world'],np.float64),
    'primary_raw_inverse_bind':np.array([x['inverse_bind_rest_mesh_to_bone'] for x in bind['armature_bindings'][0]['bone_indices']],np.float64),
    'secondary_raw_inverse_bind':np.array([x['inverse_bind_rest_mesh_to_bone'] for x in bind['armature_bindings'][1]['bone_indices']],np.float64)}
assert np.array_equal(arrays['primary_raw_inverse_bind'],arrays['secondary_raw_inverse_bind'])
for a in arrays.values(): assert np.isfinite(a).all()
file=OUT/'R4_Body_Original_Modifier_Support.npz'; assert not file.exists()
np.savez_compressed(file,**arrays)
with np.load(file,allow_pickle=False) as saved:
    for key,a in arrays.items(): assert np.array_equal(saved[key],a),key
reference=load(R/'metadata/evaluated_driver_geometry_references.json')
cases=[{'tag':x['tag'],'driver_outputs':[d for d in x['driver_outputs'] if d['owner']==body['renderer']],
    'modifier_evaluated_settings':x['modifier_evaluated_settings'][body['renderer']]} for x in reference if x['tag']=='neutral' or x['tag'].startswith('motion_')]
ablation=load(R/'metadata/DEFORMATION_LAYER_RECEIPT.json')
full=load(BASE/'o1-full-body-deformation-reference-r1/FULL_BODY_DEFORMATION_MANIFEST.json')
strong6=next(x for x in full['chunks'] if x['clip']=='YRA_R4_Struggle_Strong_Loop' and 6 in x['source_frames'])
record(BASE/'o1-full-body-deformation-reference-r1'/strong6['path'])
coverage=[]
for j,gi in enumerate(nonbone):
    ids=np.flatnonzero(mask[:,j]>0)
    coverage.append({'group_index':gi,'name':groups[gi],'array_column':j,'literal_positive_vertices':len(ids),
        'min':float(mask[:,j].min()),'max':float(mask[:,j].max()),
        'used_by':[m['name'] for m in body['modifiers'] if m['settings'].get('vertex_group')==groups[gi]]})
params={'renderer':body['renderer'],'ordered_modifiers':body['modifiers'],'original_driver_definitions':body['object_drivers'],
    'mask_columns':coverage,'primary_and_secondary_bind_rows':bind['armature_bindings'],
    'driver_output_cases':cases,'Strong_1_49_original_ablation_metrics':ablation['layer_metrics']}
write('BODY_MODIFIER_PARAMETERS_AND_DRIVERS.json',params)
upstream=[]
for p in sorted((OUT/'upstream').iterdir()):
    suffix={'MOD_util.cc':'source/blender/modifiers/intern/MOD_util.cc','armature_deform.cc':'source/blender/blenkernel/intern/armature_deform.cc','COPYING':'COPYING'}.get(p.name,'source/blender/modifiers/intern/'+p.name)
    upstream.append({'path':'upstream/'+p.name,'sha256':sha(p),'bytes':p.stat().st_size,
        'url':'https://raw.githubusercontent.com/blender/blender/9e2066aef7ef/'+suffix})
manifest={'task_id':'YURI_O1_BODY_MODIFIER_SOURCE_CONTRACT_R1','status':'DONE_SOURCE_SUPPORT_RUNTIME_GATE_PENDING',
    'lineage':'3b37f357 native original-bind carrier is distinct from earlier rebuilt GameRig; no reset/adapter abandonment from duplicate material-slot serialization.',
    'vertices':count,'source_loops':len(loops),'ordered_modifier_types':types,
    'SurfaceDeform_present':False,'CorrectiveSmooth_binding':'ORCO original mesh positions; is_bind false; no SurfaceDeform cage or bind_coords prerequisite',
    'installed_Blender_build_hash_and_upstream_ref':'9e2066aef7ef',
    'source_nonbone_mask_groups':coverage,'boundary_vertices':int(boundary.sum()),
    'unused_mask_policy':'Joint_Smoothing_Mask retained, not used by any of the current seven modifiers; do not add a stage or fold it into bone normalization.',
    'driver_channel_domain':'SINGLE_PROP raw pose.bones rotation_quaternion components, wxyz, before constraint/world evaluation. Evaluated parent-local TRS is not automatically equivalent.',
    'driver_evidence_limit':'Existing exact outputs/settings cover neutral + nine selected motion cases. No all-frame raw property/factor capture. Do not call world/local matrix-derived factors source-exact without proof.',
    'Strong_frame6_reference':{'root':str(BASE/'o1-full-body-deformation-reference-r1'),**strong6},
    'Strong_frame6_prototype':'PM reports 1.77mm residual; not runtime PASS and not proven single-stage cause. Compare original ablations and exact full-stack reference.',
    'ablation_pointer':{'root':str(R),'path':ablation['array_file'],'sha256':ablation['sha256'],'source_frames':[1,49]},
    'missing_staged_evidence':'Existing ablation combines all five surface stages; no individual-stage Strong frame6 capture. Under no-new-Blender-load scope, retain this limitation.',
    'files':[{'path':file.name,'sha256':sha(file),'bytes':file.stat().st_size},*upstream],
    'inputs':inputs,'arrays':{k:{'shape':list(v.shape),'dtype':str(v.dtype)} for k,v in arrays.items()},
    'all_array_readback_exact_and_finite':True,'source_scene_loads':0,'source_binary_writes':0,'product_repo_writes':0}
write('BODY_MODIFIER_SOURCE_CONTRACT.json',manifest)
print(json.dumps({'vertices':count,'boundary_vertices':int(boundary.sum()),'support_bytes':file.stat().st_size,
    'driver_cases':len(cases),'mask_groups':coverage},indent=2))
