"""Strict native-event context/numeric validator; default syntax/selftest only.
PASS_CONTEXT_BRANCH_CLASSIFIED is not installed arithmetic / Unity / PBR PASS.
"""
from pathlib import Path
import argparse, hashlib, json, math, struct
from armature_trace_unpack_r1 import decode

REQUEST_SHA='a46c693c28e09a93729bbe433a522d47c7a452c740a6af6ceb8868ddec370b17'
RECIPE_SHA='0cd0bdd70e5a6c0670846dab74e295b0a637a79f1c6d57d503611d5cf50aafe0'
SOURCE_SHA='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
ACTION_SHA='6874ec69d5721f385d31edaa06ef0d58c89a543b98bacd961f8f575ff57eef4d'
POSE_SHA='03fdaaad90211f411910024b94ea27a6e3d6f0728578513a5c1825d33d1d71a3'
CASES=[('YRA_R4_Startle_Short',11),('YRA_R4_Struggle_Strong_Loop',6)]
VERTICES=[11189,14918,21485,22227,40817]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fbytes(values):return struct.pack('<'+'f'*len(values),*values)
def numbers(payload):return struct.unpack('<'+'f'*(len(payload)//4),payload)
def require(condition,reason):
    if not condition:raise ValueError(reason)

def verify_arming_inputs(files,row,actual_action,actual_frame,rig,body):
    require(row in (0,1),'wrong row')
    require((actual_action,actual_frame)==CASES[row],'actual active Action/frame mismatch')
    require((rig,body)==('Meshy_Fitted_Rig','Meshy_Body_NeutralCovered'),'wrong object routing')
    expected={'source':SOURCE_SHA,'actions':ACTION_SHA,'pose':POSE_SHA,'recipe':RECIPE_SHA,'request':REQUEST_SHA}
    for name,value in expected.items():
        require(name in files and Path(files[name]).is_file(),'required actual input file missing: '+name)
        require(sha(files[name])==value,'actual file identity mismatch: '+name)
    request=json.loads(Path(files['request']).read_bytes())
    require([(x['clip'],x['frame']) for x in request['pose_inputs']]==CASES,'request Action mapping mismatch')
    require([x['source_vertex'] for x in request['selected_vertices']]==VERTICES,'request vertex order drift')
    return {'status':'FILES_AND_DECLARED_ROUTING_VERIFIED_NOT_RUNTIME_ACTION_INSPECTED',
      'row':row,'active_action':actual_action,'actual_frame':actual_frame,
      'request':request,'file_sha256':expected,
      'required_live_checks':['owned adapter reads actual bpy rig.animation_data.action and slot','actual native evaluated pose B float32 bytes','complete original rest/CSR against full recipe, helpers/masks intact','owned build executable/module/compiler flags and source patch SHA','source/Action/NLA/pose restore after joined workers, including failed captures']}

def load_events(paths):
    events={}
    for p in paths:
        for key,(contexts,values) in decode(Path(p).read_bytes()).items():
            tag=key.rsplit('_',1)[0]
            for context,payload in zip(contexts,values):
                require(all(math.isfinite(v) for v in numbers(payload)),'nonfinite real native event: '+tag)
                events.setdefault((tag,tuple(context)),[]).append(payload)
    return events

def validate(events,request,bone_metadata):
    require(len(request['bone_names'])==57 and len(bone_metadata)==57,'57-slot contract')
    require(request['bone_names']==[b['name'] for b in bone_metadata],'original slot name/order drift')
    require([v['source_vertex'] for v in request['selected_vertices']]==VERTICES,'five original sample order drift')
    # Strict allowlists: pose only modifier=-1/bone slot; caller only modifier0/1.
    pose_tags={'rest','evaluated_pose','bone_no_deform','inverse_rest','deform_matrix','normalized_rotation_columns','no_scale_branch','quat_conversion_R','real_q','dual_q'}
    caller_tags={'object_world','rig_world','deformflag','premat','postmat','full_deform','armature_mask_group'}
    sample_tags={'caller_input_local','caller_input_world','caller_output_local','caller_output_world','vertex_input_local','previous_cached_local','csr_original_group_weight','mask_weight','skip_previous_mask','skip_zero_mask','co_armature','armature_weight','previous_co_weight','eligibility','mapped_bone','running_total','running_real_q','running_dual_q','bone_segments','effective_weight','running_lbs_delta','hemisphere_sign','normalized_real_q','normalized_dual_q','quaternion_length_squared','reciprocal_length_squared','dq_rotation_matrix','dq_translation','dq_transformed_armature_co','finalize_delta','transformed_co_before_update','co_after_update','pre_mask_local','vertex_output_local'}
    for (tag,(row,mod,bone,vertex,entry)),values in events.items():
        require(all(math.isfinite(v) for p in values for v in numbers(p)),'nonfinite real native event: '+tag)
        require(row in (0,1),'unknown row')
        if mod==-1:require(tag in pose_tags and 0<=bone<57 and vertex==entry==-1,'mixed pose/caller context')
        elif vertex==-1:require(mod in (0,1) and bone==entry==-1 and tag in caller_tags,'invalid caller context')
        else:require(mod in (0,1) and bone==-1 and vertex in VERTICES and tag in sample_tags,'invalid sample context')
        if tag!='normalized_rotation_columns':require(len(values)==1,'duplicate/depsgraph evaluation ambiguity: '+tag)
    def get(tag,row,mod=-1,bone=-1,v=-1,entry=-1,n=None):
        values=events.get((tag,(row,mod,bone,v,entry)),[])
        require(len(values)==1,'missing/duplicate '+tag+' '+str((row,mod,bone,v,entry)))
        result=values[0];require(n is None or len(result)==n*4,'wrong cardinality '+tag);return result
    def scalar(tag,row,mod=-1,bone=-1,v=-1,entry=-1):return numbers(get(tag,row,mod,bone,v,entry,1))[0]
    classifications=[]
    for row in (0,1):
        for bone,b in enumerate(bone_metadata):
            for tag in ('rest','inverse_rest','evaluated_pose','deform_matrix'):get(tag,row,bone=bone,n=16)
            require(get('rest',row,bone=bone)==fbytes(request['original_rest_57'][bone]),'original rest bytes mismatch')
            require(get('evaluated_pose',row,bone=bone)==fbytes(request['pose_inputs'][row]['B_source_exact_pose'][bone]),'actual source pose mismatch; A is not accepted')
            no_deform=scalar('bone_no_deform',row,bone=bone)
            require(no_deform==float(not b['deform']),'helper/nondeform flag drift')
            if no_deform:
                for tag in ('normalized_rotation_columns','no_scale_branch','quat_conversion_R','real_q','dual_q'):
                    require((tag,(row,-1,bone,-1,-1)) not in events,'fabricated/nonexecuted helper DQ')
                classifications.append({'row':row,'bone':bone,'DQ':'NOT_COMPUTED_NATIVE_BONE_NO_DEFORM'})
            else:
                branch=scalar('no_scale_branch',row,bone=bone);require(branch in (0.,1.),'invalid native scale branch')
                normals=events.get(('normalized_rotation_columns',(row,-1,bone,-1,-1)),[])
                require(len(normals)==(1 if branch==1 else 2),'ambiguous native quaternion conversion occurrences')
                require(all(len(x)==36 for x in normals),'wrong normalized rotation shape')
                get('quat_conversion_R',row,bone=bone,n=16);get('real_q',row,bone=bone,n=4);get('dual_q',row,bone=bone,n=4)
        for mod in (0,1):
            for tag in ('object_world','rig_world','premat','postmat'):get(tag,row,mod,n=16)
            require(scalar('deformflag',row,mod)==(5. if mod==0 else 1.),'DQ-first/LBS-second actual deformflag drift')
            require(scalar('full_deform',row,mod)==0.,'not ordinary nullopt caller')
            require(scalar('armature_mask_group',row,mod)==(-1. if mod==0 else 52.),'mask group drift')
            for sample in request['selected_vertices']:
                v=sample['source_vertex'];csr=sample['ordered_CSR']
                previous_total=None;previous_state=None
                for tag in ('caller_input_local','caller_input_world','caller_output_local','caller_output_world','vertex_input_local'):get(tag,row,mod,v=v,n=3)
                if mod==0:require(get('caller_input_local',row,mod,v=v)==fbytes(sample['original_position']),'stage00 original co mismatch')
                require(get('vertex_input_local',row,mod,v=v)==get('caller_input_local',row,mod,v=v),'vertex/caller input mismatch')
                mask=next((e['weight'] for e in csr if e['group_index']==52),0.)
                if mod==1:
                    for suffix in ('local','world'):
                        require(get('caller_input_'+suffix,row,mod,v=v)==get('caller_output_'+suffix,row,0,v=v),'stage01input != stage00output')
                    require(get('object_world',row,1)==get('object_world',row,0),'object matrix changed between modifiers')
                    require(get('mask_weight',row,mod,v=v)==fbytes([mask]),'actual mask weight mismatch')
                    require(get('previous_cached_local',row,mod,v=v)==get('caller_input_local',row,0,v=v),'cached previous original coordinate drift')
                for entry,original in enumerate(csr):
                    require(get('csr_original_group_weight',row,mod,v=v,entry=entry)==fbytes([original['group_index'],original['weight']]),'original CSR order/weight drift')
                if mod==1 and mask==0.:
                    require(scalar('skip_previous_mask',row,mod,v=v)==1.,'native zero-mask skip not classified')
                    for suffix in ('local','world'):
                        require(get('caller_output_'+suffix,row,mod,v=v)==get('caller_input_'+suffix,row,mod,v=v),'skip changed coordinates')
                    allowed={'caller_input_local','caller_input_world','caller_output_local','caller_output_world','vertex_input_local','previous_cached_local','mask_weight','skip_previous_mask','csr_original_group_weight'}
                    for tag,ctx in events:
                        if ctx[:4]==(row,mod,-1,v):
                            require(tag in allowed,'fabricated computation on native skip branch')
                            if tag=='csr_original_group_weight':require(0<=ctx[4]<len(csr),'surplus CSR row')
                    classifications.append({'row':row,'modifier':mod,'vertex':v,'intermediates':'NOT_COMPUTED_NATIVE_PREVIOUS_MASK_ONE','mask_weight':0.,'stage_local_world':'ACTUAL_CALLER_UNCHANGED'})
                    continue
                require(('skip_previous_mask',(row,mod,-1,v,-1)) not in events and ('skip_zero_mask',(row,mod,-1,v,-1)) not in events,'unexpected skip branch')
                require(scalar('armature_weight',row,mod,v=v)==1.,'unexpected overall deformation mask')
                require(get('previous_co_weight',row,mod,v=v)==fbytes([0. if mod==0 else 1.-mask]),'previous mask interpolation weight drift')
                for entry,original in enumerate(csr):
                    require(get('csr_original_group_weight',row,mod,v=v,entry=entry)==fbytes([original['group_index'],original['weight']]),'original CSR order/weight drift')
                    mapped=scalar('mapped_bone',row,mod,v=v,entry=entry)
                    expected_mapping=original['bone_index']
                    if expected_mapping>=0 and not bone_metadata[expected_mapping]['deform']:expected_mapping=-1
                    require(mapped==float(expected_mapping),'native mapping drift (original helper slot is preserved in request)')
                    contributes=expected_mapping>=0 and original['weight']!=0
                    require(scalar('eligibility',row,mod,v=v,entry=entry)==float(contributes),'eligibility drift')
                    total=get('running_total',row,mod,v=v,entry=entry,n=1)
                    if mod==0:
                        get('running_real_q',row,mod,v=v,entry=entry,n=4);get('running_dual_q',row,mod,v=v,entry=entry,n=4)
                        state=get('running_real_q',row,mod,v=v,entry=entry)+get('running_dual_q',row,mod,v=v,entry=entry)
                        if contributes:
                            require(scalar('hemisphere_sign',row,mod,v=v,entry=entry) in (-1.,1.),'hemisphere sign')
                        else:
                            require(('hemisphere_sign',(row,mod,-1,v,entry)) not in events,'noncontributing sign must not be fabricated')
                    else:state=get('running_lbs_delta',row,mod,v=v,entry=entry,n=3)
                    if not contributes and previous_state is not None:
                        require(state==previous_state and total==previous_total,'noncontributing accumulator changed')
                    if expected_mapping>=0:
                        require(get('effective_weight',row,mod,v=v,entry=entry,n=1)==fbytes([original['weight']]),'unexpected envelope weight change')
                        require(scalar('bone_segments',row,mod,v=v,entry=entry)==1.,'B-bone route not admitted')
                    previous_state=state;previous_total=total
                # No surplus CSR entries, zero weights/helpers remain present.
                for tag,ctx in events:
                    if ctx[:4]==(row,mod,-1,v) and ctx[4]>=0:require(ctx[4]<len(csr),'surplus CSR row')
                for tag in ('co_armature','finalize_delta','transformed_co_before_update','co_after_update','pre_mask_local','vertex_output_local'):get(tag,row,mod,v=v,n=3)
                if mod==0:
                    for tag,n in (('normalized_real_q',4),('normalized_dual_q',4),('quaternion_length_squared',1),('reciprocal_length_squared',1),('dq_rotation_matrix',9),('dq_translation',3),('dq_transformed_armature_co',3)):get(tag,row,mod,v=v,n=n)
                else:
                    get('previous_cached_local',row,mod,v=v,n=3);get('mask_weight',row,mod,v=v,n=1)
    return {'status':'PASS_CONTEXT_BRANCH_CLASSIFIED_NOT_NUMERIC_EQUIVALENCE','branch_classification':classifications,
      'rows':2,'source_slots':57,'ordinary_modifiers':2,'vertices':5,
      'pending':['canonical numeric NPZ assembly/validity mask agreement','forward WORLD arithmetic QA and full63561/all304799 gates','compiled/backend/installed custody','actual runtime native/source restore proof']}

def selftest():
    # Negative consumer tests use synthetic format events only, no native claim.
    tests=[]
    for data in ({}, {('rest',(0,-1,0,-1,-1)):[b'\0'*64,b'\0'*64]}, {('rest',(0,9,0,-1,-1)):[b'\0'*64]}):
        try:validate(data,{'bone_names':['b']*57,'selected_vertices':[{'source_vertex':v} for v in VERTICES]},[{'name':'b','deform':True}]*57)
        except (ValueError,KeyError):tests.append('REJECTED')
        else:raise AssertionError('invalid capture accepted')
    try:verify_arming_inputs({},0,'YRA_R1_Startle_Short',11,'Meshy_Fitted_Rig','Meshy_Body_NeutralCovered')
    except ValueError:tests.append('WRONG_ACTION_REJECTED')
    else:raise AssertionError('wrong action accepted')
    return {'status':'PASS_SYNTHETIC_NEGATIVE_CHECKS_ONLY','tests':tests,'native_data_PASS':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');p.add_argument('--input',type=Path,action='append');p.add_argument('--request',type=Path);p.add_argument('--bones',type=Path);a=p.parse_args()
    if a.self_test:print(json.dumps(selftest()))
    else:
        require(a.input and a.request and a.bones,'required inputs missing');require(sha(a.request)==REQUEST_SHA,'request identity mismatch')
        print(json.dumps(validate(load_events(a.input),json.loads(a.request.read_bytes()),json.loads(a.bones.read_bytes())['Meshy_Fitted_Rig']['bones'])))
