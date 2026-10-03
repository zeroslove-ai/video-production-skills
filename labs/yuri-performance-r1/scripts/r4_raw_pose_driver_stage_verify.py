"""Independent CPU readback and restricted arithmetic driver evaluation."""
import ast,hashlib,json,re
from pathlib import Path
import numpy as np
LAB=Path(__file__).resolve().parent.parent
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-raw-pose-driver-stage-reference-r1')
E=LAB/'evidence/o1-raw-pose-driver-stage-reference-r1'
assert not (OUT/'INDEPENDENT_DRIVER_READBACK.json').exists(),'Preserve verification receipt'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((OUT/'RAW_POSE_DRIVER_STAGE_MANIFEST.json').read_text(encoding='utf8'))
assert m['unique_frames']==276 and m['loop_inclusive_samples']==384 and m['source_component_diff']=={}
assert m['all137_frozen_world_pose_max_element_delta']==0 and m['source_input_bytes_unchanged']
for p,v in m['inputs'].items():assert sha(Path(p))==v['sha256'],p
for v in m['files']:assert sha(OUT/v['path'])==v['sha256']
bone_index={name:i for i,name in enumerate(m['original_body_bone_order'])}
allowed=(ast.Expression,ast.BinOp,ast.UnaryOp,ast.Call,ast.Name,ast.Load,ast.Constant,ast.Add,ast.Sub,ast.Mult,ast.Div,ast.USub,ast.UAdd)
formula=[]
for d in m['original_driver_definitions']:
    tree=ast.parse(d['expression'],mode='eval')
    assert all(isinstance(node,allowed) for node in ast.walk(tree))
    assert all(isinstance(node.func,ast.Name) and node.func.id in ('min','max') and not node.keywords for node in ast.walk(tree) if isinstance(node,ast.Call))
    variables={}
    for var in d['variables']:
        target=var['targets'][0]
        assert var['type']=='SINGLE_PROP' and target['id']==['Object','Meshy_Fitted_Rig']
        match=re.fullmatch(r'pose\.bones\["([^"\n]+)"\]\.rotation_quaternion\[(\d)\]',target['data_path'])
        assert match is not None,target
        variables[var['name']]=(bone_index[match[1]],int(match[2]))
    formula.append((m['five_factor_paths'].index(d['output_path']),compile(tree,'<frozen numeric driver>','eval'),variables))
factor_checks=[]
with np.load(OUT/'R4_All6_Raw_Pose_Quaternions_And_Five_Driver_Factors.npz',allow_pickle=False) as z:
    for c in m['clips']:
        q=z[c['array_prefix']+'_raw_quaternion_wxyz'];f=z[c['array_prefix']+'_five_driver_factors']
        assert q.shape==(c['unique_source_frames'],57,4) and f.shape==(len(q),5)
        expected=np.zeros_like(f)
        for frame,channels in enumerate(q):
            for index,code,variables in formula:
                numeric={name:float(channels[bone,axis]) for name,(bone,axis) in variables.items()}
                expected[frame,index]=eval(code,{'__builtins__':{},'min':min,'max':max},numeric)
        delta=float(np.max(np.abs(expected.astype(np.float64)-f.astype(np.float64))))
        assert delta==0,(c['clip'],delta)
        factor_checks.append({'clip':c['clip'],'raw_channel_to_driver_float32_exact':True,'max_absolute_delta':delta,
            'factor_min':f.min(axis=0).tolist(),'factor_max':f.max(axis=0).tolist(),
            'loop_samples':c['loop_inclusive_samples'],'actual_second_cycle_rechecks':c['second_cycle_actual_rechecks']})
stage_checks=[]
for v in m['files']:
    if 'seven_stages' not in v['path']:continue
    with np.load(OUT/v['path'],allow_pickle=False) as z:
        assert len(z.files)==14
        for last in range(7):
            assert z[f'stage_{last:02d}_world_position'].shape==(63561,3)
            n=z[f'stage_{last:02d}_world_corner_normal'];assert n.shape==(254602,3)
            assert np.isfinite(n).all()
            length_error=float(np.max(np.abs(np.linalg.norm(n.astype(np.float64),axis=1)-1)))
            assert length_error<1e-6
        stage_checks.append({'file':v['path'],'stage_count':7,'source_vertices':63561,'source_corners':254602})
receipt={'task_id':m['task_id'],'manifest_sha256':sha(OUT/'RAW_POSE_DRIVER_STAGE_MANIFEST.json'),
    'frozen_inputs_hashes_reverified':len(m['inputs']),'data_files_hashes_reverified':len(m['files']),
    'raw_driver_expression_policy':'AST permits numeric arithmetic and min/max only; original expressions/targets retained, no arbitrary code execution.',
    'all276_frames_all5_raw_driver_outputs_exact_float32':True,'factor_checks':factor_checks,'stage_checks':stage_checks,
    'CPU_memory_observations':{'preflight_free_physical_KiB':31311632,'total_physical_KiB':64546164,
        'job_PID':85780,'observed_job_peak_working_set_bytes':1405853696,
        'in_flight_free_physical_KiB':31134072,'after_free_physical_KiB':31976660,
        'existing_GUI_PID':129152,'GUI_not_closed':True,'job_count':1,'Blender_threads':4,
        'note':'Windows process snapshot observation; not a continuous peak profiler. PeakWorkingSet64 includes earlier peaks at observation time.'},
    'source_writes':0,'new_Blender_jobs':0}
for p in (E,OUT):(p/'INDEPENDENT_DRIVER_READBACK.json').write_text(json.dumps(receipt,indent=2),encoding='utf8')
print('INDEPENDENT_RAW_DRIVER_VERIFIED',len(factor_checks),sum(c['unique_source_frames'] for c in m['clips']),len(stage_checks))
