"""CPU visual/deformation probe; isolated source scene, no file writes to source.
Native and imported branches share the original studio, shader-free FBX losses
remain visible. Contact-sheet/video diagnostics are not appearance promotion.
"""
import bpy,sys,json,gzip,math
from pathlib import Path
from mathutils import Vector,Matrix
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_adapter import ReactionLane
ROOT=HERE.parent;E=ROOT/'evidence/o1-native-unity-probe-r1'
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-native-unity-probe-r1')
SOURCE=ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
LIB=OUT.parent/'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'
MODE=sys.argv[sys.argv.index('--')+1];assert MODE in ('native','imported')
def load(n):return json.loads((OUT/'metadata'/n).read_text(encoding='utf8'))
def gzload(n):
    with gzip.open(OUT/'reference'/n,'rt',encoding='utf8') as f:return json.load(f)
def gzsave(n,v):
    with gzip.open(OUT/'reference'/n,'wt',encoding='utf8') as f:json.dump(v,f,separators=(',',':'))
def write(n,v):
    for p in (E/n,OUT/'metadata'/n):p.write_text(json.dumps(v,indent=2),encoding='utf8')
clips=load('export_manifest.json')['clips'];rig_names=['Meshy_Fitted_Rig','Armature','Hair_Rig_R4','AVATAR_FaceBoard']
meshnames=[m['name'] for m in load('source_renderers_bind.json')]
bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False)
s=bpy.context.scene
if MODE=='native':
    with bpy.data.libraries.load(str(LIB),link=False) as (src,dst):dst.actions=[c['authored_Action'] for c in clips]
    lane=ReactionLane()
    def bind(name):
        a=lane.on(name);lane.rig.animation_data.action_slot=next(x for x in a.slots if x.identifier=='OBMeshy_Fitted_Rig')
    def off():lane.off()
else:
    # Only disposable in-memory source scene is altered. Keep original studio
    # camera/lights/world and non-carrier objects at their original world poses.
    remove={bpy.data.objects[x['name']] for x in load('export_manifest.json')['objects']}
    for o in list(bpy.data.objects):
        if o not in remove and o.parent in remove:
            world=o.matrix_world.copy();o.parent=None;o.matrix_world=world
    for o in remove:bpy.data.objects.remove(o,do_unlink=True)
    for mat in list(bpy.data.materials):
        if mat.users==0:bpy.data.materials.remove(mat)
    with bpy.data.libraries.load(str(OUT/'YURI_O1_R4_NATIVE_IMPORTED_QA_20261003_R1.blend'),link=False) as (src,dst):
        dst.objects=list(src.objects);dst.actions=list(src.actions)
    for o in dst.objects:
        if not o.users_collection:s.collection.objects.link(o)
    rigmap={n:bpy.data.objects[n] for n in rig_names}
    inv={c['authored_Action']:{v['rig']:v for v in c['imported_rig_actions']} for c in load('take_and_slot_inventory.json')}
    def off():
        for r in rigmap.values():
            if r.animation_data:r.animation_data.action=None
            for b in r.pose.bones:b.matrix_basis=Matrix.Identity(4)
        s.frame_set(1);bpy.context.view_layer.update()
    def bind(name):
        off()
        for n,v in inv[name].items():
            r=rigmap[n];a=bpy.data.actions[v['action']];r.animation_data_create();r.animation_data.action=a;r.animation_data.action_slot=next(x for x in a.slots if x.identifier==v['slot'])

def geometry():
    deps=bpy.context.evaluated_depsgraph_get();v={}
    for n in meshnames:
        o=bpy.data.objects[n];ev=o.evaluated_get(deps);m=ev.to_mesh();v[n]=[list(ev.matrix_world@p.co) for p in m.vertices];ev.to_mesh_clear()
    return v
def metrics(actual,expected):
    rows=[]
    for n,v in actual.items():
        ref=expected[n]
        if len(v)!=len(ref):rows.append({'mesh':n,'count_equal':False});continue
        ds=[(Vector(p)-Vector(q)).length for p,q in zip(v,ref)]
        rows.append({'mesh':n,'count_equal':True,'max_corresponding_vertex_delta_m':max(ds),'mean_corresponding_vertex_delta_m':sum(ds)/len(ds)})
    return rows
off();baseline=geometry();motion_geometry={};comparison=[]
native=gzload('native_evaluated_motion_geometry_0_25_50_100.json.gz') if MODE=='imported' else None
for c in clips:
    name=c['authored_Action'];bind(name);samples={}
    for f in sorted({1,1+round((c['end']-1)*.25),1+round((c['end']-1)*.5),c['end']}):
        s.frame_set(f);bpy.context.view_layer.update();samples[str(f)]=geometry()
        if native:comparison.append({'action':name,'frame':f,'mesh_errors':metrics(samples[str(f)],native[name][str(f)])})
    motion_geometry[name]=samples;off()
if MODE=='native':gzsave('native_evaluated_motion_geometry_0_25_50_100.json.gz',motion_geometry)
else:write('motion_deformation_comparison.json',comparison)
restored=geometry();write(MODE+'_visual_geometry_receipt.json',{'OFF_ON_OFF_max_geometry_delta_m':max(r['max_corresponding_vertex_delta_m'] for r in metrics(restored,baseline)),'source_file_saved':False,'meshes_tested':len(meshnames),'evaluation_samples':24,'mode':MODE})
if MODE=='imported':
    original=gzload('source_original_vertex_weights.json.gz');rows=[]
    for n,w in original.items():
        o=bpy.data.objects[n];sourcegroups=w['groups'];actualgroups={g.index:g.name for g in o.vertex_groups};maxerr=0;missing=set()
        deform={b.name for r in rigmap.values() for b in r.data.bones}
        for i,v in enumerate(o.data.vertices):
            expected={sourcegroups[g]:weight for g,weight in w['influences'][i] if sourcegroups[g] in deform}
            actual={actualgroups[g.group]:g.weight for g in v.groups if actualgroups[g.group] in deform}
            missing.update(k for k in set(expected)-set(actual) if expected[k]>0);maxerr=max(maxerr,max([abs(expected.get(k,0)-actual.get(k,0)) for k in set(expected)|set(actual)] or [0]))
        rows.append({'mesh':n,'max_skin_bone_influence_delta':maxerr,'missing_influenced_bones':sorted(missing),'source_nonbone_mask_groups_not_FBX_skin':[g for g in sourcegroups if g not in deform]})
    write('skin_weight_roundtrip_comparison.json',rows)

# Identical CPU cycles configuration. Original material/world/light graphs
# remain untouched; imported carrier uses only its own serialized materials.
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=8;s.cycles.use_denoising=False;s.cycles.seed=0
s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.fps=24;s.render.fps_base=1
folder=OUT/'visual'/MODE;folder.mkdir(parents=True,exist_ok=True)
off();s.camera=bpy.data.objects['Assembly_Review_Camera'];s.render.resolution_x=960;s.render.resolution_y=920
s.render.filepath=str(folder/'neutral_source_camera.png');bpy.ops.render.render(write_still=True)
camera=bpy.data.objects.new('O1_QA_CAMERA',bpy.data.cameras.new('O1_QA_CAMERA_DATA'));s.collection.objects.link(camera)
camera.location=(1.8,-3,.62);camera.rotation_euler=(Vector((.002,-.025,.49))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=1.18;s.camera=camera
s.render.resolution_x=192;s.render.resolution_y=288;s.render.filepath=str(folder/'neutral_fullbody.png');bpy.ops.render.render(write_still=True)
schedule=[];counter=0
for c in clips:
    name=c['authored_Action'];bind(name);period=c['end']-1;count=period*(2 if c['loop'] else 1)
    for tick in range(count):
        f=1+tick%period;s.frame_set(f);bpy.context.view_layer.update();s.render.filepath=str(folder/f'frame_{counter:04d}.png');bpy.ops.render.render(write_still=True);counter+=1
    schedule.append({'action':name,'first_video_frame':counter-count,'video_frames':count,'fps':24,'loop_cycles':2 if c['loop'] else 1,'cuts':'separate diagnostic clip; not smooth sequence acceptance'});off()
write(MODE+'_visual_schedule.json',schedule)
print('VISUAL_PROBE_COMPLETE',MODE,counter,flush=True)
