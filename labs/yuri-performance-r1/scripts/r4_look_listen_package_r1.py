"""Existing private delivery path: one A3-derived source look/listen, gaze ownership HOLD."""
from pathlib import Path
import json,hashlib,zipfile,numpy as np
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');L=Path(__file__).resolve().parents[1];D=B/'alpha-look-listen-delivery-r1';E=L/'evidence/alpha-look-listen-source-candidate-r1'
def load(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
 with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
c=load(B/'alpha-look-listen-candidate-r1/LOOK_LISTEN_CANDIDATE_PRIVATE_R1.json');off=load(B/'alpha-look-listen-off-qa-r1/OFF_REOPEN_ORACLE_R3.json');pixel=load(B/'alpha-look-listen-off-qa-r1/OFF_RGBA_ARRAY_EQUAL_R1.json');ui=load(D/'WHOLE_1X_UI_QA_R1.json');assert pixel['all_channels_exact'] and all(x['ended'] and x['playbackRate']==1 and x['error'] is None for x in ui['end']);assert sha(c['source'])==c['source_SHA'] and sha(c['candidate'])==c['candidate_SHA'] and sha(c['lineage']['reused_A3_candidate'])==c['lineage']['reused_A3_SHA'];E.mkdir(exist_ok=False)
r=c['frames_private'];quiet={n:np.ptp([x['joints'][n] for x in r],axis=0).tolist() for n in ['root','pelvis','foot.L','foot.R']};assert all(max(a)==0 for a in quiet.values()) and c['max_sole_world_delta_m']==0 and c['return_endpoint_body_max_abs_world_delta_m']==0
summary={k:v for k,v in c.items() if k!='frames_private'};summary.update({'OFF_reopen':off,'OFF_neutral_RGBA':pixel,'quiet_joint_world_ranges_m':quiet,'normal_speed_UI':ui,'source_status':'SOURCE_ONLY_PROVISIONAL_GAZE_OWNERSHIP_HOLD','visual_verdict':'Look/listen/return readable in three normal-speed previews; no gross head/neck/shoulder break or sliding observed. Detailed neck seam/skin/final facial quality not certified.','head_ownership_runtime_integration':'HOLD; existing canonical gaze adapter not executed, no consumer code or shared head-writer arbitration introduced','remaining_defects':['A3 source was look proxy; this procedural hold/1.5deg nod is a semantic listen recipe, not a captured/authored listen source','Default source arms/fingers/face are held; no polished idle/finger/blink/facial layer claimed','Exact mesh self-intersection and fine neck seam/face/hair/skin quality HOLD; CPU2sample512x640 evidence','Consumer needs explicit chest/neck/head ownership or blending with gaze adapter; no assumption that both writers can rotate head concurrently'],'original_44TierC':44,'TierP':0,'StageB_F2_final_promotion':False,'all_prior_source_controls_and_closed_bundles_preserved':True,'new_donor_capture_count':0});write(E/'LOOK_LISTEN_MANIFEST_R1.json',summary);write(E/'ACTION_ONLY_CUSTODY_R1.json',load(B/'alpha-look-listen-off-qa-r1/ACTION_ONLY_CUSTODY_R1.json'))
guards=[]
for run in ['alpha-look-listen-candidate-broker-r1','alpha-look-listen-off-broker-r1','alpha-look-listen-probe-broker-r1','alpha-look-listen-full-broker-r1']:
 p=B/run/'NATIVE_GUARD_RESULT.json';v=load(p);assert v['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN';guards.append({'run':run,'receipt':str(p),'sha256':sha(p),'status':v['guard_status'],'wall_seconds':v['wall_seconds']})
write(E/'NATIVE_CUSTODY_R1.json',guards)
(E/'YURI_R4_LOOK_LISTEN_SOURCE_R1.md').write_text('''# Original R4 look → listen hold → neutral return: one A3-derived source candidate

Reuses verified A3 R4 Action YURI_R4_A3_BODY_CANDIDATE_R2 from immutable candidate1e16f352...; staged donor StayStill l_aro_2_32 /833e5d992179b527040b is MIT. No new download/donor scan. Local chest/neck/head quaternion delta from existing Action frame1→49 is reduced to15/33/33 percent, then a new clock/hold/nod/return is authored. Existing A3 was look proxy only; listen is a procedural semantic recipe, not captured listen. This derivative is not another donor corpus capture or Stage B completion.

One151-frame30fps/5.0sec key interval/5.033333sec movie. Neutral1–12, look13–42, listen hold43–102,1.5deg neck nod63–83, return103–151. Native head world rotation reaches11.407853deg; maximum sampled joint position step0.303165mm. Root/pelvis/feet joint world ranges0 and original-neutral sole vertex world maximum delta0 across all151frames. Lower-body/carrier channels were never used or compensated; no root freeze/floor clamp/IK correction hides foot movement. Final evaluated body geometry returns to original neutral exactly (max abs0). All151 body/head evaluated vertex arrays finite.

Original R4a30fc513 source bytes, geometry/material/nodes/textures/ShapeKeys/weights/rest/hierarchy/face-gaze drivers and78 Actions remain identical OFF. Full neutral RGBA difference0 against existing authority witness. Raw texture filepath strings remap after SaveAs; resolved properties, packed bytes/colorspace remain identical. New three-Action set contains body chest/neck/head plus existing face-rig Root and Hair_HeadRoot rigid transport only; original head skin/rig/gaze drivers and hair rig/mesh untouched. No new expressive facial or secondary-hair channels. Action-only BLEND contains0 objects/meshes/armatures. Saved source scene24fps preserved; consume Action source_fps30.

Motion owns Meshy_Fitted_Rig.chest/neck/head rotations. Armature.Root and Hair_Rig_R4.Hair_HeadRoot follow body head via existing rigid transport. Original Face_GazeYaw/Pitch and ShapeKey/driver channels have no motion keys. This source separation does NOT certify integration with the actual canonical runtime gaze adapter. If that adapter writes head/neck, consumer must provide one owner or explicit blend; applying head rotation twice is not validated. Product head/gaze arbitration, fine neck seam/skin/face/hair quality and exact mesh self-intersection HOLD. Default arms/fingers/neutral face remain source baseline; no polished facial performance claimed.

Full front/quarter/side ORTHO1.2m512×640 CPU2sample/JPEG85 previews render all151native frames, encode at30fps, whole decode and actually play through end at1x. Look/listen/return are readable without observed gross head/neck/shoulder break or sliding in the previews. Low-cost evidence does not certify final appearance/physical contact or Unity state/time/weight/AlwaysAnimate. StageB/TierP0/F2/final promotion HOLD.

Existing source, editable OFF candidate, animation-only library, unchanged reused A3 Action authority (Actions-only load, no donor geometry append), MIT notice/donor lineage, native receipts, camera/clock/timing and three normal-speed movies are in private packet. Use existing ReactionLane on three mapping pairs and off() for restore; no carrier Action. Relocated replay needs scoped paths/new exact guard. Existing greeting/C1/C3/contact-HOLD/walk/first4/six Reactions/08caad7 controls and all closed packets are preserved.

Next bounded consumer decision is explicit head/neck ownership against canonical gaze adapter using actual runtime evidence. No new framework, facial layer, product writer, Slack report or additional motion was created.
''',encoding='utf8')
files={}
def add(p,n):
 p=Path(p);assert p.is_file() and n not in files;files[n]=p
add(c['source'],'source/'+Path(c['source']).name);add(c['candidate'],'candidate/'+Path(c['candidate']).name);add(c['lineage']['reused_A3_candidate'],'lineage-action-authority/'+Path(c['lineage']['reused_A3_candidate']).name)
for folder in ['alpha-look-listen-candidate-r1','alpha-look-listen-off-qa-r1']:
 for p in (B/folder).rglob('*'):
  if p.is_file() and p.suffix not in ['.blend','.blend1']:add(p,'private-evidence/'+folder+'/'+p.relative_to(B/folder).as_posix())
for p in (B/'alpha-look-listen-off-qa-r1').glob('*.blend'):add(p,'animation-only/'+p.name)
for p in E.iterdir():add(p,'metadata/'+p.name)
for p in D.iterdir():
 if p.is_file():add(p,'review/'+p.name)
for g in guards:
 for p in (B/g['run']).rglob('*'):
  if p.is_file():add(p,'native-custody/'+g['run']+'/'+p.relative_to(B/g['run']).as_posix())
for view in ['front','quarter','side']:add(B/'alpha-look-listen-preview-r1'/view/'RENDER_RECEIPT_R4.json','camera/'+view+'_RENDER_RECEIPT_R4.json')
for p in (L/'scripts').glob('r4_look_listen*.py'):add(p,'workflow/'+p.name)
for n in ['r4_appearance_adapter.py','r4_appearance_signature.py','native_preservation.py']:add(L/'scripts'/n,'workflow/'+n)
add(L/'evidence/alpha-a3-body-candidate-r2/SOURCE_CANDIDATE_PUBLIC_RECEIPT_R2.json','lineage-action-authority/A3_PUBLIC_RECEIPT_R2.json')
lic=Path('C:/Users/JAEWAN/.codex/worktrees/common-motion-curation-r1/yuri-room-mvp/common-motion-r1/licenses/StayStill-LICENSE.txt');add(lic,'licenses/'+lic.name)
idx={n:{'bytes':p.stat().st_size,'sha256':sha(p)} for n,p in sorted(files.items())};ip=D/'MEMBER_SHA256_INDEX_R1.json';write(ip,idx);add(ip,ip.name)
zp=B/'YURI_R4_LOOK_LISTEN_SOURCE_ONLY_R1_20261004.zip'
with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):z.write(p,n)
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 for n,v in idx.items():
  b=z.read(n);assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256']
 receipt={'file':str(zp),'bytes':zp.stat().st_size,'sha256':sha(zp),'members':len(z.namelist()),'indexed_members':len(idx),'CRC_SHA_size_all_members':'PASS','candidate_SHA256':c['candidate_SHA'],'source_SHA256':c['source_SHA'],'reused_A3_SHA256':c['lineage']['reused_A3_SHA'],'TierP':0,'source_only':True,'status':'SOURCE_ONLY_PROVISIONAL_GAZE_OWNERSHIP_HOLD'}
write(E/'PRIVATE_PACKET_RECEIPT_R1.json',receipt);write(D/'PRIVATE_PACKET_RECEIPT_R1.json',receipt);print(json.dumps(receipt,indent=2))
