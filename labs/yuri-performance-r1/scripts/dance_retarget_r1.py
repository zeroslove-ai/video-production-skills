"""Reapply joint positions to an original humanoid through length-aware IK.
Uses the existing laboratory proxy and stable-frame infrastructure, body only.
"""
from pathlib import Path
import bpy,json,math,hashlib,sys
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[1];L=R/'local/dance-benchmark-r1';E=R/'evidence/dance-benchmark-r1';method=sys.argv[-1];data=json.loads((E/(method+'_motion.json')).read_text());source=R/'local/output/YURI_PERFORMANCE_PROXY_R1.blend';source_sha=hashlib.sha256(source.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;r=bpy.data.objects['ProxyHumanoid']
for o in bpy.data.objects:
    if o.animation_data:o.animation_data.action=None
    if o.type=='MESH' and o.data.shape_keys:
        if o.data.shape_keys.animation_data:o.data.shape_keys.animation_data.action=None
        for k in o.data.shape_keys.key_blocks:
            if k.name!='Basis':k.value=0
for a in bpy.data.actions:a.use_fake_user=True
s.frame_start=1;s.frame_end=360;s.render.fps=60;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=8;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4
s.render.resolution_x=480;s.render.resolution_y=720;s.render.resolution_percentage=100
for o in bpy.data.objects:
    if o.type=='CAMERA':o.hide_render=True
bpy.ops.object.camera_add(location=(.0,-4.7,1.35));cam=bpy.context.object;cam.name='DANCE_FRONT';cam.data.type='ORTHO';cam.data.ortho_scale=2.25;cam.rotation_euler=(Vector((0,0,.95))-cam.location).to_track_quat('-Z','Y').to_euler();s.camera=cam
points=data['cleaned'];hipheight=sorted((Vector(p[7])+Vector(p[8])).z/2 for p in points)[len(points)//2];source_leg_lengths=sorted(((Vector(p[7])-Vector(p[9])).length+(Vector(p[9])-Vector(p[11])).length+(Vector(p[8])-Vector(p[10])).length+(Vector(p[10])-Vector(p[12])).length)/2 for p in points);global_scale=(r.data.bones['thigh.L'].length+r.data.bones['shin.L'].length)/source_leg_lengths[len(points)//2]
ratios={};poles={};rolls={};prevq={};clamps=[];errors=[];world_rotations={};roll_repairs=0;forearm_directions={};limb_directions={};direction_repairs=[]
def frame(y,x):
    y=y.normalized();x=x-y*x.dot(y)
    if x.length<1e-5:x=Vector((0,1,0)).cross(y)
    x.normalize();z=x.cross(y).normalized();return Matrix((x,y,z)).transposed()
def place(name,pos,rotation):
    global roll_repairs
    if name in world_rotations:
        previous=world_rotations[name];y=rotation.col[1].normalized();oldx=previous.col[0]-y*previous.col[0].dot(y)
        if oldx.length>1e-5 and (name.startswith(('upper_arm.','forearm.','hand.','thigh.','shin.')) or rotation.col[0].dot(oldx)<0):
            # A near-straight limb has ambiguous axial roll. Parallel transport
            # preserves bend positions and bone direction without a 180-degree pop.
            rotation=frame(y,oldx);roll_repairs+=1
    world_rotations[name]=rotation.copy()
    b=r.pose.bones[name];b.matrix=Matrix.Translation(pos)@rotation.to_4x4();bpy.context.view_layer.update()
def ik(side,kind,start,end,pole_source):
    upper,lower=('upper_arm.','forearm.') if kind=='arm' else ('thigh.','shin.');u=r.pose.bones[upper+side];l=r.pose.bones[lower+side];d=end-start;rawlength=d.length;dist=max(.001,min(rawlength,u.bone.length+l.bone.length-.001));direction=d.normalized();goal=start+direction*dist
    pole=pole_source-start;pole-=direction*pole.dot(direction)
    key=kind+side
    if pole.length<.025 and key in poles:pole=poles[key]-direction*poles[key].dot(direction)
    if pole.length<1e-5:pole=Vector((0,-1,0))-direction*direction.y*-1
    pole.normalize()
    if key in poles:
        transported=poles[key]-direction*poles[key].dot(direction)
        if transported.length>1e-5:
            transported.normalize();angle=transported.angle(pole)
            if angle>math.radians(20):pole=transported.lerp(pole,math.radians(20)/angle).normalized()
    poles[key]=pole.copy();along=(u.bone.length**2-l.bone.length**2+dist**2)/(2*dist);h=math.sqrt(max(0,u.bone.length**2-along**2));joint=start+direction*along+pole*h;normal=direction.cross(pole).normalized()
    for b,a,z in [(u,start,joint),(l,joint,goal)]:
        # Stable bending normal, with rest-bone roll recorded once.
        rot=frame(z-a,normal)
        if b.name not in rolls:
            restx=b.bone.matrix_local.to_3x3().col[0];rolls[b.name]=math.atan2(restx.dot(rot.col[2]),restx.dot(rot.col[0]))
        angle=rolls[b.name];rot=Matrix.Rotation(angle,3,(z-a).normalized())@rot;place(b.name,a,rot)
    clamps.append(max(0,rawlength-dist));return goal,joint
action=bpy.data.actions.new('DANCE_R1_'+method+'_CLEANED');action.use_fake_user=True
for fi,values in enumerate(points):
    r.animation_data.action=None;s.frame_set(fi+1);p=[Vector(v)*global_scale for v in values];hip=(p[7]+p[8])/2;shoulder=(p[1]+p[2])/2;up=(shoulder-hip).normalized();across=(p[1]-p[2]).normalized();rot=frame(up,across)
    for name,offset in [('hips',0),('spine',.14),('chest',.30),('neck',.47)]:place(name,hip+up*offset,rot)
    hr=data['head_roll_radians'][fi];headup=Vector((-math.sin(hr),0,math.cos(hr)));place('head',hip+up*.58,frame(headup,Vector((1,0,0))))
    for side,sign,aidx,hidx,kidx,ank,heel,toe in [('L',1,(1,3,5),7,9,11,13,15),('R',-1,(2,4,6),8,10,12,14,16)]:
        sh=hip+up*.45+across*(sign*.20);u=r.pose.bones['upper_arm.'+side];lo=r.pose.bones['forearm.'+side]
        key='arm'+side
        if key not in ratios:
            lengths=sorted((Vector(v[aidx[0]])-Vector(v[aidx[1]])).length+(Vector(v[aidx[1]])-Vector(v[aidx[2]])).length for v in points);ratios[key]=(u.bone.length+lo.bone.length)/(lengths[len(lengths)//2]*global_scale)
        # Upper/lower arm ratios must be normalized separately. Total-length
        # scaling alone creates elbow inversion when source and target have
        # opposite upper/lower proportions near a fully folded elbow.
        upperdir=(p[aidx[1]]-p[aidx[0]]).normalized();lower=p[aidx[2]]-p[aidx[1]]
        if lower.length<.08 and side in forearm_directions:lowerdir=forearm_directions[side]
        else:lowerdir=lower.normalized()
        for segment,direction in [('upper',upperdir),('lower',lowerdir)]:
            dk=side+segment
            if dk in limb_directions:
                angle=limb_directions[dk].angle(direction)
                if angle>math.radians(20):
                    direction=limb_directions[dk].slerp(direction,math.radians(20)/angle);direction_repairs.append({'frame':fi+1,'segment':dk,'raw_step_deg':math.degrees(angle)})
            limb_directions[dk]=direction.copy()
            if segment=='upper':upperdir=direction
            else:lowerdir=direction
        forearm_directions[side]=lowerdir.copy();el=sh+upperdir*u.bone.length;wr=el+lowerdir*lo.bone.length
        # These normalized joint targets already satisfy both limb lengths.
        # Preserve their observed bend, rather than re-solving a singular folded
        # arm with an unrelated pole constraint. Legs still use contact-goal IK.
        place('upper_arm.'+side,sh,frame(el-sh,across));place('forearm.'+side,el,frame(wr-el,across));place('hand.'+side,wr,r.pose.bones['forearm.'+side].matrix.to_3x3())
        thighstart=hip+across*(sign*.10);footgoal=p[ank].copy()
        if data['contacts'][fi][0 if side=='L' else 1]:footgoal.z=.09
        knee=p[kidx];foot,joint=ik(side,'leg',thighstart,footgoal,knee);footdir=p[toe]-p[heel]
        if footdir.length<.03:footdir=Vector((0,-1,-.1))
        # Front-facing audit segment: 2D foot heading remains observable, while
        # monocular toe/heel depth sign is unstable. Constrain frontward heading
        # rather than allowing a hallucinated 180-degree reverse. Not suitable
        # for a turnaround phrase without another depth estimator.
        fx=max(-.13,min(.13,footdir.x));footdir=Vector((fx,-math.sqrt(max(.005,.17*.17-fx*fx)),-.04))
        place('foot.'+side,foot,frame(footdir,across))
    r.animation_data_create();r.animation_data.action=action
    for bone in r.pose.bones:
        bone.rotation_mode='QUATERNION';q=bone.rotation_quaternion.copy()
        if bone.name in prevq and prevq[bone.name].dot(q)<0:q.negate();bone.rotation_quaternion=q
        prevq[bone.name]=q.copy()
        for key in ['location','rotation_quaternion','scale']:bone.keyframe_insert(key,frame=fi+1,group=bone.name)
    errors.append(max(abs(b.scale[i]-1) for b in r.pose.bones for i in range(3)))
    if fi%60==0:print('RETARGET',method,fi,flush=True)
if action.slots:r.animation_data.action_slot=action.slots[0]
s.frame_set(1);path=L/(method+'_DANCE_R1.blend');bpy.ops.wm.save_as_mainfile(filepath=str(path))
bpy.ops.object.select_all(action='DESELECT');r.select_set(True)
for o in bpy.data.objects:
    if o.type=='MESH' and any(m.type=='ARMATURE' and m.object==r for m in o.modifiers):o.select_set(True)
bpy.context.view_layer.objects.active=r
bpy.ops.export_scene.gltf(filepath=str(L/(method+'_DANCE_R1.glb')),use_selection=True,export_animations=True,export_animation_mode='ACTIVE_ACTIONS',export_frame_range=True,export_force_sampling=True)
receipt={'method':method,'candidate':str(path),'candidate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_proxy_sha256':source_sha,'rights':'existing original procedural laboratory proxy; source performer likeness not recreated','body_only':True,'frames':360,'fps':60,'retarget':'joint positions, shoulder/hip target widths, median source arm lengths, target limb lengths, analytic two-bone IK with observed knee/elbow bend plane; hemisphere-continuous quaternion baking','hip_height_normalization_scale':global_scale,'arm_length_ratios':ratios,'target_shoulder_width_m':.4,'target_hip_width_m':.2,'max_reach_clamp_m':max(clamps),'max_bone_scale_error':max(errors),'ambiguous_axial_roll_repairs':roll_repairs,'foot_depth_heading_constraint':'front-facing segment only; preserve lateral toe heading, constrain forward Y and floor slope; original depth unresolved','floor_constraints':'source foot targets already contact-corrected; IK reach clamp can invalidate contact; downstream QA required','status':'RECONSTRUCTION_CANDIDATE_NOT_ACCURACY_PASS'}
receipt['retarget']='joint-position normalization, individual upper/lower arm lengths, target shoulder/hip widths; positional arm reconstruction and contact-goal leg IK; parallel-transported twist, hemisphere-continuous baking'
receipt['direction_outlier_repairs']=direction_repairs;receipt['direction_limit_deg_per_60fps_frame']=20;receipt['wrist_orientation']='unobserved; neutral forearm-aligned wrist, not extracted hand orientation'
receipt['head_orientation_scope']=data['head_orientation_scope'];receipt['source_leg_median_length_m']=source_leg_lengths[len(points)//2];receipt['root_scale_method']='target/source leg-chain length normalization; median hip-to-floor scaling rejected because it erased knee-flexion height'
(E/(method+'_retarget.json')).write_text(json.dumps(receipt,indent=2));assert hashlib.sha256(source.read_bytes()).hexdigest()==source_sha;print(json.dumps(receipt,ensure_ascii=True))
