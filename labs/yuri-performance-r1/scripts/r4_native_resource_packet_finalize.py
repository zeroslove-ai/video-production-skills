"""Finalize one bounded metadata/proposal packet. No native/build/Blender calls."""
from pathlib import Path
import base64, hashlib, json, shutil
import numpy as np
LAB=Path(__file__).resolve().parent.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-guarded-native-resource-sizing-r1';E=LAB/'evidence'/OUT.name
assert not (OUT/'GUARDED_NATIVE_RESOURCE_MANIFEST.json').exists(), 'do not overwrite frozen packet'
E.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
deps=load(OUT/'WINDOWS_DEPS_EXACT_PAYLOAD_MANIFEST.json')
assert deps['files']==19077 and len(deps['path_manifest'])==19077 and not deps['errors']
assert sum(deps['unique_LFS_size_map'].values())==6574796539
assert sum(r['logical_bytes'] for r in deps['path_manifest'])==6983719590
# Rehash every small official Gitblob, not the untransferred LFS payloads.
for p in (OUT/'metadata/pointer_blobs').glob('*.json'):
    row=load(p);data=base64.b64decode(row['content'])
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==p.stem
release=load(OUT/'metadata/llvm_release_20_1_8.json')
llvm=next(r for r in release['assets'] if r['name']=='LLVM-20.1.8-win64.exe')
sig=next(r for r in release['assets'] if r['name']=='LLVM-20.1.8-win64.exe.sig')
assert llvm['size']==385658654 and llvm['digest']=='sha256:3197846a2b19063687dd56e93e34cd941e3548d907f23a6131571321bdf9fe7b'
assert sig['size']==543
old=load(OUT/'expected-Strong6/EXPECTED_INPUTS.json')
current=next(Path(p) for p in old['inputs'] if p.endswith('_actual_evaluated_cycles_inputs.npz'))
assert sha(current)==old['inputs'][str(current)]['sha256']
dest=OUT/'expected-Strong6-v3';dest.mkdir()
files=[]
for row in old['files']:
    p=OUT/'expected-Strong6'/row['path'];assert sha(p)==row['sha256']
    shutil.copyfile(p,dest/row['path']);files.append(row)
with np.load(current,allow_pickle=False) as d:
    arrays={'triangle_polygons.i32':d['current_triangle_source_polygon'],
      'material_slots.i32':d['current_triangle_material_slot'],
      'object_world.f32':d['body_object_world'],
      'smooth.u8':np.ones(127040,dtype=np.uint8)}
    for name,array in arrays.items():
        dtype='<f4' if name.endswith('f32') else '<i4' if name.endswith('i32') else '|u1'
        a=np.ascontiguousarray(array,dtype=dtype);p=dest/name;p.write_bytes(a.tobytes())
        files.append({'path':name,'dtype':dtype,'shape':list(a.shape),'bytes':p.stat().st_size,'sha256':sha(p)})
old.update({'revision':'ADDITIVE_EXPECTED_V3','files':files,
 'source_smooth_policy':'source sharp_face absent defaults false; all 127040 triangles smooth; actual buffer written separately for QA'})
(dest/'EXPECTED_INPUTS.json').write_text(json.dumps(old,indent=2))
for p in (LAB/'scripts/native_readback_proposal').iterdir():
    target=OUT/'proposal-v3'/p.name;target.parent.mkdir(exist_ok=True);shutil.copyfile(p,target)
frozen=BASE/'o1-actual-cycles-readback-preparation-r1'
for name in ('EXISTING_BUILD_TOOLS_AND_SDK.json','INSTALLED_BUILD_GLOBAL_STRINGS.json',
 'SYSTEM_RESOURCE_SNAPSHOT.json','INSTALLED_PE_PDB_IDENTITY.json'):
    target=OUT/'previous-preparation'/name;target.parent.mkdir(exist_ok=True);shutil.copyfile(frozen/name,target)
licenses=[r for r in deps['path_manifest'] if any(t in r['path'].lower().split('/')[-1] for t in ('license','copying','notice'))]
(OUT/'DEPENDENCY_LICENSE_LOCATIONS.json').write_text(json.dumps({'paths':licenses,
 'notice':'Path identities/metadata only. deps.md is versions/homepages, not a blanket license. Complete notices accompany any future acquired/distributed dependency bundle.'},indent=2))
source=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
actions=BASE/'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'
immutable={'source':{'bytes':source.stat().st_size,'sha256':sha(source)},
 'actions':{'bytes':actions.stat().st_size,'sha256':sha(actions)}}
assert immutable['source']['sha256']==old['source_R4_sha256']
assert immutable['actions']['sha256']==old['Action_library_sha256']
build={'status':'PLAN_ONLY_UNCONFIGURED_UNCOMPILED_UNRUN',
 'root':'C:/YuriTransfer/native-cycles-readback-r1','root_created':False,
 'compiler':'proposed official LLVM20.1.8 clang-cl; installed exact compiler version unknown',
 'generator':'Ninja4.4-CMake plan with existing MSVC14.44/SDK10.0.19041 x64 host/link libraries',
 'source':'v5.2.1 9e2066aef7ef7e20c142ad7bd3303138a4304c93',
 'libdir':'pinned lib-windows_x64 commit60d6e96b917568278d400a4024c98da0fb777338; full baseline dependency bundle',
 'CMAKE_BUILD_TYPE':'Release','YURI_RESEARCH_HOST_READBACK':'ON (custom defaultOFF option)',
 'CMAKE_C_COMPILER':'owned LLVM20.1.8/bin/clang-cl.exe','CMAKE_CXX_COMPILER':'same',
 'CMAKE_C_FLAGS_and_CXX_FLAGS':'/clang:-ffp-contract=off /clang:-march=x86-64-v2; intent matches visible globals, target/perTU optimization equivalence unknown',
 'proposed_options':{'WITH_CYCLES':'ON','WITH_CYCLES_DEVICE_CUDA':'OFF','WITH_CYCLES_DEVICE_OPTIX':'OFF',
 'WITH_CYCLES_DEVICE_HIP':'OFF','WITH_CYCLES_DEVICE_ONEAPI':'OFF','WITH_CYCLES_OSL':'ON',
 'WITH_CYCLES_EMBREE':'ON','WITH_CYCLES_NATIVE_ONLY':'OFF','WITH_CYCLES_PARALLEL_DEVICE_KERNEL_BUILD':'OFF'},
 'config_acceptance':'Verify every option exists/accepted in configure log, CPU-only backend closure, compiled guard macro for all participating TUs and linker symbol resolution; unused options reject, not silently accepted.',
 'resources':{'build_parallel_jobs':2,'build_aggregate_RAM_cap_bytes':16*1024**3,'disk_cap_bytes':80*1024**3,
 'minimum_free_RAM_bytes':12*1024**3,'minimum_free_C_disk_bytes':100*1024**3,
 'future_capture_processes':1,'future_capture_TBB_parallelism':4,'future_capture_RAM_cap_bytes':8*1024**3,'future_capture_timeout_seconds':120},
 'owned_process_lifecycle':'Future supervisor creates only owned isolated job object/process, logs PID/starttime/exe SHA and child tree, timeout kills only that owned job. Existing GUI129152 never attached/stopped; PRODUCT_EXCLUSIVE GPU lock unchanged. No current process scheduled.',
 'guard_selftest_before_capture':'Separate isolated test processes must show each20 forbidden entry exits86 before original work and correctly logs attempt; native RNA type rejection, output no-overwrite, failed input/frame cardinality, callback join, scope destruction counters and immutable source checks must pass.'}
(OUT/'BUILD_CAPTURE_STAGED_PLAN.json').write_text(json.dumps(build,indent=2))
resources={'status':'OFFICIAL_METADATA_VERIFIED_PAYLOADS_NOT_ACQUIRED',
 'source_archive':{'url':'https://download.blender.org/source/blender-5.2.1.tar.xz','published_bytes':93666248,
 'published_MD5':'ff0022afc5b8444db46371c6e07b4dd5','published_SHA256':None,
 'verification':'official source index and .md5sum; archive not downloaded/extracted; release tag commit matches installed buildhash'},
 'LLVM_installer':{'url':llvm['browser_download_url'],'published_bytes':llvm['size'],'published_digest':llvm['digest'],
 'verification':'official release API only; installer untransferred/unverified/uninstalled'},
 'LLVM_detached_signature':{'url':sig['browser_download_url'],'published_bytes':sig['size'],'published_digest':sig['digest']},
 'Windows_deps':{'url':'https://projects.blender.org/blender/lib-windows_x64.git','commit':deps['deps_commit'],
 'tree':deps['deps_tree'],'unique_LFS_objects':1263,'unique_LFS_payload_bytes':6574796539,
 'logical_checkout_bytes':6983719590,'ordinary_git_blob_path_bytes':303161433,
 'verification':'20995 tree entries complete;1374 small Git blobs SHA1 rehashed;1263 pointers/1276 paths expose SHA256+exact size. Actual payloads not hashed/transferred.',
 'includes_clang_cl_compiler':False,'LLVM_library_version':'20.1.8'},
 'known_acquisition_payload_bytes':93666248+llvm['size']+sig['size']+6574796539,
 'additional_transport_bytes':'Git pack, ordinary compressed objects, protocol, metadata and signature trust setup not predetermined; not a fully exact network-total claim.',
 'cache_search':load(OUT/'CACHE_SEARCH_RECEIPT.json'),
 'licenses':{'Blender':'source/COPYING; whole source GPL; patched Cycles files carry Apache-2.0 notices',
 'LLVM':'official llvm/LICENSE.TXT Apache-2.0 WITH LLVM exceptions',
 'deps':'107 notice/license path identities recorded; each dependency retains its own terms, no blanket license claim'},
 'installed_configuration_obtainable':'NOT_EXACTLY_RECONSTRUCTED: full source commit and some globals available; stripped PDB no type records/exact compiler/perTU flags. Proposed customClang20.1.8+TBB cap4 is explicit divergence.',
 'approval_boundary':'Human instruction reserves large new downloads for approval. Metadata only done; no archive/LFS payload/toolchain transfer, install, build, capture, GPU or GUI attach authorized by this preparation packet.'}
(OUT/'ACQUISITION_PLAN.json').write_text(json.dumps(resources,indent=2))
report='''# R4 guarded native resource sizing / additive proposal R1

Preparation is complete; native execution readiness remains HOLD. This is a separate Desktop research checkpoint. It does not promote appearance, change source R4, alter reaction curves, or prove Unity/renderer equivalence.

| Resource | Published bytes | Identity |
|---|---:|---|
| Blender5.2.1 source archive | 93,666,248 | MD5 ff0022afc5b8444db46371c6e07b4dd5; tag full commit9e2066aef7ef7e20c142ad7bd3303138a4304c93 |
| LLVM20.1.8 win64 installer | 385,658,654 | SHA256 3197846a2b19063687dd56e93e34cd941e3548d907f23a6131571321bdf9fe7b |
| LLVM detached signature | 543 | official release asset; signer trust/signature verification pending acquisition |
| Windows pinned1263 unique LFS payloads | 6,574,796,539 | commit60d6e96b917568278d400a4024c98da0fb777338; each published SHA256/size in path manifest |

Known payload subtotal is **7,054,121,984 bytes**, plus Git pack/protocol and other metadata whose transport bytes are not predetermined. Logical dependency checkout is6,983,719,590bytes; ordinary Git path bytes303,161,433 are not a Git-network-size claim. Full pinned bundle baseline is used; reduced Release-only/CPU selective closure has not been certified. LLVM dev library is20.1.8 but dependency tree supplies clang-format, not clang-cl. Matching compiler/archive/library cache was not found in the recorded bounded scope. Existing CMake/Ninja/MSVC/SDK locations and hashes are copied from previous preparation, without modifying ComfyUI.

[Official source index](https://download.blender.org/source/), [official pinned library](https://projects.blender.org/blender/lib-windows_x64/src/commit/60d6e96b917568278d400a4024c98da0fb777338), [LLVM release](https://github.com/llvm/llvm-project/releases/tag/llvmorg-20.1.8), [Windows build handbook](https://developer.blender.org/docs/handbook/building_blender/windows/) underpin the metadata receipts. Actual archive/LFS/compiler binaries were neither downloaded nor verified. Source publishes MD5 here; do not invent an official archive SHA256. Pinned source and license text only were fetched.

V2r1 reviewed draft was reconstructed byte-for-byte to SHA f99667313fd214e91d8e05e5f9ddfbdf67e376bee497837cb1b3d2a0f5659dbb. Distinct V2r2 SHA21c6084c1607c1b08588994c5a0db0d4cb1cb9b9cc637d22082c4bc7c20e1f3e is preserved separately. **V3 is an additive, uncompiled, unapplied proposal; previous draft review is not V3 acceptance.** Source file complete types are explicit; pinned sync.cpp already included device/device.h and scene/mesh.h.

V3 contains actual typed Mesh/Attribute buffer access, mutex-protected copied routes, exactly one target and source callback, existing geometry task join, process-wide hard-denial hooks before render/session/device upload/kernel/BVH bodies, RNA typed native caller registration and fresh callback-free native engine, and local CPU context with explicit optional Embree/ISA/image-vector constructor effects. Before and after tangent generation it checks original POSITION/CORNER_NORMAL/UV bytes, type/domain/size/no-motion and route/frame invariants. It records actual TypeDesc/std/name/element/stride/count, triangle→polygon, source material/smooth, actual shader/smooth, object matrix and corner routes. No fake Mesh facade or raw ABI address call is used.

Native Sync/Scene/Device/scheduler cleanup precedes Scope counters and wrapper engine-free receipt. Proposed Python invocation verifies immutable source/action hashes, source component fingerprint, frozen expected bytes and original temporal settings, and restores OFF state. It can produce only a pending-process-exit record. Final acceptance additionally requires the supervisor’s exit0/owned-child cleanup and full output hash/numerical report. The local ccl Scene is forced MOTION_NONE: **custom host-center snapshot, not the normal installed shaded renderer**. Source temporal settings remain unchanged. Original Strong6 packed-normal expected bytes remain classified pinned algorithm reference; no actual renderer buffer is claimed.

Exact installed compiler/perTU flags and private layouts are unavailable from stripped PDB. Source commit and visible FP/march globals are pinned, but a Clang20.1.8 research build remains a custom configuration. Build plan: owned C:/YuriTransfer/native-cycles-readback-r1 only; two build tasks,16GiB aggregate RAM,80GiB disk budget, stop below12GiB freeRAM or100GiB freeC; future single capture cap4TBB/8GiB/120sec. Configure option closure, compile/link, all denial self-tests, owned native caller and source hash checks are prerequisites. No job was scheduled, no process was launched/attached, no dependency/toolchain installed, and existing GUI129152/GPU lock/product/Laptop remain untouched.

Human rule: “명백한 유료결제/대규모 신규 다운로드/제품 repo 변경만 사용자 승인 대상으로 남긴다.” This checkpoint is a concrete acquisition/build/capture preparation, not permission to transfer or execute. Preparation stops here. Next stage is approval of the sized isolated acquisition, then configure/compile/guard tests; no capture precedes those gates. R4 appearance correction and all prior frozen packets remain unchanged.
'''
for root in (OUT,E):(root/'ROOT_PM_GUARDED_NATIVE_RESOURCE_SIZING_R1.md').write_text(report,encoding='utf8')
manifest={'task_id':'ROOT_PM_GUARDED_NATIVE_PREPARATION_REVIEW_AND_RESOURCE_SIZING_R1',
 'status':'DONE_METADATA_AND_ADDITIVE_NATIVE_PROPOSAL_NATIVE_READINESS_HOLD',
 'source_R4_immutable':immutable,'appearance_promoted':False,'actual_Cycles_renderer_buffers':'HOLD_NOT_CAPTURED',
 'runtime_PBR':'HOLD','large_binary_transfers_build_Blender_GPU_render_jobs':0,'GUI_PID_preserved':129152,
 'known_acquisition_payload_bytes':resources['known_acquisition_payload_bytes'],
 'dependency_LFS_payload_bytes':6574796539,'exact_installed_config':'NOT_RECONSTRUCTED_CUSTOM_BUILD_EXPLICIT',
 'V3_diff_sha256':sha(OUT/'PROPOSED_GUARDED_NATIVE_V3.diff'),
 'draft_custody':load(OUT/'drafts/DRAFT_CUSTODY.json'),
 'remaining':'Acquisition approval, isolated configure/compile/link, guard self-tests/native wrapper validation, owned capture/process cleanup/full attribute numerical QA; no new request inferred from this preparation.',
 'files':[{'path':str(p.relative_to(OUT)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':sha(p)}
          for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='PACKET_CUSTODY.json']}
for root in (OUT,E):(root/'GUARDED_NATIVE_RESOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
for n in ('ACQUISITION_PLAN.json','BUILD_CAPTURE_STAGED_PLAN.json','NATIVE_V3_REVIEW_RECEIPT.json','CACHE_SEARCH_RECEIPT.json'):
    shutil.copyfile(OUT/n,E/n)
print(json.dumps({'files':len(manifest['files']),'packet_data_bytes':sum(r['bytes'] for r in manifest['files']),
 'known_acquisition_payload_bytes':manifest['known_acquisition_payload_bytes'],'native_run':False}))
