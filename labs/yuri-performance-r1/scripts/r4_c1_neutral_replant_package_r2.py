"""Close R2 once; improved endpoint is scoped PASS, motion remains FAIL/HOLD."""
import json,hashlib,zipfile
from pathlib import Path
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');L=Path(__file__).resolve().parents[1];D=B/'alpha-c1-neutral-replant-delivery-r2';E=L/'evidence/alpha-c1-neutral-supported-replant-r2';E.mkdir(exist_ok=False)
def load(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):
 with p.open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
d=load(B/'alpha-c1-neutral-supported-replant-r2/SUPPORTED_REPLANT_PRIVATE_R2.json');i=load(B/'alpha-c1-neutral-bridge-inspect-r1/C1_NEUTRAL_TARGET_INSPECTION_PRIVATE_R1.json');lib=load(B/'alpha-c1-neutral-replant-preview-r2/ACTION_ONLY_CUSTODY_R2.json');fresh=load(B/'alpha-c1-neutral-contact-library-qa-r2/SOURCE_PLUS_FIVE_ACTIONS_ORACLE_R2.json');offpix=load(D/'OFF_PIXEL_ORACLE_R2.json');onpix=load(D/'ON_ENDPOINT_PIXEL_ORACLE_R2.json');ui=load(D/'WHOLE_1X_UI_QA_R2.json');assert offpix['PASS'] and onpix['PASS'];assert all(v['ended'] and v['playbackRate']==1 and v['error'] is None for v in ui['end']);assert sha(d['candidate'])==d['candidate_SHA'] and sha(i['source'])==d['source_SHA'];assert len(lib['named_actions'])==5 and all(v==0 for v in d['endpoint_geometry_component_error_m'].values());rows=d['frames_private'];support=[x for r in rows for x in r['sides'].values() if x['phase']=='SUPPORT']
summary={k:v for k,v in d.items() if k not in ['frames_private']};summary.update({'status':'SOURCE_ONLY_R2_FAIL_HOLD_EXACT_ENDPOINT_PASS','OFF_reopen_pixels':offpix,'fresh_source_plus_five_Actions_endpoint_pixels':onpix,'fresh_source_plus_five_Actions_custody':fresh,'Action_only_asset':lib,'max_actual_whole_sole_world_target_error_m':max(x['whole_sole_world_constraint_max_error_m'] for r in rows for x in r['sides'].values()),'max_SUPPORT_whole_sole_world_error_m':max(x['whole_sole_world_constraint_max_error_m'] for x in support),'max_SUPPORT_grounded_patch_world_error_m':max(x['actual_grounded_patch_constraint_max_error_m'] for x in support),'max_native_knee_step_m':max(v for r in rows for v in r['knee_steps_m'].values()),'normal_speed_actual_UI':ui,'visual_scope':'Two complete fixed-view73-frame30fps transition movies played1x through-end plus every-frame feet supplement. No gross knee branch pop seen; source shading/material noise retained. Numerical motion constraint FAIL is unchanged, no production-quality acceptance.','R1_checkpoint':'50e8ab7','R1_immutable_packet_SHA':'34edd98b52618a376a31231b8c33b34c24e636f9e0a35fc7db98a69818beaaa6','original08caad7_R4_C1_R1_R2_fingers_original78Actions_unchanged':True,'source_original_appearance_promoted':False,'remaining_dependency':'Whole-sole positional targets exceed3mm during swing despite9DOF fitting; support patch error remains nonzero. This ONE alternative is closed as FAIL/HOLD. Do not hide it by endpoint certification or weaken thresholds. No third solver/neutral hypothesis in the current blocking lane.','next_bounded_task':'Neutral restoration research becomes nonblocking. Return to one independent StageA/B source motion: inspect/reuse original66-action MESHY_R2_BODY_TalkGesture as upper-body native quaternion candidate, preserve grounded feet/root and original R4 rig/rest/material/drivers. No reaction14 expansion.','product_Unity_AlwaysAnimate_physics_StageB_F2_F3_TierP':'HOLD; TierP0'})
write(E/'NEUTRAL_CONTACT_PATCH_SOURCE_MANIFEST_R2.json',summary);write(E/'ACTION_ONLY_CUSTODY_R2.json',lib)
guards=[]
for run in ['o1-c1-neutral-supported-replant-r2','o1-c1-neutral-replant-preview-r2','o1-c1-neutral-contact-library-qa-r2']:
 p=B/run/'NATIVE_GUARD_RESULT.json';g=load(p);assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN';guards.append({'run':run,'SHA':sha(p),'guard_status':g['guard_status'],'wall_seconds':g['wall_seconds']})
write(E/'NATIVE_CUSTODY_R2.json',guards)
(E/'YURI_R4_C1_NEUTRAL_CONTACT_PATCH_R2.md').write_text('''# R4 C1 neutral R2: exact endpoint PASS, full motion FAIL/HOLD

One alternative to R1 centroid/minZ constraints used actual evaluated whole-sole world vertex positions, including the55/68 currently grounded contact vertices, through existing native thigh/shin/foot9DOF. Same R1 sequential L/R steps, pelvis weight-transfer, body/head/hair and finger clocks retained. Five-iteration damped Jacobian/Broyden fit, .06rad correction clamp. A small R1 leg pose null-space correction eases toward the original source quaternion pose through all12 settle frames; antipodal signs are aligned, source endpoint is the analytic endpoint of that smooth interpolation, not a post-solve snap. Cause inspection restricted to R1 worst97 and endpoint133. No broader rig/solver/framework research.

R4 geometry/rest/weights/material/ShapeKeys/face-gaze drivers/hierarchy remain immutable. Original78 Actions, all R1/control Actions, original C1 frames1–61 evaluated geometry and existing R2 LEFT finger Action preserved. Only a new body Action is added; head/hair/root Actions reused. World root unchanged. Original08caad7/00cb890/50e8ab7 and all closed packets are retained.

Endpoint body/head/hair evaluated source geometry error0. Actual last adjacent body maximum vertex step0.1387795mm; peak sampled knee step15.0249mm, no190mm branch pop. Fresh ORIGINAL source plus ONLY five Action assets and fixed transient NLA adapter reproduced endpoint geometry0 and original source-camera960×920 RGBA0 changed pixels. OFF reopened candidate also has0 changed pixels. These endpoint/OFF/library-custody results are scoped PASS and do not certify the transition.

Full motion remains FAIL/HOLD:32 sampled constraints exceed the unchanged3mm whole-sole world-target threshold during swings, maximum8.393777mm. Maximum supported whole-sole world error2.941325mm, actual supported grounded-patch world error2.270456mm; still nonzero, no zero-slip claim. Do not relax the gate or conflate exact endpoint with faithful grounded motion. Two complete fixed-view transition movies61–133/73frames30fps2.433333seconds were fully decoded and played1x through-end, with actual every-frame feet supplement. All numerical failures retained, no product/physics/Unity/AlwaysAnimate/StageB/F2/F3/TierP promotion.

Private bundle separates immutable source, experimental candidate, five-Action-only asset0objects0meshes0rigs and fixed Blender runtime adapter. It is a failed research experiment, not a canonical character or release. Original source bytes and prior candidates unchanged. Strict owned native identity-before/after and terminal drain passed under original600sec/4GiB/two-thread/one-process guard; CPU only, healthy GUI/product/laptop workers untouched. Public Git holds scripts/scalar metadata/SHA pointers only.

R1 and this one alternative are now closed. Neutral/contact restoration stays in a nonblocking research lane; no third solver experiment here. Resume independent StageA/B motion supply by inspecting/reusing the original66-action TalkGesture as one native upper-body candidate, keeping ground/root stable and source appearance immutable. This does not count the other14 reaction motions as created.
''',encoding='utf-8')
files={}
def add(p,n):p=Path(p);assert p.is_file() and n not in files;files[n]=p
add(i['source'],'source/'+Path(i['source']).name);add(d['candidate'],'failed-research-candidate/'+Path(d['candidate']).name);add(lib['file'],'animation-only/'+Path(lib['file']).name);add(L/'evidence/alpha-c1-neutral-supported-replant-r1/PRIVATE_PACKET_RECEIPT_R1.json','unchanged-R1-lineage/PRIVATE_PACKET_RECEIPT_R1.json')
for folder in ['alpha-c1-neutral-supported-replant-r2','alpha-c1-neutral-contact-library-qa-r2']:
 for p in (B/folder).rglob('*'):
  if p.is_file() and p.suffix not in ['.blend','.blend1']:add(p,'private-evidence/'+folder+'/'+p.relative_to(B/folder).as_posix())
for p in D.iterdir():
 if p.is_file():add(p,'review/'+p.name)
for name in ['ACTION_ONLY_CUSTODY_R2.json','PREVIEW_RECEIPT_R2.json','CANDIDATE_OFF_SOURCE_NEUTRAL_R2.png']:add(B/'alpha-c1-neutral-replant-preview-r2'/name,'reopen-camera/'+name)
for p in E.iterdir():add(p,'metadata/'+p.name)
for g in guards:
 for p in (B/g['run']).rglob('*'):
  if p.is_file():add(p,'native-custody/'+g['run']+'/'+p.relative_to(B/g['run']).as_posix())
for name in ['r4_c1_neutral_supported_replant_r2.py','r4_c1_neutral_replant_preview_r2.py','r4_c1_neutral_replant_video_r2.py','r4_c1_neutral_replant_package_r2.py','r4_c1_neutral_contact_patch_adapter_r2.py','r4_c1_neutral_contact_library_qa_r2.py','r4_c1_neutral_bridge_owned_prepare_r1.py','r4_appearance_signature.py','r4_appearance_adapter.py','r4_c1_contact_path_adapter_r1.py']:add(L/'scripts'/name,'workflow/'+name)
for name in ['r4_two_input_owned_barrier_broker_r1.py','r4_two_input_live_barrier_wrapper_r1.py']:add(B/'o1-morph67-native-broker-preparation-r4/workflow'/name,'native-workflow/'+name)
idx={n:{'bytes':p.stat().st_size,'SHA':sha(p)} for n,p in sorted(files.items())};ip=D/'MEMBER_SHA256_INDEX_R2.json';write(ip,idx);add(ip,ip.name);zp=B/'YURI_R4_C1_NEUTRAL_CONTACT_PATCH_EXPERIMENT_R2_20261004.zip'
with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):z.write(p,n)
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 for n,v in idx.items():raw=z.read(n);assert len(raw)==v['bytes'] and hashlib.sha256(raw).hexdigest()==v['SHA']
 receipt={'file':str(zp),'bytes':zp.stat().st_size,'SHA':sha(zp),'members':len(z.namelist()),'indexed_members':len(idx),'CRC_SHA_size_all':'PASS','source_SHA':d['source_SHA'],'candidate_SHA':d['candidate_SHA'],'library_SHA':lib['SHA'],'motion_verdict':'FAIL_HOLD','exact_endpoint_OFF_source_camera_pixels':'PASS_CHANGED0','TierP':0};write(E/'PRIVATE_PACKET_RECEIPT_R2.json',receipt);write(D/'PRIVATE_PACKET_RECEIPT_R2.json',receipt);print(json.dumps(receipt,indent=2))
