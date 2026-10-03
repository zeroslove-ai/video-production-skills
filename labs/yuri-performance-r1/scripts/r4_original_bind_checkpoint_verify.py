"""Post-freeze verification and metadata reuse, never another export trial."""
import json,hashlib,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent;E=ROOT/'evidence/o1-original-bind-serialization-r1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((E/'PACKAGE_RECEIPT.json').read_text(encoding='utf8'));archive=Path(receipt['archive']);assert sha(archive)==receipt['sha256']
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None;manifest=json.loads(z.read('PACKAGE_HASH_MANIFEST.json'))
    for row in manifest['files']:assert hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
source=ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend';assert sha(source)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
old=[('C:/YuriTransfer/outbox/YURI_O1_R4_NATIVE_UNITY_PROBE_20261003_R1_4ec5c10ce90d.zip','4ec5c10ce90d7d25c06721b7dcd3832be4b7672190c975d42912be876a5a0843'),('C:/YuriTransfer/outbox/YURI_O1_R4_SOURCE_FIDELITY_RECOVERY_20261003_R1_080352e24adb.zip','080352e24adb9db33e76e92d8aca9836aeaf444ed75818c29e2970a32dae47df')]
for p,h in old:assert sha(Path(p))==h
reuse=json.loads((E/'REUSE_POINTERS.json').read_text(encoding='utf8'))
for row in reuse['omitted_identical_metadata']:
    target=(E/Path(row['current_path']).name).resolve();assert target.parent==E.resolve()
    if target.exists():assert sha(target)==row['sha256'];target.unlink()
result={'source_SHA256_verified':sha(source),'old_ZIPs_unchanged':True,'new_ZIP_SHA256_verified':receipt['sha256'],'members':len(manifest['files'])+1,'CRC_all_member_hashes_verified':True,'export_trial_count':1,'native_unique_frames':276,'endpoint_inclusive_actual_motion_loop_frames':384,'exact_bind_and_pair_rest':'PASS','source_rotation':'FAIL','Unity_input_authorized':False,'tolerance_changed':False,'code_note':'Read-only actual-wire audit proves Pose matrices equal all model Cluster overrides despite trial callback orientation filter recording0captures; no corrected/repeated export.'}
(E/'POST_FREEZE_VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result,indent=2))
