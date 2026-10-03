"""Compare serialized FBX model defaults, connections, axes and units directly.
This distinguishes importer float reconstruction from a mismatched FBX pair.
"""
import sys,json
from pathlib import Path
from io_scene_fbx.parse_fbx import parse
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;E=ROOT/'evidence/o1-native-unity-probe-r1'
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-native-unity-probe-r1')
def decode(v):
    if isinstance(v,bytes):return v.decode('utf8',errors='replace')
    if hasattr(v,'tolist'):return v.tolist()
    if isinstance(v,(list,tuple)):return [decode(x) for x in v]
    return v
def properties(e):
    block=next((x for x in e.elems if x.id==b'Properties70'),None)
    return {decode(x.props[0]):decode(x.props[4:]) for x in block.elems} if block else {}
def inspect(p):
    root,version=parse(str(p));sections={x.id:x for x in root.elems};models={};ids={}
    for e in sections[b'Objects'].elems:
        if e.id!=b'Model':continue
        name=decode(e.props[1]).split('\x00')[0];ids[e.props[0]]=name;models[name]={'type':decode(e.props[2]),'properties':properties(e),'parent':None}
    for e in sections[b'Connections'].elems:
        if e.props[0]==b'OO' and e.props[1] in ids and (e.props[2] in ids or e.props[2]==0):
            models[ids[e.props[1]]]['parent']=ids.get(e.props[2],str(e.props[2]))
    return {'version':version,'global':properties(sections[b'GlobalSettings']),'models':models}
model=inspect(OUT/'YURI_O1_R4_NATIVE_CARRIER_20261003_R1.fbx');motion=inspect(OUT/'YURI_O1_R4_NATIVE_ANIMATION_ONLY_20261003_R1.fbx')
rows=[]
for n,b in motion['models'].items():
    a=model['models'].get(n);diff={}
    if a:
        for k in set(a['properties'])|set(b['properties']):
            av=a['properties'].get(k);bv=b['properties'].get(k)
            if av!=bv:diff[k]={'model':av,'animation':bv}
    rows.append({'name':n,'present_in_both':a is not None,'parents_equal':a and a['parent']==b['parent'],'different_properties':diff})
result={'model_global_settings':model['global'],'animation_global_settings':motion['global'],'globals_identical':model['global']==motion['global'],'shared_object_defaults':rows,'exact_shared_defaults_PASS':all(r['present_in_both'] and r['parents_equal'] and not r['different_properties'] for r in rows),'importer_rest_gate':'Do not waive the 1e-5 imported local-rest threshold; direct defaults and imported rest are separate gates.'}
for p in (E/'fbx_wire_comparison.json',OUT/'metadata/fbx_wire_comparison.json'):p.write_text(json.dumps(result,indent=2),encoding='utf8')
print('WIRE',result['globals_identical'],result['exact_shared_defaults_PASS'],'objects',len(rows),'different_properties',sum(bool(r['different_properties']) for r in rows),'parent_mismatches',sum(not r['parents_equal'] for r in rows),flush=True)
