import bpy,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import props,custom,anim
ROOT=HERE.parent;W=ROOT/'local/o1-source-fidelity-recovery-r1';W.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'),use_scripts=False)
board=bpy.data.objects['AVATAR_FaceBoard']
v={'board':[{ 'name':b.name,'custom':custom(b),'constraints':[[c.name,props(c)] for c in b.constraints],'location':list(b.location),'rotation':list(b.rotation_euler)} for b in board.pose.bones],'node_groups':[{ 'name':g.name,'nodes':[(n.name,n.bl_idname) for n in g.nodes],'interface':[(i.name,props(i)) for i in g.interface.items_tree]} for g in bpy.data.node_groups],'materials':[{'name':m.name,'nodes':[(n.name,n.bl_idname) for n in m.node_tree.nodes] if m.node_tree else []} for m in bpy.data.materials],'modifiers':{o.name:[(m.name,m.type,props(m),custom(m)) for m in o.modifiers] for o in bpy.data.objects if o.type=='MESH'},'drivers':{x.name:anim(x) for group in (bpy.data.objects,bpy.data.shape_keys,bpy.data.node_groups,bpy.data.materials) for x in group if x.animation_data and x.animation_data.drivers}}
(W/'inspect.json').write_text(json.dumps(v,indent=2),encoding='utf8')
print('INSPECT_READY')
