"""Preserve native material recipes and extract packed textures for local handoff."""
import bpy,json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence/model-handoff-r4';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/r4-model-handoff')
bpy.ops.wm.open_mainfile(filepath=str(OUT/'Character_Master_Reaction_R4_20261002.blend'))
dest=OUT/'textures';dest.mkdir(exist_ok=True);images=[]
for i in bpy.data.images:
 if not i.packed_file:continue
 data=bytes(i.packed_file.data);ext='.png' if data.startswith(b'\x89PNG') else '.jpg' if data.startswith(b'\xff\xd8') else '.bin'
 name=re.sub('[^A-Za-z0-9._-]','_',i.name)+ext;p=dest/name;p.write_bytes(data)
 images.append({'blender_image':i.name,'file':'textures/'+name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'colorspace':i.colorspace_settings.name,'resolution':list(i.size)})
def simple(v):
 if isinstance(v,(str,float,int,bool)):return v
 try:return list(v)
 except:return str(v)
def tree(t):
 return {'nodes':[{'name':n.name,'type':n.bl_idname,'image':getattr(getattr(n,'image',None),'name',None),'group':getattr(getattr(n,'node_tree',None),'name',None),'inputs':{i.identifier:simple(i.default_value) for i in n.inputs if hasattr(i,'default_value')}} for n in t.nodes],'links':[[l.from_node.name,l.from_socket.identifier,l.to_node.name,l.to_socket.identifier] for l in t.links]}
d={'scope':'Native Blender material recipes; Unity shader reconstruction required for procedural masks/eye layers/gaze. Extracted originals, no invented texture bake.','textures':images,'materials':{m.name:tree(m.node_tree) for m in bpy.data.materials if m.node_tree},'node_groups':{n.name:tree(n) for n in bpy.data.node_groups if n.bl_idname=='ShaderNodeTree'},'mesh_material_slots':{o.name:[getattr(m,'name',None) for m in o.data.materials] for o in bpy.data.objects if o.type=='MESH' and not o.hide_render}}
(E/'materials_textures.json').write_text(json.dumps(d,indent=2),encoding='utf8');print('R4_TEXTURES',len(images),flush=True)
