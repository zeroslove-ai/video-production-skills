"""Prepare, never apply/build, a reviewable guarded native source proposal."""
from pathlib import Path
import difflib,json,hashlib
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-actual-cycles-readback-preparation-r1'
assert not (OUT/'READBACK_PREPARATION_MANIFEST.json').exists(), 'Do not change a frozen checkpoint'
up=OUT/'upstream';changes={}
p=up/'intern/cycles/blender/sync.h';original=p.read_text();s=original
assert '#pragma once' in s
s=s.replace('#pragma once','#pragma once\n\n#ifdef WITH_CYCLES_HOST_MESH_READBACK\n#  include <functional>\n#endif',1)
declaration=r'''
#ifdef WITH_CYCLES_HOST_MESH_READBACK
  /* Isolated native research entry only: no BlenderSession/Session or device_update. */
  bool readback_begin_host_target(const std::string &object_name,
                                  std::function<bool(const blender::Mesh &)> routes);
  bool readback_finish_host_target(
      const std::function<bool(const Mesh &)> &writer, std::string &error);
#endif
'''
s=s.replace('  void reset(blender::Main &b_data, blender::Scene &b_scene);',declaration+'\n  void reset(blender::Main &b_data, blender::Scene &b_scene);',1)
private=r'''
#ifdef WITH_CYCLES_HOST_MESH_READBACK
  std::string host_readback_target_;
  Mesh *host_readback_mesh_ = nullptr;
  int host_readback_matches_ = 0;
  bool host_readback_routes_ok_ = false;
  std::function<bool(const blender::Mesh &)> host_readback_routes_;
#endif
'''
s=s.replace(' private:\n',' private:\n'+private,1);changes['intern/cycles/blender/sync.h']=(original,s)
p=up/'intern/cycles/blender/mesh.cpp';original=p.read_text();s=original
route=r'''
#ifdef WITH_CYCLES_HOST_MESH_READBACK
      if (!host_readback_target_.empty() &&
          BKE_id_name(b_ob_info.real_object->id) == host_readback_target_) {
        host_readback_routes_ok_ = host_readback_routes_ && host_readback_routes_(*b_mesh);
      }
#endif
'''
needle='      free_object_to_mesh(b_ob_info, const_cast<blender::Mesh &>(*b_mesh));'
assert s.count(needle)==1;s=s.replace(needle,route+'\n'+needle,1)
capture=r'''
#ifdef WITH_CYCLES_HOST_MESH_READBACK
  if (!host_readback_target_.empty() &&
      BKE_id_name(b_ob_info.real_object->id) == host_readback_target_) {
    host_readback_mesh_ = mesh;
    ++host_readback_matches_;
  }
#endif
'''
needle='  mesh->tag_update(scene, rebuild);\n}\n\nvoid BlenderSync::sync_mesh_motion'
assert s.count(needle)==1;s=s.replace(needle,'  mesh->tag_update(scene, rebuild);\n'+capture+'}\n\nvoid BlenderSync::sync_mesh_motion',1)
changes['intern/cycles/blender/mesh.cpp']=(original,s)
p=up/'intern/cycles/blender/sync.cpp';original=p.read_text();s=original
for include in ('device/device.h','scene/mesh.h','scene/attribute.h'):
 if '#include "'+include+'"' not in s:s=s.replace('CCL_NAMESPACE_BEGIN','#include "'+include+'"\n\nCCL_NAMESPACE_BEGIN',1)
implementation=r'''
#ifdef WITH_CYCLES_HOST_MESH_READBACK
bool BlenderSync::readback_begin_host_target(
    const std::string &object_name,
    std::function<bool(const blender::Mesh &)> routes)
{
  if (!scene || !scene->device || scene->device->info.type != DEVICE_CPU ||
      scene->kernels_loaded || object_name != "Meshy_Body_NeutralCovered") {
    return false;
  }
  host_readback_target_ = object_name;
  host_readback_mesh_ = nullptr;
  host_readback_matches_ = 0;
  host_readback_routes_ok_ = false;
  host_readback_routes_ = std::move(routes);
  return true;
}

bool BlenderSync::readback_finish_host_target(
    const std::function<bool(const Mesh &)> &writer, std::string &error)
{
  if (!scene || !scene->device || scene->device->info.type != DEVICE_CPU ||
      scene->kernels_loaded || host_readback_matches_ != 1 ||
      !host_readback_mesh_ || !host_readback_routes_ok_) {
    error = "CPU/host phase/unique target/original route guard failed";
    return false;
  }
  Mesh &mesh = *host_readback_mesh_;
  if (mesh.num_verts() != 63561 || mesh.num_triangles() != 127040 ||
      mesh.get_subdivision_type() != Mesh::SUBDIVISION_NONE ||
      mesh.has_true_displacement() ||
      !mesh.attributes.find(ATTR_STD_CORNER_NORMAL) ||
      !mesh.attributes.find(ATTR_STD_UV) ||
      !mesh.need_attribute(scene, ATTR_STD_UV_TANGENT) ||
      !mesh.need_attribute(scene, ATTR_STD_UV_TANGENT_SIGN) ||
      mesh.attributes.find(ATTR_STD_UV_TANGENT)) {
    error = "Actual mesh/normal/UV/real shader request/no prior tangent guard failed";
    return false;
  }
  /* Real native Mesh + AttributeSet + real synced shaders. No facade or handport. */
  mesh.update_tangents(scene, false);
  const Attribute *t = mesh.attributes.find(ATTR_STD_UV_TANGENT);
  const Attribute *s = mesh.attributes.find(ATTR_STD_UV_TANGENT_SIGN);
  if (!t || !s || t->element != ATTR_ELEMENT_CORNER || s->element != ATTR_ELEMENT_CORNER ||
      Attribute::element_size(&mesh, t->element, ATTR_PRIM_GEOMETRY) != 381120 ||
      Attribute::element_size(&mesh, s->element, ATTR_PRIM_GEOMETRY) != 381120) {
    error = "Registered tangent/sign attribute guard failed";
    return false;
  }
  const bool result = writer && writer(mesh);
  if (!result) error = "Native buffer serialization/validation failed";
  return result;
}
#endif
'''
s=s.replace('CCL_NAMESPACE_BEGIN','CCL_NAMESPACE_BEGIN\n'+implementation,1)
changes['intern/cycles/blender/sync.cpp']=(original,s)
diff=''.join(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='a/'+n,tofile='b/'+n)) for n,(a,b) in changes.items())
(OUT/'PROPOSED_GUARDED_HOST_READBACK.diff').write_text(diff,encoding='utf8')
receipt={'status':'PROPOSED_SOURCE_DIFF_NOT_APPLIED_NOT_COMPILED','guard_macro':'WITH_CYCLES_HOST_MESH_READBACK','scope':'Only compiled into a separate research binary; defaults absent. Does not register Python API or create Scene/device/session. Driver/writers and lifecycle denial instrumentation still required.',
 'original_files':{n:{'sha256':hashlib.sha256((up/n).read_bytes()).hexdigest(),'bytes':(up/n).stat().st_size} for n in changes},'diff_sha256':hashlib.sha256((OUT/'PROPOSED_GUARDED_HOST_READBACK.diff').read_bytes()).hexdigest(),
 'not_a_safe_observer_readiness_claim':'No compilation, ABI layout, runtime side effect or caller lifetime has been verified for this proposal. Kernel flag alone cannot prove absence of earlier device upload; driver must deny device_update/load_kernels/upload/BVH/session start entrypoints and serialize native buffers with typed access.'}
(OUT/'PROPOSED_SOURCE_DIFF_RECEIPT.json').write_text(json.dumps(receipt,indent=2))
print('PROPOSED_SOURCE_DIFF_ONLY',len(diff))
