"""Package only existing audit buffers/metadata. No source/export/render access."""
import json,hashlib,zipfile,shutil
from pathlib import Path
LAB=Path(__file__).resolve().parent.parent
E=LAB/'evidence/o1-source-rotation-method-audit-r1'
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-source-rotation-method-audit-r1')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files={p.name:p for p in E.iterdir() if p.suffix in ('.json','.md') and p.name!='AUDIT_PACKAGE_CUSTODY.json'}
files['frozen_evaluated_matrix_buffers.npz']=OUT/'frozen_evaluated_matrix_buffers.npz'
for n in ('r4_o1_source_rotation_method_audit.py','r4_o1_rotation_buffer_recheck.py','r4_o1_rotation_audit_package.py'):files['scripts/'+n]=LAB/'scripts'/n
manifest={'purpose':'Immutable read-only matrix-method audit; not a new character/export','files':{n:{'sha256':sha(p),'bytes':p.stat().st_size} for n,p in files.items()}}
mp=OUT/'AUDIT_CONTENT_MANIFEST.json';mp.write_text(json.dumps(manifest,indent=2),encoding='utf8');files[mp.name]=mp
outbox=Path(r'C:/YuriTransfer/outbox');temp=OUT/'audit-packet.zip'
with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n,p in files.items():z.write(p,n)
digest=sha(temp);dest=outbox/('YURI_O1_R4_ROTATION_METHOD_AUDIT_20261003_R1_'+digest[:12]+'.zip')
if dest.exists():assert sha(dest)==digest
else:shutil.copyfile(temp,dest)
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    for n,v in manifest['files'].items():assert hashlib.sha256(z.read(n)).hexdigest()==v['sha256']
receipt={'task_id':'YURI_O1_SOURCE_ROTATION_METHOD_AUDIT_R1','zip':str(dest),'sha256':digest,'bytes':dest.stat().st_size,'entries':len(files),'all_manifest_file_hashes_verified':True,'crc_verified':True,'source_or_frozen_input_mutations':0}
for p in (E/'AUDIT_PACKAGE_CUSTODY.json',OUT/'AUDIT_PACKAGE_CUSTODY.json'):p.write_text(json.dumps(receipt,indent=2),encoding='utf8')
print(json.dumps(receipt,indent=2))
