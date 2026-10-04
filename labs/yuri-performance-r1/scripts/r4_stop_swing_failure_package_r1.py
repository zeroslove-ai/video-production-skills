"""Preserve one failed alternative: frontal improvement but causal knee-depth branch pop."""
from pathlib import Path
import json,hashlib,zipfile
from PIL import Image,ImageDraw
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');LAB=Path(__file__).resolve().parents[1];D=BASE/'stop-swing-path-alt-delivery-r1';E=LAB/'evidence/stop-swing-path-alternative-causal-failure-r1';E.mkdir(exist_ok=False)
def load(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
 with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
c=load(BASE/'stop-swing-path-alt-candidate-r1/SWING_PATH_ALTERNATIVE_RECEIPT_R1.json');before=load(BASE/'walk-contact-candidate-r3/CONTACT_CANDIDATE_RECEIPT_R3.json');authority=load(BASE/'alpha-walk-turn-candidate-r3/WALK_TURN_STOP_CANDIDATE_PRIVATE_R3.json');qa=load(D/'CONTACT_SPAN_BEFORE_AFTER_QA_R1.json');geo=load(D/'SWING_GEOMETRY_CAUSAL_DIAGNOSTIC_R1.json');pixel=load(BASE/'stop-swing-path-alt-off-qa-r1/OFF_RGBA_ARRAY_EQUAL_R1.json');assert pixel['all_channels_exact'] and sha(c['candidate'])==c['candidate_SHA']
ui={'url':'http://127.0.0.1:8785/REVIEW_STOP_SWING_PATH_ALT_BEFORE_AFTER_R1.html','views':['front','quarter','side'],'start_times_sec':[.193922,.193874,.193778],'end_times_sec':[9.766667]*3,'rates':[1]*3,'ended':[True]*3,'errors':[None]*3,'whole293_native_samples_3movies_decode':'PASS','native_FPS':30,'original_source_scene_FPS':24,'source_quality_verdict':'FAIL_KNEE_DEPTH_BRANCH_POP','remaining_defects':['New X-only corridor improves frontal frame248 crossing but L knee switches depth branch247->248 by190.580mm per native frame. This is a temporal stop-continuity regression.','Original81..98 proxy bridge remains unmodified/HOLD; no donor authored contact labels.','Dedicated turn/stop missing; source-only procedural support labels and cohort numbers are not physical contact/Unity/final visual PASS.']};write(D/'WHOLE_1X_ALT_QA_R1.json',ui)
write(E/'ALTERNATIVE_SOURCE_MANIFEST_R1.json',{'candidate':c,'baseline_SHA':before['candidate_SHA'],'authority_SHA':authority['source_SHA'],'source_quality_verdict':ui['source_quality_verdict'],'source_promoted':False,'control_replaced':False,'one_alternative_only':True,'native_OFF_preserved':True,'fullRGBA_difference':0,'more_pelvis_lowering_m':0,'full293_upperbody_face_hair_root_path_exact':True,'TierP':0,'StageB_O1_PRIMARY_Unity_F2_F3':'HOLD','candidate_vs_control':'Alternative stored as failed evidence only; prior MIXED57d9 and original35c5/08caad7 remain immutable.'})
write(E/'SWING_GEOMETRY_CAUSAL_DIAGNOSTIC_R1.json',geo);write(E/'CONTACT_PROXY_METRICS_R1.json',qa);write(E/'WHOLE_1X_ALT_QA_R1.json',ui);write(E/'OFF_RGBA_ARRAY_EQUAL_R1.json',pixel)
rows=[]
for name in ['stop-swing-path-alt-candidate-broker-r1','stop-swing-alt-off-broker-r1','stop-swing-alt-probe-broker-r1','stop-swing-alt-full-preview-broker-r1']:
 p=BASE/name/'NATIVE_GUARD_RESULT.json';v=load(p);assert v['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN';rows.append({'run':name,'receipt':str(p),'sha256':sha(p),'status':v['guard_status'],'wall_seconds':v['wall_seconds']})
write(E/'NATIVE_CUSTODY_R1.json',rows)
frames=[246,247,248,249];sheet=Image.new('RGB',(1024*4,408),'white')
for i,f in enumerate(frames):sheet.paste(Image.open(D/'pair-frames-side'/f'{f:04}.jpg'),(i*1024,0))
sheet.save(D/'SIDE_KNEE_BRANCH_FAILURE_246_249_R1.jpg',quality=94)
report='''# One stop-swing path alternative: causal temporal failure

The candidate is FAILED source evidence, not a promoted animation. R4 authority(a30fc513), original walk35c5 and MIXED stop57d9 are immutable. One distinct alternative only; no replacement of control/rig/mesh/weights/rest/material/keys/drivers or product repo. Existing44 TierC/0 TierP. StageB/O1/PRIMARY/F2/F3/Unity HOLD.

## Evidence and alternative

In57d9 at frame248, foot-cohort X targets remain separate(L+0.104m/R−0.063m), while L knee moves medially to−0.013m near R knee−0.040m. Changing to R-first was not justified by a crossing of foot targets. Instead the alternative retains existing L-first/R-second foot goals and35mm clearance, with a smooth L knee-X corridor derived from hip geometry. No stronger foot tolerance, extra pelvis lowering, root freeze or new rig/export/provider. Original contact3mm and native delta0.8rad gates retained; knee corridor residual2mm gate.

Frame248 knee-X gap improves26.328mm→101.742mm, and the rendered frontal silhouette loses its pronounced knee crossing. Support cohort ranges/speeds and foot goals remain effectively unchanged. All293 native mesh finite, all284 outside244..252 evaluated-body hashes exact against57d9. Original86 prior Actions and original appearance OFF are preserved. Root, pelvis, head, face/hair root transport and upper-body world data exact all293. OFF saved reopen packed texture/resolved properties and neutral fullRGBA difference0. Action-only library has0 objects/meshes/armatures.

## Why it fails

Frame247 L knee worldY−1.4963m changes to−1.6865m at248; total native knee step190.580mm vs prior maximum86.646mm in the same window. X-only corridor leaves the front/back bend branch free, and independent per-frame solving selects a different depth branch while satisfying foot placement. This causal inference is supported by the unchanged foot targets/root and the measured sign switch relative to the hip. Numerical foot support and one frontal screenshot did not certify temporal quality.

All three same-camera before/after9.766667s movies are whole-decoded and actual UI1x ended/errornull. Changed9frames alone rendered with unchanged512×384/CPU2samples/seed0/JPEG92; other284 frames reused with native hash proof. The side246..249 strip and full MP4 preserve the regression. Failure verdict applies to stop continuity, not merely renderer/noise. No additional variant was attempted within this one-alternative scope.

## Reuse / next scope

The failed editable OFF file, Action-only library, original source/control, numeric full before/after arrays, scripts, cameras, full1x MP4 and closed guard/member-SHA custody are preserved privately. Do not use this alternative to replace57d9 or canonical R4. Scripts use desktop scoped paths; relocated replay needs remapped paths and new exact guard argv authority. No raw private geometry/motion committed publicly.

Hold this stop bridge. A later authorized correction needs a full forward knee pole and temporal branch continuity alongside the contact goals, not a stronger foot IK/extra pelvis offset. Per PM, do not expand a contact framework now: proceed independent81..98 proxy-transition scope or next staged first-batch coverage gap. The original6 Reaction/native corrective and first4 remain unchanged; Unity AlwaysAnimate/state/time/weight gates remain consumer-owned.
'''
with (E/'YURI_R4_STOP_SWING_PATH_CAUSAL_FAILURE_R1.md').open('x',encoding='utf8') as f:f.write(report)
files={}
def add(p,n):
 p=Path(p);assert p.is_file() and n not in files;files[n]=p
for p,n in [(c['candidate'],'failed-candidate'),(before['candidate'],'before-control'),(authority['source'],'source')]:add(p,n+'/'+Path(p).name)
for folder in ['stop-swing-path-alt-candidate-r1','stop-swing-path-alt-off-qa-r1']:
 for p in (BASE/folder).rglob('*'):
  if p.is_file() and p.suffix not in ['.blend','.blend1']:add(p,'private-evidence/'+folder+'/'+p.relative_to(BASE/folder).as_posix())
for p in (BASE/'stop-swing-path-alt-off-qa-r1').glob('*.blend'):add(p,'animation-only/'+p.name)
for p in D.iterdir():
 if p.is_file():add(p,'review/'+p.name)
for p in E.iterdir():add(p,'metadata/'+p.name)
for name in [r['run'] for r in rows]:
 for p in (BASE/name).rglob('*'):
  if p.is_file():add(p,'native-custody/'+name+'/'+p.relative_to(BASE/name).as_posix())
for p in LAB.joinpath('scripts').glob('r4_stop_swing*.py'):add(p,'workflow/'+p.name)
for name in ['r4_appearance_adapter.py','r4_appearance_signature.py','native_preservation.py']:add(LAB/'scripts'/name,'workflow/'+name)
for view in ['front','quarter','side']:add(BASE/'stop-swing-path-alt-preview-r1'/view/'RENDER_RECEIPT_R4.json','camera/'+view+'_RENDER_RECEIPT_R4.json')
index={n:{'bytes':p.stat().st_size,'sha256':sha(p)} for n,p in sorted(files.items())};idx=D/'MEMBER_SHA256_INDEX_R1.json';write(idx,index);add(idx,idx.name)
zp=BASE/'YURI_R4_STOP_SWING_PATH_CAUSAL_FAILURE_R1_20261004.zip'
with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):z.write(p,n)
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 for n,v in index.items():
  data=z.read(n);assert len(data)==v['bytes'] and hashlib.sha256(data).hexdigest()==v['sha256']
 assert len(z.namelist())==len(files)
receipt={'file':str(zp),'bytes':zp.stat().st_size,'sha256':sha(zp),'members':len(files),'indexed_members':len(index),'CRC_all_members':'PASS','all_indexed_member_bytes_SHA':'PASS','candidate_bytes':c['candidate_bytes'],'candidate_sha256':c['candidate_SHA'],'control_sha256':before['candidate_SHA'],'authority_sha256':authority['source_SHA'],'source_motion_quality':'FAIL_KNEE_DEPTH_BRANCH_POP','promoted':False};write(E/'PRIVATE_PACKET_RECEIPT_R1.json',receipt);write(D/'PRIVATE_PACKET_RECEIPT_R1.json',receipt)
assert sha(before['candidate'])==before['candidate_SHA'] and sha(authority['source'])==authority['source_SHA'];print(json.dumps(receipt,indent=2))
