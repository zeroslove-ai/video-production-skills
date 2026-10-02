"""All360 actual-mesh silhouettes vs model-derived selected-person masks."""
from pathlib import Path
import json,cv2,numpy as np,hashlib,subprocess,shutil
R=Path(__file__).resolve().parents[1];E=R/'evidence/dance-benchmark-r1';L=R/'local/dance-benchmark-r1';methods=['motionbert','motionbert_reprojection_stable'];render={m:json.loads((E/(m+'_silhouette_render.json')).read_text()) for m in methods};scores={m:[] for m in methods};clipped={m:0 for m in methods};counts={m:[] for m in methods};writer=cv2.VideoWriter(str(L/'silhouette_compare.avi'),cv2.VideoWriter_fourcc(*'MJPG'),30,(690,500));cap=cv2.VideoCapture(str(L/'reference/reference.mp4'));cap.set(cv2.CAP_PROP_POS_FRAMES,1200)
for fi in range(360):
    source=cv2.resize(cv2.imread(str(L/'masks'/f'{fi:04d}.png'),0),(230,460),interpolation=cv2.INTER_AREA)>128;images=[]
    for m in methods:
        rgba=cv2.imread(str(Path(render[m]['render_folder'])/f'{fi:04d}.png'),cv2.IMREAD_UNCHANGED);assert rgba.shape==(460,230,4);mask=rgba[:,:,3]>128;assert mask.any();union=np.logical_or(mask,source).sum();scores[m].append(float(np.logical_and(mask,source).sum()/union));counts[m].append(int(mask.sum()));clipped[m]+=int(mask[0].any() or mask[-1].any() or mask[:,0].any() or mask[:,-1].any());over=np.zeros((460,230,3),np.uint8);over[source]=(0,140,0);over[mask]=(0,0,170);over[mask&source]=(30,200,220);images.append(over)
    ok,f=cap.read();assert ok
    if fi%2==0:
        original=cv2.resize(f[100:1020,1380:1840],(230,460));frame=np.zeros((500,690,3),np.uint8);frame[30:490]=np.concatenate([original,*images],axis=1)
        for j,label in enumerate(['REFERENCE','BEFORE MESH','AFTER MESH']):cv2.putText(frame,label,(j*230+5,20),cv2.FONT_HERSHEY_SIMPLEX,.42,(245,245,245),1)
        writer.write(frame)
        if fi==180:cv2.imwrite(str(L/'silhouette_compare_poster.jpg'),frame)
cap.release();writer.release();movie=L/'silhouette_compare_6sec.mp4';subprocess.run([shutil.which('ffmpeg'),'-y','-i',str(L/'silhouette_compare.avi'),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(movie)],capture_output=True,check=True)
report={'frames':360,'resolution':[230,460],'source_mask':'MediaPipe model-derived segmentation, not independently annotated ground truth; neighbouring actor overlap and skirt/clothing remain','geometry':'actual Blender skinned proxy mesh alpha, no capsule approximation; identical frozen camera before/after','color_legend':'green source-mask only / red target-mesh only / yellow intersection','candidates':[{'method':m,'candidate_sha256':render[m]['candidate_sha256'],'mean_iou':float(np.mean(scores[m])),'minimum_iou':min(scores[m]),'frame_ious':scores[m],'clipped_boundary_frames':clipped[m],'mesh_area_pixel_range':[min(counts[m]),max(counts[m])]} for m in methods],'comparison_sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'verdict':'PARTIAL_IMAGE_FIT_IMPROVEMENT_NOT_CHARACTER_SILHOUETTE_OR_WORLD_MOTION_PASS'}
(E/'actual_mesh_silhouette_qa_r2.json').write_text(json.dumps(report,indent=2));print(json.dumps([{k:v for k,v in d.items() if k!='frame_ious'} for d in report['candidates']]))
