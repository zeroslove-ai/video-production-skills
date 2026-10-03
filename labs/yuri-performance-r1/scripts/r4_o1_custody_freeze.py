"""Verify and copy an existing immutable custody ZIP. No Blender/export work.

Existing differing outbox bytes are a hard failure; never replace them.
All source/rejected artifacts and PM seed records are read-only inputs.
"""
import hashlib,json,shutil,stat,subprocess,zipfile
from pathlib import Path
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[1]
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
BASE='YURI_O1_R4_APPEARANCE_PRESERVE_20261003_407cda9db7b4'
E=ROOT/'evidence/o1-desktop-custody-freeze-r1'
OUTBOX=Path(r'C:/YuriTransfer/outbox')
SOURCE=OUT/'YURI_R4_APPEARANCE_PRESERVE_CORRECTION_R1.zip'
DEST=OUTBOX/(BASE+'.zip')
EXPECTED='407cda9db7b45053f8fbb3e83467fa4888db456f31ebec376e1701c70d4f2d64'
SOURCE_SHA='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
PRODUCER='820a23791d17838b101296b50c87fd7564db791f'
PARENT='08caad76e6a279d07698cbfaa33d5c50f2aa097d'
REMOTE='https://github.com/zeroslove-ai/video-production-skills.git'
BRANCH='research/yuri-performance-previs-r1-20261002'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO,text=True).strip()
def json_bytes(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf8')
def immutable_write(p,data):
    if p.exists():
        assert p.read_bytes()==data, f'Differing existing receipt: {p}; not overwritten'
        return
    with p.open('xb') as f:f.write(data)
def evidence(name,data):
    p=E/name
    if p.exists():assert p.read_bytes()==data, f'Differing evidence already exists: {p}'
    else:p.write_bytes(data)

assert git('branch','--show-current')==BRANCH
assert git('remote','get-url','origin')==REMOTE
head=git('rev-parse','HEAD');assert head==PRODUCER,head
remote_head=git('ls-remote','--heads','origin',BRANCH).split()[0]
assert remote_head==head,(head,remote_head)
subprocess.run(['git','merge-base','--is-ancestor',PARENT,head],cwd=REPO,check=True)
assert SOURCE.stat().st_size==62446950 and sha(SOURCE)==EXPECTED
native_source=ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
assert sha(native_source)==SOURCE_SHA
members=[]
with zipfile.ZipFile(SOURCE) as z:
    assert z.testzip() is None
    names=z.namelist();assert len(names)==len(set(names))==41
    assert all(not n.startswith(('/','\\')) and '..' not in Path(n).parts for n in names)
    manifest=json.loads(z.read('Character_R4_AssetManifest_CORRECTIVE.json'))
    for f in manifest['files']:
        b=z.read(f['path']);assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
    unlisted=set(names)-{f['path'] for f in manifest['files']}
    assert unlisted=={'Character_R4_AssetManifest_CORRECTIVE.json','metadata/corrective_manifest.json'},unlisted
    assert z.read('Character_R4_AssetManifest_CORRECTIVE.json')==z.read('metadata/corrective_manifest.json')
    assert hashlib.sha256(z.read('source/Character_Master_NeckSkin_R4.blend')).hexdigest()==SOURCE_SHA
    for n in names:
        b=z.read(n);members.append({'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
    preservation=json.loads(z.read('metadata/preservation_receipt.json'))
    for n in ['append_diff','reopen_diff','on_off_diff']:assert json.loads(z.read(f'metadata/{n}.json'))=={}
    for n in ['pixels_authority_source_camera','pixels_full_body_QA']:
        assert all(c['PASS'] and c['unequal_channels']==0 for c in json.loads(z.read(f'metadata/{n}.json')).values())
    clips=json.loads(z.read('metadata/all_frame_motion.json'))['clips']
    assert len(clips)==6 and all(c['native_motion']=='PASS' for c in clips)
    library=json.loads(z.read('metadata/action_library_only.json'))
    assert all(library[k]==0 for k in ['objects','meshes','armatures','materials','images'])

# Independently verify the final historical FBXs, including the old sealed ZIP.
historical=OUT/'r4-model-handoff'
legacy_manifest=json.loads((historical/'Character_R4_AssetManifest.json').read_text())
current=[]
for name in ['Character_GameRig_R4_20261002.fbx','YURI_REACTION_R4_ANIMATION_ONLY.fbx']:
    p=historical/name;row={'file':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
    assert row['bytes']==legacy_manifest['files'][name]['bytes'] and row['sha256']==legacy_manifest['files'][name]['sha256']
    current.append(row)
old_zip=OUT/'YURI_R4_MODEL_HANDOFF_R1.zip'
assert sha(old_zip)=='48d3a241566823991801011a63ebc7e76b2c8821c6b87aaf8d013791e6330f85'
with zipfile.ZipFile(old_zip) as z:
    for row in current:
        key=Path(row['file']).name
        choices=[n for n in z.namelist() if n==key or n.endswith('/'+key)]
        assert len(choices)==1,choices
        assert hashlib.sha256(z.read(choices[0])).hexdigest()==row['sha256']
rejected=[{'file':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted((historical/'rejected-rest-delta').glob('*.fbx'))]
seed_path=Path(r'C:/Users/JAEWAN/projects/yuri-root-pm-r1/docs/pm/YURI_ROOT_PM_WORKSTREAMS_R1.md')
seed_text=seed_path.read_text(encoding='utf8')
seed=[{'file':'Character_GameRig_R4_20261002.fbx','bytes':24914028,'sha256':'012b93322bcedeb473f65cc651eb28c503ba95fef5ef9b4301bbdc687d93773f','bones_reported_by_PM':125},
      {'file':'YURI_REACTION_R4_ANIMATION_ONLY.fbx','bytes':6320428,'sha256':'117b0fb96ee2d68f08841c33a6a87191318558ccaf299bcb9c5cddc206ad173e','bones_reported_by_PM':125}]
assert all(s['sha256'].upper() in seed_text for s in seed)
export=json.loads(git('show',PARENT+':labs/yuri-performance-r1/evidence/model-handoff-r4/game_export.json'))
assert export['bone_count']==79 and len(export['export_only_removed_unweighted_donor_bones'])==46
lineage={'PM_seed_record':{'path':str(seed_path),'sha256_of_record':sha(seed_path),'entries':seed},
    '08caad7_final_manifest_current_files':current,'final_manifest_sha256':sha(historical/'Character_R4_AssetManifest.json'),
    '08caad7_old_sealed_zip':{'path':str(old_zip),'sha256':sha(old_zip),'matching_final_FBX_bytes_verified':True},
    'preserved_rejected_snapshots':rejected,'committed_08caad7_export_bones':79,'committed_removed_unused_donor_bones':export['export_only_removed_unweighted_donor_bones'],
    'verified_conclusion':'PM seed125-bone hashes are NOT the final08caad7 79-bone pair. Final bytes match both historical manifest and sealed original handoff ZIP. Corrective820a237 instead preserves original four rigs and uses Action library only.',
    'inference':'57+57+10+RuntimeRoot=125 and removal of46 donor bones yields79. This explains structural candidate-stage difference, but does NOT prove exact012B/117B byte lineage.',
    'unresolved':'Exact012B/117B FBX binaries were not found in checked asset outputs; rejected snapshots also have different hashes. No exact generation timestamp/build provenance is claimed for PM seed bytes.',
    'records_changed':False,'old_FBX_packaged_for_new_custody':False}

rigs=json.loads((ROOT/'evidence/model-handoff-r4/R4.json').read_text())['rigs']
rig_contract={n:{'bone_count':len(v['bones']),'parent':v['parent'],'matrix_world':v['matrix_world'],
    'bones':v['bones']} for n,v in rigs.items()}
actual_frames={'Startle_Short':37,'Lift_Start':31,'Struggle_Light_Loop':61,'Struggle_Strong_Loop':49,'Land_Soft':43,'BalanceRecover':55}
contract={'marker':'YURI_O1_DESKTOP_CUSTODY_FROZEN','owner':'DESKTOP_ASSET','producer_repository':{'remote':REMOTE,'branch':BRANCH,'asset_commit':PRODUCER,'parent_historical_commit':PARENT,'origin_head_verified_at_freeze':remote_head,'origin_matches_asset_checkpoint':True},
    'source_master':{'path':str(native_source),'member':'source/Character_Master_NeckSkin_R4.blend','sha256':SOURCE_SHA,'bytes':26553642,'immutable_visual_authority':True},
    'action_asset':next(f for f in members if f['path']=='YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'),
    'OFF_preserving_master':next(f for f in members if f['path']=='Character_R4_Animation_OFF_20261003.blend'),
    'rig_contract_evidence':'rig_contract.json','rest_and_scale_assumptions':{'basis':'original Blender Z-up native A-rest; original helper bind poses are nonidentity and must remain intact','Meshy_Fitted_Rig_object_uniform_scale':0.535,'scene_unit_scale':1.0,'do_not_apply_scale_or_rebuild':True,'binding':'original Meshy_Fitted_Rig quaternion channels; OBMeshy_Fitted_Rig Action slot; retain face/hair constraints and drivers','retarget_translation_height_ratio':0.8558494790405046,'Unity_axis_unit_Avatar_rest_conversion':'NOT certified; must be specified by Laptop consumer before any export'},
    'actual_clips':[{'action':'YRA_R4_'+n,'frames':f,'duration_seconds':(f-1)/24,'fps':24,'loop':'Loop' in n,'native_PASS':True} for n,f in actual_frames.items()],
    'QA_only_not_production':[{'action':'YRA_R4_QA_Release_Placeholder','frames':19,'duration_seconds':0.75,'status':'placeholder, NOT completed release or physics motion'},{'action':'YRA_R4_QA_MilestoneA_Sequence','frames':265,'duration_seconds':11,'status':'QA sequence helper, NOT seventh physical clip'}],
    'preservation_acceptance':{'source_bytes_identical':True,'geometry_material_slots_ShapeKeys_weights_rest_pose_drivers_hash_differences':0,'OFF_neutral_RGBA_channel_differences':0,'ON_then_OFF_RGBA_channel_differences':0,'native_reactions':6,'loop_cycles_tested':2,'new_asset_generation_in_custody_task':0},
    'defects_and_limits':['CPU preview sampling noise is retained; no material edit to hide it.','Physical world-space lift/drop/release trajectory and Active Ragdoll are not implemented.','Face phoneme A/O readability remains weak in prior native face audit; no new expression promotion or raw face mapping.','Original native DQ+masked LBS+surface relax, gaze Geometry Nodes and drivers are preserved in Blender; FBX cannot encode their behavior by itself.','GameRig125/79 FBX candidates are historical compatibility experiments ONLY, never canonical source character.','Python ReactionLane is Blender-only original-hierarchy ON/OFF restoration, not a Unity Runtime adapter or exported Unity animation controller.'],
    'exact_consumers':[{'owner':'Root PM O1','workspace':r'C:\Users\JAEWAN\projects\yuri-root-pm-r1','branch':'pm/yuri-root-pm-r1','requested_by_thread':'01a0ff8a-5bc8-7541-a876-e39fcc7941bf','input':str(DEST),'responsibility':'custody/contract reconciliation and cross-host transfer; not performed here'},{'owner':'Laptop Unity O1 consumer','target_branch_reported_by_PM':'work/yuri-unity-avatar-sandbox-u0-r1','owner_identity':'awaiting Root PM/Laptop requirements; no thread or host identity invented','input':'verified source R4 + Action-only library + contract after Root PM transfer','status':'Unity adaptation/import/export gates BLOCKED pending requirements; no Laptop/product writes'}],
    'blocked_Unity_export_gates':['Laptop must return exact native Avatar rig/hierarchy paths, rest pose, import axis/unit/globalScale and Generic vs Humanoid requirements.','Laptop must identify current source-preserving geometry/material/gaze/hair adapter and DQ/LBS/surface-relax tolerance; no body merge/substitution.','Agree animation-only export format and original FittedRig57 bind paths; original face/hair follower-driver hierarchy must remain separately owned.','Consumer must run state-entered, normalized-time advanced, weight>0, AlwaysAnimate, actual nonroot motion, no root teleport, no gross mesh break, loops2cycles.','Neutral Unity before/after render and geometry/material/morph/weights/rest gates must be met before any appearance promotion.','Physics profile/G1/G2/G3/Windows Player and VRM/Humanoid facial gates are external consumer work; Desktop Blender PASS does not certify them.'],
    'stop_condition':'No new Blender export or asset production until Laptop requirements are returned; custody verified only.'}

OUTBOX.mkdir(parents=True,exist_ok=True);E.mkdir(parents=True,exist_ok=True)
if DEST.exists():assert DEST.stat().st_size==62446950 and sha(DEST)==EXPECTED, 'Differing existing ZIP: NEVER overwrite'
else:
    with SOURCE.open('rb') as src,DEST.open('xb') as dst:shutil.copyfileobj(src,dst,1024*1024)
assert sha(DEST)==EXPECTED and DEST.stat().st_size==62446950
with zipfile.ZipFile(DEST) as z:assert z.testzip() is None
DEST.chmod(stat.S_IREAD) # Destination custody copy only; source/prior outputs unchanged.
hash_manifest={'zip':{'path':str(DEST),'bytes':62446950,'sha256':EXPECTED},'members':members,'member_count':41,'CRC':'PASS','declared_per_file_manifest':'PASS','all_members_SHA256':'recorded','additional_self_manifests_only':sorted(unlisted)}
receipt={'marker':'YURI_O1_DESKTOP_CUSTODY_FROZEN','created_utc':datetime.now(timezone.utc).isoformat(),'source_zip':str(SOURCE),'frozen_zip':str(DEST),'bytes':62446950,'sha256':EXPECTED,'copied_bytes_unchanged':True,'destination_read_only':True,'ZIP_CRC_and_member_manifest':'PASS','source_R4_SHA256':SOURCE_SHA,'original_source_and_all_prior_artifacts_unchanged':True,'producer_asset_checkpoint':PRODUCER,'origin_match':True,'consumer':'Root PM O1; cross-host transfer is PM responsibility','Blender_UI_or_exports_used':False,'Unity_export':'BLOCKED; await Laptop exact contract','historical_seed_lineage':'final pair verified; exact seed012B/117B binaries unverified; see lineage.json'}
for name,value in [('hash_manifest.json',hash_manifest),('contract.json',contract),('rig_contract.json',rig_contract),('lineage.json',lineage),('receipt.json',receipt)]:
    data=json_bytes(value);evidence(name,data)
    immutable_write(OUTBOX/(BASE+'.'+name),data)
readme='''# O1 Desktop custody freeze — 2026-10-03

This is custody of the already-completed source-preserving corrective820a237 package. No rebuild, Blender UI, source edit, retarget/export, motion production, Unity code or cross-host transfer performed.

Frozen ZIP: C:/YuriTransfer/outbox/YURI_O1_R4_APPEARANCE_PRESERVE_20261003_407cda9db7b4.zip
Bytes: 62446950
SHA256: 407cda9db7b45053f8fbb3e83467fa4888db456f31ebec376e1701c70d4f2d64
Source R4 SHA256: a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa

ZIP CRC, embedded per-file manifest, all41 member hashes, copied ZIP SHA and immutable native source hash verified. The outbox ZIP is read-only. Existing differing destinations fail rather than being replaced. Original corrective/old ZIPs and08caad7/820a237 remain intact.

Producer: https://github.com/zeroslove-ai/video-production-skills.git, research/yuri-performance-previs-r1-20261002, asset820a23791d17838b101296b50c87fd7564db791f. Origin matched that asset checkpoint before custody evidence work. New evidence commit is reported separately after push.

contract.json: source and OFF master, Action-only asset SHA/bytes, four original rigs and native rest/scale/bind assumptions, six actual24fps clips, QA-only release placeholder/sequence, defects, exact consumers and blocked Unity gates. rig_contract.json contains source bone names, parent hierarchy and rest matrices; it is metadata, not a rig rebuild. Blender-only adapter does not implement Unity or Active Ragdoll.

lineage.json preserves PM seed012B.../117B... values and record hash. They describe a125-bone pair, whereas final08caad7 evidence prunes46 unused donor bones and final manifest identifies79 bones / current30094D.../83A6B... bytes. Current final bytes also match the sealed historical08caad7 bundle. Rejected snapshots are preserved but have different hashes from the PM seed. The125→79 stage explanation is supported structurally; the exact seed binaries/build provenance were not located and remain explicitly UNVERIFIED. No historical PM record was corrected/overwritten and no old compatibility FBX was inserted into the source-preserving custody ZIP.

Consumers: Root PM O1 at C:/Users/JAEWAN/projects/yuri-root-pm-r1 branchpm/yuri-root-pm-r1 owns transfer/contract reconciliation. Laptop Unity branchwork/yuri-unity-avatar-sandbox-u0-r1 is reported by PM; exact owner/import/export requirements remain pending. No new export is scheduled until target native hierarchy, axis/unit/rest/import settings, animation-only format and source-preserving face/gaze/hair/material/deformation adapter requirements are returned. AlwaysAnimate and full actual-motion/neutral/visual/physics/player gates remain consumer work.

Evidence-only checkpoint. No appearance promotion. No GameRig reconstruction, mesh merge, body substitution, donor geometry or source change.
'''
evidence('CUSTODY_CONTRACT_KO.md',readme.encode('utf8'))
immutable_write(OUTBOX/(BASE+'.CUSTODY_CONTRACT.md'),readme.encode('utf8'))
print(json.dumps(receipt,indent=2));print('CUSTODY_FREEZE_VERIFIED')
