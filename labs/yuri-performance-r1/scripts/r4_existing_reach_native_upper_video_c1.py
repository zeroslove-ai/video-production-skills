"""Encode actual C1 native samples; preserve explicit30fps vs source24fps."""
from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
B=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');D=B/'c1-existing-reach-native-upper-delivery-c1';D.mkdir(exist_ok=False);movies=[]
for view in ['front','quarter','side']:
 p=B/'c1-existing-reach-native-upper-c1'/view;assert len(list(p.glob('*.jpg')))==61
 movie=D/f'C1_NATIVE_UPPER_REACH_{view}_1x.mp4';subprocess.run(['ffmpeg','-v','error','-framerate','30','-i',str(p/'%04d.jpg'),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2','-n',str(movie)],check=True);subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(movie),'-f','null','-'],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)]));movies.append({'view':view,'file':str(movie),'bytes':movie.stat().st_size,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'whole61_frame_decode':'PASS','probe':probe})
frames=[1,11,23,31,41,51,61];g=Image.new('RGB',(512*7,408*3),'white');draw=ImageDraw.Draw(g)
for row,view in enumerate(['front','quarter','side']):
 for col,f in enumerate(frames):g.paste(Image.open(B/'c1-existing-reach-native-upper-c1'/view/f'{f:04}.jpg'),(col*512,row*408+24));draw.text((col*512+8,row*408+4),f'{view} frame{f} {(f-1)/30:.3f}s',fill='black')
g.save(D/'C1_NATIVE_UPPER_MULTIVIEW_QA_C1.jpg',quality=94)
(D/'VIDEO_CUSTODY_C1.json').write_text(json.dumps(movies,indent=2),encoding='utf8')
html='<!doctype html><meta charset="utf-8"><title>Original R4 existing Reach native-upper correction C1</title><style>body{background:#222;color:#eee;font:16px system-ui}section{display:flex;gap:8px}video{width:32%}button{padding:12px;font-size:20px}</style><h1>Original R4 · C1 reach→return</h1><p>Original native Reach upper12 on existing C1 lower/root. Different upper trajectory from old donor candidate. All61 native frames at30fps;2.033333s. Canonical source24fps preserved. Two-hand native variant, no mirror. No dedicated hold, grip/contact fixture or Unity/final visual promotion.</p><button onclick="document.querySelectorAll(\'video\').forEach(v=>{v.currentTime=0;v.playbackRate=1;v.play()})">Play all three at normal speed</button><section>'
for m in movies:html+=f'<video controls preload="auto" src="{Path(m["file"]).name}"></video>'
html+='</section><p>Fixed50mm front/quarter/side, source appearance retained. CPU2sample512×384/JPEG92 preview only. StageB/O1/PRIMARY/F2/F3/TierP and prop physics HOLD.</p>'
(D/'REVIEW_C1_NATIVE_UPPER_REACH_R1.html').write_text(html,encoding='utf8');print('C1_WHOLE_NATIVE_VIDEO_ENCODE_DECODE_PASS')

# Matched old/new whole playback, old images reused without rerender.
for view in ['front','quarter','side']:
 old=B/'alpha-c1-reach-delivery-r1'/f'C1_REACH_RETURN_{view}_1x.mp4';new=D/f'C1_NATIVE_UPPER_REACH_{view}_1x.mp4';out=D/f'OLD_LEFT_NEW_RIGHT_{view}_1x.mp4'
 subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(old),'-threads','2','-i',str(new),'-filter_complex','[0:v][1:v]hstack=inputs=2[v]','-map','[v]','-c:v','libx264','-crf','18','-threads','2','-filter_complex_threads','2','-n',str(out)],check=True);subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(out),'-f','null','-'],check=True)
 grid=Image.new('RGB',(256*8,216*8),'white');dr=ImageDraw.Draw(grid)
 for i,f in enumerate(range(1,62)):
  x=i%8*256;y=i//8*216;grid.paste(Image.open(B/'c1-existing-reach-native-upper-c1'/view/f'{f:04}.jpg').resize((256,192)),(x,y+24));dr.text((x+4,y+4),f'{view} frame{f}',fill='black')
 grid.save(D/f'ALL61_NEW_{view}_QA_C1.jpg',quality=94)
import numpy as np
a=np.array(Image.open(B/'alpha-a1-contact-qa-r3/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png').convert('RGBA'));z=np.array(Image.open(B/'c1-existing-reach-native-upper-c1/NEW_CANDIDATE_OFF_SOURCE_NEUTRAL.png').convert('RGBA'));assert a.shape==z.shape and np.array_equal(a,z)
(D/'OFF_PIXEL_QA_C1.json').write_text(json.dumps({'dimensions':list(a.shape),'changed_pixels':0,'max_RGBA_delta':0,'full_array_exact':True}),encoding='utf8')
