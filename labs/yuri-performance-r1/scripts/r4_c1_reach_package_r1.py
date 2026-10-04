"""Seal existing staged C1 source-only candidate; no hold/prop/runtime promotion."""
from pathlib import Path
import json,hashlib,zipfile
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');LAB=Path(__file__).resolve().parents[1];D=BASE/'alpha-c1-reach-delivery-r1';E=LAB/'evidence/alpha-c1-reach-source-candidate-r1';E.mkdir(exist_ok=False)
def load(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
 with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
c=load(BASE/'alpha-c1-reach-candidate-r1/C1_REACH_CANDIDATE_PRIVATE_R1.json');off=load(BASE/'alpha-c1-reach-off-qa-r1/OFF_REOPEN_ORACLE_R3.json');pixel=load(BASE/'alpha-c1-reach-off-qa-r1/OFF_RGBA_ARRAY_EQUAL_R1.json');motion=load(D/'C1_SOURCE_BODY_MOTION_QA_R1.json');assert sha(c['candidate'])==c['candidate_SHA'] and sha(c['source'])==c['source_SHA'] and pixel['all_channels_exact']
ui={'url':'http://127.0.0.1:8786/REVIEW_C1_REACH_RETURN_R1.html','views':['front','quarter','side'],'start_times_sec':[.187923,.187880,.187842],'end_times_sec':[2.033333]*3,'rates':[1]*3,'ended':[True]*3,'errors':[None]*3,'whole61_native_frames_3movies_decode':'PASS','source_candidate_status':'SOURCE_ONLY_PROVISIONAL; low-sample visual proof, no exhaustive skin self-intersection/hand/prop/contact/final facial fidelity acceptance','dedicated_hold':False,'prop_grip_contact':False,'TierP':0};write(D/'WHOLE_1X_C1_QA_R1.json',ui);write(E/'WHOLE_1X_C1_QA_R1.json',ui)
summary={k:v for k,v in c.items() if k!='frames_private'};summary.update({'OFF_geometry_material_slots_nodes_ShapeKeys_weights_rest_hierarchy_drivers_original78Actions_exact':off['all_nontexture_geometry_material_nodes_weights_keys_rest_drivers_bindings_scene_exact'],'OFF_full_RGBA_difference':0,'packed_texture_bytes_colorspace_resolved_properties_exact':off['packed_texture_bytes_colorspace_resolved_properties_exact'],'SaveAs_texture_locator_string_remap_disclosed':True,'reference_plan':'Existing first12 C1 591e303f2c630f618aea; source-only fallback explicitly delegated by Root PM after single contact alternative failure, not O2 runtime release.','original44_TierC':44,'TierP':0,'first4_and6Reaction_and_walk_controls_unchanged':True,'source_visual_promotion':False,'StageB_O1_PRIMARY_Unity_F2_F3':'HOLD'});write(E/'C1_SOURCE_MANIFEST_R1.json',summary);write(E/'C1_SOURCE_BODY_MOTION_QA_R1.json',motion);write(E/'OFF_RGBA_ARRAY_EQUAL_R1.json',pixel);write(E/'ACTION_ONLY_CUSTODY_R1.json',load(BASE/'alpha-c1-reach-off-qa-r1/ACTION_ONLY_CUSTODY_R1.json'))
rows=[]
for name in ['alpha-c1-reach-inspect-broker-r1','alpha-c1-reach-candidate-broker-r1','alpha-c1-reach-off-broker-r1','alpha-c1-reach-probe-broker-r1','alpha-c1-reach-full-preview-broker-r1']:
 p=BASE/name/'NATIVE_GUARD_RESULT.json';v=load(p);assert v['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN';rows.append({'run':name,'receipt':str(p),'sha256':sha(p),'status':v['guard_status'],'wall_seconds':v['wall_seconds']})
write(E/'NATIVE_CUSTODY_R1.json',rows)
report='''# C1 Interact reach → return: immutable original-R4 source candidate

C1 uses the existing first-batch44 TierC selection591e303f2c630f618aea, staged CC0 Quaternius UAL1 Standard Interact. No new donor/model/corpus scan/download/exporter/Unity implementation. Root PM source-only coverage fallback authorization overrides only the old wait status for this private source experiment; it is not O2 runtime release. Existing44C/0P and StageB/O1/PRIMARY/F2/F3/Unity HOLD. First4/6 Reaction/all walk stop success/failure controls remain unchanged.

## Actual source proof

Candidate26,676,877bytes SHA bad645ae396ebef88564e4b3656f5e73c9375a9b87ee217acbd87a1354964946. Original R4a30fc513 preserved. Original geometry, material slots/nodes/texture bytes/colorspace, ShapeKeys, weights, hierarchy/rest/drivers and78 Actions exact OFF. Full neutral RGBA difference0 against existing authority witness; source baseline was not rerendered. SaveAs texture locator strings are remapped but resolved properties/packed bytes exact.

61 native samples at30fps; key interval2.0s/container2.033333s; original saved source scene24fps. Fixed front/quarter/side full61-frame render, whole decode and actual UI1x ended/errornull. Low-cost512×384 CPU2sample/JPEG92 evidence only; no exhaustive self-intersection/finger/neck/final facial fidelity approval.

All61 evaluated body vertices finite; actual root range0 from source in-place root, no horizontal lock correction. Native left hand rangeX85.711mm/Y251.843mm/Z197.129mm; right hand quiet~13mm. Forward peak frame23 (0.733333s);95% kinematic peak frames20..30. This measured plateau is not a dedicated authored hold or prop-contact contract. End/start hand difference0; loop not declared or approved. Max any native joint frame step38.547mm. Per-frame pelvis sole-support-Z correction20.490..21.511mm; no physical slipping/contact certification.

## Original appearance plus Actions

Rest-aware21-bone mapping reuses native lengths/hip-height normalization and UAL180° yaw rotation (not reflection). Native fingers remain original. Four editable BODY/root carrier/body-head transport/hair transport Actions form ONE reach-return motion. Original face/gaze drivers/material/keys remain intact; no expressive face or secondary-hair channels newly authored. Action-only BLEND contains0 objects/meshes/armatures.

Bind all four mapping pairs with the existing ReactionLane adapter plus saved/restored Assembly_Root binding/transform. Evaluate1..61 at30fps; canonical saved source24fps stays untouched. Animation OFF restores original frame, pose/Action slots and carrier. Product runtime adapter/prop fixture/grip/hold alignment and AlwaysAnimate/state/time/weight checks belong to the consumer, not this Blender source proof.

The private bundle contains canonical source, editable OFF candidate, four-Action library, already licensed donor, source/clock/root/camera metadata, full native numeric QA, closed guard evidence, workflow and normal-speed movies. No private character geometry/full numeric motion is in public Git. Scripts use desktop paths; relocated replay needs scoped remapping and a new exact guard packet.

Next safe-boundary task is the delegated single actual STARTLED mouth source visual reference. The failed stop alternative4191 is retained as causal evidence and must not replace MIXED57d9 or original35c5.
'''
with (E/'YURI_R4_C1_REACH_SOURCE_CANDIDATE_R1.md').open('x',encoding='utf8') as f:f.write(report)
files={}
def add(p,n):
 p=Path(p);assert p.is_file() and n not in files;files[n]=p
add(c['candidate'],'candidate/'+Path(c['candidate']).name);add(c['source'],'source/'+Path(c['source']).name);add(c['donor']['file'],'licensed-donor/'+Path(c['donor']['file']).name)
for folder in ['alpha-c1-reach-inspect-r1','alpha-c1-reach-candidate-r1','alpha-c1-reach-off-qa-r1']:
 for p in (BASE/folder).rglob('*'):
  if p.is_file() and p.suffix not in ['.blend','.blend1']:add(p,'private-evidence/'+folder+'/'+p.relative_to(BASE/folder).as_posix())
for p in (BASE/'alpha-c1-reach-off-qa-r1').glob('*.blend'):add(p,'animation-only/'+p.name)
for p in E.iterdir():add(p,'metadata/'+p.name)
for p in D.iterdir():
 if p.is_file():add(p,'review/'+p.name)
for name in [r['run'] for r in rows]:
 for p in (BASE/name).rglob('*'):
  if p.is_file():add(p,'native-custody/'+name+'/'+p.relative_to(BASE/name).as_posix())
for p in LAB.joinpath('scripts').glob('r4_c1_reach*.py'):add(p,'workflow/'+p.name)
for name in ['r4_appearance_adapter.py','r4_appearance_signature.py','native_preservation.py']:add(LAB/'scripts'/name,'workflow/'+name)
for view in ['front','quarter','side']:add(BASE/'alpha-c1-reach-preview-r1'/view/'RENDER_RECEIPT_R4.json','camera/'+view+'_RENDER_RECEIPT_R4.json')
lic=Path(r'C:/Users/JAEWAN/.codex/worktrees/common-motion-curation-r1/yuri-room-mvp/common-motion-r1/licenses/Quaternius-LICENSE.txt');add(lic,'licenses/'+lic.name)
index={n:{'bytes':p.stat().st_size,'sha256':sha(p)} for n,p in sorted(files.items())};idx=D/'MEMBER_SHA256_INDEX_R1.json';write(idx,index);add(idx,idx.name)
zp=BASE/'YURI_R4_C1_REACH_SOURCE_ONLY_R1_20261004.zip'
with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):z.write(p,n)
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 for n,v in index.items():
  data=z.read(n);assert len(data)==v['bytes'] and hashlib.sha256(data).hexdigest()==v['sha256']
 assert len(z.namelist())==len(files)
receipt={'file':str(zp),'bytes':zp.stat().st_size,'sha256':sha(zp),'members':len(files),'indexed_members':len(index),'CRC_all_members':'PASS','all_indexed_member_bytes_SHA':'PASS','candidate_bytes':c['candidate_bytes'],'candidate_sha256':c['candidate_SHA'],'source_sha256':c['source_SHA'],'index_sha256':sha(idx),'TierP':0,'source_only':True,'dedicated_hold_prop_grip_physics_Runtime_final_visual_promoted':False};write(E/'PRIVATE_PACKET_RECEIPT_R1.json',receipt);write(D/'PRIVATE_PACKET_RECEIPT_R1.json',receipt);assert sha(c['source'])==c['source_SHA'];print(json.dumps(receipt,indent=2))
