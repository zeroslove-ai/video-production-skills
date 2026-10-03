"""Freeze existing data in independently readable <=100MiB ZIP volumes.
Usage: python this.py gaze|body|weights|bind|basis|corners|modifiers|rawpose|normals|renderdeps|cyclesinputs|cyclesmikk|zerotrace|nativezero|readbackprep. No Blender/source access.
"""
import sys,json,hashlib,zipfile
from pathlib import Path
LAB=Path(__file__).resolve().parent.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
mode=sys.argv[-1];assert mode in ('gaze','body','weights','bind','basis','corners','modifiers','rawpose','normals','renderdeps','cyclesinputs','cyclesmikk','zerotrace','nativezero','readbackprep','resourcestage1','resourcestage2')
slug='o1-gaze-evaluated-corner-reference-r1' if mode=='gaze' else 'o1-full-body-deformation-reference-r1'
name='GAZE_EVALUATED_CORNER_MANIFEST.json' if mode=='gaze' else 'FULL_BODY_DEFORMATION_MANIFEST.json'
prefix='YURI_O1_R4_GAZE_EVALUATED_CORNERS_20261003_R1' if mode=='gaze' else 'YURI_O1_R4_FULL_BODY_DEFORMATION_20261003_R1'
if mode=='weights':
    slug='o1-all-bind-and-weight-diagnostic-r1';name='ALL_BIND_AND_WEIGHT_DIAGNOSTIC_RECEIPT.json'
    prefix='YURI_O1_R4_ALL_BIND_WEIGHT_DIAGNOSTIC_20261003_R1'
if mode=='bind':
    slug='o1-bind-transport-contract-r1';name='EXACT_BIND_TRANSPORT_SOURCE_CONTRACT.json'
    prefix='YURI_O1_R4_BIND_TRANSPORT_SOURCE_CONTRACT_20261003_R1'
if mode=='basis':
    slug='o1-renderer-basis-diagnostic-r1';name='RENDERER_BASIS_DIAGNOSTIC_MANIFEST.json'
    prefix='YURI_O1_R4_RENDERER_BASIS_DIAGNOSTIC_20261003_R1'
if mode=='corners':
    slug='o1-source-corner-identity-support-r1';name='SOURCE_CORNER_IDENTITY_RECEIPT.json'
    prefix='YURI_O1_R4_SOURCE_CORNER_IDENTITY_20261003_R1'
if mode=='modifiers':
    slug='o1-body-modifier-source-contract-r1';name='BODY_MODIFIER_SOURCE_CONTRACT.json'
    prefix='YURI_O1_R4_BODY_MODIFIER_SOURCE_CONTRACT_20261003_R1'
if mode=='rawpose':
    slug='o1-raw-pose-driver-stage-reference-r1';name='RAW_POSE_DRIVER_STAGE_MANIFEST.json'
    prefix='YURI_O1_R4_RAW_POSE_DRIVER_STAGES_20261003_R1'
if mode=='normals':
    slug='o1-corner-normal-tangent-semantics-r1';name='CORNER_NORMAL_TANGENT_SEMANTIC_RECEIPT.json'
    prefix='YURI_O1_R4_CORNER_NORMAL_TANGENT_SEMANTICS_20261003_R1'
if mode=='renderdeps':
    slug='o1-body-render-tangent-dependency-r1';name='BODY_RENDER_TANGENT_DEPENDENCY_RECEIPT.json'
    prefix='YURI_O1_R4_BODY_RENDER_TANGENT_DEPENDENCY_20261003_R1'
if mode=='cyclesinputs':
    slug='o1-dynamic-body-cycles-input-reference-r1';name='DYNAMIC_BODY_CYCLES_INPUT_MANIFEST.json'
    prefix='YURI_O1_R4_DYNAMIC_BODY_CYCLES_INPUTS_20261003_R1'
if mode=='cyclesmikk':
    slug='o1-pinned-cycles-triangle-mikk-cpu-reference-r1';name='PINNED_CYCLES_TRIANGLE_MIKK_CPU_MANIFEST.json'
    prefix='YURI_O1_R4_PINNED_CYCLES_TRIANGLE_MIKK_20261003_R1'
if mode=='zerotrace':
    slug='o1-pinned-mikk-zero-trace-r1';name='PINNED_MIKK_ZERO_TRACE.json'
    prefix='YURI_O1_R4_PINNED_MIKK_ZERO_TRACE_20261003_R1'
if mode=='nativezero':
    slug='o1-native-mikk-zero-cause-trace-r1';name='NATIVE_MIKK_ZERO_CAUSE_MANIFEST.json'
    prefix='YURI_O1_R4_NATIVE_MIKK_ZERO_CAUSE_20261003_R1'
if mode=='readbackprep':
    slug='o1-actual-cycles-readback-preparation-r1';name='READBACK_PREPARATION_MANIFEST.json'
    prefix='YURI_O1_R4_CYCLES_READBACK_PREPARATION_20261003_R1'
if mode in ('resourcestage1','resourcestage2'):
    version='r1' if mode=='resourcestage1' else 'r2'
    slug='o1-guarded-native-resource-sizing-'+version;name='GUARDED_NATIVE_RESOURCE_MANIFEST.json'
    prefix='YURI_O1_R4_GUARDED_NATIVE_RESOURCE_20261003_'+version.upper()
E=LAB/'evidence'/slug;OUT=BASE/slug
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
manifest=json.loads((E/name).read_text(encoding='utf8'));digest=sha(E/name)
data=manifest['chunks' if mode=='body' else 'files']
files={v['path']:OUT/v['path'] for v in data}
for v in data:assert sha(files[v['path']])==v['sha256'] and files[v['path']].stat().st_size==v['bytes']
for p in E.iterdir():
    if p.suffix in ('.md','.json') and p.name!='PACKET_CUSTODY.json':files['metadata/'+p.name]=p
script='r4_gaze_evaluated_corner_reference.py' if mode=='gaze' else 'r4_full_body_deformation_reference.py'
if mode=='weights':script='r4_all_bind_and_weight_diagnostic.py'
if mode=='bind':script='r4_bind_transport_contract.py'
if mode=='basis':script='r4_renderer_basis_diagnostic.py'
if mode=='corners':script='r4_source_corner_identity_support.py'
if mode=='modifiers':script='r4_body_modifier_source_contract.py'
if mode=='rawpose':script='r4_raw_pose_driver_stage_reference.py'
if mode=='normals':script='r4_corner_normal_tangent_semantics.py'
if mode=='renderdeps':script='r4_body_render_tangent_dependency.py'
if mode=='cyclesinputs':script='r4_dynamic_body_cycles_input_reference.py'
if mode=='cyclesmikk':script='r4_pinned_cycles_mikk_cpu_reference.py'
if mode=='zerotrace':script='r4_pinned_mikk_zero_trace.py'
if mode=='nativezero':script='r4_native_mikk_zero_cause_trace.py'
if mode=='readbackprep':script='r4_installed_blender_pdb_inventory.py'
if mode=='resourcestage1':script='r4_native_resource_packet_finalize.py'
if mode=='resourcestage2':script='r4_native_resource_stage2_finalize.py'
for n in (script,'r4_source_reference_packet_freeze.py'):files['scripts/'+n]=LAB/'scripts'/n
if mode=='rawpose':
    for n in ('r4_raw_pose_driver_stage_verify.py','r4_appearance_signature.py','r4_appearance_adapter.py','native_preservation.py'):
        files['scripts/'+n]=LAB/'scripts'/n
if mode=='cyclesinputs':
    for n in ('r4_dynamic_body_cycles_input_recover.py','r4_appearance_signature.py','r4_appearance_adapter.py','native_preservation.py'):
        files['scripts/'+n]=LAB/'scripts'/n
if mode=='cyclesmikk':
    for n in ('r4_pinned_cycles_mikk_build.py','r4_pinned_cycles_mikk_harness.cpp'):
        files['scripts/'+n]=LAB/'scripts'/n
    for p in (OUT/'upstream').rglob('*'):
        if p.is_file():files[str(p.relative_to(OUT)).replace('\\','/')]=p
    for p in OUT.iterdir():
        if p.suffix in ('.cpp','.inc','.cmd','.log','.dll') or p.name=='download_receipt.json':files[p.name]=p
if mode=='nativezero':
    for n in ('r4_native_mikk_zero_cause_setup.py','r4_native_mikk_diagnostic_hooks.h'):
        files['scripts/'+n]=LAB/'scripts'/n
if mode=='readbackprep':
    files['scripts/r4_prepare_guarded_host_readback_patch.py']=LAB/'scripts/r4_prepare_guarded_host_readback_patch.py'
if mode in ('resourcestage1','resourcestage2'):
    for n in ('r4_guarded_native_proposal_v2.py','r4_guarded_native_proposal_v3.py',
              'r4_native_resource_text_receipts.py','r4_native_strong6_expected_inputs.py',
              'r4_freeze_native_drafts.py','r4_appearance_signature.py',
              'r4_appearance_adapter.py','native_preservation.py'):
        files['scripts/'+n]=LAB/'scripts'/n
    for p in (LAB/'scripts/native_readback_proposal').iterdir():
        files['scripts/native_readback_proposal/'+p.name]=p
file_manifest={n:{'sha256':sha(p),'bytes':p.stat().st_size} for n,p in files.items()}
dest=Path(r'C:/YuriTransfer/outbox')/(prefix+'_'+digest[:12]);dest.mkdir(exist_ok=True)
groups=[];group=[];size=0
for n,p in files.items():
    if group and size+p.stat().st_size>90*1024**2:groups.append(group);group=[];size=0
    assert p.stat().st_size<100*1024**2
    group.append((n,p));size+=p.stat().st_size
if group:groups.append(group)
parts=[]
for index,items in enumerate(groups,1):
    target=dest/f'{prefix}.part{index:02d}-of-{len(groups):02d}.zip'
    assert not target.exists(),('do not overwrite frozen volume',target)
    with zipfile.ZipFile(target,'w',zipfile.ZIP_STORED) as z:
        for n,p in items:z.write(p,n)
    assert target.stat().st_size<100*1024**2
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        for n,_ in items:assert hashlib.sha256(z.read(n)).hexdigest()==file_manifest[n]['sha256']
    parts.append({'path':str(target),'sha256':sha(target),'bytes':target.stat().st_size,'files':[n for n,_ in items]})
    print('VOLUME_VERIFIED',index,len(groups),target.stat().st_size,flush=True)
custody={'task_id':manifest['task_id'],'packet_directory':str(dest),'manifest_sha256':digest,
    'volumes':parts,'file_manifest':file_manifest,'all_file_hashes_and_CRC_verified':True,
    'zip_policy':'Independent ZIP volumes, not raw split bytes. Extract ALL volumes into same directory; exact original relative paths. No concatenate step.',
    'max_volume_bytes':max(v['bytes'] for v in parts),'data_bytes':sum(v['bytes'] for v in data),
    'aggregate_file_manifest_sha256':hashlib.sha256(json.dumps(file_manifest,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
    'source_or_frozen_input_writes':0}
for p in (E/'PACKET_CUSTODY.json',OUT/'PACKET_CUSTODY.json',dest/'PACKET_CUSTODY.json'):p.write_text(json.dumps(custody,indent=2),encoding='utf8')
print('PACKET_FREEZE_COMPLETE',str(dest),len(parts),custody['aggregate_file_manifest_sha256'],flush=True)
