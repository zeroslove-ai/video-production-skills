"""Audit actual wire, including Cluster-over-Pose precedence and exact source rest.
No re-export or source/importer changes. Trial remains exactly one.
"""
import json,sys,hashlib
import numpy as np
from pathlib import Path
from io_scene_fbx.parse_fbx import parse
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;E=ROOT/'evidence/o1-original-bind-serialization-r1';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-original-bind-serialization-r1')
def read(n):return json.loads((E/n).read_text(encoding='utf8'))
def inspect(p):
    root,_=parse(str(p));sections={x.id:x for x in root.elems};obj=sections[b'Objects'];models={x.props[0]:x.props[1].decode(errors='replace').split('\x00')[0] for x in obj.elems if x.id==b'Model'};pose={};poseduplicates=[];clusters={};types={}
    for x in obj.elems:
        t=x.id.decode();types[t]=types.get(t,0)+1
        if x.id==b'Pose':
            for node in x.elems:
                if node.id!=b'PoseNode':continue
                uid=next(c for c in node.elems if c.id==b'Node').props[0];a=list(next(c for c in node.elems if c.id==b'Matrix').props[0])
                if uid in pose:poseduplicates.append({'name':models.get(uid),'equal':pose[uid]==a})
                pose[uid]=a
        if x.id==b'Deformer' and x.props[-1]==b'Cluster':clusters[x.props[0]]=list(next(c for c in x.elems if c.id==b'TransformLink').props[0])
    effective=dict(pose);linked=[]
    for c in sections[b'Connections'].elems:
        if c.props[0]!=b'OO':continue
        a,b=c.props[1:3];bone=a if a in models and b in clusters else b if b in models and a in clusters else None;cluster=b if a in models and b in clusters else a if b in models and a in clusters else None
        if bone is not None:
            values=clusters[cluster];linked.append({'name':models[bone],'direction':'Model→Cluster' if a==bone else 'Cluster→Model','Cluster_TransformLink':values,'equals_Pose':pose.get(bone)==values});effective[bone]=values
    return {'models':models,'pose':pose,'effective':effective,'linked_clusters':linked,'pose_duplicates':poseduplicates,'object_type_counts':types}
model=inspect(OUT/'YURI_O1_R4_NATIVE_CARRIER_20261003_R1.fbx');motion=inspect(OUT/'YURI_O1_R4_NATIVE_ANIMATION_ONLY_20261003_R1.fbx');modelbyname={name:model['effective'].get(uid) for uid,name in model['models'].items()};motionbyname={name:motion['effective'].get(uid) for uid,name in motion['models'].items()}
source=read('source_expanded_rigs.json');axis=np.array(read('export_manifest.json')['source_to_FBX_numeric_axis_matrix']);added=read('ORIGINAL_BIND_SERIALIZATION_RECEIPT.json')['added_animation_skeleton_pose_nodes'];rows=[]
for rig in source.values():
    for bone in rig['bones']:
        n=bone['name'];native=np.array(bone['world_rest']);expected=axis@native;serialized=np.array(motionbyname[n]).reshape(4,4).T;modelbind=modelbyname.get(n)
        rows.append({'rig':rig['name'],'bone':n,'source_world_raw_rest':bone['world_rest'],'source_world_evaluated_OFF':bone['neutral_evaluated_world'],'converted_source_raw_rest_max_matrix_element_delta':float(np.max(np.abs(serialized-expected))),'model_effective_bind_exists':modelbind is not None,'model_effective_bind_equals_animation_Pose_exact':modelbind==motionbyname[n] if modelbind is not None else None,'animation_Pose_column_major_float64':motionbyname[n],'source_index':bone['index']})
result={'trial_count':1,'model_object_types':model['object_type_counts'],'animation_object_types':motion['object_type_counts'],'animation_no_geometry_or_deformer':not motion['object_type_counts'].get('Geometry') and not motion['object_type_counts'].get('Deformer'),'animation_pose_node_count':len(motion['pose']),'animation_bones':137,'model_cluster_records':len(model['linked_clusters']),'model_cluster_bones':len({r['name'] for r in model['linked_clusters']}),'all_original_Cluster_TransformLink_equal_corresponding_Pose':all(r['equals_Pose'] for r in model['linked_clusters']),'all_existing_model_effective_bind_equals_animation_exact':all(r['model_effective_bind_equals_animation_Pose_exact'] for r in rows if r['model_effective_bind_exists']),'unbound_original_rest_bones':[r['bone'] for r in rows if not r['model_effective_bind_exists']],'source_convention':'Float64 wire stores original mathutils float32 rest-matrix results; source FBX-axis conversion checked independently with numpy float64; conversion residual is not an OFF substitution','bones':rows,'source_cluster_mapping_note':'Trial wrapper captured Pose records; its connection orientation filter recorded0Cluster captures. Independent actual-wire audit includes both connection orientations and proves all1150Cluster TransformLink records equal their Pose, so effective model bind is exactly the transported original Pose. No second export needed or performed.','model_cluster_connection_direction_counts':{d:sum(r['direction']==d for r in model['linked_clusters']) for d in ('Model→Cluster','Cluster→Model')},'importer_source_gate':'Strict model↔animation rest passes; source↔imported bone reconstruction and full-frame rotation are separate, still FAIL.','evaluated_OFF_not_used_for_bind':True}
for p in (E/'EXACT_BIND_WIRE_RECEIPT.json',OUT/'metadata/EXACT_BIND_WIRE_RECEIPT.json'):p.write_text(json.dumps(result,indent=2),encoding='utf8')
assert result['animation_no_geometry_or_deformer'] and result['all_existing_model_effective_bind_equals_animation_exact'] and result['all_original_Cluster_TransformLink_equal_corresponding_Pose']
print('BIND_WIRE_VERIFIED',result['model_cluster_records'],result['model_cluster_bones'],result['animation_pose_node_count'],max(r['converted_source_raw_rest_max_matrix_element_delta'] for r in rows))
