"""Own isolated CPU ComfyUI; two model-free preprocessing jobs. No GPU inference.
Reuses the R1 probe startup contract; never touches shared input/output/config.
"""
from pathlib import Path
import os,json,time,socket,subprocess,urllib.request,shutil
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'local/acting-r2';E=ROOT/'evidence/acting-r2'
INSTALL=Path(r'C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install')
LOCAL=ROOT/'local/comfy-r2';PORT=8192
def api(route,data=None):
    req=urllib.request.Request(f'http://127.0.0.1:{PORT}/{route}',data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=10) as res:return json.load(res)
def main():
    with socket.socket() as probe:
        if probe.connect_ex(('127.0.0.1',PORT))==0:raise RuntimeError('Refuse unknown server on port')
    for d in ('input','output','temp','user'):(LOCAL/d).mkdir(parents=True,exist_ok=True)
    source=OUT/'greeting_wave/natural/hand_face/0001.png'
    shutil.copy2(source,LOCAL/'input/acting_first.png')
    cmd=[str(INSTALL/'python_embeded/python.exe'),str(INSTALL/'ComfyUI/main.py'),'--cpu','--listen','127.0.0.1','--port',str(PORT),'--disable-all-custom-nodes','--disable-api-nodes','--disable-auto-launch','--preview-method','none']
    for d in ('input','output','temp','user'):cmd+=['--'+d+'-directory',str(LOCAL/d)]
    env=dict(os.environ,CUDA_VISIBLE_DEVICES='-1',HIP_VISIBLE_DEVICES='-1')
    receipt={'question':'Can unchanged Blender first frame traverse local core image conditioning on CPU?','single_variable':'ImageScale interpolation: bicubic vs nearest-exact','fixed':['same source image','512x288','crop disabled','same core nodes'],'model_inference_submissions':0,'gpu_inference':0,'paid_calls':0,'jobs':[]}
    with (LOCAL/'run.log').open('w') as log:
        proc=subprocess.Popen(cmd,cwd=INSTALL/'ComfyUI',env=env,stdout=log,stderr=subprocess.STDOUT)
        try:
            deadline=time.monotonic()+85
            while time.monotonic()<deadline:
                if proc.poll() is not None:raise RuntimeError('Owned CPU server exited')
                try:receipt['system_stats']=api('system_stats');break
                except Exception:time.sleep(1)
            else:raise TimeoutError('CPU startup timeout')
            nodes=api('object_info');names=['LoadImage','ImageScale','SaveImage','UNETLoader','CLIPLoader','VAELoader','Wan22ImageToVideoLatent','KSampler','VAEDecode','CreateVideo','SaveVideo']
            (E/'comfy_node_schema.json').write_text(json.dumps({n:nodes.get(n) for n in names},indent=2))
            for method in ('bicubic','nearest-exact'):
                graph={'1':{'class_type':'LoadImage','inputs':{'image':'acting_first.png'}},'2':{'class_type':'ImageScale','inputs':{'image':['1',0],'upscale_method':method,'width':512,'height':288,'crop':'disabled'}},'3':{'class_type':'SaveImage','inputs':{'images':['2',0],'filename_prefix':'conditioning_'+method}}}
                (E/('comfy_image_'+method+'.json')).write_text(json.dumps(graph,indent=2))
                t=time.monotonic();job=api('prompt',{'prompt':graph,'client_id':'yuri-rnd-r2-cpu-only'})
                pid=job['prompt_id'];end=t+40
                while time.monotonic()<end:
                    h=api('history/'+pid)
                    if pid in h:break
                    time.sleep(.25)
                else:raise TimeoutError('Image conditioning exceeded 40s')
                record=h[pid];assert record['status']['status_str']=='success',record
                images=record['outputs']['3']['images'];assert images
                receipt['jobs'].append({'method':method,'prompt_id':pid,'elapsed_seconds':time.monotonic()-t,'images':images,'result':'CPU_IMAGE_GRAPH_PASS'})
            receipt['result']='MODEL_FREE_CONDITIONING_PASS; VIDEO_BENEFIT_UNTESTED'
        except Exception as exc:
            receipt['result']='FAIL';receipt['error']=str(exc)
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=8)
                except subprocess.TimeoutExpired:proc.kill();proc.wait(timeout=5)
            receipt['owned_pid']=proc.pid;receipt['owned_server_stopped']=proc.poll() is not None
    (E/'comfy_conditioning.json').write_text(json.dumps(receipt,indent=2))
    print(json.dumps({k:v for k,v in receipt.items() if k!='system_stats'}))
    if receipt['result']=='FAIL':raise RuntimeError(receipt['error'])
if __name__=='__main__':main()
