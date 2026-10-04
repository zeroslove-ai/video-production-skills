"""Independent existing-source TalkGesture supply, private binary assets and scalar public QA."""
from pathlib import Path
import json,hashlib,zipfile
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');L=Path(__file__).resolve().parents[1];D=B/'alpha-native-talk-delivery-r1';E=L/'evidence/alpha-native-talk-source-r1';E.mkdir(exist_ok=False)
def load(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
 with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
d=load(B/'alpha-native-talk-candidate-r1/NATIVE_TALK_CANDIDATE_PRIVATE_R1.json');intake=load(B/'alpha-native-talk-intake-r1/TALK_SOURCE_ACTION_INTAKE_PRIVATE_R1.json');lib=load(B/'alpha-native-talk-preview-r1/ACTION_ONLY_CUSTODY_R1.json');contact=load(B/'alpha-native-talk-library-contact-qa-r1/NATIVE_TALK_BOTH_ARM_SURFACE_PRIVATE_R1.json');render=load(B/'alpha-native-talk-preview-r1/NATIVE_TALK_RENDER_RECEIPT_R1.json');pixel=load(D/'OFF_PIXEL_ORACLE_R1.json');ui=load(D/'WHOLE_1X_UI_QA_R1.json');assert pixel['PASS'];assert all(x['ended'] and x['playbackRate']==1 and x['error'] is None for x in ui['end']);assert contact['bounded_contact_subset']=='PASS';assert all(x==0 for side in contact['maximum_actual_surface_pairs_by_side'].values() for x in side.values());assert sha(d['source'])==d['source_SHA'] and sha(d['candidate'])==d['candidate_SHA'];assert d['source_sole_world_error_m']==0 and d['lower_bone_world_error']==0 and d['local_finger_pose_error']==0;assert all(x==0 for end in contact['endpoint_source_geometry_component_error_m'].values() for x in end.values());summary={k:v for k,v in d.items() if k!='frames_private'};summary.update({'status':'SOURCE_ONLY_NATIVE_TALK_TECH_SCOPED_CONTACT_PASS_VISUAL_REFERENCE','Action_only_custody':lib,'actual_both_arm_surface_oracle':{k:v for k,v in contact.items() if k!='frames_private'},'OFF_reopen_source_camera_RGBA':pixel,'normal_speed_actual_UI':ui,'render_cameras':render['views'],'source_original_appearance_promoted':False,'original_66_Actions_rebuilt':False,'visual_verdict':'Two complete1x fixed views plus every-frame waist supplement: readable asymmetric open-hand talk gesture, no gross new pose pop/knee jump/mesh break observed. Original long middle pose/limited torso variation/static neutral face retained; not North-Star acting approval. No facial expression/gaze polish claimed.','provenance_correction':'Intake planning string mentioned Euler conversion, but actual inspected upper curves are already quaternion. No conversion, retarget solver, fresh acting recipe or unnecessary source66Action rebuild performed; only native upper84curves copied and lower curves excluded from COPY. Original78Actions preserved.','source_animation_supplied':'One independent body-only source component, reused original TalkGesture; no new reaction14 completion count','neutral_replant_R1_R2':'Closed FAIL/HOLD, research nonblocking; immutable checkpoints50e8ab7/d0ba548 and packets retained, no third solver experiment','Unity_AlwaysAnimate_physics_StageB_F2_F3_TierP':'HOLD, TierP0','next_bounded_task':'Independent product-owner source review of this TalkGesture component; if reused, original actual face/gaze timing is a separate layer and needs its own source QA, not automatic facial/raw mapping. Registered24-pair dance image reference matrix remains pending and nonblocking.'});write(E/'NATIVE_TALK_SOURCE_MANIFEST_R1.json',summary);write(E/'ACTION_ONLY_CUSTODY_R1.json',lib)
guards=[]
for run in ['o1-native-talk-intake-r1','o1-native-talk-candidate-r1','o1-native-talk-preview-r1','o1-native-talk-library-contact-qa-r1']:
 p=B/run/'NATIVE_GUARD_RESULT.json';g=load(p);assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN';guards.append({'run':run,'SHA':sha(p),'guard_status':g['guard_status'],'wall_seconds':g['wall_seconds']})
write(E/'NATIVE_CUSTODY_R1.json',guards)
(E/'YURI_R4_NATIVE_TALK_SOURCE_R1.md').write_text('''# Independent StageA/B source supply: original native TalkGesture upper body

Source-only technical/scoped-contact PASS; visual reference, no production promotion. Source R4 a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa remains immutable. Original78Actions including66 existing motions, geometry/weights/rest/hierarchy/keys/material/nodes/textures/face-gaze drivers preserved. No donor, GameRig, mesh merge, new reaction14, product or Unity write. Neutral-replant R1/R2 remain closed FAIL/HOLD and nonblocking; no third solver experiment.

Existing MESHY_R2_BODY_TalkGesture native source24fps/frames1–121 was inspected. Upper tracks already use quaternion, so no Euler conversion or sourceAction rebuild. COPY retains84 exact native location/quaternion curves for12 upper bones: spine/chest/neck/head, paired clavicle/upper_arm/forearm/hand. All other curves removed from COPY only; original source Action hash9f2e6524 unchanged. New face/hair Root Actions provide existing rigid body-head transport on original rigs; source expression/gaze/finger-local pose unchanged. Three-Action-only library has0objects0meshes0armatures; fixed adapter applies/restores original R4 bindings/raw poses. Source clock stays24fps, not unrelated prior30fps.

All121 actual evaluated body samples finite. Source sole vertices, lower-bone world matrices, finger-local matrices and world carrier error0. Actual body maximum component motion204.2296mm, maximum vertex step23.7035mm. Start/end original neutral body geometry0, and fresh ORIGINAL source plus ONLY three Actions/fixed adapter also measured body/head/hair source geometry0 at1 and121. No source/model pose copy or rig recreation.

Fresh-source actual per-frame dominant-weight L/R digits/hand/forearm/upper-arm cohorts against body outside corresponding weighted limb and actual head/hair, plus interdigit pairs, are0 throughout121frames. Actual evaluated Blender dynamic triangulation identities use original vertex-index triples; original polygons/vertex counts preserved. This is scoped surface PASS, not weak webbing/adjacency/full-body penetration depth/physics/grasp certification.

Saved candidate reopened, ON/OFF source snapshot exact; original source-camera960×920 RGBA changed pixels0. Complete121frames24fps5.041667seconds two fixed full-front/waist3/4 movies encoded, fully decoded, actually played1x through-end and supplemented with every-frame waist grid. Gesture is readable and asymmetric without observed gross new pop/knee jump/mesh break; original long central hold/limited torso variation and static neutral face remain. A body-only technical candidate is not North-Star/F2 acting quality. Facial/gaze timing, hair dynamics, Unity state/time/weight/AlwaysAnimate, physics and TierP/StageB/F2/F3 approval remain HOLD.

Four exact-scope native jobs passed unchanged600sec/4GiB/two-thread/one-process strict live identity barriers/terminal drain. CPU-only under unchanged product GPU lease, original GUI/product/laptop workers untouched. Pure library, source, saved-OFF candidate, fixed adapter, videos, camera metadata, private native/contact data, guard/workflow and full-memberSHA256 index are bundled privately. Public Git contains scripts/scalar QA/SHA pointers; original/private character geometry and motion/video bytes are not published.

Next is independent source-component review and, if appropriate, separately verified original face/gaze layer timing. Existing pending dance24-pair image-only analysis is not a blocker or motion accuracy certificate. No automatic product import or appearance promotion.
''',encoding='utf-8')
files={}
def add(p,n):p=Path(p);assert p.is_file() and n not in files;files[n]=p
add(d['source'],'source/'+Path(d['source']).name);add(d['candidate'],'candidate-OFF/'+Path(d['candidate']).name);add(lib['file'],'animation-only/'+Path(lib['file']).name)
for folder in ['alpha-native-talk-intake-r1','alpha-native-talk-candidate-r1','alpha-native-talk-library-contact-qa-r1']:
 for p in (B/folder).rglob('*'):
  if p.is_file() and p.suffix not in ['.blend','.blend1']:add(p,'private-evidence/'+folder+'/'+p.relative_to(B/folder).as_posix())
for p in D.iterdir():
 if p.is_file():add(p,'review/'+p.name)
for n in ['ACTION_ONLY_CUSTODY_R1.json','NATIVE_TALK_RENDER_RECEIPT_R1.json','CANDIDATE_OFF_SOURCE_NEUTRAL_R1.png']:add(B/'alpha-native-talk-preview-r1'/n,'reopen-camera/'+n)
for p in E.iterdir():add(p,'metadata/'+p.name)
for g in guards:
 for p in (B/g['run']).rglob('*'):
  if p.is_file():add(p,'native-custody/'+g['run']+'/'+p.relative_to(B/g['run']).as_posix())
for p in (L/'scripts').glob('r4_native_talk*.py'):add(p,'workflow/'+p.name)
for n in ['r4_c1_contact_surface_oracle_r3.py','r4_appearance_signature.py','r4_appearance_adapter.py']:add(L/'scripts'/n,'workflow/'+n)
for n in ['r4_two_input_owned_barrier_broker_r1.py','r4_two_input_live_barrier_wrapper_r1.py']:add(B/'o1-morph67-native-broker-preparation-r4/workflow'/n,'native-workflow/'+n)
idx={n:{'bytes':p.stat().st_size,'SHA':sha(p)} for n,p in sorted(files.items())};ip=D/'MEMBER_SHA256_INDEX_R1.json';write(ip,idx);add(ip,ip.name);zp=B/'YURI_R4_NATIVE_TALK_SOURCE_ONLY_R1_20261004.zip'
with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):z.write(p,n)
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 for n,v in idx.items():raw=z.read(n);assert len(raw)==v['bytes'] and hashlib.sha256(raw).hexdigest()==v['SHA']
 receipt={'file':str(zp),'bytes':zp.stat().st_size,'SHA':sha(zp),'members':len(z.namelist()),'indexed_members':len(idx),'CRC_SHA_size_all':'PASS','source_SHA':d['source_SHA'],'candidate_SHA':d['candidate_SHA'],'library_SHA':lib['SHA'],'source_technical_and_scoped_contact':'PASS','visual':'REFERENCE; body-only, no acting quality promotion','TierP':0};write(E/'PRIVATE_PACKET_RECEIPT_R1.json',receipt);write(D/'PRIVATE_PACKET_RECEIPT_R1.json',receipt);print(json.dumps(receipt,indent=2))
