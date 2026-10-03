"""Independent file-only audit; no bpy/process launch. Use only after actual capture."""
from pathlib import Path
import gzip,hashlib,json
OUT=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-original-idle-sampling-r3')
def main():
    load=lambda n:json.loads((OUT/n).read_bytes())
    scene=load('SCENE_SIGNATURE_BEFORE_AFTER.json')
    assert scene['before']==scene['after'] and scene['differences']=={}
    on=load('ON_SOURCE_SIGNATURE_R1.json')
    raw_phases={}
    for phase,sig in [('BEFORE',scene['before']),('ON',on),('AFTER',scene['after'])]:
        with gzip.open(OUT/f'RAW_FINGERPRINT_INPUTS_{phase}_PRIVATE_R3.json.gz','rt') as f:raw_phases[phase]=json.load(f)
        raw=raw_phases[phase]
        for category in ['objects','mesh_attributes']:
            hashes={name:hashlib.sha256(json.dumps(payload,separators=(',',':')).encode()).hexdigest() for name,payload in raw[category].items()}
            assert hashes==sig[category],('raw recomputation',phase,category)
        proof=load(f'RAW_RECOMPUTED_HASHES_{phase}_R3.json')
        assert all(proof['exact_original_signature_matches'].values())
    assert raw_phases['BEFORE']==raw_phases['AFTER']
    raw_phases.clear()
    verdict=load('FORENSIC_RESTORATION_VERDICT_R3.json')
    assert not verdict['full_signature_differences'] and verdict['raw_difference_count']==0 and not verdict['ledger_error_indices'] and verdict['driver_NLA_same']
    assert load('RAW_FIELD_DIFF_PATHS_R3.json')['difference_count']==0
    with gzip.open(OUT/'RAW_FIELD_DIFF_PRIVATE_R3.json.gz','rt') as f:assert json.load(f)==[]
    structural=load('STRUCTURAL_OFF_ON_OFF_R1.json');restored=load('STRUCTURAL_RESTORED_R1.json')
    assert structural['before']==structural['on']==restored['after']
    for category in ['meshes_shape_keys_weights','rest_rigs','actions','rest_pose_settings','materials','node_groups','textures','worlds']:
        assert category in scene['before'],category
        assert on[category]==scene['before'][category],category
    result=load('IDLE_SAMPLING_RESULT_R3.json');job=load('OWNED_JOB_RESULT_R1.json')
    assert job['guard_status']=='PASS_OWNED_JOB_EXIT_ZERO_DRAINED'
    assert job['terminal_owned_handle_exit_code']==0 and job['terminal_job_accounting']['active']==0 and job['terminal_job_pids']==[] and not job['cleanup_errors']
    custody=load('TERMINAL_FILE_CUSTODY_R3.json')
    assert custody['status']=='FINAL_CLOSED_LOG_AND_JOB_RECEIPT'
    assert {'fixed-capture.log','OWNED_JOB_RESULT_R1.json','IDLE_SAMPLING_RESULT_R3.json'} <= set(custody['files'])
    assert 'TERMINAL_FILE_CUSTODY_R3.json' not in custody['files']
    for name,receipt in custody['files'].items():
        p=OUT/name
        assert p.stat().st_size==receipt['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==receipt['sha256']
    assert 'fixed-capture.log' not in result['files'] and 'OWNED_JOB_RESULT_R1.json' not in result['files']
    assert 'TERMINAL_FILE_CUSTODY_R3.json' not in result['files']
    for name,row in result['files'].items():
        h=hashlib.sha256()
        with (OUT/name).open('rb') as f:
            for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
        assert h.hexdigest()==row['sha256']
    count=0;offset=0;static={};channels=None
    with gzip.open(OUT/'FRAMES_PRIVATE_R1.jsonl.gz','rt') as frames,gzip.open(OUT/'ALL_MESH_NATIVE_LOCAL_F32_PRIVATE_R1.bin.gz','rb') as geometry:
        for line in frames:
            row=json.loads(line);count+=1
            assert row['frame']==count and len(row['domains'])==4
            assert [len(d['channels']) for d in row['domains']]==[364,16,2,4]
            assert sum(len(r['bones']) for r in row['rigs'])==137
            assert len(next(r for r in row['rigs'] if r['object']=='Meshy_Fitted_Rig')['bones'])==57
            assert len(next(r for r in row['rigs'] if r['object']=='Hair_Rig_R4')['bones'])==10
            assert len([d for d in row['drivers'] if d['owner']=='Hair_Rig_R4'])==14
            assert sum(bool(d['mute']) for d in row['drivers'])==13
            values=[c['evaluated_RNA'] for d in row['domains'] for c in d['channels']]
            if channels is None:channels=values;static={i:True for i in range(len(values))}
            else:
                for i,v in enumerate(values):static[i]=static[i] and v==channels[i]
            for g in row['geometry']:
                assert g['offset_uncompressed_bytes']==offset
                data=geometry.read(g['bytes']);assert len(data)==g['bytes'] and hashlib.sha256(data).hexdigest()==g['sha256']
                offset+=len(data)
        assert geometry.read(1)==b''
    assert count==145 and offset==result['geometry_uncompressed_bytes']
    print(json.dumps({'status':'FILE_CUSTODY_AND_OFF_ON_OFF_AUDIT_PASS_NOT_VISUAL_OR_LOOP_PASS','frames':count,'static_evaluated_channels':[i for i,v in static.items() if v],'geometry_bytes':offset}))
if __name__=='__main__':main()
