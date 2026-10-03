"""Read frozen metadata/source only. No bpy, network, subprocess or acquisition."""
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
E = ROOT / 'evidence/o1-source-smooth-lineage-r1'
assert not E.exists(), 'immutable additive evidence; choose a new revision'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
inventory = OUT / 'o1-source-fidelity-recovery-r1/metadata/mesh_slot_UV_attributes_shape_deltas.json'
assert sha(inventory) == 'e76524048e1168a84b7a98aead4404f6b5cea76fe33f317234dcc21facc8de0c'
body = next(x for x in json.loads(inventory.read_text(encoding='utf8')) if x['renderer'] == 'Meshy_Body_NeutralCovered')
names = [x['name'] for x in body['attributes']]
assert len(names) == 15 and 'sharp_face' not in names and 'sharp_edge' in names
cached = OUT / 'o1-actual-cycles-readback-preparation-r1/upstream'
mesh = cached / 'intern/cycles/blender/mesh.cpp'
upstream_receipt = json.loads((ROOT/'evidence/o1-actual-cycles-readback-preparation-r1/UPSTREAM_SOURCE_RECEIPT.json').read_text(encoding='utf8'))
assert sha(mesh) == upstream_receipt['intern/cycles/blender/mesh.cpp']['sha256']
policy = 'std::fill(smooth, smooth + numtris, normals_domain != blender::bke::MeshNormalDomain::Face);'
assert policy in mesh.read_text(encoding='utf8')
mods = body['modifiers']
assert [m['type'] for m in mods] == ['ARMATURE','ARMATURE','CORRECTIVE_SMOOTH','SMOOTH','SMOOTH','SMOOTH','SMOOTH']
mod_sources = OUT/'o1-body-modifier-source-contract-r1/upstream'
registrations = []
for name in ('MOD_armature.cc','MOD_correctivesmooth.cc','MOD_smooth.cc'):
    p = mod_sources/name
    text = p.read_text(encoding='utf8')
    assert '/*type*/ ModifierTypeType::OnlyDeform,' in text
    registrations.append({'path':str(p),'sha256':sha(p),'registration':'ModifierTypeType::OnlyDeform'})
writer = ROOT/'scripts/r4_recovery_source_data.py'
assert "for i,a in enumerate(m.attributes):" in writer.read_text(encoding='utf8')
v5 = ROOT/'scripts/native_readback_proposal/staged_native_acquisition_v5.py'
template = ROOT/'evidence/o1-owned-job-and-acquisition-v5-r1/ACQUISITION_REVIEW_TEMPLATE_NOT_APPROVED.json'
approval = json.loads(template.read_text(encoding='utf8'))
assert approval['human_large_resource_acquisition_approved'] is False
assert sha(v5) == approval['acquisition_script_sha256']
row = {
 'status':'SOURCE_LINEAGE_VERIFIED_EVALUATED_NATIVE_CAPTURE_PENDING',
 'source_inventory':{'path':str(inventory),'sha256':sha(inventory),'renderer':body['renderer'],'attribute_names':names},
 'inventory_writer':{'path':str(writer),'sha256':sha(writer),'operation':'original o.data.attributes enumeration; nonempty attribute rows exported before ReactionLane evaluation; not evaluated smooth capture'},
 'ordered_modifiers':[{'order':x['order'],'name':x['name'],'type':x['type']} for x in mods],
 'modifier_type_registration':registrations,
 'cycles_policy':{'path':str(mesh),'sha256':sha(mesh),'receipt':upstream_receipt['intern/cycles/blender/mesh.cpp'],'empty_sharp_faces_branch':policy},
 'scope':{'original_sharp_face_absent':'VERIFIED_FROZEN_INVENTORY','non_topology_changing_modifier_types':'VERIFIED_REGISTRATIONS','all_smooth_expected':'CONDITIONAL_ON_EVALUATED_NORMALS_DOMAIN_NOT_FACE_AND_SHARP_FACE_REMAINING_ABSENT','actual_evaluated_normals_domain':'NOT_CAPTURED_HERE','actual_evaluated_sharp_face':'NOT_CAPTURED_HERE','actual_native_smooth_array':'NOT_CAPTURED_HERE'},
 'prior_r2_smooth_provenance':'Preserved unchanged; shorthand absent sharp_faces => smooth true is qualified by exact normals_domain condition here. Expected all-ones remains a diagnostic expectation, never runtime replacement data.',
 'acquisition':{'helper':str(v5),'sha256':sha(v5),'approval_template':str(template),'approval_template_sha256':sha(template),'owner_approval':False,'known_payload_bytes':7054121984,'extra_git_transport_bytes':'UNKNOWN','dry_command':f"& 'C:\\Program Files\\Python313\\python.exe' '{v5}'",'post_real_approval_command':f"& 'C:\\Program Files\\Python313\\python.exe' '{v5}' --execute --approval 'C:\\YuriTransfer\\owner-reviewed-acquisition-receipt.json'",'receipt_path':'proposed exact input path; no receipt created or approval fabricated','execution_scope':'download/verify/unpack only; no build or capture'},
 'next_gates':['Real owner acquisition approval','Verify staged resources and per-file hashes','Separate owned build and compile/link validation','Postcompile guard closure and API checks','Explicit bounded native capture acceptance; actual evaluated attributes and native buffers','Unity/PBR visual acceptance remains separate'],
 'source_or_gui_or_product_mutation':False,
}
E.mkdir(parents=True)
(E/'SOURCE_SMOOTH_LINEAGE.json').write_text(json.dumps(row,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'evidence':str(E),'sha256':sha(E/'SOURCE_SMOOTH_LINEAGE.json'),'source_attribute_names':names,'status':row['status']}))
