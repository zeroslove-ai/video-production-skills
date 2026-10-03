/* Typed native API proposal; caller supplies valid native context, no address API. */
#pragma once
#include <filesystem>
#include <cstdio>
#include <mutex>
#include <string>
#include <vector>
#include "util/defines.h"
namespace blender {
struct RenderEngine; struct Main; struct Scene; struct Depsgraph; struct Mesh; struct UserDef; struct Object;
}
CCL_NAMESPACE_BEGIN
class Mesh;
namespace host_readback {
void guard_probe(const std::string &name);
struct Capture {
  std::mutex mutex;
  Mesh *mesh = nullptr;  // Owned by the local ccl::Scene; never retained after its lifetime.
  unsigned route_calls = 0, mesh_calls = 0;
  bool failed = false;
  std::vector<int> corner_tris, corner_vertices, triangle_polygons, material_slots;
  std::vector<unsigned char> smooth;
  std::vector<float> object_world;
  void routes(const blender::Mesh &source, const blender::Object &object);
  void registered_mesh(Mesh *value);
};
/* expected directory is verified against EXPECTED_INPUTS.json by the launcher.
 * Native entry byte-compares immutable evaluated inputs before writing buffers. */
bool readback_host_strong6(blender::RenderEngine &engine,
                          blender::UserDef &preferences,
                          blender::Main &main,
                          blender::Scene &source,
                          blender::Depsgraph &depsgraph,
                          const std::filesystem::path &expected,
                          const std::filesystem::path &output,
                          FILE *audit_stream,
                          std::string &error);
}  // namespace host_readback
CCL_NAMESPACE_END
