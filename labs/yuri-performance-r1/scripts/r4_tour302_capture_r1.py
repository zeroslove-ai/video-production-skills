"""ONE view source/corrected entire local native phrase, exposed left elbow."""
import bpy,sys,json,hashlib,ast
from pathlib import Path
import numpy as np
from mathutils import Vector
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
from r4_native_tour_adapter_r1 import ACTIONS
def run(view):
 B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/('alpha-tour302-capture-'+view+'-r1');O.mkdir(exist_ok=False);m=json.loads((B/'alpha-tour302-elbow-c1d/TOUR302_ELBOW_C1_PRIVATE.json').read_bytes());old=json.loads((B/'alpha-native-tour-recovery-r2/NATIVE_TOUR_RECOVERY_PRIVATE_R2.json').read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(m['candidate'])==m['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=m['candidate'],use_scripts=False)
 s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];names=list(m['preserved81_signature_private']['actions']);before=snapshot(names);assert before==m['preserved81_signature_private'];tree=ast.parse((H/'r4_existing_reach_contact_closure_r1.py').read_text(encoding='utf8'));ns={'bpy':bpy,'np':np,'fixed':{}};exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='geom'],type_ignores=[]),'<same_actual_mesh>','exec'),ns);geom=ns['geom'];mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4']
 def bind(bodyname):
  lanes=[]
  for ob,an in ACTIONS.items():
   ln=ReactionLane(ob);ln.on(bodyname if ob==r.name else an);lanes.append(ln)
  return lanes
 def off(lanes):
  for ln in reversed(lanes):ln.off()
 lanes=bind(ACTIONS[r.name]);s.frame_set(302);bpy.context.view_layer.update();target=(r.matrix_world@r.pose.bones['forearm.L'].matrix).translation.copy();off(lanes)
 cam=s.camera;cam0=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale);changes=[(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',8),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',384),(s.render,'resolution_y',384),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','PNG'),(s.render.image_settings,'color_mode','RGBA'),(s.render.image_settings,'color_depth','8'),(s.render,'filepath','')];saved=[(o,k,getattr(o,k)) for o,k,_ in changes]
 for o,k,v in changes:setattr(o,k,v)
 cam.data.type='ORTHO';cam.data.ortho_scale=.50;direction=Vector((0,-1,0) if view=='front' else (.6,-1,0));cam.location=target+direction.normalized()*.8;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();camera={'view':view,'target_private':list(target),'location_private':list(cam.location),'scale':.5,'resolution':[384,384],'samples':8,'native_clock':[289,385],'fps':24};rows=[]
 for mode,action in [('ORIGINAL',ACTIONS[r.name]),('CORRECTED',m['corrective_action'])]:
  folder=O/mode;folder.mkdir();lanes=bind(action)
  for ix,f in enumerate(range(289,386)):
   s.frame_set(f);bpy.context.view_layer.update();actual={n:hashlib.sha256(geom(bpy.data.objects[n])[0].tobytes()).hexdigest() for n in mesh_names};expected=old['all_rows_private'][f-1]['actual_mesh_hash_private'] if mode=='ORIGINAL' else m['local_rows_private'][f-288]['actual_mesh_hash_private'];assert actual==expected
   out=folder/f'{ix+1:04}.png';s.render.filepath=str(out);bpy.ops.render.render(write_still=True);rows.append({'mode':mode,'frame':f,'ordinal':ix+1,'file_SHA':sha(out),'actual_geometry_matches_local_oracle':True})
  off(lanes)
 cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale=cam0;s.render.resolution_x=960;s.render.resolution_y=920;s.render.filepath=str(O/'OFF_SOURCE_CAMERA_NEUTRAL.png');bpy.ops.render.render(write_still=True)
 for o,k,v in saved:setattr(o,k,v)
 assert snapshot(names)==before and sha(m['candidate'])==m['candidate_SHA'];(O/'TOUR302_CAPTURE_PRIVATE_R1.json').write_text(json.dumps({'candidate_SHA':m['candidate_SHA'],'source81_OFF_restored':True,'camera':camera,'rows_private':rows},indent=2),encoding='utf8');print('TOUR302_MATCHED_PHRASE_CAPTURE_COMPLETE',view,len(rows),flush=True)
