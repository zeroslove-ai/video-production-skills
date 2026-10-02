"""Read-only reference facts and timecoded overview; source bytes stay ignored local."""
from pathlib import Path
import cv2,json,hashlib,sys,numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'local/dance-benchmark-r1';E=ROOT/'evidence/dance-benchmark-r1';E.mkdir(exist_ok=True);ref=OUT/'reference/reference.mp4';info=json.loads((OUT/'reference/IrqXrM4CaiE.info.json').read_text(encoding='utf-8'));probe=json.loads((OUT/'reference/ffprobe.json').read_text());stream=next(x for x in probe['streams'] if x['codec_type']=='video');cap=cv2.VideoCapture(str(ref));fps=cap.get(cv2.CAP_PROP_FPS);duration=float(probe['format']['duration']);times=list(np.arange(0,duration,4));cols=6;rows=(len(times)+cols-1)//cols;canvas=Image.new('RGB',(cols*320,rows*205),'#1a202a');draw=ImageDraw.Draw(canvas);folder=OUT/'overview';folder.mkdir(exist_ok=True)
for i,t in enumerate(times):
    cap.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,frame=cap.read();assert ok,(t,duration);frame=cv2.resize(frame,(320,180));p=folder/f'{t:06.2f}.jpg';cv2.imwrite(str(p),frame);x=i%cols*320;y=i//cols*205;canvas.paste(Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)),(x,y));draw.text((x+5,y+182),f'{int(t)//60:02d}:{t%60:05.2f}',fill='white')
canvas.save(OUT/'reference_overview.jpg',quality=92)
cap.set(cv2.CAP_PROP_POS_MSEC,10000);previous=None;changes=[]
for f in range(600):
    ok,frame=cap.read()
    if not ok:break
    gray=cv2.cvtColor(cv2.resize(frame,(320,180)),cv2.COLOR_BGR2GRAY)
    if previous is not None:changes.append(float(np.mean(cv2.absdiff(gray,previous))))
    previous=gray
cap.release();d={'reference_url':'https://www.youtube.com/watch?v=IrqXrM4CaiE','video_id':info['id'],'title':info['title'],'uploader_channel':info['channel'],'upload_date':info['upload_date'],'source_local_only':str(ref),'source_sha256':hashlib.sha256(ref.read_bytes()).hexdigest(),'source_committed':False,'width':stream['width'],'height':stream['height'],'encoded_fps':stream['avg_frame_rate'],'r_frame_rate':stream['r_frame_rate'],'duration_seconds':duration,'stream_duration_seconds':float(stream['duration']),'frame_count':int(stream['nb_frames']),'display_rotation':stream.get('side_data_list',[]),'reference_is_mirrored':True,'mirror_evidence':'source title explicitly MIRRORED; inference convention will be recorded separately','dancers_observed':5,'dancer_selection':'PENDING_CONTINUOUS_SEGMENT_VISIBILITY_REVIEW','dance_start_seconds':None,'dance_end_seconds':None,'camera_motion':'PENDING_BACKGROUND_FEATURE_ESTIMATION','cuts':'PENDING_FULL_TIMELINE_SCAN','floor_and_feet':'floor visible in observed early frame; full interval visibility pending','root_trajectory_world_m':'UNIDENTIFIED_WITHOUT_CAMERA_AND_SCALE_CALIBRATION','repeated_or_chorus_intervals':[],'duplicate_frame_diagnostic_10_to_20s':{'samples':len(changes),'mean_abs_gray_changes':changes,'even_pair_mean':float(np.mean(changes[::2])),'odd_pair_mean':float(np.mean(changes[1::2])),'fraction_below_0_05':float(np.mean(np.array(changes)<.05))},'status':'REFERENCE_ANALYSIS_IN_PROGRESS_NOT_MOTION_RECONSTRUCTION_PASS'}
(E/'reference_manifest.json').write_text(json.dumps(d,indent=2));print('REFERENCE_OVERVIEW',len(times),d['encoded_fps'],duration)
