"""Only ranked Tour elbow/wrist defects, matched OFF/ON native close views."""
import bpy,sys,json,hashlib,ast
from pathlib import Path
import numpy as np
from mathutils import Vector
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_native_tour_adapter_r1 import NativeTourLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
O=B/'alpha-native-tour-close-defects-r1';O.mkdir(exist_ok=False)
m=json.loads((B/'alpha-native-tour-recovery-r2/NATIVE_TOUR_RECOVERY_PRIVATE_R2.json').read_bytes())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(m['candidate'])==m['candidate_SHA']
bpy.ops.wm.open_mainfile(filepath=m['candidate'],use_scripts=False)
s=bpy.context.scene;names=list(m['original78_signature_private']['actions']);before=snapshot(names);assert before==m['original78_signature_private']
module=ast.parse((H/'r4_existing_reach_contact_closure_r1.py').read_text(encoding='utf8'));ns={'bpy':bpy,'np':np,'fixed':{}}
exec(compile(ast.Module(body=[x for x in module.body if isinstance(x,ast.FunctionDef) and x.name=='geom'],type_ignores=[]),'<actualmesh>','exec'),ns)
geom=ns['geom'];mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4']
cam=s.camera;savecam=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale)
changes=[(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',8),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',512),(s.render,'resolution_y',512),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','PNG'),(s.render.image_settings,'color_mode','RGBA'),(s.render.image_settings,'color_depth','8'),(s.render,'filepath','')]
saved=[(o,k,getattr(o,k)) for o,k,_ in changes]
for o,k,v in changes:setattr(o,k,v)
rows=[];rig=bpy.data.objects['Meshy_Fitted_Rig']
for f,bone,label in [(302,'forearm.L','LEFT_ELBOW'),(472,'hand.L','LEFT_WRIST'),(472,'hand.R','RIGHT_WRIST')]:
 ln=NativeTourLane();ln.on();s.frame_set(f);bpy.context.view_layer.update()
 actual={n:hashlib.sha256(geom(bpy.data.objects[n])[0].tobytes()).hexdigest() for n in mesh_names};assert actual==m['all_rows_private'][f-1]['actual_mesh_hash_private']
 target=(rig.matrix_world@rig.pose.bones[bone].matrix).translation.copy();ln.off()
 for view,direction in [('front',(0,-1,0)),('quarter',(.6,-1,0))]:
  cam.data.type='ORTHO';cam.data.ortho_scale=.23;cam.location=target+Vector(direction).normalized()*.8;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
  for state in ['OFF','ON']:
   if state=='ON':ln=NativeTourLane();ln.on();s.frame_set(f);bpy.context.view_layer.update();assert {n:hashlib.sha256(geom(bpy.data.objects[n])[0].tobytes()).hexdigest() for n in mesh_names}==actual
   path=O/f'{label}_{view}_f{f}_{state}.png';s.render.filepath=str(path);bpy.ops.render.render(write_still=True)
   rows.append({'frame':f,'region':label,'view':view,'state':state,'file':str(path),'SHA':sha(path),'camera_target_private':list(target),'camera_location_private':list(cam.location),'ortho_scale':.23,'resolution':[512,512]})
   if state=='ON':ln.off()
cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale=savecam
for o,k,v in saved:setattr(o,k,v)
assert snapshot(names)==before and sha(m['candidate'])==m['candidate_SHA']
(O/'MATCHED_DEFECT_CAPTURE_PRIVATE_R1.json').write_text(json.dumps({'candidate_SHA':m['candidate_SHA'],'source78_OFF_restored':True,'rows_private':rows,'no_authoring_no_source_save':True},indent=2),encoding='utf8')
print('TOUR_RANKED_DEFECT_CLOSE_COMPLETE',len(rows),flush=True)
