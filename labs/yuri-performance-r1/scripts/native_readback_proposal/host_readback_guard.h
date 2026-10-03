/* Research proposal ONLY. Not compiled, applied, or a renderer readiness claim. */
#pragma once
#include <atomic>
#include <cstdio>
#include <cstdlib>
#include <mutex>
#include <stdexcept>
#include "util/defines.h"
CCL_NAMESPACE_BEGIN
namespace host_readback {
inline std::atomic<bool> armed{false};
inline std::atomic<unsigned> denied{0}, cpu_contexts{0};
inline std::mutex audit_mutex;
inline FILE *audit = nullptr;
/* These hooks are process-wide in the isolated research build, including workers.
 * Abort before the original body; unwinding a worker exception is not relied on. */
[[noreturn]] inline void deny(const char *entry) noexcept
{
  ++denied;
  std::lock_guard<std::mutex> lock(audit_mutex);
  FILE *out = audit ? audit : stderr;
  std::fprintf(out, "{\"denied_entry\":\"%s\",\"before_original_body\":true}\n", entry);
  std::fflush(out);
  std::_Exit(86);
}
inline void require_armed()
{
  if (!armed.load()) deny("host path outside owned capture scope");
}
struct Scope {
  explicit Scope(FILE *stream)
  {
    bool expected = false;
    if (!stream || !armed.compare_exchange_strong(expected, true))
      throw std::runtime_error("non-reentrant capture requires owned audit stream");
    std::lock_guard<std::mutex> lock(audit_mutex);
    audit = stream; denied = 0; cpu_contexts = 0;
  }
  ~Scope()
  {
    std::lock_guard<std::mutex> lock(audit_mutex);
    if (audit) {
      std::fprintf(audit, "{\"scope_ended\":true,\"denied_attempts\":%u,\"CPU_contexts\":%u}\n",
                   denied.load(), cpu_contexts.load());
      std::fflush(audit);
    }
    audit = nullptr; armed = false;
  }
  Scope(const Scope &) = delete;
};
}  // namespace host_readback
CCL_NAMESPACE_END
