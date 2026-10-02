"""Fingerprints of original actions, rest rigs, meshes, native keys and skin weights."""
import bpy,json,hashlib
def digest(value):return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()
def signature(action_names):
    actions={}
    for name in action_names:
        a=bpy.data.actions[name];curves=[]
        for layer in a.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for fc in bag.fcurves:curves.append([fc.data_path,fc.array_index,[[*k.co,*k.handle_left,*k.handle_right,k.interpolation] for k in fc.keyframe_points]])
        actions[name]=digest(curves)
    meshes={}
    for o in bpy.data.objects:
        if o.type!='MESH':continue
        shapes=[[k.name,[list(v.co) for v in k.data]] for k in o.data.shape_keys.key_blocks] if o.data.shape_keys else []
        meshes[o.name]=digest([[list(v.co) for v in o.data.vertices],[[*p.vertices] for p in o.data.polygons],shapes,[[[g.group,g.weight] for g in v.groups] for v in o.data.vertices]])
    rigs={o.name:digest([[b.name,b.parent.name if b.parent else None,list(b.head_local),list(b.tail_local),b.use_connect,b.use_deform] for b in o.data.bones]) for o in bpy.data.objects if o.type=='ARMATURE'}
    return {'actions':actions,'meshes_shape_keys_weights':meshes,'rest_rigs':rigs}
