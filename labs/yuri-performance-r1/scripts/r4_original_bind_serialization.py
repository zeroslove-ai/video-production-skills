"""ONE source-preserving serializer trial: meshless original skeleton BindPose.
No source rest/geometry/driver/action edits; raw bind and OFF defaults separate.
"""
import bpy,sys,json,hashlib
from pathlib import Path
from io_scene_fbx import export_fbx_bin as fbx
from io_scene_fbx.fbx_utils import ObjectWrapper
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-original-bind-serialization-r1')
E=ROOT/'evidence/o1-original-bind-serialization-r1';OUT.mkdir(parents=True,exist_ok=True);E.mkdir(parents=True,exist_ok=True)
def write(n,v):
    for p in (E/n,OUT/'metadata'/n):p.parent.mkdir(exist_ok=True,parents=True);p.write_text(json.dumps(v,indent=2),encoding='utf8')
cache={};phase=None;rawbind={};clusterbind={};names={};added=[]
real_tx=ObjectWrapper.fbx_object_tx;real_models=fbx.fbx_data_object_elements;real_objects=fbx.fbx_objects_elements;real_scene=fbx.fbx_data_from_scene
def tx(self,scene_data,*args,**kwargs):
    if phase=='replay':
        assert self.key in cache
        return tuple(v.copy() if hasattr(v,'copy') else v for v in cache[self.key])
    result=real_tx(self,scene_data,*args,**kwargs)
    if phase=='capture':cache[self.key]=tuple(v.copy() if hasattr(v,'copy') else v for v in result)
    return result
def models(root,obj,scene_data):
    global phase
    phase='replay' if scene_data.settings.bake_anim else 'capture'
    try:return real_models(root,obj,scene_data)
    finally:phase=None
def scene(*args,**kwargs):
    result=real_scene(*args,**kwargs)
    if result.settings.bake_anim:
        assert not result.data_meshes,'Meshless trial unexpectedly has meshes'
        assert b'BindPose' not in result.templates
        result.templates[b'BindPose']=fbx.fbx_template_def_pose(result.scene,result.settings,nbr_users=1)
        result=result._replace(templates_users=result.templates_users+1)
    return result
def objects(root,scene_data):
    result=real_objects(root,scene_data);block=next(x for x in root.elems if x.id==b'Objects')
    wrappers=[o for o in scene_data.objects if o.is_bone or (o.is_object and o.type in ('ARMATURE','EMPTY'))]
    for o in wrappers:names[o.fbx_uuid]=o.name
    if not scene_data.settings.bake_anim:
        for element in block.elems:
            if element.id==b'Pose':
                for node in element.elems:
                    if node.id!=b'PoseNode':continue
                    uid=next(x for x in node.elems if x.id==b'Node').props[0]
                    rawbind[uid]=list(next(x for x in node.elems if x.id==b'Matrix').props[0])
        clusters={x.props[0]:x for x in block.elems if x.id==b'Deformer' and x.props[-1]==b'Cluster'}
        # Importer precedence: each bone->Cluster OO relation overrides its Pose.
        for connection in scene_data.connections:
            kind,child,parent,*rest=connection
            if kind==b'OO' and child in names and parent in clusters:
                element=clusters[parent];matrix=next(x for x in element.elems if x.id==b'TransformLink')
                values=list(matrix.props[0])
                if child in clusterbind:assert clusterbind[child]==values,'Conflicting original source cluster bind matrices'
                clusterbind[child]=values
        return result
    assert sum(o.is_bone for o in wrappers)==137
    pose=fbx.elem_data_single_int64(block,b'Pose',fbx.get_fbx_uuid_from_key('YURI_R4_ORIGINAL_SKELETON_BIND_R1'))
    pose.add_string(fbx.fbx_name_class(b'YURI_R4_ORIGINAL_SKELETON_BIND_R1',b'Pose'));pose.add_string(b'BindPose')
    fbx.elem_data_single_string(pose,b'Type',b'BindPose');fbx.elem_data_single_int32(pose,b'Version',fbx.FBX_POSE_BIND_VERSION);fbx.elem_data_single_int32(pose,b'NbPoseNodes',len(wrappers))
    for o in wrappers:
        if o.fbx_uuid in clusterbind:values=clusterbind[o.fbx_uuid];provenance='original model Cluster.TransformLink raw rest'
        elif o.fbx_uuid in rawbind:values=rawbind[o.fbx_uuid];provenance='original model Pose.Matrix raw rest'
        else:values=list(fbx.matrix4_to_array(o.fbx_object_matrix(scene_data,rest=True,global_space=True)));provenance='unchanged source rest=True global getter (unbound board/ancestry)'
        node=fbx.elem_empty(pose,b'PoseNode');fbx.elem_data_single_int64(node,b'Node',o.fbx_uuid);fbx.elem_data_single_float64_array(node,b'Matrix',values)
        added.append({'name':o.name,'uuid':o.fbx_uuid,'bone':o.is_bone,'matrix_column_major_float64':values,'provenance':provenance})
    return result
ObjectWrapper.fbx_object_tx=tx;fbx.fbx_data_object_elements=models;fbx.fbx_objects_elements=objects;fbx.fbx_data_from_scene=scene
original=HERE/'r4_o1_native_probe_export.py';code=original.read_text(encoding='utf8').replace("E=ROOT/'evidence/o1-native-unity-probe-r1'","E=ROOT/'evidence/o1-original-bind-serialization-r1'").replace('outputs/o1-native-unity-probe-r1','outputs/o1-original-bind-serialization-r1')
code=code.replace("LIB=OUT.parent/'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'","LIB=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend')")
code=code.replace("source_commit':'62f2e6b800e2aac4bda41c5341155c385c0b2f01'","source_commit':'ab1409f33e949e053b8abc84ec6aaaef6792d0d4'")
try:exec(compile(code,str(original),'exec'),{'__file__':str(original),'__name__':'__main__'})
finally:ObjectWrapper.fbx_object_tx=real_tx;fbx.fbx_data_object_elements=real_models;fbx.fbx_objects_elements=real_objects;fbx.fbx_data_from_scene=real_scene
write('ORIGINAL_BIND_SERIALIZATION_RECEIPT.json',{'trial_count':1,'original_OFF_Model_defaults_captured':len(cache),'original_model_cluster_bones':len(clusterbind),'original_model_pose_nodes':len(rawbind),'added_animation_skeleton_pose_nodes':added,'no_mesh_or_cluster_in_animation':True,'source_rest_changed':False,'bind_policy':'Raw original model bind, never evaluated OFF; missing unbound board rest from source rest=True','exporter_module_sha256':hashlib.sha256(Path(fbx.__file__).read_bytes()).hexdigest()})
for script in ('r4_o1_native_probe_roundtrip.py','r4_o1_native_probe_wire.py','r4_o1_native_probe_matrix_analysis.py'):
    p=HERE/script;code=p.read_text(encoding='utf8').replace("E=ROOT/'evidence/o1-native-unity-probe-r1'","E=ROOT/'evidence/o1-original-bind-serialization-r1'").replace('outputs/o1-native-unity-probe-r1','outputs/o1-original-bind-serialization-r1')
    exec(compile(code,str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})
print('ORIGINAL_BIND_TRIAL_COMPLETE')
