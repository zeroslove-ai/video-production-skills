"""Five-camera same-body normal-speed comparison, no face acceptance claim."""
from pathlib import Path
import json,cv2,numpy as np,subprocess,shutil,hashlib
R=Path(__file__).resolve().parents[1];L=R/'local/native-camera-r4';E=R/'evidence/native-camera-r4';OUT=R/'local/native-camera-compare-r5';OUT.mkdir(exist_ok=True);receipt=json.loads((E/'video_delivery.json').read_text());assert len(receipt['videos'])==15
records=[];views=['full_body','waist_threequarter','face_close','hand_face','vertical']
for clip in ['greeting_wave','shy_lookaway','please_tilt']:
    files=[L/(clip+'__'+v+'.mp4') for v in views];caps=[cv2.VideoCapture(str(p)) for p in files];assert all(c.isOpened() for c in caps);avi=OUT/(clip+'.avi');writer=cv2.VideoWriter(str(avi),cv2.VideoWriter_fourcc(*'MJPG'),24,(1240,650))
    for fi in range(120):
        frame=np.zeros((650,1240,3),np.uint8)
        for i,cap in enumerate(caps):
            ok,f=cap.read();assert ok
            if i<4:x=i%2*480;y=i//2*305+40;tile=cv2.resize(f,(480,270))
            else:x=970;y=65;tile=cv2.resize(f,(270,480))
            frame[y:y+tile.shape[0],x:x+tile.shape[1]]=tile;cv2.putText(frame,views[i],(x+5,y-8),cv2.FONT_HERSHEY_SIMPLEX,.52,(230,230,230),1)
        t=fi/24;phase='anticipation' if t<.65 else 'motion' if t<1.55 else 'emotional peak' if t<2.2 else 'hold' if t<3 else 'follow-through' if t<3.75 else 'recovery';cv2.putText(frame,f'{clip} | {t:.2f}s | recipe phase: {phase}',(8,20),cv2.FONT_HERSHEY_SIMPLEX,.58,(245,245,245),1);cv2.putText(frame,'Native BODY research | face neutral A/O FAIL | 5 camera clips, NOT 5 new motions',(8,638),cv2.FONT_HERSHEY_SIMPLEX,.55,(245,245,245),1);writer.write(frame)
    writer.release()
    for c in caps:c.release()
    movie=OUT/(clip+'_five_camera.mp4');subprocess.run([shutil.which('ffmpeg'),'-y','-i',str(avi),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)],capture_output=True,check=True);probe=json.loads(subprocess.check_output([shutil.which('ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(movie)]));assert probe['streams'][0]['nb_frames']=='120' and abs(float(probe['format']['duration'])-5)<.01
    records.append({'clip':clip,'file':str(movie),'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'duration':5,'fps':24,'sources':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],'phase_label_scope':'semantic recipe intervals, not independently scored emotional readability'})
(R/'evidence/native-camera-compare-r5').mkdir(exist_ok=True);(R/'evidence/native-camera-compare-r5/delivery.json').write_text(json.dumps({'videos':records,'new_physical_base_recipes':0,'actual_yuri_approved':0},indent=2))
html='<!doctype html><meta charset="utf-8"><title>Native acting five-camera R5</title><style>body{background:#20242d;color:#eef;font:16px system-ui;margin:24px}video{width:100%}button{padding:10px}</style><h1>First3 body acting · same animation / five cameras</h1><p>Native body study only. Actual face A/O acceptance FAIL. Timed semantic proxy face/gaze studies remain separate.</p>'
for d in records:html+=f'<section><h2>{d["clip"]}</h2><button onclick="let v=this.closest(\'section\').querySelector(\'video\');v.currentTime=0;v.playbackRate=1;v.play()">Play1x {d["clip"]}</button><video controls src="{Path(d["file"]).name}"></video></section>'
(OUT/'REVIEW_NATIVE_CAMERA_R5.html').write_text(html,encoding='utf-8');print(json.dumps({'videos':len(records)}))
