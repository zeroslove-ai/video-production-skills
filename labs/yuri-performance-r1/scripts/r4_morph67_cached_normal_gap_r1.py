"""Cached-only gap analysis and concrete NOT-RUN two-input proposal."""
from pathlib import Path
import gzip,hashlib,json
import numpy as np
LAB=Path(__file__).resolve().parent.parent
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-morph67-two-input-source-normal-proposal-r1'
E=LAB/'evidence/o1-morph67-two-input-source-normal-proposal-r1'
SHA={'WORST':'170accdfe80954ae2fe340e1aca3bdef5ac2e7fd25049be2089ab69766bd77a2','NEUTRAL':'b775d6252cc4e9c3703d76e5747a7113bfb5d8318f1d1ff5e9b2b73df5d53961'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    inputs={t:json.loads((OUT/(t+'_source_inputs_PRIVATE_R1.json')).read_bytes()) for t in SHA}
    assert all(sha(OUT/(t+'_source_inputs_PRIVATE_R1.json'))==h for t,h in SHA.items())
    frames=BASE/'o1-original-idle-sampling-r3/FRAMES_PRIVATE_R1.jsonl.gz'
    nearest={t:(float('inf'),None) for t in SHA};count=0;geometry_normal_fields=set();order=None
    with gzip.open(frames,'rt') as f:
        for line in f:
            r=json.loads(line);count+=1
            face=next(x for x in r['domains'] if x['Action']=='MESHY_R2_FACE_Idle')
            gaze=next(x for x in r['domains'] if x['Action']=='MESHY_R2_GAZE_Idle')
            assert [x['path'] for x in gaze['channels']]==['["Face_GazeYaw"]','["Face_GazePitch"]']
            paths=[x['path'] for x in face['channels']]
            if order is None:order=paths
            assert order==paths and len(order)==16
            values=np.array([x['evaluated_RNA'] for x in face['channels']]+[x['evaluated_RNA'] for x in gaze['channels']],dtype=float)
            for t,d in inputs.items():
                target=np.array(d['native_face']+[d['NativeYaw'],d['NativePitch']],dtype=float)
                delta=float(np.max(np.abs(values-target)))
                if delta<nearest[t][0]:nearest[t]=(delta,r['frame'])
            for g in r['geometry']:
                if g['object']=='Character_Body_Head':geometry_normal_fields|={k for k in g if 'normal' in k.lower() or 'tangent' in k.lower()}
    assert count==145 and not geometry_normal_fields
    raw=BASE/'o1-original-idle-sampling-r3/RAW_FINGERPRINT_INPUTS_BEFORE_PRIVATE_R3.json.gz'
    with gzip.open(raw,'rt') as f:before=json.load(f)
    key=before['Keys']['FaceControls_TEST_Jaw_Smile.001']
    assert len(key['blocks'])==72 and all(b[1]['value']==0 for b in key['blocks'])
    head=before['objects']['Character_Body_Head']
    drivers=key['anim']['drivers'];assert sum(bool(d[2]['mute']) for d in drivers)==13
    overlapping=[d for d in drivers if d[0] in order];assert len(overlapping)==13 and all(d[2]['mute'] for d in overlapping)
    gm=LAB/'evidence/o1-gaze-evaluated-corner-reference-r1/GAZE_EVALUATED_CORNER_MANIFEST.json'
    gaze=json.loads(gm.read_bytes());refs=[]
    for r in gaze['files']:
        p=BASE/'o1-gaze-evaluated-corner-reference-r1'/r['path'];assert sha(p)==r['sha256']
        refs.append({'path':str(p),'sha256':r['sha256'],'bytes':r['bytes']})
    source=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
    assert sha(source)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
    collector=LAB/'scripts/r4_morph67_two_input_normal_collector_DRAFT_R1.py'
    compile(collector.read_text(),str(collector),'exec') # no import/bpy/native execution
    topology=BASE/'o1-source-fidelity-recovery-r1/data/Character_Body_Head_original_mesh.npz'
    assert sha(topology)=='1a48cf823cb6cf0c95c7eee6d4b7e7e8a952cbaadd50d1d9ad18d909be34f473'
    with np.load(topology) as n:
        assert n['attribute_19_value'].shape==(66861,2)
        assert np.array_equal(n['attribute_19_value'].astype(np.int16).astype(np.int32),n['attribute_19_value'])
    semantic=LAB/'evidence/o1-corner-normal-tangent-semantics-r1/CORNER_NORMAL_TANGENT_SEMANTIC_RECEIPT.json'
    graph=LAB/'evidence/o1-source-fidelity-recovery-r1/executable_geometry_node_graphs.json'
    result={'capability_delta':'새 Windows 기능 없음; exact two-input source normal gap과 NOT-RUN proposal 작성',
        'source':{'path':str(source),'sha256':sha(source)},
        'pinned_Laptop_commit':'c04dda59635d400a6cf174229a196311726c2b75',
        'inputs':[{'case':t,'repository_path':f'docs/evidence/o1-bodymap-physics-provisional/morph67-normal-ab/{t}/source_inputs.json',
                   'private_local_path':str(OUT/(t+'_source_inputs_PRIVATE_R1.json')),'sha256':SHA[t],
                   'bytes':(OUT/(t+'_source_inputs_PRIVATE_R1.json')).stat().st_size,
                   'FACE_count':16,'GAZE_count':2,'runtime_named_morph_count':len(d['original_morph_weights']),
                   'native_applied_inputs_identical':d['native_face']==d['applied_face'] and d['NativeYaw']==d['AppliedYaw'] and d['NativePitch']==d['AppliedPitch'],
                   'not_zero_FACE':any(d['native_face']),'ReactionIntent':d['ReactionIntent'],
                   'nearest_cached_integer_sample':{'frame':nearest[t][1],'max_FACE_GAZE_abs_delta':nearest[t][0]}} for t,d in inputs.items()],
        'FACE_vector_order_RNA':order,'FACE_order_authority':{'path':str(frames),'sha256':sha(frames),'frames_verified':count},
        'available_semantics':{
            'source_head':'72 original Keys including Basis; relative source shapes and original driver graph; 13 native FACE bridge drivers remain muted, other37 unmuted drivers derive EyePath/correctives. Apply16 native controls, never overwrite71 derived morph values from consumer.',
            'modifier_order':[{'name':m[0],'type':m[1]['type']} for m in head['modifiers']],
            'head_GN':'Group Input -> Set Position(FaceIris.L selection) -> Set Position.001(FaceIris.R selection) -> Group Output. Cached graph has position operations, no Set Shade Smooth/Set Mesh Normal node. Keep original value drivers, geometry masks and offsets.',
            'custom_normal':'Original CORNER/INT16_2D short2, array attribute_19_value. Decode on current smooth-fan geometric normal spaces, not xyz delta/vertex averaging. Positions changed invalidate normal caches. Exact post-shape/GN custom attribute type/payload and final normal output at these inputs are not captured yet.',
            'scope':'Shape morph precedes GN and Armature. GN position mutation can alter surrounding normal spaces even when some target vertices do not move. Do not infer normal equivalence from 8.82um geometry covariate or DN0 visual improvement.',
            'normal_basis':'Compare original source-loop local CORNER normals. World row normal normalize(n_local inverse(A)); no double bone/scene transform. Consumer baked/world normal requires actual pose and basis mapping, absent from2input files.',
            'tangent':'Use evaluated local CORNER normal + current local positions + original CORNER UVMap, same RNA Mesh.calc_tangents route as existing tri/quad head reference; preserve sign, seams and source polygon correspondence.'},
        'existing_references':{'static_head_NPZ':{'path':str(topology),'sha256':sha(topology)},
            'five_evaluated_gaze_files':refs,'five_gaze_manifest':{'path':str(gm),'sha256':sha(gm)},
            'gaze_scope':'source FACE all0/frame1/OFF Armature, neutral and4cardinal gaze. Neither new input equals those controls; NEUTRAL label is not actual zero FACE.',
            'semantic_receipt':{'path':str(semantic),'sha256':sha(semantic)},'head_GN_graph':{'path':str(graph),'sha256':sha(graph)},
            'R3_geometry':'145 sampled head POSITION-only binary records. Metadata has no normal/tangent buffers. Raw BEFORE normals are original POINT baseline, not MORPH67 evaluated CORNER witness.'},
        'missing':['Evaluated source original-loop CORNER normals and UV tangents at exact WORST/NEUTRAL controls',
                   'Per SHAPE_ONLY / SHAPE_GN / FULL_SOURCE custom normal attribute type/domain/payload propagation',
                   'Derived source Key readback vs runtime71 named weights; float-percent rounding must be distinguished from actual mapping differences',
                   'Runtime actual corner/triangle mapping, deformed normal space and samepose bones/object matrices for postskin/world comparison'],
        'proposal':{
            'status':'NOT_RUN_NOT_APPROVED; strict guard review remains required',
            'draft_collector':{'path':str(collector),'sha256':sha(collector),'validation':'Python compile-only; bpy not imported/executed'},
            'preservation_helpers':[{'path':str(LAB/'scripts'/name),'sha256':sha(LAB/'scripts'/name)} for name in ['r4_appearance_signature.py','native_preservation.py']],
            'executable':{'path':'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','sha256':'284f4041f98e113f3dc10654a7193ffaaa9bfdfec8b87fa116620a48b5f6d4cb','build':'9e2066aef7ef'},
            'source_clone':'After approval, broker copies immutable source bytes into NEW private owned attempt directory; verifies same SHA, loads clone use_scripts=False. Never saves source or clone; no geometry/rig rebuild.',
            'payload_argv':'--background --factory-startup --disable-autoexec --threads 2 --python <draft_collector> -- --clone <new-private-source-copy.blend> --inputs <private-input-folder> --out <new-owned-private-result-dir> --new-approval <new-exact-packet-approval.json> --guard-before <strict-owner-before-receipt.json>',
            'cases':['WORST','NEUTRAL'],'head_only':True,'frame':1,'body_actions':'Unbound original source/rest; do not seek SourceFrame/loop_frame. This isolates normal response to FACE16/GAZE2, not full runtime timeline pose.',
            'stages':['SHAPE_ONLY: head GN/Armature disabled in private clone RAM','SHAPE_GN: original head GN enabled/Armature disabled','FULL_SOURCE: both original modifiers enabled with source original rest/pose'],
            'controls':'Set original16 Keys from native_face in verified order plus Face_GazeYaw/Pitch. Preserve every driver expression/mute and source relative shape definition; record all72 Key outputs, compare71 nonBasis outputs to consumer weights/100 diagnostically.',
            'capture':'Per stage head local positions, original-loop CORNER normals, evaluated custom_normal type/domain/payload, sharp flags, UV, topology/material/smooth flags, native triangle source corners/polygons, UV tangent/sign and object matrix; no textures/shader render, no mesh export.',
            'restore':'Finally restore16 inputs,2gaze and2modifier viewport/render flags; no Action bind. Original78 Actions/13 muted drivers unchanged. Full cached-signature helper BEFORE/AFTER exact, OFF head arrays exact. Source/input hashes pre/post exact.',
            'limits':{'native_processes':1,'Blender_threads':2,'external_wall_seconds':90,'private_output_max_MiB':64,'Job_process_memory_max_MiB':4096,'render_export_save_GPU_jobs':0,'test_inputs':2,'stage_records':6,'OFF_baseline_records':2},
            'owned_guard':'New reviewed broker must use retained owned process handle + verified PID/creation FILETIME/image path/hash and parent, private Job active_limit1/KILL_ON_CLOSE, strict BEFORE+AFTER QueryFullProcessImageName, exact termination/wait exit code plus signaled handle, JobActive0/no escaped descendants. If strict image query error5 recurs: whole FAIL/HOLD, abort/quarantine and stop; no retry/waiver/exitFILETIME substitute.',
            'approval_boundary':'No native launch authorized. Historical sampler approval consumed; original guard FAIL remains. Existing strict launcher must not be auto-reused. A new broker for this command, approved exact input/script/helper hashes and review receipt must be frozen/reviewed before run. Draft collector receipt protocol alone is not a working or verified OS guard.',
            'delivery':'At most8 compact private NPZ (6 stage records plus2 OFF baseline records) and small private receipt; source arrays are comparison evidence, never cached-pose final runtime injection. Export/public geometry forbidden.'},
        'guard_F2_F3':'FAILED-HOLD unchanged','native_executions':0,'Unity_writes':0,
        'validation':'2 pinned input hashes/order;145 cached sample metadata;5 cached gaze fileSHA;static NPZ SHA/short2;source SHA;draft compile-only'}
    E.mkdir(exist_ok=True)
    (E/'SOURCE_NORMAL_GAP_2INPUT_PROPOSAL_R1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS cache-only gap analysis; draft compile-only; no native executed')
    print('Nearest existing input observations',nearest)
if __name__=='__main__':main()
