"""File-only additive receiver packet; retains earlier frozen data ZIP."""
from pathlib import Path
import hashlib,json,shutil,zipfile
LAB=Path(__file__).resolve().parent.parent
E=LAB/'evidence/o1-exact-local-stage-capture-result-r2'
OUT=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-exact-source-local-stage-capture-r2')

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def write(p,v):
    with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2)

def main():
    original=OUT/'YURI_O1_EXACT_SOURCE_LOCAL_TWO_FRAME_R2.zip'
    assert sha(original)=='e37bd95aa5327a9734d7c90170d68b4371e712231a09dfc7441fc8e2db042e8f'
    pm=Path('C:/Users/JAEWAN/projects/yuri-root-pm-r1/docs/evidence/root-pm-o1/PM_EXACT_NATIVE_LOCAL_CAPTURE_R2_INDEPENDENT_REVIEW_R1.json')
    assert sha(pm)=='c94e9bed40c0dcd85c02325f3ff62676b300223c6c4db315ed1b10f01b9c478a'
    shutil.copyfile(pm,E/pm.name);assert sha(E/pm.name)==sha(pm)
    contract=LAB/'evidence/o1-normal-tess-domain-contract-r1/NORMAL_TESS_DOMAIN_CONTRACT_R1.json'
    assert sha(contract)=='0e6e0e6693639e93fafe0647ff104dbd44b3ad11e5ca49ded671997b1fae9552'
    additions=[E/'SOURCE_LOCAL_DOMAIN_HANDOFF_R2.md',E/pm.name,contract,Path(__file__),LAB/'scripts/r4_freeze_exact_local_capture_result_r2.py']
    receiver=OUT/'YURI_O1_EXACT_SOURCE_LOCAL_RECEIVER_HANDOFF_R2.zip'
    members={}
    with zipfile.ZipFile(original) as src,zipfile.ZipFile(receiver,'x',zipfile.ZIP_DEFLATED) as dst:
        assert src.testzip() is None
        for n in src.namelist():
            value=src.read(n);dst.writestr(n,value)
            members[n]={'bytes':len(value),'sha256':hashlib.sha256(value).hexdigest()}
        for p in additions:
            assert p.name not in members
            dst.write(p,p.name);members[p.name]={'bytes':p.stat().st_size,'sha256':sha(p)}
    with zipfile.ZipFile(receiver) as z:
        assert z.testzip() is None
        for n,row in members.items():assert hashlib.sha256(z.read(n)).hexdigest()==row['sha256']
    receipt={'status':'ACTUAL_TWO_FRAME_NATIVE_DATA_AND_OWNED_JOB_SCOPED_ACCEPTED_RECEIVER_PACKET_FROZEN','packet':str(receiver),'bytes':receiver.stat().st_size,'sha256':sha(receiver),'original_data_packet_sha256':sha(original),'PM_scoped_review_sha256':sha(pm),'ZIP_CRC_and_all_member_SHA_verified':True,'members':members,'raw_geometry_only_in_private_packet_not_public_Git':True,'first_consumer_stage_divergence':'PENDING_ACTUAL_CONSUMER_ARRAY_COMPARISON','native_cache_branch':'UNKNOWN_NOT_READ','R1_R5_FAIL_history':'PRESERVED'}
    write(E/'RECEIVER_PACKET_CUSTODY_R2.json',receipt)
    write(OUT/'RECEIVER_PACKET_CUSTODY_R2.json',receipt)
    outbox=Path('C:/YuriTransfer/outbox')/('YURI_O1_EXACT_SOURCE_LOCAL_RECEIVER_HANDOFF_R2_'+sha(receiver)[:12])
    assert not outbox.exists();outbox.mkdir(parents=True)
    shutil.copyfile(receiver,outbox/receiver.name);assert sha(outbox/receiver.name)==sha(receiver)
    write(E/'RECEIVER_PRIVATE_TRANSFER_OUTBOX_R2.json',{'path':str(outbox/receiver.name),'bytes':receiver.stat().st_size,'sha256':sha(receiver),'remote_receiver_custody':'NOT_CONFIRMED_BY_THIS_DESKTOP_FILE_COPY'})
    print(json.dumps({'packet_bytes':receiver.stat().st_size,'packet_sha256':sha(receiver),'outbox':str(outbox/receiver.name),'remote_receiver_custody':'NOT_CONFIRMED_BY_THIS_DESKTOP_FILE_COPY'}))

if __name__=='__main__':main()
