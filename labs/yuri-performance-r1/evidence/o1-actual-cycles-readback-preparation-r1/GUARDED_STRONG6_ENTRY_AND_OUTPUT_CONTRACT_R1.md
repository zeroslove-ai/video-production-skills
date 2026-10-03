# GUARDED_STRONG6_ENTRY_AND_OUTPUT_CONTRACT_R1

Proposed internal native entry signature (not currently exported/registered/compiled):

```cpp
bool readback_host_strong6(blender::RenderEngine &engine,
                          blender::Main &main,
                          blender::Scene &source_scene,
                          blender::Depsgraph &evaluated_graph,
                          const std::filesystem::path &fresh_output_root,
                          NativeReadbackReceipt &receipt,
                          std::string &error);
```

Context references must come from a validated native Blender wrapper in the separate research binary;do not manufacture them using ctypes or public RVAs. Python registration remains a future patch and must validateRNA/engine/depsgraph lifetimes. No existingSession handles or GUIcontext may be reused. API approval status isproposal only.

1.Source/Action SHA match,137 rest/78Actions/13mutedbridge contracts,exact object uniqueness and authoredStrong6 frame validated by existing preserved source adapter in isolatedprocess. No save/export/geometry/material edits. CurrentDG positions/CORNER normals/UV/source routes must match frozenStrong6 input before any native dump is accepted.
2.CapTaskScheduler/TBB at4,create explicitlyDEVICE_CPU context and realScene (notSession);log CPU/Embree context allocations; reject GPU/multidevice/unknownselection. No GPUdevice enumeration or kernel execution. Exact build/config must be recorded. Caller contract requires source shading-system/normal-map/displacement settings to be recorded;reject unsupportedSubD/trueDisplacement rather than alter source.
3.Construct realBlenderSync using valid nativeengine/main/scene and CPUScene. readback_begin_host_target(Body,routes_callback);sync_recalc;sync_data with no viewport/screen/region and exactsource renderData. RealShader::tag_update derives attribute requests;do not inject requests just to force tangent generation. Original-routes callback copies currentb_mesh.corner_tris,corner_verts,triangle→polygon and source materials while b_mesh is valid;no retained Blender mesh pointer after free_object_to_mesh. A hostsync may evaluate motion/shader/image metadata;reject unexpectedframes/motion and log sideeffects.
4.After source hostsync and all geometry tasks finish,readback_finish_host_target(writer,error) invokes actualnativeMesh::update_tangents(scene,false). Writer validates realregisteredattrs/type/element/count/stride and copies center-step raw bytes using compiledAttribute::data<void>(0),buffer_size and typedsizeof checks. No guessed field offsets. Protect unique match/callback synchronization and report postcall position/CORNERNormal/UV unchanged hashes. Emit exactly oneStrong6 body result;no other frames automatically.
5.Return/cleanupCPUhostcontext and stopprocess. Do not fall through toScene::device_update/GeometryManager::device_update/Session::start/render. Native denial counters/hard failures required for those entries plusload_kernels,shader/device upload,mem_copy_to,BVHbuild and render dispatch. Device-construction bookkeeping alone is not an upload;log it separately. Current proposal only checksCPU/kernels_loaded,so denial guards must be implemented and verified before launching anything.

| Real attribute | Native element | Count | Expected storage |
|---|---|---:|---|
| ATTR_STD_POSITION | ATTR_ELEMENT_VERTEX |63561|packed_float3/12bytes|
| ATTR_STD_CORNER_NORMAL | ATTR_ELEMENT_CORNER_NORMAL |381120|packed_normal uint32/4bytes|
| ATTR_STD_UV / actualUVMap | ATTR_ELEMENT_CORNER |381120|float2/8bytes|
| ATTR_STD_UV_TANGENT | ATTR_ELEMENT_CORNER |381120|packed_float3/12bytes|
| ATTR_STD_UV_TANGENT_SIGN | ATTR_ELEMENT_CORNER |381120|float/4bytes|

Counts are source expectations to check against actualregistration,not proof of current buffers. AttributeSet::add maps standard types/elements;attribute.cpp element_size returnsnum_triangles*3 forcorner/normal;Mesh::update_tangents819–869 allocatesactualstandard attributes and originalMikk wrapper writes their buffers. Include actualTypeDesc,AttributeStandard,name,element,step,size and data_sizeof receipts. Storetriangle vertex indices,smooth/shader slotIDs,originalcorner/vertex/polygon routes and objecttransform separately. Preserve duplicatedtrianglecorners;do not average into254602 source corners.

Strong6scope:63561positions,127040triangles,381120nativecorner records;all corners compared,canonical8zero corners traced. Optionaldecoded normals from actualpackedbytes labeleddecode-reference. Output classificationACTUAL_CYCLES_HOST_REGISTERED_ATTRIBUTE_BUFFER_FROM_CUSTOM_NATIVE_BUILD if successfullyobtained;notactualshadedpixels and not automaticallyinstalledbinaryFP-equivalence. Installedcompilerclangflags/TBB differ fromMSVCserialreference;recordvariances,do not waive originalCORNER0.001° gate. Renderer/SVMshaderresult andUnityphysicalPlayerPBR remainseparateHOLD.

Required build preparation before job:fullmatching sources/developmentdeps,compatiblecompiler/config,guarded native wrapper/registeredentrypoint,writers,call-lifetime/concurrency checks,deny-device-update assertions,debugtypes. Proposed source diff isreviewable but uncompilable/unverified as a completeapplication entry until these components exist. No implementation was inserted into installedBlender or product code.
