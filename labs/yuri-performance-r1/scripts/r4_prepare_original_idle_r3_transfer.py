"""File-only existing private Drive route: lossless64MiB chunks plus source contract."""
from pathlib import Path
import hashlib,json,zipfile
LAB=Path(__file__).resolve().parent.parent
E=LAB/'evidence/o1-original-idle-sampling-result-r3'
OUT=Path('C:/YuriTransfer/outbox/YURI_O1_IDLE_R3_935f3b6e300d')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    assert not OUT.exists()
    report=json.loads((E/'INDEPENDENT_DATA_CUSTODY_R3.json').read_bytes())
    original=Path(report['private_packet']['path']);OUT.mkdir(parents=True)
    parts=[];full=hashlib.sha256();chunk=64*1024**2
    count=(original.stat().st_size+chunk-1)//chunk
    with original.open('rb') as f:
        for i in range(1,count+1):
            data=f.read(chunk);full.update(data)
            p=OUT/f'YURI_ORIGINAL_IDLE_R3_935f3b6e300d.zip.part{i:02d}-of-{count:02d}'
            with p.open('xb') as out:out.write(data)
            parts.append({'path':str(p),'name':p.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        assert f.read(1)==b''
    assert full.hexdigest()==report['private_packet']['sha256']
    summary=json.loads((LAB/'evidence/o1-original-idle-slot-graph-result-r2/INDEPENDENT_IDLE_GRAPH_BINDING_SUMMARY_R2.json').read_bytes())
    contract={'user_capability':'새 사용자 기능 없음; PM 승인된 isolated O1-I1 Idle 구현/비교용 원본 데이터 공급 준비. strict whole guardFAIL/finalpromotionHOLD.',
      'source_sha256':report['source_SHA'],'whole_guard':'FAIL_STRICT_LIVE_IMAGE_ERROR5_NOT_WAIVED','data_only_scope':'Independent full145/rawOFFrestore/custody verified; PM authorizes isolated Laptop O1-I1 contract/consumer/comparison only',
      'canonical_geometry_rule':'Immutable original source; full native meshes/poses reference/comparison only, no frozen geometry/pose injection',
      'original_bindings_and_all_RNA_curves':summary['Action_slot_candidate_table'],
      'actual_private_data_members':report['private_packet']['members'],
      'frame_contract':{'frames':[1,145],'fps':24,'fps_base':1,'samples':145,'continuously_evaluated_original_CYCLES':True,'manual_modulo_alias_clamp_subset':False,'loop_quality_verdict':'NOT_ACCEPTED; inspect full145 orientation/driver/root/geometry and velocities'},
      'dependencies':{'BODY':'364curves/52animated, all57native rest/pose helpers; noforce scale1',
       'FACE_Blink':'16originalKeychannels,72headKeyoutputs plus all otherKeys/drivers; Blink.L/Blink.R retained; muted FACE NLA graph preserved',
       'GAZE':'Face_GazeYaw/Face_GazePitch native values/UI metadata plus actual driver dependencies and evaluated geometry; no normalization/[-1,1] clamp',
       'HAIR':'Pony_Sway/Pony_Lift/Tip_Curl/Side_Sway native UI/driver dependency/10bones14drivers/restattachmentbasis',
       'all_graph':'4rig137/78Actions/original66/fullweights/rest/materials/ShapeKeys/all13mutes preserved'},
      'payload_files':{'ORIGINAL_CURVES_AND_MODIFIERS_PRIVATE_R1.json':'Actual native numeric keyframes/Bezier interpolation/fullCYCLES modes',
       'ORIGINAL_DRIVER_GRAPH_PRIVATE_R1.json':'Original evaluated outputs/driver expressions/variables/targets',
       'ORIGINAL_PROPERTY_AND_REST_METADATA_PRIVATE_R1.json':'OriginalUIpropertyvalues/default/ranges/restparentmatrices; absentunitsUNKNOWN',
       'ORIGINAL_BINDING_KEY_INPUTS_PRIVATE_R1.json':'OriginalKeysliderlimits/values/AnimData/NLA graph',
       'FRAMES_PRIVATE_R1.jsonl.gz':'All145 fourdomainscurvevsRNA/all137poses/allKeys/allDrivers/objecttransforms/geometryindex',
       'ALL_MESH_NATIVE_LOCAL_F32_PRIVATE_R1.bin.gz':'Native fullgeometry forreference only; indexed byframe/object uncompressedoffsets, littleendianf32'},
      'private_zip':report['private_packet'],'transport':'Concatenate exact parts in ordinal order; total bytes+SHA must match original ZIP; CRC/allmemberSHA then verify input contract',
      'Drive_folder_id':'1sazEEOoVOdK7F8Ld6ZNcxwVTNyZbH0Ya','parts':parts,
      'guard_research_separation':'No fullsampler retry or weakerthreshold. WholeexecutionFAIL remains separate from independentlyverified data restoration and permitted isolated consumer work.'}
    meta=OUT/'O1_I1_ORIGINAL_IDLE_R3_SOURCE_CONTRACT.json'
    with meta.open('x',encoding='utf8') as f:json.dump(contract,f,indent=2)
    packet=OUT/'O1_I1_ORIGINAL_IDLE_R3_CONTRACT_935f3b6e300d.zip'
    with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
        z.write(meta,meta.name)
        for p in [E/'INDEPENDENT_DATA_CUSTODY_R3.json',LAB/'evidence/o1-original-idle-sampling-preparation-r3/O1_I1_SOURCE_DEPENDENCIES_R3.json']:
            z.write(p,p.name)
    with zipfile.ZipFile(packet) as z:assert z.testzip() is None
    manifest={'status':'PREPARED_PRIVATE_OWNER_ONLY_TRANSFER; NOT_UPLOAD_RECEIPT','full_zip_sha256':full.hexdigest(),'full_zip_bytes':original.stat().st_size,'part_order':parts,'contract_zip':{'path':str(packet),'name':packet.name,'bytes':packet.stat().st_size,'sha256':sha(packet)},'folder_id':contract['Drive_folder_id'],'source_model_reexport_or_delivery':False,'whole_guard':'FAIL_PRESERVED','isolated_O1_I1_data_authorization':'PM explicitly authorized independently verified full original data for isolated consumer/comparison; no finalcanonicalproductionacceptance'}
    with (E/'PRIVATE_TRANSFER_PLAN_R3.json').open('x',encoding='utf8') as f:json.dump(manifest,f,indent=2)
    print(json.dumps({'parts':count,'contract_bytes':packet.stat().st_size,'all_parts_bytes':sum(p['bytes'] for p in parts)}))
if __name__=='__main__':main()
