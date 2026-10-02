"""Full interval overlay and background-only affine diagnostics, no world claims."""
from pathlib import Path
import cv2,numpy as np,json,subprocess,shutil
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];L=R/'local/dance-benchmark-r1';E=R/'evidence/dance-benchmark-r1'
mpidx=[0,11,12,13,14,15,16,23,24,25,26,27,28,29,30,31,32];rtidx=[0,5,6,7,8,9,10,11,12,13,14,15,16,19,22,17,20]
edges=[(0,1),(0,2),(1,2),(1,3),(3,5),(2,4),(4,6),(1,7),(2,8),(7,8),(7,9),(9,11),(8,10),(10,12),(11,13),(13,15),(12,14),(14,16)]
a=np.load(L/'mediapipe_raw.npz');b=np.load(L/'rtmw3d_raw.npz');cap=cv2.VideoCapture(str(L/'reference/reference.mp4'));cap.set(cv2.CAP_PROP_POS_FRAMES,1200)
writer=cv2.VideoWriter(str(L/'raw_overlay.avi'),cv2.VideoWriter_fourcc(*'MJPG'),60,(1440,720));sheet=Image.new('RGB',(1440,4*265),'#17202a');draw=ImageDraw.Draw(sheet);camera=[];first=None
for i in range(480):
    ok,f=cap.read();assert ok;g=cv2.cvtColor(cv2.resize(f,(960,540)),cv2.COLOR_BGR2GRAY)
    if first is None:first=g.copy()
    # Exclude all five performers conservatively; retain separated studio features.
    mask=np.ones((540,960),np.uint8)*255
    for cx in [180,300,470,650,790]:cv2.rectangle(mask,(cx-70,70),(cx+70,500),0,-1)
    warp=np.eye(2,3,dtype=np.float32)
    try:
        cc,warp=cv2.findTransformECC(first,g,warp,cv2.MOTION_AFFINE,(cv2.TERM_CRITERIA_COUNT|cv2.TERM_CRITERIA_EPS,35,1e-5),mask,5)
        camera.append({'frame':i,'ecc':float(cc),'matrix':warp.tolist()})
    except cv2.error:camera.append({'frame':i,'ecc':None,'matrix':None})
    views=[]
    for label,obs,color in [('REFERENCE',None,(255,255,255)),('MEDIAPIPE',a['xy'][i,mpidx],(0,230,255)),('RTMW3D',b['xy'][i,rtidx],(255,170,0))]:
        crop=f[100:1020,1380:1840].copy()
        if obs is not None:
            pts=obs-np.array([1380,100]);pts=np.round(pts).astype(int)
            for u,v in edges:cv2.line(crop,tuple(pts[u]),tuple(pts[v]),color,3,cv2.LINE_AA)
            for j,p in enumerate(pts):cv2.circle(crop,tuple(p),5,(0,0,255) if j%2 else (0,255,0),-1)
        crop=cv2.resize(crop,(360,720));cv2.putText(crop,label,(8,28),cv2.FONT_HERSHEY_SIMPLEX,.55,color,2);views.append(crop)
    full=cv2.resize(f,(360,203));pad=np.ones((720,360,3),np.uint8)*25;pad[200:403]=full;cv2.putText(pad,f'SOURCE {20+i/60:.3f}s',(8,80),cv2.FONT_HERSHEY_SIMPLEX,.6,(255,255,255),1);views.append(pad)
    frame=np.concatenate(views,axis=1);writer.write(frame)
    if i%30==0:
        j=i//30;row=j//4;col=j%4;img=cv2.resize(frame[:,:1080],(360,240));sheet.paste(Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB)),(col*360,row*265));draw.text((col*360+4,row*265+242),f'{20+i/60:.2f}s',fill='white')
writer.release();cap.release();sheet.save(L/'raw_overlay_contact.jpg')
subprocess.run([shutil.which('ffmpeg'),'-y','-i',str(L/'raw_overlay.avi'),'-i',str(L/'reference/reference.mp4'),'-map','0:v','-map','1:a','-af','atrim=start=20:end=28,asetpts=PTS-STARTPTS','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-t','8',str(L/'raw_overlay.mp4')],capture_output=True,check=True)
valid=[x for x in camera if x['matrix'] is not None];m=np.array([x['matrix'] for x in valid]);report={'method':'background-masked affine ECC relative to frame1200; 2D stabilization diagnostic only, not 6DOF camera estimation','frames':480,'valid':len(valid),'ecc_min':min(x['ecc'] for x in valid),'max_translation_fullres_px':float(np.linalg.norm(m[:,:,2],axis=1).max()*2),'max_affine_scale_deviation':float(np.abs(m[:,:,:2]-np.eye(2)).max()),'per_frame':camera}
(E/'segment_camera.json').write_text(json.dumps(report,indent=2));print({k:v for k,v in report.items() if k!='per_frame'})
