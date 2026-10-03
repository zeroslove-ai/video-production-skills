"""Preserve reviewed draft identity before additive revision; never edits frozen inputs."""
from pathlib import Path
import hashlib, json
LAB=Path(__file__).resolve().parent.parent
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-guarded-native-resource-sizing-r1')
def put(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():assert p.read_bytes()==data, 'frozen draft overwrite'
    else:p.write_bytes(data)
for n in ('PROPOSED_GUARDED_NATIVE_V2.diff','NATIVE_V2_REVIEW_RECEIPT.json'):
    put(OUT/'drafts/v2r2'/n,(OUT/n).read_bytes())
for n in ('host_readback.cpp','host_readback.h','host_readback_guard.h'):
    s=(LAB/'scripts/native_readback_proposal'/n).read_text()
    put(OUT/'drafts/v2r2/native_readback_proposal'/n,s.encode())
    s=s.replace('#include <tbb/global_control.h>\n','').replace('    tbb::global_control hard_limit(tbb::global_control::max_allowed_parallelism, 4);\n','')
    s=s.replace('''    if (audit) {
      std::fprintf(audit, "{\\"scope_ended\\":true,\\"denied_attempts\\":%u,\\"CPU_contexts\\":%u}\\n",
                   denied.load(), cpu_contexts.load());
      std::fflush(audit);
    }
''','')
    put(OUT/'drafts/v2r1/native_readback_proposal'/n,s.encode())
code=(LAB/'scripts/r4_guarded_native_proposal_v2.py').read_text()
put(OUT/'drafts/v2r2/generator.py',code.encode())
code=code.replace("(LAB/'scripts/native_readback_proposal'/local)","(OUT/'drafts/v2r1/native_readback_proposal'/local)")
code=code.replace("OUT/'PROPOSED_GUARDED_NATIVE_V2.diff'","OUT/'drafts/v2r1/PROPOSED_GUARDED_NATIVE_V2.diff'")
code=code.replace("OUT/'NATIVE_V2_REVIEW_RECEIPT.json'","OUT/'drafts/v2r1/NATIVE_V2_REVIEW_RECEIPT.json'")
exec(compile(code,'reconstruct-reviewed-uncompiled-draft','exec'))
p=OUT/'drafts/v2r1/PROPOSED_GUARDED_NATIVE_V2.diff';digest=hashlib.sha256(p.read_bytes()).hexdigest()
known='f99667313fd214e91d8e05e5f9ddfbdf67e376bee497837cb1b3d2a0f5659dbb'
receipt={'previous_review_hash':known,'reconstructed_hash':digest,'reviewed_hash_exactly_recovered':digest==known,
 'current_v2r2_hash':hashlib.sha256((OUT/'drafts/v2r2/PROPOSED_GUARDED_NATIVE_V2.diff').read_bytes()).hexdigest(),
 'status':'UNCOMPILED_DRAFTS_ONLY_NO_APPROVAL_INHERITANCE',
 'method':'Known textual changes reverted, complete pinned-source diff regenerated, SHA256 exact comparison'}
put(OUT/'drafts/DRAFT_CUSTODY.json',json.dumps(receipt,indent=2).encode())
print(json.dumps(receipt))
