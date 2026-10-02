"""Bounded sequential CPU movies, stable candidates and explicit variant provenance."""
from pathlib import Path
import subprocess,json,hashlib,time,sys
ROOT=Path(__file__).resolve().parents[1];BLENDER=r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
phase='remaining' if 'remaining' in sys.argv else 'first'
cameras=('full_body','face_close','vertical') if phase=='remaining' else ('hand_face','waist_threequarter')
jobs=[(clip,cam,'please_hands' if clip=='please_tilt' else '') for clip in ('greeting_wave','shy_lookaway','please_tilt') for cam in cameras]
if phase=='first':jobs.append(('please_tilt','hand_face','')) # Before/after hand-strategy reference.
for clip,cam,revision in jobs:
    folder='native-body-r3-please-hands' if revision else 'native-body-r3';E=ROOT/('evidence/'+folder);OUT=ROOT/('local/'+folder)
    meta=json.loads((E/'build_receipt.json').read_text());candidate=Path(meta['candidate']);sha=meta['candidate_sha256']
    assert hashlib.sha256(candidate.read_bytes()).hexdigest()==sha
    qa=json.loads((E/'structural_qa.json').read_text());assert qa['candidate_sha256']==sha and all(c['technical']=='PASS' for c in qa['clips'])
    path=E/'video_jobs.json';state=json.loads(path.read_text()) if path.exists() else {'jobs':{}}
    key=f'{clip}__{cam}';d=OUT/clip/cam
    old=state['jobs'].get(key,{})
    if old.get('candidate_sha256')==sha and old.get('returncode')==0 and all((d/f'{f:04d}.png').exists() for f in range(1,122)):print('SKIP',key,revision,flush=True);continue
    existing=list(d.glob('*.png'))
    assert all(p.stat().st_mtime>=candidate.stat().st_mtime for p in existing),'Never mix stale candidate renders'
    cmd=[BLENDER,'--background','--factory-startup','--threads','4','--python-exit-code','1','--python',str(ROOT/'scripts/render_native_body_r3.py'),'--','video',clip,cam]
    if revision:cmd.append(revision)
    log=OUT/(key+'.log');start=time.monotonic();print('START',key,revision,flush=True)
    with log.open('w') as stream:result=subprocess.run(cmd,stdout=stream,stderr=subprocess.STDOUT,timeout=600)
    assert hashlib.sha256(candidate.read_bytes()).hexdigest()==sha
    state['jobs'][key]={'clip':clip,'camera':cam,'revision':revision or 'baseline','candidate_sha256':sha,'returncode':result.returncode,'elapsed_seconds':time.monotonic()-start,'frames':len(list(d.glob('*.png'))),'renderer':'CYCLES_CPU_4_THREADS','log':str(log),'command':cmd}
    path.write_text(json.dumps(state,indent=2));print('DONE',key,revision,state['jobs'][key]['elapsed_seconds'],flush=True)
    if result.returncode:raise RuntimeError('Preserve failed render log; correct before resume')
    package=[sys.executable,str(ROOT/'scripts/package_native_body_r3.py')]
    if revision:package.append(revision)
    subprocess.run(package,check=True)
print('NATIVE_PHASE_DONE',phase,flush=True)
