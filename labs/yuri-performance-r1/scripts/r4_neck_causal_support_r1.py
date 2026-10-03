"""Bounded cached-file extraction for neck/material comparison; no native/API/export."""
from pathlib import Path
import hashlib,json,zipfile
LAB=Path(__file__).resolve().parent.parent
REC=LAB/'evidence/o1-source-fidelity-recovery-r1'
E=LAB/'evidence/o1-neck-material-causal-support-r1'
OUT=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-neck-material-causal-support-r1')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def main():
    assert not E.exists() and not OUT.exists()
    graphs=load(REC/'executable_material_graphs.json')
    slots=load(REC/'mesh_slot_UV_attributes_shape_deltas.json')
    binds=load(LAB/'evidence/o1-native-unity-probe-r1/source_renderers_bind.json')
    mat_names=['Material_tripo_node_b28d0c45-674e-4063-9bd8-1e071df4ba6e.001','Neck transition.001','Skin_Clean_R3','R4_Meshy_OriginalDetail_FaceMatched','Hair_Pearl_PBR']
    mesh_names=['Character_Body_Head','Meshy_Body_NeutralCovered','Hair_Replacement_R4']
    def input_of(name,socket):return next(v for p in graphs[name]['principled_inputs'] for v in p['inputs'] if v['name']==socket)
    assert input_of('Hair_Pearl_PBR','Metallic')['default']==0 and not input_of('Hair_Pearl_PBR','Normal')['sources']
    assert graphs['Hair_Pearl_PBR']['node_graph']['links']==[['Hair_Color','BSDF','Material Output','Surface']]
    head=graphs[mat_names[0]]['node_graph'];links=head['links']
    assert ['Neck Rest Position','Vector','Separate XYZ.001','Vector'] in links
    assert ['Map Range.002','Result','Principled BSDF','Roughness'] in links
    head_row=next(r for r in slots if r['renderer']=='Character_Body_Head')
    neck=next(a for a in head_row['attributes'] if a['name']=='neck_rest_position')
    assert neck['domain']=='POINT' and neck['data_type']=='FLOAT_VECTOR'
    assert head_row['material_slots'][2]=='Neck transition.001'
    E.mkdir(parents=True);OUT.mkdir(parents=True)
    selected_slots=[]
    for name in mesh_names:
        r=next(r for r in slots if r['renderer']==name)
        selected_slots.append({k:r[k] for k in ['renderer','matrix_world','material_slots','UV','attributes','modifiers','constraints','object_drivers','file']})
    private={'source_sha256':'a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa','materials_exact_native_metadata':{name:graphs[name] for name in mat_names},'renderer_slots_UV_attribute_arrays_modifier_world':selected_slots,'rest_bind_hierarchy_fullweights_pointer':[r for r in binds if r['name'] in mesh_names],'textures_original_metadata':load(LAB/'evidence/model-handoff-r4/materials_textures.json')['textures'],'source_render_equivalent':load(REC/'neutral_camera_light_color_driver_state.json'),'file_only':True}
    p=OUT/'EXACT_NECK_MATERIAL_COMPARISON_INPUTS_PRIVATE_R1.json'
    with p.open('x',encoding='utf8') as f:json.dump(private,f,indent=2)
    refs=[REC/'executable_material_graphs.json',REC/'mesh_slot_UV_attributes_shape_deltas.json',LAB/'evidence/o1-native-unity-probe-r1/source_renderers_bind.json',LAB/'evidence/model-handoff-r4/materials_textures.json',REC/'neutral_camera_light_color_driver_state.json']
    public={'player_visible_delta':'새 Windows 기능 없음; neck/material matched비교용 원본 causal 입력계약 준비', 'source_SHA':private['source_sha256'],'known_source_facts':{'head_neck_attribute':{'name':'neck_rest_position','domain':neck['domain'],'type':neck['data_type'],'array':neck['fields'][0]['array'],'source_file':head_row['file']['path'],'source_file_sha256':head_row['file']['sha256'],'source_file_bytes':head_row['file']['bytes']},'head_slot2':'Neck transition.001','head_main_graph':mat_names[0],'live_neck_color_chain':['Neck Rest Position.Vector','Separate XYZ.001.Z','Map Range.001.Result','Mix (Legacy).001','R3 feathered skin halo L','R3 feathered skin halo R','Principled BSDF.Base Color'],'live_neck_roughness_chain':['Neck Rest Position.Vector','Separate XYZ.001.Z','Map Range.002.Result','Principled BSDF.Roughness'],'unused_legacy_branch':'Separate XYZ/Map Range/Mix (Legacy) branch has no live final Base Color output in cached links; do not substitute it for .001 active color chain','head_normal_caveat':'Normal Map.Normal connected to BSDF.Normal, but no cached link feeds Normal Map.Color; inspect defaults/Strength in private graph, do not invent missing image normal connection','body_graph':'R4_Meshy_OriginalDetail_FaceMatched: separate image BaseColor, image Roughness, image Normal -> tangent NormalMap -> BSDF.Normal','hair_graph':'Hair_Color -> Material Output.Surface only; no linked texture/Normal; source Metallic0. Pearl/light hair appearance is not evidence of metallic material.','heterogeneous_materials':'Head main rest-mask graph, separate flat Neck transition.001 and baked Skin_Clean_R3, and body image/normal graph differ in original source; equality of materials cannot be assumed'},
      'exact_field_refs':{'materials':'executable_material_graphs.json[exactMaterial].principled_inputs[].inputs[name].default/sources and node_graph.nodes/links; MapRange/NormalMap/Mapping properties+input defaults preserved','neck_rest':'mesh_slot_UV_attributes_shape_deltas.json[renderer=Character_Body_Head].attributes[name=neck_rest_position].fields[property=vector].array -> original NPZ POINT array; never replace with animated world-Z','UV_slot':'same renderer .UV/.material_slots; NPZ polygon_material_slot / uv_0 indexed native corners; no vertex-UV collapse','world_bind':'source_renderers_bind.json[name].path/matrix_world/matrix_local/armature_bindings[].settings/target/target_path/bone_indices; exact Armature versus Meshy_Fitted_Rig versus Hair_Rig_R4 domains','color_light':'neutral_camera_light_color_driver_state.json.camera/lights/world/color_management; originalCYCLES vs actual Unitylighting/shader pipeline separately'},
      'source_hierarchy_targets':[{k:r[k] for k in ['name','path']}|{'armature_targets':[{'target':b['target'],'target_path':b['target_path']} for b in r['armature_bindings']]} for r in binds if r['name'] in mesh_names],
      'matched_comparison_order':['Neutral frame1/source OFF unchanged: head/body neck world-position correspondence and rest/skin/hierarchy first', 'Per source polygon slot verify active neck_rest_position-restZ mask vs shader adapter attribute/interpolation and active MapRange.001/.002', 'Compare actual hair Metallic/BaseColor/Roughness/IOR/specular and native surface normals under same light/color; separate authoredPearl from wrongmetallicflag', 'Compare body image identity/colorspace/UV, roughness sampling/conversion, tangent normal convention and actual Principled feature coverage', 'Capture actual Windows camera/light/world/exposure/color reference before attributing residual difference to geometry or provider'],
      'missing_actual_consumer_fields':['Build55 actual runtime per-renderer shader/material/property-block values including hair Metallic/roughness/BaseColor/specular and final bound slot IDs', 'Active neck_rest_position source-index/corner transport and fragment-space mask samples at exact source-corresponding neck vertices/corners', 'Matched neutral Player sourceworld vs consumerworld neck positions/bind-pose/skin/rig matrices and native normals/tangents before shader', 'Actual Player camera/light/color pipeline and captured frame provenance; build success is not Player interaction proof'],
      'minimal_request_if_needed':'Ask Laptop existingwriter for these exact runtime readbacks/matched screenshot. No Desktop native capture needed: source fields/graphs/UV/rest/bind and normal conventions already cached. Exact seam vertex correspondence remains a consumer comparison task, not a new broad inventory.',
      'causal_verdict':'UNPROVEN Unitycause; source authored dependencies enumerated. No provider-label blame, source merge/weld/edit/export, guard waiver or PBRPASS.',
      'input_custody':[{'path':str(r),'bytes':r.stat().st_size,'sha256':sha(r)} for r in refs],'private_extract':{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)},'native_runs_exports':0}
    with (E/'CAUSAL_COMPARISON_CONTRACT_R1.json').open('x',encoding='utf8') as f:json.dump(public,f,indent=2)
    packet=OUT/'YURI_NECK_MATERIAL_CAUSAL_INPUTS_R1.zip'
    with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
        z.write(p,p.name);z.write(E/'CAUSAL_COMPARISON_CONTRACT_R1.json','CAUSAL_COMPARISON_CONTRACT_R1.json')
    with zipfile.ZipFile(packet) as z:assert z.testzip() is None and hashlib.sha256(z.read(p.name)).hexdigest()==sha(p)
    with (E/'PACKET_CUSTODY_R1.json').open('x',encoding='utf8') as f:json.dump({'path':str(packet),'bytes':packet.stat().st_size,'sha256':sha(packet),'CRC_private_member_SHA_verified':True,'no_geometry_source_export':True},f,indent=2)
    print(json.dumps({'packet_bytes':packet.stat().st_size,'packet_sha256':sha(packet),'native_runs':0}))
if __name__=='__main__':main()
