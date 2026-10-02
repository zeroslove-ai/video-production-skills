"""All-frame retarget wrist projection diagnostic with one fixed alignment."""
from pathlib import Path
import json,numpy as np
R=Path(__file__).resolve().parents[1]; E=R/'evidence/dance-benchmark-r1'; L=R/'local/dance-benchmark-r1'; out=[]
for m in ['mediapipe','rtmw3d','motionbert']:
    a=np.load(L/(m+'_motion.npz')); frames=json.loads((E/(m+'_retarget_joints.json')).read_text())
    mapping=[('upper_arm.L',1),('upper_arm.R',2),('thigh.L',7),('thigh.R',8)]
    p=np.array([[f['joints'][b]['head'] for b,i in mapping] for f in frames])[:,:,[0,2]]; p[:,:,1]*=-1
    target=a['xy'][:,[i for b,i in mapping]]
    # Single isotropic orthographic fit of all shoulder/hip frames. Approximate
    # camera and proportional fit; cannot establish world-space accuracy.
    pc=p.reshape(-1,2); tc=target.reshape(-1,2); scale=float(np.sum((pc-pc.mean(0))*(tc-tc.mean(0)))/np.sum((pc-pc.mean(0))**2)); offset=tc.mean(0)-scale*pc.mean(0)
    sides=[]
    for side,i in [('L',5),('R',6)]:
        wrist=np.array([f['joints']['hand.'+side]['head'] for f in frames])[:,[0,2]]; wrist[:,1]*=-1; projected=wrist*scale+offset; err=np.linalg.norm(projected-a['xy'][:,i],axis=1)
        sides.append({'side':side,'mean_error_px':float(err.mean()),'p95_error_px':float(np.percentile(err,95)),'maximum_error_px':float(err.max())})
    out.append({'method':m,'frames':360,'projection':'one all-frame isotropic orthographic fit to shoulders/hips, no per-frame alignment','scope':'retarget wrist vs estimator2D observations; independent sparse manual audit is separate; unknown perspective and body proportions affect metric','scale_px_per_m':scale,'translation_px':offset.tolist(),'wrist_trajectories':sides})
(E/'retarget_hand_trajectory_qa.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out))
