"""Audit/package already captured source arrays; no native launch or consumer writes."""
from pathlib import Path
import hashlib,json,zipfile
import numpy as np
LAB=Path(__file__).resolve().parent.parent
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
P=BASE/'o1-morph67-native-broker-preparation-r4';O=BASE/'o1-morph67-two-input-native-compare-r1'
E=LAB/'evidence/o1-morph67-two-input-native-normal-result-r1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):
    with p.open('x',encoding='utf8') as f:json.dump(v,f,ensure_ascii=False,indent=2)
def angle(a,b):
    a=a.astype(np.float64);b=b.astype(np.float64)
    a/=np.linalg.norm(a,axis=1)[:,None];b/=np.linalg.norm(b,axis=1)[:,None]
    return np.degrees(np.arctan2(np.linalg.norm(np.cross(a,b),axis=1),np.sum(a*b,axis=1)))
def main():
    assert not E.exists();E.mkdir()
    guard_path=P/'NATIVE_GUARD_RESULT_R1.json';guard=json.loads(guard_path.read_bytes())
    cfg=json.loads((P/'FIXED_BROKER_CONFIG_R1.json').read_bytes())
    approval=P/'NEW_NATIVE_APPROVAL_R1.json'
    assert guard['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN'
    assert guard['inputs_before']==guard['inputs_after']==cfg['pinned_files']
    assert all(sha(Path(p))==h for p,h in cfg['pinned_files'].items())
    assert guard['terminal_owned_handle_signaled'] and guard['terminal_exit_code']==0
    assert guard['terminal_job']=={'active':0,'total':1,'limit_terminated':0,'pids':[]} and not guard['cleanup_errors']
    for phase in ['BEFORE','AFTER']:
        assert guard[phase]['owned_handle_signaled'] is False
        assert guard[phase]['job']=={'active':1,'total':1,'limit_terminated':0,'pids':[guard['pid']]}
        for h in ['original','limited']:
            assert guard[phase][h]['QueryFullProcessImageName_success'] and guard[phase][h]['creation_FILETIME']==guard['creation_FILETIME']
    result_path=O/'TWO_INPUT_NATIVE_RESULT_PRIVATE_R1.json';result=json.loads(result_path.read_bytes())
    assert result['OFF_full_component_diff']=={} and len(result['records'])==6 and len(result['OFF_records'])==2
    static=BASE/'o1-source-fidelity-recovery-r1/data/Character_Body_Head_original_mesh.npz'
    assert sha(static)=='1a48cf823cb6cf0c95c7eee6d4b7e7e8a952cbaadd50d1d9ad18d909be34f473'
    files=result['records']+result['OFF_records'];arrays={}
    for row in files:
        p=O/row['file'];assert sha(p)==row['sha256'] and p.stat().st_size==row['bytes']
        with np.load(p,allow_pickle=False) as z:arrays[row['case']]={k:z[k].copy() for k in z.files}
    b=arrays['OFF_before'];a=arrays['OFF_after']
    assert b.keys()==a.keys() and all(np.array_equal(b[k],a[k]) for k in b)
    with np.load(static,allow_pickle=False) as s:
        rows=[];packed=hashlib.sha256(s['attribute_19_value'].astype('<i2').tobytes()).hexdigest()
        # Stable source-polygon slot selection, not a consumer pixel-owner claim.
        ps=np.flatnonzero(s['polygon_material_slot']==6)
        lash=np.concatenate([np.arange(s['polygon_loop_start'][p],s['polygon_loop_start'][p]+s['polygon_loop_total'][p]) for p in ps])
        for row in result['records']:
            x=arrays[row['case']]
            for k in ['loop_vertex_indices','polygon_loop_start','polygon_loop_total','polygon_material_slot']:assert np.array_equal(x[k],s[k])
            assert np.array_equal(x['UVMap'],s['uv_0']) and np.array_equal(x['custom_normal_short2'],s['attribute_19_value'])
            assert np.array_equal(x['custom_normal_short2'].astype(np.int16).astype(np.int32),x['custom_normal_short2'])
            assert x['local_CORNER_normal'].shape==x['local_CORNER_tangent'].shape==(66861,3)
            assert x['local_position'].shape==(12928,3) and all(np.isfinite(v).all() for v in x.values())
            tri=x['triangle_source_corners'];poly=x['triangle_source_polygon']
            assert np.all((tri>=0)&(tri<66861)) and len(poly)==len(tri)
            assert np.all(tri>=s['polygon_loop_start'][poly,None]) and np.all(tri<s['polygon_loop_start'][poly,None]+s['polygon_loop_total'][poly,None])
            assert np.array_equal(x['polygon_use_smooth'],b['polygon_use_smooth'])
            ang=angle(x['local_CORNER_normal'],b['local_CORNER_normal'])
            rows.append({'case':row['case'],'file':row['file'],'bytes':row['bytes'],'sha256':row['sha256'],
                'vertices':12928,'CORNERs':66861,'polygons':21701,'source_topology_UV_material_smooth_exact':True,
                'custom_normal_type':'CORNER INT16_2D','custom_payload_exact_original':True,'custom_short2_LE_SHA256':packed,
                'normal_unit_length_max_abs_error':float(np.max(np.abs(np.linalg.norm(x['local_CORNER_normal'],axis=1)-1))),
                'tangent_sign_values':sorted(np.unique(x['bitangent_sign']).tolist()),
                'tangent_normal_max_abs_dot':float(np.max(np.abs(np.sum(x['local_CORNER_normal']*x['local_CORNER_tangent'],axis=1)))),
                'position_vs_FULL_SOURCE_OFF_max_vector_delta_m':float(np.linalg.norm(x['local_position']-b['local_position'],axis=1).max()),
                'normal_vs_FULL_SOURCE_OFF_max_angle_deg':float(ang.max()),
                'CORNERs_vs_FULL_SOURCE_OFF_over_0_001deg':int((ang>.001).sum()),
                'head_slot6_vs_FULL_SOURCE_OFF_max_angle_deg':float(ang[lash].max()),
                'normal_diagnostic_scope':'Native stage changes versus FULL_SOURCE OFF baseline, not consumer errors. SHAPE_ONLY/GN baselines differ modifier scope; do not attribute all angle delta solely to FACE.'})
        stage_pairs=[]
        for tag in ['WORST','NEUTRAL']:
            for left,right in [('SHAPE_ONLY','SHAPE_GN'),('SHAPE_GN','FULL_SOURCE')]:
                x=arrays[tag+'_'+left];y=arrays[tag+'_'+right];ang=angle(x['local_CORNER_normal'],y['local_CORNER_normal'])
                stage_pairs.append({'input':tag,'from':left,'to':right,
                    'position_max_vector_delta_m':float(np.linalg.norm(y['local_position']-x['local_position'],axis=1).max()),
                    'normal_max_angle_deg':float(ang.max()),'normal_changed_CORNERs':int(np.any(y['local_CORNER_normal']!=x['local_CORNER_normal'],axis=1).sum()),
                    'packed_payload_exact_between_stages':np.array_equal(x['custom_normal_short2'],y['custom_normal_short2'])})
    prior=BASE/'o1-gaze-evaluated-corner-reference-r1/neutral_evaluated_corners.npz'
    with np.load(prior) as z:
        prior_delta=float(np.max(np.abs(b['local_CORNER_normal']-z['Character_Body_Head_local_corner_normal'])))
    contract={'scope':'SOURCE_REFERENCE_ONLY / original head-local source-rest, FACE16+GAZE2; no full runtime body pose parity',
        'arrays':'6stage+2OFF NPZ, original source-loop indices retained. Current local position, CORNER normal/tangent, sign, custom short2, topology/UV/smooth/triangle source polygon+corners and object matrix are private.',
        'consumer_stage_selection':'Compare unskinned Unity mesh with SHAPE_GN if consumer has applied source GN before skinning; FULL_SOURCE includes original source Armature/rest. Match local/world basis and actual bones before any postskin comparison.',
        'normal_space':'Blender head local meters/Z-up. World row n=normalize(n_local inverse(A)), tangent t=project(t_local A^T perpendicular to world normal), normalized; sign gains determinant parity. Actual consumer basis K/winding/UV signs require separate witness.',
        'identity':'Use existing original head NPZ loop_vertex_indices/polygon_loop_start/total/polygon_material_slot plus native triangle_source_corners/polygon. Do not average per source vertex or compare arbitrary Unity split-vertex order.',
        'controls':'Exact native_face16 and2gaze pinned input files; 13 source FACE bridge drivers muted,37 active source correctives derive all72 Key outputs. Consumer71weights/100 are diagnostic only, never forced into source.',
        'semantics':'Custom short2 is bit-identical original at all6stages but current evaluated normal differs. Decode on current geometric fan spaces, not normal xyz blend deltas/static rotations. Frozen normal arrays are oracle evidence, not final runtime pose injection.',
        'minimal_comparison':'At same authored input record consumer source-corner correspondence+positions/normals/tangent4+UV0 and pre/postskin scope; compare per-original-CORNER normal angle and sign/handedness. Source-only large angle metrics do not select DN0/PRIMARY policy.',
        'held':'Product normal policy/PRIMARY and canonical appearance/F2/F3 remain HOLD. Historical guard FAIL artifacts remain unchanged.'}
    dump(O/'MINIMAL_CONSUMER_NORMAL_CONTRACT_PRIVATE_R1.json',contract)
    members={p.name:p for p in O.iterdir() if p.is_file()}
    for name in ['NATIVE_GUARD_RESULT_R1.json','NEW_NATIVE_APPROVAL_R1.json','FIXED_BROKER_CONFIG_R1.json','NATIVE_PAYLOAD_CONFIG_R1.json']:
        members['custody/'+name]=P/name
    for p in (P/'native-gates-r1').iterdir():members['custody/gates/'+p.name]=p
    for p in (P/'workflow').iterdir():
        if p.is_file():members['workflow/'+p.name]=p
    inputs=BASE/'o1-morph67-two-input-source-normal-proposal-r1'
    for tag in ['WORST','NEUTRAL']:members['inputs/'+tag+'_source_inputs_PRIVATE_R1.json']=inputs/(tag+'_source_inputs_PRIVATE_R1.json')
    index={n:{'bytes':p.stat().st_size,'sha256':sha(p)} for n,p in members.items()}
    dump(O/'PRIVATE_MEMBER_SHA_INDEX_R1.json',index);members['PRIVATE_MEMBER_SHA_INDEX_R1.json']=O/'PRIVATE_MEMBER_SHA_INDEX_R1.json'
    zp=BASE/'YURI_MORPH67_TWO_INPUT_NATIVE_NORMAL_REFERENCE_R1.zip';assert not zp.exists()
    with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for n,p in members.items():z.write(p,n)
    with zipfile.ZipFile(zp) as z:
        assert z.testzip() is None
        for n,m in index.items():assert hashlib.sha256(z.read(n)).hexdigest()==m['sha256']
    public={'capability_delta':'새 Windows 기능 없음; exact2input source-rest CORNER normal reference 획득',
        'new_native_guard':{'status':guard['guard_status'],'path':str(guard_path),'sha256':sha(guard_path),
            'pid':guard['pid'],'creation_FILETIME':guard['creation_FILETIME'],'parent_pid':guard['parent_pid'],
            'BEFORE':guard['BEFORE'],'AFTER':guard['AFTER'],'terminal_exit_code':0,'terminal_job':guard['terminal_job'],
            'combined_output_bytes':guard['combined_payload_output_bytes'],'wall_seconds':guard['wall_seconds'],'cleanup_errors':[]},
        'approval':{'path':str(approval),'sha256':sha(approval),'new_exact_approval':True,'historical_approval_reused':False},
        'native_launches':1,'records':rows,'native_stage_change_diagnostics':stage_pairs,
        'OFF_ALL_ARRAYS_exact':True,'OFF_full_source_component_diff':{},
        'prior_source_neutral_local_CORNER_normal_max_abs_delta':prior_delta,
        'all20_pinned_source_clone_input_script_SHA_prepost_exact':True,
        'source_SHA256':result['source_sha256'],'input_SHA256':result['input_sha256'],
        'source_Key_vs_consumer71_weight100_diagnostic':result['morph_weight_diagnostic'],
        'consumer_contract':contract,
        'private_bundle':{'path':str(zp),'bytes':zp.stat().st_size,'sha256':sha(zp),'members':len(members),'CRC_and_member_SHA_verified':True},
        'no_render_export_save_Unity':True,'guard_history':'Historical native guard FAIL preserved. New bounded run has separate strict PASS; no retroactive relabel.',
        'held':'Runtime body pose equivalence/product normal policy/PRIMARY/appearance/F2/F3 HOLD; source-only oracle handoff.'}
    dump(E/'NATIVE_TWO_INPUT_NORMAL_CUSTODY_R1.json',public)
    print(json.dumps({'private_bundle':public['private_bundle'],'stage_changes':stage_pairs,'prior_neutral_normal_delta':prior_delta,'source_SHA':result['source_sha256']}))
if __name__=='__main__':main()
