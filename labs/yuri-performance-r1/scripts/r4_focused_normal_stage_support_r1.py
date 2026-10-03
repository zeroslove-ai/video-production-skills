"""Measure existing source normal-array changes; never recalculate mesh normals."""
from pathlib import Path
import hashlib,json,numpy as np
LAB=Path(__file__).resolve().parents[1];E=LAB/'evidence/o1-normal-tess-domain-contract-r1'
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
assert not (E/'FOCUSED_NORMAL_STAGE_SUPPORT_R1.json').exists()
contract=json.loads((E/'NORMAL_TESS_DOMAIN_CONTRACT_R1.json').read_bytes());rows=[]
for case in contract['four_actual_runtime_failures']:
    p=BASE/'o1-raw-pose-driver-stage-reference-r1'/f"{case['clip']}_frame{case['source_frame']:03d}_seven_stages.npz"
    if not p.exists():continue
    corners=np.concatenate([np.arange(x['source_corner_start'],x['source_corner_start']+5) for x in case['PM_trace_polygon_instances']]);s=np.load(p)
    changes=[]
    for stage in range(1,7):
        a=s[f'stage_{stage-1:02d}_world_corner_normal'][corners];b=s[f'stage_{stage:02d}_world_corner_normal'][corners]
        aa=a.astype(np.float64);bb=b.astype(np.float64)
        angle=np.rad2deg(np.arctan2(np.linalg.norm(np.cross(aa,bb),axis=1),np.sum(aa*bb,axis=1)))
        changes.append({'from_stage':stage-1,'to_stage':stage,'source_normal_changed_CORNERs':int(np.any(a.view(np.uint32)!=b.view(np.uint32),axis=1).sum()),'max_source_stage_change_deg':float(angle.max()),'source_CORNERs_over_0_001deg':int((angle>0.001).sum())})
    rows.append({'clip':case['clip'],'source_frame':case['source_frame'],'source_CORNERs':corners.tolist(),'stage_file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_stage_normal_changes':changes})
result={'scope':'ACTUAL_FROZEN_SOURCE_NORMAL_ARRAY_MEASUREMENT_ONLY_NOT_CONSUMER_ERROR','normal_recalculation':False,'rows':rows,'rule':'Target point coordinates being unchanged does not generally freeze surrounding smooth-fan normals; original neighboring face support must be retained.'}
(E/'FOCUSED_NORMAL_STAGE_SUPPORT_R1.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result))
