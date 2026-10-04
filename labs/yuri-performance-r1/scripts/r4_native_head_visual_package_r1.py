"""Close one private narrow source reference; no source/old-packet rewrite."""
from pathlib import Path
import json,hashlib,zipfile
LAB=Path(__file__).resolve().parents[1];B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');P=B/'alpha-native-head-visual-source-r1';D=B/'alpha-native-head-visual-delivery-r1';E=LAB/'evidence/native-head-visual-source-r1';G=B/'o1-native-head-visual-source-r1';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();js=lambda p:json.loads(Path(p).read_bytes())
m=js(P/'NATIVE_HEAD_VISUAL_SOURCE_PRIVATE_R1.json');ui=js(D/'WHOLE_NATIVE_1X_UI_R1.json');assert len(ui)==2 and all(x['ended'] and x['error'] is None and x['playbackRate']==1 for x in ui)
assert sha(m['source'])==m['source_SHA'] and m['full_raw_OFF_snapshot_equal'];g=js(G/'NATIVE_GUARD_RESULT.json');assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN' and all(sha(p)==v for p,v in g['inputs_after'].items())
for old,expected in [('YURI_R4_NATIVE_WALK_SOURCE_ONLY_R1_20261005.zip','6f88434a3758bb446e71b6907796e5ba61f9eeeefcc7f92d1cbc9dd5cfb50a50'),('YURI_R4_WALK_HEAD_BOUNDARY_SUPPLEMENT_R1_20261005.zip','7573c53446fc6868aa180726496fa8beff40052e8729dc553b9c248198e9f9ac')]:assert sha(B/old)==expected
entries={}
def add(p,a):
 p=Path(p);assert p.is_file() and a not in entries;entries[a]=p
add(m['source'],'source/Character_Master_NeckSkin_R4.blend')
for folder,prefix in [(P,'native-qa'),(D,'review'),(E,'public-qa'),(G,'guard')]:
 for p in folder.rglob('*'):
  if p.is_file():add(p,prefix+'/'+p.relative_to(folder).as_posix())
for n in ['r4_native_head_visual_source_r1.py','r4_native_head_visual_owned_prepare_r1.py','r4_native_head_visual_delivery_r1.py','r4_native_head_visual_package_r1.py','r4_appearance_signature.py','r4_appearance_adapter.py','native_preservation.py']:add(LAB/'scripts'/n,'workflow/'+n)
readme=D/'SOURCE_REFERENCE_HANDOFF_R1.md';readme.write_text('''# R4 original native head/neck visual reference

Canonical source exact SHA is in PACKET_INDEX_R1.json. Existing MESHY_R2_BODY_HeadGazeHair on Meshy_Fitted_Rig, original slot OBLegacy Slot, full1..97 native24fps. Original78Actions and all original geometry/weights/keys/rest/material/shader/texture/driver states preserved, source never saved. No candidate/exporter/new rig. Open source read-only, use workflow/r4_appearance_adapter.py ReactionLane('Meshy_Fitted_Rig').on('MESHY_R2_BODY_HeadGazeHair'); native source24fps. lane.off() restores original binding/frame/pose. Do not unmute original bridges or append donor geometry.

review/LAPTOP_MATCHED_SOURCE_REFERENCE_PRIVATE_R1.json gives exact original source/Action signature/slot, all original shader/texture signatures, cameras, representative frame1/13/25/37/49/61/73/85/97, evaluated mesh fingerprints and all72 exact morph values. All morph values are zero and eye-to-head relative transform stays constant: BODY-only reference, not native auxiliary FACE KEY/GAZE/HAIR acting proof. Actual head/hair/eye assembly movement is sampled in native-qa full97 rows. Full original24fps front/side videos plus all194 PNG frames, actual UI1x proof and OFF decodedRGBA0 available.

No gross new mouth blotch/hair break/neck seam split observed at384CPU8sample preview; silver/gray-white hair is already canonical source appearance. Fine shading artifacts are limited by sampling noise. This cannot prove Unity normal/tangent/shader parity, independent gaze/blink/mouth morph stability or runtime acceptance. Source reference scope normal, matched Unity stage needs independent examination. Existing contact/foot/velocity/TierP/F2 HOLD unchanged. Source and older packets are never overwritten.
''',encoding='utf8');add(readme,'SOURCE_REFERENCE_HANDOFF_R1.md')
idx={'source_SHA':m['source_SHA'],'existing_action':m['existing_action'],'action_signature_SHA':m['action_signature_SHA'],'verdict':'SOURCE_BODY_HEAD_VISUAL_REFERENCE_ONLY_UNITY_STAGE_UNTESTED','members':[{'path':a,'bytes':p.stat().st_size,'sha256':sha(p)} for a,p in sorted(entries.items())]};ip=D/'PACKET_INDEX_R1.json';ip.write_text(json.dumps(idx,indent=2),encoding='utf8');add(ip,'PACKET_INDEX_R1.json')
z=B/'YURI_R4_NATIVE_HEAD_VISUAL_SOURCE_R1_20261005.zip'
with zipfile.ZipFile(z,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for a,p in sorted(entries.items()):f.write(p,a)
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None
 for x in idx['members']:
  v=f.read(x['path']);assert len(v)==x['bytes'] and hashlib.sha256(v).hexdigest()==x['sha256']
r={'packet':str(z),'sha256':sha(z),'bytes':z.stat().st_size,'members':len(entries),'indexed_members':len(idx['members']),'CRC_SHA_size_all_verified':True,'source_SHA':m['source_SHA'],'source_action_signature_SHA':m['action_signature_SHA'],'closed_once':True,'source78_OFF_preserved':True,'new_candidate':None,'TierP':0};(E/'PRIVATE_PACKET_RECEIPT_R1.json').write_text(json.dumps(r,indent=2),encoding='utf8');print(json.dumps(r,indent=2))
