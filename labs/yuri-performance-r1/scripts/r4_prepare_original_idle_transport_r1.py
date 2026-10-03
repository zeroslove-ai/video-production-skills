"""File-only proposed bindings; never import bpy, launch, activate, or export."""
from pathlib import Path
import hashlib
import json

LAB = Path(__file__).resolve().parent.parent
E = LAB / 'evidence/o1-original-idle-transport-preparation-r1'
SUMMARY = LAB / 'evidence/o1-original-idle-slot-graph-result-r2/INDEPENDENT_IDLE_GRAPH_BINDING_SUMMARY_R2.json'
RAW = Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-original-idle-slot-graph-inspection-r2/IDLE_SLOT_GRAPH_RESULT_R1.json')

def main():
    assert not E.exists(), 'Frozen output: no overwrite'
    summary = json.loads(SUMMARY.read_bytes())
    raw = json.loads(RAW.read_bytes())
    assert summary['source_scene_before_after_exact'] and summary['fps'] == 24 and summary['fps_base'] == 1
    bindings = []
    for row, action in zip(summary['Action_slot_candidate_table'], raw['Actions'], strict=True):
        assert row['exact_Action'] == action['exact_Action'] and not row['existing_owner_references']
        curves = [c for b in action['slots'][0]['channelbags'] for c in b.get('fcurves', [])]
        assert len(curves) == row['complete_attributed_curves']
        bindings.append({
            **row,
            'actual_target_intent': 'ORIGINAL_AUTHOR_INTENT_UNKNOWN',
            'proposed_binding_provenance': 'PM_REQUESTED_EXPLICIT_PROPOSAL_FROM_UNIQUE_COMPLETE_RNA_COMPATIBILITY; NOT_RECOVERED_AUTHOR_INTENT',
            'original_modifier_flags': sorted({json.dumps(c['modifiers']) for c in curves}),
            'future_resolution_key': [row['exact_Action'], row['slot_handle']],
            'assigned_or_activated': False,
        })
    proposal = {
        'status': 'FILE_ONLY_PROPOSAL_NO_NATIVE_ACTIVATION_OR_EXPORT',
        'source_sha256': 'a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa',
        'graph_checkpoint': 'a5ede54',
        'graph_summary_sha256': hashlib.sha256(SUMMARY.read_bytes()).hexdigest(),
        'bindings': bindings,
        'intent_search': {
            'scope': 'Cached research repository tracked scripts/manifests/docs and all local Git history; no product or Laptop access',
            'commands': [
                "rg -n 'MESHY_R2|FaceControls_TEST_Jaw_Smile' --glob '*.py' --glob '*.md' --glob '*.json'",
                "git log --all --oneline -G 'MESHY_R2|FaceControls_TEST_Jaw_Smile' -- labs/yuri-performance-r1 ':!labs/yuri-performance-r1/evidence'",
                'git log --all --oneline -- labs/yuri-performance-r1/evidence/model-handoff-r4/R4.json',
            ],
            'result': 'NO_ORIGINAL_AUTHORING_BINDING_FOUND_IN_BOUNDED_CACHED_SCOPE; UNKNOWN_OUTSIDE_SCOPE',
            'history_hits': ['a5ede54 result reader', 'f93c507 graph completeness reader', 'ce76347 graph preparation reader', '840ac26 intake planner'],
            'inventory_first_checkpoint': '08caad7; imported inventory is descriptive, not Action owner intent',
            'evidence_locations': [
                'scripts/r4_original_idle_slot_graph_inspect_r2.py:17 @ f93c507 (exact names inspected)',
                'scripts/r4_original_living_intake_plan_r1.py:32 @ 840ac26 (dynamic name inventory lookup)',
                'scripts/r4_freeze_original_idle_graph_result_r2.py:39 @ a5ede54 (exact names audited)',
                'evidence/o1-original-idle-slot-graph-result-r2/ACTUAL_IDLE_GRAPH_HANDOFF_R2.md:9 @ a5ede54 (candidate table)',
            ],
        },
        'future_sampling': {
            'status': 'PROPOSED_NOT_IMPLEMENTED_NOT_LAUNCHED',
            'fps': 24, 'fps_base': 1, 'source_range': [1, 73],
            'continuous_evaluation_frames': [1, 145], 'inclusive_samples': 145,
            'duration_seconds': 6,
            'period_frames_provisional': 72,
            'evaluation': 'Evaluate original CYCLES modifiers continuously at frames1..145; no manual modulo remap or replacement curves. Record native curve/evaluated outputs at73,74,145 and compare1/73/145 plus boundary velocity. Modifier modes/offset and endpoint closure require native evidence before loop PASS.',
            'restore': 'Snapshot original bindings, slots, relevant properties/Key values, frame and original scene signature; bind only four exact Action+slot keys in disposable process; restore originals and reevaluate original frame; require OFF->ON->OFF signatures and source file SHA unchanged.',
            'readbacks': [
                'BODY native57 rest/pose matrices, quaternion and all4rig137 evaluated pose; body/root trajectory',
                'FACE actual16 original Key curves plus all original72 Key values and active driver evaluated outputs; no face-board pose substitute',
                'GAZE actual Character_Body_Head Face_GazeYaw/Face_GazePitch, driver evaluated outputs and native eye geometry/transform evidence',
                'HAIR actual Hair_Rig_R4 Pony_Sway/Pony_Lift/Tip_Curl/Side_Sway and10bone native outputs/14driver evaluation',
                'All145 frames synchronized; curve evaluation vs native output recorded separately including unchanged/muted/overridden channels',
            ],
            'preserve': 'Original4rig137 hierarchy/rest/full weights;78Actions including existing66; all geometry/material slots/nodes/textures/ShapeKeys/drivers and13muted bridges exactly; no aliases/new motion/unmute/donor mesh/source overwrite',
            'guard': 'Separate pinned owned Job review/receipt required: one process, CPU only2threads/affinity3/8GiB,120s watchdog, RAM>=12GiB,C>=100GiB, installed-origin gate315files; terminal exit0/Active0/PIDs[] and clean cleanup. No automatic retry.',
            'execution_packet': 'NOT_PREPARED: collector/launcher/config/argv/hash bindings require separate bounded review; prior graph receipt does not authorize sampling',
            'render': 'NOT_RUN; native sampling does not prove pixels or normal-speed playback; CPU/GPU render resources reviewed separately without touching product lease',
        },
        'transport': {
            'canonical_source': 'Immutable original R4 separate from animation-only data and runtime adapter',
            'preferred': 'Original Blender Action/slot curve library + explicit target manifest; preserve original curves/modifiers and driver graph references, no geometry merge',
            'BODY': 'Animation-only armature FBX possible after native playback proof; native hierarchy/rest unchanged; compatibility asset only',
            'FACE': 'Original KEY Action library + semantic curve metadata; armature-only FBX cannot represent this Key animation. Numeric Key/driver samples remain private.',
            'GAZE_HAIR': 'Original Object custom-property Actions + preserved driver graph semantics; generic armature FBX alone cannot guarantee transport. Runtime adapter separately consumes named properties.',
            'public_custody': 'Only metadata/counts/hashes/RNA paths/scripts; model/raw numeric curves/geometry/matrices private',
            'current_exports': 0,
        },
        'acceptance': {'original_intent': 'UNKNOWN', 'native_four_lane_playback': 'NOT_RUN', 'two_cycle_loop': 'NOT_RUN', 'normal_speed_visual': 'NOT_RUN', 'product_Unity_PBR_AlwaysAnimate': 'NOT_CLAIMED'},
    }
    E.mkdir(parents=True)
    (E / 'ORIGINAL_IDLE_BINDING_TRANSPORT_PROPOSAL_R1.json').write_text(json.dumps(proposal, indent=2) + '\n', encoding='utf8')
    print(json.dumps({'status': proposal['status'], 'bindings': len(bindings), 'samples_proposed': 145, 'exports': 0}))

if __name__ == '__main__':
    main()
