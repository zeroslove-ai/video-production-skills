"""Existing-data-only OFF context contract. No bpy/source load/evaluation."""
import json,hashlib
from pathlib import Path
import numpy as np
LAB=Path(__file__).resolve().parent.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
REC=BASE/'o1-source-fidelity-recovery-r1';NATIVE=BASE/'o1-native-unity-probe-r1';HALF=BASE/'o1-dense-half-expression-r1'
E=LAB/'evidence/o1-source-off-context-audit-r1';E.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inputs=[NATIVE/'metadata/source_expanded_rigs.json',NATIVE/'metadata/source_renderers_bind.json',
    REC/'metadata/neutral_camera_light_color_driver_state.json',REC/'metadata/evaluated_driver_geometry_references.json',
    REC/'metadata/mesh_slot_UV_attributes_shape_deltas.json',REC/'data/neutral.npz',
    REC/'data/manual_morph_peak_geometry.npz',REC/'metadata/MANUAL_MORPH_RECEIPT.json',
    HALF/'DENSE_HALF_SOURCE_RECEIPT.json',HALF/'R4_Existing_DirectMorph_Half_Dense_20261003_R1.npz',
    LAB/'scripts/r4_recovery_manual_morph.py',LAB/'scripts/r4_dense_half_expression_reference.py',
    LAB/'scripts/r4_recovery_source_data.py',LAB/'scripts/r4_o1_native_probe_export.py',
    LAB/'scripts/r4_recovery_deform_layers.py',LAB/'scripts/r4_appearance_adapter.py']
hashes={str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in inputs}
rigs=json.loads(inputs[0].read_text());renderers=json.loads(inputs[1].read_text())
context=json.loads(inputs[2].read_text())['neutral'];neutral=json.loads(inputs[3].read_text())[0]
meshmeta=json.loads(inputs[4].read_text());manual=json.loads(inputs[7].read_text());half=json.loads(inputs[8].read_text())
assert context['frame']==1 and all(v is None for v in context['rig_actions'].values())
assert len(renderers)==len(meshmeta)==21 and sum(len(v['bones']) for v in rigs.values())==137
rows=[];nonidentity=[];cross=[]
for name,rig in rigs.items():
    for i,b in enumerate(rig['bones']):
        ch=b['neutral_pose_channels'];changed=(max(map(abs,ch['location']))>1e-8 or max(abs(v-1) for v in ch['scale'])>1e-8 or
            (max(abs(v-(1 if k==0 else 0)) for k,v in enumerate(ch['quaternion_wxyz']))>1e-8 if ch['rotation_mode']=='QUATERNION' else max(map(abs,ch['euler']))>1e-8))
        d=float(np.max(np.abs(np.array(b['world_rest'])-np.array(b['neutral_evaluated_world']))))
        row={'rig':name,'bone':b['name'],'index':i,'deform':b['deform'],'parent':b['parent'],
            'matrix_file_sha256':hashes[str(inputs[0])]['sha256'],
            'json_pointer':'/'+name+'/bones/'+str(i),
            'rest_fields':['local_rest','armature_rest','world_rest'],
            'OFF_fields':['neutral_pose_channels','neutral_evaluated_armature','neutral_evaluated_world','constraints'],
            'neutral_channels_nonidentity':changed,'rest_vs_evaluated_OFF_max_matrix_delta':d}
        rows.append(row)
        if changed:nonidentity.append({'rig':name,'bone':b['name'],'channels':ch})
        if name in neutral['rig_pose']:
            cross.append(float(np.max(np.abs(np.array(b['neutral_evaluated_world'])-np.array(neutral['rig_pose'][name][b['name']])))))
npz=np.load(inputs[5]);rr=[]
for i,r in enumerate(renderers):
    m=next(v for v in meshmeta if v['renderer']==r['name']);p=npz[r['name']+'_world_position']
    bindings=[{'rig':v['target'],'modifier':v['modifier'],'bone_count':len(v['bone_indices']),
        'inverse_bind_raw_rest_field':'inverse_bind_rest_mesh_to_bone',
        'evaluated_OFF_inverse_field':'inverse_bind_evaluated_neutral_mesh_to_bone',
        'settings':v['settings']} for v in r['armature_bindings']]
    rr.append({'renderer':r['name'],'vertices':len(p),'source_path':r['path'],
        'bind_metadata_pointer':{'input_index':1,'json_pointer':'/'+str(i)},
        'stack_shape_material_pointer':{'input_index':4,'json_pointer':'/'+str(meshmeta.index(m))},
        'matrix_world':r['matrix_world'],'neutral_NPZ_world_array':r['name']+'_world_position',
        'neutral_NPZ_local_array':r['name']+'_local_position',
        'world_AABB_min':p.min(axis=0).tolist(),'world_AABB_max':p.max(axis=0).tolist(),
        'armature_bindings':bindings,'ordered_modifier_names_types':[[v[0],v[1]] for v in r['ordered_modifiers']],
        'world_arrays_already_include_object_scale':True})
assert not manual['source_component_diff'] and not half['source_component_diff']
assert all(sha(p)==hashes[str(p)]['sha256'] for p in inputs)
receipt={'task_id':'YURI_O1_SOURCE_OFF_CONTEXT_AUDIT_R1','method':'Python/NumPy existing frozen metadata/array read only; no source file load or Blender job','inputs':hashes,
    'frozen_recovery_ZIP_sha256':'080352e24adb9db33e76e92d8aca9836aeaf444ed75818c29e2970a32dae47df',
    'frozen_half_ZIP_sha256':'b262bd4d62d83823c5febe9f9c3f2903943123ef02df293542b30c7d35b7cc87',
    'source_SHA256':'a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa',
    'source_OFF_frame':context['frame'],'active_body_Action':context['rig_actions']['Meshy_Fitted_Rig'],
    'rig_Actions':context['rig_actions'],'body_object_world':rigs['Meshy_Fitted_Rig']['object_world'],
    'body_object_scale':rigs['Meshy_Fitted_Rig']['source_scale'],
    'all_137_bone_pointers':rows,'nonidentity_native_pose_channels':nonidentity,'all_21_renderer_contracts':rr,
    'native_vs_recovery_neutral_rig_world_matrix_max_delta':max(cross),'crosschecked_bones':len(cross),
    'faceboard13_pointer':'input_index 0 /AVATAR_FaceBoard/bones; recovery neutral rig_pose omitted FaceBoard but native expanded contains all13',
    'baseline_semantics':'Neutral = source evaluated OFF frame1, Action none, existing poses/constraints/drivers/ShapeKeys/modifiers retained. NOT identity pose and NOT raw rest. Bind raw rest and evaluated OFF inverses are separate fields.',
    'morph_semantics':'Manual zero/half/peak changes only saved existing head input keys then frame_set(1). No body Action/pose reset. Dense half AST-reuses exact setinput/evaluate. Frame1 OFF context retained; muted13 bridge drivers retained. Per-case half/peak rig matrices not independently captured; infer body context from frozen code and unchanged source component snapshots, not new measured matrices.',
    'precision_semantics':'Recovery neutral explicit float64 matrix multiplication -> final float32; manual/dense half matrix buffer float32 multiply -> final float32. Reused-zero observed residual <=1.666000493e-8m; does not explain centimeter discrepancy.',
    'scale_contract':'Compare world meters using each exact evaluated object world matrix once. Frozen world_position arrays already include scale (.535 body rig/object domain); do not rescale them. Unity BakeMesh raw output scale semantics must be declared and checked before its world conversion; preserve original .535 hierarchy, never compensate by changing rig/rest/geometry.',
    'PM_reported_consumer_scale_AB_not_independently_rederived':{'useScale_false':{'max_m':.369968202,'RMS_m':.235387318},'useScale_true':{'max_m':7.321465750500254e-7,'RMS_m':2.9152165e-7},'scope':'Immutable body against same frozen neutral/correspondence, per PM. Raw A/B buffers not present in this worker audit. Isolates reported measurement scale semantics; prior pose mismatch hypothesis not established.'},
    'Unity_API_source':'https://docs.unity3d.com/ScriptReference/SkinnedMeshRenderer.BakeMesh.html',
    'missing_fields_for_independent_consumer_AB':'Consumer A/B BakeMesh vertex buffers, useScale flag, actual renderer localToWorldMatrix/lossyScale, coordinate P/H and correspondence hash. Need consumer receipt, not new source capture.',
    'missing_fields_for_independent_half_pose_assertion':'Per-half/peak evaluated FaceBoard/body world matrices were not captured separately. Existing source OFF contract + generation code available; no new CPU capture justified by isolated37cm scale discrepancy.',
    'input_bytes_unchanged':True,'new_Blender_data_jobs':0,'new_export_render_bake_jobs':0,
    'gates_preserved':['Blender imported rotation FAIL','true DQ/7-weight deformation HOLD','gaze/GN HOLD','material/PBR visual HOLD','no canonical appearance promotion']}
(E/'SOURCE_OFF_CONTEXT_CONTRACT.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps({'bones':len(rows),'renderers':len(rr),'nonidentity':nonidentity,'rig_crosscheck_max':max(cross),'crosschecked_bones':len(cross)},indent=2))
