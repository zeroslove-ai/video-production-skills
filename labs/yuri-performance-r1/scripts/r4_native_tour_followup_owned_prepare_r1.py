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
scope='ROOT_PM_NATIVE_SEAT_CLOSE_TO_TOUR_SOURCE_R1: after original769 native Tour source author/data guard terminal, sequential sameSHA ONLY followup: exact all769 actual saved native geometry+dynamictriangles BVH surface identities; or one fixedfront/quarter/side256CPU2sample full769 native24fps view with exact recorded actualBODYHEADHAIR perframegeometry SHA, OFF960sourceRGBA, source78signature restoration. Original32sec clock tracks/root turn/foot intent preserved, no authoring/retarget/contact correction/pose/rerenderduplication/source saves. Existing original headhair fullworld transport revalidated; no seat-derived additiveblindadapter. Same600sec4GiB2CPU strict ownedjob, protectedGUI/GPUlease/product/Laptop/Unity unchanged. One native worker at time. Scopecontact+whole1x+OFFPASS required before supply packet; failures evidence only.'
write(payload,{'collector_argv':[],'scope':scope})
c['collector_sha256']=sha(collector)
c['pinned_files']={p:h for p,h in c['pinned_files'].items() if 'r4_source_neutral_hdr_witness' not in p and 'HDR_PAYLOAD_CONFIG' not in p}
for p in [collector,payload,*map(Path,a.pin)]:c['pinned_files'][str(p)]=sha(p)
argv=c['native']['argv'];argv[argv.index('--gates')+1]=str(root/'gates');argv[argv.index('--collector')+1]=str(collector);argv[argv.index('--collector-config')+1]=str(payload)
c['native'].update(gates=str(root/'gates'),capture_output=str(BASE/a.output),approval_path=str(root/'NEW_EXACT_SCOPE_AUTHORITY.json'),result_path=str(root/'NATIVE_GUARD_RESULT.json'))
config=root/'FIXED_CONFIG.json';write(config,c)
write(root/'NEW_EXACT_SCOPE_AUTHORITY.json',{'task':'ROOT_PM_NATIVE_SEAT_CLOSE_TO_TOUR_SOURCE_R1','new_exact_packet_authorized':True,'historical_sampler_approval_reused':False,'config_sha256':sha(config),'broker_sha256':c['broker_sha256'],'collector_sha256':c['collector_sha256'],'argv':argv,'preflight_result_sha256':sha(c['helper']['result_path']),'approval_basis':scope})
print(json.dumps({'config':str(config),'collector_SHA':c['collector_sha256']},indent=2))
