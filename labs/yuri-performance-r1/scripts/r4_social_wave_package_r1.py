"""Existing source/Action/native-custody delivery path for one authored social wave."""
from pathlib import Path
import json,hashlib,zipfile,numpy as np
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');L=Path(__file__).resolve().parents[1];D=B/'alpha-social-wave-delivery-r1';E=L/'evidence/alpha-social-greeting-source-candidate-r1'
def load(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):
 with p.open('x',encoding='utf8') as f:json.dump(x,f,indent=2)
c=load(B/'alpha-social-wave-candidate-r1/SOCIAL_WAVE_CANDIDATE_PRIVATE_R1.json');off=load(B/'alpha-social-wave-off-qa-r1/OFF_REOPEN_ORACLE_R3.json');pix=load(B/'alpha-social-wave-off-qa-r1/OFF_RGBA_ARRAY_EQUAL_R1.json');ui=load(D/'WHOLE_1X_UI_QA_R1.json');assert pix['all_channels_exact'] and all(x['ended'] and x['playbackRate']==1 and x['error'] is None for x in ui['end']);assert sha(c['source'])==c['source_SHA'] and sha(c['candidate'])==c['candidate_SHA'];E.mkdir(exist_ok=False)
rows=c['frames_private'];right=np.array([x['joints']['hand.R'] for x in rows]);quiet={n:np.ptp([r['joints'][n] for r in rows],axis=0).tolist() for n in ['root','pelvis','head','hand.L','foot.L','foot.R']}
manifest={k:v for k,v in c.items() if k!='frames_private'};manifest.update({'OFF_reopen':off,'OFF_neutral_RGBA':pix,'right_hand_world_range_m':np.ptp(right,axis=0).tolist(),'right_hand_start_end_distance_m':float(np.linalg.norm(right[-1]-right[0])),'quiet_joint_ranges_m':quiet,'lineage_license':'Native procedural authored Action in this research workspace; no external donor source/license/download','normal_speed_UI':ui,'visual_verdict':'SOURCE_ONLY_PROVISIONAL: greeting readable; no gross shoulder/elbow/forearm/wrist break or arm/head/torso penetration observed across three normal-speed previews','remaining_defects':['Finger articulation and skin quality HOLD: source finger transforms retained, low-sample512x384 evidence insufficient for fingertip/webbing acceptance','Exact skin self-intersection/contact certificate HOLD; three-view visual observation only','Neutral face/head held; body-only first greeting, no expressive face overlay added','Raise/recovery still generic and restrained; wrist wave short and modest; not a polished signature performance'],'Stage_B_Unity_TierP':'HOLD / 0; source-only candidate, not Stage B completion','old_controls_preserved':True});write(E/'SOCIAL_GREETING_MANIFEST_R1.json',manifest)
write(E/'ACTION_ONLY_CUSTODY_R1.json',load(B/'alpha-social-wave-off-qa-r1/ACTION_ONLY_CUSTODY_R1.json'))
guards=[]
for run in ['alpha-social-wave-candidate-broker-r1','alpha-social-wave-off-broker-r1','alpha-social-wave-probe-broker-r3','alpha-social-wave-full-broker-r1']:
 p=B/run/'NATIVE_GUARD_RESULT.json';v=load(p);assert v['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN';guards.append({'run':run,'receipt':str(p),'sha256':sha(p),'status':v['guard_status'],'wall_seconds':v['wall_seconds']})
write(E/'NATIVE_CUSTODY_R1.json',guards)
write(E/'FAILURE_CORRECTION_LOG_R1.json',{'probe_r1':'ModuleNotFoundError due to missing explicit script-dir import path; native owned process safely drained, no source mutation/candidate change','probe_broker_r2':'Preparation failed before native launch due to Python encoding alias typo utf8-sig; partial payload retained','probe_r3':'Same unchanged candidate/helper, explicit wrapper script path fixed in new collector; native PASS','motion_alternative_count':0,'walk_stop_knee_resumed':False})
(E/'YURI_R4_SOCIAL_GREETING_SOURCE_R1.md').write_text('''# Original R4 social greeting: one authored source candidate

One right-hand native Action was authored because the existing staged/curated SOCIAL coverage explicitly lacks validated wave/greeting. No new donor scan, download or export architecture. Immutable source a30fc513, all existing 78 Actions, skeleton/rest/hierarchy/weights/materials/nodes/textures/ShapeKeys/face-gaze drivers and head/hair remain intact. Before/save-reopen OFF appearance checks passed; full neutral RGBA difference is zero. Raw texture locator strings remap on SaveAs; resolved paths, packed bytes and colorspace remain identical.

The one additive YURI_R4_SOCIAL_GREETING_WAVE_BODY_R1 Action targets existing Meshy_Fitted_Rig and only upper_arm.R, forearm.R, hand.R quaternion channels. Local rest-aware FK orientations preserve native lengths. All root/legs/left hand/head joints stay fixed. No new rig, constraints, skin, geometry, donor-body or facial input. The candidate is saved OFF, at original scene24fps. Action playback is30fps,91 native frames,3.0sec key interval/3.033333sec container.

Timing:1–12 anticipation;13–31 raise;32–59 two small wrist/forearm waves;60–67 hold;68–91 recovery. End/start wrist joint positions match exactly. All91 evaluated body vertex buffers finite. Full front/quarter/side fixed50mm512×384 CPU2sample/JPEG92 renders were encoded at30fps, decoded through all91frames and actually played through the end at1x in the local QA page. The manifest records observed player state, camera receipts, hashes and scalar native motion evidence.

Across the full normal-speed previews no gross shoulder/elbow/forearm/wrist break or arm/head/torso penetration was observed. Low resolution/noise prevents finger-webbing, exact skin self-intersection or final facial fidelity acceptance. Source fingers remain unmodified/HOLD. Neutral face/head and modest wrist wave are deliberate body-only scope limitations; no signature-performance quality, Unity Tier-P or Stage B completion is claimed.

Bind the single Action using the existing ReactionLane adapter; evaluate1..91 at30fps, then off() restores original pose/frame/binding. No head/hair transport Actions are needed because torso/head never move. The Action-only BLEND contains zero objects/meshes/armatures. Canonical source, editable OFF candidate, Action library, lineage/timing/camera/native evidence and full1x movies are in the private packet. Relocated replay requires scoped path remapping/new exact native guard. Existing 08caad7, six Reactions, first4/C1/walk controls and failed stop alternatives are preserved.

Next safe same-scope step: consumer reviews this one body-only greeting and decides whether hand/finger close-up or actual Unity binding is useful; no further motions or facial layers generated in this checkpoint.
''',encoding='utf8')
files={}
def add(p,n):
 p=Path(p);assert p.is_file() and n not in files;files[n]=p
add(c['source'],'source/'+Path(c['source']).name);add(c['candidate'],'candidate/'+Path(c['candidate']).name)
for folder in ['alpha-social-wave-candidate-r1','alpha-social-wave-off-qa-r1']:
 for p in (B/folder).rglob('*'):
  if p.is_file() and p.suffix not in ['.blend','.blend1']:add(p,'private-evidence/'+folder+'/'+p.relative_to(B/folder).as_posix())
for p in (B/'alpha-social-wave-off-qa-r1').glob('*.blend'):add(p,'animation-only/'+p.name)
for p in E.iterdir():add(p,'metadata/'+p.name)
for p in D.iterdir():
 if p.is_file():add(p,'review/'+p.name)
for run in [g['run'] for g in guards]+['alpha-social-wave-probe-broker-r1','alpha-social-wave-probe-broker-r2']:
 for p in (B/run).rglob('*'):
  if p.is_file():add(p,'native-custody/'+run+'/'+p.relative_to(B/run).as_posix())
for view in ['front','quarter','side']:add(B/'alpha-social-wave-preview-r1'/view/'RENDER_RECEIPT_R4.json','camera/'+view+'_RENDER_RECEIPT_R4.json')
for p in (L/'scripts').glob('r4_social_wave*.py'):add(p,'workflow/'+p.name)
for n in ['r4_appearance_adapter.py','r4_appearance_signature.py','native_preservation.py']:add(L/'scripts'/n,'workflow/'+n)
idx={n:{'bytes':p.stat().st_size,'sha256':sha(p)} for n,p in sorted(files.items())};ip=D/'MEMBER_SHA256_INDEX_R1.json';write(ip,idx);add(ip,ip.name)
zp=B/'YURI_R4_SOCIAL_GREETING_SOURCE_ONLY_R1_20261004.zip'
with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):z.write(p,n)
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 for n,v in idx.items():
  b=z.read(n);assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256']
 receipt={'file':str(zp),'bytes':zp.stat().st_size,'sha256':sha(zp),'members':len(z.namelist()),'indexed_members':len(idx),'CRC_SHA_size_all_members':'PASS','candidate_SHA256':c['candidate_SHA'],'source_SHA256':c['source_SHA'],'TierP':0,'source_only':True}
write(E/'PRIVATE_PACKET_RECEIPT_R1.json',receipt);write(D/'PRIVATE_PACKET_RECEIPT_R1.json',receipt);print(json.dumps(receipt,indent=2))
