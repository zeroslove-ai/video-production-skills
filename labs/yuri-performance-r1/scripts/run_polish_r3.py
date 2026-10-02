"""Bounded CPU blink and elbow experiments, separate immutable candidates."""
from pathlib import Path
import subprocess,json,hashlib,time,sys
ROOT=Path(__file__).resolve().parents[1]
BLENDER=r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
jobs=[('acting-r3-blink',c,'face_close','blink_hold') for c in ('greeting_wave','shy_lookaway','please_tilt')]
jobs += [('native-body-r3-please-elbow','please_tilt',c,'please_elbow') for c in ('hand_face','waist_threequarter')]
for folder,clip,camera,flag in jobs:
    e=ROOT/'evidence'/folder;out=ROOT/'local'/folder
    meta=json.loads((e/'build_receipt.json').read_text());candidate=Path(meta['candidate']);sha=hashlib.sha256(candidate.read_bytes()).hexdigest()
    proxy=folder.startswith('acting');receipt=e/('render_jobs.json' if proxy else 'video_jobs.json');state=json.loads(receipt.read_text()) if receipt.exists() else {'jobs':{}}
    state['candidate_sha256']=sha;key=f'{clip}__natural__{camera}' if proxy else f'{clip}__{camera}'
    script='render_acting_r2.py' if proxy else 'render_native_body_r3.py'
    cmd=[BLENDER,'--background','--factory-startup','--threads','4','--python-exit-code','1','--python',str(ROOT/'scripts'/script),'--','video',clip,camera,flag]
    log=out/(key+'.log');print('START',folder,key,flush=True);start=time.monotonic()
    with log.open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=420)
    assert hashlib.sha256(candidate.read_bytes()).hexdigest()==sha
    state['jobs'][key]={'clip':clip,'camera':camera,'variant':'natural','candidate_sha256':sha,'returncode':r.returncode,'command':cmd,'elapsed_seconds':time.monotonic()-start,'renderer':'CYCLES_CPU_4_THREADS','log':str(log)}
    receipt.write_text(json.dumps(state,indent=2));assert r.returncode==0
    package='package_acting_r2.py' if proxy else 'package_native_body_r3.py'
    subprocess.run([sys.executable,str(ROOT/'scripts'/package),flag],check=True)
    print('DONE',folder,key,flush=True)
