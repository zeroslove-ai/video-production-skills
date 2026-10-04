"""Seal one root-contact experimental handoff without modifying prior assets."""
from pathlib import Path
import json,hashlib,zipfile
LAB=Path(__file__).resolve().parents[1];B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');P=B/'alpha-walk-root-contact-c1';W=B/'alpha-native-walk-source-r1';D=B/'alpha-walk-root-contact-delivery-c1';E=LAB/'evidence/walk-root-contact-c1';G=B/'o1-walk-root-contact-c1';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();js=lambda p:json.loads(Path(p).read_bytes());m=js(P/'WALK_ROOT_CONTACT_PRIVATE_C1.json');s=js(E/'WALK_ROOT_CONTACT_SCALAR_QA_C1.json');ui=js(D/'WHOLE_NATIVE_1X_UI_C1.json');assert len(ui)==3 and all(x['ended'] and x['error'] is None and x['playbackRate']==1 for x in ui)
assert sha(m['source'])==m['source_SHA'] and sha(m['candidate'])==m['candidate_SHA'] and sha(m['old_candidate'])==m['old_candidate_SHA'] and sha(m['library']['file'])==m['library']['sha256'];g=js(G/'NATIVE_GUARD_RESULT.json');assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN' and all(sha(p)==v for p,v in g['inputs_after'].items())
for n,h in [('YURI_R4_NATIVE_WALK_SOURCE_ONLY_R1_20261005.zip','6f88434a3758bb446e71b6907796e5ba61f9eeeefcc7f92d1cbc9dd5cfb50a50'),('YURI_R4_NATIVE_HEAD_VISUAL_SOURCE_R1_20261005.zip','5fc486676885341e04c4b597fb5a1d102f9d81a6033e13f658cbb064a7e69546')]:assert sha(B/n)==h
entries={}
def add(p,a):
 p=Path(p);assert p.is_file() and a not in entries;entries[a]=p
add(m['source'],'source/Character_Master_NeckSkin_R4.blend');add(m['old_candidate'],'original-control/'+Path(m['old_candidate']).name);add(W/'YURI_R4_NATIVE_WALK_ACTIONS_ONLY_R1.blend','original-control/YURI_R4_NATIVE_WALK_ACTIONS_ONLY_R1.blend');add(W/'NATIVE_WALK_SOURCE_PRIVATE_R1.json','original-control/NATIVE_WALK_SOURCE_PRIVATE_R1.json')
for folder,prefix in [(P,'candidate-native-qa'),(D,'review'),(E,'public-qa'),(G,'guard')]:
 for p in folder.rglob('*'):
  if p.is_file():add(p,prefix+'/'+p.relative_to(folder).as_posix())
for view in ['front','quarter','side']:
 add(B/'alpha-native-walk-delivery-r1'/f'{view}_NATIVE_WALK_FULL97_1x.mp4','original-control/'+view+'_NATIVE_WALK_FULL97_1x.mp4')
for n in ['r4_walk_root_contact_trial_c1.py','r4_walk_root_contact_adapter_c1.py','r4_walk_root_contact_owned_prepare_c1.py','r4_walk_root_contact_delivery_c1.py','r4_walk_root_contact_package_c1.py','r4_native_walk_adapter_r1.py','r4_appearance_signature.py','r4_appearance_adapter.py','r4_existing_reach_contact_closure_r1.py','native_preservation.py']:add(LAB/'scripts'/n,'workflow/'+n)
readme=D/'ROOT_CONTACT_C1_HANDOFF.md';readme.write_text('''# ONE R4 native Walk root-contact experiment

Immutable source remains sole visual authority; new candidate is default OFF and not appearance promotion. Source/prior81 Actions/raw OFF preserved. Append ONLY four Actions from candidate-native-qa/YURI_R4_WALK_ROOT_CONTACT_ACTIONS_ONLY_C1.blend onto canonical source. No meshes/rigs/materials/images in Action library. Source24fps,1..97. workflow/r4_walk_root_contact_adapter_c1.py WalkRootContactLane().on()/off() binds BODY/source hair/new head-root/carrier Actions and restores prior bindings/frame/pose/root location. Original BODY curves identical, no ankle/knee/proportion/driver/rest edits. No new exporter or Unity implementation.

One algorithm: source actual persistent sole vertices within3mm of original floor; negative median per-foot XY displacement integrated into Assembly_Root; equal-foot compromise if both near floor. RootZ0. Unparented face root gets matching XY translation. Near-floor mask and common vertices are frozen from original control, not reselected to improve numbers. Endpoint root delta about[0,-0.419831333,0]m/4seconds. Translational loop must ACCUMULATE this delta each repetition: resetting root to zero teleports. Root/body velocity seam worsens and remains HOLD, not seamless loop or physical plant proof. Sole XY drift134.124mm to2.042mm is kinematic proximity improvement, not force/COM/balance/contact-force acceptance. Original head surface gate HOLD remains.

Full97 original vs candidate native24fps1x matched fixed front/quarter/side comparison movies and candidate full97 videos in review/. Exact original source/candidate/library hashes in PACKET_INDEX_C1.json, actual source/candidate sole trajectories/masks/root/world geometry-translation/bone-pose numerical evidence in candidate-native-qa/. Root speed and double-support conflict/seam/gap limits in public-qa report. Source-cameraOFF neutral decodedRGBA0. New candidate preserved writer in-memory OFF signature before/afterSaveAs; fresh serialized candidate reopen not performed in this single native job, consumer should check before use. Protected GUI/GPU/product unchanged. No TierP/F2/StageB or Unity gate promotion. Closed prior source-Walk/head reference packets unchanged.
''',encoding='utf8');add(readme,'ROOT_CONTACT_C1_HANDOFF.md')
idx={'source_SHA':m['source_SHA'],'old_candidate_SHA':m['old_candidate_SHA'],'candidate_SHA':m['candidate_SHA'],'library_SHA':m['library']['sha256'],'verdict':s['verdict'],'TierP':0,'members':[{'path':a,'bytes':p.stat().st_size,'sha256':sha(p)} for a,p in sorted(entries.items())]};ip=D/'PACKET_INDEX_C1.json';ip.write_text(json.dumps(idx,indent=2),encoding='utf8');add(ip,'PACKET_INDEX_C1.json')
z=B/'YURI_R4_WALK_ROOT_CONTACT_EXPERIMENT_C1_20261005.zip'
with zipfile.ZipFile(z,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for a,p in sorted(entries.items()):f.write(p,a)
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None
 for x in idx['members']:
  v=f.read(x['path']);assert len(v)==x['bytes'] and hashlib.sha256(v).hexdigest()==x['sha256']
r={'packet':str(z),'sha256':sha(z),'bytes':z.stat().st_size,'members':len(entries),'indexed_members':len(idx['members']),'CRC_SHA_size_all_verified':True,'closed_once':True,'source_SHA':m['source_SHA'],'old_candidate_SHA':m['old_candidate_SHA'],'candidate_SHA':m['candidate_SHA'],'library_SHA':m['library']['sha256'],'verdict':s['verdict'],'TierP':0};(E/'PRIVATE_PACKET_RECEIPT_C1.json').write_text(json.dumps(r,indent=2),encoding='utf8');print(json.dumps(r,indent=2))
