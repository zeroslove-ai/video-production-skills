"""Capture-only proper Action bindings; exact same old/new one-pose candidates."""
import bpy,sys,json,hashlib,ast,math
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
from r4_sit_stand_adapter_r1 import SitStandLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');P=B/'alpha-sit-stand-frame8-constraint-r1';O=B/'alpha-sit-stand-frame8-capture-repair-r1b';O.mkdir(exist_ok=False);m=json.loads((P/'FRAME8_NATIVE_CONSTRAINT_PRIVATE_R1.json').read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(m['candidate'])==m['candidate_SHA'] and sha(m['library'])==m['library_SHA'];bpy.ops.wm.open_mainfile(filepath=m['candidate'],use_scripts=False);s=bpy.context.scene;names=list(m['original78_signature_private']['actions']);before=snapshot(names);assert before==m['original78_signature_private']
oldlib=B/'alpha-sit-stand-source-candidate-r1/YURI_R4_SIT_STAND_ACTIONS_ONLY_R1.blend';assert sha(oldlib)=='a423f2ef52eac9d8af935a382b655cf272ea91607d548fb70910f679fac2b1a6'
with bpy.data.libraries.load(str(oldlib),link=False) as (src,dst):dst.actions=src.actions
for fn,defs in [('r4_native_walk_source_supply_r1.py',['contact']),('r4_existing_reach_contact_closure_r1.py',['geom'])]:
 tree=ast.parse((H/fn).read_text(encoding='utf8'));exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in defs],type_ignores=[]),'<pinned_same_one_pose>','exec'))
fixed={};mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4']
def evaluate():return {n:geom(bpy.data.objects[n]) for n in mesh_names}
base,_=contact(evaluate());cam=s.camera;savecam=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale);settings=[(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',8),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',384),(s.render,'resolution_y',384),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','PNG'),(s.render.image_settings,'color_mode','RGBA'),(s.render,'filepath','')];saved=[(o,k,getattr(o,k)) for o,k,_ in settings]
for o,k,v in settings:setattr(o,k,v)
receipt=[]
for label in ['old','constraint']:
 if label=='old':lane=SitStandLane();lane.on();s.frame_set(8);lanes=[lane]
 else:
  lanes=[]
  for ob in ['Meshy_Fitted_Rig','Armature','Hair_Rig_R4']:
   ln=ReactionLane(ob);ln.on('YURI_R4_SIT_FRAME8_NATIVE_CONSTRAINT_'+ob);lanes.append(ln)
  s.frame_set(1)
 bpy.context.view_layer.update();data=evaluate();ps,_=contact(data);expected={k:{tuple(tuple(t) for t in pair) for pair in v} for k,v in m['all_old_new_pair_identities_private'][label].items()};assert all(ps[k]-base[k]==v for k,v in expected.items()),'Proper bound pose must reproduce exact measured triangle identities'
 hashes={n:hashlib.sha256(v[0].tobytes()).hexdigest() for n,v in data.items()}
 for view,direction in [('front',(0,-1,0)),('quarter',(.6,-1,0)),('side',(1,0,0))]:
  target=Vector((.002,.02,.48));cam.data.type='ORTHO';cam.data.ortho_scale=1.18;cam.location=target+Vector(direction).normalized()*.8;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();s.render.filepath=str(O/(label+'_'+view+'.png'));bpy.ops.render.render(write_still=True);after=evaluate();assert all(hashlib.sha256(after[n][0].tobytes()).hexdigest()==h for n,h in hashes.items());receipt.append({'label':label,'view':view,'bound_frame':8 if label=='old' else 1,'file_SHA':sha(s.render.filepath),'all_actual_mesh_before_after_render_equal':True,'exact_measured_old_new_surface_pair_identities_reproduced':True,'actual_mesh_SHA_private':hashes})
 for ln in reversed(lanes):ln.off()
cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale=savecam
for o,k,v in saved:setattr(o,k,v)
assert snapshot(names)==before
for o,k,v in settings:setattr(o,k,v)
s.render.resolution_x=960;s.render.resolution_y=920;s.render.filepath=str(O/'OFF_SOURCE_CAMERA_NEUTRAL.png');bpy.ops.render.render(write_still=True)
for o,k,v in saved:setattr(o,k,v)
assert snapshot(names)==before and sha(m['candidate'])==m['candidate_SHA'] and sha(m['library'])==m['library_SHA'];(O/'FRAME8_CAPTURE_REPAIR_PRIVATE_R1.json').write_text(json.dumps({'same_candidate_SHA':m['candidate_SHA'],'same_library_SHA':m['library_SHA'],'original78_OFF_equal':True,'capture_receipts':receipt,'one_pose_only_no_authoring_repeated':True,'first_visual_capture_failure':'Manual pose assignment was overridden by bound Action reevaluation: old/new decoded384RGBA identical. Preserved; excluded as evidence.'},indent=2),encoding='utf8');print('FRAME8_PROPER_BINDING_CAPTURE_COMPLETE',flush=True)
