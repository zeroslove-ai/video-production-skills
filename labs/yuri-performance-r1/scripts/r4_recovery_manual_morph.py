"""Temporary existing morph values only; muted bridges/definitions stay unchanged.
3-second1x control diagnostic is not new expression design or performance polish.
"""
import bpy,sys,json,hashlib,math
import numpy as np
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference,props
ROOT=HERE.parent;E=ROOT/'evidence/o1-source-fidelity-recovery-r1';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-source-fidelity-recovery-r1')
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'),use_scripts=False);s=bpy.context.scene;names=[a.name for a in bpy.data.actions];before=snapshot(names)
head=bpy.data.objects['Character_Body_Head'];keys=head.data.shape_keys;groups={'blink':['Blink.L','Blink.R'],'smile':['Smile.L','Smile.R'],'jaw':['JawOpen'],'brow':['BrowRaise.L','BrowRaise.R']};saved={k:keys.key_blocks[k].value for group in groups.values() for k in group}
meshes=[bpy.data.objects[r['renderer']] for r in json.loads((E/'mesh_slot_UV_attributes_shape_deltas.json').read_text(encoding='utf8'))]
def setinput(group,value):
    for k,v in saved.items():keys.key_blocks[k].value=v
    for k in groups[group]:keys.key_blocks[k].value=value
    keys.update_tag();head.update_tag();s.frame_set(1);bpy.context.view_layer.update()
def evaluate():
    deps=bpy.context.evaluated_depsgraph_get();result={}
    for o in meshes:
        ev=o.evaluated_get(deps);m=ev.to_mesh();p=np.empty((len(m.vertices),3),np.float32);m.vertices.foreach_get('co',p.reshape(-1));mw=np.array(ev.matrix_world);result[o.name]=(p@mw[:3,:3].T+mw[:3,3]).astype(np.float32);ev.to_mesh_clear()
    return result
neutral=evaluate();rows=[];arrays={}
for group in groups:
    for value in (.5,1,0):
        setinput(group,value);actual=evaluate();metric=[]
        for name,p in actual.items():
            d=np.linalg.norm(p-neutral[name],axis=1);metric.append({'mesh':name,'max_world_vertex_delta_m':float(d.max()),'RMS_m':float(np.sqrt(np.mean(d*d))),'changed_vertex_count':int(np.count_nonzero(d>1e-8))})
            if value==1:arrays[group+'_'+name]=p
        material_outputs={m.name:{n.name:[{'name':socket.name,'value':list(socket.default_value) if hasattr(getattr(socket,'default_value',None),'__len__') else getattr(socket,'default_value',None)} for socket in n.inputs if hasattr(socket,'default_value') and socket.type in ('VALUE','RGBA','VECTOR')] for n in m.node_tree.nodes if n.type in ('MIX_RGB','MATH')} for m in bpy.data.materials if m.node_tree and any(n.type in ('MIX_RGB','MATH') for n in m.node_tree.nodes)}
        rows.append({'group':group,'input_keys':groups[group],'input_value':value,'geometry':metric,'head_values':{k.name:k.value for k in keys.key_blocks},'material_driver_socket_outputs':material_outputs})
path=OUT/'data/manual_morph_peak_geometry.npz';np.savez_compressed(path,**arrays)
save=(s.render.engine,s.cycles.device,s.cycles.samples,s.cycles.seed,s.cycles.use_denoising,s.render.threads_mode,s.render.threads,s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage,s.render.fps,s.render.fps_base,s.render.filepath,s.render.image_settings.file_format)
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=8;s.cycles.seed=0;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=384;s.render.resolution_y=368;s.render.resolution_percentage=100;s.render.fps=24;s.render.fps_base=1;s.render.image_settings.file_format='PNG'
folder=OUT/'manual_morph_proof';folder.mkdir(exist_ok=True)
for index,group in enumerate(('blink','smile','jaw')):
    for tick in range(24):
        value=1-abs(2*tick/23-1);setinput(group,value);s.render.filepath=str(folder/f'frame_{index*24+tick:04d}.png');bpy.ops.render.render(write_still=True)
    setinput(group,0)
for k,v in saved.items():keys.key_blocks[k].value=v
keys.update_tag();head.update_tag();s.frame_set(1);bpy.context.view_layer.update()
(s.render.engine,s.cycles.device,s.cycles.samples,s.cycles.seed,s.cycles.use_denoising,s.render.threads_mode,s.render.threads,s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage,s.render.fps,s.render.fps_base,s.render.filepath,s.render.image_settings.file_format)=save
after=snapshot(names);delta=difference(before,after);assert not delta,delta
receipt={'method':'Existing direct shape-key values temporary0→.5→1→0 on immutable original head;13 muted source bridge Fcurves never unmuted; default values restored; no definition/data/driver/material/rig save','source_component_diff':delta,'cases':rows,'peak_arrays':{'path':path.relative_to(OUT).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()},'proof':'72frames24fps3s source camera384x368, blink then smile then jaw triangular scalar diagnostic, not authored performance; brow peak reference data only','ownership':'Body-only ReactionLane leaves face/gaze alone. Source contains muted board13; no authored mute rationale/owner declaration found in relevant appearance adapter/build/report docs. Manual-morph mode works only if measured downstream changes; board mode currently muted; PM must choose explicit runtime ownership, no automatic unmute.','F2':'Not certified by this diagnostic; requires character timing/hands/secondary/multicamera review.'}
for p in (E/'MANUAL_MORPH_RECEIPT.json',OUT/'metadata/MANUAL_MORPH_RECEIPT.json'):p.write_text(json.dumps(receipt,indent=2),encoding='utf8')
print('MANUAL_MORPH_DIAGNOSTIC_COMPLETE')
