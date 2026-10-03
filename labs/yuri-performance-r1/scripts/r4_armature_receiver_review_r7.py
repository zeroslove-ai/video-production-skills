"""Public research schema/code delivery only; excludes source model/private product code/data."""
from pathlib import Path
import hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'evidence/o1-native-armature-instrumentation-draft-r7'
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
SOURCE=BASE/'o1-native-armature-instrumentation-draft-r7'
DELIVERY=E/'receiver-review'
assert not DELIVERY.exists();DELIVERY.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((SOURCE/'SYNTHETIC_ONLY_CanonicalSchema_R7.manifest.json').read_text(encoding='utf8'))
assert manifest['classification']=='SYNTHETIC_FIXTURE_NOT_NATIVE' and len(manifest['arrays'])==65
schema={
 'purpose':'LAPTOP CONSUMER SCHEMA REVIEW ONLY; no native numeric/build/capture acceptance',
 'source_git_commit':'d02ef857e73d8a2b226422a46d9221287f6d686c',
 'original_frozen_R7_zip_SHA256':'1314692aa05bf2d62c4bb54c8fc794104a395d5adfc68b8e0627dc8cb9b638b0',
 'source_patch_SHA256':'b2ba72354e36d96f87ef98f7f7c2b1dba39a95338bff2a91f4cdeb48d64989e2',
 'original_exact_request_input_SHA256':'a46c693c28e09a93729bbe433a522d47c7a452c740a6af6ceb8868ddec370b17',
 'arrays':manifest['arrays'],
 'array_hashes_classification':'SYNTHETIC_EXAMPLE_PAYLOAD_HASHES_NOT_NATIVE; values/NPZ are not embedded in this public schema',
 'sparse_contract':manifest['sparse_contract'],
 'second_LBS_contract':manifest['second_LBS_contract'],
 'coordinate_scope':manifest['coordinate_scope'],
 'consumer_schema_agreement':'PENDING; PM requested Laptop review; no acceptance reply received',
 'review_questions':[
   'Accept deforming_bone_slots + dq_computed_valid and *_values logical [2,57] fields, without invented dense helper DQ?',
   'Accept sparse actual hemisphere events retaining all original CSR indices and explicit noncomputed sign?',
   'Accept second-LBS per-vertex/per-entry indices and NOT_COMPUTED skip mask for samples2/3/4?',
   'Confirm stage00=input before first DQ, dq_output=after first DQ, stage01=after second masked LBS; native finalize/delta primitive stays ARMATURE-space?',
   'Report precise required field/coordinate/schema amendments; numeric/world/compiler/render acceptance remains separate.'
 ],
 'no_product_writes':True,'native_numeric_acceptance':False,
}
(DELIVERY/'CANONICAL_CONSUMER_SCHEMA_R7.json').write_text(json.dumps(schema,indent=2),encoding='utf8')
shutil.copyfile(E/'SECOND_LBS_CANONICAL_SCHEMA_R7.md',DELIVERY/'SECOND_LBS_CANONICAL_SCHEMA_R7.md')
shutil.copyfile(E/'native_armature_typed_r7.patch',DELIVERY/'native_armature_typed_r7.patch')
names=['armature_canonical_pack_r7.py','armature_canonical_validate_r7.py','armature_validator_fixture_r7.py',
 'armature_owned_invocation_r7.py','armature_live_recipe_r5.py','armature_trace_unpack_r1.py','armature_trace_r4.hh.in','bpy_yuri_armature_trace_r5.hh']
for name in names:
    p=DELIVERY/'workflow'/name;p.parent.mkdir(exist_ok=True)
    shutil.copyfile(ROOT/'scripts/native_readback_proposal'/name,p)
(DELIVERY/'README.md').write_text('''# Receiver review R7

This is a PUBLIC RESEARCH code/schema review delivery, distinct from the frozen Desktop full R7 packet. It includes all65 field names/dtypes/shapes/logical shapes/per-array synthetic hashes, actual source patch and consumer/source invocation code. No source blend, source video, private product C# source, exact private request numerical payload, synthetic numeric NPZ or real native logs are embedded.

Laptop uses its existing pinned original input at8bacd64 (request SHAa46c693c...) and its own original full recipe. See CANONICAL_CONSUMER_SCHEMA_R7.json for sparse indices, validity masks, coordinate stages and explicit review questions. The fixture generator is available; invoke it against Laptop's request-inputs JSON and original57slot metadata. Fixture PASS is only consumer control-flow scope.

Source code checkpoint: https://github.com/zeroslove-ai/video-production-skills/tree/d02ef857e73d8a2b226422a46d9221287f6d686c/labs/yuri-performance-r1/evidence/o1-native-armature-instrumentation-draft-r7

No download/build/capture approval is included. Consumer agreement is pending and must be returned explicitly by Laptop/PM. This public review ZIP has its own hash; it is not the full frozen ZIP1314692a... and cannot be substituted for its custody receipt.
''',encoding='utf8')
rows=[{'path':p.relative_to(DELIVERY).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(DELIVERY.rglob('*')) if p.is_file()]
(DELIVERY/'REVIEW_MANIFEST.json').write_text(json.dumps({'classification':'PUBLIC_SCHEMA_CODE_REVIEW_ONLY','source_git_commit':schema['source_git_commit'],'files':rows},indent=2),encoding='utf8')
archive=E/'YURI_O1_ARMATURE_R7_RECEIVER_REVIEW.zip';assert not archive.exists()
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
    for p in sorted(DELIVERY.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(DELIVERY).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for row in rows:assert hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
receipt={'classification':'PUBLIC_RECEIVER_REVIEW_NOT_ORIGINAL_FROZEN_R7_PACKET','path':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive),'files':len(rows)+1,'CRC_member_hashes':'PASS','schema_fields':len(schema['arrays']),'consumer_agreement':'PENDING'}
(E/'RECEIVER_REVIEW_CUSTODY.json').write_text(json.dumps(receipt,indent=2),encoding='utf8')
print(json.dumps(receipt))
