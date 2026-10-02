"""Manual label and time-domain audit of retarget before/after, frozen camera."""
from pathlib import Path
import json,numpy as np
from scipy.signal import find_peaks,correlate
R=Path(__file__).resolve().parents[1];E=R/'evidence/dance-benchmark-r1';L=R/'local/dance-benchmark-r1';ann=json.loads((E/'heldout_wrist_annotations_r2.json').read_text());camera=json.loads((E/'arm_reprojection_r2.json').read_text())['camera_fit_frozen_from_r1'];scale=camera['scale_px_per_m'];offset=np.array(camera['translation_px']);data=np.load(L/'motionbert_motion.npz');audio=np.array(json.loads((E/'audio_reference_analysis.json').read_text())['selected_segment_audio_onsets_seconds'])
reports=[];baseline=json.loads((E/'motionbert_retarget_joints.json').read_text())
for method in ['motionbert','motionbert_reprojection','motionbert_reprojection_stable']:
    frames=json.loads((E/(method+'_retarget_joints.json')).read_text());points={};manual=[];timing=[]
    for side,index in [('L',5),('R',6)]:
        p=np.array([f['joints']['hand.'+side]['head'] for f in frames])[:,[0,2]];p[:,1]*=-1;points[side]=p*scale+offset
        reference=data['xy'][:,index];rs=np.linalg.norm(np.diff(reference,axis=0),axis=1)*60;ps=np.linalg.norm(np.diff(points[side],axis=0),axis=1)*60
        lag=int(np.argmax(correlate(rs-rs.mean(),ps-ps.mean(),mode='full'))-(len(rs)-1))
        peaks=find_peaks(rs,prominence=100,distance=12)[0];pks=find_peaks(ps,prominence=100,distance=12)[0]
        deltas=[float(min(abs(pks-i))/60*1000) for i in peaks] if len(pks) else []
        onset_distance=[float(min(abs(audio-(20+i/60)))*1000) for i in pks]
        timing.append({'side':side,'reference_detector_speed_peak_seconds':(20+peaks/60).tolist(),'retarget_speed_peak_seconds':(20+pks/60).tolist(),'speed_curve_crosscorrelation_lag_ms':lag/60*1000,'reference_peak_nearest_retarget_mean_abs_delta_ms':float(np.mean(deltas)) if deltas else None,'retarget_peak_nearest_audio_transient_mean_abs_delta_ms':float(np.mean(onset_distance)) if onset_distance else None,'scope':'detector/reference image speed vs retarget; signal transients are not choreography beat labels; no timing PASS from proximity alone'})
    for sample in ann['samples']:
        fi=round((sample['source_seconds']-20)*60)
        for j,side in enumerate(['L','R']):
            p=sample['xy_crop'][j]
            if p is None:continue
            manual.append({'source_seconds':sample['source_seconds'],'side':side,'error_px':float(np.linalg.norm(points[side][fi]-(np.array(p)+ann['crop_origin'])))})
    untouched=['hips','spine','chest','neck','head','thigh.L','shin.L','foot.L','thigh.R','shin.R','foot.R'];err=max(np.linalg.norm(np.array(f['joints'][b]['head'])-np.array(baseline[i]['joints'][b]['head'])) for i,f in enumerate(frames) for b in untouched)
    qa=json.loads((E/(method+'_retarget_allframe_qa.json')).read_text());reports.append({'method':method,'manual_label_points':len(manual),'manual_uncertainty_px':20,'manual_mean_error_px':float(np.mean([v['error_px'] for v in manual])),'manual_p95_error_px':float(np.percentile([v['error_px'] for v in manual],95)),'manual_samples':manual,'timing':timing,'nonarm_head_position_max_change_m':float(err),'rotation_max_step_deg':qa['max_quaternion_step_deg'],'verdict':'FAIL_TEMPORAL_POP' if qa['max_quaternion_step_deg']>40 else 'IMPROVED_IMAGE_FIT_NOT_WORLD_DANCE_PASS'})
(E/'reprojection_qa_r2.json').write_text(json.dumps({'camera_frozen':camera,'manual_scope':ann['scope'],'candidates':reports},indent=2));print(json.dumps([{k:v for k,v in d.items() if k not in ['manual_samples','timing']} for d in reports]))
