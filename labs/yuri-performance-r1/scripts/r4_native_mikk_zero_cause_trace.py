"""Diagnostic native fork, four immutable inputs; strict baseline equivalence."""
from pathlib import Path
import ctypes,json,hashlib,time,os,sys
import numpy as np
LAB=Path(__file__).resolve().parent.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
ALG=BASE/'o1-pinned-cycles-triangle-mikk-cpu-reference-r1'
IN=BASE/'o1-dynamic-body-cycles-input-reference-r1'
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else BASE/'o1-native-mikk-zero-cause-trace-r1'
E=OUT if len(sys.argv)>1 else LAB/'evidence/o1-native-mikk-zero-cause-trace-r1';E.mkdir(exist_ok=True)
assert not (OUT/'NATIVE_MIKK_ZERO_CAUSE_MANIFEST.json').exists()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((ALG/'PINNED_CYCLES_TRIANGLE_MIKK_CPU_MANIFEST.json').read_text())
im=json.loads((IN/'DYNAMIC_BODY_CYCLES_INPUT_MANIFEST.json').read_text())
preserved={str(p):sha(p) for p in ALG.rglob('*') if p.is_file()}
preserved.update({p:v['sha256'] for p,v in im['inputs'].items()})
for p,v in preserved.items():assert sha(Path(p))==v
for v in im['files']:assert sha(IN/v['path'])==v['sha256']
lib=ctypes.CDLL(str(OUT/'harness.dll'));P=ctypes.c_void_p;I=ctypes.c_int
compute=lib.compute_reference;compute.argtypes=[I,I,I,P,P,P,P,P,P,I,P,P,P,P];compute.restype=I
lib.begin_trace.argtypes=[ctypes.c_char_p,P,I];lib.begin_trace.restype=I
lib.end_trace.argtypes=[];lib.end_trace.restype=None
rows=[];files=[];started=time.perf_counter()
for row in m['frames']:
    f=next(v['path'] for v in m['files'] if row['clip'] in v['path'] and ('frame%03d'%row['frame']) in v['path'])
    baseline=np.load(ALG/f,allow_pickle=False)
    orig=next(v['file']['path'] for v in im['frames'] if v['clip']==row['clip'] and v['frame']==row['frame'])
    d=np.load(IN/orig,allow_pickle=False)
    zeros=np.argwhere(np.linalg.norm(baseline['tangent'].astype(float),axis=-1)==0)
    zeros=np.ascontiguousarray(zeros,dtype=np.uint32)
    prefix=row['clip']+'_frame%03d'%row['frame'];log=OUT/(prefix+'_events.jsonl')
    outnpz=OUT/(prefix+'_diagnostic_canonical.npz')
    corners=d['current_triangle_source_corners'];verts=d['current_triangle_source_vertices']
    if outnpz.exists():
        saved=np.load(outnpz,allow_pickle=False)
        packed=saved['packed_normal_uint32'];decoded=saved['decoded_normal'];tangent=saved['tangent'];sign=saved['sign']
        equivalence={k:bool(np.array_equal(a,baseline[k])) for k,a in [('packed_normal_uint32',packed),('decoded_normal',decoded),('tangent',tangent),('sign',sign)]}
        assert all(equivalence.values())
        print('RESUME_SAVED_NATIVE_OUTPUT',prefix,flush=True)
    else:
        assert not log.exists()
        assert lib.begin_trace(str(log).encode(),zeros.ctypes.data,len(zeros))==0
        corners=d['current_triangle_source_corners'];verts=d['current_triangle_source_vertices'];nt=len(corners)
        smooth=np.ones(nt,np.uint8)
        packed=np.empty((nt,3),np.uint32);decoded=np.empty((nt,3,3),np.float32)
        tangent=np.full((nt,3,3),np.nan,np.float32);sign=np.full((nt,3),np.nan,np.float32)
        position=d['current_local_position'];normal=d['current_local_corner_normal'];uv=d['current_corner_UVMap']
        rc=compute(len(position),len(normal),nt,
            *[a.ctypes.data for a in (position,normal,uv,verts,corners,smooth)],0,
            *[a.ctypes.data for a in (packed,decoded,tangent,sign)])
        lib.end_trace();assert rc==0
        equivalence={k:bool(np.array_equal(a,baseline[k])) for k,a in [('packed_normal_uint32',packed),('decoded_normal',decoded),('tangent',tangent),('sign',sign)]}
        assert all(equivalence.values()),equivalence
        outnpz=OUT/(prefix+'_diagnostic_canonical.npz');assert not outnpz.exists()
        np.savez_compressed(outnpz,packed_normal_uint32=packed,decoded_normal=decoded,tangent=tangent,sign=sign,triangle_source_corners=corners,triangle_source_vertices=verts,triangle_source_polygon=d['current_triangle_source_polygon'],triangle_material_slot=d['current_triangle_material_slot'])
    events=[json.loads(line) for line in log.read_text().splitlines()]
    for ev in events:
        if 'face' in ev:
            t=ev['face'];ev['source_polygon']=int(d['current_triangle_source_polygon'][t]);ev['material_slot']=int(d['current_triangle_material_slot'][t]);ev['source_triangle_corners']=corners[t].tolist();ev['source_triangle_vertices']=verts[t].tolist()
            if 'corner' in ev:
                j=ev['corner'];c=int(corners[t,j]);ev['source_corner']=c;ev['source_vertex']=int(verts[t,j]);ev['packed_normal_uint32']=int(packed[t,j]);ev['source_raw_corner_normal']=d['current_local_corner_normal'][c].tolist();ev['source_decoded_normal']=decoded[t,j].tolist()
                if ev['event']=='contribution':assert np.array_equal(np.array(ev['normal'],np.float32),decoded[t,j])
    details=[]
    for t,j in zeros:
        match=[ev for ev in events if ev['event']=='assign' and ev['face']==int(t) and ev['corner']==int(j)]
        assert len(match)==1,match
        target=match[0];g=target['group'];contrib=[ev for ev in events if ev['event']=='contribution' and ev['group']==g]
        pre=[ev for ev in events if ev['event']=='pre_normalize' and ev['group']==g];post=[ev for ev in events if ev['event']=='post_normalize' and ev['group']==g]
        assert len(pre)==len(post)==1
        assert np.array_equal(pre[0]['tangent'],[0,0,0]) and np.array_equal(post[0]['tangent'],[0,0,0])
        nonzero=sum(np.linalg.norm(ev['contribution'])>0 for ev in contrib)
        angle_zero=sum(ev['fast_acos_angle']==0 for ev in contrib)
        projection_zero=sum(np.linalg.norm(ev['projected_tangent'])==0 for ev in contrib)
        cause='ALL_CONTRIBUTIONS_ZERO_ANGLE' if contrib and angle_zero==len(contrib) and projection_zero==0 else 'NONZERO_CONTRIBUTIONS_CANCEL' if nonzero>0 else 'ZERO_PROJECTION_OR_NO_CONTRIBUTION_REVIEW'
        details.append({'target':target,'group_contribution_count':len(contrib),'nonzero_contribution_count':int(nonzero),'zero_angle_count':angle_zero,'zero_projection_count':int(projection_zero),'group_sum_before_normalize':pre[0]['tangent'],'group_after_normalize':post[0]['tangent'],'observed_cause':cause,'contributions':contrib})
    enriched=OUT/(prefix+'_source_linked_trace.json');enriched.write_text(json.dumps({'events':events,'canonical_zero_details':details},indent=2))
    rows.append({'clip':row['clip'],'frame':row['frame'],'canonical_zero_count':len(zeros),'bitwise_output_equivalence':equivalence,'cause_counts':{c:sum(v['observed_cause']==c for v in details) for c in sorted({v['observed_cause'] for v in details})},'target_details':details})
    for p in (log,enriched,outnpz):files.append({'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)})
    print('CASE',row['clip'],row['frame'],rows[-1]['cause_counts'],flush=True)
for p,v in preserved.items():assert sha(Path(p))==v
for p in OUT.rglob('*'):
    if p.is_file() and (p.suffix in ('.cpp','.h','.hh','.inc','.cmd','.dll','.log','.diff','.txt') or p.name=='download_receipt.json') and p.name!='execution.log':files.append({'path':str(p.relative_to(OUT)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)})
result={'task_id':'ROOT_PM_O1_NATIVE_MIKK_ZERO_CAUSE_TRACE_R1','status':'DONE_DIAGNOSTIC_NATIVE_ALGORITHM_TRACE','classification':'INSTRUMENTED_PINNED_ALGORITHM_NOT_ACTUAL_CYCLES_RENDERER_BUFFER','all_tangent_unit_gate':'FAIL_UNCHANGED_24_CANONICAL_ZEROS','runtime_Cycles_PBR':'HOLD','original_CORNER_normal_0_001_degree_gate':'UNCHANGED','source_Blender_render_GPU_Unity_save_jobs':0,'process_pid':os.getpid(),'wall_seconds':time.perf_counter()-started,'compiler_flags':'Same original /std:c++20 /EHsc /O2 /fp:precise /LD x64 serial Mikk; separate diagnostic header with read-only observers','original_reference_files_preserved':preserved,'files':files,'frames':rows}
for root in (OUT,E):(root/'NATIVE_MIKK_ZERO_CAUSE_MANIFEST.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print('DONE_DIAGNOSTIC_NATIVE_ALGORITHM_TRACE',flush=True)
