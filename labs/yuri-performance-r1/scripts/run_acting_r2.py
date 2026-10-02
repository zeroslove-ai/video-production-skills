"""Sequential resumable CPU-only shots. One scene writer; zero video-model jobs."""
from pathlib import Path
import subprocess,json,time,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'local/acting-r2';E=ROOT/'evidence/acting-r2'
BLENDER=r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
candidate=OUT/'YURI_PERFORMANCE_ACTING_R2.blend';fingerprint=hashlib.sha256(candidate.read_bytes()).hexdigest()
jobs=[(clip,camera,'natural') for clip in ('greeting_wave','shy_lookaway','please_tilt') for camera in ('full_body','waist_threequarter','face_close','hand_face','vertical')]
jobs += [(clip,'face_close','exaggerated_head') for clip in ('greeting_wave','shy_lookaway','please_tilt')]
jobs += [('shy_lookaway','face_close','simultaneous')]
path=E/'render_jobs.json';state=json.loads(path.read_text()) if path.exists() else {'jobs':{}}
state['candidate_sha256']=fingerprint;state['classification']='DERIVED_PROXY_SHOTS_NOT_COMPLETED_YURI_PERFORMANCES'
start=time.monotonic()
for clip,camera,variant in jobs:
    key=f'{clip}__{variant}__{camera}';old=state['jobs'].get(key,{})
    d=OUT/clip/variant/camera
    if old.get('candidate_sha256')==fingerprint and old.get('returncode')==0 and all((d/f'{f:04d}.png').exists() for f in range(1,122)):
        print('RESUME_SKIP',key,flush=True);continue
    assert hashlib.sha256(candidate.read_bytes()).hexdigest()==fingerprint,'Candidate changed during render batch'
    cmd=[BLENDER,'--background','--factory-startup','--threads','4','--python-exit-code','1','--python',str(ROOT/'scripts/render_acting_r2.py'),'--','video',clip,camera,variant]
    log=OUT/(key+'.log');t=time.monotonic();print('START',key,flush=True)
    with log.open('w') as stream:
        result=subprocess.run(cmd,stdout=stream,stderr=subprocess.STDOUT,timeout=360)
    state['jobs'][key]={'clip':clip,'camera':camera,'variant':variant,'candidate_sha256':fingerprint,'command':cmd,'returncode':result.returncode,'elapsed_seconds':time.monotonic()-t,'frames':len(list(d.glob('*.png'))),'renderer':'CYCLES_CPU_4_THREADS','log':str(log)}
    path.write_text(json.dumps(state,indent=2));print('DONE',key,state['jobs'][key]['elapsed_seconds'],flush=True)
    if result.returncode:raise RuntimeError('Render failed; retain log and resume after correction')
subprocess.run([sys.executable,str(ROOT/'scripts/package_acting_r2.py')],check=True)
print('ALL_R2_SHOTS_DONE',time.monotonic()-start,flush=True)
