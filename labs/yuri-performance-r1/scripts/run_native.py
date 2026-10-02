"""Run owned headless Blender with real return code; warnings are not fatal shell errors."""
from pathlib import Path
import subprocess, sys, json, time
ROOT=Path(__file__).resolve().parents[1]
BLENDER=r'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
cmd=[BLENDER,'--background','--factory-startup','--threads','4','--python-exit-code','1','--python',str(ROOT/'scripts/build_previs.py'),'--','--render']
if '--reel' in sys.argv:cmd.append('--reel')
log=ROOT/'local/build_previs.log'
t0=time.monotonic()
with log.open('w',encoding='utf-8') as out:
    result=subprocess.run(cmd,stdout=out,stderr=subprocess.STDOUT,timeout=220)
receipt={'command':cmd,'returncode':result.returncode,'elapsed_seconds':round(time.monotonic()-t0,2),'log':str(log),'gpu':'NOT_USED_CPU_ONLY'}
(ROOT/'evidence/native_execution.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(log.read_text(encoding='utf-8',errors='replace')[-4200:])
print(json.dumps(receipt))
sys.exit(result.returncode)
