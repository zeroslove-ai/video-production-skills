"""Include material-owned ShaderNodeTree drivers, beyond data.node_groups."""
import bpy,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import props,snapshot,difference,val
ROOT=HERE.parent;E=ROOT/'evidence/o1-source-fidelity-recovery-r1';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-source-fidelity-recovery-r1')
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'),use_scripts=False);actions=[a.name for a in bpy.data.actions];before=snapshot(actions)
owners=[(m.name,m.node_tree) for m in bpy.data.materials if m.node_tree and m.node_tree.animation_data and m.node_tree.animation_data.drivers];drivers=[]
for name,t in owners:
    drivers.append({'owner_path':'Material/'+name+'/node_tree','drivers':[{'path':f.data_path,'index':f.array_index,'mute':f.mute,'valid':f.driver.is_valid,'expression':f.driver.expression,'variables':[{'name':v.name,'type':v.type,'targets':[props(x) for x in v.targets]} for v in f.driver.variables],'curve_modifiers':[props(x) for x in f.modifiers]} for f in t.animation_data.drivers]})
head=bpy.data.objects['Character_Body_Head'];keys=head.data.shape_keys;groups={'blink':['Blink.L','Blink.R'],'smile':['Smile.L','Smile.R'],'jaw':['JawOpen'],'brow':['BrowRaise.L','BrowRaise.R']};values={k:keys.key_blocks[k].value for g in groups.values() for k in g};samples=[]
def output():
    result=[]
    for name,t in owners:
        for f in t.animation_data.drivers:
            v=t.path_resolve(f.data_path);v=v[f.array_index] if hasattr(v,'__len__') and not isinstance(v,str) else v
            result.append({'owner_path':'Material/'+name+'/node_tree','path':f.data_path,'index':f.array_index,'value':val(v),'valid':f.driver.is_valid,'muted':f.mute})
    return result
for group,ks in groups.items():
    for amplitude in (0,1,0):
        for k,v in values.items():keys.key_blocks[k].value=v
        for k in ks:keys.key_blocks[k].value=amplitude
        keys.update_tag();head.update_tag();bpy.context.scene.frame_set(1);bpy.context.view_layer.update();samples.append({'manual_input':group,'amplitude':amplitude,'material_owned_driver_outputs':output()})
for k,v in values.items():keys.key_blocks[k].value=v
keys.update_tag();head.update_tag();bpy.context.scene.frame_set(1);bpy.context.view_layer.update();delta=difference(before,snapshot(actions));assert not delta,delta
receipt={'source_component_diff':delta,'material_shader_node_tree_owners':drivers,'manual_input_output_OFF_ON_OFF':samples,'additional_driver_count':sum(len(r['drivers']) for r in drivers),'note':'Material node trees are not in bpy.data.node_groups. Previous872 counted object/Key/GN/material IDs; this supplement completes shader-owner coverage without duplicate graph data.'}
for p in (E/'MATERIAL_SHADER_DRIVER_RECEIPT.json',OUT/'metadata/MATERIAL_SHADER_DRIVER_RECEIPT.json'):p.write_text(json.dumps(receipt,indent=2),encoding='utf8')
print('SHADER_DRIVER_SUPPLEMENT',receipt['additional_driver_count'])
