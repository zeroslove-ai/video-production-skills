"""Source-derived recovery data, exact original bytes/indices and evaluated outputs.
CPU-only factory process. Never writes source or edits canonical geometry/rig.
"""
import bpy,sys,json,hashlib,gzip
import numpy as np
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import props,custom,tree,snapshot,difference,val
from r4_appearance_adapter import ReactionLane
ROOT=HERE.parent;E=ROOT/'evidence/o1-source-fidelity-recovery-r1';E.mkdir(parents=True,exist_ok=True)
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-source-fidelity-recovery-r1');OUT.mkdir(parents=True,exist_ok=True)
OLD=OUT.parent/'o1-native-unity-probe-r1';SOURCE=ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):
    for p in (E/n,OUT/'metadata'/n):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
def binary(n,arrays):
    p=OUT/'data'/n;p.parent.mkdir(parents=True,exist_ok=True);np.savez_compressed(p,**arrays)
    return {'path':p.relative_to(OUT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size,'arrays':{k:{'shape':list(v.shape),'dtype':str(v.dtype)} for k,v in arrays.items()}}
def array(collection,field,width=3,dtype=np.float32):
    v=np.empty(len(collection)*width,dtype=dtype);collection.foreach_get(field,v);return v.reshape((-1,width)) if width>1 else v
def drivers(owner):
    ad=getattr(owner,'animation_data',None)
    if not ad:return []
    return [{'output_path':f.data_path,'array_index':f.array_index,'expression':f.driver.expression,'type':f.driver.type,'use_self':f.driver.use_self,'variables':[{'name':v.name,'type':v.type,'targets':[props(t) for t in v.targets]} for v in f.driver.variables],'fcurve':props(f),'keyframes':[{'co':list(k.co),'handle_left':list(k.handle_left),'handle_right':list(k.handle_right),'interpolation':k.interpolation} for k in f.keyframe_points],'modifiers':[[m.name,props(m)] for m in f.modifiers]} for f in ad.drivers]
def ui(owner):
    result={}
    for key in owner.keys():
        try:result[key]=owner.id_properties_ui(key).as_dict()
        except TypeError:pass
    return result
bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False);s=bpy.context.scene
actions=[a.name for a in bpy.data.actions];before=snapshot(actions);write('source_before_components.json',before)
source_renderers=json.loads((OLD/'metadata/source_renderers_bind.json').read_text(encoding='utf8'));meshes=[bpy.data.objects[r['name']] for r in source_renderers]
texture=[]
for index,image in enumerate(i for i in bpy.data.images if i.type!='RENDER_RESULT'):
    packed=[]
    for part,p in enumerate(image.packed_files):
        raw=bytes(p.packed_file.data);ext='.png' if raw.startswith(b'\x89PNG') else '.jpg' if raw.startswith(b'\xff\xd8') else '.bin'
        target=OUT/'textures'/f'{index:02d}_{part:02d}{ext}';target.parent.mkdir(exist_ok=True);target.write_bytes(raw)
        packed.append({'path':target.relative_to(OUT).as_posix(),'bytes':len(raw),'sha256':sha(target),'original_packed_filepath':p.filepath})
    texture.append({'image':image.name,'properties':props(image),'dimensions':list(image.size),'channels':image.channels,'colorspace':props(image.colorspace_settings),'alpha_mode':image.alpha_mode,'packed':packed})
write('exact_texture_receipt.json',texture)
materials={m.name:{'properties':props(m),'node_graph':tree(m.node_tree),'drivers':drivers(m),'principled_inputs':[{'node':n.name,'inputs':[{'name':x.name,'identifier':x.identifier,'default':val(getattr(x,'default_value',None)),'sources':[{'node':l.from_node.name,'socket':l.from_socket.identifier} for l in x.links]} for x in n.inputs]} for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED']} for m in bpy.data.materials if m.node_tree}
write('executable_material_graphs.json',materials);write('executable_geometry_node_graphs.json',{g.name:tree(g) for g in bpy.data.node_groups})
meshdata=[]
for o in meshes:
    m=o.data;arrays={'positions':array(m.vertices,'co'),'vertex_normals':array(m.vertices,'normal'),'loop_vertex_indices':array(m.loops,'vertex_index',1,np.int32),'polygon_loop_start':array(m.polygons,'loop_start',1,np.int32),'polygon_loop_total':array(m.polygons,'loop_total',1,np.int32),'polygon_material_slot':array(m.polygons,'material_index',1,np.int32),'edge_vertex_indices':array(m.edges,'vertices',2,np.int32)}
    attributes=[]
    for i,a in enumerate(m.attributes):
        if not len(a.data):continue
        fields=[]
        for prop in a.data[0].bl_rna.properties:
            if prop.identifier=='rna_type' or prop.type not in ('FLOAT','INT','BOOLEAN'):continue
            width=prop.array_length if prop.is_array else 1
            try:v=array(a.data,prop.identifier,width,np.float32 if prop.type=='FLOAT' else np.int32)
            except (TypeError,RuntimeError):continue
            key=f'attribute_{i}_{prop.identifier}';arrays[key]=v;fields.append({'property':prop.identifier,'array':key})
        attributes.append({'name':a.name,'domain':a.domain,'data_type':a.data_type,'fields':fields})
    uv=[]
    for i,u in enumerate(m.uv_layers):
        key=f'uv_{i}';arrays[key]=array(u.data,'uv',2);uv.append({'name':u.name,'array':key,'active_render':u.active_render,'active':u.active})
    keys=[]
    if m.shape_keys:
        for i,k in enumerate(m.shape_keys.key_blocks):
            key=f'shapekey_{i}_relative_delta';arrays[key]=array(k.data,'co')-array(k.relative_key.data,'co')
            keys.append({'name':k.name,'relative_key':k.relative_key.name,'value':k.value,'slider_min':k.slider_min,'slider_max':k.slider_max,'vertex_group':k.vertex_group,'mute':k.mute,'array':key})
    receipt=binary(o.name.replace('/','_')+'_original_mesh.npz',arrays)
    meshdata.append({'renderer':o.name,'matrix_world':[list(r) for r in o.matrix_world],'material_slots':[p.name for p in o.material_slots],'UV':uv,'attributes':attributes,'ShapeKeys':keys,'ShapeKey_drivers':drivers(m.shape_keys) if m.shape_keys else [],'file':receipt,'modifiers':[{'order':i,'name':mod.name,'type':mod.type,'settings':props(mod),'custom':custom(mod)} for i,mod in enumerate(o.modifiers)],'object_drivers':drivers(o),'constraints':[[c.name,props(c)] for c in o.constraints]})
write('mesh_slot_UV_attributes_shape_deltas.json',meshdata)
owners=[x for group in (bpy.data.objects,bpy.data.shape_keys,bpy.data.node_groups,bpy.data.materials) for x in group if getattr(x,'animation_data',None) and x.animation_data.drivers]
write('executable_driver_dependencies.json',[{'owner_type':x.bl_rna.identifier,'owner':x.name,'drivers':drivers(x),'custom_properties':custom(x),'property_UI':ui(x)} for x in owners])
board=bpy.data.objects['AVATAR_FaceBoard'];head=bpy.data.objects['Character_Body_Head'];hair=bpy.data.objects['Hair_Rig_R4']
write('controls_contract.json',{'FaceBoard13':[{'name':b.name,'unit':'bone LOCAL translation meters; normalized intent y/max_y, not world translation','default_location':list(b.location),'constraints':[[c.name,props(c)] for c in b.constraints]} for b in board.pose.bones],'head':{'properties':custom(head),'UI':ui(head)},'hair':{'properties':custom(hair),'UI':ui(hair)},'order':'body evaluated pose → existing face COPY_TRANSFORMS helpers → head/globe GN before armature skin; hair root follower→existing driven eulers; Blender dependency graph resolves driver targets, not arbitrary Unity Update order'})
def evaluate(tag,names):
    s.frame_set(s.frame_current);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();a={};manifest=[]
    for name in names:
        o=bpy.data.objects[name];ev=o.evaluated_get(deps);m=ev.to_mesh();local=array(m.vertices,'co');normal=array(m.vertices,'normal');mw=np.array(ev.matrix_world,dtype=np.float64);world=(local@mw[:3,:3].T+mw[:3,3]).astype(np.float32);nw=normal@np.linalg.inv(mw[:3,:3]);nw/=np.maximum(np.linalg.norm(nw,axis=1,keepdims=True),1e-30)
        a[name+'_local_position']=local;a[name+'_world_position']=world;a[name+'_local_normal']=normal;a[name+'_world_normal']=nw.astype(np.float32);manifest.append({'mesh':name,'vertex_count':len(local),'index':'source vertex order; no topology-altering GN at these samples'});ev.to_mesh_clear()
    return {'tag':tag,'geometry':binary(tag+'.npz',a),'meshes':manifest,'driver_outputs':[{'owner':x.name,'path':f.data_path,'array_index':f.array_index,'value':val(x.path_resolve(f.data_path)[f.array_index]) if hasattr(x.path_resolve(f.data_path),'__len__') and not isinstance(x.path_resolve(f.data_path),str) else val(x.path_resolve(f.data_path))} for x in owners for f in x.animation_data.drivers],'rig_pose':{n:{b.name:[list(r) for r in bpy.data.objects[n].matrix_world@b.matrix] for b in bpy.data.objects[n].pose.bones} for n in ('Meshy_Fitted_Rig','Armature','Hair_Rig_R4')},'modifier_evaluated_settings':{o.name:[[m.name,props(m)] for m in o.modifiers] for o in meshes}}
refs=[evaluate('neutral',[o.name for o in meshes])]
for i,b in enumerate(board.pose.bones):
    original=b.location.copy();limit=next(c for c in b.constraints if c.type=='LIMIT_LOCATION').max_y
    for fraction in (.5,1):
        b.location.y=limit*fraction;board.update_tag();refs.append(evaluate(f'board_{i:02d}_{fraction}', ['Character_Body_Head','Globe.L','Globe.R']))
    b.location=original;board.update_tag();bpy.context.view_layer.update()
saved={k:head[k] for k in ('Face_GazeYaw','Face_GazePitch')}
for yaw,pitch in ((-1,0),(1,0),(0,-1),(0,1)):
    head['Face_GazeYaw']=yaw;head['Face_GazePitch']=pitch;head.update_tag();refs.append(evaluate(f'gaze_{yaw}_{pitch}',['Character_Body_Head','Globe.L','Globe.R']))
for k,v in saved.items():head[k]=v
head.update_tag();bpy.context.view_layer.update()
hair_props={k:hair[k] for k in hair.keys() if isinstance(hair[k],(int,float))}
for i,(k,v) in enumerate(hair_props.items()):
    limits=ui(hair).get(k,{});maximum=limits.get('soft_max',limits.get('max',v));minimum=limits.get('soft_min',limits.get('min',v));sample=max(minimum,min(maximum,v+10))
    if sample==v:continue
    hair[k]=sample;hair.update_tag();refs.append(evaluate(f'hair_knob_{i:02d}',['Hair_Replacement_R4']));hair[k]=v;hair.update_tag()
lane=ReactionLane()
for clip,frame in (('Startle_Short',19),('Lift_Start',31),('Struggle_Light_Loop',16),('Struggle_Strong_Loop',1),('Struggle_Strong_Loop',25),('Struggle_Strong_Loop',49),('Land_Soft',22),('BalanceRecover',28)):
    lane.on('YRA_R4_'+clip) if 'YRA_R4_'+clip in bpy.data.actions else None
    if lane.saved is None:
        lib=OUT.parent/'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'
        with bpy.data.libraries.load(str(lib),link=False) as (src,dst):dst.actions=['YRA_R4_'+clip]
        lane.on('YRA_R4_'+clip)
    s.frame_set(frame);refs.append(evaluate(f'motion_{clip}_{frame}',[o.name for o in meshes]));lane.off()
write('evaluated_driver_geometry_references.json',refs)
after=snapshot(actions);diff=difference(before,after);write('source_after_components.json',after);write('source_component_diff.json',diff);assert not diff,diff
write('SOURCE_DATA_RECEIPT.json',{'source_SHA256':sha(SOURCE),'component_differences':0,'packed_images':sum(len(r['packed']) for r in texture),'source_renderer_meshes':len(meshdata),'evaluated_reference_cases':len(refs),'material_graphs':len(materials),'source_saved':False,'canonical_geometry_rest_weights_drivers_actions_changed':False,'float_array_format':'NPZ float32 source RNA values; world evaluation matrices mathutils float32; texture bytes exact without image re-encode','prior_packet_reuse':str(OLD),'unsupported_runtime':'Blender node/driver semantics provided; Unity implementation remains consumer feasibility HOLD'})
print('SOURCE_RECOVERY_DATA_COMPLETE',len(refs))
