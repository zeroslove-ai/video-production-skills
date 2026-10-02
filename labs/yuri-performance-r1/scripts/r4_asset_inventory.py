"""Read-only inventory of handoff source files; never saves a source blend."""
import bpy, sys, json, hashlib, math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from native_preservation import signature,digest
src,out=map(Path,sys.argv[sys.argv.index('--')+1:])
sha=hashlib.sha256(src.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(src))
rigs={}
for o in bpy.data.objects:
 if o.type=='ARMATURE':
  rigs[o.name]={'parent':getattr(o.parent,'name',None),'matrix_world':[list(r) for r in o.matrix_world],'bones':[{ 'name':b.name,'parent':getattr(b.parent,'name',None),'head':list(b.head_local),'tail':list(b.tail_local),'deform':b.use_deform,'matrix':[list(r) for r in b.matrix_local]} for b in o.data.bones]}
meshes={}
for o in bpy.data.objects:
 if o.type!='MESH':continue
 vs=o.data.vertices;weights=[[[o.vertex_groups[g.group].name,g.weight] for g in v.groups] for v in vs]
 keys=o.data.shape_keys
 meshes[o.name]={'vertices':len(vs),'polygons':len(o.data.polygons),'parent':getattr(o.parent,'name',None),'matrix_world':[list(r) for r in o.matrix_world],'modifiers':[[m.name,m.type,getattr(getattr(m,'object',None),'name',None)] for m in o.modifiers],'materials':[getattr(m,'name',None) for m in o.data.materials],'uv_layers':[x.name for x in o.data.uv_layers],'geometry_sha':digest([list(v.co) for v in vs]),'weights_sha':digest(weights),'unweighted_vertices':sum(not w for w in weights),'influences_gt4':sum(len(w)>4 for w in weights),'weight_sum_max_error':max([abs(sum(g[1] for g in w)-1) for w in weights if w] or [0]),'shape_keys':{k.name:{'sha':digest([list(v.co) for v in k.data]),'max_delta':max([(v.co-b.co).length for v,b in zip(k.data,keys.key_blocks[0].data)] or [0])} for k in keys.key_blocks} if keys else {}}
images=[{'name':i.name,'path':i.filepath,'resolved':bpy.path.abspath(i.filepath),'packed':bool(i.packed_file),'exists':Path(bpy.path.abspath(i.filepath)).is_file(),'size':list(i.size),'source':i.source} for i in bpy.data.images]
materials={m.name:{'nodes':[[n.name,n.bl_idname,getattr(getattr(n,'image',None),'name',None)] for n in m.node_tree.nodes] if m.node_tree else [],'diffuse':list(m.diffuse_color)} for m in bpy.data.materials}
actions=[{'name':a.name,'range':list(a.frame_range),'slots':[[s.identifier,s.target_id_type] for s in a.slots]} for a in bpy.data.actions]
drivers=[]
for ids in (bpy.data.objects,bpy.data.shape_keys,bpy.data.node_groups):
 for o in ids:
  if o.animation_data:
   drivers.extend([{'owner':o.name,'path':f.data_path,'expression':f.driver.expression,'mute':f.mute} for f in o.animation_data.drivers])
d={'source_name':src.name,'source_sha256':sha,'source_bytes':src.stat().st_size,'source_unchanged':sha==hashlib.sha256(src.read_bytes()).hexdigest(),'blender':bpy.app.version_string,'unit_system':bpy.context.scene.unit_settings.system,'unit_scale':bpy.context.scene.unit_settings.scale_length,'fps':bpy.context.scene.render.fps,'rigs':rigs,'meshes':meshes,'images':images,'materials':materials,'actions':actions,'drivers':drivers,'fingerprints':signature([a.name for a in bpy.data.actions]),'vrm_addon_modules':[a.module for a in bpy.context.preferences.addons if 'vrm' in a.module.lower()]}
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(d,indent=2),encoding='utf8')
print('INVENTORY',src.name,len(actions),{k:len(v['bones']) for k,v in rigs.items()},'missing_images',[i['name'] for i in images if i['source']=='FILE' and not i['packed'] and not i['exists']])
