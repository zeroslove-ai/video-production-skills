"""Close one immutable existing native source candidate; scalar public QA only."""
from pathlib import Path
import json, hashlib, zipfile
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
L=Path(__file__).resolve().parents[1]; D=B/'alpha-native-grasp-delivery-r1'; E=L/'evidence/alpha-native-grasp-source-r1'
E.mkdir(exist_ok=False)
def load(p): return json.loads(Path(p).read_bytes())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8') as f: json.dump(v,f,indent=2)
d=load(B/'alpha-native-grasp-candidate-r1b/NATIVE_GRASP_CANDIDATE_PRIVATE_R1B.json')
lib=load(B/'alpha-native-grasp-preview-r1/ACTION_ONLY_CUSTODY_R1.json')
c=load(B/'alpha-native-grasp-library-contact-qa-r1/NATIVE_GRASP_BOTH_ARM_SURFACE_PRIVATE_R1.json')
r=load(B/'alpha-native-grasp-preview-r1/NATIVE_GRASP_RENDER_RECEIPT_R1.json')
p=load(D/'OFF_PIXEL_ORACLE_R1.json'); u=load(D/'WHOLE_1X_UI_QA_R1.json')
assert d['frame_range']==[1,169] and d['source_sole_world_error_m']==0 and d['lower_bone_world_error']==0
assert d['original78Actions_and_OFF_source_snapshot_exact'] and p['PASS']
assert all(x['ended'] and x['playbackRate']==1 and x['error'] is None for x in u['end'])
assert c['bounded_contact_subset']=='PASS'
assert all(x==0 for side in c['maximum_actual_surface_pairs_by_side'].values() for x in side.values())
assert all(x==0 for end in c['endpoint_source_geometry_component_error_m'].values() for x in end.values())
assert sha(d['source'])==d['source_SHA'] and sha(d['candidate'])==d['candidate_SHA'] and sha(lib['file'])==lib['SHA']
visual='REFERENCE ONLY. Fixed front/waist entire169-frame1x gesture visibly raises LEFT forearm, holds then releases to original neutral; no observed gross new mesh break. Original long central hold/static face remain. Right-hand tracking close is a static control, not active LEFT finger-detail QA. No LEFT high-resolution close/prop contact/physical grasp/acting-quality approval.'
summary={k:v for k,v in d.items() if k!='frames_private'}
summary.update({'status':'SOURCE_ONLY_TECH_SCOPED_SURFACE_PASS_VISUAL_REFERENCE','action_only':lib,'actual_surface':{k:v for k,v in c.items() if k!='frames_private'},'OFF_RGBA':p,'normal_speed_UI':u,'cameras':r['views'],'visual_verdict':visual,'source_appearance_promoted':False,'source66_rebuilt':False,'TierP':0,'Unity_AlwaysAnimate_physics':'HOLD','construction_failure_control':'R1 reused121-frame Talk template although original Grasp is169. Partial R1 candidate and executed script preserved; not a valid full-motion delivery. Fresh R1b repairs only full source range/head-hair transport and QA to169; source294curves remain exact. Guard terminal success alone never treated as content PASS.','task_alias':'Candidate metadata ROOT_PM_NATIVE_GRASP_SOURCE_REVIEW_NEXT_EXISTING_WAVE_R1 is a narrow reused template label; authority remains ROOT_PM_NATIVE_TALK_SOURCE_REVIEW_NEXT_EXISTING_WAVE_R1, original Wave already supplied.','already_supplied_wave':{'checkpoint':'a59499f','packet_SHA':'f1621cc214e09d3c8ddcd020b4e167d8ca739c31687c80f7ab11654e73c883fd','bytes':56086747,'this_run_archive_SHA_CRC':'PASS; not regenerated'},'already_supplied_look_listen':{'checkpoint':'82949b0','packet_SHA':'76a006e56289738d79ea0ef6b6e9b3ec4c29a5412e10c4560881ebf871df1275','provenance':'Prior A3-derived source candidate; not newly claimed as original native HeadGazeHair'},'next_bounded_task':'If this LEFT hand component is selected for reuse, add fixed LEFT active-hand close over existing169frames; retain motion untouched and independently judge curl readability/weak-webbing defects. Source-only review, no automatic Unity or TierP promotion.'})
write(E/'NATIVE_GRASP_SOURCE_MANIFEST_R1.json',summary); write(E/'ACTION_ONLY_CUSTODY_R1.json',lib)
guards=[]
for run in ['o1-native-grasp-intake-r1','o1-native-grasp-candidate-r1','o1-native-grasp-candidate-r1b','o1-native-grasp-preview-r1b','o1-native-grasp-library-contact-qa-r1']:
    f=B/run/'NATIVE_GUARD_RESULT.json'; g=load(f); assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN'
    guards.append({'run':run,'SHA':sha(f),'guard_status':g['guard_status'],'wall_seconds':g['wall_seconds']})
write(E/'NATIVE_CUSTODY_R1.json',guards)
(E/'YURI_R4_NATIVE_GRASP_SOURCE_R1.md').write_text('''# Original native GraspHoldRelease source component

Source-only technical/scoped-surface PASS; visual reference. R4 source SHA a30fc513 remains immutable. Existing78Actions including66 motions, geometry/weights/rest/hierarchy/ShapeKeys/material/nodes/textures and face/gaze drivers preserved. No donor, body substitution, merge, new GameRig, product/Unity implementation or additional reaction production.

Existing MESHY_R2_BODY_GraspHoldRelease native quaternion source1–169 at24fps is reused. Separate COPY retains294 exact location/quaternion curves for12 upper+30 finger bones. Lower tracks removed from COPY only. Original Action SHA2100d633 unchanged. Two additional existing-rig head/hair Root transport Actions preserve source face/gaze neutral. Pure three-Action library has0objects/meshes/armatures; fixed adapter restores source bindings/raw pose/frame.

All169 source sole vertices, lower-bone world matrices and carrier are unchanged. Body component motion279.917mm, maximum adjacent vertex step39.487mm; actual intentional finger-local matrix motion0.71455. Fresh original source + ONLY three Actions + fixed adapter tested all169 actual L/R dominant-weight arm/hand/digit surfaces versus outside limb body/head/hair and interdigit pairs: maximum pairs0. Endpoints1/169 body/head/hair source geometry error0. Full source OFF snapshot and original78Actions exact, saved/reopened source-camera960×920 RGBA changed pixels0. Scoped triangle tests exclude weak webbing/adjacency, penetration depth, full character collisions and physical grasp certification.

Three entire169-frame24fps7.041667sec movies encoded/full decoded and actually played1x through-end; all-frame waist and hand grids reviewed. Fixed front/waist show LEFT forearm raise/long hold/release without observed gross new mesh break. Right-hand tracking close is a static control and DOES NOT certify active LEFT finger-detail visual quality. Left active-hand close remains the one bounded review improvement. Original central hold/static neutral face and absent prop contact mean visual REFERENCE, not acting/product promotion.

Construction failure preserved: initial R1 kept121-frame Talk template while source Grasp has169. Partial candidate is a failure control, not complete animation. Fresh R1b changes source range/head-hair generation/QA to169; exact source curves and original model preserved. Original executed scripts/candidate/guard receipts untouched. All five native jobs passed unchanged strict identity barriers/terminal drain; guard success alone does not validate partial R1 content. Old Wave checkpoint a59499f/packet f1621cc2 and prior look/listen82949b0/packet76a006e5 already supplied and not rebuilt. Neutral-replant R1/R2 stay FAIL/HOLD, no third solver.

Public Git stores workflow/scalar QA/SHA pointers only. Source/candidate/pure Action file/adapter/videos/private frame data/cameras/native custody are bundled privately with full member SHA/size/CRC validation. Unity state/time/weight/AlwaysAnimate, face/gaze acting, physical grasp and TierP remain HOLD/TierP0. Root supplied completed NativeTalk receiver custody separately; no duplicate ZIP transfer or export performed.
''',encoding='utf-8')
files={}
def add(p,n):
    p=Path(p); assert p.is_file() and n not in files; files[n]=p
add(d['source'],'source/'+Path(d['source']).name); add(d['candidate'],'candidate-OFF/'+Path(d['candidate']).name); add(lib['file'],'animation-only/'+Path(lib['file']).name)
for folder in ['alpha-native-grasp-intake-r1','alpha-native-grasp-candidate-r1','alpha-native-grasp-candidate-r1b','alpha-native-grasp-library-contact-qa-r1']:
    for f in (B/folder).rglob('*'):
        if f.is_file() and f.suffix not in ['.blend','.blend1']: add(f,'private-evidence/'+folder+'/'+f.relative_to(B/folder).as_posix())
for f in D.iterdir():
    if f.is_file(): add(f,'review/'+f.name)
for n in ['ACTION_ONLY_CUSTODY_R1.json','NATIVE_GRASP_RENDER_RECEIPT_R1.json','CANDIDATE_OFF_SOURCE_NEUTRAL_R1.png']: add(B/'alpha-native-grasp-preview-r1'/n,'reopen-camera/'+n)
for f in E.iterdir(): add(f,'metadata/'+f.name)
for g in guards:
    for f in (B/g['run']).rglob('*'):
        if f.is_file(): add(f,'native-custody/'+g['run']+'/'+f.relative_to(B/g['run']).as_posix())
for f in (L/'scripts').glob('r4_native_grasp*.py'): add(f,'workflow/'+f.name)
for n in ['r4_native_talk_right_surface_oracle_r1.py','r4_c1_contact_surface_oracle_r3.py','r4_appearance_signature.py','r4_appearance_adapter.py']: add(L/'scripts'/n,'workflow/'+n)
for n in ['r4_two_input_owned_barrier_broker_r1.py','r4_two_input_live_barrier_wrapper_r1.py']: add(B/'o1-morph67-native-broker-preparation-r4/workflow'/n,'native-workflow/'+n)
idx={n:{'bytes':f.stat().st_size,'SHA':sha(f)} for n,f in sorted(files.items())}; ip=D/'MEMBER_SHA256_INDEX_R1.json'; write(ip,idx); add(ip,ip.name)
zp=B/'YURI_R4_NATIVE_GRASP_SOURCE_ONLY_R1_20261005.zip'
with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n,f in sorted(files.items()): z.write(f,n)
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None
    for n,v in idx.items(): raw=z.read(n); assert len(raw)==v['bytes'] and hashlib.sha256(raw).hexdigest()==v['SHA']
    receipt={'file':str(zp),'bytes':zp.stat().st_size,'SHA':sha(zp),'members':len(z.namelist()),'indexed_members':len(idx),'CRC_SHA_size_all':'PASS','source_SHA':d['source_SHA'],'candidate_SHA':d['candidate_SHA'],'library_SHA':lib['SHA'],'source_technical_and_scoped_surface':'PASS','visual':visual,'TierP':0}
    write(E/'PRIVATE_PACKET_RECEIPT_R1.json',receipt); write(D/'PRIVATE_PACKET_RECEIPT_R1.json',receipt); print(json.dumps(receipt,indent=2))
