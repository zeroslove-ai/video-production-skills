"""Encode actual look-listen native samples; preserve explicit30fps vs source24fps."""
from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
B=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');D=B/'alpha-look-listen-delivery-r1';D.mkdir(exist_ok=False);movies=[]
for view in ['front','quarter','side']:
 p=B/'alpha-look-listen-preview-r1'/view;assert len(list(p.glob('*.jpg')))==151
 movie=D/f'LOOK_LISTEN_{view}_1x.mp4';subprocess.run(['ffmpeg','-v','error','-framerate','30','-i',str(p/'%04d.jpg'),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2','-n',str(movie)],check=True);subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(movie),'-f','null','-'],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)]));movies.append({'view':view,'file':str(movie),'bytes':movie.stat().st_size,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'whole151_frame_decode':'PASS','probe':probe})
frames=[1,12,42,63,73,102,151];g=Image.new('RGB',(512*7,664*3),'white');draw=ImageDraw.Draw(g)
for row,view in enumerate(['front','quarter','side']):
 for col,f in enumerate(frames):g.paste(Image.open(B/'alpha-look-listen-preview-r1'/view/f'{f:04}.jpg'),(col*512,row*664+24));draw.text((col*512+8,row*664+4),f'{view} frame{f} {(f-1)/30:.3f}s',fill='black')
g.save(D/'LOOK_LISTEN_MULTIVIEW_QA_R1.jpg',quality=94)
(D/'VIDEO_CUSTODY_R1.json').write_text(json.dumps(movies,indent=2),encoding='utf8')
html='<!doctype html><meta charset="utf-8"><title>Original R4 look-listen source QA</title><style>body{background:#222;color:#eee;font:16px system-ui}section{display:flex;gap:8px}video{width:32%}button{padding:12px;font-size:20px}</style><h1>Original R4 · look-listen</h1><p>Existing MIT A3 R4 upper-body Action rotations reused; listen hold/nod/return procedural. All151 native frames at30fps;5.033333s. Canonical source24fps preserved. Chest/neck/head only; source gaze inputs/drivers unchanged. Head/gaze runtime ownership integration HOLD. No prop/contact or Unity/final visual promotion.</p><button onclick="document.querySelectorAll(\'video\').forEach(v=>{v.currentTime=0;v.playbackRate=1;v.play()})">Play all three at normal speed</button><section>'
for m in movies:html+=f'<video controls preload="auto" src="{Path(m["file"]).name}"></video>'
html+='</section><p>Fixed ORTHO1.2m front/quarter/side, source appearance retained. CPU2sample512×640/JPEG85 preview only. StageB/O1/PRIMARY/F2/F3/TierP and prop physics HOLD.</p>'
(D/'REVIEW_LOOK_LISTEN_R1.html').write_text(html,encoding='utf8');print('C1_WHOLE_NATIVE_VIDEO_ENCODE_DECODE_PASS')
