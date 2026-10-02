"""Decode first/middle/last + whole-clip SSIM; no AI generation quality claim."""
from pathlib import Path
import json,subprocess,shutil,re,hashlib
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence/comfy-video-r3';LOCAL=ROOT/'local/comfy-video-r3';data=json.loads((E/'receipt.json').read_text());source=Path(data['source']);ff=shutil.which('ffmpeg');reports=[]
def decode(video,label):
    d=LOCAL/'qa'/label;d.mkdir(parents=True,exist_ok=True)
    for f in (0,60,119):
        p=d/f'{f:04d}.png'
        subprocess.run([ff,'-y','-i',str(video),'-vf',f'select=eq(n\\,{f})','-fps_mode','passthrough','-frames:v','1',str(p)],check=True,capture_output=True)
    return d
ref=decode(source,'source')
for job in data['jobs']:
    if job['result']!='CPU_VIDEO_ROUNDTRIP_TECHNICAL_PASS':continue
    target=Path(job['file']);d=decode(target,job['argument_style'])
    result=subprocess.run([ff,'-i',str(source),'-i',str(target),'-lavfi','ssim','-f','null','-'],capture_output=True,text=True,check=True)
    match=re.search(r'All:([0-9.]+)',result.stderr);assert match
    ssim=float(match.group(1));psnrs=[]
    contact=Image.new('RGB',(1920,770),'#20242d');draw=ImageDraw.Draw(contact)
    for i,f in enumerate((0,60,119)):
        a=Image.open(ref/f'{f:04d}.png').convert('RGB');b=Image.open(d/f'{f:04d}.png').convert('RGB')
        mse=float(np.mean((np.asarray(a,dtype=np.float32)-np.asarray(b,dtype=np.float32))**2));psnr=float(10*np.log10(255**2/mse)) if mse else 100.
        psnrs.append({'decoded_frame':f,'rgb_mse':mse,'psnr_db':psnr})
        contact.paste(a,(640*i,0));contact.paste(b,(640*i,385));draw.text((640*i+6,362),f'Input decoded f{f}',fill='white');draw.text((640*i+6,747),f'Comfy {job["argument_style"]} f{f}: PSNR {psnr:.2f}dB',fill='white')
    p=LOCAL/('qa_'+job['argument_style']+'.jpg');contact.save(p,quality=90)
    reports.append({'argument_style':job['argument_style'],'whole_clip_ssim':ssim,'first_middle_last':psnrs,'contact':str(p),'technical_order_fidelity':'PASS' if ssim>.98 and min(x['psnr_db'] for x in psnrs)>35 else 'REVIEW','visual_acceptance':'PENDING_CONTACT_REVIEW; this is re-encoding, not AI inference'})
receipt={'method':'Same-time whole-clip FFmpeg SSIM plus decoded first/middle/last RGB PSNR','guard_scope':'Research re-encode fidelity only; not a video generation scoring standard','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'results':reports,'model_inference_jobs':0}
(E/'roundtrip_qa.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(reports));assert all(r['technical_order_fidelity']=='PASS' for r in reports)
