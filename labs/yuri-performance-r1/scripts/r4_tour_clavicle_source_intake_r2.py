"""Readonly source clavicle residual intake: actual surface ownership and natural close views."""
import bpy,sys,json,hashlib,ast,collections
from pathlib import Path
import numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot,props
from r4_appearance_adapter import ReactionLane
from r4_native_tour_adapter_r1 import ACTIONS
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-tour-clavicle-source-intake-r2';O.mkdir(exist_ok=False)
m=json.loads((B/'alpha-native-tour-recovery-r2/NATIVE_TOUR_RECOVERY_PRIVATE_R2.json').read_bytes());res=json.loads((B/'alpha-tour302-residual-localize-c2/RESIDUAL_SURFACE_OWNERSHIP_PRIVATE_C2.json').read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(m['candidate'])==m['candidate_SHA'] and sha(m['source'])==m['source_SHA']
bpy.ops.wm.open_mainfile(filepath=m['candidate'],use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered'];names=list(bpy.data.actions.keys());initial_frame=s.frame_current;before=snapshot(names);assert len(names)==81 and snapshot(list(m['original78_signature_private']['actions']))==m['original78_signature_private']
tree=ast.parse((H/'r4_existing_reach_contact_closure_r1.py').read_text(encoding='utf8'));ns={'bpy':bpy,'np':np,'fixed':{}};exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='geom'],type_ignores=[]),'<same_geom>','exec'),ns);geom=ns['geom'];mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4'];pair=[x['triangle_private'] for x in res['residual_original_weights_private']];ids=sorted({v for tri in pair for v in tri});gn={g.index:g.name for g in body.vertex_groups}
weights={str(i):{gn[g.group]:g.weight for g in body.data.vertices[i].groups} for i in ids};joints=['clavicle.L','neck','upper_arm.L'];rest={n:{'parent':r.data.bones[n].parent.name if r.data.bones[n].parent else None,'matrix_local_private':[list(x) for x in r.data.bones[n].matrix_local],'constraints':[(c.name,c.type,props(c)) for c in r.pose.bones[n].constraints]} for n in joints};modifiers=[props(x) for x in body.modifiers]
def bind():
 lanes=[]
 for ob,an in ACTIONS.items():ln=ReactionLane(ob);ln.on(an);lanes.append(ln)
 return lanes
def off(lanes):
 for ln in reversed(lanes):ln.off()
rawbody=body.data;raw=np.array([v.co[:] for v in rawbody.vertices],dtype=np.float64);offgeom=geom(body)[0];rows=[];lanes=bind()
for f in [1,289,302,303,337,370,371,385,472]:
 s.frame_set(f);bpy.context.view_layer.update();data={n:geom(bpy.data.objects[n])[0] for n in mesh_names};hh={n:hashlib.sha256(v.tobytes()).hexdigest() for n,v in data.items()};assert hh==m['all_rows_private'][f-1]['actual_mesh_hash_private'];rows.append({'frame':f,'actual_mesh_SHA_private':hh,'pair_vertices_private':data[body.name][ids].tolist(),'joint_local_pose_private':{n:{'rotation_mode':r.pose.bones[n].rotation_mode,'location':list(r.pose.bones[n].location),'quaternion':list(r.pose.bones[n].rotation_quaternion),'scale':list(r.pose.bones[n].scale)} for n in joints}})
s.frame_set(337);bpy.context.view_layer.update();p=geom(body)[0][ids];target=Vector(p.mean(axis=0));off(lanes)
cam=s.camera;cam0=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale);changes=[(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',16),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',512),(s.render,'resolution_y',512),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','PNG'),(s.render.image_settings,'color_mode','RGBA'),(s.render.image_settings,'color_depth','8'),(s.render,'filepath','')];saved=[(o,k,getattr(o,k)) for o,k,_ in changes]
for o,k,v in changes:setattr(o,k,v)
captures=[]
for view,direction in [('front',(0,-1,0)),('quarter',(.6,-1,0))]:
 cam.data.type='ORTHO';cam.data.ortho_scale=.22;cam.location=target+Vector(direction).normalized()*.8;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
 for mode in ['OFF','SOURCE_ON']:
  lanes=bind() if mode=='SOURCE_ON' else []
  for f in [302,303,337,370]:
   s.frame_set(f);bpy.context.view_layer.update();out=O/f'{view}_{mode}_f{f}.png';s.render.filepath=str(out);bpy.ops.render.render(write_still=True);pts=geom(body)[0];projected={str(i):list(world_to_camera_view(s,cam,Vector(pts[i]))) for i in ids};captures.append({'view':view,'mode':mode,'frame':f,'file':str(out),'SHA':sha(out),'pair_projection_private':projected})
  if lanes:off(lanes)
s.frame_set(initial_frame);bpy.context.view_layer.update();cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale=cam0;s.cycles.samples=8;s.render.resolution_x=960;s.render.resolution_y=920;s.render.filepath=str(O/'OFF_SOURCE_CAMERA_NEUTRAL.png');bpy.ops.render.render(write_still=True)
for o,k,v in saved:setattr(o,k,v)
assert snapshot(names)==before and sha(m['candidate'])==m['candidate_SHA'] and sha(m['source'])==m['source_SHA']
(O/'CLAVICLE_SOURCE_INTAKE_PRIVATE_R1.json').write_text(json.dumps({'source_SHA':m['source_SHA'],'source_native_candidate_SHA':m['candidate_SHA'],'source81_OFF_restored':True,'candidate_created':False,'pair_private':pair,'vertex_ids_private':ids,'raw_vertices_private':raw[ids].tolist(),'OFF_evaluated_vertices_private':offgeom[ids].tolist(),'weights_private':weights,'rest_constraints_private':rest,'modifiers_private':modifiers,'rows_private':rows,'captures_private':captures,'capture_camera_target_private':list(target),'capture_scale':.22,'cpu_samples':16},indent=2),encoding='utf8');print('CLAVICLE_SOURCE_READONLY_INTAKE_9FRAMES_16CAPTURES_COMPLETE',flush=True)
