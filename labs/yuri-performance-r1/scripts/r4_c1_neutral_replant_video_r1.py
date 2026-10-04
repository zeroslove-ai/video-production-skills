"""Encode both complete transition views; preserve failed experiment labels."""
import json,hashlib,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-c1-neutral-replant-delivery-r1';O.mkdir(exist_ok=False);P=B/'alpha-c1-neutral-replant-preview-r1';movies=[]
for view in ['fullbody_front','feet_side']:
 assert len(list((P/view).glob('*.jpg')))==73
 out=O/(view+'_REPLANT_EXPERIMENT_1x.mp4');subprocess.run(['ffmpeg','-v','error','-framerate','30','-i',str(P/view/'%04d.jpg'),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2','-n',str(out)],check=True);subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(out),'-f','null','-'],check=True);probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]));movies.append({'view':view,'file':str(out),'SHA':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'all73_decoded':True,'probe':probe})
 grid=Image.new('RGB',(13*144,6*164),'white');draw=ImageDraw.Draw(grid)
 for ix in range(73):
  x=(ix%13)*144;y=(ix//13)*164;grid.paste(Image.open(P/view/f'{ix+1:04}.jpg').resize((144,144)),(x,y+20));draw.text((x+2,y+2),f'f{61+ix}',fill='black')
 grid.save(O/(view+'_ALL73_FRAMES_R1.jpg'),quality=95)
baseline=np.asarray(Image.open(B/'alpha-a1-contact-qa-r3/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png'));after=np.asarray(Image.open(P/'CANDIDATE_OFF_SOURCE_NEUTRAL_R1.png'));assert baseline.shape==after.shape;pixel={'same_dimensions':list(baseline.shape),'changed_RGBA_pixels':int(np.count_nonzero(np.any(baseline!=after,axis=2))),'max_channel_error':int(np.abs(baseline.astype(int)-after.astype(int)).max()),'PASS':bool(np.array_equal(baseline,after))};assert pixel['PASS'];(O/'OFF_PIXEL_ORACLE_R1.json').write_text(json.dumps(pixel,indent=2),encoding='utf-8');(O/'VIDEO_CUSTODY_R1.json').write_text(json.dumps(movies,indent=2),encoding='utf-8')
html='<!doctype html><meta charset="utf-8"><title>R4 neutral replant experiment</title><style>body{background:#222;color:white;font:16px system-ui}video{width:46%}button{padding:14px}img{max-width:100%}</style><h1>R4 C1 → source neutral · supported replant experiment</h1><p>73 native frames61–133 at30fps; 2.433333seconds. This is one experiment, not a passed motion. Original C1 frames1–61 and R2 finger Action unchanged. L swing then R swing; actual source rig/skin/shader retained. Root unchanged. Read the constraint report before reuse.</p><button onclick="document.querySelectorAll(\'video\').forEach(v=>{v.currentTime=0;v.playbackRate=1;v.play()})">Play both at normal speed</button>'
for m in movies:html+=f'<video controls preload="auto" src="{Path(m["file"]).name}"></video>'
html+='<p>Fixed full body front and feet side. Full original C1 sequence has its own independently completed four-view normal-speed receipt; this page shows only the new transition. OFF authoritative neutral unchanged; ON exact-neutral/contact acceptance depends on the separate numerical and visual reports. No Unity/product/physics promotion.</p>'
for view in ['fullbody_front','feet_side']:html+=f'<img src="{view}_ALL73_FRAMES_R1.jpg">'
(O/'REVIEW_R4_NEUTRAL_REPLANT_EXPERIMENT_R1.html').write_text(html,encoding='utf-8');print(json.dumps({'movies':len(movies),'frames_each':73,'OFF_pixel_oracle':pixel}))
