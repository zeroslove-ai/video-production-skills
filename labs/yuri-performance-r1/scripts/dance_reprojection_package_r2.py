"""Local-only time-synced reference/overlay/before/rejected/after comparison."""
from pathlib import Path
import json,cv2,numpy as np,subprocess,shutil,hashlib
R=Path(__file__).resolve().parents[1];E=R/'evidence/dance-benchmark-r1';L=R/'local/dance-benchmark-r1';methods=['motionbert','motionbert_reprojection','motionbert_reprojection_stable'];qa={m:json.loads((E/(m+'_retarget_allframe_qa.json')).read_text()) for m in methods};joints={m:json.loads((E/(m+'_retarget_joints.json')).read_text()) for m in methods};camera=json.loads((E/'arm_reprojection_r2.json').read_text())['camera_fit_frozen_from_r1'];scale=camera['scale_px_per_m'];offset=np.array(camera['translation_px']);detector=np.load(L/'motionbert_motion.npz')['xy']
for m in methods:
    assert qa[m]['candidate_sha256']==hashlib.sha256((L/(m+'_DANCE_R1.blend')).read_bytes()).hexdigest()
    folder=Path(qa[m]['render_folder']);assert len(list(folder.glob('*.png')))==180
    subprocess.run([shutil.which('ffmpeg'),'-y','-framerate','30','-i',str(folder/'%04d.png'),'-frames:v','180','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(L/(m+'_retarget.mp4'))],capture_output=True,check=True)
cap=cv2.VideoCapture(str(L/'reference/reference.mp4'));cap.set(cv2.CAP_PROP_POS_FRAMES,1200);writer=cv2.VideoWriter(str(L/'reprojection_comparison.avi'),cv2.VideoWriter_fourcc(*'MJPG'),30,(1600,700))
labels=['REFERENCE','WRIST OVERLAY','BASELINE MOTIONBERT','REJECTED: ARM POP','CONSTRAINED REPROJECT']
for k in range(180):
    ok,f=cap.read();assert ok;cap.grab();fi=k*2;crop=f[100:1020,1380:1840].copy();over=crop.copy();cols=[]
    for side,idx in [('L',5),('R',6)]:
        cv2.circle(over,tuple(np.round(detector[fi,idx]-[1380,100]).astype(int)),6,(0,255,0),2)
        for m,color in [('motionbert',(0,220,255)),('motionbert_reprojection_stable',(80,80,255))]:
            p=joints[m][fi]['joints']['hand.'+side]['head'];pt=np.round(np.array([p[0],-p[2]])*scale+offset-[1380,100]).astype(int);cv2.circle(over,tuple(pt),8,color,2)
    for source in [crop,over]:
        panel=np.zeros((700,320,3),np.uint8);panel[50:690]=cv2.resize(source,(320,640));cols.append(panel)
    for m in methods:
        panel=np.zeros((700,320,3),np.uint8);panel[130:610]=cv2.imread(str(Path(qa[m]['render_folder'])/f'{k:04d}.png'));cols.append(panel)
    for i,p in enumerate(cols):cv2.putText(p,labels[i],(8,25),cv2.FONT_HERSHEY_SIMPLEX,.42,(245,245,245),1)
    cv2.putText(cols[1],'green detector / yellow before',(5,650),cv2.FONT_HERSHEY_SIMPLEX,.36,(230,230,230),1);cv2.putText(cols[1],'red after / frozen camera fit',(5,670),cv2.FONT_HERSHEY_SIMPLEX,.36,(230,230,230),1)
    joined=np.concatenate(cols,axis=1);cv2.putText(joined,f'SOURCE {20+fi/60:.3f}s | 1x | image-fit experiment / WORLD ACCURACY FAIL',(5,695),cv2.FONT_HERSHEY_SIMPLEX,.42,(245,245,245),1);writer.write(joined)
    if k==90:cv2.imwrite(str(L/'reprojection_comparison_poster.jpg'),joined)
writer.release();cap.release();movie=L/'reprojection_comparison_6sec.mp4';subprocess.run([shutil.which('ffmpeg'),'-y','-i',str(L/'reprojection_comparison.avi'),'-i',str(L/'reference/reference.mp4'),'-map','0:v','-map','1:a','-af','atrim=start=20:end=26,asetpts=PTS-STARTPTS','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-t','6','-movflags','+faststart',str(movie)],capture_output=True,check=True)
probe=json.loads(subprocess.check_output([shutil.which('ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(movie)]));v=next(x for x in probe['streams'] if x['codec_type']=='video');assert v['nb_frames']=='180' and v['avg_frame_rate']=='30/1' and abs(float(probe['format']['duration'])-6)<.01
(E/'reprojection_delivery_r2.json').write_text(json.dumps({'file':str(movie),'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'duration_seconds':6,'preview_fps':30,'frames':180,'motion_fps':60,'candidates':{m:qa[m]['candidate_sha256'] for m in methods},'source_media_in_git':False,'body_only':True,'scope':'same extraction, three arm retarget variants; not three additional extraction stacks','world_accuracy_gate':'FAIL'},indent=2))
(L/'REVIEW_DANCE_R2.html').write_text('<!doctype html><meta charset="utf-8"><title>Dance reprojection R2</title><style>body{background:#14202a;color:#eef;font:16px system-ui;margin:24px}video{width:100%}button{padding:10px}</style><h1>Dance6sec · reprojection before / rejected / constrained</h1><p>Reference / wrist overlay / baseline / rejected arm pop / constrained after. Same MediaPipe2D+MotionBERT. Image-fit improved; world/root/contact accuracy remains FAIL.</p><button onclick="let v=document.querySelector(\'video\');v.currentTime=0;v.playbackRate=1;v.play()">Play complete interval at 1x</button><video controls src="reprojection_comparison_6sec.mp4"></video>',encoding='utf-8');print(json.dumps({'movie':str(movie),'sha256':hashlib.sha256(movie.read_bytes()).hexdigest()}))
