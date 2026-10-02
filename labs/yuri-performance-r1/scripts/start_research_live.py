"""Instance-only existing addon bootstrap; never saves shared preferences."""
import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
receipt={'scope':'owned research Blender instance only','shared_preferences_saved':False}
try:
    bpy.ops.preferences.addon_enable(module='blender_mcp')
    receipt['operator_result']=list(bpy.ops.blendermcp.start_server())
    receipt['filepath']=bpy.data.filepath
except Exception as exc:receipt['error']=str(exc)
(ROOT/'evidence/acting-r2/live_bootstrap.json').write_text(json.dumps(receipt,indent=2))
