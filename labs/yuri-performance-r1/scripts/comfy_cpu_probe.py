"""Bounded CPU-only ComfyUI API probe; never submits inference or changes shared config."""
from pathlib import Path
import os, sys, json, time, socket, subprocess, urllib.request
ROOT=Path(__file__).resolve().parents[1]
INSTALL=Path(r'C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install')
PORT=8191

def get(route):
    with urllib.request.urlopen(f'http://127.0.0.1:{PORT}/{route}',timeout=3) as r:return json.load(r)

def main():
    ROOT.joinpath('evidence').mkdir(exist_ok=True)
    local=ROOT/'local'
    for n in ['input','output','user','temp']: (local/n).mkdir(parents=True,exist_ok=True)
    with socket.socket() as s:
        if s.connect_ex(('127.0.0.1',PORT))==0:raise RuntimeError('Port already occupied: refusing to adopt unknown server')
    cmd=[str(INSTALL/'python_embeded/python.exe'),str(INSTALL/'ComfyUI/main.py'),'--cpu','--listen','127.0.0.1','--port',str(PORT),'--disable-all-custom-nodes','--disable-api-nodes','--disable-auto-launch','--preview-method','none']
    for flag,d in [('user','user'),('input','input'),('output','output'),('temp','temp')]:cmd += ['--'+flag+'-directory',str(local/d)]
    env=dict(os.environ,CUDA_VISIBLE_DEVICES='-1',HIP_VISIBLE_DEVICES='-1')
    receipt={'status':'STARTING','cpu_only':True,'inference_submissions':0,'shared_config_changed':False,'endpoint':f'http://127.0.0.1:{PORT}','command':cmd,'time_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
    proc=None
    try:
        with (local/'comfy_probe.log').open('w',encoding='utf-8') as log:
            proc=subprocess.Popen(cmd,cwd=INSTALL/'ComfyUI',env=env,stdout=log,stderr=subprocess.STDOUT)
            receipt['owned_pid']=proc.pid
            deadline=time.monotonic()+85
            while time.monotonic()<deadline:
                if proc.poll() is not None:raise RuntimeError(f'ComfyUI exited {proc.returncode}')
                try: stats=get('system_stats');break
                except Exception:time.sleep(2)
            else:raise TimeoutError('CPU API startup exceeded 85 seconds')
            nodes=get('object_info')
            receipt.update(status='CPU_CORE_API_PASS',stats=stats,queue=get('queue'),node_count=len(nodes),relevant_nodes=sorted(n for n in nodes if any(t.lower() in n.lower() for t in ['Wan22','WanImageToVideo','UNETLoader','VAELoader','CLIPLoader','SaveVideo','CreateVideo'])))
            receipt['gpu_inference']='NOT_RUN_PRODUCT_EXCLUSIVE_LEASE'
            receipt['custom_nodes']='DISABLED_FOR_ISOLATED_PROBE_NOT_VALIDATED'
    except Exception as exc:
        receipt.update(status='CPU_API_PROBE_FAILED',error=str(exc))
    finally:
        if proc is not None and proc.poll() is None:
            proc.terminate()
            try:proc.wait(timeout=12)
            except subprocess.TimeoutExpired:proc.kill();proc.wait(timeout=5)
        receipt['owned_probe_process_stopped']=proc is None or proc.poll() is not None
        (ROOT/'evidence/comfy_cpu_probe.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        print(json.dumps(receipt,ensure_ascii=True))
    return 0 if receipt['status']=='CPU_CORE_API_PASS' else 1
if __name__=='__main__':sys.exit(main())
