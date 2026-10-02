"""Standalone review bundle with R1 bases and R2 positional arm experiments."""
from pathlib import Path
import json,shutil,hashlib,zipfile,datetime
R=Path(__file__).resolve().parents[1];E=R/'evidence/dance-benchmark-r1';L=R/'local/dance-benchmark-r1';O=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');D=O/'dance-benchmark-r2';D.mkdir(exist_ok=True)
for p in E.iterdir():
    if p.is_file():q=D/'evidence'/p.name;q.parent.mkdir(exist_ok=True);shutil.copy2(p,q)
for report,name in [('DANCE_REPROJECTION_R2_KO.md','README_KO.md'),('DANCE_BENCHMARK_R1_KO.md','R1_BASELINE_KO.md')]:shutil.copy2(R/report,D/name)
for m in ['mediapipe','rtmw3d','motionbert','motionbert_reprojection','motionbert_reprojection_stable']:
    for suffix in ['_DANCE_R1.blend','_DANCE_R1.glb','_raw.npz','_motion.npz','_retarget.mp4']:
        p=L/(m+suffix)
        if p.exists():shutil.copy2(p,D/p.name)
for name in ['reprojection_comparison_6sec.mp4','reprojection_comparison_poster.jpg','silhouette_compare_6sec.mp4','silhouette_compare_poster.jpg','REVIEW_DANCE_R2.html','heldout_wrist_grid_0.png','heldout_wrist_grid_1.png','wrist_occlusion_24_5.png']:shutil.copy2(L/name,D/name)
scripts=D/'scripts';scripts.mkdir(exist_ok=True)
for p in (R/'scripts').glob('dance_*.py'):shutil.copy2(p,scripts/p.name)
shutil.copy2(R/'local/output/YURI_PERFORMANCE_PROXY_R1.blend',D/'YURI_PERFORMANCE_PROXY_R1.blend')
index=[{'path':p.relative_to(D).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(D.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.json'];(D/'SHA256SUMS.json').write_text(json.dumps(index,indent=2));archive=O/'DANCE_BENCHMARK_R2.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in D.rglob('*'):
        if p.is_file():z.write(p,'dance-benchmark-r2/'+p.relative_to(D).as_posix())
assert not any('reference.mp4' in p['path'] or 'models/' in p['path'] for p in index);print(json.dumps({'files':len(index)+1,'zip':str(archive),'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}))
