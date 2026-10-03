"""Separate unchanged exporter input, wire defaults/binds and importer fallback."""
import sys,json,hashlib
from pathlib import Path
from io_scene_fbx.parse_fbx import parse
ROOT=Path(__file__).resolve().parent.parent;E=ROOT/'evidence/o1-source-fidelity-recovery-r1';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-source-fidelity-recovery-r1');OLD=OUT.parent/'o1-native-unity-probe-r1'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def wire(p):
    root,version=parse(str(p));objects=next(x for x in root.elems if x.id==b'Objects');counts={};pose=[];clusters=[]
    for x in objects.elems:
        typ=x.id.decode();counts[typ]=counts.get(typ,0)+1
        if x.id==b'Pose':
            pose.append({'id':x.props[0],'nodes':[{'node':n.elems[0].props[0],'matrix':list(n.elems[1].props[0])} for n in x.elems if n.id==b'PoseNode']})
        if x.id==b'Deformer' and x.props[-1]==b'Cluster':
            clusters.append({'name':x.props[1].decode(errors='replace'),'matrices':{e.id.decode():list(e.props[0]) for e in x.elems if e.id in (b'Transform',b'TransformLink',b'TransformAssociateModel')}})
    return {'version':version,'object_type_counts':counts,'bind_pose_nodes':pose,'cluster_matrix_records':clusters}
original=read(OLD/'metadata/fbx_wire_comparison.json');corrected=read(E/'static-correction/fbx_wire_comparison.json')
def effective(report):
    out=[];defaults={'Lcl Translation':[0,0,0],'Lcl Rotation':[0,0,0],'Lcl Scaling':[1,1,1]}
    for row in report['shared_object_defaults']:
        for prop,diff in row['different_properties'].items():
            a=diff['model'];b=diff['animation']
            if prop in defaults:
                a=a if a is not None else defaults[prop];b=b if b is not None else defaults[prop]
                out.append({'name':row['name'],'property':prop,'max_numeric_component_delta':max(abs(x-y) for x,y in zip(a,b)),'model_omitted_as_template_default':diff['model'] is None})
    return {'mismatched_raw_objects':sum(bool(r['different_properties']) for r in report['shared_object_defaults']),'effective_TRS_differences':out,'max_effective_TRS_component_delta':max([r['max_numeric_component_delta'] for r in out] or [0])}
data={}
for name,path in [('frozen_model',OLD/'YURI_O1_R4_NATIVE_CARRIER_20261003_R1.fbx'),('frozen_animation',OLD/'YURI_O1_R4_NATIVE_ANIMATION_ONLY_20261003_R1.fbx'),('corrected_model',OUT/'static-correction/YURI_O1_R4_NATIVE_CARRIER_20261003_R1.fbx'),('corrected_animation',OUT/'static-correction/YURI_O1_R4_NATIVE_ANIMATION_ONLY_20261003_R1.fbx')]:data[name]=wire(path)
directory=Path(r'C:/Program Files/Blender Foundation/Blender 5.2/5.2/scripts/addons_core/io_scene_fbx')
result={'exporter_input':'Native source immutable SHA/component diff0 in both trials; same evaluated OFF initial state. Nonidentity helper/constraint OFF matrices are distinct from raw bone rest; neither was reset. Action sampling unchanged.','serializer_original':'fbx_data_object_elements calls fbx_object_tx(rest=False), evaluated current pose. fbx_data_from_scene runs fbx_animations before Model serialization; NLA evaluation and restored current frame can change evaluated pose float defaults. Bone skin BindPose/Cluster separately use rest=True.','serializer_correction':'Replay captured original OFF Model TRS only during animation Model element writing. No source input/rest or curve edits; one bounded candidate.','original_effective_defaults':effective(original),'corrected_effective_defaults':effective(corrected),'wire_bind_evidence':data,'importer_mechanism':'import_fbx.py sets global bind matrices from Pose (line3477), overwrites from Cluster TransformLink (3505), then make_bind_pose_local(3541). Without Pose/Cluster it falls back to Model matrix (2575-2589). Model and animation have different bind evidence even with matched evaluated OFF defaults; float decomposition/recomposition + normalized bone construction adds a separate stage.','causal_boundary':'Confirmed differing bind/default pathways by actual wire and importer code; no claim that every coefficient is solely numeric precision. Correction did not pass strict rest or rotation. Next narrow experiment would transport original skeleton bind/rest matrices consistently into meshless motion serialization, not rewrite consumer rest. Not implemented in this bounded packet.','modules':[{'name':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [directory/'fbx_utils.py',directory/'export_fbx_bin.py',directory/'import_fbx.py']],'strict_thresholds_unchanged':{'rest_element':1e-5,'world_position_m':1e-4,'world_rotation_deg':.001}}
for p in (E/'STATIC_CAUSAL_SEPARATION.json',OUT/'metadata/STATIC_CAUSAL_SEPARATION.json'):p.write_text(json.dumps(result,indent=2),encoding='utf8')
print('STATIC_CAUSAL_ANALYSIS',result['original_effective_defaults']['max_effective_TRS_component_delta'],result['corrected_effective_defaults']['max_effective_TRS_component_delta'],{k:(v['object_type_counts'].get('Pose',0),len(v['cluster_matrix_records'])) for k,v in data.items()})
