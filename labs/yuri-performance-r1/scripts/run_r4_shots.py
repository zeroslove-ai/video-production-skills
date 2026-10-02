"""Resumable selected native five-camera references and existing proxy overlay proof."""
from pathlib import Path
import subprocess,json,hashlib,time,sys
ROOT=Path(__file__).resolve().parents[1];BLENDER=r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
jobs=[('native-camera-r4',c,v,'camera_r4','natural') for c in ('greeting_wave','shy_lookaway','please_tilt') for v in ('waist_threequarter','full_body','face_close','hand_face','vertical')]
jobs += [('face-mix-r4','greeting_wave','hand_face','face_mix',v) for v in ('natural','shy_face','please_face')]
for folder,clip,camera,flag,variant in jobs:
    proxy=folder=='face-mix-r4';e=ROOT/'evidence'/folder;out=ROOT/'local'/folder;meta=json.loads((e/'build_receipt.json').read_text());candidate=Path(meta['candidate']);sha=hashlib.sha256(candidate.read_bytes()).hexdigest()
    if not proxy:
        qa=json.loads((e/'structural_qa.json').read_text());assert qa['candidate_sha256']==sha and all(x['technical']=='PASS' for x in qa['clips'])
    receipt=e/('render_jobs.json' if proxy else 'video_jobs.json');state=json.loads(receipt.read_text()) if receipt.exists() else {'jobs':{}};state['candidate_sha256']=sha
    key=f'{clip}__{variant}__{camera}' if proxy else f'{clip}__{camera}'
    frames=out/clip/variant/camera if proxy else out/clip/camera
    old=state['jobs'].get(key,{})
    if old.get('candidate_sha256')==sha and old.get('returncode')==0 and all((frames/f'{f:04d}.png').exists() for f in range(1,122)):print('RESUME_SKIP',key,flush=True);continue
    script='render_acting_r2.py' if proxy else 'render_native_body_r3.py';args=['video',clip,camera]+([variant] if proxy else [])+[flag]
    cmd=[BLENDER,'--background','--factory-startup','--threads','4','--python-exit-code','1','--python',str(ROOT/'scripts'/script),'--',*args]
    log=out/(key+'.log');print('START',folder,key,flush=True);start=time.monotonic()
    with log.open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=480)
    assert hashlib.sha256(candidate.read_bytes()).hexdigest()==sha
    state['jobs'][key]={'clip':clip,'camera':camera,'variant':variant,'candidate_sha256':sha,'returncode':r.returncode,'frames':len(list(frames.glob('*.png'))),'elapsed_seconds':time.monotonic()-start,'command':cmd,'renderer':'CYCLES_CPU_4_THREADS','log':str(log)};receipt.write_text(json.dumps(state,indent=2));assert r.returncode==0
    package='package_acting_r2.py' if proxy else 'package_native_body_r3.py';subprocess.run([sys.executable,str(ROOT/'scripts'/package),flag],check=True)
    print('DONE',folder,key,flush=True)
print('R4_BATCH_DONE',flush=True)
