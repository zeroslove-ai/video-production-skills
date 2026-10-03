/* Uncompiled actual entry probes. No invalid object facade/ABI or dummy denial call. */
#ifdef WITH_CYCLES_HOST_MESH_READBACK
#include "util/host_readback_guard.h"
#include "device/cpu/device_impl.h"
#include "device/memory.h"
#include "scene/scene.h"
#include "session/session.h"
#include "util/stats.h"
#include "util/profiling.h"
#include "util/progress.h"
#include <string>
CCL_NAMESPACE_BEGIN
namespace host_readback {
void guard_probe(const std::string &name)
{
  Scope scope(stdout);
  DeviceInfo info;info.type=DEVICE_CPU;info.cpu_threads=4;
  Stats stats;Profiler profiler;
  if (name=="factory") { auto rejected=Device::create(info,stats,profiler,true); }
  else if (name=="session") {
    SessionParams p;p.device=info;p.threads=4;p.headless=true;
    Session rejected(p,SceneParams{});
  }
  else {
    CPUDevice device(info,stats,profiler,true);++cpu_contexts;
    device_vector<float> scratch(&device,"owned-guard-scratch",MEM_READ_WRITE);
    Progress progress;
    struct ProbeScene : Scene { using Scene::Scene; using Scene::load_kernels; };
    ProbeScene scene(SceneParams{},&device);
    if (name=="scene-upload") scene.device_update(&device,progress);
    else if (name=="scene-kernel") scene.load_kernels(progress);
    else if (name=="alloc") device.mem_alloc(scratch);
    else if (name=="upload") device.mem_copy_to(scratch);
    else if (name=="copy-from") device.mem_copy_from(scratch,0,0,0,4);
    else if (name=="zero") device.mem_zero(scratch);
    else if (name=="subptr") device.mem_alloc_sub_ptr(scratch,0,0);
    else if (name=="const") { float value=0;device.const_copy_to("owned-negative",&value,4); }
    else if (name=="global") device.global_alloc(scratch);
    else if (name=="kernel") static_cast<Device &>(device).load_kernels(0);
    else if (name=="kernel-globals") device.acquire_cpu_kernel_thread_globals();
    else throw std::runtime_error("unknown actual-entry negative probe");
  }
  throw std::runtime_error("Actual forbidden entry returned: guard test FAIL");
}
}  // namespace host_readback
CCL_NAMESPACE_END
#endif
