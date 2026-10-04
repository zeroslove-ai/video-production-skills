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
write(payload,{'collector_argv':[],'scope':'ROOT_PM_C1_BASELINE_CONTACT_PATH_R1; one minimally changed LEFT upper-arm pose-path derivative of existing C1; original R4/prior C1/R1/R2 Actions preserved; same R2 finger timing; body/root/feet/facehair fixed; evaluated contact/finite/pop/OFF/reopen/4-view1x source QA'})
c['schema']='ALPHA_WALK_TURN_SOURCE_OWNED_FIXED_SCOPE_R1';c['collector_sha256']=sha(collector)
c['pinned_files']={p:h for p,h in c['pinned_files'].items() if 'r4_source_neutral_hdr_witness' not in p and 'HDR_PAYLOAD_CONFIG' not in p}
for p in [collector,payload,*map(Path,a.pin)]:c['pinned_files'][str(p)]=sha(p)
argv=c['native']['argv'];argv[argv.index('--gates')+1]=str(root/'gates');argv[argv.index('--collector')+1]=str(collector);argv[argv.index('--collector-config')+1]=str(payload)
c['native'].update(gates=str(root/'gates'),capture_output=str(BASE/a.output),approval_path=str(root/'NEW_EXACT_SCOPE_AUTHORITY.json'),result_path=str(root/'NATIVE_GUARD_RESULT.json'))
config=root/'FIXED_CONFIG.json';write(config,c)
write(root/'NEW_EXACT_SCOPE_AUTHORITY.json',{'task':'ROOT_PM_C1_BASELINE_CONTACT_PATH_R1','new_exact_packet_authorized':True,'historical_sampler_approval_reused':False,'config_sha256':sha(config),'broker_sha256':c['broker_sha256'],'collector_sha256':c['collector_sha256'],'argv':argv,'preflight_result_sha256':sha(c['helper']['result_path']),'approval_basis':'Trusted Root PM 01a0ff8a-5bc8-7541-a876-e39fcc7941bf explicitly delegated one minimal C1 LEFT wrist/arm pose-path derivative for inherited hand/body contact at1..7 and50..61; one world-outward upper-arm hypothesis with unchanged body/root/feet/facehair/skin/rest/materials/drivers; reused R2 finger timing, actual same-frame paired surface, pop and normal-speed source QA, preserving existing RIGHT Action and original78Actions; disjoint channels/common clock; neutral/contact/physics/Unity/MUG HOLD, original source/rig/skin/rest/material/face drivers preserved, OFF/native/three-view normal-speed QA and existing delivery; no Unity release, maintaining original guard. Operator command binding only; no claim of independent prior review of this collector. Installed readonly guard and historical receipts unchanged.'})
print(json.dumps({'config':str(config),'approval':c['native']['approval_path'],'collector_SHA':c['collector_sha256'],'limits':c['limits']},indent=2))
