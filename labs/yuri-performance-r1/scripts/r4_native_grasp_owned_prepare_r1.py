"""Prepare a new exact, source-owned fixed-scope broker packet; never edit guards."""
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
write(payload,{'collector_argv':[],'scope':'ROOT_PM_NATIVE_TALK_SOURCE_REVIEW_NEXT_EXISTING_WAVE_R1; existing Wave f1621cc2 and A3 look-listen already supplied, no duplicate. ONE still-missing existing native GraspHoldRelease source hand interaction: preserve immutable R4/rest/weights/material/driver/original78Actions; native upper/finger Action copy only, grounded lower/root and neutral/OFF source restoration, actual BOTH dominant arm/hand surface QA and matched fixed1x views. No third replant solver, donor, exporter/framework, product or Unity changes.'})
c['schema']='ALPHA_WALK_TURN_SOURCE_OWNED_FIXED_SCOPE_R1';c['collector_sha256']=sha(collector)
c['pinned_files']={p:h for p,h in c['pinned_files'].items() if 'r4_source_neutral_hdr_witness' not in p and 'HDR_PAYLOAD_CONFIG' not in p}
for p in [collector,payload,*map(Path,a.pin)]:c['pinned_files'][str(p)]=sha(p)
argv=c['native']['argv'];argv[argv.index('--gates')+1]=str(root/'gates');argv[argv.index('--collector')+1]=str(collector);argv[argv.index('--collector-config')+1]=str(payload)
c['native'].update(gates=str(root/'gates'),capture_output=str(BASE/a.output),approval_path=str(root/'NEW_EXACT_SCOPE_AUTHORITY.json'),result_path=str(root/'NATIVE_GUARD_RESULT.json'))
config=root/'FIXED_CONFIG.json';write(config,c)
write(root/'NEW_EXACT_SCOPE_AUTHORITY.json',{'task':'ROOT_PM_NATIVE_TALK_SOURCE_REVIEW_NEXT_EXISTING_WAVE_R1','new_exact_packet_authorized':True,'historical_sampler_approval_reused':False,'config_sha256':sha(config),'broker_sha256':c['broker_sha256'],'collector_sha256':c['collector_sha256'],'argv':argv,'preflight_result_sha256':sha(c['helper']['result_path']),'approval_basis':'Trusted Root PM 01a0ff8a-5bc8-7541-a876-e39fcc7941bf accepted source-only TalkGesture custody and explicitly instructed ONE existing native Wave next, or if Wave already supplied return its exact evidence and choose ONE still-missing existing look/listen or social motion instead of duplicate. Existing authored Wave packet f1621cc2 and A3 look/listen76a006e5 are already supplied. Select one original66 native GraspHoldRelease hand-oriented interaction component, reuse existing source quaternion curves on immutable R4, preserve original78Actions/source/rig/rest/skin/material/driver, grounded actual feet/root, neutral/OFF source restoration, dominant BOTH arm/hand actual surfaces and fixed1x views. Physics/prop/gaze/facial/Unity/TierP promotion separate. No third replant solver/new donor/new export/framework/laptop or product write. Operator exact new scope binding only, previous approvals not reused.'})
print(json.dumps({'config':str(config),'approval':c['native']['approval_path'],'collector_SHA':c['collector_sha256'],'limits':c['limits']},indent=2))
