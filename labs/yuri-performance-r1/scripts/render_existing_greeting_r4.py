"""Reproduce existing 6s body action from untouched source with research cameras."""
from pathlib import Path
import bpy,json,math,hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];SOURCE=Path(r'C:\Users\JAEWAN\Downloads\Character_Master_R2_20261002.blend');sha=hashlib.sha256(SOURCE.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(SOURCE));s=bpy.context.scene;r=bpy.data.objects['Armature'];r.hide_set(False)
for o in bpy.data.objects:
    if o.animation_data:o.animation_data.action=None
    if o.type=='MESH' and o.data.shape_keys:
        if o.data.shape_keys.animation_data:o.data.shape_keys.animation_data.action=None
        for k in o.data.shape_keys.key_blocks:
            if k.name!='Basis':k.value=0
h=bpy.data.objects['Character_Body_Head'];h['Face_GazeYaw']=0.;h['Face_GazePitch']=0.;action=bpy.data.actions['MOTION5H_Legacy_Greeting_Wave'];r.animation_data.action=action;r.animation_data.action_slot=next(x for x in action.slots if x.target_id_type=='OBJECT')
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=12;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100
cams=json.loads((ROOT/'evidence/native-camera-r4/build_receipt.json').read_text())['cameras'];out=ROOT/'local/existing-greeting-r4';out.mkdir(exist_ok=True);receipt={'source_sha256':sha,'original_action':action.name,'frame_range':[1,145],'duration_seconds':6,'fps':24,'face':'NEUTRAL ONLY','scope':'existing original motion replay, not newly completed performance','source_rotation_modes':{b.name:b.rotation_mode for b in r.pose.bones},'frames':[]}
for name in ('waist_threequarter','hand_face'):
    c=cams[name];d=bpy.data.cameras.new('Existing reference '+name);o=bpy.data.objects.new(d.name,d);s.collection.objects.link(o);o.location=c['location_m'];o.rotation_euler=(Vector(c['target_m'])-o.location).to_track_quat('-Z','Y').to_euler();d.lens=c['lens_mm'];d.sensor_width=36;s.camera=o
    for frame in (1,37,73,109,145):
        s.frame_set(frame);p=out/name/f'{frame:04d}.png';p.parent.mkdir(exist_ok=True);s.render.filepath=str(p);bpy.ops.render.render(write_still=True);receipt['frames'].append({'camera':name,'frame':frame,'time_seconds':(frame-1)/24,'file':str(p),'root_m':list(r.matrix_world@r.pose.bones['Root'].head),'wrists_m':{side:list(r.matrix_world@r.pose.bones[f'J_Bip_{side}_Hand'].head) for side in ('L','R')}})
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==sha;e=ROOT/'evidence/existing-greeting-r4';e.mkdir(exist_ok=True);(e/'receipt.json').write_text(json.dumps(receipt,indent=2));print('EXISTING_GREETING_REPLAY_PASS')
