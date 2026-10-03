"""PREPARED ONLY. Native CPU source-local cumulative ablation; review receipt required.

No save/render/export/build/network or reconstructed normals. Never auto-launch.
"""
import hashlib, json, os, sys, time
from pathlib import Path
import bpy
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from r4_appearance_adapter import ReactionLane
from r4_appearance_signature import snapshot, difference, props, anim

LAB = HERE.parent
BASE = Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT = BASE / 'o1-exact-source-local-stage-capture-r2'
SOURCE = LAB / 'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
LIB = BASE / 'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'
RECIPE = BASE / 'o1-native-armature-full-recipe-custody-r1/SourceBodyArmatureInput_0cd0bdd7_EXACT.json'
PROPOSAL = LAB / 'evidence/o1-exact-local-stage-factory-addon-preparation-r2/CAPTURE_PROPOSAL_R2.json'
CASES = [('YRA_R4_Startle_Short', 11), ('YRA_R4_Struggle_Strong_Loop', 6)]

def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''): h.update(block)
    return h.hexdigest()

def write(name, value):
    with (OUT / name).open('x', encoding='utf8') as f: json.dump(value, f, indent=2)

def array(collection, field, width=3, dtype=np.float32):
    a = np.empty(len(collection) * width, dtype)
    collection.foreach_get(field, a)
    return a.reshape(-1, width) if width > 1 else a

def matrix(m): return np.array(m, dtype=np.float64)
def bits(v): return np.asarray(v, dtype='<f4').tobytes()
def ah(a): return hashlib.sha256(a.tobytes(order='C')).hexdigest()

def main():
    proposal = json.loads(PROPOSAL.read_bytes())
    review = json.loads((OUT / 'PM_APPROVAL_EXACT_LOCAL_CAPTURE_R2.json').read_bytes())
    assert review['scope'] == 'EXACT_TWO_FRAME_SOURCE_LOCAL_STAGE_READ_ONLY'
    assert review['approved'] is True and review['proposal_sha256'] == sha(PROPOSAL)
    assert review['collector_sha256'] == sha(__file__)
    assert review['argv'] == proposal['argv']
    assert review['reviewed_owned_job_terminal_behavior'] is True
    assert review['custom_native_build_trace_capture_approved'] is False
    assert review['large_resource_acquisition_approved'] is False
    assert bpy.app.background and bpy.app.version_string == '5.2.1 LTS'
    assert bpy.app.build_hash.decode() == '9e2066aef7ef'
    from r4_installed_addon_origin_gate_r2 import inspect_and_require
    addon_manifest = LAB / 'evidence/o1-exact-local-stage-factory-addon-preparation-r2/INSTALLED_BUNDLED_ADDON_ORIGIN_MANIFEST_R2.json'
    addon_before = inspect_and_require(bpy, addon_manifest, OUT, 'before')
    assert Path(bpy.data.filepath).resolve() == SOURCE.resolve()
    assert not list(OUT.glob('*.npz')) and not (OUT / 'CAPTURE_RESULT_R1.json').exists()
    inputs = proposal['inputs']
    assert all(sha(p) == row['sha256'] for p, row in inputs.items())
    started = time.monotonic()
    original_actions = [a.name for a in bpy.data.actions]
    assert len(original_actions) == 78 and bpy.context.scene.frame_current == 1
    before = snapshot(original_actions)
    body = bpy.data.objects['Meshy_Body_NeutralCovered']
    rig = bpy.data.objects['Meshy_Fitted_Rig']
    assert [m.type for m in body.modifiers] == ['ARMATURE', 'ARMATURE', 'CORRECTIVE_SMOOTH', 'SMOOTH', 'SMOOTH', 'SMOOTH', 'SMOOTH']
    q = json.loads(RECIPE.read_bytes())
    names = [b.name for b in rig.data.bones]
    assert names == q['boneNames'] and len(names) == 57
    assert len(body.data.vertices) == len(q['positions']) == 63561
    assert len(q['offsets']) == 63562 and q['offsets'][-1] == 304799
    assert len(body.vertex_groups) == len(q['groups']) == 58 and q['maskGroup'] == 52
    for i, b in enumerate(rig.data.bones): assert bits(matrix(b.matrix_local).ravel()) == bits(q['rest'][i])
    assert bits(matrix(body.matrix_world).ravel()) == bits(q['sourceWorld'])
    zeros = 0
    for g in body.vertex_groups:
        assert g.name == q['groups'][g.index]
        assert q['groupToBone'][g.index] == (names.index(g.name) if g.name in names else -1)
    for i, v in enumerate(body.data.vertices):
        assert bits(v.co) == bits(q['positions'][i])
        start, end = q['offsets'][i:i+2]
        assert len(v.groups) == end-start
        for j, g in enumerate(v.groups, start):
            assert g.group == q['indices'][j] and bits([g.weight]) == bits([q['weights'][j]])
            zeros += int(g.weight == 0)
    assert zeros == 37310
    topology = {
        'original_corner_vertex': array(body.data.loops, 'vertex_index', 1, np.int32),
        'original_corner_edge': array(body.data.loops, 'edge_index', 1, np.int32),
        'original_polygon_start': array(body.data.polygons, 'loop_start', 1, np.int32),
        'original_polygon_total': array(body.data.polygons, 'loop_total', 1, np.int32),
        'original_polygon_material': array(body.data.polygons, 'material_index', 1, np.int32),
    }
    assert len(topology['original_corner_vertex']) == 254602
    with bpy.data.libraries.load(str(LIB), link=False) as (src, dst): dst.actions = [c[0] for c in CASES]
    assert all(dst.actions)
    lane = ReactionLane()
    rows = []
    try:
        for clip, frame in CASES:
            lane.on(clip)
            bpy.context.scene.frame_set(frame)
            bpy.context.view_layer.update()
            assert rig.animation_data.action_slot.identifier == 'OBMeshy_Fitted_Rig'
            original_settings = [props(m) for m in body.modifiers]
            driver_factors = [m.factor for m in body.modifiers[2:]]
            data = dict(topology)
            data['rest_local_f64'] = np.stack([matrix(b.matrix_local) for b in rig.data.bones])
            assert [b.name for b in rig.pose.bones] == names
            data['pose_rig_local_f64'] = np.stack([matrix(b.matrix) for b in rig.pose.bones])
            data['raw_quaternion_wxyz_f32'] = np.array([tuple(b.rotation_quaternion) for b in rig.pose.bones], np.float32)
            data['rig_world_f64'] = matrix(rig.matrix_world)
            data['body_world_f64'] = matrix(body.matrix_world)
            data['driver_factors_f32'] = np.asarray(driver_factors, np.float32)
            clone = body.copy()
            bpy.context.scene.collection.objects.link(clone)
            clone.hide_render = True
            clone.hide_viewport = False
            clone.hide_set(False)
            stages = []
            try:
                assert clone.data is body.data
                for last in range(7):
                    for i, (m, srcm) in enumerate(zip(clone.modifiers, body.modifiers)):
                        m.show_viewport = bool(srcm.show_viewport and i <= last)
                        m.show_render = bool(srcm.show_render and i <= last)
                    clone.update_tag()
                    bpy.context.view_layer.update()
                    assert [m.factor for m in clone.modifiers[2:]] == driver_factors
                    deps = bpy.context.evaluated_depsgraph_get()
                    ev = clone.evaluated_get(deps)
                    mesh = ev.to_mesh(preserve_all_data_layers=True, depsgraph=deps)
                    try:
                        assert len(mesh.vertices) == 63561 and len(mesh.loops) == 254602
                        for k, col, field in [('original_corner_vertex', mesh.loops, 'vertex_index'), ('original_corner_edge', mesh.loops, 'edge_index'), ('original_polygon_start', mesh.polygons, 'loop_start'), ('original_polygon_total', mesh.polygons, 'loop_total'), ('original_polygon_material', mesh.polygons, 'material_index')]:
                            assert np.array_equal(array(col, field, 1, np.int32), topology[k]), k
                        local = array(mesh.vertices, 'co')
                        # Native evaluated CORNER getter. Never calc/average normals.
                        normal = array(mesh.corner_normals, 'vector')
                        assert normal.shape == (254602, 3)
                        mw = matrix(ev.matrix_world)
                        world = (local.astype(np.float64) @ mw[:3, :3].T + mw[:3, 3]).astype(np.float32)
                        wn = normal.astype(np.float64) @ np.linalg.inv(mw[:3, :3])
                        wn /= np.linalg.norm(wn, axis=1)[:, None]
                        for key, a in [('local_position', local), ('local_corner_normal', normal), ('world_position', world), ('world_corner_normal', wn.astype(np.float32)), ('evaluated_body_world', mw)]:
                            assert np.isfinite(a).all()
                            data[f'stage_{last:02d}_{key}'] = a
                        stages.append({'stage': last, 'flags': [[m.name, m.show_viewport, m.show_render] for m in clone.modifiers], 'settings': [props(m) for m in clone.modifiers], 'native_normal_route': 'evaluated mesh.corner_normals RNA getter', 'native_cache_operator_branch': 'UNKNOWN_NOT_READ', 'local_position_bits_sha256': ah(local), 'local_corner_normal_bits_sha256': ah(normal)})
                    finally: ev.to_mesh_clear()
                    print('EXACT_LOCAL_STAGE_READ', clip, frame, last, flush=True)
                assert [props(m) for m in body.modifiers] == original_settings
                frozen = Path(proposal['final_reference_by_clip'][clip])
                with np.load(frozen, allow_pickle=False) as z:
                    for key in ('local_position', 'local_corner_normal', 'world_position', 'world_corner_normal'):
                        assert data['stage_06_'+key].tobytes() == z['current_'+key].tobytes(), ('final reference drift', key)
                all_pose = {o.name: {'world': matrix(o.matrix_world).tolist(), 'bones': {b.name: {'rest_local': matrix(o.data.bones[b.name].matrix_local).tolist(), 'pose_local': matrix(b.matrix).tolist(), 'pose_world': matrix(o.matrix_world @ b.matrix).tolist()} for b in o.pose.bones}} for o in bpy.data.objects if o.type == 'ARMATURE'}
                pose_digest = hashlib.sha256(json.dumps(all_pose, separators=(',', ':')).encode()).hexdigest()
                write(f'{clip}_frame{frame:03d}_all_rig_pose_rest.json', {'rigs': all_pose, 'fingerprint': pose_digest})
                path = OUT / f'{clip}_frame{frame:03d}_native_local_seven_stages.npz'
                with path.open('xb') as f: np.savez_compressed(f, **data)
                with np.load(path, allow_pickle=False) as z:
                    assert set(z.files) == set(data)
                    for k, a in data.items(): assert z[k].dtype == a.dtype and z[k].tobytes() == a.tobytes()
                rows.append({'clip': clip, 'frame': frame, 'action_slot': rig.animation_data.action_slot.identifier, 'fps': 24, 'seconds': (frame-1)/24, 'modifiers': original_settings, 'body_drivers': anim(body), 'bone_names': names, 'all_rig_pose_rest_fingerprint': pose_digest, 'final_frozen_reference_bit_identical': True, 'stages': stages, 'file': path.name, 'sha256': sha(path), 'bytes': path.stat().st_size, 'arrays': {k: {'shape': list(a.shape), 'dtype': str(a.dtype), 'sha256': ah(a)} for k, a in data.items()}})
            finally:
                bpy.data.objects.remove(clone, do_unlink=True)
                bpy.context.view_layer.update()
                lane.off()
    finally:
        lane.off()
        for a in dst.actions:
            if a is not None: bpy.data.actions.remove(a)
        bpy.context.view_layer.update()
    addon_after = inspect_and_require(bpy, addon_manifest, OUT, 'after')
    assert addon_before['preferences_module_names'] == addon_after['preferences_module_names'] and addon_before['loaded_enabled_module_names'] == addon_after['loaded_enabled_module_names']
    after = snapshot(original_actions)
    diff = difference(before, after)
    assert not diff, diff
    assert all(sha(p) == row['sha256'] for p, row in inputs.items())
    write('SCENE_SIGNATURE_BEFORE_AFTER.json', {'before': before, 'after': after, 'differences': diff})
    write('CAPTURE_RESULT_R1.json', {'status': 'SOURCE_LOCAL_DATA_ONLY_GUARD_ACCEPTANCE_SEPARATE', 'rows': rows, 'inputs': inputs, 'source_pre_post_identical': True, 'full_CSR_original_identity': {'entries': 304799, 'zero_entries': zeros, 'recipe_sha256': sha(RECIPE)}, 'pid': os.getpid(), 'seconds': time.monotonic()-started, 'renders_exports_saves': 0, 'native_cache_operator_branch': 'UNKNOWN_NOT_READ', 'world_data_policy': 'Derived separately from native local f32 via evaluated matrix float64 then f32; world normal inverse transpose then normalization. World values are not direct native getters.', 'limitation': 'Cumulative disposable-copy ablation; normal getter may compute caches. Not instrumented in-flight modifier buffers or cache-branch proof; native numeric/PBR acceptance pending.'})

if __name__ == '__main__': main()
