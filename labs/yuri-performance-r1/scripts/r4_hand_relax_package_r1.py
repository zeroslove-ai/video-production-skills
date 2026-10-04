"""Private self-contained source-only right finger Action package; public scalar receipts."""
from pathlib import Path
import json,hashlib,zipfile
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');L=Path(__file__).resolve().parents[1];D=B/'alpha-hand-relax-delivery-r1';E=L/'evidence/alpha-hand-relax-source-candidate-r1'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
 with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
c=load(B/'alpha-hand-relax-candidate-r1/HAND_RELAX_CANDIDATE_PRIVATE_R1.json');off=load(B/'alpha-hand-relax-off-qa-r1/OFF_REOPEN_ORACLE_R3.json');pixel=load(B/'alpha-hand-relax-off-qa-r1/PIXEL_ORACLE_R1.json');surface=load(B/'alpha-hand-relax-surface-qa-r1/FINGER_SURFACE_QA_PRIVATE_R1.json');ui=load(D/'WHOLE_1X_UI_QA_R1.json');inventory=load(B/'alpha-hand-relax-inspect-r1/NATIVE_FINGER_INVENTORY_PRIVATE_R1.json');assert pixel['PASS'] and c['fixed_nonfinger_world_matrix_error']==0 and c['endpoint_evaluated_body_error_local_m']==0 and all(x['ended'] and x['playbackRate']==1 and x['error'] is None for x in ui['end']);assert sha(c['source'])==c['source_SHA'] and sha(c['candidate'])==c['candidate_SHA'];E.mkdir(exist_ok=False)
summary={k:v for k,v in c.items() if k not in ['frames_private','axes_local_private','palm_inward_rig_axis']};summary.update({'OFF_reopen':off,'OFF_neutral_RGBA':pixel,'actual_surface_QA':{k:v for k,v in surface.items() if k!='frames_private'},'native_inventory':{'native_finger_bones':30,'right_finger_bones':inventory['right_finger_bones'],'weights':inventory['weights'],'existing_finger_actions':[{'name':a['name'],'range':a['range'],'channel_count':len(a['channels'])} for a in inventory['existing_finger_actions']]},'normal_speed_UI':ui,'source_status':'SOURCE_ONLY_PROVISIONAL_CONTACT_HOLD','hand_quality':'Gentle curl and release readable; no gross finger/thumb penetration, abrupt pop or mesh explosion observed in three full1x views. Conservative digit-surface cohort measurements supplement visual evidence; weak-weight webbing/palm and same-digit folds not certified.','remaining_defects':['Source neutral open pose is used unchanged as relaxed-open; no polished hand-rest redesign','Gentle pregrasp only, no complete fist/thumb opposition/prop fit or physical grasp','Fine palm/webbing skin quality and exact whole-hand self-intersection HOLD; low-sample source QA','Original source arms/body remain neutral; no wrist/palm approach, forearm rotation or actual target-contact animation','Runtime Action ownership/clock must remain finger-only; Unity/AlwaysAnimate integration not executed'],'original_44TierC':44,'TierP':0,'StageB_F2_final_promotion':False,'new_donor_capture_count':0,'all_prior_controls_and_bundles_preserved':True});write(E/'HAND_RELAX_MANIFEST_R1.json',summary);write(E/'ACTION_ONLY_CUSTODY_R1.json',load(B/'alpha-hand-relax-off-qa-r1/ACTION_ONLY_CUSTODY_R1.json'))
guards=[]
for run in ['o1-hand-relax-inspect-r1','o1-hand-relax-candidate-r1','o1-hand-relax-off-r1','o1-hand-relax-probe-r1','o1-hand-relax-full-r1','o1-hand-relax-surface-r1']:
 p=B/run/'NATIVE_GUARD_RESULT.json';v=load(p);assert v['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN';guards.append({'run':run,'receipt':str(p),'sha256':sha(p),'status':v['guard_status'],'wall_seconds':v['wall_seconds']})
write(E/'NATIVE_CUSTODY_R1.json',guards)
text='''# Original R4 right finger-only relax → gentle pregrasp → release

One source-only procedural candidate on immutable a30fc513 original R4. Earlier response cited old820a237 correction rather than this task: no hand candidate or active native worker existed on reconciliation. Original GUI Blender PID129152 was preserved. Current work uses fresh unchanged owned process guards, CPU only, PRODUCT_EXCLUSIVE lease unchanged. No product/Unity writer, merge, paid use or downloads.

Read-only actual-source inventory confirms30 native finger bones,15 per hand, existing weights and13 original Actions containing right-finger channels. All78 source Actions remain preserved. Only15 right finger quaternion channels are authored, no wrist/hand/forearm/body/root/face/gaze/hair transform keys. Original palm plane is derived from native knuckle width and finger direction; previous experimental GameRig axis constants/geometry are not reused. Original source neutral open pose is the endpoint; maximum nominal four-finger per-joint curl12/18/10deg with small digit amplitude/1–4frame timing asymmetry, thumb4/6/4deg. This is a gentle curl recipe, not a full fist or thumb opposition solution.

105frames30fps,3.5s movie. Source open1–15; stagger curl16–52; hold53–69; release70–105. Source scene remains24fps, consume per-Action source_fps30. Existing rest axes/weights/materials/drivers and original rig maintained. All105 native evaluated body meshes finite. All42 non-right-finger body-bone world matrices are identical, including wrist/forearm/body/root/left hand. Final evaluated body vertex coordinates equal first frame exactly. OFF original full signature identical before save; reopen geometry/material/ShapeKeys/weights/rest/drivers/scene identical. Raw relative texture locator strings remap after SaveAs; resolved paths/packed bytes/colorspace remain identical. Source-camera960×920 decoded RGBA unequal channels0/maxdiff0. Source bytes remain unchanged.

Hand close / original-world front / hand-side each render all105 native frames, encode30fps, whole decode and actual UI normal-speed through-end. Full-body first/peak/end position evidence accompanies all-frame exact nonfinger matrices. Actual evaluated disjoint dominant-weight(>=.5) digit triangle cohorts are checked by BVH at all105 frames; metrics in manifest are bounded surface evidence, not full mesh collision certification. Review found gentle curl/release readable without gross thumb/finger penetration or sudden deformation pop. Weak-weight palm/webbing, same-digit folds, fine skin and final hand quality HOLD. Low-sample source preview is not final appearance promotion.

Playback: open original source, append Action datablocks ONLY from animation-only/YURI_R4_HAND_RELAX_ACTIONS_ONLY_R1.blend, then ReactionLane().on('YURI_R4_HAND_RELAX_PREGRASP_FINGERS_R1') on Meshy_Fitted_Rig. Frame1..105 at30fps in transient QA session. ReactionLane.off() restores saved pose/frame/Action slot/binding; do not reset/mute face/gaze or source helper bones. Saved OFF candidate is an editable derivative, never canonical visual authority. No object/mesh/armature/material in Action library. One Action owns only existing right-finger quaternion channels. Native source/Action/runtime adapter remain separate. No new canonical FBX/VRM.

No wrist/palm approach, target prop fitting/contact, physics, MUG or Unity/AlwaysAnimate completion claim. StageB/F2/F3/TierP0 remain HOLD. No new donor corpus count. Prior08caad7,820a237,R2/R3d/Reactions/social/C1/C3/look-listen and closed successful/failed bundles remain preserved. Next bounded motion integration is reuse of this finger-only layer on an existing reach source candidate with explicit upper-limb versus finger Action ownership and real prop/contact evidence; product implementation is outside this source checkpoint.
'''
(E/'YURI_R4_HAND_RELAX_SOURCE_R1.md').write_text(text,encoding='utf8')
files={}
def add(p,n):
 p=Path(p);assert p.is_file() and n not in files;files[n]=p
add(c['source'],'source/'+Path(c['source']).name);add(c['candidate'],'candidate/'+Path(c['candidate']).name)
for folder in ['alpha-hand-relax-inspect-r1','alpha-hand-relax-candidate-r1','alpha-hand-relax-off-qa-r1','alpha-hand-relax-surface-qa-r1']:
 for p in (B/folder).rglob('*'):
  if p.is_file() and p.suffix not in ['.blend','.blend1']:add(p,'private-evidence/'+folder+'/'+p.relative_to(B/folder).as_posix())
for p in (B/'alpha-hand-relax-off-qa-r1').glob('*.blend'):add(p,'animation-only/'+p.name)
for p in E.iterdir():add(p,'metadata/'+p.name)
for p in D.iterdir():
 if p.is_file():add(p,'review/'+p.name)
for g in guards:
 for p in (B/g['run']).rglob('*'):
  if p.is_file():add(p,'native-custody/'+g['run']+'/'+p.relative_to(B/g['run']).as_posix())
add(B/'alpha-hand-relax-preview-r1/RENDER_RECEIPT_R1.json','camera/RENDER_RECEIPT_R1.json')
for p in (L/'scripts').glob('r4_hand_relax*.py'):add(p,'workflow/'+p.name)
for n in ['r4_appearance_adapter.py','r4_appearance_signature.py','native_preservation.py']:add(L/'scripts'/n,'workflow/'+n)
idx={n:{'bytes':p.stat().st_size,'sha256':sha(p)} for n,p in sorted(files.items())};ip=D/'MEMBER_SHA256_INDEX_R1.json';write(ip,idx);add(ip,ip.name);zp=B/'YURI_R4_HAND_RELAX_SOURCE_ONLY_R1_20261004.zip'
with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):z.write(p,n)
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 for n,v in idx.items():
  b=z.read(n);assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256']
 receipt={'file':str(zp),'bytes':zp.stat().st_size,'sha256':sha(zp),'members':len(z.namelist()),'indexed_members':len(idx),'CRC_SHA_size_all_members':'PASS','candidate_SHA256':c['candidate_SHA'],'source_SHA256':c['source_SHA'],'TierP':0,'source_only':True,'status':'SOURCE_ONLY_PROVISIONAL_CONTACT_HOLD'}
write(E/'PRIVATE_PACKET_RECEIPT_R1.json',receipt);write(D/'PRIVATE_PACKET_RECEIPT_R1.json',receipt);print(json.dumps(receipt,indent=2))
