"""Seal ONE private reusable Walk source supply with exact custody; no repack."""
from pathlib import Path
import json,hashlib,zipfile
LAB=Path(__file__).resolve().parents[1];B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');P=B/'alpha-native-walk-source-r1';D=B/'alpha-native-walk-delivery-r1';E=LAB/'evidence/alpha-native-walk-source-r1';G=B/'o1-native-walk-source-r1'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
js=lambda p:json.loads(Path(p).read_bytes())
m=js(P/'NATIVE_WALK_SOURCE_PRIVATE_R1.json');assert js(G/'NATIVE_GUARD_RESULT.json')['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN';assert m['complete97_three_views'] and m['original78_OFF_raw_full_snapshot_and_candidate_reopen_equal'];assert js(D/'OFF_PIXEL_QA_R1.json')['changed_pixels']==0
assert sha(m['source'])==m['source_SHA'] and sha(m['candidate'])==m['candidate_SHA'] and sha(m['library']['file'])==m['library']['sha256']
movies=js(D/'VIDEO_CUSTODY_R1.json');assert len(movies)==6 and all(sha(x['file'])==x['sha256'] for x in movies);ui=js(D/'WHOLE_NATIVE_1X_UI_R1.json');assert len(ui)==6 and all(x['ended'] and x['error'] is None and x['playbackRate']==1 for x in ui)
readme=D/'HANDOFF_SOURCE_ONLY_WALK_R1.md';readme.write_text('''# R4 original native WalkInPlace source-only handoff

The immutable source is the visual authority. This is ONE animation supply experiment; world plant/full contact/velocity seam/Unity/F2/TierP approval remains HOLD. See public-qa/YURI_R4_NATIVE_WALK_SOURCE_SUPPLY_R1.md for numerical limits and causal exclusions. No source/control/R2/08caad7/old candidate/packet was overwritten.

Blender5.2 playback: open candidate/ animation OFF, or open source/Character_Master_NeckSkin_R4.blend and append ONLY the three Action datablocks from actions/YURI_R4_NATIVE_WALK_ACTIONS_ONLY_R1.blend. Never append Object/Collection/Mesh/Armature/Material or reset face/gaze drivers. Add workflow/ to sys.path, import NativeWalkLane from r4_native_walk_adapter_r1, create lane=NativeWalkLane(), lane.on(); play original frames1..97 at24fps; lane.off() restores previous binding/frame/pose. This is an offline Blender binder, not a Unity runtime adapter. Source scene24fps is preserved, no retiming. Body curves match original native Action exactly; two head/hair transport Actions follow the existing assembly.

Timing:4.0s endpoint span,4.041667s full97 encoded; two full Action spans use96unique frames×2=192frames=8.0s at24fps. Clip geometry repeats exactly, but measured velocity seam remains. Root is fixed; original in-place feet travel up to134.124mm during near-floor intervals. This does not demonstrate translational locomotion, planted support forces, zero slip or balance. Strict new head/hair/body-head surface identities remain HOLD, even though body-self/new body-hair contacts are zero. Do not waive source overlaps or call them numerical noise without proof.

All three full97 videos and all three two-cycle videos are in review/, original native1x; camera metadata and raw full97 floor/contact/deformation data in native-qa/. Full original78/raw appearance/weights/rest/materials/textures/ShapeKeys/drivers restored and candidate reopened exact; source-camera960x920RGBA OFF identical. One protected CPU guard only, no GPU lease/GUI/product changes. All raw native pose/triangles/images/video/model data remain private; public Git receives scalar QA, SHA pointers and scripts only.

Research collectors/guard configs retain Desktop absolute input pins. Portable playback needs only source/library/adapter. Future single existing-action hypothesis: BODY_Idle as unchanged static grounded control, unexecuted; no second Walk candidate or angle/IK/strength sweep.
''',encoding='utf8')
entries={}
def add(p,a):
 p=Path(p);assert p.is_file() and a not in entries;entries[a]=p
add(m['source'],'source/Character_Master_NeckSkin_R4.blend');add(m['candidate'],'candidate/'+Path(m['candidate']).name);add(m['library']['file'],'actions/'+Path(m['library']['file']).name)
for folder,prefix in [(P,'native-qa'),(D,'review'),(E,'public-qa'),(G,'guard')]:
 for p in folder.rglob('*'):
  if p.is_file() and p.suffix!='.blend':add(p,prefix+'/'+p.relative_to(folder).as_posix())
for n in ['r4_native_walk_source_supply_r1.py','r4_native_walk_owned_prepare_r1.py','r4_native_walk_adapter_r1.py','r4_native_walk_video_r1.py','r4_native_walk_package_r1.py','r4_appearance_signature.py','r4_appearance_adapter.py','r4_existing_reach_contact_closure_r1.py','native_preservation.py']:
 add(LAB/'scripts'/n,'workflow/'+n)
add(readme,'HANDOFF_SOURCE_ONLY_WALK_R1.md')
index={'source_SHA':m['source_SHA'],'candidate_SHA':m['candidate_SHA'],'action_SHA':m['library']['sha256'],'status':'SOURCE_SUPPLY_ONLY_CONTACT_PLANT_VELOCITY_HOLD','native_fps':24,'speed_factor':1,'TierP':0,'members':[{'path':a,'bytes':p.stat().st_size,'sha256':sha(p)} for a,p in sorted(entries.items())]};ip=D/'PACKET_INDEX_R1.json';ip.write_text(json.dumps(index,indent=2),encoding='utf8');add(ip,'PACKET_INDEX_R1.json')
z=B/'YURI_R4_NATIVE_WALK_SOURCE_ONLY_R1_20261005.zip'
with zipfile.ZipFile(z,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for a,p in sorted(entries.items()):f.write(p,a)
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None and len(f.infolist())==len(entries)
 for x in index['members']:
  v=f.read(x['path']);assert len(v)==x['bytes'] and hashlib.sha256(v).hexdigest()==x['sha256']
receipt={'packet':str(z),'sha256':sha(z),'bytes':z.stat().st_size,'members':len(entries),'indexed_members':len(index['members']),'CRC_SHA_size_all_verified':True,'closed_once':True,'source_SHA':m['source_SHA'],'candidate_SHA':m['candidate_SHA'],'action_SHA':m['library']['sha256'],'action_bytes':m['library']['bytes'],'native_fps':24,'native_speed_factor':1,'verdict':'SOURCE_SUPPLY_ONLY_CONTACT_PLANT_VELOCITY_HOLD','TierP':0};(E/'PRIVATE_PACKET_RECEIPT_R1.json').write_text(json.dumps(receipt,indent=2),encoding='utf8');print(json.dumps(receipt,indent=2))
