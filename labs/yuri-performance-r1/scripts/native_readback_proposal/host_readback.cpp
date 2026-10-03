/* Uncompiled research proposal using pinned native Mesh/Attribute storage APIs. */
#include "blender/host_readback.h"
#include "blender/sync.h"
#include "util/host_readback_guard.h"
#include "device/cpu/device_impl.h"
#include "device/device.h"  // Complete DeviceInfo/Device type.
#include "scene/mesh.h"     // Complete Mesh type; never infer ABI offsets.
#include "scene/scene.h"
#include "scene/attribute.h"
#include "util/progress.h"
#include "util/stats.h"
#include "util/profiling.h"
#include "util/task.h"
#include "BKE_mesh.hh"
#include "BKE_attribute.hh"
#include "BKE_object_types.hh"
#include "BKE_scene.hh"
#include "DEG_depsgraph_query.hh"
#include "DNA_scene_types.h"
#include <bit>
#include <algorithm>
#include <cstring>
#include <fstream>
#include <sstream>
#include <memory>
#include <stdexcept>
#include <type_traits>
#include <tbb/global_control.h>
CCL_NAMESPACE_BEGIN
namespace host_readback {
static_assert(sizeof(int) == 4 && sizeof(float) == 4 && sizeof(uint) == 4);
static_assert(sizeof(packed_float3) == 12 && sizeof(float2) == 8);
static_assert(std::endian::native == std::endian::little);
void Capture::routes(const blender::Mesh &source, const blender::Object &object)
{
  /* Copy within BMesh lifetime; no borrowed spans survive this callback. */
  std::lock_guard<std::mutex> lock(mutex);
  if (++route_calls != 1) { failed = true; return; }
  auto tris = source.corner_tris();
  auto corners = source.corner_verts();
  if (tris.size() != 127040 || corners.size() != 254602)
    { failed = true; return; }
  corner_tris.reserve(tris.size() * 3);
  for (const auto &tri : tris) for (int j = 0; j < 3; ++j) corner_tris.push_back(tri[j]);
  corner_vertices.assign(corners.begin(), corners.end());
  const auto polygons = source.corner_tri_faces();
  const blender::VArraySpan materials = *source.attributes().lookup<int>(
      "material_index", blender::bke::AttrDomain::Face);
  const blender::VArraySpan sharp = *source.attributes().lookup<bool>(
      "sharp_face", blender::bke::AttrDomain::Face);
  if (polygons.size()!=127040 ||
      (!materials.is_empty() && materials.size()!=source.faces().size()) ||
      (!sharp.is_empty() && sharp.size()!=source.faces().size())) { failed=true; return; }
  for (const int polygon : polygons) {
    if (polygon<0 || polygon>=source.faces().size()) { failed=true; return; }
    triangle_polygons.push_back(polygon);
    material_slots.push_back(materials.is_empty() ? 0 : materials[polygon]);
    smooth.push_back(sharp.is_empty() || !sharp[polygon]);
  }
  for (int row = 0; row < 4; ++row) for (int col = 0; col < 4; ++col)
    object_world.push_back(object.object_to_world()[col][row]);
}
void Capture::registered_mesh(Mesh *value)
{
  std::lock_guard<std::mutex> lock(mutex);
  if (++mesh_calls != 1 || !value) { failed = true; return; }
  mesh = value;
}
static void compare(const std::filesystem::path &file, const void *data, size_t bytes)
{
  if (!data || std::filesystem::file_size(file) != bytes)
    throw std::runtime_error("expected input size mismatch: " + file.string());
  std::vector<char> reference(bytes);
  std::ifstream stream(file, std::ios::binary);
  stream.read(reference.data(), std::streamsize(bytes));
  if (!stream || std::memcmp(reference.data(), data, bytes))
    throw std::runtime_error("source frame/motion/input byte drift: " + file.string());
}
static void write(const std::filesystem::path &file, const void *data, size_t bytes)
{
  if (!data || std::filesystem::exists(file)) throw std::runtime_error("no overwrite/null buffer");
  std::ofstream stream(file, std::ios::binary | std::ios::out);
  stream.write(static_cast<const char *>(data), std::streamsize(bytes));
  stream.close();
  if (!stream || std::filesystem::file_size(file) != bytes)
    throw std::runtime_error("native buffer write failed");
}
static const Attribute &attr(Mesh &mesh, AttributeStandard id,
                             AttributeElement domain, size_t elements, size_t stride)
{
  const Attribute *a = mesh.attributes.find(id);
  const bool type_ok = a && ((id == ATTR_STD_POSITION && a->type == TypePoint) ||
      (id == ATTR_STD_CORNER_NORMAL && a->type == TypeNormal) ||
      (id == ATTR_STD_UV && a->type == TypeFloat2) ||
      (id == ATTR_STD_UV_TANGENT && a->type == TypeVector) ||
      (id == ATTR_STD_UV_TANGENT_SIGN && a->type == TypeFloat));
  if (!type_ok || a->std != id || a->element != domain || a->has_motion() || a->data_sizeof() != stride ||
      Attribute::element_size(&mesh, domain, ATTR_PRIM_GEOMETRY) != elements ||
      a->buffer_size(&mesh, ATTR_PRIM_GEOMETRY) != elements * stride)
    throw std::runtime_error("registered attribute domain/stride/size/motion mismatch");
  return *a;
}
static std::string quoted(const char *s)
{
  std::string result = "\"";
  for (; *s; ++s) {
    if (*s == '\\' || *s == '"') result += '\\';
    if (static_cast<unsigned char>(*s) < 32) throw std::runtime_error("metadata control character");
    result += *s;
  }
  return result + "\"";
}
static void provenance(Mesh &mesh, const std::filesystem::path &output)
{
  std::ostringstream json;
  json << "{\"classification\":\"ACTUAL_CUSTOM_HOST_CENTER_SNAPSHOT_PENDING_PROCESS_QA\","
          "\"frame\":6,\"local_motion\":\"MOTION_NONE\",\"source_temporal_settings_changed\":false,"
          "\"shader_slot_count\":" << mesh.get_used_shaders().size() << ",\"attributes\":[";
  bool first = true;
  for (const auto id : {ATTR_STD_POSITION, ATTR_STD_CORNER_NORMAL, ATTR_STD_UV,
                        ATTR_STD_UV_TANGENT, ATTR_STD_UV_TANGENT_SIGN}) {
    const Attribute *a = mesh.attributes.find(id);
    if (!a) throw std::runtime_error("metadata attribute vanished");
    if (!first) json << ',';
    first = false;
    json << "{\"name\":" << quoted(a->name.c_str())
         << ",\"AttributeStandard\":" << int(a->std)
         << ",\"standard_name\":" << quoted(Attribute::standard_name(a->std))
         << ",\"TypeDesc\":" << quoted(a->type.c_str())
         << ",\"element\":" << int(a->element)
         << ",\"stride\":" << a->data_sizeof()
         << ",\"count\":" << Attribute::element_size(&mesh, a->element, ATTR_PRIM_GEOMETRY)
         << ",\"buffer_bytes\":" << a->buffer_size(&mesh, ATTR_PRIM_GEOMETRY)
         << ",\"motion_steps\":" << a->num_motion_steps() << '}';
  }
  json << "]}\n";
  const auto data=json.str();
  write(output/"ACTUAL_ATTRIBUTE_METADATA.json", data.data(), data.size());
}
bool readback_host_strong6(blender::RenderEngine &engine, blender::UserDef &preferences,
                          blender::Main &main,
                          blender::Scene &source, blender::Depsgraph &depsgraph,
                          const std::filesystem::path &expected,
                          const std::filesystem::path &output, FILE *audit_stream,
                          std::string &error)
{
  try {
    Scope scope(audit_stream);
    if (BKE_scene_frame_get(&source) != 6.0f ||
        DEG_get_input_scene(&depsgraph) != &source ||
        std::filesystem::exists(output) || !std::filesystem::is_directory(expected))
      throw std::runtime_error("Strong6/owned depsgraph/new output guard");
    /* Use the source's SVM configuration. OSL is not silently converted. */
    SceneParams params = BlenderSync::get_scene_params(preferences, main, source, true, false);
    if (params.shadingsystem != SHADINGSYSTEM_SVM)
      throw std::runtime_error("OSL source unsupported by this bounded capture");
    tbb::global_control hard_limit(tbb::global_control::max_allowed_parallelism, 4);
    TaskScheduler::init(4);
    struct JoinScheduler { ~JoinScheduler() { TaskScheduler::exit(); } } scheduler;
    Stats stats;
    Profiler profiler;
    DeviceInfo info; info.type = DEVICE_CPU; info.cpu_threads = 4;
    /* Real CPU context; image-vector/ISA selection and optional Embree context
     * allocation are explicit constructor side effects, not BVH/kernel launch. */
    CPUDevice device(info, stats, profiler, true);
    ++cpu_contexts;
    Scene scene(params, &device);
    Capture capture;
    {
      Progress progress;
      BlenderSync sync(engine, main, source, &scene, false, false, progress);
      sync.readback_begin_host_target(&capture);
      sync.sync_recalc(depsgraph, nullptr, nullptr, nullptr);
      sync.sync_data(source.r, depsgraph, nullptr, nullptr, nullptr, 1, 1, nullptr, info);
      /* Pinned sync_objects() ends geom_task_pool.wait_work() before returning;
       * research sync skips frame-changing motion sync. Capture locks serialize
       * callbacks; complete task join precedes dereferencing registered Mesh. */
      if (BKE_scene_frame_get(&source) != 6.0f || scene.kernels_loaded || denied != 0)
        throw std::runtime_error("post-sync frame/device drift");
      std::lock_guard<std::mutex> lock(capture.mutex);
      if (capture.failed || capture.route_calls != 1 || capture.mesh_calls != 1 || !capture.mesh)
        throw std::runtime_error("unique target/route/registered mesh guard");
      Mesh &mesh = *capture.mesh;
      /* Prove every container size BEFORE constant-length memcmp/data access. */
      if (capture.corner_tris.size()!=381120 || capture.corner_vertices.size()!=254602 ||
          capture.triangle_polygons.size()!=127040 || capture.material_slots.size()!=127040 ||
          capture.smooth.size()!=127040 || capture.object_world.size()!=16 ||
          mesh.get_triangles().size()!=381120 || mesh.get_shader().size()!=127040 ||
          mesh.get_smooth().size()!=127040 || mesh.get_used_shaders().empty())
        throw std::runtime_error("source/registered route vector cardinality mismatch");
      if (mesh.num_verts() != 63561 || mesh.num_triangles() != 127040 ||
          mesh.get_subdivision_type() != Mesh::SUBDIVISION_NONE || mesh.has_true_displacement() ||
          !mesh.need_attribute(&scene, ATTR_STD_UV_TANGENT) ||
          !mesh.need_attribute(&scene, ATTR_STD_UV_TANGENT_SIGN) ||
          mesh.attributes.find(ATTR_STD_UV_TANGENT))
        throw std::runtime_error("actual mesh/real shader request/pre-tangent guard");
      const Attribute &p = attr(mesh, ATTR_STD_POSITION, ATTR_ELEMENT_VERTEX, 63561, 12);
      const Attribute &n = attr(mesh, ATTR_STD_CORNER_NORMAL, ATTR_ELEMENT_CORNER_NORMAL, 381120, 4);
      const Attribute &uv = attr(mesh, ATTR_STD_UV, ATTR_ELEMENT_CORNER, 381120, 8);
      const TypeDesc p_type=p.type, n_type=n.type, uv_type=uv.type;
      compare(expected/"position.f32", p.data<void>(), 63561*12);
      compare(expected/"packed_normal.u32", n.data<void>(), 381120*4);
      compare(expected/"uv.f32", uv.data<void>(), 381120*8);
      compare(expected/"corner_tris.i32", capture.corner_tris.data(), 381120*4);
      compare(expected/"corner_vertices.i32", capture.corner_vertices.data(), 254602*4);
      compare(expected/"triangles.i32", mesh.get_triangles().data(), 381120*4);
      compare(expected/"triangle_polygons.i32", capture.triangle_polygons.data(), 127040*4);
      compare(expected/"material_slots.i32", capture.material_slots.data(), 127040*4);
      compare(expected/"smooth.u8", capture.smooth.data(), 127040);
      compare(expected/"object_world.f32", capture.object_world.data(), 16*4);
      for (size_t i=0; i<127040; ++i) {
        const int slot=std::max(0,std::min(capture.material_slots[i],
                                          int(mesh.get_used_shaders().size())-1));
        if (mesh.get_shader()[i]!=slot || mesh.get_smooth()[i]!=bool(capture.smooth[i]))
          throw std::runtime_error("registered shader/material-slot or smooth route drift");
      }
      /* Actual registered native attributes, not facade/rotation copy/handport. */
      mesh.update_tangents(&scene, false);
      const Attribute &t = attr(mesh, ATTR_STD_UV_TANGENT, ATTR_ELEMENT_CORNER, 381120, 12);
      const Attribute &s = attr(mesh, ATTR_STD_UV_TANGENT_SIGN, ATTR_ELEMENT_CORNER, 381120, 4);
      /* Re-acquire and validate registered inputs after tangent generation. */
      const Attribute &p_after = attr(mesh, ATTR_STD_POSITION, ATTR_ELEMENT_VERTEX, 63561, 12);
      const Attribute &n_after = attr(mesh, ATTR_STD_CORNER_NORMAL, ATTR_ELEMENT_CORNER_NORMAL, 381120, 4);
      const Attribute &uv_after = attr(mesh, ATTR_STD_UV, ATTR_ELEMENT_CORNER, 381120, 8);
      if (p_after.type != p_type || n_after.type != n_type || uv_after.type != uv_type)
        throw std::runtime_error("original registered type changed");
      compare(expected/"position.f32", p_after.data<void>(), 63561*12);
      compare(expected/"packed_normal.u32", n_after.data<void>(), 381120*4);
      compare(expected/"uv.f32", uv_after.data<void>(), 381120*8);
      compare(expected/"triangles.i32", mesh.get_triangles().data(), 381120*4);
      std::filesystem::create_directory(output);
      write(output/"position.f32", p.data<void>(), 63561*12);
      write(output/"packed_normal.u32", n.data<void>(), 381120*4);
      write(output/"uv.f32", uv.data<void>(), 381120*8);
      write(output/"tangent.f32", t.data<void>(), 381120*12);
      write(output/"sign.f32", s.data<void>(), 381120*4);
      write(output/"corner_tris.i32", capture.corner_tris.data(), 381120*4);
      write(output/"corner_vertices.i32", capture.corner_vertices.data(), 254602*4);
      write(output/"triangles.i32", mesh.get_triangles().data(), 381120*4);
      write(output/"triangle_polygons.i32", capture.triangle_polygons.data(), 127040*4);
      write(output/"material_slots.i32", capture.material_slots.data(), 127040*4);
      write(output/"smooth.u8", capture.smooth.data(), 127040);
      write(output/"object_world.f32", capture.object_world.data(), 16*4);
      if (mesh.get_shader().size()!=127040 || mesh.get_smooth().size()!=127040)
        throw std::runtime_error("registered shader/smooth cardinality mismatch");
      write(output/"shader_ids.i32", mesh.get_shader().data(), 127040*4);
      std::vector<unsigned char> actual_smooth;
      for (size_t i=0; i<127040; ++i) actual_smooth.push_back(mesh.get_smooth()[i]);
      write(output/"registered_smooth.u8", actual_smooth.data(), actual_smooth.size());
      provenance(mesh, output);
    }  // Sync/ID-map destruction while Scene and Device remain valid.
    /* Scene then Device destruction happen before the Scope audit is disarmed. */
    return true;
  }
  catch (const std::exception &exception) {
    error = exception.what();
    return false;  // Partial directory without marker is never accepted.
  }
}
}  // namespace host_readback
CCL_NAMESPACE_END
