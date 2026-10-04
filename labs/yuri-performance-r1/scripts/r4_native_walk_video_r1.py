"""Encode preserved native24fps Walk proof and two96-frame cycles without rerender."""
from pathlib import Path
import json,hashlib,subprocess
import numpy as np
from PIL import Image,ImageDraw
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');P=B/'alpha-native-walk-source-r1';O=B/'alpha-native-walk-delivery-r1';O.mkdir(exist_ok=False);m=json.loads((P/'NATIVE_WALK_SOURCE_PRIVATE_R1.json').read_bytes());assert m['complete97_three_views'] and m['native_retiming_factor']==1 and m['source_scene_fps']==24
g=json.loads((B/'o1-native-walk-source-r1/NATIVE_GUARD_RESULT.json').read_bytes());assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();movies=[]
for view in ['front','quarter','side']:
 assert len(list((P/view).glob('*.jpg')))==97
 for loop2 in [False,True]:
  out=O/(view+('_NATIVE_WALK_LOOP2_1x.mp4' if loop2 else '_NATIVE_WALK_FULL97_1x.mp4'))
  args=['ffmpeg','-v','error','-framerate','24','-i',str(P/view/'%04d.jpg')]
  if loop2:args += ['-vf','trim=end_frame=96,loop=loop=1:size=96:start=0,setpts=N/(24*TB)','-frames:v','192']
  args += ['-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2','-filter_threads','2','-n',str(out)];subprocess.run(args,check=True);subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(out),'-f','null','-'],check=True)
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(out)]));st=probe['streams'][0];expected=192 if loop2 else 97;assert int(st['nb_read_frames'])==expected and st['avg_frame_rate']=='24/1'
  movies.append({'file':str(out),'sha256':sha(out),'bytes':out.stat().st_size,'view':view,'frames':expected,'fps':24,'duration_seconds':float(st['duration']),'native_retiming_factor':1,'whole_frame_decode':'PASS','loop2':loop2,'loop_basis':'96 unique frames1..96 repeated twice, endpoint97 duplicate omitted only in loop encoding' if loop2 else 'all original authored frames1..97, including endpoint','probe':probe})
 grid=Image.new('RGB',(256*8,280*13),'white');dr=ImageDraw.Draw(grid)
 for i,f in enumerate(range(1,98)):
  x=i%8*256;y=i//8*280;grid.paste(Image.open(P/view/f'{f:04}.jpg').resize((256,256)),(x,y+24));dr.text((x+4,y+4),f'{view} f{f} {(f-1)/24:.3f}s',fill='black')
 grid.save(O/f'ALL97_{view}_SOURCE_QA_R1.jpg',quality=94)
frames=[1,13,25,37,49,61,73,85,97];grid=Image.new('RGB',(320*len(frames),344*3),'white');dr=ImageDraw.Draw(grid)
for row,view in enumerate(['front','quarter','side']):
 for col,f in enumerate(frames):grid.paste(Image.open(P/view/f'{f:04}.jpg'),(col*320,row*344+24));dr.text((col*320+4,row*344+4),f'{view} f{f} {(f-1)/24:.3f}s',fill='black')
grid.save(O/'NATIVE_WALK_MATCHED_THREE_VIEW_R1.jpg',quality=94)
a=np.array(Image.open(B/'alpha-a1-contact-qa-r3/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png').convert('RGBA'));z=np.array(Image.open(P/'NATIVE_WALK_OFF_SOURCE_CAMERA_NEUTRAL_R1.png').convert('RGBA'));assert a.shape==z.shape and np.array_equal(a,z)
(O/'OFF_PIXEL_QA_R1.json').write_text(json.dumps({'changed_pixels':0,'max_RGBA_delta':0,'dimensions':list(a.shape),'exact_decoded_RGBA_equal':True,'source_baseline':str(B/'alpha-a1-contact-qa-r3/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png')},indent=2),encoding='utf8');(O/'VIDEO_CUSTODY_R1.json').write_text(json.dumps(movies,indent=2),encoding='utf8')
html='<!doctype html><meta charset="utf-8"><title>Original R4 native Walk source QA</title><style>body{background:#222;color:#eee;font:16px system-ui}section{display:flex;gap:8px}video{width:32%}button{padding:12px;font-size:20px}</style><h1>Original R4 · existing WalkInPlace · SOURCE ONLY</h1><p>Original native24fps, frames1–97,4.0s endpoint span/4.041667s full97 video. Native speed factor1. No donor, retiming, geometry or skin edits. In-place walking does not prove world translation, planted foot force or balance; feet/contact/deformation failures remain HOLD. Unity/F2/TierP0.</p><button onclick="document.querySelectorAll(\'video\').forEach(v=>{v.currentTime=0;v.playbackRate=1;v.play()})">Play full clip and two cycles at original native 1x</button><h2>Full original97 frames</h2><section>'
for x in movies:
 if not x['loop2']:html+=f'<video controls preload="auto" src="{Path(x["file"]).name}"></video>'
html+='</section><h2>Two cycles ·96unique frames ×2 ·8.0s</h2><section>'
for x in movies:
 if x['loop2']:html+=f'<video controls preload="auto" src="{Path(x["file"]).name}"></video>'
html+='</section><p>Fixed orthographic fullbody front/quarter/side,320×320CPU2sampleJPEG92 previews; source material/face/gaze retained. No smoothing/contact correction/Unity implementation.</p>'
(O/'REVIEW_NATIVE_WALK_SOURCE_R1.html').write_text(html,encoding='utf8');print('NATIVE_WALK_FULL97_AND_TWO_CYCLES_NATIVE24FPS_DECODE_OFF_PASS')
