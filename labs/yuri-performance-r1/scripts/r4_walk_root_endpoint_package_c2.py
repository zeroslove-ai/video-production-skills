"""Close ONE C2 plus original source/C1 comparison and preserved failure provenance."""
from pathlib import Path
import json,hashlib,zipfile
LAB=Path(__file__).resolve().parents[1];B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');P=B/'alpha-walk-root-endpoint-c2b';W=B/'alpha-walk-root-contact-c1';D=B/'alpha-walk-root-endpoint-delivery-c2';E=LAB/'evidence/walk-root-endpoint-c2';G=B/'o1-walk-root-endpoint-c2b';F=B/'o1-walk-root-endpoint-c2';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();js=lambda p:json.loads(Path(p).read_bytes());m=js(P/'WALK_ROOT_ENDPOINT_PRIVATE_C2.json');s=js(E/'WALK_ROOT_ENDPOINT_SCALAR_QA_C2.json');ui=js(D/'WHOLE_TWO_CYCLE_1X_UI_C2.json');assert len(ui)==3 and all(x['ended'] and x['error'] is None and x['playbackRate']==1 and x['duration']==8 for x in ui)
assert sha(m['source'])==m['source_SHA'] and sha(m['candidate'])==m['candidate_SHA'] and sha(m['library']['file'])==m['library']['sha256'];g=js(G/'NATIVE_GUARD_RESULT.json');assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN' and all(sha(p)==v for p,v in g['inputs_after'].items());assert sha(B/'YURI_R4_WALK_ROOT_CONTACT_EXPERIMENT_C1_20261005.zip')=='3c24596b3af58e0095f4e86168db2ff94639c190336739d06ceb3a824cf931bc'
entries={}
def add(p,a):
 p=Path(p);assert p.is_file() and a not in entries;entries[a]=p
add(m['source'],'source/Character_Master_NeckSkin_R4.blend')
for n in ['Character_R4_WalkRootContact_EXPERIMENT_OFF_C1_20261005.blend','YURI_R4_WALK_ROOT_CONTACT_ACTIONS_ONLY_C1.blend','WALK_ROOT_CONTACT_PRIVATE_C1.json','SOURCE_AND_CANDIDATE_SOLE_TRAJECTORIES_PRIVATE_C1.npz']:add(W/n,'original-C1/'+n)
for folder,prefix in [(P,'C2-native-qa'),(D,'review'),(E,'public-qa'),(G,'guard-C2b'),(F,'preserved-first-implementation-failure')]:
 for p in folder.rglob('*'):
  if p.is_file():add(p,prefix+'/'+p.relative_to(folder).as_posix())
for n in ['r4_walk_root_endpoint_trial_c2.py','r4_walk_root_endpoint_trial_c2b.py','r4_walk_root_endpoint_owned_prepare_c2.py','r4_walk_root_endpoint_owned_prepare_c2b.py','r4_walk_root_endpoint_adapter_c2.py','r4_walk_root_endpoint_delivery_c2.py','r4_walk_root_endpoint_package_c2.py','r4_walk_root_contact_adapter_c1.py','r4_appearance_adapter.py','r4_appearance_signature.py','r4_existing_reach_contact_closure_r1.py','native_preservation.py']:add(LAB/'scripts'/n,'workflow/'+n)
readme=D/'C2_ACCUMULATED_LOOP_HANDOFF.md';readme.write_text('''# ONE C2 root endpoint experiment, no automatic promotion

Immutable source authority, original source78/C1prior83/rawOFF preserved. Fresh serialized C1 OFF and fresh C2 OFF compared to source in the owned job. Candidate defaults OFF. Append ONLY four C2 Actions from C2-native-qa/YURI_R4_WALK_ROOT_ENDPOINT_ACTIONS_ONLY_C2.blend onto original source; never append rigs/mesh/material/image or unmute drivers. workflow/r4_walk_root_endpoint_adapter_c2.py WalkRootEndpointLane().on()/off() binds exact existing hierarchy and restores previous bindings/frame/poses/carrier location. Native source24fps, phase1..97; actual global1..193 demonstrates two4second cycles. Videos omit terminal duplicate193 only,192samples/8sec. Blender CYCLES modifiers REPEAT body/hair/quaternion, REPEAT_OFFSET carrier/head location accumulate0.419831m/cycle. Unity/exporter/import/runtime consumption untested; do not assume modifiers are portable without independent serialization validation.

One endpoint method only: first/last8-frame compact cubic bump, fixed endpoints/rootZ, equal average root finite velocity. Max0.643241mm correction. BODY/Hair source pose keys/interpolation unchanged. Original BODY already has364Cycles; copied modifiers reused, no duplicate Cycles. First implementation incorrectly asserted no source modifiers, failed before asset save; preserved first guard/code plus new C2b exact guard repair. Only one C2 motion candidate saved; no parameter/strength family.

Root seam velocity mismatch0.02017 to0m/s; body seam0.08951 to0.07018m/s, source BODY derivative remains HOLD. Translation-only irreducible residual lower bound0.056027m/s. Maximum sole drift2.042mm retained; right1.202 to1.845mm tradeoff. Root reaches0.420m and0.840m after two cycles without reset; physical contact/COM/balance/head-contact/TierP/F2/Unity HOLD. Source-cameraOFF decodedRGBA0. See scalar/report for acceleration, pose/relative geometry and limitations.

Fixed wider front/quarter/side two-cycle comparison videos, all192 C2 native frames and new C1cycle2 native frames available. C1cycle1 reuses cached native1..96 through documented calibrated orthographic reframe/bicubic resampling, never rerenders original approved baseline. C1cache-to-native texture-noise change at97 is disclosed and not a shader or motion correction. Full C1/C2 global1..193 actual world evaluation supports quantitative comparison; normal1x UI8seconds completed and whole9videos decoded. All raw geometry/motion/captures stay private; only scripts/scalars/hash pointers in public Git. No source/product/GUI/GPU/closedpacket changes.

Next ONE recommendation, unexecuted: inspect source BODY endpoint derivatives on a separate animation copy with sole QA; uniform root cannot remove heterogeneous source body velocity field. No further root-strength sweep.
''',encoding='utf8');add(readme,'C2_ACCUMULATED_LOOP_HANDOFF.md')
idx={'source_SHA':m['source_SHA'],'C1_candidate_SHA':m['C1_candidate_SHA'],'candidate_SHA':m['candidate_SHA'],'library_SHA':m['library']['sha256'],'status':s['verdict'],'TierP':0,'members':[{'path':a,'bytes':p.stat().st_size,'sha256':sha(p)} for a,p in sorted(entries.items())]};ip=D/'PACKET_INDEX_C2.json';ip.write_text(json.dumps(idx,indent=2),encoding='utf8');add(ip,'PACKET_INDEX_C2.json')
z=B/'YURI_R4_WALK_ROOT_ENDPOINT_EXPERIMENT_C2_20261005.zip'
with zipfile.ZipFile(z,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for a,p in sorted(entries.items()):f.write(p,a)
with zipfile.ZipFile(z) as f:
 assert f.testzip() is None
 for x in idx['members']:
  v=f.read(x['path']);assert len(v)==x['bytes'] and hashlib.sha256(v).hexdigest()==x['sha256']
r={'packet':str(z),'sha256':sha(z),'bytes':z.stat().st_size,'members':len(entries),'indexed_members':len(idx['members']),'CRC_SHA_size_all_verified':True,'source_SHA':m['source_SHA'],'C1_candidate_SHA':m['C1_candidate_SHA'],'candidate_SHA':m['candidate_SHA'],'library_SHA':m['library']['sha256'],'closed_once':True,'status':s['verdict'],'TierP':0};(E/'PRIVATE_PACKET_RECEIPT_C2.json').write_text(json.dumps(r,indent=2),encoding='utf8');print(json.dumps(r,indent=2))
