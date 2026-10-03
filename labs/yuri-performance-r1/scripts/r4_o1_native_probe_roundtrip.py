"""Measure native FBX pair path/rest/motion/deformation, using fresh imports.
No source writes; original source remains immutable. QA disposal affects only
this isolated background process. No Unity/PBR/driver fidelity claim.
"""
import bpy,sys,json,gzip,math,hashlib
from pathlib import Path
from mathutils import Matrix,Vector
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import props,digest
ROOT=HERE.parent;E=ROOT/'evidence/o1-native-unity-probe-r1';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-native-unity-probe-r1')
SOURCE=ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend';RIG_NAMES=['Meshy_Fitted_Rig','Armature','Hair_Rig_R4','AVATAR_FaceBoard']
MODEL=OUT/'YURI_O1_R4_NATIVE_CARRIER_20261003_R1.fbx';MOTION=OUT/'YURI_O1_R4_NATIVE_ANIMATION_ONLY_20261003_R1.fbx'
def load(n):return json.loads((OUT/'metadata'/n).read_text(encoding='utf8'))
def zipped(n):
    with gzip.open(OUT/'reference'/n,'rt',encoding='utf8') as f:return json.load(f)
def write(n,v):
    for p in (E/n,OUT/'metadata'/n):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
def rows(m):return [list(r) for r in m]
def path(o):return (path(o.parent)+'/' if o.parent else '')+o.name
def rig_info(o):
    return {'name':o.name,'path':path(o),'matrix_world':rows(o.matrix_world),'matrix_local':rows(o.matrix_local),'bones':[{'index':i,'name':b.name,'parent':b.parent.name if b.parent else None,'local_rest':rows(b.parent.matrix_local.inverted()@b.matrix_local if b.parent else b.matrix_local),'armature_rest':rows(b.matrix_local),'world_rest':rows(o.matrix_world@b.matrix_local)} for i,b in enumerate(o.data.bones)]}
def matrix_error(a,b):return max(abs(a[i][j]-b[i][j]) for i in range(4) for j in range(4))
def rotation_error(a,b):
    qa=list(a.to_quaternion());qb=list(b.to_quaternion())
    dot=abs(sum(x*y for x,y in zip(qa,qb))/math.sqrt(sum(x*x for x in qa)*sum(y*y for y in qb)))
    return 2*math.acos(min(1,max(0,dot)))
source_rigs=load('source_expanded_rigs.json');export=load('export_manifest.json');refs=zipped('native_evaluated_all_frames.json.gz');neutral=zipped('source_neutral_evaluated_world_vertices.json.gz')
# Factory process currently owns only its default cube; remove disposable defaults.
for o in list(bpy.data.objects):bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.import_scene.fbx(filepath=str(MODEL),use_anim=False,automatic_bone_orientation=False,force_connect_children=False)
model_objects=list(bpy.data.objects);model_rigs={n:bpy.data.objects[n] for n in RIG_NAMES};model_meshes={o.name:o for o in model_objects if o.type=='MESH'}
model_info={n:rig_info(o) for n,o in model_rigs.items()};write('imported_model_expanded_rigs.json',model_info)
renderer=[]
for n,o in model_meshes.items():
    mods=[m for m in o.modifiers if m.type=='ARMATURE']
    renderer.append({'name':n,'path':path(o),'vertices':len(o.data.vertices),'polygons':len(o.data.polygons),'UV_layers':[u.name for u in o.data.uv_layers],'material_slots':[p.name for p in o.material_slots],'shape_keys':[k.name for k in o.data.shape_keys.key_blocks] if o.data.shape_keys else [],'matrix_world':rows(o.matrix_world),'armature_bindings':[{'target':m.object.name,'settings':props(m),'bone_indices':[{'index':i,'name':b.name,'inverse_bind_rest_mesh_to_bone':rows((m.object.matrix_world@b.matrix_local).inverted()@o.matrix_world)} for i,b in enumerate(m.object.data.bones)]} for m in mods]})
write('imported_renderer_bind.json',renderer)
original_meshes={m['name']:m for m in load('source_renderers_bind.json')};rep=[]
for n,o in model_meshes.items():
    rep.append({'name':n,'source_vertices':original_meshes[n]['vertices'],'imported_vertices':len(o.data.vertices),'source_polygons':original_meshes[n]['polygons'],'imported_polygons':len(o.data.polygons),'source_shape_key_count':len(original_meshes[n]['shape_keys']),'imported_shape_key_count':len(o.data.shape_keys.key_blocks) if o.data.shape_keys else 0,'source_material_slot_names':original_meshes[n]['material_slots'],'imported_slot_names':[p.name for p in o.material_slots],'vertex_split_or_reorder_policy':'FBX UV/normal/material loop representation; compare counts/positions explicitly; no source mesh edit'})
write('mesh_representation_comparison.json',rep)
before=set(bpy.data.objects);action_before=set(bpy.data.actions)
bpy.ops.import_scene.fbx(filepath=str(MOTION),use_anim=True,automatic_bone_orientation=False,force_connect_children=False)
added=[o for o in bpy.data.objects if o not in before];actions=[a for a in bpy.data.actions if a not in action_before]
anim_rigs={n:next(o for o in added if o.type=='ARMATURE' and (o.name==n or o.name.startswith(n+'.'))) for n in RIG_NAMES}
anim_info={n:rig_info(o) for n,o in anim_rigs.items()};write('imported_animation_expanded_rigs.json',anim_info)
print('IMPORTED_ACTIONS',[(a.name,[(s.identifier,s.target_id_type) for s in a.slots]) for a in actions],flush=True)
pair=[]
for n in RIG_NAMES:
    mb=model_info[n]['bones'];ab=anim_info[n]['bones'];source=source_rigs[n]['bones'];by_source={b['name']:b for b in source}
    ordered=[b['name'] for b in mb]==[b['name'] for b in ab]
    parents=[(b['name'],b['parent']) for b in mb]==[(b['name'],b['parent']) for b in ab]
    rest=max(matrix_error(a['local_rest'],b['local_rest']) for a,b in zip(mb,ab)) if ordered else None
    original_world_rest=max(matrix_error(b['world_rest'],by_source[b['name']]['world_rest']) for b in mb)
    pair.append({'rig':n,'source_bones':len(source),'model_bones':len(mb),'animation_bones':len(ab),'ordered_model_animation_names_equal':ordered,'parents_equal':parents,'pair_max_local_rest_matrix_element_delta':rest,'model_vs_source_max_world_rest_matrix_element_delta':original_world_rest,'source_index_to_import_index':{str(b['index']):next(m['index'] for m in mb if m['name']==b['name']) for b in source},'PASS':ordered and parents and rest is not None and rest<1e-5 and len(mb)==len(source)})
write('pair_path_rest_comparison.json',pair)
# Resolve explicit imported OBJECT slots, never an arbitrary fallback.
clip_map={name:{} for name in refs}
for a in actions:
    name=next((n for n in refs if n in a.name),None)
    if not name:continue
    target=a.name.split('|',1)[0]
    rig=next((n for n,o in anim_rigs.items() if target==o.name),None)
    if rig is None:continue # Exported ancestry-object constant tracks are separately declared.
    slots=[slot for slot in a.slots if slot.target_id_type=='OBJECT']
    assert len(slots)==1,(a.name,[slot.identifier for slot in slots])
    assert rig not in clip_map[name],(a.name,rig)
    clip_map[name][rig]=(a,slots[0])
assert all('Meshy_Fitted_Rig' in v for v in clip_map.values()),{k:list(v) for k,v in clip_map.items()}
write('take_and_slot_inventory.json',[{'authored_Action':n,'logical':n.replace('YRA_R4_','YRA_R1_'),'imported_rig_actions':[{'rig':r,'action':a.name,'slot':s.identifier,'target_id_type':s.target_id_type} for r,(a,s) in data.items()]} for n,data in clip_map.items()])
for o in added:bpy.data.objects.remove(o,do_unlink=True)
s=bpy.context.scene;s.render.fps=24;s.render.fps_base=1
def off():
    for o in model_rigs.values():
        if o.animation_data:o.animation_data.action=None
        for b in o.pose.bones:b.matrix_basis=Matrix.Identity(4)
    s.frame_set(1);bpy.context.view_layer.update()
def bind(name):
    for n,o in model_rigs.items():
        if n not in clip_map[name]:continue
        a,slot=clip_map[name][n];o.animation_data_create();o.animation_data.action=a;o.animation_data.action_slot=slot
def geometry_difference():
    deps=bpy.context.evaluated_depsgraph_get();stats=[]
    for n,o in model_meshes.items():
        e=o.evaluated_get(deps);m=e.to_mesh();expected=neutral[n]
        if len(expected)==len(m.vertices):
            ds=[(e.matrix_world@v.co-Vector(p)).length for v,p in zip(m.vertices,expected)];row={'mesh':n,'vertices':len(ds),'source_import_count_equal':True,'max_corresponding_vertex_delta_m':max(ds),'mean_corresponding_vertex_delta_m':sum(ds)/len(ds)}
        else:row={'mesh':n,'source_import_count_equal':False,'source_vertices':len(expected),'imported_vertices':len(m.vertices)}
        stats.append(row);e.to_mesh_clear()
    return stats
off();neutral_stats=geometry_difference();write('neutral_geometry_comparison.json',neutral_stats)
checks=[];quarter=[]
for name,frames in refs.items():
    off();bind(name);end=len(frames);loop='Loop' in name;count=2*(end-1)+1 if loop else end;first=None;previous=None;actual=0;step=0;root=[];errors={n:0 for n in RIG_NAMES};orientation={n:0 for n in RIG_NAMES};world_samples={};seam=None
    for f in range(1,count+1):
        local=1+(f-1)%(end-1) if loop and f>end else f;s.frame_set(local);bpy.context.view_layer.update();v={}
        for n,o in model_rigs.items():
            v[n]={b.name:(o.matrix_world@b.matrix).copy() for b in o.pose.bones}
            for bone,m in v[n].items():
                reference=Matrix(frames[local-1][n][bone]['world_matrix']);errors[n]=max(errors[n],(m.translation-reference.translation).length);orientation[n]=max(orientation[n],rotation_error(m,reference))
        body=v['Meshy_Fitted_Rig']
        if first is None:first={n:m.copy() for n,m in body.items()}
        actual=max(actual,max((m.translation-first[n].translation).length for n,m in body.items() if n!='root'))
        if previous:step=max(step,max((m.translation-previous[n].translation).length for n,m in body.items()))
        previous=body;root.append(body['root'].translation.copy())
        if f==end:seam=max((body[n].translation-first[n].translation).length for n in body)
        if f in {1,1+round((end-1)*.25),1+round((end-1)*.5),end}:world_samples[str(f)]={n:{b:list(m.translation) for b,m in bones.items()} for n,bones in v.items()}
    checks.append({'action':name,'frames_sampled':count,'fps':24,'duration_seconds':(end-1)/24,'loop_cycles':2 if loop else 1,'actual_non_root_motion_m':actual,'max_body_bone_step_m':step,'root_excursion_m':max((p-root[0]).length for p in root),'loop_seam_position_m':seam if loop else None,'max_source_world_joint_error_m_by_rig':errors,'max_source_world_rotation_error_deg_by_rig':{n:math.degrees(v) for n,v in orientation.items()},'actual_motion':'PASS' if actual>1e-4 else 'FAIL','source_pose_fidelity':'PASS' if max(errors.values())<1e-4 else 'FAIL','loops':'PASS' if not loop or seam<1e-5 else 'FAIL'})
    checks[-1]['source_pose_fidelity']='PASS' if max(errors.values())<1e-4 and max(math.degrees(v) for v in orientation.values())<.001 else 'FAIL'
    checks[-1]['source_pose_fidelity_criteria']={'position_m':1e-4,'rotation_deg':.001,'rotation_method':'normalized quaternion dot in Python double'}
    quarter.append({'action':name,'imported_world_landmark_samples_0_25_50_100_percent':world_samples})
off();write('roundtrip_motion.json',checks);write('roundtrip_world_landmarks.json',quarter)
write('roundtrip_receipt.json',{'pair_static_contract_PASS':all(p['PASS'] for p in pair),'six_actual_clips':len(checks),'actual_motion_PASS':all(c['actual_motion']=='PASS' for c in checks),'source_pose_fidelity_PASS':all(c['source_pose_fidelity']=='PASS' for c in checks),'loop_2cycles_PASS':all(c['loops']=='PASS' for c in checks),'native_source_geometry_visual_PASS':False,'Unity_PASS':False,'status':'COMPATIBILITY PROBE; visual/deformation/driver gates remain HOLD'})
# Save scratch imported carrier + imported animation, never source or old outputs.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'YURI_O1_R4_NATIVE_IMPORTED_QA_20261003_R1.blend'),relative_remap=False)
print('ROUNDTRIP_COMPLETE',checks,flush=True)
