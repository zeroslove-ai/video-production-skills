"""Finalize measured compatibility blocker, proof videos and immutable custody ZIP.
Run after both visual jobs complete. No original source/old artifact overwrite.
"""
from pathlib import Path
import json,hashlib,shutil,subprocess,zipfile,gzip
from PIL import Image,ImageDraw
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;E=ROOT/'evidence/o1-native-unity-probe-r1'
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-native-unity-probe-r1')
OLD=OUT.parent/'r4-appearance-preserve-correction-r1';SOURCE=ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def load(n):return json.loads((E/n).read_text(encoding='utf8'))
def write(n,v):
    for p in (E/n,OUT/'metadata'/n):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
def command(args):
    result=subprocess.run(args,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    if result.returncode:raise RuntimeError(result.stderr.decode('utf8',errors='replace')[-2500:])
font=Path('labs/yuri-performance-r1/local/o1-native-unity-probe-r1/arial.ttf')
shutil.copyfile(Path('C:/Windows/Fonts/arial.ttf'),font)
for mode in ('native','imported'):
    schedule=load(mode+'_visual_schedule.json');count=sum(v['video_frames'] for v in schedule)
    assert count==378
    assert len(list((OUT/'visual'/mode).glob('frame_*.png')))==count
    command(['ffmpeg','-y','-framerate','24','-i',str(OUT/'visual'/mode/'frame_%04d.png'),'-frames:v',str(count),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(OUT/'visual'/f'{mode}_six_clips_24fps.mp4')])
command(['ffmpeg','-y','-i',str(OUT/'visual/native_six_clips_24fps.mp4'),'-i',str(OUT/'visual/imported_six_clips_24fps.mp4'),'-filter_complex',f'[0:v]pad=iw:ih+24:0:24:color=black,drawtext=fontfile={font.as_posix()}:text=SOURCE_R4_NATIVE:x=4:y=4:fontcolor=white:fontsize=12[a];[1:v]pad=iw:ih+24:0:24:color=black,drawtext=fontfile={font.as_posix()}:text=ACTUAL_FBX_HOLD:x=4:y=4:fontcolor=white:fontsize=12[b];[a][b]hstack=inputs=2','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(OUT/'visual/source_vs_actual_FBX_24fps.mp4')])
probes={}
for mode in ('native','imported'):
    p=OUT/'visual'/f'{mode}_six_clips_24fps.mp4';result=subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=r_frame_rate,avg_frame_rate,nb_read_frames,duration','-of','json',str(p)],text=True);v=json.loads(result)['streams'][0]
    assert int(v['nb_read_frames'])==378 and v['avg_frame_rate']=='24/1';probes[mode]=v
def pixels(a,b):
    aa=np.array(Image.open(a).convert('RGBA'));bb=np.array(Image.open(b).convert('RGBA'));d=np.abs(aa.astype(int)-bb.astype(int))
    return {'dimensions':list(Image.open(a).size),'unequal_channels':int(np.count_nonzero(d)),'mean_absolute_8bit_channel_difference':float(d.mean()),'maximum_8bit_channel_difference':int(d.max()),'PASS':bool(not np.any(d))}
visual={'native_vs_frozen_authority':pixels(OLD/'neutral/authority_source_camera_before.png',OUT/'visual/native/neutral_source_camera.png'),'native_vs_actual_FBX':pixels(OUT/'visual/native/neutral_source_camera.png',OUT/'visual/imported/neutral_source_camera.png'),'render':'CPU Cycles8 samples/seed0/no denoise; source camera960x920; same original world/lights; no original character shader or modifier copied into FBX side','video_probes':probes,'full_duration_seconds':15.75,'normal_speed':'378 consecutive frames at24fps; both loops2cycles; six diagnostic clips separated by cuts, not milestone sequence or Unity state graph PASS'}
assert visual['native_vs_frozen_authority']['PASS'];write('visual_pixel_video_receipt.json',visual)
# Contact sheet is supplemental; every rendered frame and every sampled bone
# frame is covered by the videos and data. No first/middle/last-only gate.
sheet=Image.new('RGB',(768,6*180),(28,28,32));draw=ImageDraw.Draw(sheet)
for row,c in enumerate(load('native_visual_schedule.json')):
    first=c['first_video_frame'];length=c['video_frames'];draw.text((4,row*180+2),c['action'],fill='white')
    for col,fraction in enumerate((0,.25,.5,.99)):
        index=first+min(length-1,round((length-1)*fraction))
        for offset,mode in enumerate(('native','imported')):
            im=Image.open(OUT/'visual'/mode/f'frame_{index:04d}.png').convert('RGB');im.thumbnail((96,144));sheet.paste(im,(col*192+offset*96,row*180+24))
sheet.save(OUT/'visual/clip_contact_sheet.png')
pair=load('pair_path_rest_comparison.json');motion=load('motion_position_rotation_fidelity.json');geo=load('motion_deformation_comparison.json');weights=load('skin_weight_roundtrip_comparison.json')
previous=load('roundtrip_motion.json');byname={r['action']:r for r in motion['clips']}
for row in previous:
    r=byname[row['action']];row['legacy_Quaternion_angle_measurement_superseded']=True
    row['max_source_world_rotation_error_deg_by_rig']={n:v['rotation_deg'] for n,v in r['by_rig'].items()}
    row['source_pose_fidelity']='PASS' if r['PASS'] else 'FAIL'
    row['source_pose_fidelity_criteria']={'position_m':1e-4,'rotation_deg':.001,'rotation_method':'normalized quaternion dot in Python double'}
write('roundtrip_motion.json',previous)
# First measurement counted omitted zero entries as missing group entries.
# Max numeric influence error is0, so classify these explicitly as zero only.
for w in weights:
    w['missing_zero_weight_group_entries']=w['missing_influenced_bones'] if w['max_skin_bone_influence_delta']==0 else []
    if w['max_skin_bone_influence_delta']==0:w['missing_influenced_bones']=[]
write('skin_weight_roundtrip_comparison.json',weights)
worst=max((dict(action=c['action'],frame=c['frame'],**r) for c in geo for r in c['mesh_errors']),key=lambda r:r.get('max_corresponding_vertex_delta_m',0))
summary={'disposition':'PROBE_COMPLETE / PROMOTION_HOLD / NOT_CANONICAL','source_preservation_PASS':True,'source_components_changed':0,'native_authority_pixel_PASS':True,'native_OFF_ON_OFF_geometry_delta_m':load('native_visual_geometry_receipt.json')['OFF_ON_OFF_max_geometry_delta_m'],'original_actions_preserved':78,'body_bones':57,'total_original_rig_bones':137,'six_actual_motion_PASS':True,'two_loop_cycles_PASS':True,'pair_static_contract_PASS':False,'position_rotation_combined_fidelity_PASS':motion['PASS'],'max_joint_position_error_m':max(c['max_position_error_m'] for c in motion['clips']),'max_rotation_error_deg':max(c['max_rotation_error_deg_double_dot'] for c in motion['clips']),'rotation_budget_degrees':.001,'worst_evaluated_motion_geometry':worst,'max_numeric_skin_bone_weight_difference':max(r['max_skin_bone_influence_delta'] for r in weights),'carrier_visual_pixel_PASS':False,'Unity_PASS':False,'source_SHA256':sha(SOURCE),'Action_library_SHA256':sha(OLD/'YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'),'prior_checkpoints_preserved':['08caad76e6a279d07698cbfaa33d5c50f2aa097d','820a23791d17838b101296b50c87fd7564db791f','62f2e6b800e2aac4bda41c5341155c385c0b2f01']}
assert summary['source_SHA256']=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa';write('PROBE_DISPOSITION.json',summary)
report=f'''# O1 R4 native export compatibility probe R1

**Completed bounded experiment; appearance/Unity promotion HOLD.** Source R4 remains the immutable visual authority. This carrier is a compatibility test, never a canonical character or replacement GameRig. No product repo, shared Blender GUI, old artifacts, source mesh/material/weights/rest/driver changes.

## Accepted source evidence

Source SHA256 `{summary['source_SHA256']}` unchanged. Before/after exporter component diff={{}}; all78 original Actions retained. No new rig or geometry, no merge/prune/donor substitution. Original4rigs:57body +57face +10hair +13board.51 consumer semantic paths match native paths as metadata only. Source scale0.535 applied once, no second height normalization.

Native OFF→ON→OFF geometry delta0m for21 meshes. Fresh source neutral render versus frozen authority:0 unequal pixel channels (960×920). Shader, material slots, ShapeKeys, weights, rest and drivers preserved in native authoring. Existing action-only library reused, not regenerated.

## Motion and rest gates

All6 clips actually move nonroot bones; Light/Strong sampled2cycles. Root excursions remain original authored compression (0–0.033m), no gravity trajectory. Six FBX stacks,24fps, durations1.5/1.25/2.5/2/1.75/2.25s. Export uses original source OBJECT slot OBMeshy_Fitted_Rig; Blender import creates generic OBSlot bound explicitly by exported object+take. QA Release/sequence not exported.

Position error max {summary['max_joint_position_error_m']:.9g}m; rotation error max {summary['max_rotation_error_deg']:.9g}° using normalized quaternion dot in Python double. Combined position<1e-4m AND rotation<0.001° **FAIL**, independently of actual motion PASS. Earlier Quaternion.angle reported0° due float resolution; this has been corrected, tolerance not loosened.

Ordered names/parents/counts match model and motion. Local-rest matrix gate1e-5 **FAIL**: body thigh.L max1.138448715e-5 (scale delta1.132488251e-5); face J_Bip_L_Index3 max4.565156996e-5, translation2.504889911e-7m, rotation0.003331253°. Worst animation rotation also that face index bone. Full source/model/animation world/local TRS differences perbone in rest_matrix_decomposed_by_bone.json. Small neutral bind effect is measured below; this does not waive static contract. Serialized default properties themselves differ, not merely importer reconstruction; identical settings/axis/unit/parents do not imply identical floating defaults. Some missing versus explicit identity properties also differ harmlessly and are shown unfiltered in wire evidence.

## Exact carrier defects

Neutral geometry max corresponding vertex error ~2.81e-7m, all21 mesh counts equal. Numeric skin bone influence error0; omitted zero entries and procedural mask groups declared separately. Mesh/ShapeKey/material slot counts retained (see permesh report); FBX material graphs are not native graphs.

Same camera/lights/world, actual FBX materials and deformation: {visual['native_vs_actual_FBX']['unequal_channels']} unequal RGBA8 channels, mean error {visual['native_vs_actual_FBX']['mean_absolute_8bit_channel_difference']:.9g}/255. Visible eye iris/gaze material loss, washed face/hair shading. **Visual FAIL.** No source shader/modifier was copied into the imported carrier to hide this failure.

Motion mesh worst {worst['max_corresponding_vertex_delta_m']:.9g}m on {worst['mesh']} in {worst['action']} frame{worst['frame']}. Native DQ + masked second LBS + corrective/smooth stack becomes conventional FBX skinning. Gaze Geometry Nodes, expression/hair driver logic, board-driven morph behavior and arbitrary shader graphs are not executable FBX content. Bone follower motion is evaluated/baked for these6 takes only; this does not recreate future constraints/driver behavior. Deformation difference is a combined measured effect; individual causal contributions have not been isolated.

## Playback evidence and boundary

visual/source_vs_actual_FBX_24fps.mp4: left native / right actual FBX,15.75s,378frames24fps. Full interval rendered for6 clips and2 loop cycles each, no speed remap/interpolation. Perclip hard cuts are intentional diagnostic segmentation; no smooth sequence or runtime state graph acceptance claimed. Both full native/imported videos included. Contact sheet supplements complete videos and all-frame bone checks. CPU only; GPU PRODUCT_EXCLUSIVE untouched. Unity state entered/normalizedTime/weight/AlwaysAnimate/actual mesh playback **PENDING consumer test**, never Unity PASS.

## Narrow next adapter requirement

Consumer/PM should decide a source-preserving runtime adapter contract before another export: resolve exact rest/default matrix and bind representation, keep4native hierarchy/137bones/nondeform helpers, evaluate future face/gaze/hair board logic, preserve source material appearance and DQ/masked skin behavior. No new GameRig/geometry, source rig edits or silent shader replacement. If Unity cannot execute these original procedures faithfully, remain HOLD and retain Blender Action/NLA as canonical animation path. This worker stops at this bounded probe; no next production task.

## Reproduction

Fresh Blender5.2.1 LTS `--factory-startup --background --disable-autoexec --python-exit-code 1`; run export, roundtrip, wire, matrix_analysis, visual(native), visual(imported), package scripts in order. Scripts are in scripts/; original immutable source and action library are in source/. Adjust script absolute OUT path on another host. Native source never saved. Consumer intake refs8a1bba98/825a7f87 and PM reporting037b1f40 recorded; latest reporting addendum2d828a81 used for structured checkpoint. Failures: initial importer exact source Action-slot expectation rejected because imported slot is generic OBSlot; explicit target+slot fixed in scratch data only. Static/rotation/procedural failures retained, no threshold relaxation or corrective character rebuild.
'''
for p in (E/'YURI_O1_NATIVE_UNITY_PROBE_R1.md',OUT/'README.md'):p.write_text(report,encoding='utf8')
(OUT/'source').mkdir(exist_ok=True);(OUT/'scripts').mkdir(exist_ok=True)
for src in (SOURCE,OLD/'YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'):
    dst=OUT/'source'/src.name
    if dst.exists():assert sha(dst)==sha(src)
    else:shutil.copyfile(src,dst)
for pattern in ('r4_o1_native_probe_*.py','r4_appearance_adapter.py','r4_appearance_signature.py'):
    for p in HERE.glob(pattern):shutil.copyfile(p,OUT/'scripts'/p.name)
# Include exact consumer/PM inputs without writing to those repositories.
for p in (ROOT/'local/o1-native-unity-probe-r1/intake').glob('*'):
    target=OUT/'intake'/p.name;target.parent.mkdir(exist_ok=True);shutil.copyfile(p,target)
files=[p for p in sorted(OUT.rglob('*')) if p.is_file() and not(p.name.startswith('frame_') or p.name in ('PACKAGE_HASH_MANIFEST.json','PACKAGE_RECEIPT.json'))]
manifest={'scope':'O1 native compatibility probe; immutable source included; HOLD','files':[{'path':p.relative_to(OUT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files]}
(OUT/'PACKAGE_HASH_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf8');files.append(OUT/'PACKAGE_HASH_MANIFEST.json')
archive=OUT.parent/'YURI_O1_R4_NATIVE_UNITY_PROBE_20261003_R1.zip';assert not archive.exists(),'immutable archive already exists; use explicit new version'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in files:z.write(p,p.relative_to(OUT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for p in manifest['files']:assert hashlib.sha256(z.read(p['path'])).hexdigest()==p['sha256']
h=sha(archive);dest=Path('C:/YuriTransfer/outbox')/f'YURI_O1_R4_NATIVE_UNITY_PROBE_20261003_R1_{h[:12]}.zip';assert not dest.exists();shutil.copyfile(archive,dest);assert sha(dest)==h
dest.chmod(0o444)
receipt={'archive':str(dest),'sha256':h,'bytes':dest.stat().st_size,'members':len(files),'CRC_and_member_hashes_verified':True,'model':load('export_receipt.json')['model'],'animation':load('export_receipt.json')['animation'],'disposition':summary['disposition'],'Unity_PASS':False}
write('PACKAGE_RECEIPT.json',receipt);(OUT/'PACKAGE_RECEIPT.json').write_text(json.dumps(receipt,indent=2),encoding='utf8');dest.with_suffix('.receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf8')
print(json.dumps(receipt,indent=2))
