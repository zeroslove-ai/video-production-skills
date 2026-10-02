"""Private R2 reference, body-only adapter of the first three semantic acting scores.
Target face A/O gate failed; no elaborate facial recipe is authored here.
No product integration/export. Original 66 actions, skin, rig and shape geometry preserved.
"""
from pathlib import Path
import bpy,math,json,hashlib,sys
from mathutils import Vector,Quaternion,Matrix
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
ELBOW='please_elbow' in sys.argv
REVISION='please_hands' in sys.argv or ELBOW
from acting_recipe import score,curve
from native_preservation import signature
SOURCE=Path(r'C:\Users\JAEWAN\Downloads\Character_Master_R2_20261002.blend')
folder='native-body-r3-please-elbow' if ELBOW else 'native-body-r3-please-hands' if REVISION else 'native-body-r3'
OUT=ROOT/('local/'+folder);OUT.mkdir(parents=True,exist_ok=True)
E=ROOT/('evidence/'+folder);E.mkdir(parents=True,exist_ok=True)
sha=hashlib.sha256(SOURCE.read_bytes()).hexdigest();assert sha=='5e88819a61120b74c9a0e3de03f90b9890b7ac13eea2113e10fcada321d21d2e'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));s=bpy.context.scene;r=bpy.data.objects['Armature'];r.hide_set(False)
original=sorted(a.name for a in bpy.data.actions);preserved=signature(original)
r.animation_data.action=bpy.data.actions['MOTION5H_WeightShift_Loop_8s'];s.frame_set(1)
base={b.name:b.matrix_basis.copy() for b in r.pose.bones};world={b.name:b.matrix.to_quaternion() for b in r.pose.bones}
for o in bpy.data.objects:
    if o.animation_data:
        o.animation_data.action=None
        for tr in o.animation_data.nla_tracks:tr.mute=True
    if o.type=='MESH' and o.data.shape_keys:
        if o.data.shape_keys.animation_data:o.data.shape_keys.animation_data.action=None
        for k in o.data.shape_keys.key_blocks:
            if k.name in ('JawOpen','Smile.L','Smile.R','Blink.L','Blink.R','BrowRaise.L','BrowRaise.R','BrowKnit.L','BrowKnit.R','CheekLift.L','CheekLift.R','LipPucker','MouthWide','ExprSmileCurve','ExprMouthDown','ExprBrowInnerUp'):k.value=0.
h=bpy.data.objects['Character_Body_Head'];h['Face_GazeYaw']=0.;h['Face_GazePitch']=0.
def rotate(name,angles):
    q=Quaternion((1,0,0),0)
    for axis,deg in zip(((1,0,0),(0,1,0),(0,0,1)),angles):q=Quaternion(axis,math.radians(deg))@q
    b=r.pose.bones[name];b.matrix_basis=base[name]@(world[name].inverted()@q@world[name]).to_matrix().to_4x4()
def neutral():
    for b in r.pose.bones:b.matrix_basis=base[b.name]
    rotate('J_Bip_L_UpperArm',(0,20,0));rotate('J_Bip_R_UpperArm',(0,-20,0));bpy.context.view_layer.update()
neutral();neutral_basis={b.name:b.matrix_basis.copy() for b in r.pose.bones}
wrists={side:r.pose.bones[f'J_Bip_{side}_Hand'].matrix.copy() for side in ('L','R')}
arm_rolls={}
def stable_frame(y,normal,roll):
    y=y.normalized();x=normal.normalized();z=x.cross(y).normalized();x=y.cross(z).normalized()
    return Matrix((x*math.cos(roll)+z*math.sin(roll),y,z*math.cos(roll)-x*math.sin(roll))).transposed()
def arm_ik(side,goal,hand_rotation,elbow_low=False):
    u=r.pose.bones[f'J_Bip_{side}_UpperArm'];l=r.pose.bones[f'J_Bip_{side}_LowerArm'];hand=r.pose.bones[f'J_Bip_{side}_Hand']
    hip=u.head.copy();d=goal-hip;length=min(d.length,u.bone.length+l.bone.length-1e-5);direction=d.normalized();goal=hip+direction*length
    a=u.bone.length;b=l.bone.length;along=(a*a-b*b+length*length)/(2*length);height=math.sqrt(max(0,a*a-along*along))
    # Outward pole avoids the wrist-path crossing the old diagonal pole direction.
    pole=Vector((1 if side=='L' else -1,-.4 if elbow_low else 0,-1.6 if elbow_low else 0));pole=(pole-direction*direction.dot(pole)).normalized();elbow=hip+direction*along+pole*height
    normal=direction.cross(pole).normalized()
    for bone,target,position in ((u,elbow-hip,hip),(l,goal-elbow,elbow)):
        if bone.name not in arm_rolls:
            reference=stable_frame(bone.tail-bone.head,normal,0)
            original_x=bone.matrix.to_3x3().col[0].normalized()
            arm_rolls[bone.name]=math.atan2(original_x.dot(reference.col[2]),original_x.dot(reference.col[0]))
        bone.matrix=Matrix.Translation(position)@stable_frame(target,normal,arm_rolls[bone.name]).to_4x4()
        bpy.context.view_layer.update()
    hand.matrix=Matrix.Translation(goal)@hand_rotation.to_matrix().to_4x4();bpy.context.view_layer.update()
    return (hand.head-goal).length
upright=Matrix(((1,0,0),(0,0,1),(0,-1,0))).transposed().to_quaternion()
records=[];registry={};max_error=0
for clip in ('greeting_wave','shy_lookaway','please_tilt'):
    arm_rolls.clear()
    a=bpy.data.actions.new('RND_R3_'+clip+'_BODY_ONLY');a.use_fake_user=True;registry[clip]=a.name
    samples=[];previous_quaternions={}
    for f in range(1,122):
        r.animation_data.action=None;s.frame_set(f);neutral();t=(f-1)/24;v=score(clip,t)
        for logical,native in (('head','J_Bip_C_Head'),('neck','J_Bip_C_Neck'),('chest','J_Bip_C_Chest')):
            x,y,z=v['rotations_degrees'].get(logical,(0,0,0));rotate(native,(x,-z,y))
        bpy.context.view_layer.update()
        if clip=='greeting_wave':
            lift=curve(t,[(0,0),(.35,0),(.65,-.06),(1.58,1),(2.75,1),(3.25,.86),(4.6,0),(5,0)])
            wave=v['rotations_degrees']['hand.R'][2]
            start=wrists['R'].translation;goal=start.lerp(Vector((-.115,-.135,.872)),lift)
            goal.x-=.070*math.sin(math.pi*max(0,min(1,lift)))
            rotation=wrists['R'].to_quaternion().slerp(Quaternion((0,1,0),math.radians(wave))@upright,max(0,lift))
            max_error=max(max_error,arm_ik('R',goal,rotation))
        elif clip=='please_tilt':
            ask=curve(t,[(0,0),(.45,-.07),(1.4,1),(2.95,1),(3.35,1.045),(4.65,0),(5,0)])
            for side,sign in (('L',1),('R',-1)):
                destination=Vector((sign*.075,-.14,.635));hand_target=upright
                if REVISION:
                    destination=Vector((sign*.045,-.19+sign*.005,.730+sign*.007))
                    finger_direction=Vector((-sign*.30,0,.95)).normalized()
                    palm=Vector((-sign*.95,0,-.30)).normalized()
                    across=finger_direction.cross(palm).normalized()
                    hand_target=Matrix((across,finger_direction,palm)).transposed().to_quaternion()
                goal=wrists[side].translation.lerp(destination,ask)
                rotation=wrists[side].to_quaternion().slerp(hand_target,(1. if REVISION else .75)*max(0,min(1,ask)))
                max_error=max(max_error,arm_ik(side,goal,rotation,elbow_low=ELBOW))
        r.animation_data.action=a
        for b in r.pose.bones:
            b.rotation_mode='QUATERNION'
            q=b.rotation_quaternion.copy()
            if b.name in previous_quaternions and previous_quaternions[b.name].dot(q)<0:q.negate();b.rotation_quaternion=q
            previous_quaternions[b.name]=q.copy()
            b.keyframe_insert('rotation_quaternion',frame=f,group=b.name);b.keyframe_insert('location',frame=f,group=b.name);b.keyframe_insert('scale',frame=f,group=b.name)
        samples.append({'frame':f,'root':list(r.pose.bones['Root'].matrix.translation),'feet':[list(r.pose.bones[f'J_Bip_{side}_Foot'].head) for side in ('L','R')],'wrists':[list(r.pose.bones[f'J_Bip_{side}_Hand'].head) for side in ('L','R')]})
    for layer in a.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for p in fc.keyframe_points:p.interpolation='LINEAR'
    records.append({'clip':clip,'action':a.name,'samples':samples})
assert max_error<1e-5
assert signature(original)==preserved;assert sha==hashlib.sha256(SOURCE.read_bytes()).hexdigest()
for act in bpy.data.actions:act.use_fake_user=True
allowed={o.name for o in bpy.data.objects if o.type=='MESH' and any(m.type=='ARMATURE' and m.object==r for m in o.modifiers)}|{'Globe.L','Globe.R','Hair_Scalp_Coverage'}
for o in bpy.data.objects:
    if o.type=='MESH':o.hide_render=o.name not in allowed
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=16;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4;s.render.fps=24;s.render.image_settings.file_format='PNG'
# Keep existing source lighting: controlled adapter, not a beauty/material revision.
cameras={}
for name,lens,loc,target,res in [('full_body',50,(0,-3.3,.64),(0,0,.49),(640,360)),('waist_threequarter',65,(.65,-2,.92),(0,0,.74),(640,360)),('hand_face',65,(-.23,-1.25,.95),(-.055,0,.855),(640,360)),('face_close',85,(.07,-1.05,.92),(0,0,.89),(640,360)),('vertical',50,(.07,-2.0,.75),(0,0,.55),(360,640))]:
    cd=bpy.data.cameras.new('RND_R3_'+name);cam=bpy.data.objects.new(cd.name,cd);s.collection.objects.link(cam);cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cd.lens=lens;cd.sensor_width=36
    cameras[name]={'object':cam.name,'lens_mm':lens,'location_m':loc,'target_m':target,'rotation_euler':list(cam.rotation_euler),'sensor_width_mm':36,'resolution':res}
r.animation_data.action=bpy.data.actions[registry['greeting_wave']];s.frame_start=1;s.frame_end=121;s.frame_set(1);s.camera=bpy.data.objects[cameras['waist_threequarter']['object']]
s['research_status']='PRIVATE_BODY_TIMING_ADAPTER; FACE_NEUTRAL; NOT_YURI_PRODUCT_ANIMATION'
p=OUT/'R2_NATIVE_BODY_TIMING_R3.blend';bpy.ops.wm.save_as_mainfile(filepath=str(p))
(E/'preservation.json').write_text(json.dumps({'result':'PASS','original_actions':len(original),'digests':preserved,'source_sha256':sha,'source_unchanged':True},indent=2))
(E/'build_receipt.json').write_text(json.dumps({'candidate':str(p),'candidate_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'revision':'please elbow pole downward; same wrist goals/palm orientation as hand revision' if ELBOW else 'please hand strategy (wrist destination + palm orientation) only' if REVISION else 'baseline','action_registry':registry,'cameras':cameras,'max_ik_error_m':max_error,'face':'NEUTRAL ONLY; A/O readability gate failed; elaborate target face recipes withheld','actual_yuri_approved_performances':0,'classification':'NATIVE_BODY_RESEARCH_REFERENCE_NO_PRODUCT_INTEGRATION','clips':records},indent=2))
print('NATIVE_BODY_R3_BUILD_PASS',p,max_error)
