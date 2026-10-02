"""Compose existing independent proxy action bindings; identical body, changed face/gaze."""
from pathlib import Path
import bpy,json,hashlib,copy
ROOT=Path(__file__).resolve().parents[1];src=ROOT/'evidence/acting-r3-blink';meta=json.loads((src/'build_receipt.json').read_text());registry=json.loads((src/'action_registry.json').read_text())
bpy.ops.wm.open_mainfile(filepath=meta['candidate']);r=bpy.data.objects['ProxyHumanoid'];s=bpy.context.scene
body=next(x for x in registry['greeting_wave']['natural'] if x[0]=='ProxyHumanoid');mix=copy.deepcopy(registry)
for mode,face in [('shy_face','shy_lookaway'),('please_face','please_tilt')]:mix['greeting_wave'][mode]=[body]+[x for x in registry[face]['natural'] if x[0]!='ProxyHumanoid']
for frame in range(1,122):
    matrices=[]
    for mode in ('natural','shy_face','please_face'):
        for o in bpy.data.objects:
            if o.animation_data:o.animation_data.action=None
            if o.type=='MESH' and o.data.shape_keys and o.data.shape_keys.animation_data:o.data.shape_keys.animation_data.action=None
        for owner,name in mix['greeting_wave'][mode]:
            o=bpy.data.objects.get(owner) or bpy.data.shape_keys.get(owner);o.animation_data_create();o.animation_data.action=bpy.data.actions[name]
        s.frame_set(frame);bpy.context.view_layer.update();matrices.append([[list(row) for row in b.matrix] for b in r.pose.bones])
    assert matrices[0]==matrices[1]==matrices[2],frame
out=ROOT/'local/face-mix-r4';e=ROOT/'evidence/face-mix-r4';out.mkdir(exist_ok=True);e.mkdir(exist_ok=True);p=out/'PROXY_FACE_MIX_R4.blend';s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(p))
(e/'action_registry.json').write_text(json.dumps(mix,indent=2));(e/'camera_metadata.json').write_text((src/'camera_metadata.json').read_text())
(e/'build_receipt.json').write_text(json.dumps({**meta,'candidate':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source':meta['candidate'],'source_sha256':meta['sha256'],'new_physical_recipes':0,'comparison':'same greeting body/head; existing smile vs shy vs pleading face/gaze bindings only','all_121_body_matrices_exactly_identical':True,'limitations':'semantic proxy; transplanted timing is a composability proof, not authored emotional coherence or target facial acceptance'},indent=2));print('FACE_MIX_R4_PASS')
