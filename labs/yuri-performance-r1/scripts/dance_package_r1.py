"""Time-synced full interval comparison, local-only reference pixels and audio."""
from pathlib import Path
import cv2,numpy as np,json,hashlib,subprocess,shutil,struct
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];L=R/'local/dance-benchmark-r1';E=R/'evidence/dance-benchmark-r1'
methods=['mediapipe','rtmw3d','motionbert'];meta={m:json.loads((E/(m+'_retarget.json')).read_text()) for m in methods};qa={m:json.loads((E/(m+'_retarget_allframe_qa.json')).read_text()) for m in methods};a={m:np.load(L/(m+'_motion.npz')) for m in methods};edges=[(0,1),(0,2),(1,2),(1,3),(3,5),(2,4),(4,6),(1,7),(2,8),(7,8),(7,9),(9,11),(8,10),(10,12),(11,13),(13,15),(12,14),(14,16)]
for m in methods:
    assert meta[m]['candidate_sha256']==qa[m]['candidate_sha256']==hashlib.sha256(Path(meta[m]['candidate']).read_bytes()).hexdigest()
    folder=Path(qa[m]['render_folder']);assert len(list(folder.glob('*.png')))==180
    subprocess.run([shutil.which('ffmpeg'),'-y','-framerate','30','-i',str(folder/'%04d.png'),'-frames:v','180','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(L/(m+'_retarget.mp4'))],capture_output=True,check=True)
    glb=L/(m+'_DANCE_R1.glb');data=glb.read_bytes();chunk_len,kind=struct.unpack_from('<II',data,12);g=json.loads(data[20:20+chunk_len]);assert kind==0x4e4f534a and len(g.get('animations',[]))==1 and len(g['animations'][0]['channels'])==51;meta[m]['glb_structure']={'animations':[x.get('name') for x in g['animations']],'skin_joint_counts':[len(x['joints']) for x in g.get('skins',[])],'sha256':hashlib.sha256(data).hexdigest(),'note':'Blender ACTIVE_ACTIONS exporter merges baked active body into animation named Animation; one clip with 51 channels verified, not action-name identity'}
cap=cv2.VideoCapture(str(L/'reference/reference.mp4'));cap.set(cv2.CAP_PROP_POS_FRAMES,1200);writer=cv2.VideoWriter(str(L/'comparison.avi'),cv2.VideoWriter_fourcc(*'MJPG'),30,(1920,700));sheet=Image.new('RGB',(1920,6*285),'#14202a');draw=ImageDraw.Draw(sheet)
for k in range(180):
    ok,f=cap.read();assert ok;cap.grab();fi=k*2;cols=[]
    for m in [None,*methods[:2]]:
        crop=f[100:1020,1380:1840].copy();color=(0,230,255) if m=='mediapipe' else (255,180,0)
        if m:
            p=np.round(a[m]['xy'][fi]-[1380,100]).astype(int)
            for u,v in edges:cv2.line(crop,tuple(p[u]),tuple(p[v]),color,3,cv2.LINE_AA)
        panel=np.zeros((700,320,3),np.uint8);panel[50:690]=cv2.resize(crop,(320,640));cv2.putText(panel,'REFERENCE' if m is None else m.upper()+' RAW',(8,25),cv2.FONT_HERSHEY_SIMPLEX,.46,(245,245,245),1);cols.append(panel)
    for m in methods:
        panel=np.zeros((700,320,3),np.uint8);render=cv2.imread(str(Path(qa[m]['render_folder'])/f'{k:04d}.png'));assert render is not None;panel[130:610]=render;cv2.putText(panel,m.upper()+' RETARGET',(8,25),cv2.FONT_HERSHEY_SIMPLEX,.43,(245,245,245),1);cv2.putText(panel,'assumed scale / body only',(8,640),cv2.FONT_HERSHEY_SIMPLEX,.4,(180,180,190),1);cols.append(panel)
    frame=np.concatenate(cols,axis=1);cv2.putText(frame,f'SOURCE {20+fi/60:.3f}s | 1x | 60fps motion / 30fps preview',(10,695),cv2.FONT_HERSHEY_SIMPLEX,.45,(255,255,255),1);writer.write(frame)
    if k%15==0:
        j=k//15;thumb=cv2.resize(frame,(960,265));sheet.paste(Image.fromarray(cv2.cvtColor(thumb,cv2.COLOR_BGR2RGB)),((j%2)*960,(j//2)*285));draw.text(((j%2)*960+5,(j//2)*285+268),f'{20+fi/60:.2f}s',fill='white')
writer.release();cap.release();sheet.save(L/'comparison_contact.jpg')
movie=L/'comparison_6sec.mp4';subprocess.run([shutil.which('ffmpeg'),'-y','-i',str(L/'comparison.avi'),'-i',str(L/'reference/reference.mp4'),'-map','0:v','-map','1:a','-af','atrim=start=20:end=26,asetpts=PTS-STARTPTS','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-t','6','-movflags','+faststart',str(movie)],capture_output=True,check=True)
probe=json.loads(subprocess.check_output([shutil.which('ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(movie)]));v=next(x for x in probe['streams'] if x['codec_type']=='video');assert v['nb_frames']=='180' and v['avg_frame_rate']=='30/1' and abs(float(probe['format']['duration'])-6)<.01
receipt={'comparison':str(movie),'comparison_sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'duration_seconds':6,'display_fps':30,'frames':180,'motion_fps':60,'source_start_seconds':20,'source_end_exclusive_seconds':26,'reference_pixels_local_only':True,'source_audio_in_local_comparison_only':True,'candidates':meta,'not_accuracy_pass':True};(E/'delivery_receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps({k:v for k,v in receipt.items() if k!='candidates'},ensure_ascii=True))
html='<!doctype html><meta charset="utf-8"><title>Dance benchmark R1</title><style>body{background:#14202a;color:#eef;font:16px system-ui;margin:24px}video{width:100%}button{padding:10px}</style><h1>Dance benchmark · 20–26s · 1x comparison</h1><p>Reference / MediaPipe raw / RTMW3D raw / MediaPipe retarget / RTMW3D retarget / MotionBERT temporal retarget. MotionBERT reuses MediaPipe 2D observations. Body only. Absolute world root and hand orientation unresolved. Accuracy gate: FAIL; no chorus extension.</p><button onclick="let v=document.querySelector(\'video\');v.currentTime=0;v.playbackRate=1;v.play()">Play complete interval at 1x</button><video controls src="comparison_6sec.mp4"></video><h2>Reusable candidates</h2><p><a href="mediapipe_DANCE_R1.blend">MediaPipe .blend</a> · <a href="mediapipe_DANCE_R1.glb">MediaPipe GLB</a> · <a href="rtmw3d_DANCE_R1.blend">RTMW3D .blend</a> · <a href="rtmw3d_DANCE_R1.glb">RTMW3D GLB</a> · <a href="motionbert_DANCE_R1.blend">MotionBERT .blend</a> · <a href="motionbert_DANCE_R1.glb">MotionBERT GLB</a></p>'
(L/'REVIEW_DANCE_R1.html').write_text(html,encoding='utf-8')
