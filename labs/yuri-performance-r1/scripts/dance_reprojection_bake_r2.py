"""Bake solver positions into a private MotionBERT-derived normalized rig."""
from pathlib import Path
import bpy,json,hashlib,sys
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[1];E=R/'evidence/dance-benchmark-r1';L=R/'local/dance-benchmark-r1';stable='stable' in sys.argv;method='motionbert_reprojection_stable' if stable else 'motionbert_reprojection';source=L/'motionbert_DANCE_R1.blend';sha=hashlib.sha256(source.read_bytes()).hexdigest();solution=json.loads((E/('arm_reprojection_r2_stable.json' if stable else 'arm_reprojection_r2.json')).read_text());assert sha==solution['base_candidate_sha256']
bpy.ops.wm.open_mainfile(filepath=str(source));rig=bpy.data.objects['ProxyHumanoid'];s=bpy.context.scene;base=rig.animation_data.action;action=base.copy();action.name='DANCE_R2_ARM_REPROJECTION';action.use_fake_user=True
poses=[]
for fi in range(360):
    s.frame_set(fi+1);poses.append({b.name:b.matrix.copy() for b in rig.pose.bones})
rig.animation_data.action=action
if action.slots:rig.animation_data.action_slot=action.slots[0]
previous={};rolls={};maxerr=0.
def matrix(pos,axis,name):
    y=axis.normalized();x=rolls.get(name,poses[0][name].to_3x3().col[0]).copy();x-=y*x.dot(y)
    if x.length<1e-5:x=Vector((0,1,0)).cross(y)
    x.normalize();rolls[name]=x.copy();z=x.cross(y).normalized();return Matrix.Translation(pos)@Matrix((x,y,z)).transposed().to_4x4()
for fi in range(360):
    s.frame_set(fi+1)
    for b in rig.pose.bones:b.matrix=poses[fi][b.name]
    for side_solution in solution['solutions']:
        side=side_solution['side'];p=side_solution['frames'][fi];sh,el,wr=[Vector(p[k]) for k in ['shoulder','elbow','wrist']]
        for n,pos,axis in [('upper_arm.'+side,sh,el-sh),('forearm.'+side,el,wr-el),('hand.'+side,wr,wr-el)]:
            b=rig.pose.bones[n];b.matrix=matrix(pos,axis,n);bpy.context.view_layer.update();q=b.rotation_quaternion.copy()
            if n in previous and previous[n].dot(q)<0:q.negate();b.rotation_quaternion=q
            previous[n]=q.copy()
            for key in ['location','rotation_quaternion','scale']:b.keyframe_insert(key,frame=fi+1,group=n)
        maxerr=max(maxerr,(rig.pose.bones['hand.'+side].head-wr).length)
s.frame_set(1);path=L/(method+'_DANCE_R1.blend');bpy.ops.wm.save_as_mainfile(filepath=str(path))
bpy.ops.object.select_all(action='DESELECT');rig.select_set(True)
for o in bpy.data.objects:
    if o.type=='MESH' and any(m.type=='ARMATURE' and m.object==rig for m in o.modifiers):o.select_set(True)
bpy.context.view_layer.objects.active=rig;bpy.ops.export_scene.gltf(filepath=str(L/(method+'_DANCE_R1.glb')),use_selection=True,export_animations=True,export_animation_mode='ACTIVE_ACTIONS',export_frame_range=True,export_force_sampling=True)
meta=json.loads((E/'motionbert_retarget.json').read_text());meta.update({'method':method,'candidate':str(path),'candidate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'base_candidate_sha256':sha,'arm_reprojection_summary':solution['summary'],'max_baked_wrist_position_error_m':maxerr,'retarget':'original normalized rig and body/root/legs/head; arms optimized against fixed2D camera with target bone lengths','status':'REPROJECTION_EXPERIMENT_NOT_WORLD_ACCURACY_PASS'})
(E/(method+'_retarget.json')).write_text(json.dumps(meta,indent=2));assert hashlib.sha256(source.read_bytes()).hexdigest()==sha;print(json.dumps({'candidate':str(path),'sha256':meta['candidate_sha256'],'max_wrist_bake_error_m':maxerr}))
