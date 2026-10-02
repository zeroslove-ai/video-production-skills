"""Explicitly assumed camera reconstruction + beat-aware procedural cleanup.
No monocular absolute scale/depth ground truth is invented.
"""
from pathlib import Path
import numpy as np,json
from scipy.signal import savgol_filter
from scipy.ndimage import binary_closing,label,median_filter,maximum_filter1d
R=Path(__file__).resolve().parents[1];L=R/'local/dance-benchmark-r1';E=R/'evidence/dance-benchmark-r1';N=360;FPS=60
names=['nose','shoulder_L','shoulder_R','elbow_L','elbow_R','wrist_L','wrist_R','hip_L','hip_R','knee_L','knee_R','ankle_L','ankle_R','heel_L','heel_R','toe_L','toe_R']
indices={'mediapipe':[0,11,12,13,14,15,16,23,24,25,26,27,28,29,30,31,32],'rtmw3d':[0,5,6,7,8,9,10,11,12,13,14,15,16,19,22,17,20]}
if (L/'motionbert_raw.npz').exists():indices['motionbert']=indices['mediapipe']
reports=[]
for method,idx in indices.items():
    a=np.load(L/(method+'_raw.npz'));xy=a['xy'][:N,idx].copy();c=a['confidence'][:N,idx];c=c[:,:,0] if c.ndim==3 else c
    eyeidx=[2,5] if method in ('mediapipe','motionbert') else [1,2];eyevec=a['xy'][:N,eyeidx[0]]-a['xy'][:N,eyeidx[1]];headroll=np.arctan2(-eyevec[:,1],eyevec[:,0]);headroll=(headroll+np.pi/2)%np.pi-np.pi/2;headroll=savgol_filter(np.clip(headroll,-np.radians(40),np.radians(40)),5,2)
    hips=xy[:,7:9].mean(1);span=np.median(xy[:,[15,16],1].max(1)-xy[:,0,1])+55;ppm=span/1.65;focal=1700.;D=focal/ppm
    if method in ('mediapipe','motionbert'):
        q=a['xyz'][:N,idx].copy();q-=q[:,7:9].mean(1)[:,None,:]
        scale=1.65/np.median(q[:,[15,16],1].max(1)-q[:,0,1]+.12);q*=scale
        world=np.stack([q[:,:,0],q[:,:,2],-q[:,:,1]],axis=-1)
        root=np.stack([(hips[:,0]-hips[0,0])/ppm,np.zeros(N),-(hips[:,1]-hips[0,1])/ppm],axis=-1);world+=root[:,None,:]
        head=a['xyz'][:N,[7,8]].mean(1)-a['xyz'][:N,[23,24]].mean(1);head*=scale;head=np.stack([head[:,0],head[:,2],-head[:,1]],axis=-1)+root
    else:
        z=a['xyz'][:N,idx,2].copy();z-=z[:,7:9].mean(1)[:,None]
        cam=(xy-np.array([960,540]))/focal*(D+z)[:,:,None]
        world=np.stack([cam[:,:,0],z,-cam[:,:,1]],axis=-1);world[:,:,0]-=world[0,7:9,0].mean()
        ez=a['xyz'][:N,[3,4],2]-a['xyz'][:N,[11,12],2].mean(1)[:,None];exy=a['xy'][:N,[3,4]];ecam=(exy-[960,540])/focal*(D+ez)[:,:,None];head=np.stack([ecam[:,:,0],ez,-ecam[:,:,1]],axis=-1).mean(1);head[:,0]-=cam[0,7:9,0].mean()
    floor=np.percentile(world[:,[13,14,15,16],2],5);world[:,:,2]-=floor;head[:,2]-=floor;head_raw=head.copy();head=savgol_filter(head,7,2,axis=0)
    raw=world.copy();filtered=raw.copy();spikes=[]
    # Reject isolated reversals before preserving sharp beats. A genuine sharp
    # phrase has sustained neighbouring motion; a single-frame detector jump
    # returns immediately and would otherwise be incorrectly "preserved".
    for k in range(1,N-1):
        for j in [0,3,4,5,6,9,10,11,12,13,14,15,16]:
            before=raw[k,j]-raw[k-1,j];after=raw[k+1,j]-raw[k,j];mid=(raw[k-1,j]+raw[k+1,j])/2
            reversal=np.dot(before,after)/max(1e-9,np.linalg.norm(before)*np.linalg.norm(after))
            image_jump=np.linalg.norm(xy[k,j]-(xy[k-1,j]+xy[k+1,j])/2)
            if reversal<-.7 and np.linalg.norm(raw[k,j]-mid)>.08 and image_jump>40:
                filtered[k,j]=mid;spikes.append({'frame':k,'joint':names[j],'image_midpoint_residual_px':float(image_jump)})
    # Depth has no independently observable fast-beat evidence in this frontal
    # view. Regularize that uncertain axis separately, keep sharp image motion.
    filtered[:,:,1]=median_filter(filtered[:,:,1],size=(7,1),mode='nearest')
    smooth=savgol_filter(filtered,5,2,axis=0,mode='interp')
    # Large intentional acceleration retains raw samples, rather than broad smoothing.
    acc=np.linalg.norm(np.gradient(np.gradient(xy,axis=0),axis=0),axis=2);threshold=np.percentile(acc,85,axis=0)
    preserve=np.clip((acc-threshold)/np.maximum(threshold,1e-5),0,1);clean=smooth*(1-preserve[:,:,None]) + filtered*preserve[:,:,None]
    clean[:,:,1]=smooth[:,:,1]
    contacts=np.zeros((N,2),bool);locks=[]
    for side,ank,heel,toe in [(0,11,13,15),(1,12,14,16)]:
        sole=clean[:,[heel,toe]].mean(1);speed=np.linalg.norm(np.gradient(sole,axis=0)*FPS,axis=1);height=clean[:,[heel,toe],2].min(1)
        image_sole=median_filter(xy[:,[heel,toe]].mean(1),size=(9,1),mode='nearest');image_speed=np.linalg.norm(np.gradient(image_sole,axis=0)*FPS,axis=1);local_floor=maximum_filter1d(image_sole[:,1],size=61,mode='nearest');image_lift=local_floor-image_sole[:,1]
        # Contact decisions use image evidence, rather than noisy monocular Z.
        # This is a heuristic contact candidate, independently audited below.
        mask=(image_lift<20)&(image_speed<175)&(c[:,ank]>.4);mask=binary_closing(mask,structure=np.ones(3),border_value=1);labels,count=label(mask)
        for lab in range(1,count+1):
            frames=np.where(labels==lab)[0]
            if len(frames)<4:continue
            contacts[frames,side]=True;anchor=np.median(sole[frames,:2],axis=0);ankle_anchor=np.median(clean[frames,ank,:2],axis=0)
            for k in frames:
                # Foot observations are IK targets; knee and hip are solved by retarget.
                delta=np.r_[anchor-sole[k,:2],-height[k]];clean[k,[ank,heel,toe]]+=delta;clean[k,ank,:2]=ankle_anchor
            locks.append({'side':side,'start_frame':int(frames[0]),'end_frame':int(frames[-1]),'anchor_xy_assumed_m':anchor.tolist()})
    # Prevent floor penetration; preserve lateral root and source timing.
    penetration=np.minimum(clean[:,[13,14,15,16],2].min(1),0);clean[:,:,2]-=penetration[:,None]
    head[:,2]-=penetration
    np.savez_compressed(L/(method+'_motion.npz'),raw=raw,cleaned=clean,xy=xy,confidence=c,contacts=contacts,timestamps=np.arange(N)/FPS+20)
    motion={'schema':'dance-joint-positions-v1','joint_names':names,'fps':FPS,'start_source_seconds':20.,'coordinates':'Blender Z-up, camera-facing X; Y estimated relative depth; metre scale ASSUMED','raw':raw.tolist(),'cleaned':clean.tolist(),'head_centres_raw':head_raw.tolist(),'head_centres_cleaned':head.tolist(),'confidence':c.tolist(),'contacts':contacts.astype(int).tolist()}
    motion['head_roll_radians']=headroll.tolist();motion['head_orientation_scope']='screen-space eye-line roll only; unreliable monocular pitch/yaw not applied to rig'
    (E/(method+'_motion.json')).write_text(json.dumps(motion,separators=(',',':')))
    sliding=[]
    for side,j in [(0,15),(1,16)]:
        pairs=contacts[1:,side]&contacts[:-1,side]
        sliding.append({'side':side,'contact_frame_pairs':int(pairs.sum()),'raw_mean_speed_m_s':float(np.linalg.norm(np.diff(raw[:,j,:2],axis=0)[pairs],axis=1).mean()*FPS) if pairs.any() else None,'cleaned_mean_speed_m_s':float(np.linalg.norm(np.diff(clean[:,j,:2],axis=0)[pairs],axis=1).mean()*FPS) if pairs.any() else None})
    reports.append({'estimator':method,'fps':FPS,'frames':N,'assumed_height_m':1.65,'assumed_focal_px':focal,'derived_constant_depth_m':D,'scale_not_ground_truth':True,'camera_selected':'20–26s fixed studio seams; 26–28s excluded from final benchmark','contact_locks':locks,'sliding_internal_diagnostic_not_GT_contact_accuracy':sliding,'max_cleanup_displacement_m':float(np.linalg.norm(clean-raw,axis=2).max()),'root_x_range_assumed_m':float(np.ptp(raw[:,7:9,0].mean(1))),'root_depth_world_trajectory':'UNRESOLVED; hip-relative model depth and assumed constant camera distance cannot establish real floor trajectory','depth_uncertainty':'single camera and unknown intrinsics/body size; no metric-world PASS','sharp_preserved_samples':int((preserve>.5).sum())})
(E/'cleanup_receipt.json').write_text(json.dumps(reports,indent=2));print(json.dumps(reports,ensure_ascii=True))
