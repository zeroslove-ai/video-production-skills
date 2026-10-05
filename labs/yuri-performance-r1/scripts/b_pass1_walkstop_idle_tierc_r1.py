"""PASS1 ONE missing B walk-boundary -> native Idle transition, explicit Tier-C placeholder."""
import bpy,sys,json,hashlib,ast,math
from pathlib import Path
import numpy as np
from mathutils import Matrix,Vector
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'b-pass1-walkstop-idle-tierc-r1';O.mkdir(exist_ok=False);source=Path('C:/Users/JAEWAN/scratch/YURI_COMMON_MOTION_CURATION_R1/provisional-first4-r1/target-reference/Character_Master_NeckSkin_R4.blend');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(source)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa';bpy.ops.wm.open_mainfile(filepath=str(source),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];names=list(bpy.data.actions.keys());before=snapshot(names);assert len(names)==78
ns={'bpy':bpy,'np':np,'fixed':{}};tree=ast.parse((H/'r4_existing_reach_contact_closure_r1.py').read_text(encoding='utf8'));exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='geom'],type_ignores=[]),'<same_geom>','exec'),ns);geom=ns['geom'];mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4']
walk=bpy.data.actions['MESHY_R2_BODY_WalkInPlace'];idle=bpy.data.actions['MESHY_R2_BODY_Idle'];walk_name=walk.name;idle_name=idle.name;curves=[f for l in walk.layers for st in l.strips for ba in st.channelbags for f in ba.fcurves];bones=sorted({f.data_path.split('"')[1] for f in curves if f.data_path.startswith('pose.bones[')});assert len(bones)==52
head_ref=r.matrix_world@r.pose.bones['head'].matrix;rigrefs={ob:bpy.data.objects[ob].matrix_world@bpy.data.objects[ob].pose.bones[bn].matrix for ob,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]}
def source_pose(action,frame):
 ln=ReactionLane();ln.on(action);s.frame_set(frame);bpy.context.view_layer.update();p={n:(r.pose.bones[n].location.copy(),r.pose.bones[n].rotation_quaternion.copy()) for n in bones};body=geom(bpy.data.objects[mesh_names[0]])[0].copy();ln.off();return p,body
start,startv=source_pose(walk.name,97);end,endv=source_pose(idle.name,1);assert snapshot(names)==before
A={'Meshy_Fitted_Rig':'YURI_R4_B_WALKSTOP_IDLE_TIERC_BODY_R1','Armature':'YURI_R4_B_WALKSTOP_IDLE_TIERC_HEAD_R1','Hair_Rig_R4':'YURI_R4_B_WALKSTOP_IDLE_TIERC_HAIR_R1'}
for ob,an in A.items():
 ac=bpy.data.actions.new(an);ac.use_fake_user=True;ac.slots.new(id_type='OBJECT',name=ob);ac['quality_tier']='Tier-C placeholder; PASS1 E2E only; TierP0';ac['source_fps']=24;ac['scope']='One native Walk phase97 -> native Idle phase1 transition, 1sec; no foot/contact precision certification'
lanes=[]
for ob,an in A.items():ln=ReactionLane(ob);ln.on(an);lanes.append(ln)
cam=s.camera;cam0=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale);changes=[(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',8),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',384),(s.render,'resolution_y',512),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','PNG'),(s.render.image_settings,'color_mode','RGBA'),(s.render.image_settings,'color_depth','8'),(s.render,'filepath','')];saved=[(o,k,getattr(o,k)) for o,k,_ in changes]
for o,k,v in changes:setattr(o,k,v)
neutral=np.concatenate([geom(bpy.data.objects[n])[0] for n in mesh_names]);lo,hi=neutral.min(axis=0),neutral.max(axis=0);target=Vector((lo+hi)*.5);direction=Vector((.6,-1,0)).normalized();cam.data.type='ORTHO';cam.data.ortho_scale=float((hi[2]-lo[2])*1.18);cam.location=target+direction*2;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();folder=O/'FULLBODY_1x';folder.mkdir();rows=[]
for f in range(1,26):
 s.frame_set(f);t=(f-1)/24;u=t*t*t*(t*(t*6-15)+10)
 for n in bones:
  pb=r.pose.bones[n];pb.location=(start[n][0].copy() if f==1 else end[n][0].copy() if f==25 else start[n][0].lerp(end[n][0],u));pb.rotation_quaternion=(start[n][1].copy() if f==1 else end[n][1].copy() if f==25 else start[n][1].slerp(end[n][1],u));pb.keyframe_insert('location',frame=f,group=n);pb.keyframe_insert('rotation_quaternion',frame=f,group=n)
 bpy.context.view_layer.update();delta=(r.matrix_world@r.pose.bones['head'].matrix)@head_ref.inverted();delta=Matrix.LocRotScale(delta.translation,delta.to_quaternion(),Vector((1,1,1)))
 for ob,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]:
  obj=bpy.data.objects[ob];pb=obj.pose.bones[bn];pb.matrix=obj.matrix_world.inverted()@delta@rigrefs[ob];pb.keyframe_insert('location',frame=f);pb.keyframe_insert('rotation_quaternion',frame=f)
 bpy.context.view_layer.update();data={n:geom(bpy.data.objects[n])[0] for n in mesh_names};finite=all(np.isfinite(v).all() for v in data.values());assert finite
 if f==1:assert np.array_equal(data[mesh_names[0]],startv)
 if f==25:assert np.array_equal(data[mesh_names[0]],endv)
 out=folder/f'{f:04}.png';s.render.filepath=str(out);bpy.ops.render.render(write_still=True);rows.append({'frame':f,'PNG_SHA':sha(out),'finite':bool(finite),'body_start_or_end_matches_existing_native_source':f in [1,25],'actual_mesh_SHA_private':{n:hashlib.sha256(v.tobytes()).hexdigest() for n,v in data.items()}})
for an in A.values():
 for la in bpy.data.actions[an].layers:
  for st in la.strips:
   for ba in st.channelbags:
    for fc in ba.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
for ln in reversed(lanes):ln.off()
cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale=cam0;s.render.resolution_x=960;s.render.resolution_y=920;s.render.filepath=str(O/'OFF_SOURCE_CAMERA_NEUTRAL.png');bpy.ops.render.render(write_still=True)
for o,k,v in saved:setattr(o,k,v)
assert snapshot(names)==before;candidate=O/'Character_R4_B_WalkStopIdle_TierC_OFF_R1_20261005.blend';bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=False);bpy.ops.wm.open_mainfile(filepath=str(candidate),use_scripts=False);assert snapshot(names)==before
library=O/'YURI_R4_B_WALKSTOP_IDLE_TIERC_ACTIONS_ONLY_R1.blend';bpy.data.libraries.write(str(library),{bpy.data.actions[n] for n in A.values()},fake_user=True);assert sha(source)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
with bpy.data.libraries.load(str(library),link=False) as (src,dst):assert sorted(src.actions)==sorted(A.values()) and not src.objects and not src.meshes and not src.armatures
meta={'source':str(source),'source_SHA':sha(source),'source_Walk_Action_SHA':before['actions'][walk_name],'source_Idle_Action_SHA':before['actions'][idle_name],'candidate':str(candidate),'candidate_SHA':sha(candidate),'library':str(library),'library_SHA':sha(library),'library_bytes':library.stat().st_size,'actions':A,'quality':'Tier-C placeholder for PASS1 B only','TierP':0,'native_frames':[1,25],'fps':24,'key_interval_sec':1.0,'source_Walk_phase':97,'target_native_Idle_phase':1,'binding_recipe':'Original source +3 Actions via existing ReactionLane; play walkstop once1..25@24, then off/resume existingIdle. Walk cycle boundary source start only; arbitrary interrupt must use owner crossfade. Root navigation owned separately.','original78_OFF_signature_exact':True,'geometry_rest_weights_material_shapes_facegaze_unchanged':True,'motion_start_and_end_body_match_existing_native_source':True,'rows_private':rows,'deferred_PASS2':['foot sliding/floor/contact/COM','hand/finger/neck/hair/mouth precision','continuous derivative/seam polish','G1-G3/TierP/F2-F3'],'Unity_pass':'UNTESTED','source_precision_PASS':False}
# Record after reopen using stable names; old Blender handles can become invalid.
(O/'B_WALKSTOP_IDLE_TIERC_PRIVATE_R1.json').write_text(json.dumps(meta,indent=2),encoding='utf8');print('B_ONE_WALKSTOP_IDLE_TIERC_PLACEHOLDER25_FRAMES_OFF_SOURCE_PRESERVED',flush=True)
