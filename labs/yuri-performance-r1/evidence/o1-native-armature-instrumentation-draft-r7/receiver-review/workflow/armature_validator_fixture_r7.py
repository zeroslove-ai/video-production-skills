"""Complete SYNTHETIC fixture for validator control flow only. Never native evidence."""
import copy,json,struct
from pathlib import Path
from armature_canonical_validate_r7 import validate,fbytes,numbers,VERTICES

def fixture(request,bones):
    events={}
    def emit(tag,row,values,mod=-1,bone=-1,v=-1,entry=-1):events[(tag,(row,mod,bone,v,entry))]=[fbytes(values)]
    identity=[1.,0.,0.,0.,0.,1.,0.,0.,0.,0.,1.,0.,0.,0.,0.,1.]
    for row in (0,1):
        for slot,b in enumerate(bones):
            for tag,value in (('rest',request['original_rest_57'][slot]),('inverse_rest',identity),('deform_matrix',identity),('evaluated_pose',request['pose_inputs'][row]['B_source_exact_pose'][slot])):emit(tag,row,value,bone=slot)
            emit('bone_no_deform',row,[float(not b['deform'])],bone=slot)
            if b['deform']:
                emit('no_scale_branch',row,[1.],bone=slot)
                emit('normalized_rotation_columns',row,[1.,0.,0.,0.,1.,0.,0.,0.,1.],bone=slot)
                emit('quat_conversion_R',row,identity,bone=slot)
                emit('real_q',row,[1.,0.,0.,0.],bone=slot);emit('dual_q',row,[0.]*4,bone=slot)
        for mod in (0,1):
            for tag in ('object_world','rig_world','premat','postmat'):emit(tag,row,identity,mod=mod)
            for tag,value in (('deformflag',5. if mod==0 else 1.),('full_deform',0.),('armature_mask_group',-1. if mod==0 else 52.)):emit(tag,row,[value],mod=mod)
            for sample in request['selected_vertices']:
                v=sample['source_vertex'];original=sample['original_position'];csr=sample['ordered_CSR'];mask=next((e['weight'] for e in csr if e['group_index']==52),0.)
                for tag in ('caller_input_local','caller_input_world','caller_output_local','caller_output_world','vertex_input_local'):emit(tag,row,original,mod=mod,v=v)
                for index,e in enumerate(csr):emit('csr_original_group_weight',row,[e['group_index'],e['weight']],mod=mod,v=v,entry=index)
                if mod==1:
                    emit('mask_weight',row,[mask],mod=mod,v=v);emit('previous_cached_local',row,original,mod=mod,v=v)
                    if mask==0.:
                        emit('skip_previous_mask',row,[1.],mod=mod,v=v);continue
                emit('armature_weight',row,[1.],mod=mod,v=v)
                emit('previous_co_weight',row,[0. if mod==0 else 1.-mask],mod=mod,v=v)
                total=0.;state=[0.]*4
                for index,e in enumerate(csr):
                    mapping=e['bone_index'];mapping=-1 if mapping>=0 and not bones[mapping]['deform'] else mapping
                    contributes=mapping>=0 and e['weight']!=0.
                    if contributes:total=numbers(fbytes([total+e['weight']]))[0];state=[total,0.,0.,0.]
                    for tag,value in (('mapped_bone',float(mapping)),('eligibility',float(contributes)),('running_total',total)):emit(tag,row,[value],mod=mod,v=v,entry=index)
                    if mapping>=0:
                        emit('effective_weight',row,[e['weight']],mod=mod,v=v,entry=index);emit('bone_segments',row,[1.],mod=mod,v=v,entry=index)
                    if mod==0:
                        emit('running_real_q',row,state,mod=mod,v=v,entry=index);emit('running_dual_q',row,[0.]*4,mod=mod,v=v,entry=index)
                        if contributes:emit('hemisphere_sign',row,[1.],mod=mod,v=v,entry=index)
                    else:emit('running_lbs_delta',row,[total,0.,0.],mod=mod,v=v,entry=index)
                if mod==1:emit('lbs_finalize_scale_factor',row,[1./total],mod=mod,v=v)
                for tag in ('co_armature','finalize_delta','transformed_co_before_update','co_after_update','pre_mask_local','vertex_output_local'):emit(tag,row,original,mod=mod,v=v)
                if mod==0:
                    for tag,value in (('normalized_real_q',[1.,0.,0.,0.]),('normalized_dual_q',[0.]*4),('quaternion_length_squared',[1.]),('reciprocal_length_squared',[1.]),('dq_rotation_matrix',[1.,0.,0.,0.,1.,0.,0.,0.,1.]),('dq_translation',[0.]*3),('dq_transformed_armature_co',original)):emit(tag,row,value,mod=mod,v=v)
    return events

def tests(request,bones):
    valid=fixture(request,bones);result=validate(valid,request,bones)
    assert result['status']=='PASS_CONTEXT_BRANCH_CLASSIFIED_NOT_NUMERIC_EQUIVALENCE'
    tests=[]
    def defect(name,mutate,reason):
        sample=copy.deepcopy(valid);mutate(sample)
        try:validate(sample,request,bones)
        except ValueError as e:
            assert reason in str(e),(name,str(e),reason)
            tests.append({'name':name,'status':'REJECTED_AT_INTENDED_GATE','reason':str(e)})
        else:raise AssertionError('defect accepted '+name)
    key=('csr_original_group_weight',(1,1,-1,40817,len(request['selected_vertices'][-1]['ordered_CSR'])-1))
    defect('late_row_missing_CSR',lambda e:e.pop(key),'missing/duplicate csr_original_group_weight')
    key=('inverse_rest',(1,-1,56,-1,-1))
    defect('duplicate_late_event',lambda e:e[key].append(e[key][0]),'duplicate/depsgraph')
    key=('normalized_rotation_columns',(1,-1,1,-1,-1))
    defect('duplicate_normalized_columns',lambda e:e[key].append(e[key][0]),'ambiguous native quaternion')
    key=('caller_output_local',(1,1,-1,40817,-1))
    defect('nonfinite',lambda e:e.__setitem__(key,[fbytes([float('nan'),0.,0.])]),'nonfinite')
    key=('inverse_rest',(1,-1,56,-1,-1))
    defect('wrong_shape',lambda e:e.__setitem__(key,[e[key][0][:-4]]),'wrong cardinality inverse_rest')
    defect('mixed_context',lambda e:e.__setitem__(('rest',(0,9,0,-1,-1)),[b'\0'*64]),'invalid caller context')
    defect('full_deform_caller',lambda e:e.__setitem__(('full_deform',(1,1,-1,-1,-1)),[fbytes([1.])]),'not ordinary nullopt')
    defect('wrong_DQ_LBS_flag',lambda e:e.__setitem__(('deformflag',(1,1,-1,-1,-1)),[fbytes([5.])]),'DQ-first/LBS-second')
    defect('fabricated_helper_DQ',lambda e:e.__setitem__(('real_q',(0,-1,0,-1,-1)),[fbytes([1.,0.,0.,0.])]),'fabricated/nonexecuted helper')
    def flip(e,key):
        data=bytearray(e[key][0]);data[0]^=1;e[key]=[bytes(data)]
    defect('wrong_rest_bits',lambda e:flip(e,('rest',(1,-1,56,-1,-1))),'original rest bytes mismatch')
    defect('wrong_pose_bits',lambda e:flip(e,('evaluated_pose',(1,-1,56,-1,-1))),'actual source pose mismatch')
    defect('wrong_mask',lambda e:e.__setitem__(('mask_weight',(1,1,-1,11189,-1)),[fbytes([0.])]),'actual mask weight mismatch')
    def bad_link(e):
        for tag in ('caller_input_local','vertex_input_local'):e[(tag,(1,1,-1,11189,-1))]=[fbytes([0.,0.,0.])]
    defect('stage01_link',bad_link,'stage01input != stage00output')
    defect('fake_computation_on_skip',lambda e:e.__setitem__(('finalize_delta',(1,1,-1,40817,-1)),[fbytes([0.]*3)]),'fabricated computation on native skip branch')
    defect('missing_LBS_scale_factor',lambda e:e.pop(('lbs_finalize_scale_factor',(1,1,-1,11189,-1))),'missing/duplicate lbs_finalize_scale_factor')
    return {'classification':'SYNTHETIC_CONTROL_FLOW_ONLY_NOT_NATIVE_NUMERIC_PASS','complete_fixture':result,'one_defect_tests':tests,'records':len(valid),'native_data_PASS':False}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--request',type=Path,required=True);p.add_argument('--bones',type=Path,required=True);a=p.parse_args()
    print(json.dumps(tests(json.loads(a.request.read_bytes()),json.loads(a.bones.read_bytes())['Meshy_Fitted_Rig']['bones']),indent=2))
