"""Build private self-contained R4 handoff, metadata-only research checkpoint."""
import json,hashlib,shutil,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence/model-handoff-r4';L=ROOT/'local/model-handoff-r4';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/r4-model-handoff')
read=lambda n:json.loads((E/n).read_text(encoding='utf8'))
native=read('native_qa.json');final=read('final_native_receipt.json');fbx=read('fbx_roundtrip.json');export=read('game_export.json');retarget=read('retarget.json');surface=read('surface_compare.json')
assert all(x['skeleton_roundtrip']=='PASS' for x in fbx['clips'])
src=OUT/'source';src.mkdir(exist_ok=True);shutil.copy2(L/'Character_Master_NeckSkin_R4.blend',src/'Character_Master_NeckSkin_R4.blend')
meta=OUT/'metadata';meta.mkdir(exist_ok=True)
for p in E.glob('*.json'):shutil.copy2(p,meta/p.name)
if (E/'face-audit/calibration.json').exists():shutil.copy2(E/'face-audit/calibration.json',meta/'face_calibration.json')
methods=OUT/'workflow';methods.mkdir(exist_ok=True)
for p in (ROOT/'scripts').glob('r4_*.py'):shutil.copy2(p,methods/p.name)
for n in ['native_preservation.py','calibrate_r2_source_face.py']:shutil.copy2(ROOT/'scripts'/n,methods/n)
states={'Startle_Short':'GRABBED','Lift_Start':'LIFTED','Struggle_Light_Loop':'AIRBORNE','Struggle_Strong_Loop':'AIRBORNE','Land_Soft':'IMPACT','BalanceRecover':'RECOVERING'}
mapping={'contract':'IPhysicalAnimationLane clip-mapping data; exact C# interface source unavailable, no compilation claim','implementation':'animation-only research; no Active Ragdoll/product code','rig':'Generic / CHARACTER_NATIVE','culling_mode':'AlwaysAnimate REQUIRED','applyRootMotion':False,'world_root_owner':'IPhysicalAnimationLane / external interaction controller','skeletal_root':'RuntimeRoot stationary; child root compression preserved','state_graph':['GROUNDED','GRABBED','LIFTED','AIRBORNE','IMPACT','RECOVERING','GROUNDED'],'clips':[]}
for c in native['clips']:
 short=c['action'].removeprefix('YRA_R4_');mapping['clips'].append({'state':states[short],'source_action':'YRA_R1_'+short,'target_action':c['action'],'fbx_take':'GameRig_R4|'+c['action'],'duration_seconds':(c['frames_evaluated']-1)/24,'loop':'Loop' in short,'root_excursion_m':c['root_excursion_m'],'physics_pose_drive':'future consumer only; not implemented'})
(OUT/'IPhysicalAnimationLane_ClipMapping_R4.json').write_text(json.dumps(mapping,indent=2),encoding='utf8')
manifest={'status':'R4_NATIVE_REACTION_COMPATIBLE; FBX_SKELETON_ROUNDTRIP_PASS; UNITY_RUNTIME_UNTESTED; MATERIAL_PORT_PENDING','sources':{n:read(n+'.json')['source_sha256'] for n in ['R2','R3d','R4']},'incoming_r4_actions':78,'r2_original_66_actions':'Absent in incoming R4; archived unchanged into research master, not recreated or claimed R4-compatible','master_actions':166,'production_reaction_clips':6,'qa_helper_clips':2,'game_rig_bones':export['bone_count'],'game_rig_meshes':export['mesh_count'],'game_rig_shape_keys_head':fbx['shape_key_counts']['Character_Body_Head'],'game_rig_top_root':'RuntimeRoot','scale':{'native_fitted_object_scale':.535,'unit_length_scale':read('R4.json')['unit_scale'],'apply_unit_conversion':'FBX scale metadata; do not manually multiply by 100','rig_poses':'native target A-rest; source common performance neutral reference'},'candidate_sha256':final['candidate_sha256'],'normal_speed':{'fps':24,'sequence_seconds':11,'light_loop_cycles':2,'strong_loop_cycles':2,'startle_seconds':1.5,'full_playback_receipt':'metadata/playback_receipt.json'},'native_missing_textures':0,'extracted_texture_count':len(read('materials_textures.json')['textures']),'face_gate':'Neutral/blink/gaze sampled on R4; A/O approximate recipes remain visually weak, no phoneme certification','vrm':'Optional reference omitted; no new rights/license metadata invented','limitations':export['deformation_transfer_limits']+['Unity Generic import, clip weight, state-entered, normalized-time advance and AlwaysAnimate runtime gate still need laptop validation.'],'files':{}}
report='''# YURI_REACTION_R4_COMPAT_R1

R4 native Reaction 6개 재사용/retarget 및 GameRig FBX export를 완료했다. Unity 제품 repository는 수정하지 않았다. Unity runtime PASS는 주장하지 않는다.

## 원본 비교와 보존

- R4와 R3d의 4개 rig hierarchy/rest fingerprint 및 78 actions가 동일하다.
- R2 donor `Armature` 57 bones는 그대로 유지되지만 실제 R4 몸통은 `Meshy_Fitted_Rig` 57 bones, object scale .535에 묶여 있다. R2 clips를 donor rig에만 붙이는 방식은 몸통 재생 검증이 아니다.
- R4 얼굴 72 keys의 R3d 대비 expression delta 차이 0, z>.843 얼굴 정점 차이 0. 네크 geometry/weights와 피부 재질 변경은 incoming R4 그대로 보존했다.
- Incoming R4에는 R2의 기존 66 actions가 없다. 연구 master에 그 66개를 곡선 그대로 보관했다. 이 66개 전체의 R4 runtime 호환성을 인증한 것은 아니다.
- Polished Reaction 원본 6개, face/gaze와 QA helpers를 재사용했고 원본 곡선을 덮어쓰지 않았다. R4 파생 6개 + QA helpers 2개만 추가했다. master 총 166 actions.
- 최종 original R4 mesh/weights/ShapeKeys/rest 및 R4 78 + R2 66 action fingerprint 일치: PASS.

## 재생과 export

Source common neutral performance pose → R4 A-rest 기준으로 retarget. 본 길이를 target에 유지하고 pelvis/root translation을 hip height 기준으로 정규화했다. Grounded 구간만 target 길이의 2-bone IK로 발 접촉을 보정했다. 최대 발 미끄러짐 12.345mm → 0.2µm 미만.

Lift → Light 2 cycles → Release QA placeholder → Land → Recover 11초 / 24fps. Strong 2 cycles 4초, Startle 1.5초를 별도 정상속도 영상으로 제공한다. Release helper는 제작용 motion으로 세지 않는다.

'''
report+='| Clip | Native bone motion | Loop | Root excursion | FBX roundtrip |\n|---|---:|---|---:|---|\n'
for c in native['clips']:
 f=next(x for x in fbx['clips'] if x['action']==c['action']);report+=f"| {c['action']} | {c['actual_non_root_bone_motion_m']:.4f} m | {'2 cycles' if 'Loop' in c['action'] else 'one-shot'} | {c['root_excursion_m']:.4f} m | {f['max_world_joint_position_error_m']*1e6:.2f} µm |\n"
report+=f'''
Lift→Light pose delta {final['transitions'][0]['max_bone_position_difference_m']:.3g}m / 0°, Land→Recover 0m / 0°. 모든 clip의 actual non-root motion 및 시간별 포즈 변화 확인. Loop root 이동 0, 위치 seam 0.2µm 이하. Root 이동은 bounded skeletal compression이며 world teleport/fall을 구현하지 않는다.

단일 export GameRig: {export['bone_count']} bones / 21 meshes / head 72 ShapeKeys. Body, donor face, hair 3 rig의 평가된 motion을 bake하고, export 사본에서만 미사용 donor body bones를 제외했다. 원본 multi-rig master는 보존했다.

FBX 재입력의 6개 clip 전체 프레임 joint error 최대 {max(x['max_world_joint_position_error_m'] for x in fbx['clips'])*1e6:.2f}µm. Unity에서 AlwaysAnimate/state/weight/normalized time gate는 아직 미실행이다.

## 남은 결함 및 승격 범위

Blender의 DQ+masked LBS와 pose-dependent surface relaxation은 FBX standard LBS로 그대로 재현되지 않는다. 표본 몸통 정점 차이는 최대 {max(t['max_corresponding_vertex_difference_m'] for x in fbx['clips'] for t in x['sampled_skin_difference'])*1000:.2f}mm. Native gaze Geometry Nodes/driver 및 복잡한 눈·피부 node shader를 Unity 로직으로 이식하지 않았다. FBX 눈/피부 표현의 차이는 `comparison_24fps.mp4`에서 확인하고 원본 15 textures와 material node manifest로 복원해야 한다. R4 native appearance PASS와 Unity final appearance PASS를 구분한다.

R4 native blink L/R 및 gaze 응답을 검수했다. A/O approximate mouth shape는 시각적 구별이 약하며 phoneme/viseme PASS가 아니다. 기존 표정/눈썹/턱/입 데이터는 보존했으며 raw face mapping은 하지 않았다. 헤어 10 bones와 head-follow binding은 bake/reimport로 확인했으나 새 물리 hair simulation은 만들지 않았다.

VRM reference는 선택 산출물이어서 생략했다. FBX/packed master 전달이 우선이며, 신규 VRM license metadata를 임의로 만들지 않았다.

## 시행착오

1. T-rest delta를 target A-rest에 그대로 적용하면 팔이 몸 안으로 접혀 어깨가 부풀었다. 공통 neutral 연기 pose 보정으로 해결. rejected-rest-delta의 원본 실패 증거는 연구 로컬에 보존했다.
2. 3개 object scale(.535/1/1)를 단순 결합하면 bone scale/parent 변환이 중복된다. mesh world transform 보존, root rest-axis 및 scale 정규화, export-only connected/scale inheritance 처리로 보정했다.
3. Animation-only FBX를 첫 연기 pose에서 export하면 default node/bind transform이 master와 달라져 hair joint error가 59–73mm 발생했다. Action을 detach하고 모든 basis를 rest로 되돌린 뒤 all-action baking하면 전체 6개가 약 1µm 수준으로 일치한다.
4. Blender 5.2 multi-slot Action을 새 rig에 할당할 때 `action_slot`을 명시하지 않으면 active Action 이름만 있고 실제 재생은 0일 수 있다. roundtrip 검사에서 slot을 명시했다.

## 노트북 Unity Codex 전달 지침

1. Master FBX와 animation-only FBX를 Generic/native lane에 import한다. 동일 GameRig hierarchy/Avatar와 clips를 연결한다. `RuntimeRoot`와 `GameRig_R4` transform 계층을 유지한다.
2. `IPhysicalAnimationLane_ClipMapping_R4.json`의 매핑대로 animation-only graph를 연결한다. GROUNDED→GRABBED→LIFTED→AIRBORNE→IMPACT→RECOVERING→GROUNDED. 실제 interface source가 없으므로 C# 구현/컴파일 호환을 주장하지 않는 데이터 매핑이다.
3. Animator AlwaysAnimate 유지, applyRootMotion=false. World root/fall은 향후 physical lane 소유. Active Ragdoll 구현을 이식하지 않는다.
4. 모든 clip state entered / normalized time advance / weight>0 / 실제 non-root motion / no teleport / no gross mesh break 검증. Light/Strong 2 cycles. Blend 및 shader 복원 후 정상속도 전체 시퀀스를 재생한다.
5. Generic 경로 결과를 먼저 기록한다. Humanoid 변환은 blocker로 삼지 않는다. R2/R3d는 삭제·덮어쓰지 않는다.

`Character_Master_Reaction_R4_20261002.blend`는 원본 R4의 asset data와 기존 actions를 보존한 packed 연구 master다. `Character_GameRig_R4_20261002.blend`는 export 전용 파생물이다. `YURI_REACTION_R4_QA_SEQUENCE.fbx`는 검수 helper이며 production catalog의 6 clips에 포함하지 않는다.
'''
(OUT/'YURI_REACTION_R4_COMPAT_R1.md').write_text(report,encoding='utf8');(ROOT/'R4_MODEL_HANDOFF_R1_KO.md').write_text(report,encoding='utf8')
for p in OUT.rglob('*'):
 if not p.is_file() or any(x in p.parts for x in ['render_frames','fbx_sequence_frames','rejected-rest-delta']) or p.suffix=='.blend1' or p.name=='Character_R4_AssetManifest.json':continue
 manifest['files'][p.relative_to(OUT).as_posix()]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(OUT/'Character_R4_AssetManifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8');(E/'handoff_summary.json').write_text(json.dumps({k:v for k,v in manifest.items() if k!='files'},indent=2),encoding='utf8')
print('R4_PACKAGE_METADATA',len(manifest['files']),flush=True)
