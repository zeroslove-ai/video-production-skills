"""Cached-only hidden lid guide / visible pigment dependency support; no native calls."""
from pathlib import Path
import gzip,hashlib,json,zipfile
LAB=Path(__file__).resolve().parent.parent
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
RAW=BASE/'o1-original-idle-sampling-r3/RAW_FINGERPRINT_INPUTS_BEFORE_PRIVATE_R3.json.gz'
E=LAB/'evidence/o1-lid-owner-visibility-causal-support-r1';OUT=BASE/'o1-lid-owner-visibility-causal-support-r1'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def main():
    assert not E.exists() and not OUT.exists()
    with gzip.open(RAW,'rt') as f:raw=json.load(f)
    slots=load(LAB/'evidence/o1-source-fidelity-recovery-r1/mesh_slot_UV_attributes_shape_deltas.json')
    binds=load(LAB/'evidence/o1-native-unity-probe-r1/source_renderers_bind.json')
    graphs=load(LAB/'evidence/o1-source-fidelity-recovery-r1/executable_material_graphs.json')
    rows=[];keynames=[]
    for side in ['L','R']:
        name='LidMarginRefine.'+side;o=raw['objects'][name];mesh=o['props']['data'][1]
        k=next((n,k) for n,k in raw['Keys'].items() if k['props'].get('user')==['Mesh',mesh])
        keynames.append(k[0]);assert o['props']['hide_render'] is True and o['props']['hide_viewport'] is False
        assert len(k[1]['anim']['drivers'])==8 and o['anim'] is None
        m=raw['mesh_attributes'][mesh]
        rows.append({'object':name,'props':o['props'],'custom':o['custom'],'materials':o['materials'],'modifiers':o['modifiers'],'constraints':o['constraints'],'object_anim':o['anim'],'Key_ID':k[0],'Key':k[1],'source_vertices':len(m['vertices']),'source_polygons':len(m['polygons']),'raw_mesh_source_SHA':hashlib.sha256(json.dumps(m,separators=(',',':')).encode()).hexdigest(),'renderer_NPZ_in_existing21':next((r['file'] for r in slots if r['renderer']==name),None)})
    assert keynames==['Key.014','Key.015']
    visible_names=[n for n,o in raw['objects'].items() if any(x in n for x in ['LashRootRepair.','OriginalMedialLashes.','LowerLashesClean.']) and o['props']['hide_render'] is False]
    mats=['Face_Lash_Pigment','Face_LowerLash_Pigment','ContinuousEyeSkin.L','ContinuousEyeSkin.R']
    # Bounded exact reference search: objects and original cached node-group graph.
    group=load(LAB/'evidence/model-handoff-r4/materials_textures.json').get('node_groups',{})
    targets={r['object'] for r in rows}|set(keynames)|{r['props']['data'][1] for r in rows}
    references=[]
    def visit(v,path):
        if isinstance(v,dict):
            for k,x in v.items():visit(x,path+[k])
        elif isinstance(v,list):
            if len(v)==2 and v[0] in ['Object','Key','Mesh'] and isinstance(v[1],str) and v[1] in targets:references.append({'path':path,'ID':v})
            else:
                for i,x in enumerate(v):visit(x,path+[i])
    visit(raw['objects'],['objects']);visit(group,['node_groups']);visit(raw['Keys'],['Keys'])
    external=[r for r in references if not (r['path'][0]=='objects' and r['path'][1] in targets) and not (r['path'][0]=='Keys' and r['path'][1] in keynames)]
    private={'source_sha256':'a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa','hidden_guides':rows,'visible_lash_owners':{n:raw['objects'][n] for n in visible_names},'visible_owner_rest_bind_NPZ':[{'bind':b,'NPZ':next((r['file'] for r in slots if r['renderer']==b['name']),None)} for b in binds if b['name'] in visible_names],'visible_material_graphs':{n:graphs[n] for n in mats},'reference_scan':references,'external_references_in_scope':external}
    assert not external,'Unexpected indirect dependency: record before cause conclusion'
    # Native existing full145 already includes guide geometry and Key outputs; no new NPZ/subset export.
    first_geometry=None;key_output_verified={n:0 for n in keynames}
    with gzip.open(BASE/'o1-original-idle-sampling-r3/FRAMES_PRIVATE_R1.jsonl.gz','rt') as f:
        for i,line in enumerate(f):
            r=json.loads(line)
            for name in keynames:assert any(k['Key']==name for k in r['Keys']);key_output_verified[name]+=1
            if i==0:first_geometry=[g for g in r['geometry'] if g['object'] in {x['object'] for x in rows}]
    assert len(first_geometry)==2 and all(v==145 for v in key_output_verified.values())
    private['existing145_custody']={'guide_frame1_geometry_records':first_geometry,'guide_Key_output_frames':key_output_verified,'full_zip_bytes':365787042,'full_zip_sha256':'935f3b6e300d4c5ace9f44215137a9d82d7654ecd5659337de1ba4b66838b30e','receiver':'PM confirmed existing Laptop R3 actual local custody; no duplicate full packet'}
    E.mkdir(parents=True);OUT.mkdir(parents=True)
    p=OUT/'LID_GUIDE_VISIBLE_PIGMENT_INPUTS_PRIVATE_R1.json'
    with p.open('x',encoding='utf8') as f:json.dump(private,f,indent=2)
    public={'player_visible_delta':'새 Windows 기능 없음; missingLidMargin owner가 original rendered pigment owner인지 구분 완료','source_SHA':private['source_sha256'],'actual_hidden_guide_facts':[{'object':r['object'],'mesh':r['props']['data'][1],'hide_render':r['props']['hide_render'],'hide_viewport':r['props']['hide_viewport'],'parent':r['props']['parent'],'material':r['materials'][0][0],'Key_ID':r['Key_ID'],'Key_block_names':[b[0] for b in r['Key']['blocks']],'driver_count':8,'input_owner':'Key FaceControls_TEST_Jaw_Smile.001; Blink.'+s,'source_vertices':r['source_vertices'],'source_polygons':r['source_polygons'],'source_purpose':r['custom'].get('Purpose'),'NPZ_status':'NOT_PRESENT_IN_ORIGINAL21_RENDERER_PACKET; cached raw original mesh and full145 native geometry/Key outputs present'} for r,s in zip(rows,['L','R'])],
      'visibility_caveat':'hide_renderTrue excludes direct Cycles normal render. hide_viewportFalse alone does not prove per-viewlayer visibility: hide_get/exclude not cached. Scan finds no external guide Object/Key/Mesh references within raw Object/Key and cached node_groups; not a universal dependency proof.',
      'visible_lash_owner_names':visible_names,'visible_lash_materials':['Face_Lash_Pigment','Face_LowerLash_Pigment'],'pigment_fact':'Both are untextured dark brown source Principled materials with Metallic0. White/silver output needs actual material slot/shader uniform/color pipeline witness, not inferred guide omission.',
      'visible_lid_materials':['ContinuousEyeSkin.L','ContinuousEyeSkin.R'],'material_color_chain':'Linked shader BaseColor comes from R3 soft warm fold and Blink texture corrective/masked source texture; white unlinked Principled BaseColor default is not final source output.',
      'material_driver_fields':[{'material':n,'path':d[0],'index':d[1],'source_owner_ID':'FaceControls_TEST_Jaw_Smile.001','input_path':'key_blocks["Blink.'+s+'"].value'} for n,s in [('ContinuousEyeSkin.L','L'),('ContinuousEyeSkin.R','R')] for d in graphs[n]['node_graph']['animation']['drivers']],
      'source_attributes':['R3_LidPigmentMask.L','R3_LidPigmentMask.R','R3_AnatomicalFold.L','R3_AnatomicalFold.R','neck_rest_position'],
      'NPZ_custody':'No new NPZ/export. Full source original raw BEFORE and native145 guide records/Key014015 are already in verified receiver935f3 ZIP. Visible lash owner NPZ paths/bytes/SHA retained in focused private extract.',
      'missing_witnesses':['Actual Player white boundary pixel owner/slot segmentation at closed-eye frame32','Runtime material IDs/uniforms for visible upper/lower lashes and ContinuousEyeSkin slot3/4 vs source links','Evaluated Blink texture corrective/fold material driver inputs and sourcePOINT-mask interpolation at exact same blink/gaze/frame','Per-viewlayer hide_get/collection exclude only if source viewport guide visibility needs reproduction; not required to establish hide_renderTrue'],
      'next_distinguishing_test':'Existing Laptop writer holds geometry/pose/camera/frame fixed at open/closed states, records visible boundary renderer/material-slot identity and exact linked eyelid-color driver outputs. Compare visible dark lash pigment/default vs actual bound shader; test sourceContinuousEyeSkin live color path with nativeBlink/masks separately. Keep hidden guides hidden; adding them does not reproduce originalnormal render.',
      'cause_verdict':'Missing LidMarginRefine is not a demonstrated cause of visible artifact; direct source-render contribution excluded by hide_renderTrue. Visible material/slot/driver path mismatch remains hypothesis, needs witness. FACE16 curve agreement does not certify shader drivers/pigment.',
      'private_extract':{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)},'raw_source_custody':{'path':str(RAW),'sha256':sha(RAW)},'native_runs_exports_source_edits':0,'guard_PBR_fullappearance':'HOLD_UNCHANGED'}
    with (E/'LID_OWNER_VISIBILITY_CONTRACT_R1.json').open('x',encoding='utf8') as f:json.dump(public,f,indent=2)
    packet=OUT/'YURI_LID_OWNER_VISIBLE_PIGMENT_CONTRACT_R1.zip'
    with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:z.write(p,p.name);z.write(E/'LID_OWNER_VISIBILITY_CONTRACT_R1.json','LID_OWNER_VISIBILITY_CONTRACT_R1.json')
    with zipfile.ZipFile(packet) as z:assert z.testzip() is None and hashlib.sha256(z.read(p.name)).hexdigest()==sha(p)
    with (E/'PACKET_CUSTODY_R1.json').open('x',encoding='utf8') as f:json.dump({'path':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'CRC_private_member_SHA_verified':True,'no_duplicate_fullcapture_or_newNPZ':True},f,indent=2)
    print(json.dumps({'packet_bytes':packet.stat().st_size,'packet_sha256':sha(packet),'hidden_guides':2,'visible_lash_owners':len(visible_names),'external_refs_in_scope':len(external)}))
if __name__=='__main__':main()
