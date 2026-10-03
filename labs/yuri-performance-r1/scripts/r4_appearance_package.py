"""Encode native proof, document canonical authority, package a corrective bundle."""
import json,hashlib,shutil,subprocess,zipfile
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/r4-appearance-preserve-correction-r1')
E=ROOT/'evidence/r4-appearance-preserve-correction-r1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):
    for p in (OUT/'metadata'/name,E/name):p.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf8')
def load(n):return json.loads((E/n).read_text(encoding='utf8'))
assert load('append_diff.json')==load('reopen_diff.json')==load('on_off_diff.json')=={}
assert all(v['PASS'] for v in load('pixels_authority_source_camera.json').values())
assert all(v['PASS'] for v in load('pixels_full_body_QA.json').values())
videos=[]
for label,count in [('sequence',264),('strong_2cycles',96),('startle',36)]:
    assert len(list((OUT/'render_frames'/label).glob('*.png')))==count+1
    dest=OUT/f'{label}_24fps.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate','24','-start_number','1','-i',str(OUT/'render_frames'/label/'%04d.png'),'-frames:v',str(count),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(dest)],check=True)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(dest)]))
    stream=probe['streams'][0]
    assert int(stream['nb_read_frames'])==count and stream['r_frame_rate']=='24/1'
    subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],check=True)
    videos.append({'file':dest.name,'frames':count,'fps':24,'duration_seconds':float(probe['format']['duration']),'width':stream['width'],'height':stream['height'],'complete_decode':'PASS','normal_speed':True,'audio':'none; animation QA'})
write('video_receipt.json',videos)
retarget=json.loads((ROOT/'evidence/model-handoff-r4/retarget.json').read_text(encoding='utf8'))
mapping={'canonical_source':'source/Character_Master_NeckSkin_R4.blend','native_body_rig':'Meshy_Fitted_Rig','native_body_bones':57,'existing_face_rig':'Armature','existing_hair_rig':'Hair_Rig_R4','existing_face_board':'AVATAR_FaceBoard','bone_mapping_provenance':retarget['mapping'],'translation_height_ratio':retarget['translation_height_ratio'],'original_appearance_alteration':False,'action_asset':'YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend','adapter':'workflow/r4_appearance_adapter.py','adapter_scope':'Blender native original hierarchy ONLY; no Unity implementation','AlwaysAnimate':'MANDATORY future Unity import regression gate','Unity_state_weight_normalized_time':'PENDING external owner','GameRig_08caad7':'HISTORICAL COMPATIBILITY EXPERIMENT ONLY; not canonical character','states':['GROUNDED','GRABBED','LIFTED','AIRBORNE','IMPACT','RECOVERING','GROUNDED'],'clips':[]}
states=['GRABBED','LIFTED','AIRBORNE','AIRBORNE','IMPACT','RECOVERING']
for c,state in zip(load('all_frame_motion.json')['clips'],states):mapping['clips'].append({'logical_name':c['action'].replace('YRA_R4_','YRA_R1_'),'action':c['action'],'state':state,'loop':'Loop' in c['action'],'root_policy':'bounded authored local compression; external physical trajectory owned by future adapter','native_motion':c['native_motion']})
write('clip_mapping.json',mapping)
write('failure_correction_log.json',{'failures_preserved_in_code_and_receipts':[
    {'issue':'RGBA image pixels accidentally included in generic RNA fingerprint','effect':'read-only audit became expensive; no source changes','correction':'hash packed image bytes and colorspace; compare actual rendered pixels in a separate gate'},
    {'issue':'Blender library loader replaces assigned action-name list entries with Action IDs','effect':'build halted before save','correction':'assign list copy; retain immutable name list'},
    {'issue':'session_uid differs after reopening every Blender ID','effect':'false fingerprint mismatch; evaluated geometry unchanged','correction':'exclude transient session ID; retain all visual/hierarchy/driver checks'},
    {'issue':'ActionSlot uses identifier, not name, in Blender5.2','effect':'adapter binding halted','correction':'explicit OBMeshy_Fitted_Rig slot identifier'},
    {'issue':'Action ON then OFF retains last_slot_identifier cache','effect':'OFF pixels/geometry unchanged, but strict binding metadata differed','correction':'capture and restore slot handle and last_slot_identifier; strict ON/OFF fingerprint now identical'}],
    'new_motion_created':False,'new_geometry_created':False,'old_checkpoint_deleted_or_overwritten':False})
source=OUT/'source/Character_Master_NeckSkin_R4.blend'
assert sha(source)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
report='''# R4 Appearance Preserve Correction R1 — 2026-10-03

R4 외형의 유일한 authority는 `source/Character_Master_NeckSkin_R4.blend`다. 원본 파일 SHA256은 a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa이며 다운로드 원본과 byte-identical이다. 외형 승격이나 새로운 캐릭터 제작을 하지 않았다.

기존 08caad76e6a279d07698cbfaa33d5c50f2aa097d 및 이전 bundle/FBX/GameRig/master는 보존했다. 그 GameRig는 **structural/animation compatibility experiment ONLY**이며 canonical character로 사용하면 안 된다. 이 checkpoint가 원본 외형 보존 규칙을 추가한다.

| Acceptance | 결과 / 증거 |
|---|---|
| neutral geometry / topology / UV / attributes | 동일, append·save/reopen·ON→OFF hash diff={} |
| material slots / shaders / nodes / packed textures | 동일, 19 materials 유지 |
| ShapeKeys / expression drivers | 동일, 원본 head 72 keys 포함 |
| skin weights / modifier settings | 동일, source native DQ·GN·surface corrections 유지 |
| hierarchy / rest pose / bind helper pose | 동일, 원본 4 rigs / 97 objects 유지 |
| original Action curves | 원본 R4 78개 동일; R2 원본 66개 파일은 건드리지 않음 |
| animation OFF neutral pixels | 960×920 source camera + 256×384 full-body QA 모두 unequal RGBA channels=0, max diff=0 |
| ON→OFF neutral pixels | 위 두 구도 모두 exact 동일 |
| Action library | 6 physical + 2 existing QA Actions, geometry/rig/material/image 0개 |
| actual bone motion / loop | 6 clips 전 프레임 검사 PASS, Light/Strong 각각 2 cycles |
| Unity runtime / appearance | 미검증; 외형 승격 없음, AlwaysAnimate 필수 gate 유지 |

신규 GameRig/mesh merge/body substitution/donor geometry append는 0회다. 원본 R4가 이미 가지고 있는 얼굴·헤어 assembly와 gaze/face drivers를 그대로 사용한다. ON에서는 기존 Meshy_Fitted_Rig에 Action만 연결하고, OFF에서는 원래 pose channels, frame, action slot/binding metadata까지 복원한다. Blender Action/NLA 경로를 선택했고 새 캐릭터 FBX/VRM을 만들지 않았다.

정상속도 proof: `sequence_24fps.mp4` (11초: Lift_Start → Light 2 cycles → Release placeholder → Land_Soft → BalanceRecover), `strong_2cycles_24fps.mp4` (4초), `startle_24fps.mp4` (1.5초). 24fps의 실제 authored 시간을 유지하며 endpoint 중복 한 프레임만 encode에서 제외한다. 전체 PNG와 joint checks는 전 구간 기준이고 MP4 전체 decode를 검증한다. 큰 mesh explosion/face detachment/root teleport는 관찰되지 않았다. 낮은 preview sampling noise는 원본과 동일한 QA 렌더 설정이며 shader 수정으로 제거하지 않았다.

원본 source camera/조명/구도는 authoritative neutral PNG에서 유지한다. CPU Cycles 8 samples, seed=0, animated seed OFF, denoise OFF, RGBA8 PNG가 동일하게 적용된 QA overrides다. 별도 전신 camera/resolution 변경은 저장하지 않는 QA process에서만 적용했다. master는 원래 scene/render/camera 설정과 animation OFF 상태로 저장되어 있다. `neutral/authority_source_camera_before.png`를 기준으로 삼고 `metadata/pixels_*.json`의 decoded pixel SHA를 확인한다.

## 사용법

1. Blender 5.2에서 `Character_R4_Animation_OFF_20261003.blend`를 열면 원본 외형과 neutral/driver/binding 상태이고 reaction은 재생되지 않는다. 원본 R4 78 Actions + 추가 8 Actions만 존재한다.
2. 원본 파일에서 시작하려면 `YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend`의 Action datablocks만 Append한다. Object/Collection/Mesh/Armature/Material append나 rig rebuild는 금지한다.
3. Python Console에서 아래 adapter를 사용한다. source rigs/constraints/face/gaze drivers를 clear/reset/mute하지 않는다.

```python
import sys
sys.path.insert(0, r"<bundle>/workflow")
from r4_appearance_adapter import ReactionLane
lane = ReactionLane()
lane.on('YRA_R4_QA_MilestoneA_Sequence')
# Timeline 1..265, 24 fps로 재생. 24fps 설정은 QA session에서만 변경.
lane.off()  # source frame / pose / action slot 상태를 정확히 복원
```

adapter는 원본 hierarchy의 Blender playback용이다. Unity Runtime adapter를 구현했다고 주장하지 않는다. `metadata/clip_mapping.json`은 future IPhysicalAnimationLane 연결을 위한 mapping/data contract이며 Active Ragdoll 구현은 없다. Unity에서는 canonical source / animation-only asset / runtime adapter를 분리하고, state-entered / normalized-time / weight>0 / AlwaysAnimate / 실제 bone motion / mesh/root / loop2cycles를 해당 owner가 검사해야 한다. 제품 repo는 수정하지 않았다.

재현: workflow의 saved bpy scripts와 metadata receipts를 참고한다. authoring build/QA scripts는 이 Desktop 연구 workspace 경로를 기록하고, 휴대 가능한 playback은 위 Action library + adapter 경로다. 기존 foot cleanup·retarget curves를 다시 제작하지 않고 재사용했다. 검사 구현의 실패와 수정은 metadata/failure_correction_log.json에 남겼다.

다음 bounded experiment는 원본 authority와 분리된 Unity native animation-only import가 source shader/face/gaze adapter와 충돌하지 않는지 검증하는 것이다. Unity 외형 동일성이나 Humanoid/VRM 적합성은 이 Blender PASS에 포함되지 않는다.
'''
report_name='YURI_R4_APPEARANCE_PRESERVE_CORRECTION_R1.md'
(OUT/report_name).write_text(report,encoding='utf8')
(ROOT/'R4_APPEARANCE_PRESERVE_CORRECTION_R1_KO.md').write_text(report,encoding='utf8')
for name in ['r4_appearance_qa.py','r4_appearance_package.py']:
    shutil.copyfile(ROOT/'scripts'/name,OUT/'workflow'/name)
page='''<!doctype html><html lang="ko"><meta charset="utf-8"><title>R4 Appearance Preserve Correction</title><style>body{background:#151820;color:#eee;font:16px system-ui;margin:24px}video{max-height:70vh;background:#111}img{max-width:42vw}button{font-size:20px;margin:12px;padding:12px}section{margin:30px 0} .row{display:flex;gap:14px}</style><h1>R4 원본 외형 보존 / Action only</h1><p>08caad7 보존 · GameRig는 compatibility experiment ONLY · 외형 승격 없음 · neutral decoded pixels 차이=0 · Unity 미검증</p><div class="row"><img src="neutral/authority_source_camera_before.png"><img src="neutral/authority_source_camera_after_OFF.png"></div><p>왼쪽 original authority / 오른쪽 Actions appended, OFF. Shader/material/geometry 그대로.</p><button onclick="document.querySelectorAll('video').forEach(v=>{v.currentTime=0;v.play()})">전체 정상속도 proof 재생</button>'''
for v in videos:page+=f'<section><h2>{v["file"]} · {v["duration_seconds"]}s · 24fps</h2><video id="{v["file"].split("_")[0]}" controls preload="auto" src="{v["file"]}"></video></section>'
page+='<p><a href="YURI_R4_APPEARANCE_PRESERVE_CORRECTION_R1.md">검수 / 사용법 / 한계</a></p></html>'
(OUT/'REVIEW_R4_APPEARANCE_CORRECTION.html').write_text(page,encoding='utf8')
# Fixed before/after and representative ON proof, no shader alterations.
from PIL import Image,ImageOps,ImageDraw
frames=[OUT/'neutral/full_body_QA_before.png',OUT/'render_frames/sequence/0031.png',OUT/'render_frames/sequence/0091.png',OUT/'render_frames/sequence/0181.png',OUT/'render_frames/sequence/0265.png',OUT/'neutral/full_body_QA_after_ON_then_OFF.png']
grid=Image.new('RGB',(256*6,414),'#151820');draw=ImageDraw.Draw(grid)
for i,p in enumerate(frames):grid.paste(Image.open(p).convert('RGB'),(256*i,30));draw.text((256*i+8,8),['SOURCE OFF','LIFT','LIGHT cycle 1/2','LAND','RECOVER end','RESTORED OFF'][i],fill='white')
grid.save(OUT/'appearance_motion_proof_grid.png')
files=[]
for p in sorted(OUT.rglob('*')):
    if not p.is_file() or 'render_frames' in p.parts or p.suffix=='.blend1' or p.name in {'Character_R4_AssetManifest_CORRECTIVE.json','corrective_manifest.json','bundle_receipt.json'}:continue
    files.append({'path':p.relative_to(OUT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
manifest={'checkpoint':'R4_APPEARANCE_PRESERVE_CORRECTION_R1','created_utc':datetime.now(timezone.utc).isoformat(),'parent_checkpoint':'08caad76e6a279d07698cbfaa33d5c50f2aa097d','canonical_source':source.name,'source_sha256':sha(source),'appearance_promoted':False,'new_GameRig':False,'source_changes':0,'OFF_pixel_max_difference':0,'native_reactions':6,'Unity_validated':False,'files':files}
(OUT/'Character_R4_AssetManifest_CORRECTIVE.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
write('corrective_manifest.json',manifest)
print('R4_APPEARANCE_PACKAGE_READY',flush=True)
