"""Read/reproduce existing greeting actions before selecting reusable source motion."""
from pathlib import Path
import bpy,json,math,hashlib
ROOT=Path(__file__).resolve().parents[1];SOURCE=Path(r'C:\Users\JAEWAN\Downloads\Character_Master_R2_20261002.blend')
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));s=bpy.context.scene;r=bpy.data.objects['Armature'];r.hide_set(False);reports=[]
for a in bpy.data.actions:
    if 'Greeting_Wave' not in a.name:continue
    slots=[x for x in a.slots if x.target_id_type=='OBJECT']
    if not slots:
        reports.append({'action':a.name,'target_slots':[(x.identifier,x.target_id_type) for x in a.slots],'scope':'not an armature action; excluded from body replay'})
        continue
    r.animation_data.action=a;r.animation_data.action_slot=slots[0]
    start,end=a.frame_range;points=[];matrices=[]
    for frame in range(int(start),int(end)+1):
        s.frame_set(frame);bpy.context.view_layer.update();matrices.append({b.name:b.matrix.copy() for b in r.pose.bones})
        points.append({'frame':frame,'hands_m':{side:list(r.matrix_world@r.pose.bones[f'J_Bip_{side}_Hand'].head) for side in ('L','R')}})
    maxstep=max(math.degrees(min(q,p)) for m,n in zip(matrices,matrices[1:]) for name in m for q in [m[name].to_quaternion().rotation_difference(n[name].to_quaternion()).angle] for p in [2*math.pi-q])
    reports.append({'action':a.name,'frame_range':[start,end],'source_scene_fps':s.render.fps,'duration_seconds':(end-start)/s.render.fps,'max_rotation_step_deg_per_frame':maxstep,'hand_samples':points,'scope':'read-only existing motion; no face/skin/action edits; not visual acceptance'})
out=ROOT/'evidence/existing-greeting-r3';out.mkdir(exist_ok=True);(out/'inspection.json').write_text(json.dumps({'source':str(SOURCE),'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'actions':reports},indent=2));print([{k:v for k,v in x.items() if k!='hand_samples'} for x in reports])
