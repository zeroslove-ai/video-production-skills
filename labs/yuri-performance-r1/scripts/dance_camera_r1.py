"""Static studio line checks reject unreliable performer-contaminated ECC."""
from pathlib import Path
import cv2,numpy as np,json
R=Path(__file__).resolve().parents[1];L=R/'local/dance-benchmark-r1';E=R/'evidence/dance-benchmark-r1';cap=cv2.VideoCapture(str(L/'reference/reference.mp4'));rows=[]
for idx in range(0,12457,30):
    cap.set(cv2.CAP_PROP_POS_FRAMES,idx);ok,f=cap.read()
    if not ok:break
    g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY);profile=np.abs(np.diff(g[20:140].astype(float),axis=1)).mean(0)
    lines=[int(lo+np.argmax(profile[lo:hi])) for lo,hi in [(350,650),(1250,1500)]]
    floor=np.mean(g[:,np.r_[0:220,1850:1920]],axis=1);gradient=np.abs(np.diff(floor));floor_y=int(700+np.argmax(gradient[700:960]));rows.append([idx/60,*lines,floor_y])
cap.release();a=np.array(rows);sel=a[(a[:,0]>=20)&(a[:,0]<28)];d={'method':'two high studio-wall vertical seams plus floor/wall edge away from performers; line positions are image diagnostics, not camera intrinsics or world calibration','samples_2hz':rows,'selected_segment':{'seam_x_peak_to_peak_px':np.ptp(sel[:,1:3],axis=0).tolist(),'seam_spacing_peak_to_peak_px':float(np.ptp(sel[:,2]-sel[:,1])),'floor_y_peak_to_peak_px':float(np.ptp(sel[:,3]))},'ecc_rejected':'low correlation min0.343 and implausible302px translation despite stationary studio seams; performer-contaminated affine estimates must not modify root','whole_video_camera':'framing changes visible later; no universal static-camera assumption'}
(E/'studio_camera_lines.json').write_text(json.dumps(d,indent=2));print(d['selected_segment'])
