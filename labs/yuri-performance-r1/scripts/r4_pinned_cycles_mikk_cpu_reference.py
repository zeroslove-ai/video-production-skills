"""Frozen-input CPU native algorithm reference; never actual renderer buffers."""
from pathlib import Path
import ctypes,json,hashlib,time,os,sys
import numpy as np
LAB=Path(__file__).resolve().parent.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=Path(sys.argv[1]) if len(sys.argv)>1 else BASE/'o1-pinned-cycles-triangle-mikk-cpu-reference-r1'
assert not (OUT/'PINNED_CYCLES_TRIANGLE_MIKK_CPU_MANIFEST.json').exists() and not list(OUT.glob('*_pinned_algorithm_reference.npz')), 'Do not repeat a frozen reference' 
E=OUT if len(sys.argv)>1 else LAB/'evidence/o1-pinned-cycles-triangle-mikk-cpu-reference-r1';E.mkdir(exist_ok=True)
IN=BASE/'o1-dynamic-body-cycles-input-reference-r1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((IN/'DYNAMIC_BODY_CYCLES_INPUT_MANIFEST.json').read_text())
for path,v in manifest['inputs'].items():assert sha(Path(path))==v['sha256']
for v in manifest['files']:assert sha(IN/v['path'])==v['sha256']
source=BASE/'o1-source-fidelity-recovery-r1'
topo=np.load(source/'data/Meshy_Body_NeutralCovered_original_mesh.npz',allow_pickle=False)
rest=np.load(source/'data/Meshy_Body_NeutralCovered_corner_basis.npz',allow_pickle=False)
meta=json.loads((source/'metadata/mesh_slot_UV_attributes_shape_deltas.json').read_text())
body=next(m for m in meta if m['renderer']=='Meshy_Body_NeutralCovered')
assert not any(a['name']=='sharp_face' for a in body['attributes'])
# Source sharp_face absent defaults false: all polygon/triangle smooth flags true.
lib=ctypes.CDLL(str(OUT/'harness.dll'));compute=lib.compute_reference
P=ctypes.c_void_p;I=ctypes.c_int
compute.argtypes=[I,I,I,P,P,P,P,P,P,I,P,P,P,P];compute.restype=I
def native(d,corners,verts,raw=False):
    corners=np.ascontiguousarray(corners,dtype=np.int32)
    verts=np.ascontiguousarray(verts,dtype=np.int32)
    n=len(corners);smooth=np.ones(n,np.uint8)
    pos=np.ascontiguousarray(d['current_local_position']);norm=np.ascontiguousarray(d['current_local_corner_normal']);uv=np.ascontiguousarray(d['current_corner_UVMap'])
    packed=np.empty((n,3),np.uint32);decoded=np.empty((n,3,3),np.float32)
    tangent=np.full((n,3,3),np.nan,np.float32);sign=np.full((n,3),np.nan,np.float32)
    t=time.perf_counter()
    rc=compute(len(pos),len(norm),n,*[a.ctypes.data for a in (pos,norm,uv,verts,corners,smooth)],int(raw),*[a.ctypes.data for a in (packed,decoded,tangent,sign)])
    assert rc==0,rc
    assert np.isfinite(decoded).all() and np.isfinite(tangent).all() and np.isfinite(sign).all()
    assert np.isin(sign,[-1,1]).all()
    nl=np.linalg.norm(decoded.astype(float),axis=-1);tl=np.linalg.norm(tangent.astype(float),axis=-1)
    dot=np.sum(decoded.astype(float)*tangent.astype(float),axis=-1)
    return {'packed_normal_uint32':packed,'decoded_normal':decoded,'tangent':tangent,'sign':sign,'triangle_source_corners':corners,'triangle_source_vertices':verts,'smooth_triangle':smooth}, {'seconds':time.perf_counter()-t,'decoded_normal_unit_max_error':float(abs(nl-1).max()),'tangent_unit_max_error':float(abs(tl-1).max()),'zero_tangent_count':int((tl==0).sum()),'nonzero_tangent_unit_max_error':float(abs(tl[tl>0]-1).max()),'unit_tangent_gate':'FAIL_ZERO_TANGENTS' if np.any(tl==0) else 'PASS','decoded_normal_tangent_abs_dot_max':float(abs(dot).max()),'sign_positive':int((sign==1).sum()),'sign_negative':int((sign==-1).sum()),'finite':True,'sign_valid':True}
def angles(a,b):
    a=a.astype(float);b=b.astype(float)
    al=np.linalg.norm(a,axis=-1,keepdims=True);bl=np.linalg.norm(b,axis=-1,keepdims=True)
    a=np.divide(a,al,out=np.full_like(a,np.nan),where=al>0);b=np.divide(b,bl,out=np.full_like(b,np.nan),where=bl>0)
    return np.rad2deg(np.arctan2(np.linalg.norm(np.cross(a,b),axis=-1),np.sum(a*b,axis=-1)))
def stats(x):
    valid=x[np.isfinite(x)];return {'max':float(np.max(valid)),'mean':float(np.mean(valid)),'p99':float(np.percentile(valid,99)),'undefined_zero_vector_count':int(x.size-valid.size)}
rows=[];files=[];started=time.perf_counter()
ordered=sorted(manifest['frames'],key=lambda x:0 if x['clip']=='YRA_R4_Struggle_Strong_Loop' and x['frame']==6 else 1)
for frame in ordered:
    file=frame['file']['path'];d=np.load(IN/file,allow_pickle=False)
    corners=d['current_triangle_source_corners'];verts=d['current_triangle_source_vertices']
    primary,qa=native(d,corners,verts)
    print('CANONICAL_SANITY',json.dumps(qa),flush=True)
    assert qa['nonzero_tangent_unit_max_error']<1e-5 and qa['decoded_normal_unit_max_error']<1e-5
    raw,qraw=native(d,corners,verts,True)
    frozen,qrest=native(d,rest['loop_triangle_loops'],rest['loop_triangle_vertices'])
    primary['raw_normal_tangent']=raw['tangent'];primary['raw_normal_sign']=raw['sign']
    primary['rest_triangle_tangent']=frozen['tangent'];primary['rest_triangle_sign']=frozen['sign']
    primary['rest_triangle_source_corners']=frozen['triangle_source_corners']
    primary['rest_triangle_source_vertices']=frozen['triangle_source_vertices']
    primary['triangle_source_polygon']=d['current_triangle_source_polygon']
    primary['triangle_material_slot']=d['current_triangle_material_slot']
    # Compare only identical face-corner triples; changed faces have no equivalent row.
    old={tuple(map(int,c)):i for i,c in enumerate(frozen['triangle_source_corners'])}
    match=[(i,old[tuple(map(int,c))]) for i,c in enumerate(corners) if tuple(map(int,c)) in old]
    ii,jj=np.array(match,dtype=np.int32).T
    raw_delta=angles(primary['tangent'],raw['tangent'])
    rest_delta=angles(primary['tangent'][ii],frozen['tangent'][jj])
    raw_sign=primary['sign']!=raw['sign'];rest_sign=primary['sign'][ii]!=frozen['sign'][jj]
    normal_delta=angles(d['current_local_corner_normal'][corners],primary['decoded_normal'])
    fn=file.replace('_actual_evaluated_cycles_inputs.npz','_pinned_algorithm_reference.npz');p=OUT/fn
    assert not p.exists(),'Do not overwrite algorithm reference'
    np.savez_compressed(p,**primary)
    files.append({'path':fn,'bytes':p.stat().st_size,'sha256':sha(p)})
    row={'clip':frame['clip'],'frame':frame['frame'],'input_sha256':sha(IN/file),'canonical':qa,'raw_ablation':qraw,'rest_ablation':qrest,'packing_normal_angle_degrees':stats(normal_delta),'raw_vs_packed_tangent_angle_degrees':stats(raw_delta),'raw_vs_packed_tangent_sign_difference_count':int(raw_sign.sum()),'rest_vs_dynamic_identical_triangle_count':len(ii),'unmatched_dynamic_triangles':int(len(corners)-len(ii)),'rest_vs_dynamic_matched_tangent_angle_degrees':stats(rest_delta),'rest_vs_dynamic_matched_sign_difference_count':int(rest_sign.sum()),'rest_vs_dynamic_matched_tangent_corners_over_0_001_degree':int((rest_delta>.001).sum()),'classification':'PINNED_ALGORITHM_REFERENCE_NOT_ACTUAL_CYCLES_RENDERER_BUFFER'}
    rows.append(row);print(json.dumps(row),flush=True)
result={'task_id':'ROOT_PM_O1_PINNED_CYCLES_TRIANGLE_MIKK_CPU_REFERENCE_R1','status':'DONE_PINNED_ALGORITHM_REFERENCE','classification':'PINNED_ALGORITHM_REFERENCE','actual_Cycles_renderer_buffer':'HOLD_NOT_CAPTURED','runtime_PBR_acceptance':'HOLD','source_saved_render_export_GPU_Blender_jobs':0,'process_pid':os.getpid(),'wall_seconds':time.perf_counter()-started,'compiler':'MSVC cl.exe file version 19.44.35228.0 x64 (see actual logs)','flags':'/std:c++20 /EHsc /O2 /fp:precise /LD; default x64 SSE, no WITH_TBB, no WITH_KERNEL_AVX2; standalone configuration, not claimed identical to installed Blender build flags','source_build':'9e2066aef7ef','native_wrapper':'Unmodified MikkMeshWrapper and Triangle::compute_normal blocks extracted verbatim from pinned scene/mesh.cpp; minimal Mesh buffer facade supplies original ordered triangles/positions/smooth and UV/corner normal arrays. No renderer attribute allocator/scene compiled. RawNormalWrapper is explicitly an ablation only.','smooth_policy':'Body source sharp_face attribute absent => default false => all faces smooth; no flat normal branch reached.','input_manifest_sha256':sha(IN/'DYNAMIC_BODY_CYCLES_INPUT_MANIFEST.json'),'files':files,'frames':rows,'remaining_gate':'Actual Cycles packed/tangent buffers + Unity actual corner readback/equivalent PBR/physical Player required; no baked runtime or tolerance waiver.'}
result['compile_and_harness_files']={p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in OUT.iterdir() if p.suffix in ('.cpp','.inc','.cmd','.log','.dll','.json') and p.name not in ('PINNED_CYCLES_TRIANGLE_MIKK_CPU_MANIFEST.json','PACKET_CUSTODY.json','execution_completed.log')}
for root in (OUT,E):(root/'PINNED_CYCLES_TRIANGLE_MIKK_CPU_MANIFEST.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print('DONE_PINNED_ALGORITHM_REFERENCE',flush=True)
