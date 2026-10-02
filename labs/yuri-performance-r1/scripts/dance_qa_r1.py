"""Sparse independent image audit plus full-interval diagnostics, labelled scope."""
from pathlib import Path
import numpy as np,json,cv2
from scipy.signal import correlate,find_peaks
R=Path(__file__).resolve().parents[1];L=R/'local/dance-benchmark-r1';E=R/'evidence/dance-benchmark-r1';ann=json.loads((E/'manual_joint_annotations.json').read_text());names=json.loads((E/'mediapipe_motion.json').read_text())['joint_names'];idx=[names.index(n) for n in ann['joint_order']];reports=[]
reference_contacts=[{'source_seconds':20,'L':True,'R':True},{'source_seconds':21,'L':True,'R':True},{'source_seconds':22,'L':True,'R':True},{'source_seconds':23,'L':True,'R':True},{'source_seconds':24,'L':False,'R':True},{'source_seconds':25,'L':True,'R':True}]
for method in ['mediapipe','rtmw3d']+(['motionbert'] if (E/'motionbert_retarget_joints.json').exists() else []):
    a=np.load(L/(method+'_motion.npz'));xy=a['xy'];errors=[];perjoint={n:[] for n in ann['joint_order']};hands=[]
    for sample in ann['samples']:
        fi=round((sample['source_seconds']-20)*60)
        for j,(n,p) in enumerate(zip(ann['joint_order'],sample['xy_crop'])):
            if p is None:continue
            err=float(np.linalg.norm(xy[fi,idx[j]]-(np.array(p)+ann['crop_origin'])));errors.append(err);perjoint[n].append(err)
            if 'wrist' in n:hands.append(err)
    joints=json.loads((E/(method+'_retarget_joints.json')).read_text());root=np.array([v['root'] for v in joints]);feet=np.array([[v['joints']['foot.'+side]['head'] for side in ['L','R']] for v in joints]);hip2d=xy[:,7:9].mean(1)
    # One global scale and translation; no per-frame alignment that could hide root drift.
    coef=np.polyfit(root[:,0],hip2d[:,0],1);fit_x=np.polyval(coef,root[:,0]);root_error=np.abs(fit_x-hip2d[:,0])
    sliding=[]
    for side in [0,1]:
        pairs=a['contacts'][1:,side]&a['contacts'][:-1,side]
        sliding.append({'side':side,'contact_pairs':int(pairs.sum()),'retarget_ankle_xy_mean_speed_m_s':float(np.linalg.norm(np.diff(feet[:,side,:2],axis=0)[pairs],axis=1).mean()*60) if pairs.any() else None})
    matches=[]
    for sample in reference_contacts:
        fi=round((sample['source_seconds']-20)*60)
        for side,key in [(0,'L'),(1,'R')]:matches.append(bool(a['contacts'][fi,side])==sample[key])
    # Pelvis rhythm against original estimator observations over all360frames.
    # This is cleanup timing preservation, NOT independent music beat accuracy.
    source=hip2d[:,1]-hip2d[:,1].mean();ret=root[:,2]-root[:,2].mean();c=correlate(source,-ret,mode='full');lag=int(np.argmax(c)-(len(source)-1))
    # Silhouette proxy audit: inferred capsules vs MediaPipe person mask.
    # Mask is model-derived and clothing/character proportions differ.
    ious=[];edges=[(1,3),(3,5),(2,4),(4,6),(1,7),(2,8),(7,9),(9,11),(8,10),(10,12)]
    for fi in range(360):
        maskp=L/'masks'/f'{fi:04d}.png';mask=cv2.imread(str(maskp),0)>128;caps=np.zeros(mask.shape,np.uint8);p=np.round(xy[fi]-[1380,100]).astype(int)
        cv2.fillConvexPoly(caps,p[[1,2,8,7]],1);cv2.circle(caps,tuple(p[0]),60,1)
        for u,v in edges:cv2.line(caps,tuple(p[u]),tuple(p[v]),1,35 if u in [1,2,3,4] else 50)
        union=np.logical_or(caps,mask).sum();ious.append(float(np.logical_and(caps,mask).sum()/union) if union else 0.)
    qa=json.loads((E/(method+'_retarget_allframe_qa.json')).read_text());retarget=json.loads((E/(method+'_retarget.json')).read_text())
    reports.append({'estimator':method,'major_joint_manual_audit':{'samples':len(errors),'mean_error_px':float(np.mean(errors)),'p95_error_px':float(np.percentile(errors,95)),'manual_uncertainty_px':15,'per_joint_mean_px':{n:float(np.mean(v)) for n,v in perjoint.items()},'limitation':'six sparse audited frames, not full360-frame joint ground truth; independent from estimator outputs'},'hand_trajectory_sparse_wrist_error_px':float(np.mean(hands)),'foot_contact_sparse_audit':{'labels':12,'matched':sum(matches),'accuracy_fraction':float(np.mean(matches)),'limitation':'visible shoe contact estimate at six frames, no force/3D ground truth'},'retarget_contact_sliding':sliding,'root_lateral_fit':{'one_global_scale_px_per_m':float(coef[0]),'mae_px':float(root_error.mean()),'range_px':float(np.ptp(hip2d[:,0])),'range_assumed_m':float(np.ptp(root[:,0])),'world_floor_depth_accuracy':'UNRESOLVED'},'cleanup_pelvis_rhythm_lag_frames':lag,'cleanup_pelvis_rhythm_lag_ms':lag/60*1000,'music_beat_accuracy':'NOT_ESTABLISHED_BY_SELF_TIMING_METRIC','silhouette_model_capsule_proxy':{'mean_iou':float(np.mean(ious)),'minimum_iou':min(ious),'scope':'all360frames; inferred skeleton capsules against model-derived person mask, not Blender mesh silhouette accuracy'},'left_right':'model anatomical label convention preserved on displayed MIRRORED video; manual audit uses same convention, no performer anatomical unmirror claim','retarget_allframe':qa,'direction_repairs_count':len(retarget['direction_outlier_repairs']),'verdict':'FAIL_ACCURATE_REUSABLE_DANCE_GATE: metric world depth/root unresolved, residual contact and sparse-only independent accuracy audit; do not extend to chorus/full'})
(E/'motion_qa_report.json').write_text(json.dumps({'reference_contacts_sparse':reference_contacts,'candidates':reports},indent=2));print(json.dumps([{k:v for k,v in d.items() if k not in ['retarget_allframe','left_right','silhouette_model_capsule_proxy']} for d in reports],ensure_ascii=True))
