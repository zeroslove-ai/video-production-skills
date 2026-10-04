"""One constant sole-floor correction in copied A1 Action; original/R2 retained."""
import bpy,sys,json,hashlib
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'alpha-a1-idle-candidate-r3';OUT.mkdir(exist_ok=False)
OLD=BASE/'alpha-a1-idle-candidate-r2/Character_R4_A1_Female_Idle_BODY_CANDIDATE_OFF_R2_20261004.blend'
assert hashlib.sha256(OLD.read_bytes()).hexdigest()=='7c2f28066f3aeff655bec3879b26c4737dd685dc12b2dd8d3ed0e281e85c7743'
contact=json.loads((BASE/'alpha-a1-contact-qa-r2/A1_CONTACT_QA_PRIVATE_R2.json').read_bytes())
offset=min(contact['soles'][side]['min_z_offset_to_source_floor_m'] for side in ['L','R'])
assert 0<offset<.01
bpy.ops.wm.open_mainfile(filepath=str(OLD),use_scripts=False);original=[a.name for a in bpy.data.actions];before=snapshot(original)
r=bpy.data.objects['Meshy_Fitted_Rig'];p=r.data.bones['pelvis'];a=bpy.data.actions['YURI_R4_A1_Female_Idle_BODY_CANDIDATE_R2'].copy();a.name='YURI_R4_A1_Female_Idle_BODY_CANDIDATE_R3';a.use_fake_user=True
a['source_fps']=30.0;a['root_policy']='In-place original root; normalized donor pelvis first-frame displacement with constant sole-floor cleanup';a['floor_cleanup_world_z_m']=-offset
delta=p.matrix_local.to_quaternion().inverted()@r.matrix_world.to_quaternion().inverted()@Vector((0,0,-offset))/r.matrix_world.to_scale().x
changed=0
for layer in a.layers:
    for strip in layer.strips:
        for bag in strip.channelbags:
            for fc in bag.fcurves:
                if fc.data_path=='pose.bones["pelvis"].location':
                    for k in fc.keyframe_points:
                        k.co.y+=delta[fc.array_index];k.handle_left.y+=delta[fc.array_index];k.handle_right.y+=delta[fc.array_index]
                    fc.update();changed+=1
assert changed==3 and before==snapshot(original)
dest=OUT/'Character_R4_A1_Female_Idle_BODY_CANDIDATE_OFF_R3_20261004.blend';bpy.ops.wm.save_as_mainfile(filepath=str(dest))
receipt=json.loads((BASE/'alpha-a1-idle-candidate-r2/A1_RETARGET_RECEIPT_PRIVATE_R1.json').read_bytes())
receipt.update(candidate=str(dest),candidate_bytes=dest.stat().st_size,candidate_SHA=hashlib.sha256(dest.read_bytes()).hexdigest(),action=a.name,floor_or_IK_cleanup_applied=True,floor_cleanup_world_z_m=-offset,source_scene_fps_preserved=24,action_source_fps_embedded=30,previous_candidate_preserved=str(OLD),gate='R3 CANDIDATE; revalidation required')
with (OUT/'A1_RETARGET_RECEIPT_PRIVATE_R1.json').open('x') as f:json.dump(receipt,f,indent=2)
print('A1_R3_FLOOR_CLEANUP_SAVED',receipt['candidate_SHA'],receipt['candidate_bytes'],offset,flush=True)
