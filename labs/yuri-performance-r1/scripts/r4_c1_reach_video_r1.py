"""Encode actual C1 native samples; preserve explicit30fps vs source24fps."""
from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
B=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');D=B/'alpha-c1-reach-delivery-r1';movies=[]
for view in ['front','quarter','side']:
 p=B/'alpha-c1-reach-preview-r1'/view;assert len(list(p.glob('*.jpg')))==61
 movie=D/f'C1_REACH_RETURN_{view}_1x.mp4';subprocess.run(['ffmpeg','-v','error','-framerate','30','-i',str(p/'%04d.jpg'),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2','-n',str(movie)],check=True);subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(movie),'-f','null','-'],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)]));movies.append({'view':view,'file':str(movie),'bytes':movie.stat().st_size,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'whole61_frame_decode':'PASS','probe':probe})
frames=[1,11,23,31,41,51,61];g=Image.new('RGB',(512*7,408*3),'white');draw=ImageDraw.Draw(g)
for row,view in enumerate(['front','quarter','side']):
 for col,f in enumerate(frames):g.paste(Image.open(B/'alpha-c1-reach-preview-r1'/view/f'{f:04}.jpg'),(col*512,row*408+24));draw.text((col*512+8,row*408+4),f'{view} frame{f} {(f-1)/30:.3f}s',fill='black')
g.save(D/'C1_REACH_MULTIVIEW_QA_R1.jpg',quality=94)
(D/'VIDEO_CUSTODY_R1.json').write_text(json.dumps(movies,indent=2),encoding='utf8')
html='<!doctype html><meta charset="utf-8"><title>Original R4 C1 reach-return source QA</title><style>body{background:#222;color:#eee;font:16px system-ui}section{display:flex;gap:8px}video{width:32%}button{padding:12px;font-size:20px}</style><h1>Original R4 · C1 reach→return</h1><p>Existing staged CC0 Interact. All61 native frames at30fps;2.033333s. Canonical source24fps preserved. Native left hand dominant, no mirror. No dedicated hold, grip/contact fixture or Unity/final visual promotion.</p><button onclick="document.querySelectorAll(\'video\').forEach(v=>{v.currentTime=0;v.playbackRate=1;v.play()})">Play all three at normal speed</button><section>'
for m in movies:html+=f'<video controls preload="auto" src="{Path(m["file"]).name}"></video>'
html+='</section><p>Fixed50mm front/quarter/side, source appearance retained. CPU2sample512×384/JPEG92 preview only. StageB/O1/PRIMARY/F2/F3/TierP and prop physics HOLD.</p>'
(D/'REVIEW_C1_REACH_RETURN_R1.html').write_text(html,encoding='utf8');print('C1_WHOLE_NATIVE_VIDEO_ENCODE_DECODE_PASS')
