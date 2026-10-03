"""Frozen-array indexing/stage analysis only. No bpy, normal recalculation or kernel run."""
from pathlib import Path
import hashlib,json,numpy as np
LAB=Path(__file__).resolve().parents[1]
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-normal-tess-domain-contract-r1';E=LAB/'evidence/o1-normal-tess-domain-contract-r1'
PM=Path(r'C:/Users/JAEWAN/projects/yuri-root-pm-r1/docs/evidence/root-pm-o1')
assert not E.exists();E.mkdir()
inputs={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(p):inputs[str(p)]={'bytes':p.stat().st_size,'sha256':sha(p)};return p
def read(p):return json.loads(record(p).read_bytes())
def arrays(p):return np.load(record(p),allow_pickle=False)
t=arrays(BASE/'o1-source-fidelity-recovery-r1/data/Meshy_Body_NeutralCovered_original_mesh.npz')
support=arrays(BASE/'o1-body-modifier-source-contract-r1/R4_Body_Original_Modifier_Support.npz')
params=read(BASE/'o1-body-modifier-source-contract-r1/BODY_MODIFIER_PARAMETERS_AND_DRIVERS.json')
metrics=read(PM/'PM_ACTUAL_FOURFRAME_DYNAMIC_TESSELLATION_REVIEW_R1.json')
ear=read(PM/'PM_WRONG_POLYGON_EAR_TRACE_CAUSAL_REVIEW_R1.json')
normal=read(PM/'PM_ACTUAL_BODY_NORMAL_FLOAT32_CORRECTION_REVIEW_R1.json')
recipe=read(BASE/'o1-native-armature-full-recipe-custody-r1/SourceBodyArmatureInput_0cd0bdd7_EXACT.json')
assert inputs[str(BASE/'o1-native-armature-full-recipe-custody-r1/SourceBodyArmatureInput_0cd0bdd7_EXACT.json')]['sha256']=='0cd0bdd70e5a6c0670846dab74e295b0a637a79f1c6d57d503611d5cf50aafe0'
raw_manifest=read(BASE/'o1-raw-pose-driver-stage-reference-r1/RAW_POSE_DRIVER_STAGE_MANIFEST.json')
raw=arrays(BASE/'o1-raw-pose-driver-stage-reference-r1/R4_All6_Raw_Pose_Quaternions_And_Five_Driver_Factors.npz')
custody=read(OUT/'PRIVATE_CONSUMER_SOURCE_CUSTODY.json')
for item in custody:assert sha(record(OUT/item['name']))==item['sha256']
native_norm=record(BASE/'o1-corner-normal-tangent-semantics-r1/upstream/mesh_normals.cc')
native_runtime=record(BASE/'o1-corner-normal-tangent-semantics-r1/upstream/mesh_runtime.cc')
body_code=record(BASE/'o1-native-armature-instrumentation-draft-r7/upstream-reference/O1SourceBodyArmature.cs')
starts,sizes,cp=t['polygon_loop_start'],t['polygon_loop_total'],t['loop_vertex_indices']
assert (len(cp),len(starts),len(t['positions']))==(254602,63781,63561)
rows=[];targets=set();stage_rows=[]
for row,trace in zip(metrics['rows'],ear['rows']):
    clip,frame=row['clip'],row['source_frame'];assert (clip,frame)==(trace['clip'],trace['source_frame'])
    p=BASE/'o1-dynamic-body-cycles-input-reference-r1'/f'{clip}_frame{frame:03d}_actual_evaluated_cycles_inputs.npz'
    d=arrays(p);assert sha(p)==row['source_sha256']
    assert np.array_equal(d['original_corner_to_source_vertex'],cp)
    slot_global=np.flatnonzero(d['current_triangle_material_slot']==0)
    known=[]
    for mismatch in row['slots'][0]['first_mismatches']:
        g=int(slot_global[mismatch['slot_row']]);poly=int(d['current_triangle_source_polygon'][g])
        # PM rows use the declared Unity handedness/winding: source [0,2,1].
        assert d['current_triangle_source_corners'][g][[0,2,1]].tolist()==mismatch['source']
        assert all(starts[poly]<=c<starts[poly]+sizes[poly] for c in mismatch['actual'])
        known.append({'slot_row':mismatch['slot_row'],'source_global_triangle':g,'polygon':poly,'polygon_size':int(sizes[poly]),'source_corner_triangle':mismatch['source'],'actual_corner_triangle':mismatch['actual']})
    polygons=[]
    for polyrow in trace['polygons']:
        poly=polyrow['polygon'];s,n=int(starts[poly]),int(sizes[poly]);assert n==5
        corners=np.arange(s,s+n,dtype=np.int32);points=cp[corners];targets.update(map(int,points))
        globals_=np.flatnonzero(d['current_triangle_source_polygon']==poly)
        polygons.append({'source_polygon':poly,'source_corner_start':s,'source_corner_count':n,'original_source_vertex_ids':points.tolist(),'source_corner_edge_ids':t['attribute_12_value'][corners].tolist(),'material_slot':int(t['polygon_material_slot'][poly]),'current_source_triangle_rows':globals_.tolist(),'current_original_corner_triangles':d['current_triangle_source_corners'][globals_].tolist(),'source_custom_short2_sha256':hashlib.sha256(d['original_custom_normal_short2'][corners].tobytes()).hexdigest(),'PM_measured_local_delta_max_m':polyrow['local_delta_max_m'],'initial_signs_actual':polyrow['initial_signs_actual'],'initial_signs_source':polyrow['initial_signs_source'],'first_reported_trace_divergence':polyrow['first_reported_trace_divergence']})
    selected=np.unique(np.concatenate([np.array(x['original_source_vertex_ids']) for x in polygons]))
    clipmeta=next(x for x in raw_manifest['clips'] if x['clip']==clip)
    factors=raw[clipmeta['array_prefix']+'_five_driver_factors'][frame-1]
    assert np.array_equal(factors[1:],np.zeros(4,np.float32))
    group52=np.array(support['raw_nonbone_group_weights'][selected,1]);group53=np.array(support['raw_nonbone_group_weights'][selected,2])
    contract={'clip':clip,'source_frame':frame,'actual_triangle_mismatch_rows':row['slots'][0]['mismatched_rows'],'known_first_rows_mapped':known,'PM_trace_polygon_instances':polygons,'population_scope':'PM first_mismatches and 12 focused ear-trace instances only; not exhaustive actual mismatched-row inventory','normal_max_deg':row['normal_max_deg'],'normal_corners_above_unchanged_gate':row['normals_over_0_001_deg'],'normal_gate_deg':0.001,'UV_exact':row['UV_exact'],'slots1_2_exact':all(x['mismatched_rows']==0 for x in row['slots'][1:]),'raw_five_driver_factors':factors.tolist(),'selected_vertices':selected.tolist(),'selected_mask52_positive':int(np.count_nonzero(group52)),'selected_corrective_mask53_positive':int(np.count_nonzero(group53)),'corrective_output_inactive_for_targets':bool(factors[0]==0 or not np.any(group53)),'ordinary_smooth_four_factors_exact_zero':True}
    rows.append(contract)
    stagepath=BASE/'o1-raw-pose-driver-stage-reference-r1'/f'{clip}_frame{frame:03d}_seven_stages.npz'
    if stagepath.exists():
        st=arrays(stagepath);changes=[]
        for stage in range(1,7):
            a,b=st[f'stage_{stage-1:02d}_world_position'],st[f'stage_{stage:02d}_world_position']
            changed=np.any(a[selected].view(np.uint32)!=b[selected].view(np.uint32),axis=1)
            changes.append({'from_stage':stage-1,'to_stage':stage,'target_changed_vertices':int(changed.sum()),'target_max_world_position_delta_m':float(np.linalg.norm(a[selected].astype(float)-b[selected].astype(float),axis=1).max()),'whole_mesh_changed_vertices':int(np.any(a.view(np.uint32)!=b.view(np.uint32),axis=1).sum())})
        same=np.array_equal(st['stage_06_world_position'],d['current_world_position'])
        stage_rows.append({'clip':clip,'source_frame':frame,'target_vertices':selected.tolist(),'source_world_stage_changes':changes,'stage06_world_positions_equal_dynamic_reference':same,'all_target_source_stage0_to6_world_bits_equal':bool(np.array_equal(st['stage_00_world_position'][selected].view(np.uint32),st['stage_06_world_position'][selected].view(np.uint32))),'arrays_domain':'WORLD f32 only; no source-local intermediate arrays in this existing dataset','normal_arrays_domain':'actual source CORNER WORLD f32; not recomputed','consumer_matching_seven_stage_arrays_available_here':False})
    else:stage_rows.append({'clip':clip,'source_frame':frame,'seven_stage_source_reference':'NOT_PRESENT; final local source reference and raw driver factors are present'})
targets=sorted(targets)
csr=[]
for v in targets:
    a,b=recipe['offsets'][v:v+2]
    csr.append({'source_vertex':v,'original_ordered_CSR_start':a,'original_ordered_CSR_end':b,'entries':b-a,'zero_weight_entries':sum(w==0 for w in recipe['weights'][a:b]),'original_mapping_recipe_sha256':'0cd0bdd70e5a6c0670846dab74e295b0a637a79f1c6d57d503611d5cf50aafe0'})
edges=t['edge_vertex_indices'];sorted_edges=np.sort(edges,axis=1)
duplicate_endpoint_rows=len(edges)-len(np.unique(sorted_edges,axis=0))
result={'status':'READONLY_DOMAIN_AND_STAGE_CONTRACT_NO_RUNTIME_FIX','inputs':inputs,'four_actual_runtime_failures':rows,'source_stage_analysis':stage_rows,'focused_target_source_vertices':targets,'target_ordered_CSR_ranges':csr,'focused_targets_overlap_existing_R7_five_vertices':sorted(set(targets)&{11189,14918,21485,22227,40817}),'original_parallel_edge_endpoint_duplicate_rows':duplicate_endpoint_rows,'earliest_proven_divergence':'Actual final SOURCE_LOCAL position inputs already differ from Blender reference before normal/tessellation. Initial ear convex/concave signs differ at trace0. Exact first upstream comparative modifier stage unproved: actual consumer seven-stage arrays not present.','normal_same_local_evidence':[{'clip':x['clip'],'source_frame':x['source_frame'],'actual_source_error_deg':x['mesh_readback_normal_max_deg'],'same_local_CSharp_vs_independent_deg':x['same_local_CSharp_vs_independent_max_deg']} for x in normal['PM_independent_actual_mesh_readback']],'missing_evidence':['Full actual 27 wrong triangle rows plus corner-normal error IDs/readback: only 20 first rows available in PM four-frame receipt','Consumer DiagnosticStageObserver local/rendered outputs stage0..6 for Startle11/Strong6; existing source stage world arrays must use explicit instance/P mapping','Source-local f32 stage0..6 native intermediate coordinates unavailable; inverting already-rounded WORLD f32 loses local ULP provenance','Native corner-tris cache dirty/with-normals branch and actual projection/ear-sweep trace not captured','Exact native normalization/compiler operation trace before claiming remaining same-input differences explained','Normal max-error CORNER/fan IDs for all four samples, complete original-edge adjacency/fan traversal and any source-local face/corner outputs'],'operator_contract':{'geometry':'Original63561 basis + exact57 rest/pose + full ordered304799CSR -> source-local DQ(stage0) -> cached-original masked LBS(stage1) -> original-edge ORCO corrective(stage2) -> four Smooth(stage3..6); never canonical rest fit/prune/normalize influences','normal':'Source-local current positions + original polygon/corner/edge topology + sharp attrs + signed CORNER short2 -> true Newell face normals -> ordered original-edge smooth fans -> fan space + signed averaged short2 decode -> local CORNER normals -> inverse-transpose world once; no triangle normal recalculation','tessellation':'Same source-local current positions + original polygon/corner indices -> exact native dirty/with-face-normals cache route -> triangle/quad/ngon projection + float32 sign/ear sweep -> original CORNER triangles -> material slot partition + P winding reversal once','static_native_terms_not_recorded_by_current_portable_tess':'Cached mesh runtime can use corner_tris_calc_with_normals(face_normals()) instead of recomputing Newell projection; short2 Face normals may average decoded CORNER values; actual cached branch pending, not asserted cause','acceptance':'unchanged normal0.001deg, exact topology/CSR order/triangle identities, actual renderer readback, no source substitution/epsilon/approx normals'},'source_R5_identity_accepted_scope_only':True,'native_numeric_acceptance':False,'visual_PBR_PRIMARY_promotion':False,'Blender_render_build_trace_download_jobs_in_this_analysis':0}
for name,value in [('NORMAL_TESS_DOMAIN_CONTRACT_R1.json',result),('PRIVATE_SOURCE_CUSTODY_RECEIPT.json',custody)]:
    (E/name).write_text(json.dumps(value,indent=2),encoding='utf8')
print(json.dumps({'domain_polygons':[x['source_polygon'] for r in rows for x in r['PM_trace_polygon_instances']],'target_vertices':len(targets),'known_actual_triangle_rows':sum(len(r['known_first_rows_mapped']) for r in rows),'stage_rows':stage_rows,'evidence':str(E)}))
