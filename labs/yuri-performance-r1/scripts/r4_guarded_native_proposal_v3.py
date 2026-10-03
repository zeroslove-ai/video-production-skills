"""Additive v3 review diff. All drafts versioned; never apply/build/run."""
from pathlib import Path
import hashlib,json
LAB=Path(__file__).resolve().parent.parent
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-guarded-native-resource-sizing-r1')
assert not (OUT/'GUARDED_NATIVE_RESOURCE_MANIFEST.json').exists()
assert not (OUT/'PROPOSED_GUARDED_NATIVE_V3.diff').exists(), 'freeze each reviewed revision'
code=(LAB/'scripts/r4_guarded_native_proposal_v2.py').read_text()
code=code.replace("host_capture_->routes(*b_mesh);","host_capture_->routes(*b_mesh, *b_ob_info.real_object);")
code=code.replace("PROPOSED_GUARDED_NATIVE_V2.diff","PROPOSED_GUARDED_NATIVE_V3.diff").replace("NATIVE_V2_REVIEW_RECEIPT.json","NATIVE_V3_REVIEW_RECEIPT.json")
# Add actual RNA wrapper registration and source includes, preserving stock/default OFF path.
extra=r"""
changes['intern/cycles/blender/host_readback_python.inc']=('',(LAB/'scripts/native_readback_proposal/host_readback_python.inc').read_text())
def python_wrapper(s):
    headers='''
#ifdef WITH_CYCLES_HOST_MESH_READBACK
#  include "blender/host_readback.h"
#  include "BKE_context.hh"
#  include "BKE_global.hh"
#  include "BLI_threads.h"
#  include "bpy_rna.hh"
#  include "RNA_prototypes.hh"
#  include "RE_engine.h"
#  include <cstring>
#  include <filesystem>
#endif
'''
    s=s.replace('CCL_NAMESPACE_BEGIN',headers+'\nCCL_NAMESPACE_BEGIN',1)
    s=s.replace('namespace {','namespace {\n#ifdef WITH_CYCLES_HOST_MESH_READBACK\n#  include "blender/host_readback_python.inc"\n#endif',1)
    return s.replace('    {"init", init_func,', '#ifdef WITH_CYCLES_HOST_MESH_READBACK\n    {"host_mesh_readback", host_readback_func, METH_VARARGS, "Isolated typed RNA host readback"},\n#endif\n    {"init", init_func,',1)
edit('intern/cycles/blender/python.cpp',python_wrapper)
a,b=changes['intern/cycles/blender/CMakeLists.txt']
b=b.replace('  ../../../source/blender/makesrna','  ../../../source/blender/python/intern\n  ../../../source/blender/makesrna',1)
changes['intern/cycles/blender/CMakeLists.txt']=(a,b)
"""
code=code.replace("diff=''.join(",extra+"\ndiff=''.join(",1)
exec(compile(code,'additive-v3-proposal','exec'))
p=OUT/'NATIVE_V3_REVIEW_RECEIPT.json';r=json.loads(p.read_text())
r.update({'revision':'V3_ADDITIVE_NO_V2_REVIEW_INHERITANCE',
 'api_registration':'Guarded _cycles.host_mesh_readback validates typed Context/Preferences/Depsgraph RNA; fresh zero-flag native RenderEngine with no callbacks/depsgraph/GPUcontext; native RE_engine_free after driver returns. No as_pointer/PyLong/ABI addresses/stock Session.',
 'post_tangent_invariance':'Re-acquire POSITION/CN/UV; domain/stride/count/no-motion and copied TypeDesc comparison plus exact original bytes and triangles checked before writing.',
 'actual_attribute_provenance':'TypeDesc string, std/name/element/stride/count/buffer bytes/motion_steps recorded from actual native objects.',
 'route_provenance':'original triangle polygon, material slot, smooth IDs, object world transform plus actual registered shader IDs/smooth buffers written.',
 'cleanup_acceptance':'No marker inside local Scene/Device lifetime; Scope logs post-destruction counters, wrapper frees engine and logs return. Future Python helper verifies all source/action/output hashes, OFF restore and original temporal settings; pending process-exit receipt only. Supervisor exit0/job-tree cleanup still required.',
 'custom_build_divergence':'Local ccl Scene forced MOTION_NONE; source temporal flags unchanged; hostcenter customsnapshot, not normal shaded installed renderer equivalence.',
 'must_not_launch_yet':'Configure/compile/link and guards self-tests unrun; owned caller/API must be validated in isolated build before native capture.'})
p.write_text(json.dumps(r,indent=2))
print('ADDITIVE_V3_UNCOMPILED',r['diff_sha256'])
