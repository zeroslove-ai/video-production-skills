"""Freeze private exact review packet; public receipts contain no numeric input vectors."""
from pathlib import Path
import hashlib,json,zipfile
LAB=Path(__file__).resolve().parent.parent
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
P=BASE/'o1-morph67-native-broker-preparation-r4'
E=LAB/'evidence/o1-morph67-native-broker-review-r1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):
    with p.open('x',encoding='utf8') as f:json.dump(v,f,ensure_ascii=False,indent=2)
def main():
    assert not E.exists();E.mkdir()
    cp=P/'FIXED_BROKER_CONFIG_R1.json';cfg=json.loads(cp.read_bytes())
    rp=P/'HELPER_PREFLIGHT_RESULT_R1.json';r=json.loads(rp.read_bytes())
    assert r['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN' and not r['native_Blender_launched']
    assert r['inputs_before']==r['inputs_after']==cfg['pinned_files']
    assert r['terminal_owned_handle_signaled'] and r['terminal_exit_code']==0
    assert r['terminal_job']=={'active':0,'total':1,'limit_terminated':0,'pids':[]} and not r['cleanup_errors']
    for phase in ['BEFORE','AFTER']:
        assert r[phase]['owned_handle_signaled'] is False
        assert all(r[phase][h]['QueryFullProcessImageName_success'] and r[phase][h]['error']==0 for h in ['original','limited'])
    assert all(sha(Path(p))==h for p,h in cfg['pinned_files'].items())
    template={'task':'ROOT_PM_MORPH67_TWO_INPUT_SOURCE_NORMAL_GAP_R1',
        'new_exact_packet_authorized':False,'historical_sampler_approval_reused':False,
        'config_sha256':sha(cp),'broker_sha256':cfg['broker_sha256'],'collector_sha256':cfg['collector_sha256'],
        'argv':cfg['native']['argv'],'preflight_result_sha256':sha(rp),
        'note':'TEMPLATE ONLY. Root PM must supply new exact approval at configured native approval_path. No native launch authorized.'}
    dump(P/'NEW_APPROVAL_TEMPLATE_NOT_AUTHORIZED_R1.json',template)
    members={str(p.relative_to(P)).replace('\\','/'):p for p in P.rglob('*') if p.is_file()}
    clone=BASE/'o1-morph67-native-broker-preparation-r1/SOURCE_BYTE_CLONE_R4.blend'
    members['source/SOURCE_BYTE_CLONE_R4.blend']=clone
    failures=[]
    for tag in ['r1','r2','r3']:
        previous=BASE/('o1-morph67-native-broker-preparation-'+tag)
        receipt=previous/'HELPER_PREFLIGHT_RESULT_R1.json';old=json.loads(receipt.read_bytes())
        failures.append({'attempt':tag,'status':old['guard_status'],'receipt_path':str(receipt),'receipt_sha256':sha(receipt),
                         'pid':old['pid'],'strict_AFTER_available':'AFTER' in old,'terminal_cleanup_job':old['cleanup_job_before_close']})
        for path in [receipt,previous/'FIXED_BROKER_CONFIG_R1.json',previous/'BROKER_REVIEW_PACKET_METADATA_R1.json',*list((previous/'workflow').iterdir()),*list((previous/'helper-gates-r1').iterdir())]:
            members[f'preserved_attempts/{tag}/'+str(path.relative_to(previous)).replace('\\','/')]=path
    index={name:{'bytes':p.stat().st_size,'sha256':sha(p)} for name,p in members.items()}
    dump(P/'PRIVATE_PACKET_MEMBERS_R1.json',index);members['PRIVATE_PACKET_MEMBERS_R1.json']=P/'PRIVATE_PACKET_MEMBERS_R1.json'
    zp=BASE/'YURI_MORPH67_TWO_INPUT_BROKER_REVIEW_R1.zip';assert not zp.exists()
    with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in members.items():z.write(p,name)
    with zipfile.ZipFile(zp) as z:
        assert z.testzip() is None
        for name,meta in index.items():assert hashlib.sha256(z.read(name)).hexdigest()==meta['sha256']
    public={'capability_delta':'새 Windows 기능 없음; native 미실행 exact broker packet + harmless helper strict preflight 공급',
        'native_authorized':False,'historical_guard_FAIL_preserved':True,
        'private_packet':{'path':str(zp),'bytes':zp.stat().st_size,'sha256':sha(zp),'members':len(members),'CRC_and_private_member_SHA_verified':True},
        'final_config':{'path':str(cp),'sha256':sha(cp)},'broker':{'path':str(P/'workflow/r4_two_input_owned_barrier_broker_r1.py'),'sha256':cfg['broker_sha256']},
        'collector_sha256':cfg['collector_sha256'],'wrapper_sha256':sha(P/'workflow/r4_two_input_live_barrier_wrapper_r1.py'),
        'final_helper':{'path':str(rp),'sha256':sha(rp),'pid':r['pid'],'creation_FILETIME':r['creation_FILETIME'],'parent_pid':r['parent_pid'],
            'status':r['guard_status'],'BEFORE':r['BEFORE'],'AFTER':r['AFTER'],'terminal_exit_code':r['terminal_exit_code'],
            'terminal_job':r['terminal_job'],'combined_payload_output_bytes':r['combined_payload_output_bytes'],'wall_seconds':r['wall_seconds']},
        'previous_attempts_preserved':failures,'config':cfg,
        'scope':'PM authorized preparation+helper only. No Blender native/source evaluation/render/export/save/product write. CMD DETACHED helper PASS is not Blender guard/native normal witness.',
        'source_inputs_private_keys':'native_face ordered FACE16 and NativeYaw/NativePitch are source inputs. applied_* match. original_morph_weights is71 consumer percent outputs; source evaluates original37 active correctives and preserves13 muted bridges instead of forcing those71 values. Exact numeric inputs remain inside private packet.',
        'source_custom_normal_semantics':'Original head CORNER INT16_2D short2 encodes fan-space normal, not xyz normal delta. Current shape/GN positions alter fan spaces/cache. Capture evaluated attribute type/payload and current CORNER normals per stage; preserve original adjacency/UV/smooth. Consumer DN0 improvement with zero geometry delta does not prove source-equivalent normal.',
        'hypothesis_result':'NoWindow console helpers both failed extra Job processes despite successful BEFORE image queries. DETACHED_PROCESS cooperative BEFORE/AFTER + original/limited handle queries passed. No identity proof of old extra PID executable, so conhost cause remains hypothesis. Strict AFTER unchanged; no image error waiver/exitFILETIME terminal substitute.',
        'next':'Root PM reviews exact final config/broker/collector/packet and supplies NEW approval; native remains unrun pending that decision.'}
    dump(E/'FROZEN_BROKER_REVIEW_R1.json',public)
    print(json.dumps({'packet':public['private_packet'],'broker_SHA':cfg['broker_sha256'],'config_SHA':sha(cp),'preflight_SHA':sha(rp),'native_Blender_calls':0}))
if __name__=='__main__':main()
