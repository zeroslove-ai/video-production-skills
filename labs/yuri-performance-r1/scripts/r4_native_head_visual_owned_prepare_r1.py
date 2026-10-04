"""Fresh source-owned guard binding for ONE measured existing Reach upper-chain correction."""
import argparse,copy,hashlib,json
from pathlib import Path
LAB=Path(__file__).resolve().parents[1]
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
 with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
ap=argparse.ArgumentParser();ap.add_argument('name');ap.add_argument('collector');ap.add_argument('output');ap.add_argument('--pin',action='append',default=[]);a=ap.parse_args()
root=BASE/a.name;root.mkdir(exist_ok=False)
c=copy.deepcopy(json.loads((BASE/'o1-alpha-a-source-hdr-broker-r2/FIXED_HDR_CONFIG_R2.json').read_bytes()))
collector=(LAB/'scripts'/a.collector).resolve();payload=root/'PAYLOAD_CONFIG.json'
scope='ROOT_PM_HEAD_BOUNDARY_CLOSE_TO_NATIVE_HEAD_VISUAL_R1: exact immutable R4 original MESHY_R2_BODY_HeadGazeHair unique complete RNA Object target resolve, existing Action only no new candidate or auxiliary FACE/GAZE/HAIR assignment. Actual97frames original24fps body/head/eye/hair/morph values and hashes, fixed headneck front/side384CPU8 captures plus original sourcecamera OFF pixel reference. No Walk contact/epsilon/precision/wholeWalk/Idle rerender or exporter/framework/corpus/rig/geometry/material/driver/identity changes. Source78/rawOFF/rest/fullweights/textures/ShapeKeys/drivers/cameras/settings exact restore; source never saved. One CPU2thread4GiB600secownedguard protectedGUI/GPU/product untouched. Unity/TierP/F2 HOLD.'
write(payload,{'collector_argv':[],'scope':scope})
c['collector_sha256']=sha(collector)
c['pinned_files']={p:h for p,h in c['pinned_files'].items() if 'r4_source_neutral_hdr_witness' not in p and 'HDR_PAYLOAD_CONFIG' not in p}
for p in [collector,payload,*map(Path,a.pin)]:c['pinned_files'][str(p)]=sha(p)
argv=c['native']['argv'];argv[argv.index('--gates')+1]=str(root/'gates');argv[argv.index('--collector')+1]=str(collector);argv[argv.index('--collector-config')+1]=str(payload)
c['native'].update(gates=str(root/'gates'),capture_output=str(BASE/a.output),approval_path=str(root/'NEW_EXACT_SCOPE_AUTHORITY.json'),result_path=str(root/'NATIVE_GUARD_RESULT.json'))
config=root/'FIXED_CONFIG.json';write(config,c)
write(root/'NEW_EXACT_SCOPE_AUTHORITY.json',{'task':'ROOT_PM_HEAD_BOUNDARY_CLOSE_TO_NATIVE_HEAD_VISUAL_R1','new_exact_packet_authorized':True,'historical_sampler_approval_reused':False,'config_sha256':sha(config),'broker_sha256':c['broker_sha256'],'collector_sha256':c['collector_sha256'],'argv':argv,'preflight_result_sha256':sha(c['helper']['result_path']),'approval_basis':scope})
print(json.dumps({'config':str(config),'collector_SHA':c['collector_sha256']},indent=2))
