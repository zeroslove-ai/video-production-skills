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
write(payload,{'collector_argv':[],'scope':'ROOT_PM_INDEPENDENT_STAGE_AB_TALK_SOURCE_R1; after closing two neutral-return failures, one independent grounded StageA/B upper-body TalkGesture motion from existing66Action source; no third neutral solver. Immutable R4/rest/skin/geometry/material/drivers/original78Actions, native quaternion-only Action addition, actual stationary foot/root and rigid headhair/OFF/reopen/1x QA, no Unity/product/export rig changes'})
c['schema']='ALPHA_WALK_TURN_SOURCE_OWNED_FIXED_SCOPE_R1';c['collector_sha256']=sha(collector)
c['pinned_files']={p:h for p,h in c['pinned_files'].items() if 'r4_source_neutral_hdr_witness' not in p and 'HDR_PAYLOAD_CONFIG' not in p}
for p in [collector,payload,*map(Path,a.pin)]:c['pinned_files'][str(p)]=sha(p)
argv=c['native']['argv'];argv[argv.index('--gates')+1]=str(root/'gates');argv[argv.index('--collector')+1]=str(collector);argv[argv.index('--collector-config')+1]=str(payload)
c['native'].update(gates=str(root/'gates'),capture_output=str(BASE/a.output),approval_path=str(root/'NEW_EXACT_SCOPE_AUTHORITY.json'),result_path=str(root/'NATIVE_GUARD_RESULT.json'))
config=root/'FIXED_CONFIG.json';write(config,c)
write(root/'NEW_EXACT_SCOPE_AUTHORITY.json',{'task':'ROOT_PM_INDEPENDENT_STAGE_AB_TALK_SOURCE_R1','new_exact_packet_authorized':True,'historical_sampler_approval_reused':False,'config_sha256':sha(config),'broker_sha256':c['broker_sha256'],'collector_sha256':c['collector_sha256'],'argv':argv,'preflight_result_sha256':sha(c['helper']['result_path']),'approval_basis':'Trusted Root PM 01a0ff8a-5bc8-7541-a876-e39fcc7941bf explicitly instructed one R2 alternative to neutral restoration, and after repeated failure move that research to nonblocking and return one independent StageA/B source motion supply item. R1 and one R2 closed as FAIL/HOLD; this exact new packet inspects/reuses existing immutable original66Action TalkGesture for ONE native upper-body source candidate. Preserve source/rig/rest/skin/material/driver/all original78Actions, grounded actual feet/root, transient source-only body/head/hair ownership and fixed1x/OFF evidence. No original guard changes, GPU inference, new donor/model, product or Unity write, no third neutral solver. Operator exact collector/argv binding only; old scope approval not reused.'})
print(json.dumps({'config':str(config),'approval':c['native']['approval_path'],'collector_SHA':c['collector_sha256'],'limits':c['limits']},indent=2))
