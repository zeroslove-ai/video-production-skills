"""One native-hierarchy FBX serialization probe. Immutable source, no rig rebuild.

Background --factory-startup --disable-autoexec only. All temporary selection/NLA
state restored; no source/Action/prior output save. Native 4 rig names retained.
"""
import bpy,sys,json,gzip,hashlib,math,shutil
from pathlib import Path
from mathutils import Matrix
from bpy_extras.io_utils import axis_conversion
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference,props,custom,anim,digest
from r4_appearance_adapter import ReactionLane
ROOT=HERE.parent;E=ROOT/'evidence/o1-native-unity-probe-r1';WORK=ROOT/'local/o1-native-unity-probe-r1'
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-native-unity-probe-r1')
SOURCE=ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
LIB=OUT.parent/'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'
RIG_NAMES=['Meshy_Fitted_Rig','Armature','Hair_Rig_R4','AVATAR_FaceBoard']
CLIPS=['YRA_R4_'+n for n in ['Startle_Short','Lift_Start','Struggle_Light_Loop','Struggle_Strong_Loop','Land_Soft','BalanceRecover']]
MODEL='YURI_O1_R4_NATIVE_CARRIER_20261003_R1.fbx';MOTION='YURI_O1_R4_NATIVE_ANIMATION_ONLY_20261003_R1.fbx'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(m):return [list(r) for r in m]
def write(n,v):
    for p in (E/n,OUT/'metadata'/n):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
def zipped(n,v):
    p=OUT/'reference'/n;p.parent.mkdir(parents=True,exist_ok=True)
    with gzip.open(p,'wt',encoding='utf8') as f:json.dump(v,f,separators=(',',':'))
def object_path(o):return (object_path(o.parent)+'/' if o.parent else '')+o.name
def bone_path(o,b):return object_path(o)+'/'+('/'.join(reversed([b.name]+[p.name for p in b.parent_recursive])))
def rig_info(o):
    return {'name':o.name,'parent':o.parent.name if o.parent else None,'path':object_path(o),'object_world':rows(o.matrix_world),'object_local':rows(o.matrix_local),'source_scale':list(o.scale),
        'bones':[{'index':i,'name':b.name,'parent':b.parent.name if b.parent else None,'path':bone_path(o,b),'deform':b.use_deform,'connected':b.use_connect,'inherit_scale':b.inherit_scale,'inherit_rotation':b.use_inherit_rotation,
            'armature_rest':rows(b.matrix_local),'local_rest':rows(b.parent.matrix_local.inverted()@b.matrix_local if b.parent else b.matrix_local),'world_rest':rows(o.matrix_world@b.matrix_local),
            'neutral_pose_channels':{'location':list(o.pose.bones[b.name].location),'rotation_mode':o.pose.bones[b.name].rotation_mode,'quaternion_wxyz':list(o.pose.bones[b.name].rotation_quaternion),'euler':list(o.pose.bones[b.name].rotation_euler),'scale':list(o.pose.bones[b.name].scale)},
            'neutral_evaluated_armature':rows(o.pose.bones[b.name].matrix),'neutral_evaluated_world':rows(o.matrix_world@o.pose.bones[b.name].matrix),
            'constraints':[[c.name,props(c)] for c in o.pose.bones[b.name].constraints]} for i,b in enumerate(o.data.bones)]}
OUT.mkdir(parents=True,exist_ok=True);WORK.mkdir(parents=True,exist_ok=True)
assert sha(SOURCE)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
assert sha(LIB)=='6874ec69d5721f385d31edaa06ef0d58c89a543b98bacd961f8f575ff57eef4d'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False)
s=bpy.context.scene;original_actions=[a.name for a in bpy.data.actions];before=snapshot(original_actions)
rigs=[bpy.data.objects[n] for n in RIG_NAMES];r=rigs[0]
source_rigs={o.name:rig_info(o) for o in rigs};write('source_expanded_rigs.json',source_rigs)
meshes=[o for o in bpy.data.objects if o.type=='MESH' and not o.hide_render and any(m.type=='ARMATURE' and m.object in rigs for m in o.modifiers)]
selected=set(rigs+meshes)
for o in list(selected):
    p=o.parent
    while p:selected.add(p);p=p.parent
ordered_objects=sorted(selected,key=lambda o:object_path(o))
objects=[{'name':o.name,'type':o.type,'path':object_path(o),'parent':o.parent.name if o.parent else None,'matrix_world':rows(o.matrix_world),'matrix_local':rows(o.matrix_local)} for o in ordered_objects]
body_map=json.loads((WORK/'intake/current-runtime-body-map.json').read_text(encoding='utf8'))['bodyMap']
semantics=[{'semantic':v['semantic'],'native_name':v['name'],'original_native_path':bone_path(r,r.data.bones[v['name']]),'Laptop_control_reference_path':v['path'],'metadata_paths_equal':bone_path(r,r.data.bones[v['name']])==v['path'],'native_local_rest':rows(r.data.bones[v['name']].parent.matrix_local.inverted()@r.data.bones[v['name']].matrix_local)} for v in body_map]
write('semantic_mapping.json',semantics)
assert len(semantics)==51 and len(r.data.bones)==57
geometry={};renderers=[];weights={};deps=bpy.context.evaluated_depsgraph_get()
for o in meshes:
    ev=o.evaluated_get(deps);m=ev.to_mesh();geometry[o.name]=[list(ev.matrix_world@v.co) for v in m.vertices];ev.to_mesh_clear()
    mods=[m for m in o.modifiers if m.type=='ARMATURE'];binding=[]
    for mod in mods:
        arm=mod.object;binding.append({'modifier':mod.name,'settings':props(mod),'target':arm.name,'target_path':object_path(arm),'bone_indices':[{ 'index':i,'name':b.name,'inverse_bind_rest_mesh_to_bone':rows((arm.matrix_world@b.matrix_local).inverted()@o.matrix_world),'inverse_bind_evaluated_neutral_mesh_to_bone':rows((arm.matrix_world@arm.pose.bones[b.name].matrix).inverted()@o.matrix_world)} for i,b in enumerate(arm.data.bones)]})
    renderers.append({'name':o.name,'path':object_path(o),'matrix_world':rows(o.matrix_world),'matrix_local':rows(o.matrix_local),'vertices':len(o.data.vertices),'polygons':len(o.data.polygons),'UV_layers':[u.name for u in o.data.uv_layers],'material_slots':[p.name for p in o.material_slots],'shape_keys':[k.name for k in o.data.shape_keys.key_blocks] if o.data.shape_keys else [],'ordered_modifiers':[[m.name,m.type,props(m)] for m in o.modifiers],'armature_bindings':binding})
    weights[o.name]={'vertex_indices':'source mesh vertex order; do not silently remap','groups':[g.name for g in o.vertex_groups],'influences':[[[g.group,g.weight] for g in v.groups] for v in o.data.vertices]}
zipped('source_neutral_evaluated_world_vertices.json.gz',geometry);zipped('source_original_vertex_weights.json.gz',weights)
write('source_renderers_bind.json',renderers)
driver_owners={d.name:anim(d) for collection in [bpy.data.objects,bpy.data.shape_keys,bpy.data.materials,bpy.data.node_groups] for d in collection if getattr(d,'animation_data',None) and len(d.animation_data.drivers)}
write('source_driver_graph.json',driver_owners)
write('face_board_inputs.json',[{'name':b.name,'location':list(b.location),'quaternion_wxyz':list(b.rotation_quaternion),'euler':list(b.rotation_euler),'scale':list(b.scale),'properties':custom(b),'constraints':[[c.name,props(c)] for c in b.constraints]} for b in rigs[3].pose.bones])
with bpy.data.libraries.load(str(LIB),link=False) as (src,dst):dst.actions=list(CLIPS)
for name in CLIPS:
    a=bpy.data.actions[name];assert any(slot.identifier=='OBMeshy_Fitted_Rig' and slot.target_id_type=='OBJECT' for slot in a.slots),name
lane=ReactionLane();samples={};clip_rows=[]
for name in CLIPS:
    a=lane.on(name);a_slot=next(slot for slot in a.slots if slot.identifier=='OBMeshy_Fitted_Rig');r.animation_data.action_slot=a_slot
    frames=[];previous={};qmin=1;end=round(a.frame_range[1])
    for f in range(1,end+1):
        s.frame_set(f);bpy.context.view_layer.update();frame={}
        for o in rigs:
            bones={}
            for b in o.pose.bones:
                local=b.parent.matrix.inverted()@b.matrix if b.parent else b.matrix
                loc,q,scale=local.decompose();key=(o.name,b.name)
                if key in previous and q.dot(previous[key])<0:q.negate()
                if key in previous:qmin=min(qmin,q.dot(previous[key]))
                previous[key]=q.copy();bones[b.name]={'world_matrix':rows(o.matrix_world@b.matrix),'armature_matrix':rows(b.matrix),'parent_local_matrix':rows(local),'local_TRS':{'location':list(loc),'quaternion_wxyz':list(q),'scale':list(scale)}}
            frame[o.name]=bones
        frames.append(frame)
    samples[name]=frames
    clip_rows.append({'logical':'YRA_R1_'+name.removeprefix('YRA_R4_'),'authored_Action':name,'slot':a_slot.identifier,'target_id_type':'OBJECT','start':1,'end':end,'fps':24,'duration_seconds':(end-1)/24,'loop':'Loop' in name,'evaluated_local_quaternion_min_adjacent_dot':qmin,'gravity_trajectory':'NONE; bounded authored compression only; no height-ratio rescale'})
    lane.off()
zipped('native_evaluated_all_frames.json.gz',samples)
quarter={name:{str(f):samples[name][f-1] for f in sorted({1,1+round((len(frames)-1)*.25),1+round((len(frames)-1)*.5),len(frames)})} for name,frames in samples.items()}
zipped('native_reference_0_25_50_100_percent.json.gz',quarter)
settings=dict(use_selection=True,object_types={'ARMATURE','EMPTY','MESH'},global_scale=1.0,apply_unit_scale=True,apply_scale_options='FBX_SCALE_ALL',use_space_transform=True,bake_space_transform=False,axis_forward='-Z',axis_up='Y',primary_bone_axis='Y',secondary_bone_axis='X',add_leaf_bones=False,use_armature_deform_only=False,use_mesh_modifiers=False,path_mode='COPY',embed_textures=True,armature_nodetype='NULL')
axis=axis_conversion(to_forward='-Z',to_up='Y').to_4x4()
export_manifest={'exporter':'Blender '+bpy.app.version_string+' io_scene_fbx binary exporter','source_commit':'62f2e6b800e2aac4bda41c5341155c385c0b2f01','settings':{k:sorted(v) if isinstance(v,set) else v for k,v in settings.items()},'native_basis':'Blender Z-up / native source matrices / scene unit1','source_to_FBX_numeric_axis_matrix':rows(axis),'FBX_UnitScaleFactor_cm_per_file_unit':100.0,'FBX_SCALE_ALL_effect':'unit100 is metadata; no manual multiplication of native position or scale; 0.535 appears on original body object exactly once','Animator_root':'FBX file container, not a new Blender object or source reshaping','objects':objects,'rig_bone_counts':{o.name:len(o.data.bones) for o in rigs},'clips':clip_rows,'QA_helpers_exported':False,'source_scale_or_height_ratio_reapplied':False,'procedural_visuals':'UNSUPPORTED automatic conversion; raw geometry/morph/material serialization only; roundtrip visual gate required'}
write('export_manifest.json',export_manifest)
states={o.name:(o.hide_get(),o.hide_viewport,o.select_get()) for o in bpy.data.objects};old_active=bpy.context.view_layer.objects.active;fps=s.render.fps;fps_base=s.render.fps_base
for o in bpy.data.objects:o.select_set(False)
for o in ordered_objects:o.hide_set(False);o.hide_viewport=False;o.select_set(True)
bpy.context.view_layer.objects.active=r
assert set(o.name for o in bpy.context.selected_objects)==set(o.name for o in selected)
bpy.ops.export_scene.fbx(filepath=str(OUT/MODEL),bake_anim=False,**settings)
# Animation has exactly the same original rigs/ancestors, but no mesh geometry.
for o in meshes:o.select_set(False)
s.render.fps=24;s.render.fps_base=1
lane.on(CLIPS[0]);lane.off() # Capture/restore support; force source OFF before strips.
lane.on(CLIPS[0]);r.animation_data.action=None
tracks=[]
for name in CLIPS:
    a=bpy.data.actions[name];track=r.animation_data.nla_tracks.new();track.name=name;strip=track.strips.new(name,1,a)
    strip.action_slot=next(slot for slot in a.slots if slot.identifier=='OBMeshy_Fitted_Rig');strip.frame_start=1;strip.frame_end=a.frame_range[1];strip.action_frame_start=1;strip.action_frame_end=a.frame_range[1];strip.extrapolation='NOTHING';strip.blend_type='REPLACE';tracks.append(track)
bpy.ops.export_scene.fbx(filepath=str(OUT/MOTION),bake_anim=True,bake_anim_use_all_bones=True,bake_anim_use_nla_strips=True,bake_anim_use_all_actions=False,bake_anim_force_startend_keying=True,bake_anim_step=1,bake_anim_simplify_factor=0,**settings)
for track in tracks:r.animation_data.nla_tracks.remove(track)
lane.off();s.render.fps=fps;s.render.fps_base=fps_base
for o in bpy.data.objects:
    hidden,viewport,selection=states[o.name];o.hide_viewport=viewport;o.hide_set(hidden);o.select_set(selection)
bpy.context.view_layer.objects.active=old_active
after=snapshot(original_actions);delta=difference(before,after);write('source_after_export_diff.json',delta)
write('source_before_components.json',before);write('source_after_components.json',after)
assert not delta,delta
assert sha(SOURCE)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
write('export_receipt.json',{'source_OFF_restored':True,'source_component_differences':0,'source_file_immutable':True,'original_Action_curves_preserved':len(original_actions),'new_meshes_or_rigs':0,'six_existing_clips':True,'model':{'file':MODEL,'bytes':(OUT/MODEL).stat().st_size,'sha256':sha(OUT/MODEL)},'animation':{'file':MOTION,'bytes':(OUT/MOTION).stat().st_size,'sha256':sha(OUT/MOTION)},'Unity_PASS':False,'visual_gate':'PENDING roundtrip; unsupported native procedures not silently replaced'})
print('NATIVE_HIERARCHY_EXPORT_COMPLETED',flush=True)
