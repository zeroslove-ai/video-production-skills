"""Encode one whole169-frame LEFT active-hand camera supplement at original24fps."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image,ImageDraw
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');P=B/'alpha-native-grasp-left-close-r1';O=B/'alpha-native-grasp-left-close-delivery-r1';O.mkdir(exist_ok=False)
g=json.loads((B/'o1-native-grasp-left-close-restore-r1b/NATIVE_GUARD_RESULT.json').read_bytes());assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN'
assert len(list((P/'left_hand_close').glob('*.jpg')))==169
out=O/'LEFT_ACTIVE_HAND_NATIVE_GRASP_1x.mp4'
subprocess.run(['ffmpeg','-v','error','-framerate','24','-i',str(P/'left_hand_close/%04d.jpg'),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2','-n',str(out)],check=True)
subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(out),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]))
assert int(probe['streams'][0]['nb_frames'])==169
(O/'VIDEO_CUSTODY_R1.json').write_text(json.dumps({'file':str(out),'SHA':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'whole169_decode':'PASS','probe':probe},indent=2),encoding='utf-8')
grid=Image.new('RGB',(13*192,13*212),'white');dr=ImageDraw.Draw(grid)
for ix in range(169):
    x=ix%13*192;y=ix//13*212;grid.paste(Image.open(P/'left_hand_close'/f'{ix+1:04}.jpg').resize((192,192)),(x,y+20));dr.text((x+2,y+2),f'f{ix+1}',fill='black')
grid.save(O/'LEFT_ACTIVE_HAND_ALL169_R1.jpg',quality=96)
(O/'REVIEW_R4_GRASP_LEFT_ACTIVE_HAND_R1.html').write_text('''<!doctype html><meta charset="utf-8"><title>R4 Grasp LEFT active hand supplement</title><style>body{background:#222;color:white;font:18px system-ui}video{width:512px;max-width:95%}button{padding:16px}img{max-width:100%}</style><h1>R4 Grasp · actual moving LEFT hand</h1><p>Same immutable candidate89a3a8ca / existing native169frames / original24fps /7.041667seconds. Camera follows wrist world translation with constant target offset; camera rotation fixed. Lighting/material/source motion unchanged. This close judges active finger/thumbnail readability only; feet/root/body use previously completed fixed front/waist views.</p><button onclick="const v=document.querySelector('video');v.currentTime=0;v.playbackRate=1;v.play()">Play LEFT active hand at normal speed</button><br><video controls preload="auto" src="LEFT_ACTIVE_HAND_NATIVE_GRASP_1x.mp4"></video><p>Source preservation and dominant-weight surface tests are technical/scoped evidence; visual review is separate. No prop, physical grasp, Unity or TierP approval. Original right-hand close remains static control. Earlier packet9d23f40e unchanged; this is a separate camera supplement.</p><img src="LEFT_ACTIVE_HAND_ALL169_R1.jpg">''',encoding='utf-8')
print('LEFT active hand movie/grid prepared; actual whole1x UI and visual verdict pending')
