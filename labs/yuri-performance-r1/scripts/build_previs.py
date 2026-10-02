"""Original proxy ONLY: three acting seeds, six cameras, skeletal+morph GLB proof.
Run with Blender --background --factory-startup --threads 4 --python this_file.
Uses CPU Cycles only. Never reads/writes existing avatar or live Blender scenes.
"""
from pathlib import Path
import bpy, json, math, hashlib, struct, sys
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'local/output'
OUT.mkdir(parents=True,exist_ok=True)
FPS=24
FRAMES=96
scene=bpy.context.scene
# This entry point must be a new factory-startup process, not a live MCP call.
if bpy.data.filepath:
    raise RuntimeError('Refusing to modify an already-open .blend; use factory-startup')
initial={'blender':bpy.app.version_string,'initial_objects':len(bpy.data.objects),'initial_filepath':bpy.data.filepath}
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene.unit_settings.system='METRIC'
scene.render.fps=FPS
scene.frame_start=1
scene.frame_end=FRAMES*3
scene.render.engine='CYCLES'
scene.cycles.device='CPU'
scene.cycles.samples=24
scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED'
scene.render.threads=4
scene.render.resolution_x=480
scene.render.resolution_y=270
scene.render.resolution_percentage=100
scene.world.color=(.12,.12,.12)
scene.view_settings.view_transform='Standard'

def material(name,color):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Roughness'].default_value=.72
    return m
skin=material('Proxy skin',(.78,.56,.42))
suit=material('Proxy lavender suit',(.39,.35,.64))
legs=material('Proxy slate legs',(.20,.24,.35))
dark=material('Proxy face ink',(.055,.035,.065))
white=material('Neutral studio',(.75,.77,.80))

# Original 17-bone rest skeleton; not claimed to be VRM or universal retarget data.
bones={
 'hips':((0,0,.86),(0,0,1.0),None),
 'spine':((0,0,1.0),(0,0,1.16),'hips'),
 'chest':((0,0,1.16),(0,0,1.33),'spine'),
 'neck':((0,0,1.33),(0,0,1.44),'chest'),
 'head':((0,0,1.44),(0,0,1.70),'neck')}
for side,sign in [('L',1),('R',-1)]:
 bones.update({
  'upper_arm.'+side:((sign*.20,0,1.31),(sign*.34,0,1.08),'chest'),
  'forearm.'+side:((sign*.34,0,1.08),(sign*.40,0,.86),'upper_arm.'+side),
  'hand.'+side:((sign*.40,0,.86),(sign*.42,0,.75),'forearm.'+side),
  'thigh.'+side:((sign*.10,0,.86),(sign*.11,0,.47),'hips'),
  'shin.'+side:((sign*.11,0,.47),(sign*.11,0,.09),'thigh.'+side),
  'foot.'+side:((sign*.11,0,.09),(sign*.11,-.17,.05),'shin.'+side)})
armdata=bpy.data.armatures.new('ProxyHumanoidData')
arm=bpy.data.objects.new('ProxyHumanoid',armdata)
scene.collection.objects.link(arm)
bpy.context.view_layer.objects.active=arm
arm.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
for name,(head,tail,parent) in bones.items():
 b=armdata.edit_bones.new(name);b.head=head;b.tail=tail
 if parent:b.parent=armdata.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT')
arm['asset_status']='ORIGINAL_PROXY_NOT_YURI_NOT_FACE_ACCEPTANCE'
arm['source_license']='Original procedural geometry; no third-party input'
arm['rest_convention']='Z up; -Y forward; arms relaxed; rigid single-bone segment weights'
meshes=[]

def ellipsoid(name,center,scale,mat,bone=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,location=center)
    obj=bpy.context.object;obj.name=name;obj.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    obj.data.materials.append(mat)
    for p in obj.data.polygons:p.use_smooth=True
    if bone:
        vg=obj.vertex_groups.new(name=bone)
        vg.add(list(range(len(obj.data.vertices))),1,'REPLACE')
        mod=obj.modifiers.new('Proxy armature','ARMATURE');mod.object=arm
        obj.parent=arm
    meshes.append(obj)
    return obj

def segment(name,a,b,r,mat,bone):
    a,b=Vector(a),Vector(b)
    obj=ellipsoid(name,(a+b)/2,(r,r,(b-a).length*.56),mat,bone)
    obj.rotation_mode='QUATERNION';obj.rotation_quaternion=(b-a).to_track_quat('Z','Y')
    return obj
ellipsoid('Hip',(0,0,.9),(.18,.13,.13),legs,'hips')
ellipsoid('Torso',(0,0,1.15),(.22,.14,.25),suit,'spine')
ellipsoid('Neck',(0,0,1.39),(.075,.07,.1),skin,'neck')
ellipsoid('Head',(0,-.008,1.60),(.195,.17,.225),skin,'head')
for side in ['L','R']:
 for label in ['upper_arm','forearm','hand','thigh','shin','foot']:
  name=label+'.'+side;a,b,_=bones[name]
  segment(name,a,b,.058 if label in ['upper_arm','forearm','hand'] else .074,skin if label in ['forearm','hand'] else suit if label=='upper_arm' else legs,name)

keys={}
def morph(obj,name,edit):
    if obj.data.shape_keys is None:obj.shape_key_add(name='Basis')
    key=obj.shape_key_add(name=name)
    for v in key.data:edit(v.co)
    keys[name]=key
    return key
for side,sign in [('L',1),('R',-1)]:
    eye=ellipsoid('Eye.'+side,(sign*.077,-.174,1.645),(.038,.017,.044),dark,'head')
    morph(eye,'blink_'+side.lower(),lambda v:setattr(v,'z',v.z*.06))
    brow=ellipsoid('Brow.'+side,(sign*.078,-.165,1.709),(.049,.014,.011),dark,'head')
    morph(brow,'brow_up_'+side.lower(),lambda v:setattr(v,'z',v.z+.025))
mouth=ellipsoid('Mouth',(0,-.17,1.532),(.063,.014,.009),dark,'head')
morph(mouth,'smile',lambda v:setattr(v,'z',v.z+.027*(abs(v.x)/.063)**2))
morph(mouth,'jaw_open',lambda v:setattr(v,'z',v.z*3.3))

# Keep the original proxy definition and controls explicit; no topology/face claim.
clip_ids=['greeting_wave','shy_lookaway','please_tilt']

def pose(frame, rotations=None, values=None):
    rotations=rotations or {};values=values or {}
    for p in arm.pose.bones:
        p.rotation_mode='XYZ'
        p.rotation_euler=tuple(math.radians(a) for a in rotations.get(p.name,(0,0,0)))
        p.keyframe_insert(data_path='rotation_euler',frame=frame,group=p.name)
    for name,key in keys.items():
        key.value=values.get(name,0.0)
        key.keyframe_insert(data_path='value',frame=frame)

# Separate anticipations, beats, holds and returns rather than a single pose snap.
beats=[
 [(0,{},{}),(.15,{'head':(0,0,-4)},{'smile':.2}),(.35,{'upper_arm.R':(-22,0,-20),'forearm.R':(-115,0,0),'head':(0,0,-5)},{'smile':.65}),(.48,{'upper_arm.R':(-22,0,-20),'forearm.R':(-115,0,-14),'hand.R':(0,0,-18)},{'smile':.75}),(.6,{'upper_arm.R':(-22,0,-20),'forearm.R':(-115,0,14),'hand.R':(0,0,18)},{'smile':.75,'blink_l':1,'blink_r':1}),(.68,{'upper_arm.R':(-22,0,-20),'forearm.R':(-115,0,0)},{'smile':.6}),(.82,{'head':(0,0,-2)},{'smile':.3}),(1,{}, {})],
 [(0,{},{}),(.18,{'head':(-3,0,0)},{'smile':.25}),(.32,{'head':(4,18,0),'neck':(0,3,0)},{'smile':.35,'blink_l':.8,'blink_r':.8}),(.42,{'head':(6,20,0),'chest':(0,2,0)},{'smile':.35,'brow_up_l':.18}),(.62,{'head':(6,20,0)},{'smile':.3}),(.78,{'head':(2,-3,0)},{'smile':.5}),(1,{}, {})],
 [(0,{},{}),(.16,{'head':(0,0,-4)},{'brow_up_l':.15,'brow_up_r':.15}),(.36,{'head':(0,0,-13),'chest':(3,0,0),'forearm.L':(-30,0,0),'forearm.R':(-30,0,0)},{'smile':.28,'brow_up_l':.4,'brow_up_r':.3,'jaw_open':.1}),(.6,{'head':(0,-13,0),'chest':(3,0,0),'forearm.L':(-30,0,0),'forearm.R':(-30,0,0)},{'smile':.3,'brow_up_l':.4,'brow_up_r':.3}),(.78,{'head':(0,0,-5)},{'smile':.4}),(1,{}, {})]
]
for idx,rows in enumerate(beats):
    start=1+idx*FRAMES
    for t,r,v in rows:pose(start+round(t*(FRAMES-1)),r,v)
    scene.timeline_markers.new(clip_ids[idx],frame=start)
arm.animation_data.action.name='Proxy_Performance_3_Seeds'

# Cameras are separate assets, never baked into motion or automatically forced at runtime.
camera_specs=json.loads((ROOT/'catalog/cameras.json').read_text(encoding='utf-8'))['cameras']
for c in camera_specs:
 data=bpy.data.cameras.new(c['id']);obj=bpy.data.objects.new(c['id'],data)
 scene.collection.objects.link(obj);obj.location=c['location']
 obj.rotation_euler=(Vector(c['target'])-obj.location).to_track_quat('-Z','Y').to_euler()
 data.lens=c['lens_mm'];data.sensor_width=c['sensor_width_mm']
 obj['resolution']=c['resolution'];obj['preset_status']=c['status']
scene.camera=bpy.data.objects['full_front']
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.015))
floor=bpy.context.object;floor.name='Stage';floor.data.materials.append(white)
for name,loc,power,size in [('Key',(-3,-4,5),500,4),('Fill',(3,-2,3),260,3)]:
 data=bpy.data.lights.new(name,'AREA');obj=bpy.data.objects.new(name,data)
 scene.collection.objects.link(obj);obj.location=loc;data.energy=power;data.shape='DISK';data.size=size
 obj.rotation_euler=(Vector((0,0,1))-obj.location).to_track_quat('-Z','Y').to_euler()
scene.frame_set(1)
scene['quality_status']='TECHNICAL_PROXY_ONLY_NOT_FINAL_CHARACTER_OR_ACTING_ACCEPTANCE'
scene['fps_contract']=FPS
scene['gpu_use']='NONE_CYCLES_CPU'
blend=OUT/'YURI_PERFORMANCE_PROXY_R1.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(blend))

reports=[]
for idx,id_ in enumerate(clip_ids):
 start=1+idx*FRAMES;end=start+FRAMES-1
 scene.frame_start=start;scene.frame_end=end;scene.frame_set(start)
 bpy.ops.object.select_all(action='DESELECT')
 for obj in [arm,*meshes]:obj.select_set(True)
 bpy.context.view_layer.objects.active=arm
 path=OUT/(id_+'__proxy.glb')
 result=bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='SCENE',export_frame_range=True,export_force_sampling=True,export_morph=True,export_morph_animation=True,export_anim_slide_to_zero=True,export_skins=True,export_apply=False)
 raw=path.read_bytes();size=struct.unpack_from('<I',raw,12)[0];doc=json.loads(raw[20:20+size])
 animations=doc.get('animations',[])
 channel_paths=sorted(set(c['target']['path'] for a in animations for c in a.get('channels',[])))
 time_bounds=[(doc['accessors'][s['input']].get('min'),doc['accessors'][s['input']].get('max')) for a in animations for s in a['samplers']]
 has_skeletal_rotation=any(c['target']['path']=='rotation' and c['target'].get('node') in set(j for skin in doc.get('skins',[]) for j in skin.get('joints',[])) for a in animations for c in a.get('channels',[]))
 assert 'weights' in channel_paths and has_skeletal_rotation, (id_,channel_paths)
 assert doc.get('skins'), 'No skin in proxy export'
 sample=[]
 for frame in [start,start+FRAMES//2,end]:
  scene.frame_set(frame)
  sample.append({'frame':frame,'head_matrix':[list(row) for row in arm.pose.bones['head'].matrix],'face_values':{n:round(k.value,5) for n,k in keys.items()}})
 reports.append({'id':id_,'status':'PROXY_EXPORT_STRUCTURE_PASS','path':str(path),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'frames':[start,end],'sample_fps':FPS,'sampled_duration_seconds':(FRAMES-1)/FPS,'channels':channel_paths,'skeletal_rotation':has_skeletal_rotation,'skin_count':len(doc.get('skins',[])),'animation_count':len(animations),'time_bounds_first':time_bounds[:2],'samples':sample,'production_ready':False,'retarget_roundtrip':'NOT_TESTED','visual_acceptance':'PROXY_ONLY_NOT_FINAL'})
scene.frame_start=1;scene.frame_end=FRAMES*3;scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
receipt={'initial':initial,'result':'PROXY_NATIVE_BUILD_AND_GLB_STRUCTURE_PASS','bone_count':len(armdata.bones),'morph_count':len(keys),'cameras':len(camera_specs),'renderer':'CYCLES_CPU','file':str(blend),'clips':reports,'production_clips_completed':0,'proxy_seed_clips':3,'input_assets':'NONE_ORIGINAL_PROCEDURAL_PROXY','limitations':['rigid segments, no smooth anatomical deformation','no independent eyeball gaze','no fingers or real eyelid/lip/tongue topology','not actual Yuri and not a production face rig']}
(ROOT/'evidence/blender_proxy_build.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')

if '--render' in sys.argv:
 previews=[]
 for idx,id_ in enumerate(clip_ids):
  scene.camera=bpy.data.objects['waist_threequarter']
  scene.frame_set(idx*FRAMES+FRAMES//2)
  path=OUT/(id_+'__proxy_preview.png');scene.render.filepath=str(path)
  bpy.ops.render.render(write_still=True);previews.append(str(path))
 receipt['preview_frames']=previews
 (ROOT/'evidence/blender_proxy_build.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
if '--reel' in sys.argv:
 seq=OUT/'greeting_frames';seq.mkdir(exist_ok=True)
 scene.camera=bpy.data.objects['full_front']
 scene.render.resolution_x=384;scene.render.resolution_y=216;scene.cycles.samples=4
 for i,frame in enumerate(range(1,FRAMES+1,2)):
  scene.frame_set(frame);scene.render.filepath=str(seq/f'{i:04d}.png')
  bpy.ops.render.render(write_still=True)
 receipt['reel_sequence']={'path':str(seq),'frames':48,'output_fps':12,'clip_id':'greeting_wave','status':'RENDERED_AWAITING_ENCODING'}
 (ROOT/'evidence/blender_proxy_build.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print('YURI_PROXY_BUILD_COMPLETE',json.dumps({'bone_count':len(armdata.bones),'clips':len(reports),'file':str(blend)}))
