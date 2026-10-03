"""Post-freeze verification outside immutable ZIP; no circular commit self-hash."""
import json,hashlib,subprocess,zipfile
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent.parent;E=ROOT/'evidence/o1-source-fidelity-recovery-r1';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-source-fidelity-recovery-r1');receipt=json.loads((E/'PACKAGE_RECEIPT.json').read_text(encoding='utf8'))
digest=hashlib.sha256();total=0
for row in receipt['raw_split_parts']:
    p=Path(row['path']);raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sha256'];digest.update(raw);total+=len(raw)
assert digest.hexdigest()==receipt['sha256'] and total==receipt['bytes']
with zipfile.ZipFile(receipt['archive']) as z:
    assert z.testzip() is None;manifest=json.loads(z.read('PACKAGE_HASH_MANIFEST.json'))
    for row in manifest['files']:assert hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
source=ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend';sourcehash=hashlib.sha256(source.read_bytes()).hexdigest();assert sourcehash=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
a=np.load(OUT/'data/Strong_1_49_deformation_layer_ablation.npz');b=np.load(OUT/'data/motion_Struggle_Strong_Loop_1.npz');copydelta=float(np.linalg.norm(a['native_full_frame1']-b['Meshy_Body_NeutralCovered_world_position'],axis=1).max());assert copydelta<1e-6
probe=Path('C:/YuriTransfer/outbox/YURI_O1_R4_NATIVE_UNITY_PROBE_20261003_R1_4ec5c10ce90d.zip');assert hashlib.sha256(probe.read_bytes()).hexdigest()=='4ec5c10ce90d7d25c06721b7dcd3832be4b7672190c975d42912be876a5a0843'
receipt={'source_SHA256_verified':sourcehash,'prior_frozen_probe_unchanged':True,'package_SHA256':receipt['sha256'],'split_reassembly_SHA256_verified':True,'split_total_bytes':total,'zip_CRC_member_hashes_verified':True,'zip_members':len(manifest['files'])+1,'staged_copy_native_full_vs_original_max_world_vertex_delta_m':copydelta,'parent_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'quality_reference_read':{'PM_AGENTS_blob':'1e022e0bab56fac7292371d95c0a77bc25dcf29a','MOTION_PERFORMANCE_NORTH_STAR_blob':'fce303892cff42b004cdb311b5025ce078909ff4'},'next':'PM REVIEW / consumer adapter feasibility; source mute policy and strict bind representation unresolved'}
(E/'POST_FREEZE_VERIFICATION.json').write_text(json.dumps(receipt,indent=2),encoding='utf8')
# Avoid recommitting metadata already present verbatim at parent d204379b.
# Only newly generated corrective evidence paths are removed; OUT files and all
# frozen original checkpoints remain intact. Exact reuse pointers are committed.
deduplicated=json.loads((E/'DUPLICATE_OMISSION_POINTERS.json').read_text(encoding='utf8'))
for row in deduplicated:
    target=(E/'static-correction'/Path(row['omitted_current_path']).name).resolve()
    assert target.parent==(E/'static-correction').resolve()
    if target.exists():
        assert hashlib.sha256(target.read_bytes()).hexdigest()==row['sha256']
        target.unlink()
print(json.dumps(receipt,indent=2))
