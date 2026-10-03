"""Reuse actual existing source renders and receipts; no bpy/render/export."""
from pathlib import Path
import hashlib,json,zipfile
LAB=Path(__file__).resolve().parent.parent
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OLD=BASE/'r4-appearance-preserve-correction-r1'
E=LAB/'evidence/o1-normal-blender-visual-source-reference-r1'
OUT=BASE/'o1-normal-blender-visual-source-reference-r1'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def main():
    assert not E.exists() and not OUT.exists()
    prior=LAB/'evidence/r4-appearance-preserve-correction-r1'
    recovery=LAB/'evidence/o1-source-fidelity-recovery-r1'
    camera=load(prior/'neutral_authority_manifest.json')
    state=load(recovery/'neutral_camera_light_color_driver_state.json')
    inventory=load(LAB/'evidence/model-handoff-r4/R4.json')
    slots=load(recovery/'mesh_slot_UV_attributes_shape_deltas.json')
    assert camera['source_sha256']==inventory['source_sha256']=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
    assert state['neutral']['frame']==camera['neutral_frame']==1
    images=[OLD/'neutral'/f'{kind}_{phase}.png' for kind in ['authority_source_camera','full_body_QA'] for phase in ['before','after_OFF','after_ON_then_OFF']]
    assert all(p.exists() for p in images)
    existing=BASE/'YURI_R4_APPEARANCE_PRESERVE_CORRECTION_R1.zip'
    receipt=load(prior/'bundle_receipt.json');assert sha(existing)==receipt['sha256']
    with zipfile.ZipFile(existing) as z:
        for p in images:assert hashlib.sha256(z.read('neutral/'+p.name)).hexdigest()==sha(p)
    renderer_metadata=[]
    for name in ['Character_Body_Head','Meshy_Body_NeutralCovered','Hair_Replacement_R4']:
        v=inventory['meshes'][name];detail=next(r for r in slots if r['renderer']==name)
        renderer_metadata.append({'object':name,'source_vertices':v['vertices'],'source_polygons':v['polygons'],'parent':v['parent'],'material_slots':v['materials'],'UV_layers':v['uv_layers'],'geometry_SHA':v['geometry_sha'],'weights_SHA':v['weights_sha'],'ShapeKey_names':list(v['shape_keys']),'modifier_order':[{'order':m['order'],'name':m['name'],'type':m['type'],'armature_target':m['settings'].get('object'),'preserve_volume':m['settings'].get('use_deform_preserve_volume'),'mask':m['settings'].get('vertex_group')} for m in detail['modifiers']],'attribute_names':[a['name'] for a in detail['attributes']],'native_coordinates_scale_rest_bind_fullvalues':'Existing private source/bind/slotUV/bodymodifier/CSR packets; no matrix decomposition or provider-label substitution'})
    pointers=[LAB/'evidence/o1-native-unity-probe-r1/source_renderers_bind.json',LAB/'evidence/o1-native-unity-probe-r1/source_expanded_rigs.json',LAB/'evidence/o1-native-unity-probe-r1/source_driver_graph.json',recovery/'mesh_slot_UV_attributes_shape_deltas.json',recovery/'neutral_camera_light_color_driver_state.json']
    manifest={'user_visible_delta':'새 Windows 기능 없음; 실제 기존 Blender neutral 이미지와 source 비교 조건을 제공해 neck/material/face defect stage 진단 준비',
      'source_SHA':camera['source_sha256'],'actual_images_inspected':True,'visual_observation':'Source-camera actual PNG shows original face/hair/neck/shoulders; no gross neck detachment visible in this frame. 8sample CPU noise and single view do not certify subtle seam or Windows appearance. Fullbody256x384 provides framing/silhouette reference only.',
      'images':[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p),'member_in_existing_private_packet':'neutral/'+p.name} for p in images],
      'source_action_state':'Original source loaded with use_scripts=False, original frame1/pose/bindings; no new Action assigned for BEFORE neutral. Explicit ON_then_OFF is old corrective Reaction trial, not original Idle145 render.',
      'provenance_workflow':{'path':'scripts/r4_appearance_qa.py','sha256':sha(LAB/'scripts/r4_appearance_qa.py'),'render_overrides':camera['render_overrides_only'],'source_camera':camera['camera'],'source_resolution':camera['source_resolution'],'fullbody_override':camera['full_body_QA_override_only'],'world':camera['world'],'lights_exact_metadata_pointer':'neutral_authority_manifest.json','color_management':state['color_management'],'color_capture_scope':'Later same-source neutral native metadata; renderer setup leaves color state unchanged. Historical PNG does not itself contain a full color-state readback; no invented render-time receipt.'},
      'pixel_comparison':load(prior/'pixels_authority_source_camera.json'),
      'existing_owner_only_Drive_packet':{'id':'1eCbLylN5wYoM7WPwzbjBP_wLp0IGRRZK','bytes':receipt['bytes'],'sha256':receipt['sha256'],'metadata_readback_owner_only':True,'duplicate_source_export_upload':False},
      'mixed_lineage':'Owner-described Tripo head/hair versus Meshy body retained in immutable original source; measured Object/rig/material/attribute domains listed individually. Provider label is not a defect cause conclusion.',
      'renderer_source_metadata':renderer_metadata,
      'exact_private_receipt_pointers':[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in pointers],
      'comparison_stages':['Same neutral source frame1/bindings and source properties; actualPNG plus native evaluated world geometry', 'Importer rest hierarchy/scale/world transforms/source vertex+corner identity+allweights; detect positional/neck boundary mismatch first', 'Runtime source rest/bone/mask/modifier order; body/head/hair native outputs versus consumer before shader', 'Slot/UV/vertexattribute/texture/node dependency and native normal/tangent conventions at neck transition; compare material-constant test only in product-owned adapter', 'Matched source-camera ORTHO0.24/viewAgX/MediumHighContrast/exposure0.25/lights/world; final WindowsPlayer actual frame'],
      'neck_boundary_policy':'Use original neck_rest_position/source vertex attributes, original Neck transition.001 material slot and independent head/body mesh topology/bind/weights. Existing receipts are available; no newly measured exact seam vertex set is claimed; no welding/body replacement to hide mismatch.',
      'next_one_task':'Laptop matched neutral source-camera Windows capture plus source world-position/slot/UV/rest/skin pipeline checkpoint to locate neck/material/face divergence, preserving source hierarchy; no Desktop Unity implementation.',
      'native_render_export_launches_this_step':0,'WindowsPlayer_visual_PASS':False,'guard_fullsampler':'R3 strictFAIL research separated; independent original data restoration available for PM-authorized isolated comparison'}
    E.mkdir(parents=True);OUT.mkdir(parents=True)
    with (E/'ACTUAL_BLENDER_REFERENCE_PROVENANCE_R1.json').open('x',encoding='utf8') as f:json.dump(manifest,f,indent=2)
    packet=OUT/'YURI_EXISTING_BLENDER_VISUAL_SOURCE_REFERENCE_R1.zip'
    files=images+[prior/'neutral_authority_manifest.json',prior/'pixels_authority_source_camera.json',prior/'pixels_full_body_QA.json',prior/'preservation_receipt.json',recovery/'neutral_camera_light_color_driver_state.json',E/'ACTUAL_BLENDER_REFERENCE_PROVENANCE_R1.json']
    with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,p.name)
    with zipfile.ZipFile(packet) as z:
        assert z.testzip() is None
        for p in files:assert hashlib.sha256(z.read(p.name)).hexdigest()==sha(p)
    with (E/'PACKET_CUSTODY_R1.json').open('x',encoding='utf8') as f:json.dump({'status':'EXISTING_ACTUAL_RENDER_REUSE_PROVENANCE_ONLY_NO_NEW_NATIVE_RUN','path':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'CRC_member_SHA_verified':True,'source_model_reexport':False},f,indent=2)
    print(json.dumps({'packet_bytes':packet.stat().st_size,'packet_sha256':sha(packet),'images':len(images),'native_runs':0}))
if __name__=='__main__':main()
