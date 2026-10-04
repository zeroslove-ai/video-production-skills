"""Fixed A2-A4 private source-candidate packet; excludes donor/source binaries from Git."""
import argparse,hashlib,json,zipfile
from pathlib import Path
from PIL import Image
import numpy as np
LAB=Path(__file__).resolve().parents[1];BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):
 with Path(p).open('x',encoding='utf8') as f:json.dump(d,f,ensure_ascii=False,indent=2)
def packet(step):
 assert step in ['a2','a3','a4'];out=BASE/f'alpha-{step}-contact-candidate-r2';d=json.loads((out/'CONTACT_CANDIDATE_PRIVATE_R2.json').read_bytes());q=json.loads((out/'ENCODE_AND_CONTACT_PROXY_RECEIPT_R1.json').read_bytes());ui=json.loads((out/'OBSERVED_UI_PLAYBACK_R1.json').read_bytes())
 assert all(v['ended'] and v['rate']==1 and v['error'] is None for v in ui['videos'])
 source=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend';assert sha(source)==d['source_SHA'];assert sha(d['candidate'])==d['candidate_SHA']
 original=BASE/'r4-appearance-preserve-correction-r1'
 # Resolve immutable original baseline through its existing evidence, not a new render.
 baseline=list(BASE.rglob('SOURCE_NEUTRAL.png'))
 if not baseline:baseline=list(BASE.rglob('source_neutral.png'))
 # Native OFF signatures already exact; neutral equality independently against A1 source-camera witness.
 witness=BASE/'alpha-a1-idle-candidate-r3/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png'
 if not witness.exists():witness=BASE/'alpha-a1-contact-qa-r3/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png'
 if not witness.exists():
  candidates=list((BASE/'alpha-a1-contact-qa-r3').glob('*.png'));assert len(candidates)==1;witness=candidates[0]
 a=Image.open(witness).convert('RGBA');b=Image.open(out/'CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png').convert('RGBA');assert a.size==b.size and np.array_equal(np.asarray(a),np.asarray(b))
 public=LAB/'evidence'/f'alpha-{step}-body-candidate-r2';public.mkdir(exist_ok=False)
 guards={};preview_revision='r3' if step=='a2' else 'r2'
 for name in [f'alpha-{step}-inspect-broker-r1',f'alpha-{step}-candidate-broker-r1',f'alpha-{step}-contact-broker-r2',*[f'alpha-{step}-{v}-preview-broker-{preview_revision}' for v in ['front','quarter','side']]]:
  path=BASE/name/'NATIVE_GUARD_RESULT.json'
  if not path.exists():
   # Candidate execution folder spelling is recorded, never fabricate a gate.
   alternate=BASE/f'alpha-{step}-bake-broker-r1'/'NATIVE_GUARD_RESULT.json';assert alternate.exists();path=alternate
  g=json.loads(path.read_bytes());assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN';guards[str(path)]={'sha256':sha(path),'status':g['guard_status']}
 allowed=['source_SHA','donor_SHA','previous_candidate_SHA','candidate','candidate_SHA','candidate_bytes','action','mapped_bones','frame_range','action_source_fps_readback','source_scene_fps_readback','original_BVH_fps_readback','key_interval_sec','original_actions_and_OFF_snapshot_exact','face_gaze_hair_channel_writes','support_z_correction_range_m','root_range_m','max_joint_frame_step_m','clean_sole_offsets_m','loop_authored','foot_contact_physics_certified','self_intersection_certified','TierP','root_policy','consumer_export_clock','limits']
 r={k:d[k] for k in allowed};r.update({'scope':'Source-only immutable-R4 additive body Action candidate; no visual/product promotion','step':step,'OFF_neutral_pixel_exact':True,'OFF_max_RGBA_difference':0,'neutral_witness_path':str(witness),'neutral_witness_SHA':sha(witness),'native_geometry_frames_evaluated':q['whole_native_geometry_frames'],'body_min_z_offset_min_m':q['body_min_z_offset_min_m'],'contact_proxy':q['contact_proxy'],'movies':q['movies'],'UI_playback':ui,'native_guard_receipts':guards,'semantics':{'a2':'long idle; not authored loop','a3':'look proxy, NOT authored listen','a4':'weight shift; not authored loop'}[step],'visual_verdict':'Source subset only; no obvious gross silhouette break in sampled views; complete media playback/decode observed. Low sample/resolution, static face/gaze, no exhaustive self-intersection/stance-slip certification.','acceptance_hold':['Unity AlwaysAnimate regression gate','TierP','StageB','O1','PRIMARY','F2-F3 final quality']})
 write(public/'SOURCE_CANDIDATE_PUBLIC_RECEIPT_R2.json',r)
 write(out/'CLIP_MAPPING_SOURCE_ONLY_R2.json',{'clip_uid':step,'semantic':r['semantics'],'action':d['action'],'frame_range':d['frame_range'],'body_timebase_fps':30,'scene_fps_preserved':24,'original_BVH_fps':30.0003,'preview_fps':7.5 if step=='a2' else 30,'frame_count':d['frame_range'][1],'key_interval_sec':d['key_interval_sec'],'container_duration_sec':d['frame_range'][1]/30,'loop_authored':False,'root_policy':d['root_policy'],'rig':'Meshy_Fitted_Rig original 57 bones','target_source_SHA':d['source_SHA'],'candidate_SHA':d['candidate_SHA'],'consumer_requirement':'Consume Action source_fps=30; do not infer clip speed from immutable source scene24. Actual export/Unity import not executed. Runtime adapter owned by Laptop sole writer.','face_gaze_fingers':'Original preserved, no LaFAN donor fingers or face mapping','TierP':0})
 files={}
 for file in out.iterdir():
  if file.is_file():files['candidate/'+file.name]=file
 for f in (LAB/'evidence/alpha-first4-source-checkpoint-r1').glob('*.json'):
  files['supplement/'+f.name]=f
 for f in [BASE/'alpha-first4-reopen-off-r3/SAVED_OFF_LOCATOR_DOMAIN_READBACK_R3.json',BASE/'alpha-first4-reopen-off-broker-r3/NATIVE_GUARD_RESULT.json']:
  files['supplement-native/'+f.name]=f
 files['source-only-public-receipt.json']=public/'SOURCE_CANDIDATE_PUBLIC_RECEIPT_R2.json'
 for view in ['front','quarter','side']:files['render/'+view+'_RENDER_RECEIPT.json']=BASE/f'alpha-{step}-preview-{view}-{preview_revision}/RENDER_RECEIPT.json'
 for guard in guards:
  root=Path(guard).parent
  for f in root.rglob('*'):
   if f.is_file():files['native/'+root.name+'/'+str(f.relative_to(root)).replace(chr(92),'/')]=f
 for f in (LAB/'scripts').glob('r4_alpha_'+step+'*.py'):files['workflow/'+f.name]=f
 for name in ['r4_alpha_first4_contact_cleanup_r1.py','r4_alpha_first4_preview_r1.py','r4_appearance_adapter.py','r4_appearance_signature.py']:
  files['workflow/'+name]=LAB/'scripts'/name
 lic=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/licenses')
 if lic.exists():
  for f in lic.rglob('*'):
   if f.is_file():files['licenses/'+str(f.relative_to(lic)).replace(chr(92),'/')]=f
 if step=='a2':
  for f in (BASE/'alpha-a2-front-preview-broker-r2').rglob('*'):
   if f.is_file():files['preserved-failed-output-cap-r2/'+str(f.relative_to(BASE/'alpha-a2-front-preview-broker-r2')).replace(chr(92),'/')]=f
 index={name:{'bytes':file.stat().st_size,'sha256':sha(file)} for name,file in files.items()}
 zpath=BASE/f'YURI_R4_{step.upper()}_BODY_CANDIDATE_R2_20261004.zip'
 with zipfile.ZipFile(zpath,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name,file in files.items():z.write(file,name)
  z.writestr('SHA256_INDEX.json',json.dumps(index,indent=2))
  z.writestr('README_PRIVATE_SCOPE.txt','Private project-use source-candidate bundle. Original R4 authority and donor FBX are not redistributed. Candidate BLEND contains immutable original character plus additive Actions; not canonical GameRig or final product. Source scene24, body Action30, A2 video7.5 normal time. TierP=0; no authored listen/loop or contact physics certification.')
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None
  for name,entry in index.items():data=z.read(name);assert len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256']
  members=len(z.namelist())
 custody={'path':str(zpath),'bytes':zpath.stat().st_size,'sha256':sha(zpath),'members':members,'member_SHA256_and_CRC_verified':True,'public_repo_contains_source_or_motion_binaries':False,'original_R4_and_donor_binary_excluded':True}
 write(public/'PRIVATE_PACKET_RECEIPT_R1.json',custody)
 text=f"""# {step.upper()} R4 appearance-preserved source candidate

실제 Windows capability 구현 증가: 0. DESKTOP source-only 후보이며 TierP=0 / StageB / O1 / PRIMARY / F2-F3 HOLD.

DONE: 원본 R4 SHA `{d['source_SHA']}` 유지. 원본 geometry/material/ShapeKeys/weights/rest/driver와 기존 Actions OFF snapshot exact, neutral RGBA difference 0. 신규 Action과 pelvis support-Z cleanup만 추가. Candidate bytes {d['candidate_bytes']}, SHA `{d['candidate_SHA']}`. 21 original body bones mapped; native fingers/face/gaze/hair preserved. Native guarded inspect/bake/contact/render 모두 PASS.

CLOCK: source scene24 unchanged / Action30 native readback / original BVH30.0003 / frame range {d['frame_range']}. Key interval {d['key_interval_sec']:.6f}s; video container {d['frame_range'][1]/30:.6f}s. A2는 4 native frames마다 pose를 취한 7.5fps 영상, source-time 1x이다. A3/A4 영상은 30fps 전 native frames. 실제 Unity/export는 미실행; consumer는 scene24 대신 Action.source_fps30 적용 필요.

QA: {q['whole_native_geometry_frames']} native frames evaluated, root range {d['root_range_m']}m, finite mesh. 실제 발바닥 vertex cohort와 near-floor phase proxy를 검사했으며 관절 전체 이동 범위를 sole slide FAIL로 오판하지 않음. 물리 contact/완전한 self-intersection/stance slip 인증은 HOLD. 세 시점 full movie decode와 UI normal1x ended/error-null 관찰 완료. Low sample 미리보기(A2 128x192, A3/A4 256x384)는 final-quality 판정 자료가 아님.

SEMANTICS: {r['semantics']}. Face/gaze/finger layer 신규 제작 없음.

FAILED/HOLD: 기존 A1 R1 pelvis channel 및 R2 support float는 수정 후 별도 R3 보존. A2 contact batch의 A3 duplicate preparation은 exclusive path 보호로 중복 실행 전 차단; 개별 A3/A4 native PASS와 구분. 이번 로컬 video metadata script의 HTML quoting syntax를 native 실행 전에 수정. A2 preview R2 COMBINED_OUTPUT_CAP 실패는 보존; R3 fresh128x192 preview는 동일 guard로 PASS. Saved OFF reopen R1 raw texture locator diff / R2 wrong-directory reference resolver FAIL 보존; R3 actual byte-identical bake source location으로 packed bytes/colorspace/resolved properties 및 모든 nontexture categories exact PASS. Raw filepath strings는 save-as remap이므로 byte-string identical이라고 주장하지 않음. Healthy render 중단/재시작 없음.

CAUSE/FIX: neutral/rest 바꾸지 않고 원본 pelvis Action channels에서 grounded support sole 높이만 보정. 수평 stepping은 강제 고정하지 않음.

NEXT: PM source-subset 리뷰 이후 Laptop 단일 consumer가 clip clock30/AlwaysAnimate/actual bone motion을 독립 검증. authored listen/loop 또는 최종 연기 품질로 승격하지 않음. 새로운 exporter/runtime/product writer 없음.

VISUAL_EVIDENCE: `{out}` (3 MP4, multiview grid, whole interval samples, OFF PNG); private bundle `{zpath}`, {custody['bytes']} bytes, SHA `{custody['sha256']}`. 공개 Git에는 분석 metadata와 workflow만 기록.
"""
 with (public/'SOURCE_CANDIDATE_R2_KO.md').open('x',encoding='utf8') as f:f.write(text)
 print(json.dumps(custody,indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('step',choices=['a2','a3','a4']);packet(ap.parse_args().step)
