"""Extend the R1 checkpoint; preserve baseline and author only original proxy.
Blender --background --factory-startup --threads 4 --python-exit-code 1 --python this.py
"""
from pathlib import Path
import bpy,json,math,hashlib,sys
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from acting_recipe import score,timing_sheet
OUT=ROOT/'local/acting-r2';OUT.mkdir(parents=True,exist_ok=True)
E=ROOT/'evidence/acting-r2';E.mkdir(parents=True,exist_ok=True)
SOURCE=ROOT/'local/output/YURI_PERFORMANCE_PROXY_R1.blend'
source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));s=bpy.context.scene;r=bpy.data.objects['ProxyHumanoid']
original_bones=[b.name for b in r.data.bones]
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=12;s.cycles.use_denoising=True
s.render.threads_mode='FIXED';s.render.threads=4;s.render.fps=24
s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100
# Original checkpoint Actions remain in the file; detach, never delete.
for action in bpy.data.actions:action.use_fake_user=True
for obj in bpy.data.objects:
    if obj.animation_data:obj.animation_data.action=None
    if obj.type=='MESH' and obj.data.shape_keys and obj.data.shape_keys.animation_data:
        obj.data.shape_keys.animation_data.action=None
for b in r.pose.bones:b.rotation_euler=(0,0,0)

skin=bpy.data.materials['Proxy skin'];dark=bpy.data.materials['Proxy face ink']
def mat(name,c):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*c,1)
    n=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    n.inputs['Base Color'].default_value=(*c,1);n.inputs['Roughness'].default_value=.6
    return m
eye_white=mat('R2 eye ivory',(.88,.86,.81));iris=mat('R2 iris warm violet',(.09,.055,.18))
def ellipsoid(name,centre,scale,material,bone='head'):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=centre)
    o=bpy.context.object;o.name=name;o.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(material)
    for p in o.data.polygons:p.use_smooth=True
    vg=o.vertex_groups.new(name=bone);vg.add(list(range(len(o.data.vertices))),1,'REPLACE')
    m=o.modifiers.new('Original proxy rigid attachment','ARMATURE');m.object=r;o.parent=r
    return o
keys={k.name:k for o in bpy.data.objects if o.type=='MESH' and o.data.shape_keys for k in o.data.shape_keys.key_blocks if k.name!='Basis'}
for k in keys.values():k.value=0
whites={};pupils={};pupil_locations={};catchlights={};catchlight_locations={}
for side,sign in [('L',1),('R',-1)]:
    eye=bpy.data.objects['Eye.'+side];eye.hide_render=True
    whites[side]=ellipsoid('R2 white.'+side,(sign*.077,-.170,1.646),(.042,.020,.047),eye_white)
    pupils[side]=ellipsoid('R2 pupil.'+side,(sign*.077,-.190,1.646),(.022,.007,.031),iris)
    pupil_locations[side]=pupils[side].location.copy()
    for o in (whites[side],pupils[side]):
        o.shape_key_add(name='Basis');k=o.shape_key_add(name='r2_eye_close')
        for v in k.data:v.co.z*=.035
    # New independent squint shares the blink composition budget, not another writer.
    catchlights[side]=ellipsoid('R2 catchlight.'+side,(sign*.077-.006,-.196,1.657),(.004,.002,.004),eye_white)
    catchlight_locations[side]=catchlights[side].location.copy()
    catchlights[side].shape_key_add(name='Basis');k=catchlights[side].shape_key_add(name='r2_eye_close')
    for v in k.data:v.co*=.001

# An open-palm silhouette, rigid proxy fingers; no finger-rig acceptance claim.
for side,sign in [('L',1),('R',-1)]:
    hand=r.data.bones['hand.'+side]
    rest=hand.matrix_local
    for i in range(4):
        centre=rest@Vector(((i-1.5)*.021,.085,.007))
        o=ellipsoid(f'R2 finger {i}.{side}',centre,(.009,.048-i*.003,.009),skin,'hand.'+side)
        o.rotation_mode='QUATERNION';o.rotation_quaternion=rest.to_quaternion()
    centre=rest@Vector((-.060*sign,.028,0))
    ellipsoid('R2 thumb.'+side,centre,(.027,.012,.018),skin,'hand.'+side)
    bpy.data.objects['hand.'+side].scale=(.75,.55,.65)

bindings=[]
def action_for(owner,name):
    owner.animation_data_create();a=bpy.data.actions.new(name);a.use_fake_user=True
    owner.animation_data.action=a;bindings.append((owner,a));return a
def bake(clip,gain=1,lead=.18,suffix='natural'):
    bindings.clear();body=action_for(r,f'R2_{clip}_{suffix}_BODY')
    animated_keys=[o.data.shape_keys for o in bpy.data.objects if o.type=='MESH' and o.data.shape_keys and not o.hide_render]
    for k in animated_keys:action_for(k,f'R2_{clip}_{suffix}_FACE_{k.name}')
    for o in [*pupils.values(),*catchlights.values()]:action_for(o,f'R2_{clip}_{suffix}_GAZE_{o.name}')
    samples=[]
    for frame in range(1,122):
        t=(frame-1)/24;v=score(clip,t,gain,lead)
        # Avoid action evaluation overwriting intended values while baking.
        for owner,a in bindings:owner.animation_data.action=None
        for b in r.pose.bones:
            b.rotation_mode='XYZ';b.rotation_euler=tuple(math.radians(x) for x in v['rotations_degrees'].get(b.name,(0,0,0)))
        for k in keys.values():k.value=v['face_intents'].get(k.name,0)
        for side in ('L','R'):
            blink=v['face_intents']['blink_'+side.lower()]
            squint=v['face_intents']['squint_'+side.lower()]
            close=max(blink,squint)
            for o in (whites[side],pupils[side]):o.data.shape_keys.key_blocks['r2_eye_close'].value=close
            pupils[side].location=pupil_locations[side]+Vector((v['gaze_xy'][0]*.014,0,v['gaze_xy'][1]*.014))
            catchlights[side].location=catchlight_locations[side]+Vector((v['gaze_xy'][0]*.014,0,v['gaze_xy'][1]*.014))
            catchlights[side].data.shape_keys.key_blocks['r2_eye_close'].value=close
        for owner,a in bindings:owner.animation_data.action=a
        for b in r.pose.bones:b.keyframe_insert('rotation_euler',frame=frame,group=b.name)
        for k in animated_keys:
            for key in k.key_blocks:
                if key.name!='Basis':key.keyframe_insert('value',frame=frame)
        for o in [*pupils.values(),*catchlights.values()]:o.keyframe_insert('location',frame=frame)
        samples.append(v)
    for owner,a in bindings:
        for layer in a.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for fc in bag.fcurves:
                        for p in fc.keyframe_points:p.interpolation='LINEAR'
    return [(o.name,a.name) for o,a in bindings]

registry={};clips=['greeting_wave','shy_lookaway','please_tilt']
for clip in clips:
    registry[clip]={}
    for mode,gain in [('natural',1),('exaggerated_head',1.45)]:
        registry[clip][mode]=bake(clip,gain,suffix=mode)
    (E/(clip+'_timing.json')).write_text(json.dumps(timing_sheet(clip),indent=2))
registry['shy_lookaway']['simultaneous']=bake('shy_lookaway',lead=0,suffix='simultaneous')

def bind(clip,mode='natural'):
    for o in bpy.data.objects:
        if o.animation_data:o.animation_data.action=None
        if o.type=='MESH' and o.data.shape_keys and o.data.shape_keys.animation_data:o.data.shape_keys.animation_data.action=None
    for owner,name in registry[clip][mode]:
        o=bpy.data.objects.get(owner) or bpy.data.shape_keys.get(owner)
        o.animation_data_create();o.animation_data.action=bpy.data.actions[name]
    s.frame_set(1)

camera_specs={
 'full_body':(50,(0,-5.8,1.1),(0,0,.94),(640,360)),
 'waist_threequarter':(65,(1.6,-3.5,1.7),(0,0,1.35),(640,360)),
 'face_close':(85,(.10,-2.25,1.67),(0,0,1.61),(640,360)),
 'hand_face':(60,(-.70,-2.3,1.6),(-.12,0,1.43),(640,360)),
 'vertical':(50,(.10,-3.8,1.45),(0,0,1.08),(360,640))}
cameras={}
for name,(lens,location,target,res) in camera_specs.items():
    data=bpy.data.cameras.new('R2_'+name);o=bpy.data.objects.new('R2_'+name,data);s.collection.objects.link(o)
    o.location=location;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();data.lens=lens;data.sensor_width=36
    cameras[name]={'object':o.name,'lens_mm':lens,'location_m':location,'target_m':target,'rotation_euler':list(o.rotation_euler),'sensor_width_mm':36,'resolution':res,'sensor_fit':data.sensor_fit,'coordinate_space':'Z up, -Y front, meters','runtime_camera':False}
s.frame_start=1;s.frame_end=121;bind('greeting_wave');s.camera=bpy.data.objects['R2_waist_threequarter']
s['asset_status']='ORIGINAL_R1_PROXY_EXTENDED_FOR_SEMANTIC_TIMING; NOT_ACTUAL_YURI'
s['research_gpu']='NO_GPU_RENDER_OR_INFERENCE'
assert original_bones==[b.name for b in r.data.bones]
path=OUT/'YURI_PERFORMANCE_ACTING_R2.blend';bpy.ops.wm.save_as_mainfile(filepath=str(path))
(E/'action_registry.json').write_text(json.dumps(registry,indent=2))
(E/'camera_metadata.json').write_text(json.dumps(cameras,indent=2))
(E/'build_receipt.json').write_text(json.dumps({'source':str(SOURCE),'source_sha256':source_hash,'candidate':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'body_bones_preserved':len(original_bones),'physical_recipes':3,'derived_animation_variants_not_new_clips':4,'actual_yuri_approved':0,'face_gate':'PROXY_ONLY; ACTUAL_TARGET_PENDING','gpu_render_inference':0},indent=2))
print('ACTING_R2_BUILD_PASS',path)
