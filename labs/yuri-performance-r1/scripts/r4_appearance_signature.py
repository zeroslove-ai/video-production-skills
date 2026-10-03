"""Read-only hashes of source appearance, hierarchy, drivers and OFF evaluation."""
import bpy,json,hashlib,struct,array
from native_preservation import signature,digest

def val(v):
    if isinstance(v,bpy.types.ID):return [v.bl_rna.identifier,v.name]
    if isinstance(v,(str,int,float,bool)) or v is None:return v
    if isinstance(v,bpy.types.bpy_struct):return [v.bl_rna.identifier,getattr(v,'name',None)]
    if hasattr(v,'items'):
        try:return {k:val(x) for k,x in v.items()}
        except TypeError:pass
    try:return [val(x) for x in v]
    except TypeError:return [getattr(v,'bl_rna',None).identifier if hasattr(v,'bl_rna') else type(v).__name__,getattr(v,'name',None)]

def props(x):
    result={}
    for p in x.bl_rna.properties:
        if p.identifier in {'rna_type','name','pixels','session_uid','is_updated','is_updated_data','is_updated_transform','users','use_fake_user','is_runtime_data'} or p.type=='COLLECTION':continue
        try:result[p.identifier]=val(getattr(x,p.identifier))
        except (TypeError,ValueError,AttributeError):pass
    return result

def custom(x):
    try:return {k:val(x[k]) for k in x.keys() if k!='_RNA_UI'}
    except TypeError:return {}

def anim(x):
    a=getattr(x,'animation_data',None)
    if not a:return None
    return {'binding':props(a),'drivers':[[f.data_path,f.array_index,props(f),props(f.driver),
        [[props(v),[props(t) for t in v.targets]] for v in f.driver.variables]] for f in a.drivers],
        'nla':[[props(t),[props(s) for s in t.strips]] for t in a.nla_tracks]}

def tree(t):
    if t is None:return None
    return {'props':props(t),'custom':custom(t),'animation':anim(t),
        'nodes':[[n.name,props(n),custom(n),
                  [props(n.color_ramp),[props(e) for e in n.color_ramp.elements]] if hasattr(n,'color_ramp') else None,
                  [props(n.mapping),[[props(p) for p in c.points] for c in n.mapping.curves]] if hasattr(n,'mapping') and hasattr(n.mapping,'curves') else None,
                  [[s.identifier,props(s)] for s in n.inputs],
                  [[s.identifier,props(s)] for s in n.outputs]] for n in t.nodes],
        'links':[[l.from_node.name,l.from_socket.identifier,l.to_node.name,l.to_socket.identifier] for l in t.links],
        'interface':[[i.name,props(i)] for i in t.interface.items_tree]}

def attribute_hash(a):
    if not len(a.data):return ''
    d=a.data[0];fields=[]
    for p in d.bl_rna.properties:
        if p.identifier=='rna_type' or p.type not in {'FLOAT','INT','BOOLEAN'}:continue
        count=p.array_length if p.is_array else 1
        buf=array.array('f' if p.type=='FLOAT' else 'i',[0])*(len(a.data)*count)
        try:a.data.foreach_get(p.identifier,buf)
        except (TypeError,RuntimeError):continue
        fields.append([p.identifier,hashlib.sha256(buf.tobytes()).hexdigest()])
    return fields

def snapshot(action_names):
    s=bpy.context.scene;s.frame_set(s.frame_current,subframe=s.frame_subframe);bpy.context.view_layer.update()
    out=signature(action_names)
    print('FINGERPRINT geometry/keys/weights/actions',flush=True)
    out['objects']={o.name:digest({'props':props(o),'custom':custom(o),'anim':anim(o),
        'modifiers':[[m.name,props(m),custom(m)] for m in o.modifiers],
        'constraints':[[c.name,props(c)] for c in o.constraints],
        'materials':[[p.name,props(p)] for p in o.material_slots],
        'groups':[[g.name,g.index,g.lock_weight] for g in o.vertex_groups],
        'pose':[[b.name,props(b),custom(b),[[c.name,props(c)] for c in b.constraints]] for b in o.pose.bones] if o.type=='ARMATURE' else None}) for o in bpy.data.objects}
    out['mesh_attributes']={m.name:digest({'props':props(m),
        'vertices':[[*v.co,*v.normal,v.hide,v.select] for v in m.vertices],
        'edges':[[*e.vertices,e.use_edge_sharp,e.use_seam] for e in m.edges],
        'polygons':[[*p.vertices,p.material_index,p.use_smooth] for p in m.polygons],
        'attributes':[[a.name,a.data_type,a.domain,attribute_hash(a)] for a in m.attributes],
        'keys':{'props':props(m.shape_keys),'anim':anim(m.shape_keys),'blocks':[[k.name,props(k)] for k in m.shape_keys.key_blocks]} if m.shape_keys else None}) for m in bpy.data.meshes}
    out['rest_pose_settings']={o.name:digest([[b.name,props(b),custom(b)] for b in o.data.bones]) for o in bpy.data.objects if o.type=='ARMATURE'}
    print('FINGERPRINT hierarchy/rest/attributes',flush=True)
    out['materials']={m.name:digest([props(m),custom(m),anim(m),tree(m.node_tree)]) for m in bpy.data.materials}
    out['node_groups']={t.name:digest(tree(t)) for t in bpy.data.node_groups}
    out['textures']={i.name:digest([props(i),props(i.colorspace_settings),
        [hashlib.sha256(p.packed_file.data).hexdigest() for p in i.packed_files]]) for i in bpy.data.images if i.type!='RENDER_RESULT'}
    out['worlds']={w.name:digest([props(w),tree(w.node_tree)]) for w in bpy.data.worlds}
    print('FINGERPRINT shaders/drivers/packed-textures',flush=True)
    out['camera_lights']={o.name:digest(props(o.data)) for o in bpy.data.objects if o.type in {'CAMERA','LIGHT'}}
    out['scene']=digest([s.name,s.frame_current,s.frame_subframe,s.frame_start,s.frame_end,
        props(s.render),props(s.cycles),props(s.view_settings),props(s.display_settings),s.camera.name,
        [[c.name,props(c)] for c in bpy.data.collections]])
    deps=bpy.context.evaluated_depsgraph_get();evaluated={}
    for o in bpy.data.objects:
        if o.type!='MESH':continue
        e=o.evaluated_get(deps);m=e.to_mesh();h=hashlib.sha256()
        for v in m.vertices:h.update(struct.pack('<3d',*(e.matrix_world@v.co)))
        for p in m.polygons:h.update(struct.pack('<'+'I'*len(p.vertices),*p.vertices))
        evaluated[o.name]=h.hexdigest();e.to_mesh_clear()
    out['evaluated_geometry_world']=evaluated
    return out

def difference(a,b):
    return {category:[k for k in sorted(set(a[category])|set(b.get(category,{}))) if a[category].get(k)!=b.get(category,{}).get(k)]
        if isinstance(a[category],dict) else ['value'] for category in a if a[category]!=b.get(category)}
