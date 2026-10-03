"""Generate a complete review diff, never apply/configure/compile or start Blender."""
from pathlib import Path
import difflib, hashlib, json, re
LAB=Path(__file__).resolve().parent.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OLD=BASE/'o1-actual-cycles-readback-preparation-r1/upstream'
OUT=BASE/'o1-guarded-native-resource-sizing-r1'
assert not (OUT/'GUARDED_NATIVE_RESOURCE_MANIFEST.json').exists(), 'frozen checkpoint'
changes={}; hooks=[]
def read(name):
    p=OUT/'upstream'/name
    if not p.exists():
        p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((OLD/name).read_bytes())
    return p.read_text()
def edit(name, transform):
    a=read(name);changes[name]=(a,transform(a))
def include(s):
    return s.replace('CCL_NAMESPACE_BEGIN','#ifdef WITH_CYCLES_HOST_MESH_READBACK\n#  include "util/host_readback_guard.h"\n#endif\n\nCCL_NAMESPACE_BEGIN',1)
def insert_body(s, token, code):
    # Source-pinned native declaration, then its first column-zero body brace.
    start=s.index(token);body=s.index('\n{',start)
    assert ';' not in s[start:body], ('not a function definition',token)
    return s[:body+2]+'\n#ifdef WITH_CYCLES_HOST_MESH_READBACK\n'+code+'\n#endif\n'+s[body+2:]
def deny_functions(name,tokens):
    def transform(s):
        s=include(s)
        for token in tokens:
            s=insert_body(s,token,'  host_readback::deny("'+token.rstrip('(')+'");')
            hooks.append({'file':name,'entry':token,'policy':'process-wide hard exit86 before original body'})
        return s
    edit(name,transform)
def sync_header(s):
    s=s.replace('#pragma once','#pragma once\n#ifdef WITH_CYCLES_HOST_MESH_READBACK\n#  include "blender/host_readback.h"\n#endif',1)
    s=s.replace('  void reset(blender::Main &b_data, blender::Scene &b_scene);',
      '#ifdef WITH_CYCLES_HOST_MESH_READBACK\n  void readback_begin_host_target(host_readback::Capture *capture) { host_capture_ = capture; }\n#endif\n\n  void reset(blender::Main &b_data, blender::Scene &b_scene);',1)
    return s.replace(' private:\n',' private:\n#ifdef WITH_CYCLES_HOST_MESH_READBACK\n  host_readback::Capture *host_capture_ = nullptr;\n#endif\n',1)
edit('intern/cycles/blender/sync.h',sync_header)
def sync_mesh(s):
    s=include(s)
    needle='      free_object_to_mesh(b_ob_info, const_cast<blender::Mesh &>(*b_mesh));'
    assert s.count(needle)==1
    s=s.replace(needle,'#ifdef WITH_CYCLES_HOST_MESH_READBACK\n      if (host_capture_ && BKE_id_name(b_ob_info.real_object->id) == "Meshy_Body_NeutralCovered")\n        host_capture_->routes(*b_mesh);\n#endif\n'+needle,1)
    needle='  mesh->tag_update(scene, rebuild);\n}\n\nvoid BlenderSync::sync_mesh_motion'
    assert s.count(needle)==1
    s=s.replace(needle,'  mesh->tag_update(scene, rebuild);\n#ifdef WITH_CYCLES_HOST_MESH_READBACK\n  if (host_capture_ && BKE_id_name(b_ob_info.real_object->id) == "Meshy_Body_NeutralCovered")\n    host_capture_->registered_mesh(mesh);\n#endif\n}\n\nvoid BlenderSync::sync_mesh_motion',1)
    return insert_body(s,'void BlenderSync::sync_mesh_motion(', '  host_readback::deny("BlenderSync::sync_mesh_motion");')
edit('intern/cycles/blender/mesh.cpp',sync_mesh)
def objects(s):
    assert 'geom_task_pool.wait_work();' in s
    return insert_body(include(s),'void BlenderSync::sync_objects_and_motion(',
      '  host_readback::require_armed();\n  if (!host_capture_ || scene->need_motion() != Scene::MOTION_NONE)\n    host_readback::deny("motion/source context mismatch");\n  sync_objects(b_depsgraph, b_screen, b_v3d);\n  return;  // Joined by existing geom_task_pool.wait_work(); no RE_engine_frame_set.')
edit('intern/cycles/blender/object.cpp',objects)
def scene(s):
    s=include(s)
    for token in ['void Scene::device_update(', 'bool Scene::load_kernels(']:
        s=insert_body(s,token,'  host_readback::deny("'+token+' before upload/kernel launch");')
        hooks.append({'file':'intern/cycles/scene/scene.cpp','entry':token,'policy':'hard exit before original body'})
    return insert_body(s,'Scene::MotionType Scene::need_motion(',
      '  host_readback::require_armed();\n  return MOTION_NONE; // Local ccl::Scene only; source settings unchanged.')
edit('intern/cycles/scene/scene.cpp',scene)
deny_functions('intern/cycles/session/session.cpp',[
  'Session::Session(', 'void Session::start(', 'void Session::run_main_render_loop('])
deny_functions('intern/cycles/blender/session.cpp',[
  'void BlenderSession::render(', 'void BlenderSession::synchronize('])
deny_functions('intern/cycles/device/device.cpp',['unique_ptr<Device> Device::create('])
deny_functions('intern/cycles/bvh/bvh.cpp',['unique_ptr<BVH> BVH::create('])
deny_functions('intern/cycles/device/cpu/device_impl.cpp',[
 'void CPUDevice::mem_alloc(', 'void CPUDevice::mem_copy_to(',
 'void CPUDevice::mem_copy_from(', 'void CPUDevice::mem_zero(',
 'device_ptr CPUDevice::mem_alloc_sub_ptr(', 'void CPUDevice::const_copy_to(',
 'void CPUDevice::global_alloc(', 'void CPUDevice::image_alloc(',
 'void CPUDevice::build_bvh(', 'bool CPUDevice::load_kernels(',
 'vector<ThreadKernelGlobalsCPU> *CPUDevice::acquire_cpu_kernel_thread_globals('])
# Default off. Global research macro required by all participating Cycles TUs.
def cmake(s):
    index=s.index('project(Blender')
    return s[:index]+'''option(YURI_RESEARCH_HOST_READBACK "Isolated no-render host-buffer proposal" OFF)
if(YURI_RESEARCH_HOST_READBACK)
  if(NOT WIN32)
    message(FATAL_ERROR "Reviewed proposal is Windows x64 only")
  endif()
  add_compile_definitions(WITH_CYCLES_HOST_MESH_READBACK)
endif()

'''+s[index:]
edit('CMakeLists.txt',cmake)
edit('intern/cycles/blender/CMakeLists.txt',lambda s:s.replace('  camera.cpp','  host_readback.cpp\n  camera.cpp',1))
for local,remote in [('host_readback.cpp','intern/cycles/blender/host_readback.cpp'),
 ('host_readback.h','intern/cycles/blender/host_readback.h'),
 ('host_readback_guard.h','intern/cycles/util/host_readback_guard.h')]:
    # Wrap the entire new TU/header for the default-OFF build, preserving ordinary code.
    content=(LAB/'scripts/native_readback_proposal'/local).read_text()
    if local=='host_readback.cpp':content='#ifdef WITH_CYCLES_HOST_MESH_READBACK\n'+content+'\n#endif\n'
    changes[remote]=('',content)
diff=''.join(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),
 fromfile='a/'+name if a else '/dev/null',tofile='b/'+name)) for name,(a,b) in changes.items())
(OUT/'PROPOSED_GUARDED_NATIVE_V2.diff').write_text(diff,encoding='utf8')
receipt={'status':'COMPLETE_TYPED_DRIVER_WRITER_DENIAL_PROPOSAL_UNCOMPILED_UNAPPLIED',
 'guard_hooks':hooks,'original_source':{n:{'bytes':len(a.encode()),'sha256':hashlib.sha256(a.encode()).hexdigest()} for n,(a,b) in changes.items() if a},
 'diff_sha256':hashlib.sha256((OUT/'PROPOSED_GUARDED_NATIVE_V2.diff').read_bytes()).hexdigest(),
 'default_off':True,'actual_native_capture':'HOLD_NOT_RUN','runtime_PBR':'HOLD',
 'native_entry':'readback_host_strong6(RenderEngine&,UserDef&,Main&,Scene&,Depsgraph&,expected,out,FILE*,error)',
 'api_registration':'Native function proposal only. No stock GUI attach, Python raw-address API or _cycles.create. Native caller registration/compile acceptance required before any capture job.',
 'concurrency':'source corner routes copied under mutex; mesh capture serialized; exact one route/mesh required; existing geom_task_pool.wait_work joins before writer; no worker exception used for cardinality errors',
 'source_frame_motion_guard':'frame6, same input Scene, no temporal sync, existing evaluated POSITION/packedCN/UV/triangles/routes byte comparison before writing',
 'type_include_review':'Pinned sync.cpp already directly includes device/device.h and scene/mesh.h; new driver explicitly includes both, plus scene/attribute.h. No ABI offsets guessed.',
 'scope_limit':'Source diff applicability checked against pinned text only; no compile/link/runtime safety result. Guard self-test and native caller required; not a build/run approval.'}
(OUT/'NATIVE_V2_REVIEW_RECEIPT.json').write_text(json.dumps(receipt,indent=2))
print(json.dumps({'proposal_bytes':len(diff),'modified_or_added_files':len(changes),'denial_entry_hooks':len(hooks),'compiled':False}))
