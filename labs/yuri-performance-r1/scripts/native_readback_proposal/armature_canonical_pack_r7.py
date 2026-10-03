"""Canonical lossless native-event packing with explicit sparse NOT_COMPUTED fields.
No masked slot is filled with invented quaternion/identity/zero evidence.
"""
import hashlib,json,struct,zipfile
from pathlib import Path
from armature_canonical_validate_r7 import validate,require,VERTICES,fbytes,numbers
from armature_trace_unpack_r1 import npy

def pack(events,request,bones,path,classification,custody=None):
    result=validate(events,request,bones)
    require(classification in ('NATIVE_CAPTURE_CONTEXT_VALIDATED_NUMERIC_EQUIVALENCE_PENDING','SYNTHETIC_FIXTURE_NOT_NATIVE'),'explicit custody classification required')
    if classification.startswith('NATIVE_'):
        require(isinstance(custody,dict),'actual native custody required; no caller label alone')
        for name in ('compiled_custody','owned_capture_receipt','source_restore_receipt'):
            entry=custody[name];require(Path(entry['path']).is_file() and hashlib.sha256(Path(entry['path']).read_bytes()).hexdigest()==entry['sha256'],'native custody file missing/changed '+name)
        restore=json.loads(Path(custody['source_restore_receipt']['path']).read_bytes())
        require(restore['source_action_restore']=='VERIFIED' and restore['joined_workers'] is True,'native restore/join proof required')
        require(restore['original_full_recipe']['CSR_entries']==304799,'full live CSR proof required')
        from armature_canonical_validate_r7 import load_events
        logs=[]
        for entry in custody['raw_logs']:
            require(hashlib.sha256(Path(entry['path']).read_bytes()).hexdigest()==entry['sha256'],'native raw log changed');logs.append(Path(entry['path']))
        require(load_events(logs)==events,'canonical values not from recorded native logs')
    path=Path(path);require(not path.exists() and not path.with_suffix('.manifest.json').exists(),'immutable new output required')
    arrays={};metadata={}
    def add(name,dtype,shape,payload,stage,logical_shape=None):
        require(len(payload)==4*__import__('math').prod(shape),'canonical byte shape mismatch '+name)
        arrays[name]=npy(dtype,tuple(shape),payload)
        metadata[name]={'dtype':dtype,'shape':shape,'uncompressed_array_sha256':hashlib.sha256(payload).hexdigest(),'operation_stage':stage}
        if logical_shape:metadata[name]['logical_shape']=logical_shape
    def get(tag,row,mod=-1,bone=-1,v=-1,entry=-1):return events[(tag,(row,mod,bone,v,entry))][0]
    for tag in ('rest','inverse_rest','evaluated_pose','deform_matrix'):
        add(tag,'<f4',[2,57,4,4],b''.join(get(tag,row,bone=slot) for row in (0,1) for slot in range(57)),'actual pose completion, original armature coordinates; native column -> row-major once')
    active=[i for i,b in enumerate(bones) if b['deform']]
    add('deforming_bone_slots','<i4',[len(active)],struct.pack('<'+'i'*len(active),*active),'original slot indices; helpers retained in57-slot rest/pose arrays')
    validity=[int(b['deform']) for row in (0,1) for b in bones]
    add('dq_computed_valid','<i4',[2,57],struct.pack('<'+'i'*len(validity),*validity),'1 actual native conversion; 0 BONE_NO_DEFORM NOT_COMPUTED')
    for tag,width,tail in (('real_q',4,[4]),('dual_q',4,[4]),('normalized_rotation_columns',9,[3,3])):
        payload=b''.join(events[(tag,(row,-1,slot,-1,-1))][-1] for row in (0,1) for slot in active)
        add(tag+'_values','<f4',[2,len(active)]+tail,payload,'sparse actual mat4_to_dquat conversion; final normalized rotation event only',[2,57]+tail)
    branch=[int(numbers(get('no_scale_branch',row,bone=slot))[0]) for row in (0,1) for slot in active]
    add('no_scale_branch_values','<i4',[2,len(active)],struct.pack('<'+'i'*len(branch),*branch),'actual native branch classification; helper fields absent',[2,57])
    samples=request['selected_vertices'];offsets=[0];groups=[];mapping=[];weights=[]
    for s in samples:
        for e in s['ordered_CSR']:groups.append(e['group_index']);mapping.append(e['bone_index']);weights.append(e['weight'])
        offsets.append(len(groups))
    for name,values in (('vertex_ids',VERTICES),('csr_offsets',offsets),('csr_group',groups),('csr_bone',mapping)):
        add(name,'<i4',[len(values)],struct.pack('<'+'i'*len(values),*values),'original request metadata, independently validated against actual event CSR; not an extracted native primitive')
    add('csr_weight','<f4',[len(weights)],fbytes(weights),'original CSR bits, exact equality verified with native caller rows')
    eligibility=[]
    for row in (0,1):
        for s in samples:
            for entry,e in enumerate(s['ordered_CSR']):
                ctx=(row,0,-1,s['source_vertex'],entry)
                eligible=int(numbers(events[('eligibility',ctx)][0])[0]);eligibility.append(eligible)
                # Missing hemisphere on noncontributing entry is a classification,
                # not a computed native +/- sign. Sparse sign storage below.
    add('csr_eligible','<i4',[2,len(weights)],struct.pack('<'+'i'*len(eligibility),*eligibility),'actual mapped/weight eligibility; original CSR rows retained')
    sign_indices=[];sign_values=[]
    for row in (0,1):
        k=0
        for s in samples:
            for entry,e in enumerate(s['ordered_CSR']):
                ctx=(row,0,-1,s['source_vertex'],entry)
                if ('hemisphere_sign',ctx) in events:sign_indices.extend([row,k]);sign_values.append(events[('hemisphere_sign',ctx)][0])
                k+=1
    add('hemisphere_sign_indices','<i4',[len(sign_values),2],struct.pack('<'+'i'*len(sign_indices),*sign_indices),'[case,original concatenated CSR entry] for actual native sign events')
    add('hemisphere_sign_values','<f4',[len(sign_values)],b''.join(sign_values),'sparse actual sign; noncontributing sign NOT_COMPUTED',[2,len(weights)])
    for tag,n,tail in (('running_total',1,[]),('running_real_q',4,[4]),('running_dual_q',4,[4])):
        data=b''.join(get(tag,row,0,v=s['source_vertex'],entry=e) for row in (0,1) for s in samples for e in range(len(s['ordered_CSR'])))
        add(tag,'<f4',[2,len(weights)]+tail,data,'actual first-DQ ordered post-entry state, unchanged for noncontributing entries')
    for name,tag,mod,tail in (
        ('original_co','caller_input_local',0,[3]),('transformed_co','dq_transformed_armature_co',0,[3]),('finalize_delta','finalize_delta',0,[3]),
        ('stage00_local','caller_input_local',0,[3]),('stage00_world','caller_input_world',0,[3]),
        ('dq_output_local','caller_output_local',0,[3]),('dq_output_world','caller_output_world',0,[3]),
        ('stage01_local','caller_output_local',1,[3]),('stage01_world','caller_output_world',1,[3]),
        ('normalized_real_q','normalized_real_q',0,[4]),('normalized_dual_q','normalized_dual_q',0,[4]),
        ('quaternion_length_squared','quaternion_length_squared',0,[]),('reciprocal_length_squared','reciprocal_length_squared',0,[]),
        ('dq_rotation_matrix','dq_rotation_matrix',0,[3,3]),('dq_translation','dq_translation',0,[3])):
        add(name,'<f4',[2,5]+tail,b''.join(get(tag,row,mod,v=v) for row in (0,1) for v in VERTICES),'actual first DQ ARMATURE primitive (finalize_delta is native armature-space vector, not reconstructed body-local delta)' if tag.startswith(('dq_','normalized_','quaternion_','reciprocal_')) or tag=='finalize_delta' else 'actual original body LOCAL/WORLD; stage00 before first DQ; stage01 after second masked LBS; no inverse-WORLD reconstruction')
    for tag in ('object_world','rig_world','premat','postmat'):
        add(tag,'<f4',[2,4,4],b''.join(get(tag,row,0) for row in (0,1)),'actual first-DQ caller transport; original legacy inverse order')
    mask=[]
    for row in (0,1):
        for v in VERTICES:mask.append(int(('skip_previous_mask',(row,1,-1,v,-1)) not in events))
    add('stage01_intermediates_computed_valid','<i4',[2,5],struct.pack('<'+'i'*len(mask),*mask),'0 zero mask/native return; caller coordinates remain actual and unchanged')
    # Second modifier fields are copied from exact native events, never rebuilt
    # from final WORLD or first-DQ values. Sparse indices preserve skipped rows.
    computed=[(row,index) for row in (0,1) for index,v in enumerate(VERTICES) if mask[row*5+index]]
    flat=[value for pair in computed for value in pair]
    add('lbs_computed_vertex_indices','<i4',[len(computed),2],struct.pack('<'+'i'*len(flat),*flat),'[case,original sample index] actual LBS computation present; skipped rows absent')
    per_vertex=(('lbs_co_armature_values','co_armature',[3]),
      ('lbs_previous_co_weight_values','previous_co_weight',[]),('lbs_armature_weight_values','armature_weight',[]),
      ('lbs_finalize_scale_factor_values','lbs_finalize_scale_factor',[]),('lbs_finalize_delta_armature_values','finalize_delta',[3]),
      ('lbs_co_before_finalize_update_values','transformed_co_before_update',[3]),('lbs_co_after_finalize_update_values','co_after_update',[3]),
      ('lbs_pre_mask_local_values','pre_mask_local',[3]),('lbs_vertex_output_local_values','vertex_output_local',[3]))
    for name,tag,tail in per_vertex:
        add(name,'<f4',[len(computed)]+tail,b''.join(get(tag,row,1,v=VERTICES[index]) for row,index in computed),
            'actual SECOND masked LBS native primitive; co/delta ARMATURE, pre_mask/output original BODY LOCAL; sparse NOT_COMPUTED skip',[2,5]+tail)
    for name,tag in (('lbs_mask_weight','mask_weight'),('lbs_previous_cached_local','previous_cached_local'),
                     ('lbs_caller_input_local','caller_input_local'),('lbs_caller_input_world','caller_input_world')):
        tail=[] if tag=='mask_weight' else [3]
        add(name,'<f4',[2,5]+tail,b''.join(get(tag,row,1,v=v) for row in (0,1) for v in VERTICES),'actual second caller/mask/cache including native skip branch')
    entry_indices=[];entry_context=[]
    for row,index in computed:
        s=samples[index]
        for local,e in enumerate(s['ordered_CSR']):
            entry_indices.extend([row,index,local,offsets[index]+local]);entry_context.append((row,s['source_vertex'],local))
    add('lbs_computed_csr_indices','<i4',[len(entry_context),4],struct.pack('<'+'i'*len(entry_indices),*entry_indices),
        '[case,sample index,original local CSR entry,original concatenated CSR entry]; ZERO/helpers/masks retained; only native skipped vertex rows absent')
    for name,tag,tail in (('lbs_running_delta_values','running_lbs_delta',[3]),('lbs_running_total_values','running_total',[]),
                         ('lbs_mapped_bone_values','mapped_bone',[]),('lbs_eligibility_values','eligibility',[])):
        add(name,'<f4',[len(entry_context)]+tail,b''.join(get(tag,row,1,v=v,entry=entry) for row,v,entry in entry_context),
            'actual SECOND LBS ordered per-entry post-state; unchanged for noncontributing zero/helpers/mask entries',[2,len(weights)]+tail)
    add('lbs_finalize_total_values','<f4',[len(computed)],b''.join(get('running_total',row,1,v=VERTICES[index],entry=len(samples[index]['ordered_CSR'])-1) for row,index in computed),
        'actual native accumulator total passed unchanged to LinearMixer.finalize; copied last native post-entry total',[2,5])
    for tag in ('object_world','rig_world','premat','postmat'):
        add('lbs_'+tag,'<f4',[2,4,4],b''.join(get(tag,row,1) for row in (0,1)),
            'actual SECOND modifier transport matrices; native legacy inverse order; not reused first-modifier matrices')
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for name,data in arrays.items():z.writestr(name+'.npy',data)
    manifest={'classification':classification,'npz_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'arrays':metadata,'context_validation':result,
      'sparse_contract':'Logical [2,57] fields use deforming_bone_slots + dq_computed_valid. No dense native helper DQ/no-scale bytes exist. Sparse hemisphere likewise retains NOT_COMPUTED sign, not0/identity proof.',
      'canonical_names_changed_for_missing_fields':'*_values indexed sparse arrays; consumer must explicitly agree this branch-aware schema before original dense request acceptance.',
      'coordinate_scope':'LOCAL original source body; WORLD source object positive uniform matrix before Unity P; stage01 explicitly second modifier output',
      'native_numeric_acceptance':False,'installed_compiler_equivalence':False}
    manifest['second_LBS_contract']={'computed_samples':computed,'NOT_COMPUTED_sample_indices':[2,3,4],
      'per_vertex_index':'lbs_computed_vertex_indices [case,sample]',
      'per_entry_index':'lbs_computed_csr_indices [case,sample,local original CSR,concatenated original CSR]',
      'primitive_source':'actual row/modifier1/bone-1/vertex/entry event bytes; no re-normalization or reconstruction',
      'full_deform_matrix':'NOT_COMPUTED ordinary nullopt path; do not invent unused matrix',
      'consumer_schema_agreement':'NOT_YET_CONFIRMED_WITH_LAPTOP; acceptance remains pending'}
    path.with_suffix('.manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
    return manifest
