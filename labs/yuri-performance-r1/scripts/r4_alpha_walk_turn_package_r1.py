"""Seal private packet with byte/SHA custody; no character mutation."""
from pathlib import Path
import json,hashlib,zipfile,math
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');LAB=Path(__file__).resolve().parents[1]
E=LAB/'evidence/alpha-walk-turn-stop-source-candidate-r1';E.mkdir(exist_ok=False)
D=BASE/'alpha-walk-turn-delivery-r1'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def write(p,v):
 with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2,ensure_ascii=False)
def norm(v):return math.sqrt(sum(x*x for x in v))
def minus(a,b):return [x-y for x,y in zip(a,b)]
c=load(BASE/'alpha-walk-turn-candidate-r3/WALK_TURN_STOP_CANDIDATE_PRIVATE_R3.json');frames=c['frames_private'];source=Path(c['source']);candidate=Path(c['candidate']);assert sha(source)==c['source_SHA'] and sha(candidate)==c['candidate_SHA']
rootstep=max(norm(minus(a['root_carrier_world'],b['root_carrier_world'])) for a,b in zip(frames[1:],frames))
relative={}
for joint in frames[0]['joints']:
 coords=[minus(f['joints'][joint],f['root_carrier_world']) for f in frames]
 relative[joint]={'relative_to_world_carrier_axis_range_m':[max(v[i] for v in coords)-min(v[i] for v in coords) for i in range(3)]}
bridge={}
for name,(a,b) in c['segments'].items():
 if name not in ['walk_to_attention_proxy_deceleration','stop_to_idle_placeholder']:continue
 rows=frames[a-2:b]
 bridge[name]={side:{'max_cohort_centroid_XY_speed_m_s':max(norm(minus(x['soles'][side]['centroid'][:2],y['soles'][side]['centroid'][:2]))*30 for x,y in zip(rows[1:],rows)),'XY_range_m':[max(x['soles'][side]['centroid'][i] for x in rows)-min(x['soles'][side]['centroid'][i] for x in rows) for i in [0,1]]} for side in ['L','R']}
metrics={'candidate_sha256':c['candidate_SHA'],'all_293_native_frames_geometry_finite':True,'max_world_root_frame_step_m':rootstep,'root_world_range_m':c['root_world_range_m'],'root_end_displacement_m':c['root_end_displacement_m'],'root_path_length_m':c['root_path_length_m'],'floor_support_Z_correction_range_m':c['floor_support_Z_correction_range_m'],'actual_bone_motion_relative_to_world_carrier':relative,'bridge_sole_cohort_kinematics':bridge,'bridge_contact_semantics':'UNKNOWN; no authored stance labels. XY centroid movement alone does not establish physical slip. No horizontal root locking.','face_hair_socket_gap_m':[min(f['face_socket_body_head_distance_m'] for f in frames),max(f['face_socket_body_head_distance_m'] for f in frames)],'physics_contact_slip_certified':False}
write(E/'SOURCE_KINEMATIC_QA_R1.json',metrics)
off=load(BASE/'alpha-walk-turn-off-qa-r3/OFF_REOPEN_ORACLE_R3.json');pixel=load(BASE/'alpha-walk-turn-off-qa-r3/OFF_RGBA_ARRAY_EQUAL_R3.json')
write(E/'APPEARANCE_OFF_ACCEPTANCE_R1.json',{'immutable_source_sha256':c['source_SHA'],'candidate_sha256':c['candidate_SHA'],'geometry_material_slots_nodes_ShapeKeys_weights_rest_drivers_original_78_Actions_exact':off['all_nontexture_geometry_material_nodes_weights_keys_rest_drivers_bindings_scene_exact'],'packed_texture_bytes_colorspace_resolved_properties_exact':off['packed_texture_bytes_colorspace_resolved_properties_exact'],'raw_texture_locator_strings_remapped_by_Blender_SaveAs':True,'neutral_pixels':pixel,'rig_hierarchy_changes':False,'donor_geometry_appended':False,'canonical_visual_promotion':False,'six_Reaction_reuse':'Existing corrective 820a237 preserved; six native normal-speed PASS and two-cycle loops, not rerendered/rebuilt for this walk supplement. Unity gate pending.'})
actions=load(BASE/'alpha-walk-turn-actions-only-r1/ACTION_ONLY_CUSTODY_R1.json');write(E/'ACTION_ONLY_CUSTODY_R1.json',actions)
clock={k:c[k] for k in ['source_fps','source_scene_fps','turn_original_BVH_fps','frames','key_interval_sec','movie_duration_sec','segments','additive_body_actions']}
clock.update({'walk':'CC0 UAL1 RM actual Walk_Loop1..41,40-key period,two cycles1..81; unwrapped world root; hip height ratio .5485982342668642;180deg yaw rotation, not mirror.','turn':'MIT StayStill lb_lef_2_08 Action~2..148; attention-turn proxy, not dedicated locomotion turn. Hip height ratio .548901349870254.','stop':'Procedural Hermite deceleration/settle + existing CC0 Idle_Loop start; dedicated stop missing.','clock_policy':'Saved OFF original scene24fps; Actions source_fps=30. Native293 samples encoded30fps. Do not play keys at24 without time conversion.','root':'Existing Assembly_Root carries actual world path; bind all four Actions together. Local body root constant is not world-root lock.','transport':'Armature.Root and Hair_HeadRoot rigid body/head transport only; original face/gaze drivers remain unchanged.'});write(E/'ROOT_CLOCK_REUSE_MAPPING_R1.json',clock)
donors=[{'file':r'C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/UnityQA/Assets/Motions/Native/5a5f5de6f18e9c91.fbx','license':'CC0 Quaternius','expected_sha256':'5a5f5de6f18e9c91cdbc40eb26319ec85cc45070bc00965bc2737beb4b2984ea'},{'file':r'C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/UnityQA/Assets/Motions/BVH/bc5e6bd9a98755f6.fbx','license':'MIT StayStill','expected_sha256':'417f3257f323815c13dc89ca5bfe4349ef58f762a990b093bbc5acf2eaed45da'}]
for donor in donors:
 donor['actual_sha256']=sha(donor['file']);donor['bytes']=Path(donor['file']).stat().st_size;assert donor['actual_sha256']==donor['expected_sha256']
write(E/'SOURCE_AND_DONOR_CUSTODY_R1.json',{'source':str(source),'source_bytes':source.stat().st_size,'source_sha256':sha(source),'candidate':str(candidate),'candidate_bytes':candidate.stat().st_size,'candidate_sha256':sha(candidate),'donors':donors,'TierC_count':44,'TierP_count':0,'first4_checkpoint_preserved':'f5211f1','historical_experiment_preserved':'08caad7','six_Reaction_rebuilt':False,'Laptop_Unity_product_change':False,'GPU_paid_provider_download':False})
write(E/'FAILURE_AND_CORRECTION_LEDGER_R1.json',[{'run':'candidate-r1','result':'FAIL','cause':'Empty layered Action slot caused existing ReactionLane StopIteration. No candidate saved.','fix':'Explicit OBJECT slot in additive Actions only.'},{'run':'candidate-r2','result':'FAIL','cause':'Version rename changed pinned inspection input to absent R2 filename; FileNotFound before source load.','fix':'R3 reads actual pinned R1 inspection.'},{'run':'probe-r3','result':'SIZING_ONLY, not final output-containment acceptance','cause':'Small three-view images outside shared capture_root; PNG full293 forecast exceeds64MiB.','fix':'No fullR3PNG render. R4 same512x384 JPEG92 nested scoped capture root, all final three guards PASS.'},{'run':'package-script-preparation','result':'FAIL before file creation','cause':'Nested triple-quote source generator syntax error.','fix':'Write literal UTF8 script without nested quoting; no character mutation.'}])
ui={'url':'http://127.0.0.1:8783/REVIEW_WALK_TURN_STOP_R1.html','observed_by':'cua UI button + readonly HTMLMediaElement state','start_times_sec':[.226258,.226174,.225991],'views':['front','quarter','side'],'end_times_sec':[9.766667]*3,'duration_sec':[9.766667]*3,'playbackRate':[1]*3,'ended':[True]*3,'error':[None]*3,'all293_native_frames_rendered_per_view':True,'whole_interval_decode':'PASS all3','visual_limit':'Low-sample preview; no exhaustive neck seam, hand, self-intersection/F2/F3 certification.'};write(D/'WHOLE_1X_PLAYBACK_QA_R1.json',ui);write(E/'WHOLE_1X_PLAYBACK_QA_R1.json',ui)
guards=[]
for name in ['inspect-broker-r1','candidate-broker-r3','off-qa-broker-r3','actions-only-broker-r1','probe-broker-r4','front-preview-broker-r4','quarter-preview-broker-r4','side-preview-broker-r4']:
 p=BASE/f'alpha-walk-turn-{name}'/'NATIVE_GUARD_RESULT.json';g=load(p);guards.append({'run':name,'result_sha256':sha(p),'receipt':str(p),'status':g.get('guard_status',g.get('status'))})
write(E/'NATIVE_GUARD_RECEIPTS_R1.json',guards)
report='''# Original R4 appearance preserved: one walk → attention-turn proxy → stop source candidate

R4(a30fc513…) is the immutable visual authority. No character promotion, new GameRig, mesh merge, body substitution or donor geometry. Existing08caad7, corrective820a237, first4f5211f1, R2/R3d and six Reaction assets remain unchanged. Existing44 TierC/0 TierP. This is ONE source-only sequence, not four finished performances.

## Actual preservation and playback

Original geometry, material slots/nodes, ShapeKeys, weights, rest pose, hierarchy, gaze/face drivers and78 Actions: exact OFF. Packed texture bytes/colorspace/resolved properties: exact. Six texture locator strings remapped by Blender SaveAs are disclosed separately. Saved OFF neutral RGBA full-array difference0 against existing authority witness.

Candidate27,040,460bytes, SHA35c5a9d00bdef2ca2b82e35645bf9da87e6f050ae6ead0ce0a9f9bd859bbf026, default animation OFF. All293 native frames finite body geometry. Actual root endpoint displacement1.562923m/path1.688190m. Full293-frame front/quarter/side rendered, all three movies fully decoded and UI played1x through ended=true/error=null.

Actions30fps, original source scene24fps preserved. Native key interval9.733333s; movie container9.766667s. Fixed50mm cameras do not follow root. Native bones retained; rest-aware21-bone retarget + hip-height normalized world path, limb direction/native lengths. Native finger channels retained. CC0 donor180° yaw is rotation, not mirror.

Four editable BODY/Assembly_Root world path/Armature.Root rigid head transport/Hair_HeadRoot rigid transport Actions comprise this one sequence. No expressive face/gaze/secondary-hair channels modified. Action-only BLEND contains0 objects/meshes/armatures. Head/hair transport is necessary because original source has separate body/head/hair parent paths; hierarchy is unchanged.

## Explicit defects and limits

Walk uses existing staged CC0 UAL RM Walk_Loop for2cycles. Turn uses existing MIT StayStill attention-turn proxy, not dedicated locomotion turn. Stop is Hermite/pose blend + existing Idle_Loop placeholder, not authored stop. Neither missing input is counted complete.

Frame-corresponded source toe-marker height/speed stance proxy shows target walk sole-cohort Y drift up to12.85mm and proxy stance sole height up to~14mm. This is not authored stance labels or physical foot-slip certification. Procedural bridges have no source contact labels: UNKNOWN. Horizontal root is not locked. Pelvis support-Z correction−4.996..+38.662mm; world rootZ=0.

Head/hair socket gap~2.978mm stays stable; this does not prove deformed neck-seam fidelity. 512×384 CPU2sample JPEG92 preview is low-cost source QA. No obvious gross detachment in inspected views is not an exhaustive self-intersection/hand/final visual fidelity certification. F2/F3, Unity, StageB/O1/PRIMARY remain HOLD. Unity AlwaysAnimate/state entered/normalized time/weight gates remain consumer-owned.

## Source / Action / adapter separation

Open a copy of canonical source and verify SHA. Append only4 Actions from animation-only library. Bind all four object→Action pairs in ROOT_CLOCK_REUSE_MAPPING_R1.json together. Use existing ReactionLane to save/restore three rigs; additionally save/restore Assembly_Root Action slot, binding and transform. Evaluate native1..293 at30fps clock; original saved scene24fps remains authority. On OFF restore original frame, pose, bindings/slots and carrier. Do not change weights/material/keys/drivers/hierarchy.

Runtime adapter/Unity import are separate consumer tasks. Existing six Reaction sealed corrective bundle is reused without rebuild. The private packet includes original R4, editable OFF candidate, Action-only library, staged licensed inputs, license notices, scripts, root/clock/camera metadata, full1x movies and closed native/failure receipts; no private character or numeric motion enters public Git.

## Next bounded experiments

Acquire frame-corresponded support-contact labels for82..97 and244..263, then inspect support-foot IK/XY residual while preserving donor beat/root trajectory. Replace proxy/placeholder only when dedicated turn/stop input exists. Separate higher-resolution neck seam and hand/finger fidelity review remains required. Canonical appearance and first4 stay immutable.
'''
with (E/'YURI_R4_WALK_TURN_STOP_SOURCE_CANDIDATE_R1.md').open('x',encoding='utf8') as f:f.write(report)
files={}
def add(p,member):
 p=Path(p);assert p.is_file() and member not in files;files[member]=p
add(candidate,'candidate/'+candidate.name);add(source,'source/'+source.name)
for donor in donors:add(donor['file'],'licensed-donors/'+Path(donor['file']).name)
for p in (BASE/'alpha-walk-turn-actions-only-r1').iterdir():
 if p.is_file():add(p,'animation-only/'+p.name)
for p in D.iterdir():
 if p.is_file():add(p,'review/'+p.name)
for p in E.iterdir():add(p,'metadata/'+p.name)
for folder in ['alpha-walk-turn-inspect-r1','alpha-walk-turn-candidate-r1','alpha-walk-turn-candidate-r2','alpha-walk-turn-candidate-r3','alpha-walk-turn-off-qa-r3']:
 if (BASE/folder).exists():
  for p in (BASE/folder).rglob('*'):
   if p.is_file() and p.suffix not in ['.blend','.blend1']:add(p,'private-qa/'+folder+'/'+p.relative_to(BASE/folder).as_posix())
for p in LAB.joinpath('scripts').glob('r4_alpha_walk_turn*.py'):add(p,'workflow/'+p.name)
for name in ['r4_appearance_adapter.py','r4_appearance_signature.py','native_preservation.py']:
 p=LAB/'scripts'/name
 if p.exists():add(p,'workflow/'+name)
for script in LAB.joinpath('scripts').glob('r4_alpha_walk_turn*.py'):
 for line in script.read_text(encoding='utf8').splitlines():
  if line.startswith('from r4_'):
   name=line.split()[1]+'.py';p=LAB/'scripts'/name
   if p.exists() and 'workflow/'+name not in files:add(p,'workflow/'+name)
for folder in BASE.glob('alpha-walk-turn-*-broker-r*'):
 for p in folder.rglob('*'):
  if p.is_file():add(p,'native-custody/'+folder.name+'/'+p.relative_to(folder).as_posix())
for view in ['front','quarter','side']:add(BASE/f'alpha-walk-turn-preview-{view}-r4/RENDER_RECEIPT_R4.json','camera/'+view+'_RENDER_RECEIPT_R4.json')
add(BASE/'WALK_TURN_PREVIEW_CAPACITY_AND_CAPTURE_ROUTE_R4.json','private-qa/WALK_TURN_PREVIEW_CAPACITY_AND_CAPTURE_ROUTE_R4.json')
licenses=Path(r'C:/Users/JAEWAN/.codex/worktrees/common-motion-curation-r1/yuri-room-mvp/common-motion-r1/licenses')
for name in ['Quaternius-LICENSE.txt','StayStill-LICENSE.txt']:add(licenses/name,'licenses/'+name)
index={name:{'bytes':p.stat().st_size,'sha256':sha(p)} for name,p in sorted(files.items())};idx=D/'MEMBER_SHA256_INDEX_R1.json';write(idx,index);add(idx,idx.name)
zip_path=BASE/'YURI_R4_WALK_TURN_STOP_SOURCE_ONLY_R1_20261004.zip'
with zipfile.ZipFile(zip_path,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for name,p in sorted(files.items()):z.write(p,name)
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None
 for name,v in index.items():
  b=z.read(name);assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256']
 assert len(z.namelist())==len(files)
receipt={'bundle':str(zip_path),'bytes':zip_path.stat().st_size,'sha256':sha(zip_path),'members':len(files),'CRC_all_members':'PASS','SHA_bytes_all_indexed_members':'PASS','index_sha256':sha(idx),'contains_original_R4_source':True,'contains_licensed_donors':True,'public_Git_private_binary_motion':False,'candidate_sha256':sha(candidate),'action_only_sha256':actions['sha256'],'stage_visual_Unity_promotion':False};write(E/'PRIVATE_PACKET_RECEIPT_R1.json',receipt);write(D/'PRIVATE_PACKET_RECEIPT_R1.json',receipt)
assert sha(source)==c['source_SHA'] and sha(candidate)==c['candidate_SHA']
print(json.dumps(receipt,indent=2))
