"""Existing saved data/operator-source review only; no bpy/replay/capture."""
from pathlib import Path
import hashlib,json,zipfile
import numpy as np

LAB=Path(__file__).resolve().parent.parent
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
DATA=BASE/'o1-exact-source-local-stage-capture-r2'
OLD=BASE/'o1-raw-pose-driver-stage-reference-r1'
PM=Path('C:/Users/JAEWAN/projects/yuri-root-pm-r1/docs/evidence/root-pm-o1')
E=LAB/'evidence/o1-source-pose-matrix-input-boundary-r1'

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def ah(a):return hashlib.sha256(a.tobytes(order='C')).hexdigest()
def write(n,v):
    with (E/n).open('x',encoding='utf8') as f:json.dump(v,f,indent=2)

def main():
    assert not E.exists(),'Immutable new analysis only'
    inputs={}
    def record(p):inputs[str(p)]={'bytes':p.stat().st_size,'sha256':sha(p)};return p
    def load(p):return json.loads(record(p).read_bytes())
    current=load(DATA/'CAPTURE_RESULT_R1.json')
    old_manifest=load(OLD/'RAW_POSE_DRIVER_STAGE_MANIFEST.json')
    recipe=load(BASE/'o1-native-armature-full-recipe-custody-r1/SourceBodyArmatureInput_0cd0bdd7_EXACT.json')
    expanded=load(BASE/'o1-native-unity-probe-r1/metadata/source_expanded_rigs.json')
    old_raw=np.load(record(OLD/'R4_All6_Raw_Pose_Quaternions_And_Five_Driver_Factors.npz'),allow_pickle=False)
    transferred=load(PM/'PM_PAIRED43_VISIBLE_QUALITY_AND_ACTUAL_LOCAL_R2_LAPTOP_CUSTODY_R1.json')['Laptop_transfer']
    assert transferred['sha256']=='41798f214f1b5a67c78765c42e9d82d3763157e85da0dca9c81964db10cdbedf'
    assert transferred['ZIP_CRC_member_validation']['both_exact_declared_size_SHA']
    record(PM/'PM_TWOFRAME_STAGE_AND_POSE_BOUNDARY_REVIEW_R1.json')
    record(PM/'PM_POSE_AB_INPUT_PROVENANCE_REVIEW_R1.json')
    record(PM/'PM_POSE_INPUT_AB_RECOMPUTE_R1.json')
    upstream=BASE/'o1-native-armature-instrumentation-draft-r7/upstream/source/blender/blenkernel/intern'
    for p in [upstream/'armature_update.cc',upstream/'armature_deform.cc',LAB/'scripts/r4_appearance_adapter.py',LAB/'scripts/r4_exact_local_stage_collector_r2.py',LAB/'scripts/r4_raw_pose_driver_stage_reference.py']:record(p)
    rows=[]
    for r in current['rows']:
        clip,frame=r['clip'],r['frame']
        path=record(DATA/r['file']);assert sha(path)==r['sha256']
        z=np.load(path,allow_pickle=False)
        names=r['bone_names'];assert names==recipe['boneNames'] and len(names)==57
        oldclip=next(c for c in old_manifest['clips'] if c['clip']==clip)
        prefix=oldclip['array_prefix']
        q=z['raw_quaternion_wxyz_f32'];factors=z['driver_factors_f32']
        q_equal=q.tobytes()==old_raw[prefix+'_raw_quaternion_wxyz'][frame-1].tobytes()
        factors_equal=factors.tobytes()==old_raw[prefix+'_five_driver_factors'][frame-1].tobytes()
        assert q_equal and factors_equal
        pose=load(DATA/f'{clip}_frame{frame:03d}_all_rig_pose_rest.json')
        native=pose['rigs']['Meshy_Fitted_Rig']
        direct=z['pose_rig_local_f64'];rig_world=z['rig_world_f64']
        assert np.array_equal(rig_world,np.asarray(native['world']))
        assert direct.tobytes()==np.asarray([native['bones'][n]['pose_local'] for n in names],np.float64).tobytes()
        widened={k:bool(np.array_equal(z[k],z[k].astype(np.float32).astype(np.float64))) for k in ['rest_local_f64','pose_rig_local_f64','body_world_f64','rig_world_f64']}
        assert all(widened.values())
        world=np.asarray([native['bones'][n]['pose_world'] for n in names],np.float64)
        recovered=np.linalg.inv(rig_world)@world
        recovered_f32=recovered.astype(np.float32)
        diff=np.abs(recovered-direct);idx=np.unravel_index(diff.argmax(),diff.shape)
        changed=int(np.count_nonzero(recovered_f32.view(np.uint32)!=direct.astype(np.float32).view(np.uint32)))
        assert z['rest_local_f64'].astype('<f4').tobytes()==np.asarray(recipe['rest'],dtype='<f4').reshape(57,4,4).tobytes()
        rest_json=np.asarray([native['bones'][n]['rest_local'] for n in names],np.float64)
        assert rest_json.tobytes()==z['rest_local_f64'].tobytes()
        rows.append({'clip':clip,'frame':frame,'bone_names':names,'actual_native_pose_rest_JSON_and_NPZ_same_bits':True,'float64_storage_is_exact_upcast_of_f32_values':widened,'raw_native_channels_equal_prior276frame_dataset_bits':q_equal,'raw_driver_factors_equal_prior_dataset_bits':factors_equal,'raw_quat_SHA':ah(q),'raw_factor_SHA':ah(factors),'direct_native_pose_f32_rowmajor_SHA':ah(direct.astype('<f4')),'rest_f32_rowmajor_SHA':ah(z['rest_local_f64'].astype('<f4')),'body_world_f32_SHA':ah(z['body_world_f64'].astype('<f4')),'rig_world_f32_SHA':ah(rig_world.astype('<f4')),'matrix_recovery_control_ONLY_not_consumer_or_native_operator':{'method':'numpy float64 inverse(rigWorld) @ already native-rounded poseWorld, then f32','max_component_delta_vs_direct_native_pose':float(diff.max()),'worst_bone':names[idx[0]],'worst_row':int(idx[1]),'worst_column':int(idx[2]),'f32_components_changed':changed,'bitexact_direct_pose':changed==0,'reason':'Round world matrix output loses local component information. This inverse is not a native premat/bone-operator implementation and does not attribute consumer mismatch.'},'rest_matches_original57_recipe_bits':True})
        z.close()
    result={'status':'SOURCE_INPUT_DOMAIN_AND_REPRODUCIBILITY_FILE_ONLY_VERIFIED','inputs':inputs,'rows':rows,'Laptop_actual_byte_custody':transferred,'no_duplicate_receiver_packet_sent':True,'source_checkpoint':'ea015dba7146f6c6447476fd5ded514e99ccf72f','current_consumer_local_metrics_from_PM_delegation_NOT_recomputed_here':{'Startle11_stage0_full_max_local_units':1.311979e-6,'Strong6_stage0_full_max_local_units':1.899182e-6,'Startle11_focused_max_local_units':0.439367e-6,'Strong6_focused_max_local_units':0.926304e-6,'rest_f32':'EXACT','worst_pose_bone':'R3_Shoulder_L_Bind','source_actual_pose_component_max_delta':[2.115934e-6,1.956017e-6],'body_world_component_max_delta':2.622604e-8,'actual_consumer_rig_world':'NOT_SEPARATELY_RECORDED','cause':'NOT_ISOLATED'},'expanded_source_metadata_schema':{'rig_keys':list(expanded['Meshy_Fitted_Rig']),'bone_collection_type':type(expanded['Meshy_Fitted_Rig'].get('bones')).__name__},'source_operator_review':{'armature_update':'BKE_pose_bone_done: native float imat= inverse(bone.arm_mat), chan_mat=pose_mat*imat, DQ only if not BONE_NO_DEFORM. R7 trace draft did not execute native arithmetic.','armature_deform':'Compiled #else branch: armature_to_target=target.world_to_object*arm.object_to_world; target_to_armature=invert(armature_to_target). Alternate direct inverse-arm*target-world #if0 is disabled; algebraic equivalence does not imply f32 operation equivalence.','channel_to_pose_internal_arithmetic':'Not reconstructed by this script; evaluated pose is direct saved authority. Native inverse/rest/deform/DQ/premat actual intermediates not in R2 capture. Need prove all existing input identity before declaring these missing terms causal.'},'no_Blender_build_acquisition_or_replay':True,'native_operator_cache_route':'UNKNOWN_NOT_READ','cause':'NOT_ISOLATED','next':'Use existing direct native quat/pose/rest/bodyWorld/rigWorld arrays to control consumer reconstruction and matrix input boundaries separately; receiver validates actual57-slot/rawbit inputs before operator attribution.'}
    E.mkdir(parents=True);write('SOURCE_POSE_MATRIX_BOUNDARY_ANALYSIS_R1.json',result)
    write('LAPTOP_EXISTING_INPUT_AB_CONTRACT_R1.json',{'status':'DATA_DOMAIN_REQUIREMENTS_ONLY_NOT_EXECUTED','inputs':{'raw_quaternion':'NPZ raw_quaternion_wxyz_f32[57,4], original57 names, no implicit sign change/normalization; wxyz order','evaluated_pose':'NPZ pose_rig_local_f64 is widened native f32. Read direct then f32 row-major slots. Do not inverse poseWorld or decompose/recompose TRS.','rest':'rest_local_f64 direct57 rest f32; keep helper slots and source inheritance/topology metadata','object_matrices':'body_world_f64 and rig_world_f64 separate; record consumer both before any matrix products','geometry_weights':'Full original63561/304799 ordered CSR+zeros and exact mask/group law unchanged'},'comparisons':[{'boundary':'channel import/evaluation','control':'Compare actual consumer original channel components/time/slot/quaternion semantics with direct native q; source exact q through SAME consumer hierarchy/constraint/inheritance evaluator changes only channel input. Raw q alone is not all LRS/constraints.'},{'boundary':'pose construction input','control':'Keep exact geometry/rest/body+rig worlds/flags/CSR; substitute direct native pose matrix array transiently, bypassing imported-channel pose reconstruction. Compare stage0 local. This is diagnostic, not runtime source-frame pose substitution.'},{'boundary':'object transform input','control':'Hold direct pose/rest/CSR; compare actual versus direct native bodyWorld and rigWorld independently, then both. Consumer rigWorld missing in earlier receipt; do not infer it from bodyWorld or poseWorld.'},{'boundary':'operator arithmetic','control':'Only after all input arrays/source flag/weights/order identity demonstrated: compare native versus consumer inverse-rest/deform/premat/postmat/DQ. R2 does not contain native internal intermediates; do not fabricate them or launch source job absent demonstrated missing datum.'}],'outputs_required':'Frozen input rawbit hashes plus actual local stage0/1/2 arrays and frame/instance/bone identity; direct SOURCE_LOCAL comparison excludes P/world transport confounds. No new Desktop capture.','driver_warning':'Quaternion sign alignment is orientation diagnostic only; source SINGLE_PROP wxyz-driven factors can change under sign/normalization. Preserve raw component factors as separate controls; factor changes start at source CorrectiveSmooth, not primary stage0.','native_source_numeric_arrays_already_delivered':True,'product_promotion':'HOLD'})
    print(json.dumps({'status':result['status'],'rows':[{'clip':r['clip'],'world_to_local_control_delta':r['matrix_recovery_control_ONLY_not_consumer_or_native_operator']['max_component_delta_vs_direct_native_pose'],'changed_f32_components':r['matrix_recovery_control_ONLY_not_consumer_or_native_operator']['f32_components_changed']} for r in rows]}))

if __name__=='__main__':main()
