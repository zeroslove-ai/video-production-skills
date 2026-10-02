"""Compare naive local-X curl to per-joint anatomical palm-plane axes.
Transient pose experiments only; original skin/rest rig/actions/source candidates untouched.
"""
from pathlib import Path
import bpy,json,math,hashlib,sys,numpy as np
from mathutils import Vector,Quaternion
ROOT=Path(__file__).resolve().parents[1];meta=json.loads((ROOT/'evidence/native-camera-r4/build_receipt.json').read_text());source=Path(meta['candidate']);sha=hashlib.sha256(source.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;r=bpy.data.objects['Armature'];r.animation_data.action=bpy.data.actions[meta['action_registry']['greeting_wave']];r.animation_data.action_slot=r.animation_data.action.slots[0];s.frame_set(49);bpy.context.view_layer.update();baseline={b.name:b.matrix_basis.copy() for b in r.pose.bones};r.animation_data.action=None
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=16;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=640;s.render.resolution_y=480;s.render.resolution_percentage=100
wide='wide' in sys.argv;folder='finger-calibration-r4-wide' if wide else 'finger-calibration-r4';out=ROOT/'local'/folder;out.mkdir(exist_ok=True);reports=[]
def evaluated_mesh_xyz():
    mesh=bpy.data.objects['Character_Body_Head'].evaluated_get(bpy.context.evaluated_depsgraph_get()).data;xyz=np.empty(len(mesh.vertices)*3,np.float32);mesh.vertices.foreach_get('co',xyz);return xyz.reshape(-1,3)
baseline_mesh=evaluated_mesh_xyz().copy()
for side in ('R','L'):
    hand=r.pose.bones['J_Bip_'+side+'_Hand'];palm=hand.matrix.to_3x3().col[2].normalized();names=[f'J_Bip_{side}_{finger}{joint}' for finger in ('Index','Middle','Ring','Little') for joint in (1,2,3)]
    centre=r.matrix_world@((hand.head+sum((r.pose.bones[n].tail for n in names),Vector())/len(names))*.5)
    data=bpy.data.cameras.new('Finger diagnostic '+side);camera=bpy.data.objects.new(data.name,data);s.collection.objects.link(camera);data.type='ORTHO';data.ortho_scale=.24 if wide else .15;camera.location=centre+(r.matrix_world.to_3x3()@palm)*.4+Vector((0,0,.03));camera.rotation_euler=(centre-camera.location).to_track_quat('-Z','Y').to_euler();s.camera=camera
    for case,amount,mapped in [('open',0,True),('naive_x_15',15,False),('palm_plane_15',15,True),('palm_plane_25',25,True)]:
        for b in r.pose.bones:b.matrix_basis=baseline[b.name]
        bpy.context.view_layer.update();start={finger:list(r.pose.bones[f'J_Bip_{side}_{finger}3'].tail) for finger in ('Index','Middle','Ring','Little')};axes={}
        for name in names:
            b=r.pose.bones[name];world_axis=b.matrix.to_3x3().col[1].normalized().cross(palm).normalized();axis=b.matrix.to_quaternion().inverted()@world_axis if mapped else Vector((1,0,0));axes[name]=list(axis);b.matrix_basis=b.matrix_basis@Quaternion(axis,math.radians(amount)).to_matrix().to_4x4();bpy.context.view_layer.update()
        tips={finger:list(r.pose.bones[f'J_Bip_{side}_{finger}3'].tail) for finger in ('Index','Middle','Ring','Little')};toward={finger:(Vector(tips[finger])-Vector(start[finger])).dot(palm) for finger in tips};p=out/f'{side}__{case}.png';s.render.filepath=str(p);bpy.ops.render.render(write_still=True)
        delta=np.linalg.norm(evaluated_mesh_xyz()-baseline_mesh,axis=1)
        reports.append({'side':side,'case':case,'degrees_per_joint':amount,'axis_local':axes,'fingertip_displacement_toward_palm_m':toward,'all_four_fingers_bend_toward_palm':all(v>0 for v in toward.values()) if amount else None,'evaluated_skin_max_delta_m_after_render':float(delta.max()),'skin_vertices_moved_over_1mm':int((delta>.001).sum()),'image':str(p),'camera_ortho_scale':data.ortho_scale,'thumb':'unchanged; no opposition/contact gesture claim'})
assert hashlib.sha256(source.read_bytes()).hexdigest()==sha;e=ROOT/'evidence'/folder;e.mkdir(exist_ok=True);(e/'receipt.json').write_text(json.dumps({'source_candidate_sha256':sha,'source_frame':49,'original_66_actions_skin_rest_rig_changes':0,'cases':reports,'scope':'axis calibration reference only; no finger-heart/new signature completion'},indent=2));print('FINGER_CALIBRATION_R4_DONE')
