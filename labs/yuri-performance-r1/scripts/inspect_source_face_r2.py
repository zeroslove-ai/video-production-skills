"""Read-only native key deltas, gaze node graph and missing texture inventory."""
from pathlib import Path
import bpy,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path(r'C:\Users\JAEWAN\Downloads\Character_Master_R2_20261002.blend')
before=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
h=bpy.data.objects['Character_Body_Head'];keys=h.data.shape_keys.key_blocks
ref=keys['Basis'];deltas={}
for name in ('JawOpen','MouthWide','LipPucker','Smile.L','Smile.R','BrowRaise.L','CheekLift.L'):
    ds=[(v.co-b.co).length for v,b in zip(keys[name].data,ref.data)]
    weighted=sum((b.co*x for b,x in zip(ref.data,ds)),ref.data[0].co*0)/sum(ds)
    deltas[name]={'max_delta_m':max(ds),'weighted_centroid':list(weighted),'moved_vertices_1um':sum(x>1e-6 for x in ds),'slider_min':keys[name].slider_min,'slider_max':keys[name].slider_max}
nodes=[]
for modifier in h.modifiers:
    if modifier.type=='NODES' and modifier.node_group:
        nodes.append({'modifier':modifier.name,'tree':modifier.node_group.name,'nodes':[{'name':n.name,'type':n.bl_idname,'operation':getattr(n,'operation',None),'inputs':{i.name:str(i.default_value) for i in n.inputs if hasattr(i,'default_value')}} for n in modifier.node_group.nodes]})
missing=[{'name':im.name,'path':bpy.path.abspath(im.filepath),'file':Path(im.filepath).name} for im in bpy.data.images if im.source=='FILE' and not im.packed_file and im.filepath and not Path(bpy.path.abspath(im.filepath)).exists()]
data={'source_sha256':before,'key_deltas':deltas,'gaze_properties':{k:str(v) for k,v in h.items() if 'Gaze' in k},'geometry_nodes':nodes,'missing_external_images':missing,'source_unchanged':before==hashlib.sha256(SOURCE.read_bytes()).hexdigest()}
p=ROOT/'evidence/source-face-r2/native_inspection.json';p.write_text(json.dumps(data,indent=2));print(json.dumps({'key_deltas':deltas,'missing':missing}))
