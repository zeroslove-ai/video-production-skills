"""Close one failed native-neutral experiment, private motion assets stay out of public Git."""
from pathlib import Path
import json,hashlib,zipfile
from PIL import Image
import numpy as np
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');L=Path(__file__).resolve().parents[1];D=B/'alpha-c1-neutral-replant-delivery-r1';E=L/'evidence/alpha-c1-neutral-supported-replant-r1';E.mkdir(exist_ok=False)
def load(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
 with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
d=load(B/'alpha-c1-neutral-supported-replant-r1/SUPPORTED_REPLANT_PRIVATE_R1.json');i=load(B/'alpha-c1-neutral-bridge-inspect-r1/C1_NEUTRAL_TARGET_INSPECTION_PRIVATE_R1.json');negative=load(B/'alpha-c1-neutral-frozen-contact-probe-r1/FROZEN_CONTACT_CAUSAL_NEGATIVE_PRIVATE_R1.json');pixel=load(D/'OFF_PIXEL_ORACLE_R1.json');ui=load(D/'WHOLE_1X_UI_QA_R1.json');assert all(v['ended'] and v['playbackRate']==1 and v['error'] is None for v in ui['end']);assert pixel['PASS'];assert sha(d['candidate'])==d['candidate_SHA'] and sha(i['source'])==d['source_SHA']
a=np.asarray(Image.open(B/'alpha-a1-contact-qa-r3/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png'));c=np.asarray(Image.open(B/'alpha-c1-neutral-frozen-contact-probe-r1/EXACT_SOURCE_NEUTRAL_POSE_PROBE.png'));assert np.array_equal(a,c)
rows=d['frames_private'];summary={k:v for k,v in d.items() if k not in ['frames_private','endpoint_native_rotation_gap_rad']};summary.update({'status':'SOURCE_ONLY_REPLANT_EXPERIMENT_FAIL_HOLD','original_R4_appearance_promoted':False,'frozen_contact_causal_negative_closed_once':{k:negative[k] for k in ['decision','declared_target','target_missing','target_exact_evaluated_body_head_hair_world_error_m','actual_grounded_vertex_constraints','proof']},'source_target_probe_RGBA_changed_pixels':0,'OFF_reopened_RGBA_pixel_oracle':pixel,'max_actual_surface_centroid_minZ_solver_residual_m':max(x['solver_residual_m'] for r in rows for x in r['sides'].values()),'max_supported_sole_vertex_drift_m':max(v for r in rows for v in r['support_contact_vertex_drift_m'].values()),'max_knee_step_m':max(v for r in rows for v in r['knee_step_m'].values()),'max_body_vertex_step_m':max(r['body_max_vertex_step_m'] for r in rows),'normal_speed_actual_UI':ui,'new_movies':'Only transition frames61..133,73frames30fps2.433333seconds in fixed body-front/feet-side; original C1 entire61frame four-view1x receipt remains separate and unchanged','not_certified':'Exact neutral, zero planted vertex drift, full-body collision/physics/Unity/AlwaysAnimate/StageB/F2/F3/production promotion HOLD. No new reaction completion counted.','narrow_actual_dependency':'Existing three-scalar sole centroid/minZ solver leaves rotational pose null-space and does not constrain the entire support contact patch. Explicit canonical endpoint leg pose plus grounded patch/orientation constraints are required; current single experiment leaves3.061628mm support drift at97 and0.949101mm endpoint body component error. No target snap was applied.','quaternion_metric_note':'Private raw rotation_difference.angle may report2pi for antipodal quaternions; public verdict uses actual evaluated geometry/contact, not that raw diagnostic.','source_correction_checkpoint':'820a237; original08caad7 retained; six-reaction source-only appearance-preserving evidence unchanged','prior_contact_checkpoint':'00cb890','no_new_GameRig_export_donor_rig_mesh_weights_material_or_product_changes':True,'TierP':0})
write(E/'NEUTRAL_REPLANT_SOURCE_MANIFEST_R1.json',summary)
guards=[]
for n in ['o1-c1-neutral-bridge-inspect-r1','o1-c1-neutral-frozen-contact-probe-r1','o1-c1-neutral-supported-replant-r1','o1-c1-neutral-replant-preview-r1']:
 p=B/n/'NATIVE_GUARD_RESULT.json';v=load(p);assert v['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN';guards.append({'run':n,'receipt_SHA':sha(p),'guard_status':v['guard_status'],'wall_seconds':v['wall_seconds']})
write(E/'NATIVE_CUSTODY_R1.json',guards)
(E/'YURI_R4_C1_NEUTRAL_SUPPORTED_REPLANT_R1.md').write_text('''# R4 exact-source neutral: one supported replant experiment

Source-only FAIL/HOLD. Original R4 SHA a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa remains the immutable visual authority. Existing78 source Actions,8 reused control Actions, R2 finger timing, original C1 frames1–61, hierarchy/rest/skin/geometry/keys/material/drivers and world carrier were preserved. Candidate contains only additive Action copies, saved OFF. No GameRig/donor/mesh merge/export/product change. Existing08caad7 and completed00cb890 contact packet remain immutable.

The approved target is original animation-OFF frame1 source pose, not guessed idle. Source frame1 and91 evaluated body/head/hair are identical. Applying exact original pose in a diagnostic probe reproduces authoritative960×920 RGBA with0 changed pixels. Both currently grounded feet need horizontal displacement to reach that source pose: minimum112mm left/123mm right among grounded vertex cohorts. Therefore frozen contacts and exact source-neutral geometry cannot both hold; this incompatibility is closed once.

One actual native candidate follows: L swing/replant transition6–30 while R supported, R swing/replant36–60 while L supported,12-frame settle. 72 new frames at30fps after C1 frame61. Pelvis weight-transfer recipe18mm sideways/8mm lowering,35mm sin² lift, toe and world foot orientation change only during each swing. Existing evaluated-surface thigh/shin damped Jacobian solver reused,12 iterations, .12rad step clamp, temporal warm-start. This is an animation support recipe, not a physics/COM certificate.

Whole native133-frame candidate retains original61 evaluated body hashes. Body/head/hair/source structure and all previous Actions restored exactly OFF before save. Root unchanged. Maximum solver centroid/minZ residual0.747847mm and knee per-frame step15.0249mm; no190mm knee branch pop recurred. However supported right sole vertex drift3.061628mm at97 exceeds the predeclared3mm experiment threshold, and final body maximum component error0.949101mm differs from exact canonical neutral. Head/hair endpoint error0. No forced canonical-pose snap hides the residual. Three scalar foot constraints leave rotational null-space and do not certify an entire planted patch. A canonical endpoint leg pose plus contact-patch/orientation constraint is the narrow next dependency; no rig/skin edit is needed or authorized.

Reopened candidate OFF source-camera RGBA0 changed pixels. Complete new transition frames61–133 were rendered in two fixed views, encoded at30fps, fully decoded and actually played1x through-end. These movies show the experiment even though acceptance fails; they are not a new passed production motion. Original C1 four-view61-frame normal-speed evidence remains separate. Whole-body/weak-weight collision, prop/physics, Unity/AlwaysAnimate, StageB/F2/F3/TierP remain HOLD. No new reaction completion count or appearance promotion.

Unchanged installed broker, exact new collector custody, CPU-only native processes,600sec/4GiB/two-thread/one-process limits and strict identity-before/after/terminal-drain receipts passed. Original GUI/product/laptop workers untouched. Raw geometry/poses/Actions/images/movies are private local evidence; public Git contains scripts, scalar reports and SHA pointers only.
''',encoding='utf-8')
files={}
def add(p,n):p=Path(p);assert p.is_file() and n not in files;files[n]=p
add(i['source'],'source/'+Path(i['source']).name);add(d['candidate'],'experimental-candidate/'+Path(d['candidate']).name);add(i['action_library'],'unchanged-lineage-actions/'+Path(i['action_library']).name)
for folder in ['alpha-c1-neutral-bridge-inspect-r1','alpha-c1-neutral-frozen-contact-probe-r1','alpha-c1-neutral-supported-replant-r1']:
 for p in (B/folder).rglob('*'):
  if p.is_file() and p.suffix not in ['.blend','.blend1']:add(p,'private-evidence/'+folder+'/'+p.relative_to(B/folder).as_posix())
for p in D.iterdir():
 if p.is_file():add(p,'review/'+p.name)
add(B/'alpha-c1-neutral-replant-preview-r1/PREVIEW_RECEIPT_R1.json','camera/PREVIEW_RECEIPT_R1.json');add(B/'alpha-c1-neutral-replant-preview-r1/CANDIDATE_OFF_SOURCE_NEUTRAL_R1.png','OFF/CANDIDATE_OFF_SOURCE_NEUTRAL_R1.png')
for p in E.iterdir():add(p,'metadata/'+p.name)
for g in guards:
 for p in (B/g['run']).rglob('*'):
  if p.is_file():add(p,'native-custody/'+g['run']+'/'+p.relative_to(B/g['run']).as_posix())
for p in (L/'scripts').glob('r4_c1_neutral*.py'):add(p,'workflow/'+p.name)
for n in ['r4_appearance_signature.py','r4_appearance_adapter.py','r4_c1_contact_path_adapter_r1.py','r4_c1_contact_surface_oracle_r3.py']:add(L/'scripts'/n,'workflow/'+n)
for n in ['r4_two_input_owned_barrier_broker_r1.py','r4_two_input_live_barrier_wrapper_r1.py']:add(B/'o1-morph67-native-broker-preparation-r4/workflow'/n,'native-workflow/'+n)
idx={n:{'bytes':p.stat().st_size,'SHA':sha(p)} for n,p in sorted(files.items())};ip=D/'MEMBER_SHA256_INDEX_R1.json';write(ip,idx);add(ip,ip.name);zp=B/'YURI_R4_C1_NEUTRAL_REPLANT_EXPERIMENT_R1_20261004.zip'
with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):z.write(p,n)
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 for n,v in idx.items():raw=z.read(n);assert len(raw)==v['bytes'] and hashlib.sha256(raw).hexdigest()==v['SHA']
 receipt={'file':str(zp),'bytes':zp.stat().st_size,'SHA':sha(zp),'members':len(z.namelist()),'indexed_members':len(idx),'CRC_SHA_size_all':'PASS','candidate_SHA':d['candidate_SHA'],'source_SHA':d['source_SHA'],'verdict':'FAIL_HOLD','TierP':0};write(E/'PRIVATE_PACKET_RECEIPT_R1.json',receipt);write(D/'PRIVATE_PACKET_RECEIPT_R1.json',receipt);print(json.dumps(receipt,indent=2))
