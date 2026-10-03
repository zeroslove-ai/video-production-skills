"""Recover metadata after JSON NumPy-int failure without another Blender job.
Validate persisted actual inputs against frozen references, never regenerate them.
"""
import json,hashlib,gzip
from pathlib import Path
import numpy as np
LAB=Path(__file__).resolve().parent.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-dynamic-body-cycles-input-reference-r1';E=LAB/'evidence/o1-dynamic-body-cycles-input-reference-r1'
assert not (OUT/'DYNAMIC_BODY_CYCLES_INPUT_MANIFEST.json').exists(),'Preserve recovered manifest'
R=BASE/'o1-source-fidelity-recovery-r1';N=BASE/'o1-native-unity-probe-r1';FULL=BASE/'o1-full-body-deformation-reference-r1'
inputs={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(p):inputs[str(p)]={'sha256':sha(p),'bytes':p.stat().st_size};return p
def load(p):return json.loads(record(p).read_text(encoding='utf8'))
def write(n,v):
    for p in (OUT,E):(p/n).write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf8')
source=record(LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend')
library=record(BASE/'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend')
assert sha(source)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
assert sha(library)=='6874ec69d5721f385d31edaa06ef0d58c89a543b98bacd961f8f575ff57eef4d'
diff=load(OUT/'SOURCE_COMPONENT_DIFF.json');assert diff['differences']=={} and diff['before']==diff['after']
full=load(FULL/'FULL_BODY_DEFORMATION_MANIFEST.json')
meta=next(x for x in load(R/'metadata/mesh_slot_UV_attributes_shape_deltas.json') if x['renderer']=='Meshy_Body_NeutralCovered')
original=np.load(record(R/'data/Meshy_Body_NeutralCovered_original_mesh.npz'),allow_pickle=False)
rest=np.load(record(R/'data/Meshy_Body_NeutralCovered_corner_basis.npz'),allow_pickle=False)
record(N/'metadata/source_expanded_rigs.json');record(N/'reference/native_evaluated_all_frames.json.gz')
rawmanifest=load(BASE/'o1-raw-pose-driver-stage-reference-r1/RAW_POSE_DRIVER_STAGE_MANIFEST.json')
raw=np.load(record(BASE/'o1-raw-pose-driver-stage-reference-r1/R4_All6_Raw_Pose_Quaternions_And_Five_Driver_Factors.npz'),allow_pickle=False)
rows=[];files=[]
cases=[('YRA_R4_Startle_Short',1),('YRA_R4_Startle_Short',11),('YRA_R4_Struggle_Strong_Loop',6),('YRA_R4_Struggle_Strong_Loop',44)]
for clip,frame in cases:
    p=OUT/f'{clip}_frame{frame:03d}_actual_evaluated_cycles_inputs.npz';assert p.exists()
    with np.load(p,allow_pickle=False) as z:
        arrays={k:z[k] for k in z.files}
        assert all(np.isfinite(a).all() for a in arrays.values())
        assert len(arrays)==13
        assert np.array_equal(arrays['current_corner_UVMap'],original['uv_0'])
        assert np.array_equal(arrays['original_custom_normal_short2'].astype(np.int32),original['attribute_13_value'])
        assert np.array_equal(arrays['original_corner_to_source_vertex'],original['loop_vertex_indices'])
        assert np.array_equal(arrays['source_vertex_id'],np.arange(63561))
        tc=arrays['current_triangle_source_corners'];tp=arrays['current_triangle_source_polygon'];tv=arrays['current_triangle_source_vertices']
        assert np.array_equal(tv,original['loop_vertex_indices'][tc])
        corner_polygon=np.repeat(np.arange(len(original['polygon_loop_total'])),original['polygon_loop_total'])
        assert np.array_equal(corner_polygon[tc],np.repeat(tp[:,None],3,axis=1))
        assert np.array_equal(arrays['current_triangle_material_slot'],original['polygon_material_slot'][tp])
        chunk=next(c for c in full['chunks'] if c['clip']==clip and frame in c['source_frames'])
        reference=record(FULL/chunk['path']);assert sha(reference)==chunk['sha256']
        with np.load(reference,allow_pickle=False) as frozen:
            ix=chunk['source_frames'].index(frame)
            errors={field:float(np.max(np.abs(arrays['current_'+field]-frozen[field][ix]))) for field in ('local_position','world_position','local_corner_normal','world_corner_normal')}
            assert all(v==0 for v in errors.values())
        assert np.array_equal(tp,rest['triangle_polygon_index']) and tc.shape==rest['loop_triangle_loops'].shape
        changed=np.any(tc!=rest['loop_triangle_loops'],axis=1);changed_poly=np.unique(tp[changed]);diagonal=[];order=[]
        for pi in changed_poly:
            mask=tp==pi
            a=sorted(tuple(sorted(v)) for v in tc[mask].tolist())
            b=sorted(tuple(sorted(v)) for v in rest['loop_triangle_loops'][mask].tolist())
            (diagonal if a!=b else order).append(int(pi))
        sizes=original['polygon_loop_total']
        stats={'triangle_rows_different_from_rest':int(changed.sum()),'polygons_with_different_rows':len(changed_poly),
            'corner_set_topology_changed_polygons':len(diagonal),'triangle_order_or_winding_only_polygons':len(order),
            'quad_diagonal_changed_polygons':int(sum(sizes[i]==4 for i in diagonal)),
            'ngon_triangulation_changed_polygons':int(sum(sizes[i]>4 for i in diagonal)),
            'changed_source_polygon_ids':diagonal,'order_only_source_polygon_ids':order}
        file={'path':p.name,'sha256':sha(p),'bytes':p.stat().st_size,'uncompressed_bytes':sum(a.nbytes for a in arrays.values()),
            'arrays':{k:{'shape':list(a.shape),'dtype':str(a.dtype)} for k,a in arrays.items()}}
        files.append(file)
        prior=next(c for c in rawmanifest['clips'] if c['clip']==clip)
        q=raw[prior['array_prefix']+'_raw_quaternion_wxyz'][frame-1]
        factors=raw[prior['array_prefix']+'_five_driver_factors'][frame-1]
        rows.append({'clip':clip,'frame':frame,'authored_seconds':(frame-1)/24,'Action':clip,'action_slot':'OBMeshy_Fitted_Rig',
            'file':file,'triangles':len(tc),'full_body_reference_exact_deltas':errors,'reference_chunk':chunk['path'],
            'reference_chunk_sha256':chunk['sha256'],'rest_triangulation_comparison':stats,
            'original_packed_custom_normal_unchanged':True,'original_UV_and_source_corner_route_exact':True,
            'prior_frozen_raw_quaternion_wxyz':q.tolist(),'prior_frozen_five_factors':factors.tolist(),
            'raw_property_provenance':'Reused actual prior 424517b raw capture, not recovered from current triangles or presented as newly persisted current-job raw pose rows.',
            'not_actual_Cycles_renderer_buffer':True})
compiler=Path(r'C:/Program Files (x86)/Microsoft Visual Studio/2022/BuildTools/VC/Tools/MSVC/14.44.35207/bin/Hostx64/x64/cl.exe')
assert compiler.exists();record(compiler)
manifest={'task_id':'ROOT_PM_O1_DYNAMIC_BODY_CYCLES_INPUT_REFERENCE_R1','status':'DONE_EVALUATED_INPUT_REFERENCE_JSON_RECOVERED_ACTUAL_CYCLES_BUFFER_HOLD',
    'inputs':inputs,'source_component_diff':{},'source_input_bytes_unchanged':True,
    'preservation_evidence':'Original one-job code reached SOURCE_COMPONENT_DIFF={} and all frozen SHA checks before the final manifest JSON int64 exception. Recovery independently rehashes master/library, validates persisted arrays and identical before/after fingerprints.',
    'original_Actions_preserved':len(diff['before']['actions']),'original137_rest_and_hierarchy_preserved':diff['before']['rest_pose_settings']==diff['after']['rest_pose_settings'],
    'muted13_bridge_contract':'Original job explicitly asserted13 source bridge mute flags before load of two reaction Actions and again before manifest write; source object/driver fingerprints match on OFF return.',
    'all137_world_pose_validation':'Original four-frame job asserted zero element delta against native_evaluated_all_frames at every frame before each NPZ write; raw current-job matrix rows were not persisted.',
    'source_saved':False,'export_render_GPU_tasks':0,'existing_GUI_touched':False,
    'coordinate_policy':'Actual evaluated local geometry and Blender world meters Z-up; row normal normalized with inverse object linear; original source corner/polygon/control-point IDs, no Unity basis conversion.',
    'frames':rows,'files':files,'job_log':{'exec_session_id':12455,'job_count':1,'threads':4,'Blender':'5.2.1 LTS','build_hash':'9e2066aef7ef',
        'pid':135608,'pid_provenance':'Root PM message ROOT_PM_DYNAMIC_INPUT_OBSERVATION independently observed CPU PID135608, then process absent; supplied in this task after metadata recovery. Original job script did not persist PID before its final JSON failure.',
        'wall_seconds':None,'missing_metadata_reason':'Original wall time was held in final manifest object which failed serialization; not recoverable from saved stdout. No duration fabricated and no second Blender job launched.',
        'preflight_free_physical_KiB':32017120,'total_physical_KiB':64546164,'after_free_physical_KiB':31780916,
        'GUI_PID_before_after':129152,'source_process_cleanup':'Blender quit; subsequent process inventory contains existing GUI only.'},
    'failure_correction':{'error':'TypeError: Object of type int64 is not JSON serializable at final manifest write',
        'cause':'sum over NumPy boolean polygon-size comparisons yielded np.int64',
        'script_fix':'Cast quad/ngon counts to Python int; no source job repeated.',
        'recovery':'This plain-Python validator reconstructs metadata from intact four actual NPZ + completed source fingerprint receipt; validates hashes/mappings/references.'},
    'Cycles_reference_feasibility':{'compiler':str(compiler),'compiler_on_initial_PATH':False,'found_by':'vswhere VC.Tools.x86.x64',
        'unmodified_Mikk_headers':['mikktspace.hh','mikk_atomic_hash_set.hh','mikk_float3.hh','mikk_util.hh'],
        'normal_packing_source':'Pinned Cycles util/types_normal.h, packed_normal uint32 encode/decode before triangle Mikk input',
        'remaining_native_compile_dependencies':['Pinned util/defines.h, util/math_float3.h, util/math_int4.h and their exact transitive type/math headers',
            'MSVC vcvars64/Windows SDK compiler environment and matching CPU/FP build definitions',
            'Exact Cycles triangle/smooth/corner-normal packed attribute wrapper and optimization configuration'],
        'assessment':'A separately compiled pinned algorithm reference is feasible with discovered MSVC, but full exact dependency/configuration assembly was not performed. No handport or substitute normal/tangent output generated.',
        'native_API_gap':'No inspected Blender Python API exposes current Cycles Mesh::update_tangents packed-normal/tangent attribute buffers; actual renderer proof needs separately authorized native Cycles buffer instrumentation/export hook, not RNA calc_tangents.'},
    'scope_limit':'Four actual Blender-evaluated inputs only; full-body chunks used as identity/position/normal QA references, not triangle runtime input. No Cycles packed normal/tangent or shader result captured.',
    'runtime_tangent_PBR_verdict':'HOLD'}
assert manifest['original_Actions_preserved']==78
write('DYNAMIC_BODY_CYCLES_INPUT_MANIFEST.json',manifest)
print('DYNAMIC_METADATA_RECOVERED',len(rows),sum(v['bytes'] for v in files))
