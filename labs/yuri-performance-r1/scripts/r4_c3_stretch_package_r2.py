"""Seal one existing C3 stretch plus explicit neutral recovery; contact/fingers remain HOLD."""
from pathlib import Path
import json,hashlib,zipfile,numpy as np
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');L=Path(__file__).resolve().parents[1];D=B/'alpha-c3-stretch-delivery-r2';E=L/'evidence/alpha-c3-stretch-source-candidate-r2'
def load(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
 with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
c=load(B/'alpha-c3-stretch-candidate-r2/C3_STRETCH_CANDIDATE_PRIVATE_R2.json');control=load(B/'alpha-c3-stretch-candidate-r1/C3_STRETCH_CANDIDATE_PRIVATE_R1.json');off=load(B/'alpha-c3-stretch-off-qa-r2/OFF_REOPEN_ORACLE_R3.json');pixel=load(B/'alpha-c3-stretch-off-qa-r2/OFF_RGBA_ARRAY_EQUAL_R1.json');ui=load(D/'WHOLE_1X_UI_QA_R2.json');assert pixel['all_channels_exact'] and all(x['ended'] and x['playbackRate']==1 and x['error'] is None for x in ui['end']);assert sha(c['candidate'])==c['candidate_SHA'] and sha(c['source'])==c['source_SHA'];E.mkdir(exist_ok=False)
rows=c['frames_private'];qa={}
for n in ['root','pelvis','head','hand.L','hand.R','foot.L','foot.R']:
 a=np.array([r['joints'][n] for r in rows]);qa[n]={'full_range_m':np.ptp(a,axis=0).tolist(),'start_end_distance_m':float(np.linalg.norm(a[-1]-a[0])),'donor215_to_recovery216_step_m':float(np.linalg.norm(a[215]-a[214])),'recovery215_to263_displacement_m':float(np.linalg.norm(a[-1]-a[214])),'recovery_path_length_m':float(np.linalg.norm(np.diff(a[214:],axis=0),axis=1).sum())}
sole_qa={}
for side in ['L','R']:
 a=np.array([r['soles'][side]['centroid'] for r in rows]);z=np.array([r['soles'][side]['offset_m'] for r in rows]);sole_qa[side]={'recovery_fixed_original_sole_cohort_centroid_XY_shift_m':float(np.linalg.norm((a[-1]-a[214])[:2])),'recovery_minimum_cohort_vertex_clearance_range_m':[float(z[214:].min()),float(z[214:].max())],'scope':'Fixed original-neutral sole vertex cohort; minimum clearance/centroid is kinematic diagnostic, not authored physical contact certificate'}
summary={k:v for k,v in c.items() if k!='frames_private'};summary.update({'task':'ROOT_PM_EXISTING_STRETCH_SOURCE_CANDIDATE_R1','legacy_collector_labels_disclosed':'Raw receipt task/segment/Reach filename retain copied C1 labels; selected source is st_arm_1_33|Scene/C3 only, not a new reach or second motion','original_BVH_fps':30.0003,'original_BVH_frames':[0,214],'original_BVH_SHA256':'9585998126bc797d362423da4587193382926808f9169eda49857362dbc05d13','staged_FBXSHA256':c['donor']['sha256'],'OFF_reopen':off,'OFF_neutral_RGBA':pixel,'native_motion_QA':qa,'sole_cohort_recovery_QA':sole_qa,'normal_speed_UI':ui,'candidate_status':'SOURCE_ONLY_MIXED_HOLD_CONTACT','visual_verdict':'Stretch and upper-body recovery readable; no gross shoulder/elbow/wrist/neck break observed in three normal-speed previews. Detailed skin/neck/finger acceptance not certified. Grounded foot slide/twist observed on recovery; fixed sole-cohort centroid XY shifts31.539/59.079mm with minimum clearance at most0.142/1.230mm. Contact quality HOLD; no contact-aware alternative attempted, candidate closed as source HOLD.','remaining_defects':['Original staged215-frame source ends in extended pose and has no donor-authored recovery; R1 kept as incomplete control','R2 recovery is48-frame quintic local quaternion/pelvis/carrier interpolation to canonical source neutral, not captured donor motion; boundary angular velocity not explicitly matched','Recovery ankle displacement47.338/59.327mm, root/carrier returns~19.581mm; no step/lift/contact plan, foot sliding/contact HOLD','Fingers remain original, no finger-curl/grip/hand-touch acceptance','Exact skin self-intersection and neck seam/final skin quality HOLD; low-sample512x384 previews only'],'source_original_78Actions_preserved':True,'all_prior_motion_controls_preserved':True,'TierP':0,'StageB_F2_final_promotion':False});write(E/'C3_STRETCH_MANIFEST_R2.json',summary);write(E/'NATIVE_MOTION_QA_R2.json',qa);write(E/'ACTION_ONLY_CUSTODY_R2.json',load(B/'alpha-c3-stretch-off-qa-r2/ACTION_ONLY_CUSTODY_R1.json'))
guards=[]
for run in ['alpha-c3-stretch-inspect-broker-r1','alpha-c3-stretch-candidate-broker-r1','alpha-c3-stretch-off-broker-r1','alpha-c3-stretch-probe-broker-r1','alpha-c3-stretch-candidate-broker-r2','alpha-c3-stretch-off-broker-r2','alpha-c3-stretch-probe-broker-r2','alpha-c3-stretch-full-broker-r2']:
 p=B/run/'NATIVE_GUARD_RESULT.json';v=load(p);assert v['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN';guards.append({'run':run,'receipt':str(p),'sha256':sha(p),'status':v['guard_status'],'wall_seconds':v['wall_seconds']})
write(E/'NATIVE_CUSTODY_R2.json',guards);write(E/'RECOVERY_CORRECTION_LOG_R2.json',{'R1_control':{k:v for k,v in control.items() if k!='frames_private'},'causal_defect':'Selected actual staged clip stops with both hands extended; no donor-authored recovery. End-start hand position differences334.618/354.360mm. It is not a loop/complete stretch-return.','one_bounded_correction':'Same source215frames retained,48quintic Action-only samples appended toward original R4 neutral; no source/skeleton/skin/rest/material edits','R2_endpoint_body_world_max_abs_difference_m':c['recovery_end_body_world_max_abs_delta_from_original_OFF_m'],'sole_cohort_recovery_QA':sole_qa,'closure':'Full source QA completed, current recovery contact-safe neutral return NOT proved. Preserve R1/R2; close contact HOLD without repeating failed knee-X/stronger IK or adding a solver. A separate authored reposition contact plan would be needed for promotion.','new_limit':'Returning leg pose and carrier to canonical rest changes grounded stance; feet/contact HOLD. No IK/stop-knee experiments resumed, no further variants generated.'})
(E/'YURI_R4_C3_STRETCH_SOURCE_R2.md').write_text('''# Original R4 C3 standing stretch: source-only candidate, contact HOLD

Selected existing first-batch C3 c7cb1c20db655031333f / StayStill st_arm_1_33, MIT. Raw BVH958599... and staged FBX9e8fa8... lineage/hashes preserved. No new donor scan/download/framework. Original staged clip contains215 frames30fps (BVH30.0003fps) and ends with arms extended; it lacks recovery. R1 candidate and receipts remain immutable as the incomplete source control. R2 keeps all215 source samples and appends48 explicitly procedural quintic recovery samples. It is one stretch candidate, not two motions or a new authored family.

Original R4a30fc513 geometry/materials/nodes/packed textures/colorspace/ShapeKeys/weights/rest/hierarchy/face-gaze drivers and78 Actions remain identical OFF. Neutral full RGBA difference0 against reused authoritative witness. Raw texture locator strings remap after SaveAs; resolved properties/packed bytes are identical. Existing greeting/C1/walk/first4/six Reaction/all failed stop controls unchanged. Original saved scene24fps; four editable body/carrier/head-hair rigid transport Actions form one263-frame30fps sequence. Action-only BLEND contains0 objects/meshes/armatures. No new GameRig/mesh merge/donor geometry.

Native rest-aware21-bone mapping retains R4 lengths/hip-height normalization and staged StayStill world axes, no mirror. Hips XY trajectory is scaled onto existing Assembly_Root; pelvis residual plus sole-support-Z correction only. Original face/gaze drivers remain authored; existing Armature.Root and Hair_HeadRoot rigidly follow body head, without new expressive facial/secondary-hair channels or rig edits. This does not certify exact neck surface continuity.

Full263 frames front/quarter/side fixed50mm512×384 CPU2sample/JPEG92 rendered, encoded at30fps, whole decoded and actually played through end at1x. Key interval8.733333sec/container8.766667sec. All263 native body vertex arrays finite. Max native joint frame step19.207mm; source stretch→procedural recovery first wrist step~0.043mm. Final recovered evaluated body world vertices equal original neutral exactly (max abs0). OFF and this endpoint result are separate tests, not Unity runtime proof.

Stretch/upper-body recovery are readable without observed gross shoulder/elbow/wrist/neck break in the previews. Contact is MIXED/HOLD: recovering to canonical rest changes ankle positions47.338/59.327mm and carrier~19.581mm, without an authored step/lift/contact plan. Fixed original sole-cohort centroid XY shifts31.539/59.079mm while minimum clearance stays within0.142/1.230mm; full1x and crop strip show grounded slide/twist. Do not treat minimum-sole-Z cleanup as a physical support certificate. Contact-aware alternative was not attempted; source HOLD closes this bounded task. A future authored reposition plan would need independent contact evidence, not root freezing or tolerance changes. Source fingers remain original; hand-touch/grip/finger curl/exact skin self-intersection/neck seam/final quality HOLD. Endpoint velocity was not explicitly fitted; neutral-entry/exit integration requires consumer review. Stage B/Unity TierP0/F2/final promotion remain HOLD.

Use existing ReactionLane for body/head/hair plus restored carrier Action binding; evaluate1..263 at30fps. Off restores original bindings/frame/poses. Packet includes immutable canonical source, editable OFF R2 candidate, four-Action library, existing MIT donor/notice, original215-source and recovery lineage, native receipts, camera metadata, full1x movies and defects. Public Git contains scripts/scalar custody only; numeric geometry/motion remains private. Relocated replay needs scoped paths/new exact native guard. Legacy copied Reach filename/raw task label does not denote another motion.

Next safe same-scope decision is consumer review of this one candidate/contact limitation; no IK or repeated walk-stop/knee forensics were resumed and no new variants were generated.
''',encoding='utf8')
files={}
def add(p,n):
 p=Path(p);assert p.is_file() and n not in files;files[n]=p
add(c['source'],'source/'+Path(c['source']).name);add(c['candidate'],'candidate/'+Path(c['candidate']).name);add(c['donor']['file'],'licensed-donor/'+Path(c['donor']['file']).name)
for folder in ['alpha-c3-stretch-inspect-r1','alpha-c3-stretch-candidate-r1','alpha-c3-stretch-off-qa-r1','alpha-c3-stretch-candidate-r2','alpha-c3-stretch-off-qa-r2']:
 for p in (B/folder).rglob('*'):
  if p.is_file() and p.suffix not in ['.blend','.blend1']:add(p,'private-evidence/'+folder+'/'+p.relative_to(B/folder).as_posix())
for p in (B/'alpha-c3-stretch-off-qa-r2').glob('*.blend'):add(p,'animation-only/'+p.name)
for p in E.iterdir():add(p,'metadata/'+p.name)
for p in (B/'alpha-c3-stretch-recovery-visual-qa-r2').iterdir():add(p,'recovery-visual/'+p.name)
for p in D.iterdir():
 if p.is_file():add(p,'review/'+p.name)
for g in guards:
 for p in (B/g['run']).rglob('*'):
  if p.is_file():add(p,'native-custody/'+g['run']+'/'+p.relative_to(B/g['run']).as_posix())
for view in ['front','quarter','side']:add(B/'alpha-c3-stretch-preview-r2'/view/'RENDER_RECEIPT_R4.json','camera/'+view+'_RENDER_RECEIPT_R4.json')
for p in (L/'scripts').glob('r4_c3_stretch*.py'):add(p,'workflow/'+p.name)
for n in ['r4_appearance_adapter.py','r4_appearance_signature.py','native_preservation.py']:add(L/'scripts'/n,'workflow/'+n)
lic=Path('C:/Users/JAEWAN/.codex/worktrees/common-motion-curation-r1/yuri-room-mvp/common-motion-r1/licenses/StayStill-LICENSE.txt');add(lic,'licenses/'+lic.name)
idx={n:{'bytes':p.stat().st_size,'sha256':sha(p)} for n,p in sorted(files.items())};ip=D/'MEMBER_SHA256_INDEX_R2.json';write(ip,idx);add(ip,ip.name)
zp=B/'YURI_R4_C3_STRETCH_SOURCE_ONLY_R2_20261004.zip'
with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):z.write(p,n)
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 for n,v in idx.items():
  b=z.read(n);assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256']
 receipt={'file':str(zp),'bytes':zp.stat().st_size,'sha256':sha(zp),'members':len(z.namelist()),'indexed_members':len(idx),'CRC_SHA_size_all_members':'PASS','candidate_SHA256':c['candidate_SHA'],'source_SHA256':c['source_SHA'],'TierP':0,'source_only':True,'status':'SOURCE_ONLY_MIXED_HOLD_CONTACT'}
write(E/'PRIVATE_PACKET_RECEIPT_R2.json',receipt);write(D/'PRIVATE_PACKET_RECEIPT_R2.json',receipt);print(json.dumps(receipt,indent=2))
