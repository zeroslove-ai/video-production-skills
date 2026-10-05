"""Fresh exact scope binding to unchanged native guard for read-only consumer data."""
from pathlib import Path
import json,hashlib,copy
H=Path(__file__).resolve().parent;B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');R=B/'o1-b-pass1-existing-walk-consumer-r1';R.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
write=lambda p,v:Path(p).write_text(json.dumps(v,indent=2),encoding='utf8')
c=copy.deepcopy(json.loads((B/'o1-b-pass1-walkstop-idle-tierc-r1/FIXED_CONFIG.json').read_bytes()));collector=H/'b_pass1_existing_walk_consumer_samples_r1.py';payload=R/'PAYLOAD_CONFIG.json'
scope='ROOT_PM_WALK_UNITY_CONSUMER_SUPPLY_R1: ONE existing original native Walk1..97@24fps BODY/head/hair local TRS and exact FCurve channel data matching existing Talk116 Recipe/Channel/Key, read-only existing closed Walk candidate, source81 OFF full signature and source bytes unchanged. No save/export framework/new motion/render/contact cleanup/product edit; Tier-C/TierP0. Same600sec4GiB2CPU64MiB strict live guard.'
write(payload,{'collector_argv':[],'scope':scope});c['collector_sha256']=sha(collector)
c['pinned_files']={p:h for p,h in c['pinned_files'].items() if 'b_pass1_walkstop_idle' not in p and 'o1-b-pass1-walkstop-idle' not in p}
old=json.loads((B/'alpha-native-walk-source-r1/NATIVE_WALK_SOURCE_PRIVATE_R1.json').read_bytes())
for p in [collector,payload,Path(old['candidate']),H/'r4_appearance_adapter.py']:c['pinned_files'][str(p)]=sha(p)
argv=c['native']['argv'];argv[argv.index('--gates')+1]=str(R/'gates');argv[argv.index('--collector')+1]=str(collector);argv[argv.index('--collector-config')+1]=str(payload)
c['native'].update(gates=str(R/'gates'),capture_output=str(B/'b-pass1-existing-walk-consumer-r1'),approval_path=str(R/'NEW_EXACT_SCOPE_AUTHORITY.json'),result_path=str(R/'NATIVE_GUARD_RESULT.json'))
config=R/'FIXED_CONFIG.json';write(config,c);write(R/'NEW_EXACT_SCOPE_AUTHORITY.json',{'task':'ROOT_PM_WALK_UNITY_CONSUMER_SUPPLY_R1','new_exact_packet_authorized':True,'historical_sampler_approval_reused':False,'config_sha256':sha(config),'broker_sha256':c['broker_sha256'],'collector_sha256':c['collector_sha256'],'argv':argv,'preflight_result_sha256':sha(c['helper']['result_path']),'approval_basis':scope});print(str(config))
