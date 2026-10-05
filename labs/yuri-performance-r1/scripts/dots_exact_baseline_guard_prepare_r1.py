"""Prepare fresh exact bounded read-only comparison authority, preserving fixed guard."""
import json,hashlib
from pathlib import Path
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');G=B/'o1-dots-exact-baseline-compare-r1';G.mkdir(exist_ok=False)
L=Path('C:/Users/JAEWAN/projects/yuri-motion-previs-lab-r1/labs/yuri-performance-r1/scripts');C=L/'dots_exact_baseline_compare_r1.py'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
cfg=json.loads((B/'o1-dots-r2-readonly-custody-r1/FIXED_CONFIG.json').read_bytes());scope='ROOT_PM_DOTS_EXACT_BASELINE_CUSTODY_COMPARE_R1: Exact separately verified Dots master/control versus existing67fd96 R2. One CPU2 read-only Blender job, no save/render/export/new asset/Unity/Laptop/GUI/GPU. Original domains/common keys/actions/bind/weights comparison; canonical R4 distinct. TierP0/contact HOLD.'
payload=G/'PAYLOAD_CONFIG.json';payload.write_text(json.dumps({'collector_argv':[],'scope':scope},indent=2),encoding='utf8')
cfg['collector_sha256']=sha(C)
cfg['pinned_files']={k:v for k,v in cfg['pinned_files'].items() if not k.endswith('dots_r2_readonly_custody_r1.py') and not k.endswith('o1-dots-r2-readonly-custody-r1\\PAYLOAD_CONFIG.json')}
cfg['pinned_files'][str(C)]=sha(C);cfg['pinned_files'][str(payload)]=sha(payload)
receipt=json.loads((B/'dots-exact-baseline-inputs-r1/BASELINE_RECEIVER_RECEIPT_R1.json').read_bytes())
for a in receipt['assets']:cfg['pinned_files'][a['native']]=a['native_sha256']
n=cfg['native'];n['gates']=str(G/'gates');n['capture_output']=str(B/'dots-exact-baseline-custody-r1');n['approval_path']=str(G/'NEW_EXACT_SCOPE_AUTHORITY.json');n['result_path']=str(G/'NATIVE_GUARD_RESULT.json')
argv=n['argv'];argv[argv.index('--gates')+1]=n['gates'];argv[argv.index('--collector')+1]=str(C);argv[argv.index('--collector-config')+1]=str(payload)
config=G/'FIXED_CONFIG.json';config.write_text(json.dumps(cfg,indent=2),encoding='utf8')
approval={'task':'ROOT_PM_DOTS_EXACT_BASELINE_CUSTODY_COMPARE_R1','new_exact_packet_authorized':True,'historical_sampler_approval_reused':False,'config_sha256':sha(config),'broker_sha256':cfg['broker_sha256'],'collector_sha256':sha(C),'argv':argv,'preflight_result_sha256':sha(cfg['helper']['result_path']),'approval_basis':scope}
Path(n['approval_path']).write_text(json.dumps(approval,indent=2),encoding='utf8')
print(str(config))
