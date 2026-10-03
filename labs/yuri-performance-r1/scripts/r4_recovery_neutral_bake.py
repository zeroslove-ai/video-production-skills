"""CPU-derived neutral references; copy materials in disposable memory only.
EXR scene-linear Base Color/Alpha inputs and tangent normal. These are diagnostics
for frozen neutral state, not replacement canonical textures or dynamic shaders.
"""
import bpy,sys,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference
ROOT=HERE.parent;E=ROOT/'evidence/o1-source-fidelity-recovery-r1';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-source-fidelity-recovery-r1')
SOURCE=ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):
    for p in (E/n,OUT/'metadata'/n):p.write_text(json.dumps(v,indent=2),encoding='utf8')
bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False);s=bpy.context.scene
before=snapshot([a.name for a in bpy.data.actions]);save=(s.render.engine,s.cycles.device,s.cycles.samples,s.render.threads_mode,s.render.threads,s.render.bake.margin,s.render.bake.use_clear,s.render.bake.use_selected_to_active,s.render.bake.normal_space,s.render.image_settings.file_format,s.render.image_settings.color_depth,s.render.image_settings.color_mode)
states={o.name:(o.hide_get(),o.hide_viewport,o.select_get()) for o in bpy.data.objects};active=bpy.context.view_layer.objects.active
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=1;s.render.threads_mode='FIXED';s.render.threads=4;s.render.bake.margin=2;s.render.bake.use_clear=True;s.render.bake.use_selected_to_active=False;s.render.bake.normal_space='TANGENT'
s.render.image_settings.file_format='OPEN_EXR';s.render.image_settings.color_depth='32';s.render.image_settings.color_mode='RGBA'
references=[]
for name in ('Character_Body_Head','Globe.L','Globe.R','Meshy_Body_NeutralCovered','Hair_Replacement_R4'):
    o=bpy.data.objects[name];original=[slot.material for slot in o.material_slots]
    if not o.data.uv_layers:continue
    for channel in ('Base Color','Alpha','Tangent Normal'):
        image=bpy.data.images.new('R4_DERIVED_REFERENCE',width=512,height=512,alpha=True,float_buffer=True);image.colorspace_settings.name='Non-Color';copies=[]
        for i,mat in enumerate(original):
            copy=mat.copy();copies.append(copy);o.material_slots[i].material=copy;t=copy.node_tree
            principled=[n for n in t.nodes if n.type=='BSDF_PRINCIPLED'];assert len(principled)==1,(mat.name,len(principled))
            if channel!='Tangent Normal':
                socket=principled[0].inputs[channel];emission=t.nodes.new('ShaderNodeEmission');emission.inputs['Strength'].default_value=1
                if socket.is_linked:t.links.new(socket.links[0].from_socket,emission.inputs['Color'])
                else:
                    value=socket.default_value;emission.inputs['Color'].default_value=tuple(value) if hasattr(value,'__len__') else (value,value,value,1)
                output=next(n for n in t.nodes if n.type=='OUTPUT_MATERIAL' and n.is_active_output)
                for link in list(output.inputs['Surface'].links):t.links.remove(link)
                t.links.new(emission.outputs['Emission'],output.inputs['Surface'])
            target=t.nodes.new('ShaderNodeTexImage');target.image=image;t.nodes.active=target;target.select=True
        for obj in bpy.data.objects:obj.select_set(False)
        o.hide_set(False);o.hide_viewport=False;o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.context.view_layer.update()
        bpy.ops.object.bake(type='NORMAL' if channel=='Tangent Normal' else 'EMIT')
        file=OUT/'neutral_bakes'/f'{name}_{channel.replace(" ","_")}_512.exr';file.parent.mkdir(exist_ok=True);image.filepath_raw=str(file);image.file_format='OPEN_EXR';image.save_render(str(file),scene=s)
        references.append({'renderer':name,'channel':channel,'path':file.relative_to(OUT).as_posix(),'sha256':sha(file),'bytes':file.stat().st_size,'dimensions':[512,512],'UV':o.data.uv_layers.active.name,'space':'scene-linear RGB without display view transform; Alpha in RGB (do not confuse image coverage A)','normal_convention':'Blender tangent bake R:+X,G:+Y,B:+Z; encoded [0,1] to[-1,1]; preserve original UV orientation, no automatic green inversion','purpose':'Frozen source neutral input reference only; not authoritative source texture; combined slots may overlap UVs, exact polygon/UV assignment remains authority'})
        for i,mat in enumerate(original):o.material_slots[i].material=mat
        for copy in copies:bpy.data.materials.remove(copy)
        bpy.data.images.remove(image)
        print('BAKE_REFERENCE',name,channel,flush=True)
(s.render.engine,s.cycles.device,s.cycles.samples,s.render.threads_mode,s.render.threads,s.render.bake.margin,s.render.bake.use_clear,s.render.bake.use_selected_to_active,s.render.bake.normal_space,s.render.image_settings.file_format,s.render.image_settings.color_depth,s.render.image_settings.color_mode)=save
for o in bpy.data.objects:
    hidden,viewport,selection=states[o.name];o.hide_viewport=viewport;o.hide_set(hidden);o.select_set(selection)
bpy.context.view_layer.objects.active=active
after=snapshot([a.name for a in bpy.data.actions]);diff=difference(before,after);write('neutral_bake_source_component_diff.json',diff);assert not diff,diff
write('NEUTRAL_BAKE_RECEIPT.json',{'source_saved':False,'source_component_differences':0,'CPU_only':True,'image_references':references,'opacity':'Principled Alpha actual input graph sampled; no opacity redesign','roughness':'Original graph/packed Non-Color texture authoritative; Unity smoothness=1-roughness where same scalar convention, no clamp/tuning permitted','masks':'Exact source POINT/CORNER attributes and polygon material-slot arrays in NPZ; no invented color mask','limitations':'512px neutral UV diagnostic, not dynamic material equivalence; positional/procedural terms and board/blink drivers must remain executable. UV overlap/lighting/PBR differences are not hidden.'})
print('NEUTRAL_REFERENCE_BAKE_COMPLETE',len(references))
