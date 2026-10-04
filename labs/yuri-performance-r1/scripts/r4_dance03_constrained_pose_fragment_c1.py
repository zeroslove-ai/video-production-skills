# ONE source-native constrained03 solution; no sweeps or generic IK framework.
existing=json.loads((B/'dance03-existing-solutions-inspect-c1/EXISTING_NATIVE_SOLUTIONS_PRIVATE_C1.json').read_bytes())
walk=next(x for x in existing['rows'] if x['action']=='MESHY_R2_BODY_WalkInPlace')
leg_source=next(x for x in walk['key_frames'] if x['frame']==39)
reach=next(x for x in existing['rows'] if x['action']=='MESHY_R2_BODY_Reach')
hinge_source=next(x for x in reach['key_frames'] if x['frame']==77)['bones']['forearm.L']
native_hinge=Vector(hinge_source['axis']).normalized()
oldlib=B/'dance-two-pose-native-r1/YURI_R4_DANCE_STATIC03_16_ACTIONS_ONLY_R1.blend'
oldlib_sha=sha(oldlib)
with bpy.data.libraries.load(str(oldlib),link=False) as (aa,bb):bb.actions=['YURI_R4_DANCE_STATIC_03_BODY_R1']
oldright=bb.actions[0]
oldright_q={}
for n in ['upper_arm.R','forearm.R']:
 path='pose.bones["'+n+'"].rotation_quaternion'
 cs={f.array_index:f for l in oldright.layers for st in l.strips for ba in st.channelbags for f in ba.fcurves if f.data_path==path}
 oldright_q[n]=Quaternion([cs[j].evaluate(1) for j in range(4)])
bpy.data.actions.remove(oldright)
assert snapshot(names)==before
constraint={}
def set_pose(pid):
 assert pid=='03'
 # Reuse exact existing Walk39 LEFT thigh/shin/foot solution; source pelvis/root and RIGHT leg stay untouched.
 for n in ['thigh.L','shin.L','foot.L']:r.pose.bones[n].rotation_quaternion=Quaternion(leg_source['bones'][n]['q'])
 for n,q in oldright_q.items():r.pose.bones[n].rotation_quaternion=q
 update()
 shoulder=worldpoint('upper_arm.L');l1=(worldpoint('upper_arm.L',True)-shoulder).length;l2=(worldpoint('forearm.L',True)-worldpoint('forearm.L')).length
 target=Vector((.025,-.220,.700));pole=Vector((.170,-.105,.650));delta=target-shoulder;dist=delta.length;u=delta.normalized()
 assert abs(l1-l2)+.005<dist<l1+l2-.005
 along=(l1*l1-l2*l2+dist*dist)/(2*dist);height=math.sqrt(max(0,l1*l1-along*along));p=pole-shoulder;p=(p-u*p.dot(u)).normalized();elbow=shoulder+u*along+p*height
 ud=(elbow-shoulder).normalized();fd=(target-elbow).normalized();normal=ud.cross(fd).normalized()
 aim('upper_arm.L',ud)
 axis=(r.matrix_world.to_3x3()@r.pose.bones['forearm.L'].matrix.to_3x3()@native_hinge).normalized()
 axisproj=(axis-ud*axis.dot(ud)).normalized()
 # Explicit bounded upper-arm axial twist to align the native elbow hinge with the pole plane.
 twist=math.atan2(ud.dot(axisproj.cross(normal)),axisproj.dot(normal));bound=math.radians(35);applied=max(-bound,min(bound,twist));axisrotate('upper_arm.L',ud,math.degrees(applied))
 current=(worldpoint('forearm.L',True)-worldpoint('forearm.L')).normalized();axis=(r.matrix_world.to_3x3()@r.pose.bones['forearm.L'].matrix.to_3x3()@native_hinge).normalized()
 bend=math.atan2(axis.dot(current.cross(fd)),current.dot(fd));bnd=math.radians(85);clamped=max(-bnd,min(bnd,bend))
 r.pose.bones['forearm.L'].rotation_quaternion=Quaternion(native_hinge,clamped);update()
 actual_elbow=worldpoint('forearm.L');actual_wrist=worldpoint('forearm.L',True)
 constraint.update({'native_two_bone_lengths_m':[l1,l2],'target_world_m':list(target),'pole_world_m':list(pole),'analytic_elbow_world_m':list(elbow),'actual_elbow_world_m':list(actual_elbow),'actual_wrist_world_m':list(actual_wrist),'target_distance_m':dist,'actual_wrist_target_error_m':(actual_wrist-target).length,'native_elbow_hinge_axis_from_Reach77':list(native_hinge),'requested_upper_axial_twist_degrees':math.degrees(twist),'applied_upper_axial_twist_degrees':math.degrees(applied),'upper_axial_twist_bound_degrees':35,'requested_elbow_bend_degrees':math.degrees(bend),'applied_elbow_bend_degrees':math.degrees(clamped),'elbow_bend_bound_degrees':85,'existing_leg_source':'MESHY_R2_BODY_WalkInPlace39 exact3quaternions; pelvis/root/lowerRIGHT unchanged','existing_leg_delta_degrees':{n:leg_source['bones'][n]['delta_deg'] for n in ['thigh.L','shin.L','foot.L']},'right_arm_previous03_quaternions_exact':True,'one_candidate_no_sweep':True})
 update()
