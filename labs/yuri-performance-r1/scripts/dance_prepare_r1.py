"""Bounded CPU benchmark assets; reference/model bytes never enter Git."""
from pathlib import Path
import urllib.request,hashlib,json,concurrent.futures
import cv2,numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];L=ROOT/'local/dance-benchmark-r1';E=ROOT/'evidence/dance-benchmark-r1'
models=L/'models';models.mkdir(exist_ok=True)
urls={'mediapipe_heavy.task':'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task','rtmw3d.onnx':'https://huggingface.co/Soykaf/RTMW3D-x/resolve/main/onnx/rtmw3d-x_8xb64_cocktail14-384x288-b0a0eab7_20240626.onnx'}
def download(kv):
    name,url=kv;p=models/name
    if not p.exists():
        with urllib.request.urlopen(url,timeout=120) as r,open(p.with_suffix('.partial'),'wb') as f:
            while b:=r.read(1024*1024):f.write(b)
        p.with_suffix('.partial').replace(p)
    d={'name':name,'source_url':url,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'execution':'CPU_ONLY','git':'IGNORED_LOCAL_MODEL'};print(d,flush=True);return d
cap=cv2.VideoCapture(str(L/'reference/reference.mp4'));sheet=Image.new('RGB',(1600,4*245),'#17202a');dr=ImageDraw.Draw(sheet)
for i,t in enumerate(np.arange(20,28,.5)):
    cap.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=cap.read();assert ok
    x=i%4*400;y=i//4*245;sheet.paste(Image.fromarray(cv2.cvtColor(cv2.resize(f,(400,225)),cv2.COLOR_BGR2RGB)),(x,y));dr.text((x+4,y+226),f'{t:.2f}s',fill='white')
sheet.save(L/'segment20_28_contact.jpg');cap.release()
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:receipt=list(pool.map(download,urls.items()))
(E/'model_receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
