"""Close the timing-only source packet; no claim of baseline contact repair."""
from pathlib import Path
import json,hashlib,zipfile
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');L=Path(__file__).resolve().parents[1];D=B/'alpha-reach-left-finger-timing-delivery-r2';E=L/'evidence/alpha-reach-left-finger-timing-r2';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
 with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
c=load(B/'alpha-reach-left-finger-timing-candidate-r2/REACH_LEFT_FINGER_TIMING_CANDIDATE_PRIVATE_R2.json');off=load(B/'alpha-reach-left-finger-timing-off-qa-r2/OFF_REOPEN_ORACLE_R3.json');pix=load(B/'alpha-reach-left-finger-timing-off-qa-r2/PIXEL_ORACLE_R2.json');pair=load(B/'alpha-reach-left-finger-timing-paired-qa-r2/PAIRED_SURFACE_ORACLE_PRIVATE_R2.json');ui=load(D/'WHOLE_1X_UI_QA_R2.json');assert pix['PASS'] and c['nonfinger_C1_same_time_world_matrix_max_error']==0 and c['composition_start_end_body_local_error_m']==0;assert all(v['ended'] and v['playbackRate']==1 and v['error'] is None for v in ui['end']);assert sha(c['source'])==c['source_SHA'] and sha(c['candidate'])==c['candidate_SHA'];E.mkdir(exist_ok=False)
summary={k:v for k,v in c.items() if k not in ['frames_private','left_finger_inventory_private','left_finger_axes_private']};summary.update({'baseline_remaining_defects':load(B/'alpha-reach-left-finger-timing-paired-qa-r2/C1_BASELINE_REMAINING_DEFECTS_R2.json'),'timing_only_lineage_oracle':load(B/'alpha-reach-left-finger-timing-paired-qa-r2/TIMING_ONLY_LINEAGE_ORACLE_R2.json'),'OFF_reopen':off,'OFF_pixels':pix,'paired_oracle':{k:v for k,v in pair.items() if k!='frames_private'},'normal_speed_UI':ui,'status':'SOURCE_ONLY_TIMING_ADDED_INTERSECTION_'+pair['added_intersections_subset']+'_BASELINE_CONTACT_HOLD','C1_baseline':'FAIL_HOLD','original_neutral':'HOLD: C1 endpoint remains different, OFF restores original authority','source_only':True,'TierP':0,'no_product_or_laptop_edits':True,'prior_checkpoint':'1153398','private_control_packet_SHA':'68b46806fef28dbaeeb7221ca38fdfbe4f876a75f0c653d56d0facb28751516d','action_custody_note':'Seven named playback/control Actions; candidate also retains four unused duplicated C1 library Actions from independent lineage loads, unbound, source-owned curves unmodified. Action-only delivery contains only seven named Actions.'});write(E/'TIMING_SOURCE_MANIFEST_R2.json',summary);write(E/'ACTION_ONLY_CUSTODY_R2.json',load(B/'alpha-reach-left-finger-timing-off-qa-r2/ACTION_ONLY_CUSTODY_R1.json'))
guards=[]
for run in ['o1-reach-left-finger-timing-candidate-r2','o1-reach-left-finger-timing-paired-r2','o1-reach-left-finger-timing-off-r2','o1-reach-left-finger-timing-full-r2','o1-reach-left-finger-timing-full-r2b']:
 p=B/run/'NATIVE_GUARD_RESULT.json';v=load(p);assert v['guard_status']==('FAIL' if run=='o1-reach-left-finger-timing-full-r2' else 'PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN');guards.append({'run':run,'SHA':sha(p),'status':v['guard_status'],'wall_seconds':v['wall_seconds']})
write(E/'NATIVE_CUSTODY_R2.json',guards)
(E/'YURI_R4_C1_FINGER_TIMING_R2.md').write_text('''# R4 C1 LEFT finger timing-only derivative R2

Full-render wrapper R2 failed before rendering due to missing sibling-module import path (ModuleNotFoundError); protected processes unchanged, owned exit95/drain0. Failure packet retained; new R2b wrapper restores local script path only and uses same pinned preview/candidate/guard.

Existing C1 body/arm/wrist/root/head/hair curves and all original R4 source content preserved. One new native LEFT15-finger quaternion Action keeps R1 axes, amplitude and onset, holds peak31–32, releases33–44, exactly open45–61 before previously measured return51–55 intersections. No rest/weight/material/driver or source file edit. Original right and previous left Actions retained unbound. Seven named playback/control Actions in animation-only library; no objects/mesh/rig. Candidate additionally retains four unused duplicated C1 lineage Actions, unbound. Transient fixed NLA adapter removes its track and restores original authority on off(). Source24fps preserved; authored61frames30fps.

Same-frame all61 C1 nonfinger world matrices/carrier/face/hair transport error0. Original78Actions preserved, candidate OFF signatures exact, reopen original geometry/materials/slots/keys/weights/rest/drivers and resolved packed textures exact. SaveAs raw relative texture locator strings may remap; pixels checked with original source camera deterministic CPU8samples. Endpoint equals C1 baseline, not canonical neutral: original-neutral return HOLD. No C1 baseline contact repair claimed.

Actual paired evaluated-surface oracle compares identical triangle ID sets, not only counts, at every OFF/ON frame. New intersection subset decision and every measured pair are in manifest. Dominant digit weight>=.5 and non-hand body triangles excluding left-hand/finger weight>.01; triangle intersections are not depth/volume or whole-body/hair collision certificate. All four61-frame normal-speed movies fully decoded and actual1x UI through-end. Existing C1 baseline collisions stay FAIL/HOLD, prop/physics/Unity/MUG/StageB/F2/TierP0. Candidate is source experiment only; immutable R4 source remains visual authority and original08caad7/prior controls are retained.
''',encoding='utf-8')
files={}
def add(p,n):
 p=Path(p);assert p.is_file() and n not in files;files[n]=p
add(c['source'],'source/'+Path(c['source']).name);add(c['candidate'],'candidate/'+Path(c['candidate']).name)
for folder in ['alpha-reach-left-finger-timing-candidate-r2','alpha-reach-left-finger-timing-off-qa-r2','alpha-reach-left-finger-timing-paired-qa-r2']:
 for p in (B/folder).rglob('*'):
  if p.is_file() and p.suffix not in ['.blend','.blend1']:add(p,'private-evidence/'+folder+'/'+p.relative_to(B/folder).as_posix())
for p in (B/'alpha-reach-left-finger-timing-off-qa-r2').glob('*.blend'):add(p,'animation-only/'+p.name)
for p in E.iterdir():add(p,'metadata/'+p.name)
for p in D.iterdir():
 if p.is_file():add(p,'review/'+p.name)
add(B/'alpha-reach-left-finger-timing-preview-r2/RENDER_RECEIPT_R1.json','camera/RENDER_RECEIPT_R2.json')
for g in guards:
 for p in (B/g['run']).rglob('*'):
  if p.is_file():add(p,'native-custody/'+g['run']+'/'+p.relative_to(B/g['run']).as_posix())
for p in (L/'scripts').glob('r4_reach_left_finger_timing*.py'):add(p,'workflow/'+p.name)
for n in ['r4_appearance_adapter.py','r4_appearance_signature.py','native_preservation.py']:add(L/'scripts'/n,'workflow/'+n)
add(Path('C:/Users/JAEWAN/.codex/worktrees/common-motion-curation-r1/yuri-room-mvp/common-motion-r1/licenses/Quaternius-LICENSE.txt'),'licenses/Quaternius-LICENSE.txt')
idx={n:{'bytes':p.stat().st_size,'sha256':sha(p)} for n,p in sorted(files.items())};ip=D/'MEMBER_SHA256_INDEX_R2.json';write(ip,idx);add(ip,ip.name);zp=B/'YURI_R4_C1_LEFT_FINGER_TIMING_SOURCE_ONLY_R2_20261004.zip'
with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):z.write(p,n)
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 for n,v in idx.items():
  raw=z.read(n);assert len(raw)==v['bytes'] and hashlib.sha256(raw).hexdigest()==v['sha256']
 receipt={'file':str(zp),'bytes':zp.stat().st_size,'sha256':sha(zp),'members':len(z.namelist()),'indexed_members':len(idx),'CRC_SHA_size_all_members':'PASS','source_SHA':c['source_SHA'],'candidate_SHA':c['candidate_SHA'],'added_intersections_subset':pair['added_intersections_subset'],'C1_baseline_contact':'FAIL_HOLD','original_neutral_return':'HOLD','TierP':0};write(E/'PRIVATE_PACKET_RECEIPT_R2.json',receipt);write(D/'PRIVATE_PACKET_RECEIPT_R2.json',receipt);print(json.dumps(receipt,indent=2))
