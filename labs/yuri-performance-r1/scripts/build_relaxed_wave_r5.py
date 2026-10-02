"""Mapped native finger relaxation over the existing greeting body, separate R&D candidate."""
from pathlib import Path
import bpy,json,math,hashlib,sys
from mathutils import Quaternion
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from acting_recipe import curve
from native_preservation import signature
meta=json.loads((ROOT/'evidence/native-camera-r4/build_receipt.json').read_text());source=Path(meta['candidate']);sha=hashlib.sha256(source.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;r=bpy.data.objects['Armature'];original=list(json.loads((ROOT/'evidence/native-camera-r4/preservation.json').read_text())['before']['actions']);before=signature(original)
source_action=bpy.data.actions[meta['action_registry']['greeting_wave']];new=source_action.copy();new.name='RND_R5_greeting_wave_RELAXED_FINGERS';new.use_fake_user=True;names=[f'J_Bip_R_{finger}{joint}' for finger in ('Index','Middle','Ring','Little') for joint in (1,2,3)];samples=[]
for frame in range(1,122):
    r.animation_data.action=source_action;r.animation_data.action_slot=source_action.slots[0];s.frame_set(frame);bpy.context.view_layer.update();baseline={b.name:b.matrix.copy() for b in r.pose.bones};r.animation_data.action=None
    gain=curve((frame-1)/24,[(0,0),(.4,.15),(.85,.5),(1.7,1),(2.95,1),(3.2,.7),(4.4,0),(5,0)]);palm=r.pose.bones['J_Bip_R_Hand'].matrix.to_3x3().col[2].normalized()
    for finger,amount in [('Index',5),('Middle',7),('Ring',9),('Little',11)]:
        for joint,weight in [(1,.8),(2,1),(3,.7)]:
            b=r.pose.bones[f'J_Bip_R_{finger}{joint}'];axis_world=b.matrix.to_3x3().col[1].normalized().cross(palm).normalized();axis_local=b.matrix.to_quaternion().inverted()@axis_world;b.matrix_basis=b.matrix_basis@Quaternion(axis_local,math.radians(amount*weight*gain)).to_matrix().to_4x4();bpy.context.view_layer.update()
    error=max(abs(b.matrix[i][j]-baseline[b.name][i][j]) for b in r.pose.bones if b.name not in names for i in range(4) for j in range(4));assert error<1e-7,(frame,error)
    r.animation_data.action=new;r.animation_data.action_slot=new.slots[0]
    for name in names:r.pose.bones[name].keyframe_insert('rotation_quaternion',frame=frame,group=name)
    samples.append({'frame':frame,'curl_envelope':gain,'non_finger_matrix_error':error})
for layer in new.layers:
    for strip in layer.strips:
        for bag in strip.channelbags:
            for fc in bag.fcurves:
                for k in fc.keyframe_points:k.interpolation='LINEAR'
assert signature(original)==before and hashlib.sha256(source.read_bytes()).hexdigest()==sha
out=ROOT/'local/native-relaxed-wave-r5';e=ROOT/'evidence/native-relaxed-wave-r5';out.mkdir(exist_ok=True);e.mkdir(exist_ok=True);p=out/'R2_RELAXED_WAVE_R5.blend';s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(p));receipt={**meta,'candidate':str(p),'candidate_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'action_registry':{'greeting_wave':new.name},'source_candidate':str(source),'source_candidate_sha256':sha,'revision':'right finger palm-plane relaxation only; body/head/wrist motion fixed','finger_parameters':{'degrees_by_finger':{'Index':5,'Middle':7,'Ring':9,'Little':11},'joint_weights':[.8,1,.7],'thumb':'unchanged'},'new_physical_base_recipes':0,'original_actions_preserved':66,'non_finger_121frame_matrix_invariant':'PASS','finger_overlay_samples':samples};(e/'build_receipt.json').write_text(json.dumps(receipt,indent=2));(e/'preservation.json').write_text(json.dumps({'result':'PASS','before':before,'after':signature(original)},indent=2));print('RELAXED_WAVE_R5_BUILD_PASS')
