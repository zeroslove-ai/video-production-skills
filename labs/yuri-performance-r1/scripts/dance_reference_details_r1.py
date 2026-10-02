from pathlib import Path
import cv2,numpy as np,json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];L=R/'local/dance-benchmark-r1';E=R/'evidence/dance-benchmark-r1';cap=cv2.VideoCapture(str(L/'reference/reference.mp4'))
times=[0,.25,.5,1,2,3,4,5,6,198,200,202,204,205,206,207,207.5,207.6];sheet=Image.new('RGB',(1200,6*245),'#17202a');d=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
    cap.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=cap.read();assert ok;x=i%3*400;y=i//3*245;sheet.paste(Image.fromarray(cv2.cvtColor(cv2.resize(f,(400,225)),cv2.COLOR_BGR2RGB)),(x,y));d.text((x+4,y+226),f'{t:.3f}s',fill='white')
sheet.save(L/'dance_start_end_contact.jpg')
sheet=Image.new('RGB',(1380,2*940),'#17202a');d=ImageDraw.Draw(sheet)
for i,t in enumerate([20,21,22,23,24,25]):
    cap.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,f=cap.read();crop=f[100:1020,1380:1840];x=i%3*460;y=i//3*940;sheet.paste(Image.fromarray(cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)),(x,y))
    for gx in range(0,460,50):d.line((x+gx,y,x+gx,y+920),fill='#aaaaaa',width=1);d.text((x+gx,y+2),str(gx),fill='#ff2222')
    for gy in range(0,920,50):d.line((x,y+gy,x+460,y+gy),fill='#aaaaaa',width=1);d.text((x+2,y+gy),str(gy),fill='#ff2222')
    d.text((x+5,y+922),str(t)+'s',fill='white')
sheet.save(L/'manual_joint_annotation_grid.jpg');cap.release()
# Conventional scene-score scan across the entire reference at 2Hz; proposed cuts require visual inspection.
cap=cv2.VideoCapture(str(L/'reference/reference.mp4'));prev=None;scores=[]
for i in range(0,12457,30):
    cap.set(cv2.CAP_PROP_POS_FRAMES,i);ok,f=cap.read()
    if not ok:break
    g=cv2.cvtColor(cv2.resize(f,(320,180)),cv2.COLOR_BGR2GRAY)
    if prev is not None:scores.append([i/60,float(np.mean(cv2.absdiff(g,prev)))/255])
    prev=g
cap.release();report={'scan_fps':2,'score':'mean absolute grayscale frame difference /255; candidate detector, not proof of absence','max':max(x[1] for x in scores),'candidates_over_0_20':[x for x in scores if x[1]>.20],'per_sample':scores};(E/'cut_scan.json').write_text(json.dumps(report,indent=2));print({k:v for k,v in report.items() if k!='per_sample'})
