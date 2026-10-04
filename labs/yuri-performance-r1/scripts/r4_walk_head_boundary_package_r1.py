"""Seal a new private supplement once; never repack previous handoffs."""
from pathlib import Path
import json,hashlib,zipfile
LAB=Path(__file__).resolve().parents[1];B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
P=B/'alpha-walk-head-boundary-r1';D=B/'alpha-walk-head-boundary-delivery-r1';E=LAB/'evidence/walk-head-boundary-r1';G=B/'o1-walk-head-boundary-r1'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
js=lambda p:json.loads(Path(p).read_bytes())
m=js(P/'HEAD_BOUNDARY_DISCRIMINATOR_PRIVATE_R1.json');s=js(E/'HEAD_BOUNDARY_SCALAR_QA_R1.json');ui=js(D/'WHOLE_NATIVE_1X_UI_R1.json');assert len(ui)==4 and all(x['ended'] and x['error'] is None and x['playbackRate']==1 for x in ui)
old=B/'YURI_R4_NATIVE_WALK_SOURCE_ONLY_R1_20261005.zip';assert sha(old)=='6f88434a3758bb446e71b6907796e5ba61f9eeeefcc7f92d1cbc9dd5cfb50a50'
assert sha(B/'YURI_R4_APPEARANCE_PRESERVE_CORRECTION_R1.zip')=='407cda9db7b45053f8fbb3e83467fa4888db456f31ebec376e1701c70d4f2d64'
inputs=js(G/'NATIVE_GUARD_RESULT.json')['inputs_after']; assert all(sha(p)==v for p,v in inputs.items())
scope={'visual_scope':'All24 affected frames in both fixed views and both roles inspected; no new gross face/neck/hair break. Exact48 decoded image pairs equal; contact HOLD not waived.','all4_native_1x_UI_complete':True,'native_fps':24,'frames':[74,97],'TierP':0}
(E/'WHOLE_NATIVE_1X_VISUAL_SCOPE_R1.json').write_text(json.dumps(scope,indent=2),encoding='utf8')
entries={}
def add(p,a):
 p=Path(p);assert p.is_file() and a not in entries;entries[a]=p
for folder,prefix in [(P,'native-qa'),(D,'review'),(E,'public-qa'),(G,'guard')]:
 for p in folder.rglob('*'):
  if p.is_file():add(p,prefix+'/'+p.relative_to(folder).as_posix())
for n in ['r4_walk_head_boundary_r1.py','r4_walk_head_boundary_owned_prepare_r1.py','r4_walk_head_boundary_delivery_r1.py','r4_walk_head_boundary_package_r1.py','r4_native_walk_adapter_r1.py','r4_existing_reach_contact_closure_r1.py','r4_appearance_signature.py','r4_appearance_adapter.py','native_preservation.py']:
 add(LAB/'scripts'/n,'workflow/'+n)
ledger=B/'alpha-native-walk-source-r1/NATIVE_WALK_TRIANGLE_IDENTITIES_PRIVATE_R1.json.gz';add(ledger,'existing-walk-reference/'+ledger.name)
readme=D/'SUPPLEMENT_README_R1.md';readme.write_text('''# R4 immutable-appearance head boundary supplement

No new character or motion candidate. Original BODY-only control exactly equals existing additive transport candidate in all body/head/hair coordinates at91/92. Contact remains HOLD; original head nonrigid residual causal mechanism unresolved. Source-neutral OFF pixels exact. See public-qa report/scalars, native-qa saved failed-frame coordinates and anatomical ledger, guard terminal receipts, review original24fps1x segment74..97.

This supplement is evidence/workflow; reusable source/Actions/Blender adapter are in the unchanged self-contained YURI_R4_NATIVE_WALK_SOURCE_ONLY_R1_20261005.zip SHA6f88434a3758bb446e71b6907796e5ba61f9eeeefcc7f92d1cbc9dd5cfb50a50. Do not append geometry/rig/materials, alter driver/rest/weights/texture strings, or promote appearance. No Unity runtime implementation. Protected GUI/GPU/product repositories untouched. Original files/closed packets not overwritten.
''',encoding='utf8');add(readme,'SUPPLEMENT_README_R1.md')
index={'verdict':s['verdict'],'source_SHA':m['source_SHA'],'old_candidate_SHA':m['old_candidate_SHA'],'old_library_SHA':m['old_library_SHA'],'old_walk_packet_SHA':sha(old),'members':[{'path':a,'bytes':p.stat().st_size,'sha256':sha(p)} for a,p in sorted(entries.items())]};ip=D/'PACKET_INDEX_R1.json';ip.write_text(json.dumps(index,indent=2),encoding='utf8');add(ip,'PACKET_INDEX_R1.json')
z=B/'YURI_R4_WALK_HEAD_BOUNDARY_SUPPLEMENT_R1_20261005.zip'
with zipfile.ZipFile(z,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for a,p in sorted(entries.items()):f.write(p,a)
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None
 for x in index['members']:
  v=f.read(x['path']);assert len(v)==x['bytes'] and hashlib.sha256(v).hexdigest()==x['sha256']
r={'packet':str(z),'sha256':sha(z),'bytes':z.stat().st_size,'members':len(entries),'indexed_members':len(index['members']),'CRC_SHA_size_all_verified':True,'closed_once':True,'old_walk_packet_unchanged':True,'source_SHA':m['source_SHA'],'new_candidate':None,'verdict':s['verdict'],'TierP':0};(E/'PRIVATE_PACKET_RECEIPT_R1.json').write_text(json.dumps(r,indent=2),encoding='utf8');print(json.dumps(r,indent=2))
