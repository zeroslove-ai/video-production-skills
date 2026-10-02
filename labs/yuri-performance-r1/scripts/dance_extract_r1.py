"""Two actual CPU estimators on the same eight-second, single-dancer ROI.

Raw observations remain untouched. RTMW3D XY output is input-pixel space,
not metres: preserve it and reconstruct later with stated camera assumptions.
"""
from pathlib import Path
import json,time,sys,os
os.environ['OMP_NUM_THREADS']='4'
import cv2,numpy as np,mediapipe as mp,onnxruntime as ort
from rtmlib import RTMPose3d
R=Path(__file__).resolve().parents[1];L=R/'local/dance-benchmark-r1';E=R/'evidence/dance-benchmark-r1'
START=20.;FPS=60;N=480;ROI=[1380,100,1840,1020];x0,y0,x1,y1=ROI
def frames():
    cap=cv2.VideoCapture(str(L/'reference/reference.mp4'));cap.set(cv2.CAP_PROP_POS_FRAMES,int(START*FPS))
    for i in range(N):
        ok,f=cap.read();assert ok;yield i,f
    cap.release()
mode=sys.argv[1];begin=time.monotonic();xy=[];xyz=[];conf=[];extra=[]
if mode=='mediapipe':
    options=mp.tasks.vision.PoseLandmarkerOptions(base_options=mp.tasks.BaseOptions(model_asset_path=str(L/'models/mediapipe_heavy.task'),delegate=mp.tasks.BaseOptions.Delegate.CPU),running_mode=mp.tasks.vision.RunningMode.VIDEO,num_poses=1,output_segmentation_masks=True)
    detector=mp.tasks.vision.PoseLandmarker.create_from_options(options);masks=L/'masks';masks.mkdir(exist_ok=True)
    for i,f in frames():
        crop=f[y0:y1,x0:x1];rgb=cv2.cvtColor(crop,cv2.COLOR_BGR2RGB)
        result=detector.detect_for_video(mp.Image(image_format=mp.ImageFormat.SRGB,data=rgb),round(i*1000/FPS))
        if result.pose_landmarks:
            p=result.pose_landmarks[0];w=result.pose_world_landmarks[0]
            xy.append([[a.x*(x1-x0)+x0,a.y*(y1-y0)+y0] for a in p]);xyz.append([[a.x,a.y,a.z] for a in w]);conf.append([[a.visibility,a.presence] for a in p])
            if result.segmentation_masks:cv2.imwrite(str(masks/f'{i:04d}.png'),np.uint8(np.clip(result.segmentation_masks[0].numpy_view()*255,0,255)))
        else:xy.append(np.full((33,2),np.nan));xyz.append(np.full((33,3),np.nan));conf.append(np.zeros((33,2)))
        if i%60==0:print(mode,i,'seconds',round(time.monotonic()-begin,1),flush=True)
    detector.close()
elif mode=='rtmw3d':
    # Construct the maintained decoder without its unlimited-thread session.
    model=RTMPose3d.__new__(RTMPose3d);model.model_input_size=(288,384);model.mean=(123.675,116.28,103.53);model.std=(58.395,57.12,57.375);model.z_range=2.1744869;model.backend='onnxruntime';model.to_openpose=False
    opt=ort.SessionOptions();opt.intra_op_num_threads=4;opt.inter_op_num_threads=1
    model.session=ort.InferenceSession(str(L/'models/rtmw3d.onnx'),sess_options=opt,providers=['CPUExecutionProvider'])
    for i,f in frames():
        p,s,simcc,p2=model(f,bboxes=[ROI]);xy.append(p2[0]);xyz.append(p[0]);conf.append(s[0]);extra.append(simcc[0])
        if i%60==0:print(mode,i,'seconds',round(time.monotonic()-begin,1),flush=True)
else:raise ValueError(mode)
out=L/(mode+'_raw.npz');np.savez_compressed(out,xy=np.array(xy),xyz=np.array(xyz),confidence=np.array(conf),simcc=np.array(extra),timestamps=np.arange(N)/FPS+START)
receipt={'estimator':mode,'frames':N,'fps':FPS,'source_start_seconds':START,'source_end_exclusive_seconds':28.,'roi_xyxy':ROI,'dancer':'white layered dress, rightmost through selected interval; appearance track, no identity attribution','elapsed_seconds':time.monotonic()-begin,'execution':'CPU_ONLY','mirror':'faithful to displayed mirrored choreography; no input horizontal flip; inferred model anatomical labels do not establish original performer anatomical sides','raw':str(out),'missing_frames':int(np.isnan(np.array(xy)).any(axis=(1,2)).sum()),'units':'MediaPipe XYZ hip-relative metres; RTMW3D raw XY input pixels and Z relative metres, deliberately not treated as homogeneous world coordinates','status':'RAW_ESTIMATION_COMPLETE_NOT_BENCHMARK_PASS'}
(E/(mode+'_extraction.json')).write_text(json.dumps(receipt,indent=2));print(receipt,flush=True)
