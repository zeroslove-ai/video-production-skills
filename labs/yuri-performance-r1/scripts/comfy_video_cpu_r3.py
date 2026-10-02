"""Model-free CPU VIDEO roundtrip and SaveVideo API compatibility experiment.
Read the existing installed nodes_video.py; own directories/port/process only.
No video-model loader, inference, custom/API nodes, GPU, update or download.
"""
from pathlib import Path
import os,json,time,socket,subprocess,urllib.request,urllib.error,shutil,hashlib
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence/comfy-video-r3';E.mkdir(parents=True,exist_ok=True)
LOCAL=ROOT/'local/comfy-video-r3';PORT=8192
INSTALL=Path(r'C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install')
SOURCE=ROOT/'local/acting-r2/greeting_wave__natural__hand_face.mp4'
def api(route,data=None):
    request=urllib.request.Request(f'http://127.0.0.1:{PORT}/{route}',data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(request,timeout=10) as response:return json.load(response)
def main():
    with socket.socket() as probe:
        if probe.connect_ex(('127.0.0.1',PORT))==0:raise RuntimeError('Unknown server on owned test port; refuse reuse')
    for d in ('input','output','temp','user'):(LOCAL/d).mkdir(parents=True,exist_ok=True)
    shutil.copy2(SOURCE,LOCAL/'input/blender_previs.mp4')
    cmd=[str(INSTALL/'python_embeded/python.exe'),str(INSTALL/'ComfyUI/main.py'),'--cpu','--listen','127.0.0.1','--port',str(PORT),'--disable-all-custom-nodes','--disable-api-nodes','--disable-auto-launch','--preview-method','none']
    for d in ('input','output','temp','user'):cmd+=['--'+d+'-directory',str(LOCAL/d)]
    env=dict(os.environ,CUDA_VISIBLE_DEVICES='-1',HIP_VISIBLE_DEVICES='-1',OMP_NUM_THREADS='4',MKL_NUM_THREADS='4')
    receipt={'question':'Can existing core VIDEO nodes preserve Blender clip duration/order on isolated CPU, and does legacy SaveVideo JSON still validate?','source':str(SOURCE),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'fixed':'same video, frames, 24fps, SDR8, codec auto; SaveVideo argument paths only differ','model_inference_jobs':0,'gpu_inference':0,'jobs':[]}
    with (LOCAL/'server.log').open('w') as log:
        process=subprocess.Popen(cmd,cwd=INSTALL/'ComfyUI',env=env,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            deadline=time.monotonic()+85
            while time.monotonic()<deadline:
                if process.poll() is not None:raise RuntimeError('Owned server exited')
                try:receipt['system_stats']=api('system_stats');break
                except Exception:time.sleep(1)
            else:raise TimeoutError('CPU startup timeout')
            nodes=api('object_info');names=('LoadVideo','GetVideoComponents','CreateVideo','SaveVideo')
            assert all(n in nodes for n in names)
            (E/'node_schema.json').write_text(json.dumps({n:nodes[n] for n in names},indent=2))
            for label,settings in [('legacy',{'format':'auto','codec':'auto'}),('dynamic',{'format':'auto','format.codec':'auto'})]:
                graph={'1':{'class_type':'LoadVideo','inputs':{'file':'blender_previs.mp4'}},'2':{'class_type':'GetVideoComponents','inputs':{'video':['1',0]}},'3':{'class_type':'CreateVideo','inputs':{'images':['2',0],'fps':['2',2],'bit_depth':8,'color_space':'sRGB'}},'4':{'class_type':'SaveVideo','inputs':{'video':['3',0],'filename_prefix':'roundtrip_'+label,**settings}}}
                (E/(label+'_graph.json')).write_text(json.dumps(graph,indent=2))
                t=time.monotonic();record={'argument_style':label}
                try:
                    response=api('prompt',{'prompt':graph,'client_id':'yuri-rnd-model-free-video-cpu'});pid=response['prompt_id'];end=t+60
                    while time.monotonic()<end:
                        history=api('history/'+pid)
                        if pid in history:break
                        time.sleep(.25)
                    else:raise TimeoutError('CPU video graph exceeded 60s')
                    h=history[pid];record.update(prompt_id=pid,status=h['status'],outputs=h['outputs']);assert h['status']['status_str']=='success',h['status']
                    output=h['outputs']['4']['images'][0];path=LOCAL/'output'/output['subfolder']/output['filename']
                    probe=json.loads(subprocess.check_output([shutil.which('ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(path)]));stream=probe['streams'][0]
                    assert abs(float(probe['format']['duration'])-5)<.01 and stream['avg_frame_rate']=='24/1' and int(stream['nb_frames'])==120
                    record.update(result='CPU_VIDEO_ROUNDTRIP_TECHNICAL_PASS',file=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),duration=5,fps=24,frames=120)
                except urllib.error.HTTPError as error:record.update(result='VALIDATION_REJECTED',error=json.loads(error.read().decode()))
                except Exception as error:record.update(result='FAIL',error=str(error))
                record['elapsed_seconds']=time.monotonic()-t;receipt['jobs'].append(record)
            assert receipt['jobs'][-1]['result']=='CPU_VIDEO_ROUNDTRIP_TECHNICAL_PASS'
            receipt['result']='CORE_VIDEO_CPU_PASS; MODEL_GENERATION_BENEFIT_UNTESTED'
        except Exception as error:receipt.update(result='FAIL',error=str(error))
        finally:
            if process.poll() is None:
                process.terminate()
                try:process.wait(timeout=8)
                except subprocess.TimeoutExpired:process.kill();process.wait(timeout=5)
            receipt.update(owned_pid=process.pid,owned_server_stopped=process.poll() is not None)
    (E/'receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps({k:v for k,v in receipt.items() if k!='system_stats'}))
    if receipt['result']=='FAIL':raise RuntimeError(receipt.get('error'))
if __name__=='__main__':main()
