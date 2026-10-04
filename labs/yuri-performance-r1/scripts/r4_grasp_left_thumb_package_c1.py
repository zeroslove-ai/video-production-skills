"""Preserve one failed thumb correction, source-only artifact and reproducible QA."""
from pathlib import Path
import json,hashlib,zipfile
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');L=Path(__file__).resolve().parents[1];D=B/'alpha-grasp-left-thumb-delivery-c1';E=L/'evidence/alpha-grasp-left-thumb-c1';E.mkdir(exist_ok=False)
def load(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
 with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
d=load(B/'alpha-grasp-left-thumb-c1/LEFT_THUMB_C1_PRIVATE_MANIFEST.json');r=load(B/'alpha-grasp-left-thumb-preview-c1/THUMB_C1_RENDER_RECEIPT.json');p=load(D/'OFF_PIXEL_ORACLE_C1.json');u=load(D/'WHOLE_1X_UI_QA_C1.json');v=load(D/'VISUAL_QA_C1.json');assert p['PASS'] and r['OFF_full_snapshot_restored'];assert all(x['ended'] and x['playbackRate']==1 and x['error'] is None for x in u['end']);assert sha(d['candidate'])==d['candidate_SHA'] and sha(d['source'])==d['source_SHA'] and sha(d['base_candidate'])==d['base_candidate_SHA']
bad=[x['frame'] for x in d['frames_private'] if x['new_pairs_same_frame']['nonadjacent_all_body']];summary={k:x for k,x in d.items() if k not in ['frames_private','native_axis']};summary.update({'native_axis_basis':d['native_axis']['basis'],'opposition_degrees':20,'longitudinal_roll_degrees':10,'source_reference_frame':85,'target_distance_units':'Recorded thumb_tip_to_finger_target_m is RIG-SPACE Blender coordinate distance, not world metric distance. Ratio only; no physicalmm claim.','contact_failure_frames':bad,'baseline_maximum_actual_pairs':{k:max(x['before_counts'][k] for x in d['frames_private']) for k in d['frames_private'][0]['before_counts']},'cameras':r['views'],'OFF_RGBA':p,'normal_speed':u,'visual_QA':v,'action_only':r['library'],'status':'FAIL_HOLD: one thumb-shape correction creates new nonadjacent palm/digit intersection','next_one_alternative':'Proposed ONLY thumb phase gate: delay opposition onset until after native finger/hand transition61, ramp62–85 into collision-free hold and release before later return. Preserve20deg10deg/native axes/all other motion. NOT EXECUTED; no second candidate in this task.','source_appearance_promoted':False,'physics_MUG_F2_Unity_TierP':'HOLD/TierP0','Root_Laptop_Talk':'Independent sole Laptop runtime integration, nonblocking'})
write(E/'LEFT_THUMB_C1_SOURCE_QA_MANIFEST.json',summary)
(E/'YURI_R4_LEFT_THUMB_ONE_CORRECTION_C1.md').write_text('''# One LEFT thumb opposition correction: FAIL/HOLD

ONE candidate only, based on immutable original R4 and prior native Grasp169frames24fps. Existing actual LEFT thumb1 base/tip and index2/middle2 pose at85 define local correction axis; no failed right-R5 constants or donor/rig reconstruction. Separate Action COPY changes only thumb1.L quaternion4channels: smooth20degree toward-finger opposition plus10degree longitudinal roll, existing19–57/121–156 thumb envelope. Other290curves/timing and all prior81Actions including original78 remain exact. Wrist/body/root/feet/face/hair pose matrices and zero-thumb-weight evaluated body geometry difference0 all169. Endpoints1/169 original-base neutral geometry0, saved/reopened OFF full signature0 and source-camera960×920RGBA changed pixels0. New character appearance/weights/rig/exporter/material/physics changes0.

Actual inclusive surface test deliberately expands prior dominant-weight-only scope: ALL body triangles with ANY thumb1/2/3.L weight>.01 versus ALL actual body triangles, including hand.L-weight palm, other digit weak weight and webbing. Same-frame before/after on all169. Shared-vertex adjacency raw reported separately (baseline maximum491, candidate466), not silently discarded or claimed as penetration depth. Identical triangle raw0. Nonadjacent baseline0; correction maximum98 new all-body intersections, palm-influenced15, other-digit-influenced94 (overlapping categories, do not sum). Fail15frames47–61; hold85 has0. Thus collision FAIL/HOLD despite closer tip-to-target and unchanged body. Full containment/adjacent deformation/physical contact not certified.

Whole169frames24fps7.041667sec LEFT active close and fixed waist before/after comparisons encoded/full decoded/actually1x played through-end, supplemented by all-frame paired grids. Camera: LEFT wrist world translation follow with constant target offset/fixed rotation, same original512square CPU8samples/light/material; fixed waist384square2samples same prior camera. OFF full settings restoration is explicit; original earlier render-setting failure retained unchanged. Visible thumb is pulled into palm/finger-base during turning/curl transition; hold is closer but incomplete grip, not a grasp approval. Failure rather than global acting/rig research.

Candidate/source Action-only3/0objects/meshes/rigs and fixed original-three-rig adapter are packaged privately with numeric motion/contact data, two before/after videos, cameras, guard receipts and full-memberSHA/size/CRC index. Source/old candidates/closed packets/08caad7 remain unchanged; public Git only scripts/scalar QA/pointers. Two CPU-only exact-scope guard jobs retain unchanged limits and strict barriers. MUG/physics/F2/Unity/TierP0 remain HOLD; sole Laptop grounded Talk integration independent.

One different next hypothesis, proposed NOT executed: change only thumb opposition phase envelope to start after transition61 and ramp62–85 into the observed collision-free hold, release before native return. Keep source wrist/body/finger tracks and current actual native axis unchanged, then repeat inclusive contact+whole1x before/after. No second motion candidate produced here.
''',encoding='utf-8')
guards=[]
for run in ['o1-grasp-left-thumb-c1','o1-grasp-left-thumb-preview-c1']:
 f=B/run/'NATIVE_GUARD_RESULT.json';g=load(f);assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN';guards.append({'run':run,'SHA':sha(f),'status':g['guard_status'],'seconds':g['wall_seconds']})
write(E/'NATIVE_CUSTODY_C1.json',guards);files={}
def add(p,n):p=Path(p);assert p.is_file() and n not in files;files[n]=p
add(d['candidate'],'candidate-OFF/'+Path(d['candidate']).name);add(r['library']['file'],'animation-only/'+Path(r['library']['file']).name);add(B/'alpha-grasp-left-thumb-c1/LEFT_THUMB_C1_PRIVATE_MANIFEST.json','private-QA/LEFT_THUMB_C1_PRIVATE_MANIFEST.json');add(B/'alpha-grasp-left-thumb-preview-c1/THUMB_C1_RENDER_RECEIPT.json','private-QA/THUMB_C1_RENDER_RECEIPT.json');add(B/'alpha-grasp-left-thumb-preview-c1/CANDIDATE_OFF_SOURCE_NEUTRAL_C1.png','private-QA/CANDIDATE_OFF_SOURCE_NEUTRAL_C1.png')
for f in D.iterdir():
 if f.is_file():add(f,'review/'+f.name)
for f in E.iterdir():add(f,'metadata/'+f.name)
for g in guards:
 for f in (B/g['run']).rglob('*'):
  if f.is_file():add(f,'native-custody/'+g['run']+'/'+f.relative_to(B/g['run']).as_posix())
for f in (L/'scripts').glob('r4_grasp_left_thumb*.py'):add(f,'workflow/'+f.name)
for n in ['r4_native_grasp_adapter_r1.py','r4_appearance_signature.py','r4_appearance_adapter.py']:add(L/'scripts'/n,'workflow/'+n)
idx={n:{'bytes':f.stat().st_size,'SHA':sha(f)} for n,f in sorted(files.items())};ip=D/'MEMBER_SHA256_INDEX_C1.json';write(ip,idx);add(ip,ip.name);zp=B/'YURI_R4_LEFT_THUMB_OPPOSITION_FAIL_CONTROL_C1_20261005.zip'
with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,f in sorted(files.items()):z.write(f,n)
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 for n,x in idx.items():raw=z.read(n);assert len(raw)==x['bytes'] and hashlib.sha256(raw).hexdigest()==x['SHA']
 receipt={'file':str(zp),'SHA':sha(zp),'bytes':zp.stat().st_size,'members':len(z.namelist()),'indexed_members':len(idx),'CRC_SHA_size_all':'PASS','source_SHA':d['source_SHA'],'base_candidate_SHA':d['base_candidate_SHA'],'candidate_SHA':d['candidate_SHA'],'library_SHA':r['library']['SHA'],'candidate_verdict':'FAIL/HOLD: new thumb-palm/other-digit intersections47–61','OFF_pixels':p,'TierP':0};write(E/'PRIVATE_PACKET_RECEIPT_C1.json',receipt);print(json.dumps(receipt,indent=2))
