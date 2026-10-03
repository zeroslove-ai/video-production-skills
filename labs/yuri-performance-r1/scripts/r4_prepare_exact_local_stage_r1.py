"""CPU file-only preparation. Does not import bpy, spawn processes or launch Blender."""
from pathlib import Path
import ast, hashlib, json, zipfile
import numpy as np

LAB = Path(__file__).resolve().parent.parent
BASE = Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
E = LAB / 'evidence/o1-exact-local-stage-preparation-r1'
COLLECTOR = LAB / 'scripts/r4_exact_local_stage_collector_r1.py'
BLENDER = Path('C:/Program Files/Blender Foundation/Blender 5.2/blender.exe')
SOURCE = LAB / 'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
ACTION = BASE / 'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'
RECIPE = BASE / 'o1-native-armature-full-recipe-custody-r1/SourceBodyArmatureInput_0cd0bdd7_EXACT.json'
REF = BASE / 'o1-dynamic-body-cycles-input-reference-r1'
FINAL = {
    'YRA_R4_Startle_Short': REF / 'YRA_R4_Startle_Short_frame011_actual_evaluated_cycles_inputs.npz',
    'YRA_R4_Struggle_Strong_Loop': REF / 'YRA_R4_Struggle_Strong_Loop_frame006_actual_evaluated_cycles_inputs.npz',
}

def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''): h.update(b)
    return h.hexdigest()

def write(n, v):
    with (E/n).open('x', encoding='utf8') as f: json.dump(v, f, indent=2)

def main():
    assert not E.exists(), 'Frozen preparation cannot be overwritten'
    ast.parse(COLLECTOR.read_text(encoding='utf8'))
    compile(COLLECTOR.read_text(encoding='utf8'), str(COLLECTOR), 'exec')
    assert sha(SOURCE) == 'a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
    assert sha(ACTION) == '6874ec69d5721f385d31edaa06ef0d58c89a543b98bacd961f8f575ff57eef4d'
    assert sha(RECIPE) == '0cd0bdd70e5a6c0670846dab74e295b0a637a79f1c6d57d503611d5cf50aafe0'
    assert sha(BLENDER) == '284f4041f98e113f3dc10654a7193ffaaa9bfdfec8b87fa116620a48b5f6d4cb'
    keys = []
    for p in FINAL.values():
        with np.load(p, allow_pickle=False) as z:
            for k, shape in [('local_position', (63561, 3)), ('world_position', (63561, 3)), ('local_corner_normal', (254602, 3)), ('world_corner_normal', (254602, 3))]:
                a = z['current_'+k]
                assert a.shape == shape and a.dtype == np.float32
                keys.append({'file': p.name, 'array': 'current_'+k, 'shape': list(a.shape), 'dtype': str(a.dtype)})
    inputs = [SOURCE, ACTION, RECIPE, COLLECTOR] + [LAB/'scripts'/n for n in ['r4_appearance_adapter.py', 'r4_appearance_signature.py', 'native_preservation.py']] + list(FINAL.values())
    argv = [str(BLENDER), '-b', '--factory-startup', '--offline-mode', '--disable-autoexec', '-t', '2', str(SOURCE), '--python-exit-code', '93', '--python', str(COLLECTOR)]
    E.mkdir(parents=True)
    proposal = {
        'status': 'PREPARED_ONLY_NOT_RUN', 'scope': 'EXACT_TWO_FRAME_SOURCE_LOCAL_STAGE_READ_ONLY',
        'approval': {'PM_review_pending': True, 'new_Blender_launch_authorized': False, 'custom_native_build_trace_capture_approved': False, 'large_resource_acquisition_approved': False},
        'argv': argv, 'blender_sha256': sha(BLENDER), 'inputs': {str(p): {'sha256': sha(p), 'bytes': p.stat().st_size} for p in inputs},
        'final_reference_by_clip': {c: str(p) for c, p in FINAL.items()},
        'cases': [{'clip': 'YRA_R4_Startle_Short', 'source_frame': 11, 'seconds': 10/24}, {'clip': 'YRA_R4_Struggle_Strong_Loop', 'source_frame': 6, 'seconds': 5/24}],
        'activation_route': 'Existing ReactionLane, exact appended Action, OBMeshy_Fitted_Rig slot, direct scene.frame_set(frame), no bake/retarget/new Actions',
        'stages': ['0 primary Armature', '1 secondary Armature', '2 Corrective Smooth', '3 original Smooth 1', '4 original Smooth 2', '5 original Smooth 3', '6 original Smooth 4'],
        'output_private_directory': str(BASE/'o1-exact-source-local-stage-capture-r1'),
        'output_schema': {
            'two_npz_files': {'stages': 7, 'each_stage': {'local_position': ['float32', 63561, 3], 'local_corner_normal': ['float32', 254602, 3], 'world_position': ['float32', 63561, 3], 'world_corner_normal': ['float32', 254602, 3], 'evaluated_body_world': ['float64', 4, 4]}, 'original_corner_vertex_edge_ids': ['int32', 254602], 'original_polygon_start_total_material': ['int32', 63781], 'rest_local_and_pose_rig_local': ['float64', 57, 4, 4], 'body_world_rig_world': ['float64', 4, 4], 'raw_quaternion_wxyz': ['float32', 57, 4], 'driver_factors': ['float32', 5]},
            'two_all_rig_pose_rest_json': 'All original armature rest/pose local and world matrices with fingerprint; private only',
            'scene_signature_before_after': 'Original 78 Actions, all objects/meshes/weights/ShapeKeys/rest/drivers/material/node/image/scene/OFF evaluated signatures; no differences allowed',
            'result_manifest': 'Per-array raw bits SHA256, input pre/post hashes, pose/rest/fullCSR fingerprints, stage flags/settings/factors, native getter provenance, PID/duration and limitations',
        },
        'native_data_provenance': 'Local arrays directly from evaluated mesh vertices.co and mesh.corner_normals.vector. No inverse-world reconstruction, calc_normals, vertex average or triangle normal substitute.',
        'world_data_provenance': 'Separate derived transform of captured native local f32 using evaluated bodyWorld f64, rounded f32. World normals inverse transpose and normalization. Explicitly not direct native world getters.',
        'operator_cache_route': 'UNKNOWN_NOT_READ; getter can recompute cache. Disposable copy cumulative ablation is not instrumented in-flight original modifier-buffer capture.',
        'read_only_policy': 'Source opened by fixed argv use_scripts disabled by CLI; shared original mesh remains read-only. Later modifier visibility only on disposable object copies. Original rig Action/pose binding restored with ReactionLane; imported Actions removed; full scene before/after compared. Never save source.',
        'guard_proposal': {
            'reference_path': str(LAB/'scripts/r4_readonly_source_job_guard_r5.py'), 'reference_sha256': sha(LAB/'scripts/r4_readonly_source_job_guard_r5.py'),
            'reference_whole_guard_status': 'FAIL_PRESERVED; source-data and terminal cleanup scoped acceptance only',
            'existing_R5_route_executable_for_this_collector': False,
            'pending_review': 'R5 fixed verifier/receipt scope cannot run this collector. PM must approve exact collector/argv, activation+copy scope and a separately reviewed minimal fixed-purpose route configuration. No new guard/probes/Blender launch in preparation.',
            'required_owned_job_limits': {'active_process_limit': 1, 'creation': 'SUSPENDED|DETACHED_PROCESS 0xC; assign owned Job before resume', 'CPU_affinity': 3, 'threads': 2, 'process_and_job_memory_bytes': 8*1024**3, 'watchdog_seconds': 120, 'free_RAM_min_bytes': 12*1024**3, 'free_C_min_bytes': 100*1024**3, 'kill_on_job_close': True},
            'required_terminal_evidence': 'PID/creation/executable same owned handle; native Job limits readback, accounting and PID list. Missing image on LIVE handle fails. On failure terminate only owned Job; finally terminal signaled/exit code and zero active/empty PID list before close. Preserve raw failure; no rerun to green.',
            'network': 'Factory/offline with no addons required; Windows Job is not a network sandbox. Collector contains no account/network/plugin operations.',
        },
        'budget': {'workers': 1, 'frames': 2, 'native_evaluations': 14, 'primary_uncompressed_stage_array_bytes': 2*7*(63561+254602)*3*4*2, 'total_expected_output_upper_bytes': 256*1024**2, 'estimated_peak_memory_upper_bytes': 8*1024**3, 'estimates_not_measured': True, 'snapshot_extra_evaluations': 'Two OFF full-scene snapshots using existing signature helper, beyond 14 body stage evaluations', 'no_render_export_bake_GPU_download_build': True},
        'pass_requirements': ['Original 63561/254602 topology order and all304799 CSR entries incl37310 zeros exact', '7 native local stages per frame; finite/readback raw bits exact', 'stage6 local/world position and CORNER normals equal frozen final reference', 'source/action/recipe/dependency SHA unchanged and full scene signature no differences', 'Data verifier result and whole owned Job result reported separately'],
        'acceptance_exclusions': ['No Unity/runtime/PBR/AlwaysAnimate PASS', 'No inferred cache branch', 'No first comparative divergence without actual consumer stage arrays'],
    }
    write('CAPTURE_PROPOSAL_R1.json', proposal)
    write('PREPARATION_VALIDATION_R1.json', {'status': 'STATIC_AND_EXISTING_FILE_SCHEMA_ONLY_PASS', 'collector_ast_compile': True, 'existing_final_array_keys': keys, 'source_action_recipe_blender_hashes_verified': True, 'Blender_launched': False, 'collector_executed': False, 'native_API_clone_driver_restoration_verified_in_this_turn': False, 'proposal_sha256': sha(E/'CAPTURE_PROPOSAL_R1.json')})
    packet = E/'YURI_O1_EXACT_LOCAL_STAGE_PREPARATION_R1.zip'
    with zipfile.ZipFile(packet, 'x', zipfile.ZIP_DEFLATED) as z:
        for p in [E/'CAPTURE_PROPOSAL_R1.json', E/'PREPARATION_VALIDATION_R1.json', COLLECTOR, Path(__file__), LAB/'scripts/r4_appearance_adapter.py', LAB/'scripts/r4_appearance_signature.py', LAB/'scripts/native_preservation.py']: z.write(p, p.name)
    with zipfile.ZipFile(packet) as z: assert z.testzip() is None
    write('PACKET_CUSTODY_R1.json', {'zip': str(packet), 'bytes': packet.stat().st_size, 'sha256': sha(packet), 'source_private_numeric_payload_in_zip': False, 'status': 'PREPARATION_ONLY_PM_REVIEW_PENDING'})
    print(json.dumps({'collector_sha256': sha(COLLECTOR), 'proposal_sha256': sha(E/'CAPTURE_PROPOSAL_R1.json'), 'packet_sha256': sha(packet), 'Blender_launched': False}))

if __name__ == '__main__': main()
