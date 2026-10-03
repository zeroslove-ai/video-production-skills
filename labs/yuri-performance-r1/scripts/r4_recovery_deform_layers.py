"""CPU staged object-copy stack ablation. Shared source mesh is read-only.
No source modifier, rig, rest, skin weights or Action curve is changed.
"""
import bpy,sys,json,hashlib
import numpy as np
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference,props,tree,custom
from r4_appearance_adapter import ReactionLane
ROOT=HERE.parent;E=ROOT/'evidence/o1-source-fidelity-recovery-r1';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-source-fidelity-recovery-r1')
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'),use_scripts=False);s=bpy.context.scene;names=[a.name for a in bpy.data.actions];before=snapshot(names)
view={'camera':{'name':s.camera.name,'object_world':[list(r) for r in s.camera.matrix_world],'settings':props(s.camera.data)},'lights':[{'name':o.name,'matrix_world':[list(r) for r in o.matrix_world],'settings':props(o.data)} for o in bpy.data.objects if o.type=='LIGHT'],'world':{'settings':props(s.world),'tree':tree(s.world.node_tree)},'color_management':{'view':props(s.view_settings),'display':props(s.display_settings),'sequencer':props(s.sequencer_colorspace_settings)},'render':props(s.render),'neutral':{'frame':s.frame_current,'head_properties':custom(bpy.data.objects['Character_Body_Head']),'rig_actions':{o.name:o.animation_data.action.name if o.animation_data and o.animation_data.action else None for o in bpy.data.objects if o.type=='ARMATURE'}}}
for p in (E/'neutral_camera_light_color_driver_state.json',OUT/'metadata/neutral_camera_light_color_driver_state.json'):p.write_text(json.dumps(view,indent=2),encoding='utf8')
with bpy.data.libraries.load(str(OUT.parent/'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'),link=False) as (src,dst):dst.actions=['YRA_R4_Struggle_Strong_Loop']
body=bpy.data.objects['Meshy_Body_NeutralCovered'];clone=body.copy();clone.name='R4_DIAGNOSTIC_DEFORM_STACK';s.collection.objects.link(clone);clone.hide_render=True;clone.hide_viewport=False;clone.hide_set(False)
lane=ReactionLane();lane.on('YRA_R4_Struggle_Strong_Loop');rows=[];arrays={}
for frame in (1,49):
    s.frame_set(frame);bpy.context.view_layer.update();states={m.name:(m.show_viewport,m.use_deform_preserve_volume if m.type=='ARMATURE' else None) for m in clone.modifiers}
    for stage in ('native_full','DQ_maskedLBS_no_surface','DQ_only','LBS_only'):
        for i,m in enumerate(clone.modifiers):
            m.show_viewport=states[m.name][0]
            if m.type=='ARMATURE':m.use_deform_preserve_volume=states[m.name][1]
            if stage!='native_full' and m.type in ('SMOOTH','CORRECTIVE_SMOOTH'):m.show_viewport=False
            if stage in ('DQ_only','LBS_only') and m.type=='ARMATURE' and i!=0:m.show_viewport=False
            if stage=='LBS_only' and m.type=='ARMATURE' and i==0:m.use_deform_preserve_volume=False
        clone.update_tag();bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();ev=clone.evaluated_get(deps);mesh=ev.to_mesh();p=np.empty((len(mesh.vertices),3),np.float32);mesh.vertices.foreach_get('co',p.reshape(-1));mw=np.array(ev.matrix_world);world=p@mw[:3,:3].T+mw[:3,3];key=f'{stage}_frame{frame}';arrays[key]=world;ev.to_mesh_clear()
        rows.append({'frame':frame,'stage':stage,'array':key,'vertices':len(p),'modifier_settings':[[m.name,props(m)] for m in clone.modifiers]})
    for m in clone.modifiers:
        m.show_viewport=states[m.name][0]
        if m.type=='ARMATURE':m.use_deform_preserve_volume=states[m.name][1]
def metric(a,b):
    d=np.linalg.norm(a-b,axis=1);return {'max_m':float(d.max()),'RMS_m':float(np.sqrt(np.mean(d*d))),'p95_m':float(np.percentile(d,95)),'worst_vertex':int(d.argmax())}
metrics=[]
for frame in (1,49):
    for a,b in [('native_full','DQ_maskedLBS_no_surface'),('DQ_maskedLBS_no_surface','DQ_only'),('DQ_only','LBS_only')]:metrics.append({'frame':frame,'layer_difference':a+' versus '+b,**metric(arrays[f'{a}_frame{frame}'],arrays[f'{b}_frame{frame}'])})
file=OUT/'data/Strong_1_49_deformation_layer_ablation.npz';np.savez_compressed(file,**arrays)
lane.off();bpy.data.objects.remove(clone,do_unlink=True);after=snapshot(names);delta=difference(before,after);assert not delta,delta
receipt={'scope':'Original body mesh read-only shared by temporary disposable object-copy; source modifiers unchanged, source rig/Action untouched; copy removed','source_component_diff':delta,'source_saved':False,'array_file':file.relative_to(OUT).as_posix(),'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'arrays':rows,'layer_metrics':metrics,'caveat':'Layer ablations show actual Blender stack responses; do not promote LBS-only or retune canonical masks. Full native procedure remains authority.'}
for p in (E/'DEFORMATION_LAYER_RECEIPT.json',OUT/'metadata/DEFORMATION_LAYER_RECEIPT.json'):p.write_text(json.dumps(receipt,indent=2),encoding='utf8')
print('DEFORMATION_LAYERS_COMPLETE',metrics)
