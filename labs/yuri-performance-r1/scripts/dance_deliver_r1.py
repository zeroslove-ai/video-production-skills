"""Copy reviewable deliverables; never copy source video or model weights."""
from pathlib import Path
import json,shutil,hashlib,zipfile,datetime
R=Path(__file__).resolve().parents[1]; E=R/'evidence/dance-benchmark-r1';L=R/'local/dance-benchmark-r1'
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');D=OUT/'dance-benchmark-r1';D.mkdir(parents=True,exist_ok=True)
methods=['mediapipe','rtmw3d','motionbert']
config={'schema':'DANCE_RETARGET_R1','source_seconds':[20,26],'source_frame_start':1200,'frames':360,'fps':60,'preview_fps':30,'roi_xyxy':[1380,100,1840,1020],'mirror':'preserve displayed mirrored source; no horizontal flip','actor_height_assumed_m':1.65,'focal_assumed_px':1700,'camera':'selected2Dbackgroundstatic only; no6DOF estimate','world_root_depth':'unresolved, held constant','floor':'heuristic normalized floor; metric calibration unresolved','target_rig':'original procedural ProxyHumanoid,17bones','target_shoulder_width_m':.4,'target_hip_width_m':.2,'root_scale':'target thigh+shin / median source hip-knee-ankle summed length','arms':'normalized positions at target per-bone lengths','legs':'positional IK, image-derived stance goals, knee pole continuity','twist':'parallel transport; wrist orientation neutral','head':'2Deye-line roll only; yaw/pitch unresolved','face':'none','cleanup':'see dance_clean_r1.py; preserve raw; contact heuristic, conservative image smoothing, depth filtering, foot lock, direction repairs logged','export':'GLB one skin17joints one Animation51channels; Blender60fps baked action','methods':{m:json.loads((E/(m+'_retarget.json')).read_text()) for m in methods},'acceptance':'FAIL_CHOREOGRAPHY_ACCURACY; export technical pass'}
(E/'retarget_config.json').write_text(json.dumps(config,indent=2),encoding='utf-8')
(E/'playback_receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'comparison_sha256':json.loads((E/'delivery_receipt.json').read_text())['comparison_sha256'],'browser_video':{'currentTime':6,'duration':6,'ended':True,'playbackRate':1},'scope':'entire6sec1x browser playback plus all360frame structural/trajectory diagnostics','visual_verdict':'FAIL accurate dance; residual arm/hand/knee/depth deviations','mcp_live_inspect':{'candidate':'motionbert_DANCE_R1.blend','frame':181,'bones':17,'saved':False},'gpu_lease':'PRODUCT_EXCLUSIVE preserved; CPU-only; RTX4080SUPER observed2876MiB/5percent; no GPU inference'},indent=2))
for p in E.iterdir():
    if p.is_file():dest=D/'evidence'/p.name;dest.parent.mkdir(exist_ok=True);shutil.copy2(p,dest)
shutil.copy2(R/'DANCE_BENCHMARK_R1_KO.md',D/'README_KO.md')
for m in methods:
    for suffix in ['_DANCE_R1.blend','_DANCE_R1.glb','_raw.npz','_motion.npz','_retarget.mp4']:shutil.copy2(L/(m+suffix),D/(m+suffix))
for name in ['comparison_6sec.mp4','comparison_contact.jpg','REVIEW_DANCE_R1.html','reference_overview.jpg','dance_start_end_contact.jpg','manual_joint_annotation_grid.jpg']:shutil.copy2(L/name,D/name)
scripts=D/'scripts';scripts.mkdir(exist_ok=True)
for p in (R/'scripts').glob('dance_*.py'):shutil.copy2(p,scripts/p.name)
shutil.copy2(R/'local/output/YURI_PERFORMANCE_PROXY_R1.blend',D/'YURI_PERFORMANCE_PROXY_R1.blend')
index=[]
for p in sorted(D.rglob('*')):
    if p.is_file() and p.name!='SHA256SUMS.json':index.append({'path':p.relative_to(D).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(D/'SHA256SUMS.json').write_text(json.dumps(index,indent=2))
archive=OUT/'DANCE_BENCHMARK_R1.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in D.rglob('*'):
        if p.is_file():z.write(p,'dance-benchmark-r1/'+p.relative_to(D).as_posix())
assert not any('reference.mp4' in x['path'] or 'models/' in x['path'] for x in index)
print(json.dumps({'files':len(index)+1,'zip':str(archive),'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}))
