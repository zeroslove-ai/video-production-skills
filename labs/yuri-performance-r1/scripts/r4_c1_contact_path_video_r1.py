"""Encode complete native right-hand samples at authored30fps and full-body witness."""
from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');D=B/'alpha-c1-contact-path-delivery-r1';D.mkdir(exist_ok=False);movies=[]
for view in ['hand_close','front','side','fullbody']:
 p=B/'alpha-c1-contact-path-preview-r1'/view;assert len(list(p.glob('*.jpg')))==61
 movie=D/f'REACH_LEFT_FINGER_{view}_1x.mp4';subprocess.run(['ffmpeg','-v','error','-framerate','30','-i',str(p/'%04d.jpg'),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2','-n',str(movie)],check=True);subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(movie),'-f','null','-'],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)]));movies.append({'view':view,'file':str(movie),'bytes':movie.stat().st_size,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'whole61_frame_decode':'PASS','probe':probe})
 # Every-frame filmstrip supplement: actual whole playback is required separately.
 g=Image.new('RGB',(15*160,5*180),'white');draw=ImageDraw.Draw(g)
 for f in range(1,62):
  x=((f-1)%15)*160;y=((f-1)//15)*180;g.paste(Image.open(p/f'{f:04}.jpg').resize((160,160)),(x,y+20));draw.text((x+4,y+3),str(f),fill='black')
 g.save(D/f'REACH_LEFT_FINGER_{view}_ALL61_FRAMES_R1.jpg',quality=95)
frames=[1,10,14,27,35,46,61];g=Image.new('RGB',(512*7,536*3),'white');draw=ImageDraw.Draw(g)
for row,view in enumerate(['hand_close','front','side']):
 for col,f in enumerate(frames):g.paste(Image.open(B/'alpha-c1-contact-path-preview-r1'/view/f'{f:04}.jpg'),(col*512,row*536+24));draw.text((col*512+8,row*536+4),f'{view} f{f} {(f-1)/30:.3f}s',fill='black')
g.save(D/'REACH_LEFT_FINGER_MULTIVIEW_QA_R1.jpg',quality=95)
g=Image.new('RGB',(512*3,536),'white');draw=ImageDraw.Draw(g)
for col,f in enumerate([1,27,61]):g.paste(Image.open(B/'alpha-c1-contact-path-preview-r1/fullbody'/f'{f:04}.jpg'),(col*512,24));draw.text((col*512+8,4),f'Fixed body/wrist f{f}',fill='black')
g.save(D/'REACH_LEFT_FINGER_FULLBODY_POSITION_R1.jpg',quality=95)
(D/'VIDEO_CUSTODY_R1.json').write_text(json.dumps(movies,indent=2),encoding='utf8')
html='<!doctype html><meta charset="utf-8"><title>R4 finger-only source QA</title><style>body{background:#222;color:#eee;font:16px system-ui}section{display:flex;gap:8px}video{width:24%}button{padding:12px;font-size:20px}img{max-width:100%}</style><h1>Original R4 · C1 LEFT reach + LEFT arm clearance + existing R2 finger timing</h1><p>61 native frames ·30fps ·2.033333s. Only upper_arm.L quaternion paths changed; same R2 LEFT15-finger NLA, all other C1 body channels/feet/root/facehair unchanged. Original source24fps preserved; Action source_fps=30. 8deg outward endpoint shoulder path, original18-43 peak unchanged. Paired all61 inspected left digit/hand/arm-body/head/hair intersection pairs0; original neutral return HOLD. Source-only; prop/physics/Unity/MUG HOLD.</p><button onclick="document.querySelectorAll(\'video\').forEach(v=>{v.currentTime=0;v.playbackRate=1;v.play()})">Play all four at normal speed</button><section>'
for m in movies:html+=f'<video controls preload="auto" src="{Path(m["file"]).name}"></video>'
html+='</section><p>Hand close · original-world front · hand-side · fullbody fixed cameras; close camera follows C1 wrist only. C1 frames1–61 at30fps, one upper-arm channel derivative; left finger1–61 at same clock. Same-hand source combination; original-neutral return HOLD, return reaches C1 baseline only. No physical grasp claimed. Original materials/skin unchanged. Baseline same-camera controls at1,7,18,31,50,61; scoped contact PASS, weak-webbing/full collision/physical contact and Unity remain HOLD.</p><img src="REACH_LEFT_FINGER_FULLBODY_POSITION_R1.jpg"><p>Whole playback required; every-frame strips are additional evidence.</p>'
(D/'REVIEW_C1_LEFT_ARM_CONTACT_R1.html').write_text(html,encoding='utf8');print('REACH_LEFT_FINGER_WHOLE61_ENCODE_DECODE_PASS')

# Matched same-camera before/after controls at contact boundaries and original peak.
frames=[1,7,18,31,50,61]
for view in ['hand_close','front','side','fullbody']:
 g=Image.new('RGB',(6*256,2*280),'white');draw=ImageDraw.Draw(g)
 for col,f in enumerate(frames):
  for row,folder,label in [(0,B/'alpha-c1-contact-path-preview-r1/baseline_same_camera'/view,'C1 baseline + R2 fingers'),(1,B/'alpha-c1-contact-path-preview-r1'/view,'8deg arm path + same R2 fingers')]:
   g.paste(Image.open(folder/f'{f:04}.jpg').resize((256,256)),(col*256,row*280+24));draw.text((col*256+4,row*280+4),f'{label} f{f}',fill='black')
 g.save(D/f'SAME_CAMERA_BEFORE_AFTER_{view}_R1.jpg',quality=95)
