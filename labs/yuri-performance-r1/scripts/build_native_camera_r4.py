"""Assemble selected body-only references and isolate a camera framing correction."""
from pathlib import Path
import bpy,json,sys,hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from native_preservation import signature
base=json.loads((ROOT/'evidence/native-body-r3/build_receipt.json').read_text());elbow=json.loads((ROOT/'evidence/native-body-r3-please-elbow/build_receipt.json').read_text())
bpy.ops.wm.open_mainfile(filepath=base['candidate']);original=list(json.loads((ROOT/'evidence/native-body-r3/preservation.json').read_text())['digests']['actions'])
before=signature(original);s=bpy.context.scene;r=bpy.data.objects['Armature'];action_name=base['action_registry']['please_tilt'];r.animation_data.action=None;bpy.data.actions.remove(bpy.data.actions[action_name])
with bpy.data.libraries.load(elbow['candidate'],link=False) as (src,dst):dst.actions=[action_name]
assert bpy.data.actions.get(action_name);bpy.data.actions[action_name].use_fake_user=True
cams=base['cameras'];camera=bpy.data.objects[cams['waist_threequarter']['object']]
camera.location=(1.15,-1.4,1.0);target=Vector((0,0,.83));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.lens=85
cams['waist_threequarter'].update({'location_m':list(camera.location),'target_m':list(target),'rotation_euler':list(camera.rotation_euler),'lens_mm':85,'revision':'true ~39 degree threequarter; waist-up target; rendered silhouette still required'})
assert before==signature(original)
out=ROOT/'local/native-camera-r4';e=ROOT/'evidence/native-camera-r4';out.mkdir(exist_ok=True);e.mkdir(exist_ok=True);p=out/'R2_NATIVE_CAMERA_R4.blend'
r.animation_data.action=bpy.data.actions[base['action_registry']['greeting_wave']];s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(p))
receipt={**base,'candidate':str(p),'candidate_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'cameras':cams,'revision':'selected greeting/shy baseline + please elbow correction; waist camera only correction','inputs':[{'candidate':base['candidate'],'sha256':base['candidate_sha256'],'clips':['greeting_wave','shy_lookaway']},{'candidate':elbow['candidate'],'sha256':elbow['candidate_sha256'],'clips':['please_tilt']}],'selected_body_quality':'RESEARCH_CANDIDATE; wrist ingress/recovery remaining defect'}
receipt['clips']=[x for x in base['clips'] if x['clip']!='please_tilt']+[x for x in elbow['clips'] if x['clip']=='please_tilt'];receipt['max_ik_error_m']=max(base['max_ik_error_m'],elbow['max_ik_error_m'])
(e/'build_receipt.json').write_text(json.dumps(receipt,indent=2));(e/'preservation.json').write_text(json.dumps({'before':before,'after':signature(original),'result':'PASS'},indent=2));print('NATIVE_CAMERA_R4',receipt['candidate_sha256'])
