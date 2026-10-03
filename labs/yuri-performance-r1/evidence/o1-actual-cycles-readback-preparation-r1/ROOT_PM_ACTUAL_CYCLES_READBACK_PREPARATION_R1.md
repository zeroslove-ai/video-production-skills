# ROOT_PM_ACTUAL_CYCLES_READBACK_PREPARATION_R1

DONE_READ_ONLY_RESOURCE_AND_PUBLIC_SYMBOL_INVENTORY. Safe actual host attribute observer NOT READY. Actual Cycles/PBR HOLD; unit tangent FAIL and CORNER normal0.001° gate unchanged. No Blender launch/attach, render, GPU, build, source save or product modification. Existing GUI129152 remained; PRODUCT_EXCLUSIVE untouched.

## Installed identity and ABI limits

Installed EXE: C:\Program Files\Blender Foundation\Blender 5.2\blender.exe,113,014,232bytes,SHA284f4041f98e113f3dc10654a7193ffaaa9bfdfec8b87fa116620a48b5f6d4cb.

Matching blender.pdb:88,977,408bytes,SHA3086e93547d9ce8c7b559422ed331441d3f8de29f42e7cf13d15b98975cf20ce. PE RSDS at fileoffset97,812,920 and MSFstream1 agree GUID9033ee60-d621-7701-4c4c-44205044422e,age1. Identity is verified on disk, not a live process/ABI-layout proof.

PDB S_PUB32 record for ccl::Mesh::update_tangents:section1(.text),offset61,826,336,RVA61,830,432. All148 target public records lie within their actual PE virtual/raw sections. AttributeSet::find, GeometryManager::device_update, BlenderSync::sync_mesh and BlenderSession::synchronize RVAs also recorded. EXE export table has10 names; it does not export these private Cycles APIs. No call through recovered RVAs is authorized or performed.

DBI flags2; TPIstream56bytes,indexbegin=end4096,typerecordbytes0. Thus no Mesh/Attribute/AttributeSet member layout is available from this shipped PDB. IPI details and5793 module entries are recorded. Eight relevant Cycles mesh/attribute modules have no recovered S_COMPILE3 compiler version records. Public addresses alone cannot safely serialize private object fields. No ctypes memory walking, debugger attachment, symbol server or inferred offsets used.

Build globals were read from PDB-named char[] symbols in PE .data, validated against pinned source/creator/buildinfo.c declarations. Installed build_hash is9e2066aef7ef; branchblender-v5.2-release,Release/Windows/CMake,built2026-08-25 at02:38:20 (embedded build metadata, not current task time). Windows file version is5.2; prior source-job runtime receipts report5.2.1LTS with this hash. CXX globals contain /clang:-ffp-contract=off and -march=x86-64-v2. They do not expose every per-target/release optimization flag or exact compiler version.96 parsed MikkMeshWrapper TBB public symbols show the shipped Cycles Mikk parallel templates exist. Our prior serial MSVC /fp:precise harness is not claimed equivalent to this installed compiler/TBB context.

## Existing resources and concrete gaps

| Resource | Verified state |
|---|---|
| MSVC/SDK | VSBuildTools17.14.40;cl19.44.35228.0,vcvars64;WindowsSDK10.0.19041.0 headers/kernel32/ucrt libs present with hashes |
| CMake | Existing ComfyUI python_embeded package data/bin/cmake.exe,version4.4.0;absolute path only,installation unchanged |
| Ninja | Existing ComfyUI python_embeded/Scripts/ninja.exe,version1.13.0.git.kitware.jobserver-pipe-1;unchanged |
| clang-cl | Not found on PATH,VSBuildTools recursive search or default LLVM locations;exact installed-build compiler version unrecovered |
| Native source | Only individually pinned research files available;no complete matching source checkout found in listed conventional/work/dev/download roots |
| Windows build deps | Installed runtimeTBB/OIDN/OpenImageIO binaries are present;matching Windows development headers/.libs bundle not located in searched roots |
| Debug types | Matching shipped PDB found,but stripped type records;no full private PDB/layout or ready supported debugger inspector |
| Build config | Embedded globals available;no matching localCMakeCache/compile_commands/build_info fullconfiguration found |

Searches were bounded to the install,VSBuildTools,listed conventional Blender source paths,C:\Users\JAEWAN\dev,C:\work,C:\workspace,C:\w,C:\c andDownloads. Absence means not located in that inventory,not a universal all-disk claim. Early narrow module filename pattern found0; consolidated parser correctly found8 mesh.cpp.obj/attribute.cpp.obj modules; neither query recovered compiler records. Guessed geometry_node.cpp URL404; real geometry_attributes.cpp fetched. All small pinned-source downloads total below1MiB;no large source/dependency/model downloads.

At snapshot:16 logical processors,64,546,164KiB visible RAM;31,787,788KiB free≈30.315GiB. C free263,764,242,432bytes≈245.65GiB;D free409,198,850,048bytes≈381.09GiB. These are availability snapshots,not reservations. Proposed isolated rootC:\YuriTransfer\native-cycles-readback-r1 does not exist and was not created. Planned src/deps/build-clang/capture subdirectories do not touch installedEXE/PDB/master/GUI/product repositories.

Planning caps,not measured requirements:reserve80GiB disk under isolated root;initial build2parallel tasks,max16GiB aggregate working set;stop on exceeding cap or freeRAMbelow12GiB/Cfreebelow100GiB. Future isolated Strong6 capture4CPUthreads,max8GiB and120s timeout,1process. Preserve logs/hash/diff/captures;terminate only the owned process if needed;no recursive cleanup until exact root is validated. Source/library and installedEXE/PDB hashes before/after. No build/capture process was scheduled in this task.

Exact additional resource list:complete pinned source checkout;matching Windows development dependency bundle;clang-cl compatible toolchain/version or explicit custom-build compiler divergence;complete CMake/target flags;full typed native guarded adapter+writers+lifecycle denial checks;isolated build outputs/debugtypes. Download sizes are not known from current local inventory;measure actual remote file manifests or existing caches before requesting a large-transfer decision. The applicable large-download restriction is the human user's instruction, not an inferred skill rule: “명백한 유료결제/대규모 신규 다운로드/제품 repo 변경만 사용자 승인 대상으로 남긴다.” No approval question or large transfer is issued by this resource checkpoint.

## Actual phase ordering and safe route

Stock python.cpp sync_func→BlenderSession::synchronize is viewport-only:session.cpp774–808 returns with no b_v3d or pause;normal pathsync_data then session->start at856. A pause avoids useful synchronization;unpaused sync starts rendering. It cannot serve as a stock sync-only dump API.

General renderer path Scene::device_update compiles shaders215,loads kernels240,uploads shader data254,updates background/scene attributes/camera and objects,then GeometryManager::device_update311. Tangents are generated inside geometry.cpp928–930,not device_update_preprocess. Therefore a hook there is before that manager's mesh upload/BVH phase but AFTER earlier renderer kernel/device activity;it cannot alone satisfy zero earlier uploads.

New isolated host route must avoid Session/BlenderSession::synchronize/Scene::device_update entirely. Real BlenderSync::sync_data330–340 syncs source shaders then objects. blender/shader.cpp calls realShader::tag_update;shader.cpp388–395 computes real node attribute requests on host. Geometry::need_attribute(geometry_attributes.cpp24–63) uses those actual shader requests. Thus there is a source-supported host boundary where real synced Mesh attributes and real shader requests exist,allowing direct realMesh::update_tangents(scene,false) without the ordinary device-update pipeline. This route is not implemented/compiled/executed yet.

Scene cannot be constructed with a nullDevice (constructor dereferencesdevice->info). An explicitly CPUDevice context is needed;CPUDevice constructordevice_impl.cpp44–60 selects CPU kernels metadata and optionally creates an Embree device context. That is CPU context initialization,not BVH build or render dispatch. Scene/ImageManager allocation and sync image metadata are side effects that the native driver must log. A device-null/facade replacement would fail the actualnative-context requirement.

PROPOSED_GUARDED_HOST_READBACK.diff is a concrete uncompiled proposal against exact pinnedsync.h/sync.cpp/mesh.cpp. Disabled unlessWITH_CYCLES_HOST_MESH_READBACK is explicitly compiled in a separate binary. Public begin/finish methods select the actual sourceBody,CPU-only/no loadedkernels,unique match,real original routes,63561verts/127040triangles,nonSubD/no true displacement,existingCornerNormal/UV and actual tangent/sign shader requests. sync_mesh captures the real nativeMesh after attribute move,not the temporary mesh. finish calls realMesh::update_tangents and passes constMesh to a native writer. Source files themselves were not patched. Proposed diff does not register a Python API,create device/Scene/Session or implement writer/route serialization;these remain bounded implementation work,not readinessPASS. Kernel flag alone does not prove no earlier upload;driver denial instrumentation is still mandatory.

See GUARDED_STRONG6_ENTRY_AND_OUTPUT_CONTRACT_R1.md for the exact entrysignature,caller requirements,phase denial boundaries and native attribute output table. PM can schedule only a dependency/configuration/guard implementation stage from these concrete gaps. No stocksync,GUIattach or speculative pointer-reader job is ready.
