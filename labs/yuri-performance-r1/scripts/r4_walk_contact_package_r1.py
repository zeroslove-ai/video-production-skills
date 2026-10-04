"""Seal ONE contact-corrected source candidate and before/after evidence; no promotion."""
from pathlib import Path
import json,hashlib,zipfile
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');LAB=Path(__file__).resolve().parents[1];D=BASE/'walk-contact-delivery-r1';E=LAB/'evidence/walk-stop-contact-source-closure-r1';E.mkdir(exist_ok=False)
def load(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
 with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
c=load(BASE/'walk-contact-candidate-r3/CONTACT_CANDIDATE_RECEIPT_R3.json');qa=load(D/'CONTACT_SPAN_BEFORE_AFTER_QA_R1.json');pixel=load(BASE/'walk-contact-off-qa-r3/OFF_RGBA_ARRAY_EQUAL_R3.json');off=load(BASE/'walk-contact-off-qa-r3/OFF_REOPEN_ORACLE_R3.json');ui=load(D/'WHOLE_1X_UI_BEFORE_AFTER_QA_R1.json')
assert sha(c['candidate'])==c['candidate_SHA'] and pixel['all_channels_exact'];assert all(ui[k]==[True]*3 for k in ['ended']) and ui['rates']==[1]*3 and ui['errors']==[None]*3
summary={k:v for k,v in c.items()};summary.update({'source_visual_quality_verdict':'MIXED_HOLD','visible_remaining_defects':ui['visible_remaining_defects'],'phase_contact_ground_truth':False,'first_bridge_81_98':'UNLABELED procedural transfer; no extracted contact labels. Low-clearance large travel remains unchanged/HOLD.','second_bridge_243_264':'One new designed sequential-step correction, not dedicated authored stop. Support cohort drift measured; physics slip remains uncertified.','OFF_geometry_material_keys_weights_rest_drivers_78_authority_Actions_exact':off['all_nontexture_geometry_material_nodes_weights_keys_rest_drivers_bindings_scene_exact'],'OFF_RGBA_all_channels_exact':True,'texture_packed_bytes_colorspace_resolved_properties_exact':off['packed_texture_bytes_colorspace_resolved_properties_exact'],'raw_SaveAs_texture_locator_remap_disclosed':True,'source_visual_promotion':False,'StageB_O1_PRIMARY_Unity_F2_F3_TierP':'HOLD; no promotion','existing_44_TierC':44,'existing_TierP':0,'candidate_count':'ONE successfully saved correction; R1 residual failure and R2 watchdog failure preserve receipts.','whole_normal_speed_before_after':ui})
write(E/'SOURCE_CONTACT_CLOSURE_MANIFEST_R1.json',summary);write(E/'CONTACT_SPAN_BEFORE_AFTER_QA_R1.json',qa);write(E/'OFF_RGBA_ARRAY_EQUAL_R3.json',pixel)
for a,b in [('81','98'),('243','264')]:
 p=BASE/'walk-contact-transition-analysis-r1'/f'BEFORE_SPAN_{a}_{b}_CONTACT_RATIONALE_R1.json';write(E/p.name,load(p))
write(E/'FAILURE_LEDGER_R1.json',[{'attempt':'R1','status':'FAIL, no candidate saved','cause':'Frame252 left sole solve residual4.286mm exceeded3mm gate; fixed pelvis reach allowance, not weaker acceptance.'},{'attempt':'R2','status':'FAIL_WATCHDOG, no candidate saved','cause':'Recomputed full mesh Jacobian every iteration exceeded600seconds. Owned Job cleanup active0, exit90; never reused this guard as PASS.'},{'attempt':'R3','status':'PASS native','change':'Same35mm step goals,10mm pelvis allowance and3mm gate. Cached full original baseline numerics pinned, native anchor hashes checked; secant Jacobian updates reduce repeated mesh cost. All273 untouched native mesh hashes rechecked exact in new passed run. Guards unchanged.'}])
report='''# One preserved-baseline stop bridge contact correction

Original R4 remains immutable appearance authority. Original walk R3 candidate/70,575,977byte packet/a2a0ffa checkpoint preserved. Exactly ONE successfully saved source candidate, not a new motion library. Existing44 TierC/0 TierP; no Unity/StageB/O1/PRIMARY/F2/F3 promotion.

## Two bridge semantics

81–98: original walk endpoint R source toe-marker proxy is stance, but procedural bridge has no authored donor contact labels. L/R cohorts translate at low clearance. This is an UNLABELED ground-skimming procedural transfer; it cannot be certified as authored swing or physical slip PASS/FAIL. No change was made to this bridge. Contact remains HOLD.

243–264: before stance widens from attention neutral to Idle_Loop by moving both feet nearly at floor height. This visible low-clearance widening was the SINGLE selected defect. After native243 is preserved;244..263 uses designed L swing first, R swing second,35mm sin² lift and at most10mm vertical pelvis support allowance. L/R support goals remain world-space stationary in their respective phases. Carrier/root path is exactly R3 on all293 frames; walking root was not frozen.

Phase tags are new procedural design intentions, not contact labels extracted from the donor. Quantitative cohort residual/drift and lowest-vertex clearance are proxies, not physical pressure/contact or exhaustive slipping certification. First bridge and dedicated turn/stop remain unresolved inputs.

## Actual remaining visible defect: MIXED/HOLD

The front view at frame248 (8.233333s), around246..251, shows prominent leg silhouette crossover/pinching during the first new step. Side support/clearance improved, but foot-cohort numeric agreement and >.99 knee-plane cosines did not certify the deformed silhouette. Mesh self-intersection was not exhaustively measured; exact cause is not established. This one candidate is MIXED/HOLD and does NOT replace the R3 baseline. No further variant was made within this one-candidate scope.

## Preservation / actual evidence

Native all293 body geometry finite; all273 frames outside244..263 body world-vertex hashes exact against pinned R3 baseline. Existing82 Actions (original78 + prior4) remain unchanged. Source geometry/hierarchy/rest/weights/material/nodes/ShapeKeys/gaze/face drivers preserve original authority OFF. Only new Actions: native thigh/shin/foot rotations, <=10mm pelvis support, original face/hair rigid-root transport following body. No new rig/constraint/geometry/exporter or paid/GPU provider.

Saved OFF reopen oracle and neutral full RGBA comparison against existing witness are exact. Packed texture bytes/colorspace/resolved properties exact; SaveAs locator strings explicitly disclosed. Action-only library contains0 objects/meshes/armatures.

Before/after fixed front/quarter/side whole9.766667s MP4s:293 native samples encoded30fps, source scene24fps preserved. Existing273 exact frames reused; only20 changed frames rendered fresh with same fixed50mm cameras, CPU2samples/threads2/seed0/JPEG92. All three whole decoded and UI normal-speed ended/errornull. This low-cost source preview does not certify final visual fidelity, finger/neck seam, contact physics or runtime.

## Reapply / reproduce

Use canonical source, four new Actions and separate existing binding adapter. Bind BODY/root carrier/body-head transport/hair transport together with source_fps30; OFF restores original frame, pose, Action slots, carrier transforms and bindings. The private packet contains authority source, exact R3 before candidate, corrected OFF candidate, Action-only library, numeric baseline/contact/after measurements, scripts, cameras, whole1x movies, license notices and native resource/failure custody. Scripts retain desktop paths; on another desktop, remap scoped paths and create a fresh exact native packet rather than reusing historical argv approvals.

R1 failed solve before save; R2 timed out under unchanged600second guard, drained owned Job to0 and saved no candidate. R3 uses the same goals/gates with secant Jacobian updates. Its pinned baseline cache from R2 is numerical input, NOT a PASS receipt. Native anchors and all273 untouched evaluated hashes were checked again in this successful run. All failures remain preserved.

Next bounded source target is deformed-leg silhouette/twist QA during the selected stop step, then first-bridge contact design or dedicated turn/stop input. Do not count the current source-only result as contact-physics/Living StageB acceptance. High-resolution neck/hand and full facial/secondary/runtimes remain separate gates.
'''
with (E/'YURI_R4_STOP_CONTACT_SOURCE_CLOSURE_R1.md').open('x',encoding='utf8') as f:f.write(report)
files={}
def add(p,name):
 p=Path(p);assert p.is_file() and name not in files;files[name]=p
add(c['candidate'],'candidate/'+Path(c['candidate']).name)
old=load(BASE/'alpha-walk-turn-candidate-r3/WALK_TURN_STOP_CANDIDATE_PRIVATE_R3.json');add(old['candidate'],'before/'+Path(old['candidate']).name);add(old['source'],'source/'+Path(old['source']).name)
for folder in ['walk-contact-candidate-r1','walk-contact-candidate-r2','walk-contact-candidate-r3','walk-contact-off-qa-r3','walk-contact-transition-analysis-r1']:
 for p in (BASE/folder).rglob('*'):
  if p.is_file() and p.suffix not in ['.blend','.blend1']:add(p,'private-evidence/'+folder+'/'+p.relative_to(BASE/folder).as_posix())
for p in (BASE/'walk-contact-off-qa-r3').glob('*.blend'):add(p,'animation-only/'+p.name)
for p in E.iterdir():add(p,'metadata/'+p.name)
for p in D.iterdir():
 if p.is_file():add(p,'review/'+p.name)
for folder in list(BASE.glob('walk-stop-contact-*-broker-r*'))+list(BASE.glob('walk-contact-*-broker-r*')):
 for p in folder.rglob('*'):
  if p.is_file():add(p,'native-custody/'+folder.name+'/'+p.relative_to(folder).as_posix())
for p in LAB.joinpath('scripts').glob('r4_walk*contact*.py'):add(p,'workflow/'+p.name)
for name in ['r4_appearance_adapter.py','r4_appearance_signature.py','native_preservation.py']:add(LAB/'scripts'/name,'workflow/'+name)
for view in ['front','quarter','side']:add(BASE/'walk-contact-preview-r3'/view/'RENDER_RECEIPT_R4.json','camera/'+view+'_RENDER_RECEIPT_R4.json')
licenses=Path(r'C:/Users/JAEWAN/.codex/worktrees/common-motion-curation-r1/yuri-room-mvp/common-motion-r1/licenses')
for name in ['Quaternius-LICENSE.txt','StayStill-LICENSE.txt']:add(licenses/name,'licenses/'+name)
index={n:{'bytes':p.stat().st_size,'sha256':sha(p)} for n,p in sorted(files.items())};idx=D/'MEMBER_SHA256_INDEX_R1.json';write(idx,index);add(idx,idx.name)
zpath=BASE/'YURI_R4_STOP_CONTACT_SOURCE_CANDIDATE_R1_20261004.zip'
with zipfile.ZipFile(zpath,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):z.write(p,n)
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None
 for n,v in index.items():
  raw=z.read(n);assert len(raw)==v['bytes'] and hashlib.sha256(raw).hexdigest()==v['sha256']
 assert len(z.namelist())==len(files)
receipt={'file':str(zpath),'bytes':zpath.stat().st_size,'sha256':sha(zpath),'members':len(files),'indexed_members':len(index),'CRC_all_members':'PASS','all_indexed_member_size_SHA':'PASS','candidate_bytes':c['candidate_bytes'],'candidate_sha256':c['candidate_SHA'],'original_R3_sha256':old['candidate_SHA'],'canonical_R4_sha256':old['source_SHA'],'index_sha256':sha(idx),'public_Git_raw_private_geometry_motion':False,'contact_physics_Unity_final_visual_promoted':False};write(E/'PRIVATE_PACKET_RECEIPT_R1.json',receipt);write(D/'PRIVATE_PACKET_RECEIPT_R1.json',receipt)
assert sha(old['source'])==old['source_SHA'] and sha(old['candidate'])==old['candidate_SHA'];print(json.dumps(receipt,indent=2))
