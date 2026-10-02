"""Fixed-camera positional arm optimization; no new extraction/model claim."""
from pathlib import Path
import json,numpy as np,sys
from scipy.optimize import least_squares,minimize
R=Path(__file__).resolve().parents[1];E=R/'evidence/dance-benchmark-r1';L=R/'local/dance-benchmark-r1';method='motionbert'
frames=json.loads((E/(method+'_retarget_joints.json')).read_text());a=np.load(L/(method+'_motion.npz'))
stable='stable' in sys.argv
camera=next(v for v in json.loads((E/'retarget_hand_trajectory_qa.json').read_text()) if v['method']==method);scale=camera['scale_px_per_m'];offset=np.array(camera['translation_px']);results=[];summary=[]
def direction(theta,phi):return np.array([np.sin(theta)*np.cos(phi),np.sin(theta)*np.sin(phi),np.cos(theta)])
def angles(v):v=v/np.linalg.norm(v);return [np.arccos(np.clip(v[2],-1,1)),np.arctan2(v[1],v[0])]
for side,ei,wi in [('L',3,5),('R',4,6)]:
    previous=None;records=[];before=[];after=[];steps=[]
    for fi,f in enumerate(frames):
        sh=np.array(f['joints']['upper_arm.'+side]['head']);el=np.array(f['joints']['forearm.'+side]['head']);wr=np.array(f['joints']['hand.'+side]['head']);u=el-sh;lo=wr-el;lu=np.linalg.norm(u);ll=np.linalg.norm(lo);seed=np.array(angles(u)+angles(lo))
        target_e=(a['xy'][fi,ei]-offset)/scale;target_w=(a['xy'][fi,wi]-offset)/scale
        conf=float(min(a['confidence'][fi,ei],a['confidence'][fi,wi])) if 'confidence' in a.files else 1.
        def points(v):d1=direction(*v[:2]);d2=direction(*v[2:]);return sh+d1*lu,sh+d1*lu+d2*ll,d1,d2
        def project(v):return np.array([v[0],-v[2]])
        def residual(v):
            e,w,d1,d2=points(v);loss=[*(.8*(project(e)-target_e)),*(1.8*(project(w)-target_w)),.35*(e[1]-el[1]),.35*(w[1]-wr[1]),*(.04*(d1-u/lu)),*(.04*(d2-lo/ll))]
            if previous is not None:loss.extend(.025*(np.r_[d1,d2]-previous))
            return np.array(loss)
        solved=least_squares(residual,seed,max_nfev=55,ftol=1e-7,xtol=1e-7,gtol=1e-7)
        values=solved.x
        if stable and previous is not None:
            cosine=np.cos(np.radians(20))
            def constraints(v):
                e,w,d1,d2=points(v);return np.array([np.dot(d1,previous[:3])-cosine,np.dot(d2,previous[3:])-cosine])
            seeds=[np.array(angles(previous[:3])+angles(previous[3:])),solved.x]
            options=[minimize(lambda v:float(np.dot(residual(v),residual(v))),v,method='SLSQP',constraints=[{'type':'ineq','fun':constraints}],options={'maxiter':80,'ftol':1e-9}) for v in seeds]
            feasible=[v for v in options if np.min(constraints(v.x))>=-1e-6]
            values=min(feasible,key=lambda v:v.fun).x if feasible else seeds[0]
        e,w,d1,d2=points(values);new=np.r_[d1,d2]
        if previous is not None:steps.append(float(max(np.degrees(np.arccos(np.clip(np.dot(previous[:3],d1),-1,1))),np.degrees(np.arccos(np.clip(np.dot(previous[3:],d2),-1,1))))))
        previous=new;be=float(np.linalg.norm(project(wr)*scale+offset-a['xy'][fi,wi]));af=float(np.linalg.norm(project(w)*scale+offset-a['xy'][fi,wi]));before.append(be);after.append(af)
        records.append({'frame':fi+1,'shoulder':sh.tolist(),'elbow':e.tolist(),'wrist':w.tolist(),'upper_length':lu,'lower_length':ll,'cost':float(solved.cost),'nfev':solved.nfev,'detector_confidence':conf,'before_wrist_error_px':be,'after_wrist_error_px':af})
    results.append({'side':side,'frames':records});summary.append({'side':side,'before_mean_px':float(np.mean(before)),'after_mean_px':float(np.mean(after)),'before_p95_px':float(np.percentile(before,95)),'after_p95_px':float(np.percentile(after,95)),'max_direction_step_deg':max(steps)})
receipt={'schema':'DANCE_ARM_REPROJECTION_R2','base_candidate_sha256':json.loads((E/'motionbert_retarget.json').read_text())['candidate_sha256'],'camera_fit_frozen_from_r1':camera,'source':'same MediaPipe2D + MotionBERT, NOT fourth extraction stack','solver':'length-constrained spherical upper/lower directions, wrist/elbow reprojection, weak depth/temporal priors','maximum_direction_step_deg':20 if stable else None,'weights':{'elbow_xy':.8,'wrist_xy':1.8,'depth_prior':.35,'direction_prior':.04,'previous_direction':.025},'frames':360,'fps':60,'scope':'source2D fit; no independent depth/world-root proof','summary':summary,'solutions':results}
(E/('arm_reprojection_r2_stable.json' if stable else 'arm_reprojection_r2.json')).write_text(json.dumps(receipt,separators=(',',':')));print(json.dumps(summary))
