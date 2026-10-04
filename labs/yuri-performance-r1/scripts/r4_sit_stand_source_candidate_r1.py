"""ONE known dedicated CC0 seated phrase retarget; original R4 animation-only."""
import bpy,sys,json,hashlib,ast,time,gzip,math
from pathlib import Path
import numpy as np
from mathutils import Matrix,Vector,Quaternion
from mathutils.bvhtree import BVHTree
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
from r4_sit_stand_adapter_r1 import SitStandLane,ACTIONS
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-sit-stand-source-candidate-r1';O.mkdir(exist_ok=False);I=B/'alpha-sit-stand-source-intake-r1/SIT_STAND_SOURCE_INTAKE_PRIVATE_R1.json';i=json.loads(I.read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();P=Path(i['source']);assert sha(P)==i['source_SHA'] and sha(i['FBX_source'])==i['FBX_SHA'];start=time.perf_counter();bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];names=list(bpy.data.actions.keys());before=snapshot(names);assert len(names)==78
module=ast.parse((H/'r4_native_walk_source_supply_r1.py').read_text(encoding='utf8'));exec(compile(ast.Module(body=[x for x in module.body if isinstance(x,ast.FunctionDef) and x.name in ['contact']],type_ignores=[]),'<pinned_whole_actual_contact>','exec'));module=ast.parse((H/'r4_existing_reach_contact_closure_r1.py').read_text(encoding='utf8'));exec(compile(ast.Module(body=[x for x in module.body if isinstance(x,ast.FunctionDef) and x.name=='geom'],type_ignores=[]),'<pinned_actual_geometry>','exec'));fixed={};mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4'];body=bpy.data.objects[mesh_names[0]]
def evaluate():return {n:geom(bpy.data.objects[n]) for n in mesh_names}
neutral=evaluate();basepairs,baseraw=contact(neutral);v0=neutral[mesh_names[0]][0];floor=float(v0[:,2].min());groups={g.index:g.name for g in body.vertex_groups};footids={q:np.array([v.index for v in body.data.vertices if sum(g.weight for g in v.groups if groups[g.group] in ['foot.'+q,'toe.'+q])>.5],int) for q in ['L','R']};patchids={q:footids[q][np.where(v0[footids[q],2]<=floor+.003)[0]] for q in footids};assert all(len(x)>0 for x in patchids.values());offworld={b.name:r.matrix_world@b.matrix for b in r.pose.bones};refhead=offworld['head'];refs={ob:bpy.data.objects[ob].matrix_world@bpy.data.objects[ob].pose.bones[bn].matrix for ob,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]}
# Native limb lengths retained; source rotations converted through common world basis/rest and target hierarchical rest.
mapping={'pelvis':'pelvis','spine':'spine_01','chest':'spine_03','neck':'neck_01','head':'Head'}
for q,u in [('L','l'),('R','r')]:
 for t,src in [('clavicle','clavicle'),('upper_arm','upperarm'),('forearm','lowerarm'),('hand','hand'),('thigh','thigh'),('shin','calf'),('foot','foot'),('toe','ball')]:mapping[t+'.'+q]=src+'_'+u
source_rest={n:Matrix(v) for n,v in i['rest_world_private'].items()};first={n:Matrix(v) for n,v in i['samples_private']['Sitting_Enter'][0].items()};basis=Quaternion(Vector((0,0,1)),math.pi);target_leg=sum(r.data.bones[n].length*r.matrix_world.to_scale().x for n in ['thigh.L','shin.L']);source_leg=sum(i['bones'][n]['length_world'] for n in ['thigh_l','calf_l']);scale=target_leg/source_leg
phrase=[('Sitting_Enter',j,rec) for j,rec in enumerate(i['samples_private']['Sitting_Enter'],1)]+[('Sitting_Idle_Loop',j,rec) for j,rec in enumerate(i['samples_private']['Sitting_Idle_Loop'][1:],2)]+[('Sitting_Exit',j,rec) for j,rec in enumerate(i['samples_private']['Sitting_Exit'][1:],2)];F=len(phrase);assert F==121;actions={};lanes=[]
for ob in ['Meshy_Fitted_Rig','Armature','Hair_Rig_R4']:
 ac=bpy.data.actions.new(ACTIONS[ob]);ac.use_fake_user=True;ac.slots.new(id_type='OBJECT',name=ob);ac['source_fps']=30;ac['source_sequence']='Sitting_Enter / Sitting_Idle_Loop / Sitting_Exit';actions[ob]=ac;ln=ReactionLane(ob);ln.on(ac.name);lanes.append(ln)
carrier=bpy.data.objects['Assembly_Root'];ac=bpy.data.actions.new(ACTIONS['Assembly_Root']);ac.use_fake_user=True;ac.slots.new(id_type='OBJECT',name=carrier.name);actions[carrier.name]=ac
# Constant carrier action created without attaching; world root movement is mapped pelvis only.
for f in [1,F]:
 for axis in range(3):pass
# Carrier constant keys using temporary binding and exact restore below via binder-owned transform.
savedad=carrier.animation_data;carrierSave={'had':savedad is not None,'action':savedad.action if savedad else None,'slot':savedad.action_slot if savedad else None,'handle':savedad.action_slot_handle if savedad else 0,'last':savedad.last_slot_identifier if savedad else '', 'loc':carrier.location.copy()};ad=carrier.animation_data_create();ad.action=ac;ad.action_slot=ac.slots[0]
for f in [1,F]:carrier.keyframe_insert('location',frame=f)
previous={};author=[];targetnominal={};pose_samples=[]
upper=set(mapping)-{'pelvis'}-{n+'.'+q for q in ['L','R'] for n in ['thigh','shin','foot','toe']}
for f,(tag,sf,rec) in enumerate(phrase,1):
 s.frame_set(f);bpy.context.view_layer.update();src={n:Matrix(v) for n,v in rec.items()};desired={};rotations={}
 for pb in r.pose.bones:
  if pb.name not in mapping:continue
  sn=mapping[pb.name];ref=first[sn] if pb.name in upper else source_rest[sn];delta=basis@src[sn].to_quaternion()@ref.to_quaternion().inverted()@basis.inverted();want=delta@offworld[pb.name].to_quaternion();desired[pb.name]=want
  pq=desired.get(pb.parent.name,offworld[pb.parent.name].to_quaternion()) if pb.parent else r.matrix_world.to_quaternion();rel=pb.parent.bone.matrix_local.inverted()@pb.bone.matrix_local if pb.parent else pb.bone.matrix_local;qq=rel.to_quaternion().inverted()@pq.inverted()@want
  if pb.name in previous and previous[pb.name].dot(qq)<0:qq.negate()
  previous[pb.name]=qq.copy();pb.rotation_quaternion=qq;rotations[pb.name]=qq.copy()
 # World pelvis translation normalized by native leg lengths, baseline source anatomical rest; no limb scale/rest changes.
 pb=r.pose.bones['pelvis'];goal=offworld['pelvis'].translation+(basis@(src['pelvis'].translation-source_rest['pelvis'].translation))*scale;targetnominal[f]=list(goal);bpy.context.view_layer.update();actual=r.matrix_world@pb.head;parentlinear=(r.matrix_world.to_3x3()@pb.parent.matrix.to_3x3()@(pb.parent.bone.matrix_local.inverted()@pb.bone.matrix_local).to_3x3()) if pb.parent else r.matrix_world.to_3x3()@pb.bone.matrix_local.to_3x3();pb.location=parentlinear.inverted()@(goal-actual);bpy.context.view_layer.update()
 # ONE explicit kinematic floor fit: uniform pelvis Z raises/lowers lowest actual sole vertex to original floor.
 vv=geom(body)[0];gap=min(float(vv[ids,2].min()-floor) for ids in footids.values());pb.location+=parentlinear.inverted()@Vector((0,0,-gap));bpy.context.view_layer.update()
 for bn in mapping:r.pose.bones[bn].keyframe_insert('rotation_quaternion',frame=f,group=bn)
 pb.keyframe_insert('location',frame=f,group='pelvis');bpy.context.view_layer.update();delta=(r.matrix_world@r.pose.bones['head'].matrix)@refhead.inverted();delta=Matrix.LocRotScale(delta.translation,delta.to_quaternion(),Vector((1,1,1)))
 for ob,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]:
  oo=bpy.data.objects[ob];pp=oo.pose.bones[bn];bb=pp.bone.matrix_local.inverted()@oo.matrix_world.inverted()@delta@refs[ob];pp.location=bb.translation;pp.rotation_quaternion=bb.to_quaternion();pp.keyframe_insert('location',frame=f,group=bn);pp.keyframe_insert('rotation_quaternion',frame=f,group=bn)
 author.append({'frame':f,'source_action':tag,'source_local_frame':sf,'uniform_floor_fit_pelvis_Z_m':-gap,'nominal_pelvis_world_m':list(goal),'actual_pelvis_world_m':list(r.matrix_world@r.pose.bones['pelvis'].head)})
for aa in actions.values():
 for la in aa.layers:
  for st in la.strips:
   for bag in st.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
# Fixed fitted seat witness based on existing source seated terminal pelvis after ONE floor fit, not physical chair geometry.
seat_pelvis=author[39]['actual_pelvis_world_m'];seat_surface_z=seat_pelvis[2]-.035;seat={'pelvis_anchor_world_m':seat_pelvis,'surface_plane_world_z_m':seat_surface_z,'surface_height_above_source_floor_m':seat_surface_z-floor,'nominal_source_normalized_pelvis_anchor_m':targetnominal[40],'pelvis_clearance_design_m':.035,'basis':'Known dedicated seated source normalized by target leg lengths + ONE actual-sole floor fit; fixed frame40 witness. No geometry prop/force/support certificate.'}
rows=[];feet={q:[] for q in footids};ledger={'baseline':{k:sorted(v) for k,v in basepairs.items()},'frames':[]};prev=None;endpoint={};rom={n:[] for n in ['thigh.L','thigh.R','shin.L','shin.R','upper_arm.L','upper_arm.R']};headerrors=[]
for f in range(1,F+1):
 s.frame_set(f);bpy.context.view_layer.update();data=evaluate();v=data[mesh_names[0]][0];pairs,raw=contact(data);new={k:len(v-basepairs[k]) for k,v in pairs.items()};j={n:list(r.matrix_world@r.pose.bones[n].head) for n in ['pelvis','head','thigh.L','shin.L','foot.L','thigh.R','shin.R','foot.R']}
 for q,ids in footids.items():feet[q].append(v[ids].copy())
 for n in rom:rom[n].append(float(r.pose.bones[n].rotation_quaternion.rotation_difference(Matrix(before['rest_pose_settings']['rigs'][r.name]['bones'][n]['matrix_basis']) .to_quaternion()).angle) if False else float(r.pose.bones[n].rotation_quaternion.angle*180/math.pi))
 delta=(r.matrix_world@r.pose.bones['head'].matrix)@refhead.inverted();delta=Matrix.LocRotScale(delta.translation,delta.to_quaternion(),Vector((1,1,1)));err={ob:float(np.abs(np.array(bpy.data.objects[ob].matrix_world@bpy.data.objects[ob].pose.bones[bn].matrix)-np.array(delta@refs[ob])).max()) for ob,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]};headerrors.append(err)
 step=float(np.linalg.norm(v-prev,axis=1).max()) if prev is not None else 0;prev=v.copy();rows.append({'frame':f,'finite':True,'pelvis_world_m':j['pelvis'],'new_surface_pair_counts_vs_source_OFF':new,'absolute_pair_counts':{k:len(v) for k,v in pairs.items()},'body_max_vertex_step_m':step,'feet_min_gap_m':{q:float(v[ids,2].min()-floor) for q,ids in footids.items()},'head_hair_root_rigid_transport_matrix_error':err,'joint_world_private':j});ledger['frames'].append({'frame':f,'new_pair_identities':{k:sorted(v-basepairs[k]) for k,v in pairs.items()}})
 if f in [1,40,90,121]:endpoint[f]={n:x[0] for n,x in data.items()}
 if f%15==1:print('SIT_STAND_ACTUAL_CONTACT',f,new,rows[-1]['feet_min_gap_m'],flush=True)
for ln in reversed(lanes):ln.off()
ad=carrier.animation_data;ad.action=carrierSave['action']
if carrierSave['action'] and carrierSave['slot']:ad.action_slot=carrierSave['slot']
ad.action_slot_handle=carrierSave['handle'];ad.last_slot_identifier=carrierSave['last'];carrier.location=carrierSave['loc']
if not carrierSave['had']:carrier.animation_data_clear()
bpy.context.view_layer.update();assert snapshot(names)==before and sha(P)==i['source_SHA']
foot_summary={}
for q,vvs in feet.items():
 vv=np.array(vvs);patch=np.array([np.where(footids[q]==idx)[0][0] for idx in patchids[q]]);proximity=[set(np.where(x[:,2]-floor<=.003)[0].tolist()) for x in vv];maxstep=0
 for t in range(1,F):
  common=sorted(proximity[t-1]&proximity[t])
  if common:maxstep=max(maxstep,float(np.linalg.norm(vv[t,common,:2]-vv[t-1,common,:2],axis=1).max()))
 foot_summary[q]={'original_support_patch_3mm_vertices':len(patch),'original_patch_max_world_XY_excursion_m':float(np.linalg.norm(vv[:,patch,:2]-vv[0,patch,:2],axis=2).max()),'original_patch_gap_min_max_m':[float((vv[:,patch,2]-floor).min()),float((vv[:,patch,2]-floor).max())],'whole_foot_min_gap_m':float((vv[:,:,2]-floor).min()),'persistent_proximity3mm_max_XY_step_m':maxstep,'proximity_frames':sum(bool(x) for x in proximity),'not_force_contact':True}
candidate=O/'Character_R4_SitStand_SOURCE_EXPERIMENT_OFF_R1_20261005.blend';bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=False);assert snapshot(names)==before;lib=O/'YURI_R4_SIT_STAND_ACTIONS_ONLY_R1.blend';bpy.data.libraries.write(str(lib),set(actions.values()),fake_user=True)
with bpy.data.libraries.load(str(lib),link=False) as (src,dst):assert len(src.actions)==4 and not src.objects and not src.meshes and not src.armatures
cs=sha(candidate);bpy.ops.wm.open_mainfile(filepath=str(candidate),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];assert snapshot(names)==before
meta={'task':'ROOT_PM_WALK_C3_CAUSAL_FAILURE_TO_SIT_STAND_SOURCE_R1','source':str(P),'source_SHA':i['source_SHA'],'FBX_source':i['FBX_source'],'FBX_SHA':i['FBX_SHA'],'source_actions':i['source_action_intake'],'original78_signature_private':before,'source78_fullraw_OFF_and_fresh_serialized_equal':True,'candidate':str(candidate),'candidate_SHA':cs,'candidate_bytes':candidate.stat().st_size,'library':{'file':str(lib),'sha256':sha(lib),'bytes':lib.stat().st_size,'actions':4,'objects':0,'meshes':0,'armatures':0},'actions':ACTIONS,'fps':30,'source_scene_fps_saved':s.render.fps/s.render.fps_base,'frames':[1,F],'phase_frames':{'enter':[1,40],'hold':[40,90],'exit':[90,121]},'source_duration_endpoint_seconds':4.0,'encoded_duration_seconds':121/30,'normalized_leg_scale':scale,'target_leg_length_m':target_leg,'source_leg_length_m':source_leg,'world_basis':'180deg around Z maps source anatomical left-negativeX to R4 left-positiveX; upZ preserved.','mapping':mapping,'retarget':'World rest-aware rotation deltas; upper common standing neutral calibration, lower anatomical source rest; target hierarchy/rest/native limb lengths unchanged; leglength-normalized pelvis translation, ONE uniform actual sole floor-fit pelvisZ. No bone scale/copy-rotation direct/IK candidate family.','seat_witness':seat,'author_rows_private':author,'rows_private':rows,'feet':foot_summary,'ROM_local_quaternion_angle_degrees':{n:[min(v),max(v)] for n,v in rom.items()},'max_body_step_m':max(x['body_max_vertex_step_m'] for x in rows),'head_hair_rigid_transport_matrix_error_max':{ob:max(x[ob] for x in headerrors) for ob in headerrors[0]},'first_last_body_head_hair_component_error_m':{n:float(np.abs(endpoint[1][n]-endpoint[121][n]).max()) for n in mesh_names},'source_neutral_vs_ON_start_component_error_m':{n:float(np.abs(endpoint[1][n]-neutral[n][0]).max()) for n in mesh_names},'pelvis_stand_to_seat_delta_m':(np.array(author[39]['actual_pelvis_world_m'])-np.array(author[0]['actual_pelvis_world_m'])).tolist(),'seated_pelvis_anchor_max_distance_m':max(float(np.linalg.norm(np.array(x['actual_pelvis_world_m'])-seat_pelvis)) for x in author[39:90]),'all121_new_surface_pair_peak':{k:max(x['new_surface_pair_counts_vs_source_OFF'][k] for x in rows) for k in basepairs},'surface_scope':'All actual BODY/HEAD/HAIR triangles weak/unweighted inclusive; self nonadjacent and cross identities vs original OFF; identical/shared-vertex adjacency excluded; no volume/force/physical chair/Unity/TierP/F2/StageB approval.','donor_geometry_into_R4':False,'TierP':0,'elapsed_before_render_seconds':time.perf_counter()-start}
with gzip.open(O/'SIT_STAND_TRIANGLE_IDENTITIES_PRIVATE_R1.json.gz','wt',encoding='utf8') as f:json.dump(ledger,f)
np.savez_compressed(O/'SIT_STAND_ACTUAL_SOLES_PRIVATE_R1.npz',L=np.array(feet['L']),R=np.array(feet['R']),L_original_support_patch_vertex_ids=patchids['L'],R_original_support_patch_vertex_ids=patchids['R']);(O/'SIT_STAND_SOURCE_PRIVATE_R1.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
cam=s.camera;savecam=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width);changes=[(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',2),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',384),(s.render,'resolution_y',384),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','JPEG'),(s.render.image_settings,'color_mode','RGB'),(s.render.image_settings,'color_depth','8'),(s.render.image_settings,'quality',92),(s.render,'filepath','')];saves=[(ob,k,getattr(ob,k)) for ob,k,_ in changes]
for ob,k,v in changes:setattr(ob,k,v)
ln=SitStandLane();ln.on();views={}
for view,direction in [('front',(0,-1,0)),('quarter',(.6,-1,0)),('side',(1,0,0))]:
 folder=O/view;folder.mkdir();target=Vector((.002,.02,.48));cam.data.type='ORTHO';cam.data.ortho_scale=1.18;cam.location=target+Vector(direction).normalized()*.8;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();views[view]={'type':'ORTHO','ortho_scale':1.18,'target':list(target),'location':list(cam.location),'rotation_euler':list(cam.rotation_euler),'resolution':[384,384],'fps':30,'frames':[1,F],'fixed':True}
 for f in range(1,F+1):s.frame_set(f);bpy.context.view_layer.update();s.render.filepath=str(folder/f'{f:04}.jpg');bpy.ops.render.render(write_still=True)
ln.off();cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width=savecam;s.render.resolution_x=960;s.render.resolution_y=920;s.cycles.samples=8;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(O/'SIT_STAND_OFF_SOURCE_NEUTRAL_R1.png');bpy.ops.render.render(write_still=True)
for ob,k,v in saves:setattr(ob,k,v)
assert snapshot(names)==before and sha(P)==i['source_SHA'] and sha(i['FBX_source'])==i['FBX_SHA'] and sha(candidate)==cs;meta['views']=views;meta['actual_complete121_threeview_capture']=True;meta['fullraw_OFF_after_render_equal']=True;meta['collector_elapsed_seconds']=time.perf_counter()-start;(O/'SIT_STAND_SOURCE_PRIVATE_R1.json').write_text(json.dumps(meta,indent=2),encoding='utf8');print('SIT_STAND_ONE_SOURCE_CANDIDATE_COMPLETE',meta['all121_new_surface_pair_peak'],foot_summary,flush=True)
