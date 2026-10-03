"""UNRUN: executed only by the owned supervisor after binary compile acceptance."""
import sys
import bpy
assert bpy.app.background
case=sys.argv[sys.argv.index('--')+1]
import _cycles
assert hasattr(_cycles,'host_mesh_guard_probe')
_cycles.host_mesh_guard_probe(case)
raise RuntimeError('Denied native entry returned; negative test failed')
