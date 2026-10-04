"""Encode complete native right-hand samples at authored30fps and full-body witness."""
from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');D=B/'alpha-hand-relax-delivery-r1';D.mkdir(exist_ok=False);movies=[]
for view in ['hand_close','front','side']:
 p=B/'alpha-hand-relax-preview-r1'/view;assert len(list(p.glob('*.jpg')))==105
 movie=D/f'HAND_RELAX_{view}_1x.mp4';subprocess.run(['ffmpeg','-v','error','-framerate','30','-i',str(p/'%04d.jpg'),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2','-n',str(movie)],check=True);subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(movie),'-f','null','-'],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)]));movies.append({'view':view,'file':str(movie),'bytes':movie.stat().st_size,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'whole105_frame_decode':'PASS','probe':probe})
 # Every-frame filmstrip supplement: actual whole playback is required separately.
 g=Image.new('RGB',(15*160,7*180),'white');draw=ImageDraw.Draw(g)
 for f in range(1,106):
  x=((f-1)%15)*160;y=((f-1)//15)*180;g.paste(Image.open(p/f'{f:04}.jpg').resize((160,160)),(x,y+20));draw.text((x+4,y+3),str(f),fill='black')
 g.save(D/f'HAND_RELAX_{view}_ALL105_FRAMES_R1.jpg',quality=95)
frames=[1,16,32,53,69,87,105];g=Image.new('RGB',(512*7,536*3),'white');draw=ImageDraw.Draw(g)
for row,view in enumerate(['hand_close','front','side']):
 for col,f in enumerate(frames):g.paste(Image.open(B/'alpha-hand-relax-preview-r1'/view/f'{f:04}.jpg'),(col*512,row*536+24));draw.text((col*512+8,row*536+4),f'{view} f{f} {(f-1)/30:.3f}s',fill='black')
g.save(D/'HAND_RELAX_MULTIVIEW_QA_R1.jpg',quality=95)
g=Image.new('RGB',(512*3,536),'white');draw=ImageDraw.Draw(g)
for col,f in enumerate([1,53,105]):g.paste(Image.open(B/'alpha-hand-relax-preview-r1/fullbody'/f'{f:04}.jpg'),(col*512,24));draw.text((col*512+8,4),f'Fixed body/wrist f{f}',fill='black')
g.save(D/'HAND_RELAX_FULLBODY_POSITION_R1.jpg',quality=95)
(D/'VIDEO_CUSTODY_R1.json').write_text(json.dumps(movies,indent=2),encoding='utf8')
html='<!doctype html><meta charset="utf-8"><title>R4 finger-only source QA</title><style>body{background:#222;color:#eee;font:16px system-ui}section{display:flex;gap:8px}video{width:32%}button{padding:12px;font-size:20px}img{max-width:100%}</style><h1>Original R4 · right hand relax / gentle pregrasp / release</h1><p>105 native frames ·30fps ·3.5s. Existing15 finger bones only. Wrist/forearm/body/root fixed. Original source24fps preserved; Action source_fps=30. Source-only; prop/contact/physics/Unity/MUG HOLD.</p><button onclick="document.querySelectorAll(\'video\').forEach(v=>{v.currentTime=0;v.playbackRate=1;v.play()})">Play all three at normal speed</button><section>'
for m in movies:html+=f'<video controls preload="auto" src="{Path(m["file"]).name}"></video>'
html+='</section><p>Hand close · original-world front · hand-side fixed cameras. Source open15f, stagger curl16–52, hold53–69, release70–105. No wrist/palm approach or physical grasp claimed. Original materials/skin unchanged.</p><img src="HAND_RELAX_FULLBODY_POSITION_R1.jpg"><p>Whole playback required; every-frame strips are additional evidence.</p>'
(D/'REVIEW_HAND_RELAX_R1.html').write_text(html,encoding='utf8');print('HAND_RELAX_WHOLE105_ENCODE_DECODE_PASS')
