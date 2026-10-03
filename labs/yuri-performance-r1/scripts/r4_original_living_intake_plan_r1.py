"""File-only original take/slot custody planning; no bpy, export or source rewrite."""
from pathlib import Path
import hashlib,json
LAB=Path(__file__).resolve().parent.parent
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
E=LAB/'evidence/o1-original-living-intake-plan-r1'

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def main():
    assert not E.exists(),'Immutable planning checkpoint only'
    inputs={}
    def load(p):inputs[str(p)]={'sha256':sha(p),'bytes':p.stat().st_size};return json.loads(p.read_bytes())
    inventory=load(LAB/'evidence/model-handoff-r4/R4.json')
    scene=load(BASE/'o1-exact-source-local-stage-capture-r2/SCENE_SIGNATURE_BEFORE_AFTER.json')
    existing_takes=load(LAB/'evidence/o1-native-unity-probe-r1/take_and_slot_inventory.json')
    exporter=load(LAB/'evidence/o1-native-unity-probe-r1/export_manifest.json')
    source=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
    assert sha(source)==inventory['source_sha256']=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
    inputs[str(source)]={'sha256':sha(source),'bytes':source.stat().st_size}
    script=LAB/'scripts/r4_o1_native_probe_export.py'
    inputs[str(script)]={'sha256':sha(script),'bytes':script.stat().st_size}
    actions={a['name']:a for a in inventory['actions']}
    assert len(actions)==78 and sum(len(r['bones']) for r in inventory['rigs'].values())==137
    assert scene['differences']=={} and scene['before']==scene['after']
    rows=[]
    for lane in ['BODY','FACE','GAZE','HAIR']:
        name=f'MESHY_R2_{lane}_Idle';a=actions[name]
        curve_hash=inventory['fingerprints']['actions'][name]
        assert curve_hash==scene['before']['actions'][name]
        expected='KEY' if lane=='FACE' else 'OBJECT'
        assert a['slots']==[['KELegacy Slot' if lane=='FACE' else 'OBLegacy Slot',expected]]
        assert a['range']==[1.0,73.0]
        rows.append({'exact_original_Action':name,'lane':lane,'original_curve_fingerprint':curve_hash,'slot_identifier':a['slots'][0][0],'target_id_type':expected,'Action_frame_range':a['range'],'recorded_source_fps':inventory['fps'],'fps_base':'NOT_RECORDED_BY_THIS_INVENTORY','effective_fps':'CONFIRM_BEFORE_EXPORT','provisional_duration_at24fps_seconds':3.0,'source_endpoint_frames':[1,73],'two_cycle_sample_policy_if_endpoint_closure_proven':'73 first-cycle inclusive samples, then source2..73 for cycle2 =145samples/6s at24fps; no duplicate seam frame1','endpoint_loop_closure':'NOT_MEASURED','actual_target_ID_name_and_binding':'NOT_IDENTIFIED_BY_GENERIC_LEGACY_SLOT_INVENTORY','slot_handle_channelbag_paths':'NOT_RECORDED; must inspect actual slot/channelbag/ID relation before assigning','prior_FBXTakes_include_this_Action':False,'source_neutral_ON_motion_face_gaze_hair_native_qa':'NOT_PERFORMED_FOR_THIS_4_ACTION_COMBINATION','runtime_alias':'NONE_PROPOSED'})
    assert all(t['authored_Action'].startswith('YRA_R4_') for t in existing_takes)
    muted=[d for d in inventory['drivers'] if d['mute']]
    assert len(muted)==13
    deferred=[]
    for take in ['HeadGazeHair','Reach','Wave']:
        for lane in ['BODY','FACE','GAZE','HAIR']:
            name=f'MESHY_R2_{lane}_{take}'
            deferred.append({'exact_original_Action':name,'original_range':actions[name]['range'],'recorded_slot':actions[name]['slots'],'scope':'DEFERRED_UNTIL_EXPLICIT_PRODUCT_TRIGGER_NEED; presence only, not accepted playback'})
    result={'status':'FILE_ONLY_ORIGINAL_LIVING_MINIMAL_INTAKE_PLAN_NOT_EXPORTED_NOT_PLAYBACK_PASS','inputs':inputs,'canonical_source_sha256':inventory['source_sha256'],'minimum_requested':rows,'rig_ID_inventory':[{'exact_Object_ID':n,'parent_ID':r['parent'],'original_bones':len(r['bones'])} for n,r in inventory['rigs'].items()],'original_total_bones':137,'original_Actions_preserved':78,'source_material_count':len(inventory['materials']),'original_muted_bridges_preserved':muted,'actual_binding_limitation':'Slots indicate OBJECT versus KEY only, not unique target Object/Key. Repeated generic identifiers are not aliases or proof of playback. FACE is KEY data, not automatically AVATAR_FaceBoard rig animation. GAZE/HAIR targets cannot be assigned by lane name.','known_existing_exporter':{'script':str(script),'settings':exporter['settings'],'native_basis':exporter['native_basis'],'coverage':'Exactly6 reaction BODY Actions; auxiliary rig bones are sampled/static, not original Living FACE/GAZE/HAIR Action proof. Animation-only file selects no meshes; KEY/morph animation compatibility is unproven.','can_reuse':'Immutable native hierarchy/137bone/rest/selection restoration and object animation serializer after actual target binding established.','cannot_claim':'No exact original Living target/take/shapeKey driver/gaze/hair/native endpoint evidence. Existing carrier/GameRig is compatibility reference only, not canonical appearance.'},'deferred_takes':deferred,'required_before_activation_or_export':['Exact Action slot handle/channelbag paths and intended Object/Key IDs, targetRNA availability; no fallback to arbitrary first OBJECT slot','Record actual current Action/slot/NLA/pose/key values, original rest/weights/material/driver/mute signature; do not unmute13 bridges','Confirm fps/fps_base and native range/endpoints; full normal-speed Idle2cycles across BODY/FACE/GAZE/HAIR independently then combined','Verify expected actual body/face/key/gaze/hair changes; source-neutral before/after unchanged and full scene/input SHA preserved'], 'proposed_bounded_export':{'authorization':'NOT_AUTHORIZED; exact saved native script/argv/new fixed Job route must be prepared and reviewed separately','scope':'Resolve only4 exact original Idle slots/targets first. If valid, sample native4rig poses and originalKEY/driver/gaze outputs at source1..73 plus two-cycle endpoint QA; preserve source unchanged.','outputs':'Action/NLA-only library carrying existing Actions+slot metadata without objects/geometry; animation-only FBX only for resolved OBJECT channels on original rig/ancestors; separate native evaluated KEY/face/gaze/hair semantic-channel receipt if FBX cannot carry originals without changing appearance. No new curves or driver reconstruction.','forbidden':'No model re-export required for Idle intake; no new GameRig/mesh merge/neutral substitution/donor face/unmuting/deleting drivers/normalizing weights/rest changes','execution_budget_proposal':'One CPU-only installed factory/offline bounded Job, two threads/active1/affinity3/8GiB, unchanged resource floors; estimate120s sampling/export requires review, failure no retries. No launch under this planning receipt.','stop_condition':'Ambiguous target binding, absent targetRNA, channel mismatch, KEY compatibility unknown or original endpoint failure => retain evidence, no fabricated alias/exportPASS'},'Laptop_receipts_required':['Private packet exact bytes/SHA/CRC and exact source/Action identities','Original take IDs→imported take/slot/targetIDs verified on actualruntime; include KEY semantic paths separately','state entered/time advanced/weight>0/AlwaysAnimate, expected body+face+gaze+hair changes with native reference','normal-speed continuous Idle2cycles, endpoint seam/neutral restore/mesh and material fidelity; render/playback not screenshots alone','137bones/rest/fullweights/native material/node/texture/ShapeKeys/drivers/muted bridge preservation plus precise unsupported terms','head/gaze/pointer/slider effects assessed separately; genericAlive label or nonzero RigTransform stream is not acceptance'],'no_Blender_launch_export_or_product_write':True,'product_status':'ORIGINAL_LIVING_FACE_GAZE_INTEGRATION_NOT_ACCEPTED; PM confirms current neutral+6reaction only'}
    E.mkdir(parents=True)
    with (E/'ORIGINAL_LIVING_INTAKE_PLAN_R1.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
    print(json.dumps({'status':result['status'],'minimum_actions':[r['exact_original_Action'] for r in rows],'slots':[[r['slot_identifier'],r['target_id_type']] for r in rows],'target_binding':'UNKNOWN_FROM_EXISTING_GENERIC_SLOTS','original137bones':True,'muted_bridges':len(muted),'existingLivingFBXTakes':0}))

if __name__=='__main__':main()
