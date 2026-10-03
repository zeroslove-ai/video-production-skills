"""Existing source/actual Unity matrices -> domain-correct transport contract.
NumPy only; no Unity/source/FBX writes, no fitting bone/rest or pose matrices.
"""
import json,hashlib
from pathlib import Path
import numpy as np
LAB=Path(__file__).resolve().parent.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
N=BASE/'o1-native-unity-probe-r1';E=LAB/'evidence/o1-bind-transport-contract-r1';OUT=BASE/'o1-bind-transport-contract-r1'
E.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
PM=Path(r'C:/Users/JAEWAN/projects/yuri-root-pm-r1/docs/evidence/root-pm-o1')
inputs=[N/'metadata/source_expanded_rigs.json',N/'metadata/source_renderers_bind.json',
    PM/'PM_UNITY_R_MIDDLE3_RAW_BIND_CASE_R1.json',PM/'LAPTOP_ORIGINAL_BIND_bind-rest-summary.json',
    LAB/'evidence/o1-all-bind-and-weight-diagnostic-r1/ALL_BIND_AND_WEIGHT_DIAGNOSTIC_RECEIPT.json']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf8'))
def write(n,v):
    for p in (E/n,OUT/n):p.write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf8')
hashes={str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in inputs}
rigs=load(inputs[0]);renderers=load(inputs[1]);case=load(inputs[2]);basis=load(inputs[3])['basis']
P=np.array(basis['P'],dtype=np.float64);H=np.array(basis['H'],dtype=np.float64)
def polar(m):
    u,_,v=np.linalg.svd(m[:3,:3]);return u@np.diag([1,1,np.linalg.det(u@v)])@v
def delta(a,b):
    r=polar(a).T@polar(b);skew=np.array([r[2,1]-r[1,2],r[0,2]-r[2,0],r[1,0]-r[0,1]])/2
    return {'translation_vector_distance':float(np.linalg.norm(a[:3,3]-b[:3,3])),
        'rotation_polar_deg':float(np.degrees(np.arctan2(np.linalg.norm(skew),(np.trace(r)-1)/2))),
        'max_matrix_element_delta':float(np.max(np.abs(a-b)))}
identities=[];buffers={k:[] for k in ['source_inverse_raw_rest_bind','source_inverse_evaluated_OFF_bind',
    'source_mesh_world','expected_Unity_bone_world_raw_rest','expected_Unity_bone_world_evaluated_OFF',
    'expected_Unity_mesh_world_IF_local_geometry_H','expected_Unity_bind_IF_local_geometry_H']}
source_inverse_recompute_max=0
for ri,r in enumerate(renderers):
    for mi,mod in enumerate(r['armature_bindings']):
        rig=rigs[mod['target']];native={b['name']:b for b in rig['bones']}
        for bi,b in enumerate(mod['bone_indices']):
            n=native[b['name']];W=np.array(n['world_rest']);M=np.array(r['matrix_world']);B=np.array(b['inverse_bind_rest_mesh_to_bone'])
            source_inverse_recompute_max=max(source_inverse_recompute_max,float(np.max(np.abs(np.linalg.inv(W)@M-B))))
            row=len(identities);identities.append({'row':row,'renderer':r['name'],'source_renderer_path':r['path'],
                'source_modifier':mod['modifier'],'rig':mod['target'],'bone':b['name'],'source_bone_index':b['index'],
                'source_bone_path':n['path'],'source_bind_pointer':'/'+str(ri)+'/armature_bindings/'+str(mi)+'/bone_indices/'+str(bi)})
            values={'source_inverse_raw_rest_bind':B,'source_inverse_evaluated_OFF_bind':np.array(b['inverse_bind_evaluated_neutral_mesh_to_bone']),
                'source_mesh_world':M,'expected_Unity_bone_world_raw_rest':P@W@H,
                'expected_Unity_bone_world_evaluated_OFF':P@np.array(n['neutral_evaluated_world'])@H,
                'expected_Unity_mesh_world_IF_local_geometry_H':P@M@H,
                'expected_Unity_bind_IF_local_geometry_H':H@B@H}
            for k,v in values.items():buffers[k].append(v)
assert len(identities)==1207
p=OUT/'R4_Original_All1207_Bind_Transport_Source_Matrices.npz'
np.savez_compressed(p,**{k:np.array(v,dtype=np.float64) for k,v in buffers.items()})
index=next(v['row'] for v in identities if v['renderer']=='Character_Body_Head' and v['bone']=='J_Bip_R_Middle3')
W=np.array(buffers['expected_Unity_bone_world_raw_rest'][index]);M=np.array(case['Unity_renderer_world']);B=np.array(case['Unity_bindpose']);current=np.array(case['Unity_current_bone_world'])
recovered=M@np.linalg.inv(B);expected_source_bind=np.array(buffers['expected_Unity_bind_IF_local_geometry_H'][index])
# Actual-renderer-frame target for consumer test ONLY; not an applied mesh edit.
B_actual_frame=np.linalg.inv(W)@M
corrected_recovered=M@np.linalg.inv(B_actual_frame)
measure={'inverse_bind_translation_domain_NOT_world_position':delta(B,expected_source_bind),
    'recovered_world_bind_bone_vs_source_raw_rest':delta(recovered,W),
    'current_Unity_world_bone_vs_source_raw_rest':delta(current,W),
    'actual_renderer_vs_source_declared_geometry_basis':delta(M,np.array(buffers['expected_Unity_mesh_world_IF_local_geometry_H'][index])),
    'offline_actual_renderer_frame_transport_recovered_world':delta(corrected_recovered,W),
    'offline_B_actual_frame_vs_source_H_bind_H':delta(B_actual_frame,expected_source_bind)}
source_closure=[]
for i in range(len(identities)):
    recovered_source=np.array(buffers['expected_Unity_mesh_world_IF_local_geometry_H'][i])@np.linalg.inv(np.array(buffers['expected_Unity_bind_IF_local_geometry_H'][i]))
    source_closure.append(delta(recovered_source,np.array(buffers['expected_Unity_bone_world_raw_rest'][i])))
with np.load(p,allow_pickle=False) as check:
    assert len(check.files)==7
    for k,values in buffers.items():
        assert check[k].shape==(1207,4,4) and np.isfinite(check[k]).all() and np.array_equal(check[k],np.array(values))
correction={'task_id':'YURI_O1_R_MIDDLE3_BIND_DOMAIN_CORRECTION_R1','inputs':hashes,'measurements':measure,
    'original_Unity_bindpose':B.tolist(),'original_Unity_renderer_world':M.tolist(),'source_expected_raw_rest_Unity_world':W.tolist(),
    'proposed_bind_for_THIS_actual_renderer_frame':B_actual_frame.tolist(),'source_H_inverse_raw_rest_bind_H':expected_source_bind.tolist(),
    'reported_domain_correction':'10.416765mm is inverse-bind translation-coordinate discrepancy, not reconstructed world bone displacement. World recovered bind residual ~0.186um but ~0.675783deg rotation FAIL. Current Unity world bone rest comparison passes separately.',
    'offline_transport_scope':'Computing inverse(W_source_expected)@M_actual algebraically restores recovered raw bind world only; actual geometry basis/correspondence and all rows/deformation must be validated before applying to isolated cloned Mesh. No consumer write or runtime PASS.',
    'causal_limit':'Actual imported bindpose rotation differs despite actual bone world pose PASS and exact source FBX bind transport. Empty Cluster is observed; importer zero-cluster causality not proven without code/data evidence.',
    'rotation_threshold_deg_unchanged':.001,'original_bind_rotation_PASS':measure['recovered_world_bind_bone_vs_source_raw_rest']['rotation_polar_deg']<.001}
write('R_MIDDLE3_DOMAIN_CORRECTION.json',correction)
manifest={'task_id':'YURI_O1_EXACT_BIND_TRANSPORT_SOURCE_CONTRACT_R1','inputs':hashes,'rows':1207,'renderers':21,'original_rig_bones':137,
    'all_row_identity':identities,'files':[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)}],
    'source_float64_reinversion_vs_original_stored_inverse_max_element_delta':source_inverse_recompute_max,
    'source_only_declared_basis_closure_NOT_actual_Unity_allrow_PASS':{
        'max_recovered_world_position_m':max(v['translation_vector_distance'] for v in source_closure),
        'max_recovered_world_rotation_deg':max(v['rotation_polar_deg'] for v in source_closure),
        'max_matrix_element':max(v['max_matrix_element_delta'] for v in source_closure)},
    'matrix_arrays':{k:{'shape':[1207,4,4],'dtype':'float64','finite_and_readback_exact':True} for k in buffers},
    'matrix_precision':'Original native stored float32 matrix values promoted to float64; original stored source inverses retained, not recomputed/rewritten. Derived target matrices float64. No polar-normalizing bind scale/shear.',
    'transport_derivation':'Let local exported mesh geometry v_u=K v_s; target bone world W_u=G P W_s H_b. For rest geometry M_u K=G P M_s, source B_s=inverse(W_s) M_s. Then B_u=H_b B_s inverse(K). H B_s H only if K=H. Inverse(W_u) M_u uses ACTUAL validated renderer frame. G is declared common instance transform, never per-bone fitted correction.',
    'renderer_basis_gate':'For every renderer establish exact local geometry K using source/import split-vertex correspondence and original topology/weights. Validate actual M_u K versus G P M_s. Do not infer K solely from a matching bone pose or one position. If mismatch, reject that transport proposal rather than changing bone/rest/geometry to fit.',
    'consumer_operation_contract':'Apply only after validation on isolated cloned Mesh bindposes with original bone identity/order and geometry/material/ShapeKey/weights unchanged. Source/master and immutable imported FBX Mesh remain unchanged. Body two modifier binding rows remain distinct stage identities; duplicated rig rows do not create a second Unity skin or substitute for original DQ/maskedLBS/corrective stack.',
    'consumer_acceptance':'Original raw-rest world recovered from actual renderer@inverse(proposed_bind) must meet unchanged gates for ALL1207source binding rows incl zero-weight. Also retain current all137rest/pose checks and complete276/384frame fullstack position/cornernormal/reference comparison. Algebraic bind closure alone not deformation/appearance PASS.',
    'source_preservation':'Existing frozen arrays/PM actual matrices read only. No Blender/source/FBX load/save/export or Unity writes. Source component mutations0; all input SHA unchanged.',
    'prior_checkpoint':'ff5806fbf1aff364cb1ebe05f9714ee505f4394c','gates_preserved':['Unity R_Middle3 bind rotation FAIL','strict Blender source/import rotation FAIL','all-bind incl zero support','full deformation/material/gaze/F2/Player separate gates'],
    'data_role':'Source-owned transport proposal; Laptop sole Unity writer. Actual current isolated clone matrices/all1207row closure still required.'}
assert all(sha(v)==hashes[str(v)]['sha256'] for v in inputs)
write('EXACT_BIND_TRANSPORT_SOURCE_CONTRACT.json',manifest)
print('BIND_DOMAIN_CORRECTION',json.dumps(measure),flush=True)
