"""ONE existing Reach upper-chain source correction after proven contact closure failure."""
import bpy,sys,json,hashlib,math,ast
from pathlib import Path
import numpy as np
from mathutils import Matrix,Vector,Quaternion
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'c1-existing-reach-native-upper-c1';O.mkdir(exist_ok=False)
d=json.loads((B/'alpha-c1-reach-candidate-r1/C1_REACH_CANDIDATE_PRIVATE_R1.json').read_bytes());closed=json.loads((B/'c1-existing-reach-contact-closure-r1/EXISTING_REACH_CONTACT_CLOSURE_PRIVATE_R1.json').read_bytes());P=Path(d['source']);C=Path(d['candidate']);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(C)==d['candidate_SHA'];assert closed['verdict']=='FAIL_HOLD_NONADJACENT_SURFACE_DEFECT'
# Reuse the already executed meaningful inclusive oracle functions without running its collector.
module=ast.parse((H/'r4_existing_reach_contact_closure_r1.py').read_text(encoding='utf8'));needed={'setup','geom','evaluate','contacts','fingerprint','topweights','locations'}
exec(compile(ast.Module(body=[x for x in module.body if isinstance(x,ast.FunctionDef) and x.name in needed],type_ignores=[]),'<pinned_existing_inclusive_oracle>','exec'))
from mathutils.bvhtree import BVHTree
fixed={};body=None;verts={};regions={};groupnames={};bonegroups={}
bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);source_names=list(bpy.data.actions.keys());source_sig=snapshot(source_names);setup();neutral=evaluate();baseline_counts,baseline_pairs=contacts(neutral)
bpy.ops.wm.open_mainfile(filepath=str(C),use_scripts=False);s=bpy.context.scene;rig=bpy.data.objects['Meshy_Fitted_Rig'];carrier=bpy.data.objects['Assembly_Root'];face=bpy.data.objects['Armature'];hair=bpy.data.objects['Hair_Rig_R4'];names=list(bpy.data.actions.keys());setup()
oldpaths={n:(bpy.data.images[n].filepath,bpy.data.images[n].filepath_raw) for n in closed['texture_locator_string_differences']}
for n,x in closed['texture_locator_string_differences'].items():bpy.data.images[n].filepath=x['source'][0];bpy.data.images[n].filepath_raw=x['source'][1]
before=snapshot(names);assert snapshot(source_names)==source_sig
upper=['spine','chest','neck','head']+[n+'.'+side for side in ['L','R'] for n in ['clavicle','upper_arm','forearm','hand']]
lower=[n+'.'+side for side in ['L','R'] for n in ['thigh','shin','foot','toe']]+['pelvis']
def curve_dict(a):return {(f.data_path,f.array_index):f for l in a.layers for st in l.strips for ba in st.channelbags for f in ba.fcurves}
def curve_record(f):return [(list(k.co),list(k.handle_left),list(k.handle_right),k.interpolation) for k in f.keyframe_points]
native=bpy.data.actions['MESHY_R2_BODY_Reach'];native_curves=curve_dict(native);old=bpy.data.actions[d['additive_body_actions']['Meshy_Fitted_Rig']]
for n in upper:
 assert all(('pose.bones["'+n+'"].rotation_quaternion',j) in native_curves for j in range(4))
 for j in range(3):
  f=native_curves.get(('pose.bones["'+n+'"].location',j))
  if f:assert all(abs(f.evaluate(1+(k-1)*96/60))<1e-8 for k in range(1,62))
newbody=old.copy();newbody.name='YURI_R4_C1_REACH_NATIVE_UPPER_BODY_C1';newbody.use_fake_user=True
paths={'pose.bones["'+n+'"].rotation_quaternion' for n in upper}
for l in newbody.layers:
 for st in l.strips:
  for ba in st.channelbags:
   for f in list(ba.fcurves):
    if f.data_path in paths:ba.fcurves.remove(f)
oldother={(p,j):curve_record(f) for (p,j),f in curve_dict(old).items() if p not in paths}
actions={'Meshy_Fitted_Rig':newbody.name,'Assembly_Root':d['additive_body_actions']['Assembly_Root']}
for obj in ['Armature','Hair_Rig_R4']:
 a=bpy.data.actions[d['additive_body_actions'][obj]].copy();a.name='YURI_R4_C1_REACH_NATIVE_UPPER_'+('HEAD' if obj=='Armature' else 'HAIR')+'_C1';a.use_fake_user=True;actions[obj]=a.name
ref_head=rig.matrix_world@rig.pose.bones['head'].matrix;ref_face=face.matrix_world@face.pose.bones['Root'].matrix;ref_hair=hair.matrix_world@hair.pose.bones['Hair_HeadRoot'].matrix
class Lane:
 def __init__(self,mapping):self.mapping=mapping
 def on(self):
  self.lanes=[];ad=carrier.animation_data;self.save={'had_ad':ad is not None,'action':ad.action if ad else None,'slot':ad.action_slot if ad else None,'handle':ad.action_slot_handle if ad else 0,'last':ad.last_slot_identifier if ad else '', 'loc':carrier.location.copy()}
  for obj in ['Meshy_Fitted_Rig','Armature','Hair_Rig_R4']:
   lane=ReactionLane(obj);lane.on(self.mapping[obj]);self.lanes.append(lane)
  ad=carrier.animation_data_create();ad.action=bpy.data.actions[self.mapping['Assembly_Root']];ad.action_slot=ad.action.slots[0]
 def off(self):
  for q in reversed(self.lanes):q.off()
  v=self.save;ad=carrier.animation_data;ad.action=v['action']
  if v['action'] and v['slot']:ad.action_slot=v['slot']
  ad.action_slot_handle=v['handle'];ad.last_slot_identifier=v['last'];carrier.location=v['loc']
  if not v['had_ad']:carrier.animation_data_clear()
  bpy.context.view_layer.update()
oldlane=Lane(d['additive_body_actions']);oldlane.on();ref=[];footids={side:sorted({v.index for v in body.data.vertices if sum(g.weight for g in v.groups if groupnames[g.group] in ['foot.'+side,'toe.'+side])>.5}) for side in ['L','R']}
for f in range(1,62):
 s.frame_set(f);bpy.context.view_layer.update();v=geom(body)[0];ref.append({'lower':{n:np.array(rig.matrix_world@rig.pose.bones[n].matrix) for n in lower},'root':np.array(carrier.matrix_world),'foot':{side:v[ids].copy() for side,ids in footids.items()}})
oldlane.off();assert snapshot(names)==before
lane=Lane(actions);lane.on();phase_rows=[]
for f in range(1,62):
 s.frame_set(f);phase=1+(f-1)*96/60
 for n in upper:
  path='pose.bones["'+n+'"].rotation_quaternion';pb=rig.pose.bones[n];pb.rotation_quaternion=Quaternion([native_curves[(path,j)].evaluate(phase) for j in range(4)]);pb.keyframe_insert('rotation_quaternion',frame=f,group=n)
 bpy.context.view_layer.update();delta=(rig.matrix_world@rig.pose.bones['head'].matrix)@ref_head.inverted();delta=Matrix.LocRotScale(delta.translation,delta.to_quaternion(),Vector((1,1,1)))
 for obj,bn,refmat in [(face,'Root',ref_face),(hair,'Hair_HeadRoot',ref_hair)]:
  pb=obj.pose.bones[bn];basis=pb.bone.matrix_local.inverted()@obj.matrix_world.inverted()@delta@refmat;pb.rotation_quaternion=basis.to_quaternion();pb.location=basis.translation;pb.keyframe_insert('rotation_quaternion',frame=f,group=bn);pb.keyframe_insert('location',frame=f,group=bn)
 phase_rows.append({'frame':f,'native_original_Reach_phase_frame':phase})
for n in [actions['Meshy_Fitted_Rig'],actions['Armature'],actions['Hair_Rig_R4']]:
 for f in curve_dict(bpy.data.actions[n]).values():
  for k in f.keyframe_points:k.interpolation='LINEAR'
assert oldother=={(p,j):curve_record(f) for (p,j),f in curve_dict(newbody).items() if p not in paths}
rows=[];sourcev=neutral[0];edges=neutral[2];sourcelen=np.linalg.norm(sourcev[edges[:,0]]-sourcev[edges[:,1]],axis=1);valid=sourcelen>1e-6
for f in range(1,62):
 s.frame_set(f);bpy.context.view_layer.update();data=evaluate();co,pairs=contacts(data);new={k:len(v-baseline_pairs[k]) for k,v in pairs.items()};v=data[0];ratio=np.linalg.norm(v[edges[valid,0]]-v[edges[valid,1]],axis=1)/sourcelen[valid];lowererror=max(float(np.max(np.abs(np.array(rig.matrix_world@rig.pose.bones[n].matrix)-ref[f-1]['lower'][n]))) for n in lower);rooterror=float(np.max(np.abs(np.array(carrier.matrix_world)-ref[f-1]['root'])));footerror={side:float(np.max(np.linalg.norm(v[ids]-ref[f-1]['foot'][side],axis=1))) for side,ids in footids.items()};assert lowererror==0 and rooterror==0 and max(footerror.values())==0
 rows.append({'frame':f,'time_seconds':(f-1)/30,'counts':co,'new_vs_source_OFF':new,'locations_private':locations(data,pairs),'finite':True,'topology_equal':True,'lower_matrix_vs_old_C1_error':lowererror,'root_vs_old_C1_error':rooterror,'all_actual_foot_vertices_vs_old_C1_error_m':footerror,'edge_ratio_min_max':[float(ratio.min()),float(ratio.max())],'edge_ratio_p01_p99':np.quantile(ratio,[.01,.99]).tolist()});print('NATIVE_UPPER_CORRECTION_C1_FULL_CONTACT',f,new,flush=True)
lane.off();assert snapshot(names)==before and snapshot(source_names)==source_sig
candidate=O/'Character_R4_C1_Reach_NativeUpper_EXPERIMENT_OFF_C1_20261005.blend';bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=False);assert snapshot(names)==before and snapshot(source_names)==source_sig
lib=O/'YURI_R4_C1_REACH_NATIVE_UPPER_ACTIONS_ONLY_C1.blend';bpy.data.libraries.write(str(lib),{bpy.data.actions[n] for n in actions.values()},fake_user=True)
with bpy.data.libraries.load(str(lib),link=False) as (a,b):assert len(a.actions)==4 and not a.objects and not a.meshes and not a.armatures
# Necessary NEW motion proof only after meaningful contact clearance; never rerender prior C1 footage.
clear=not any(any(v for v in x['new_vs_source_OFF'].values()) for x in rows);renders={}
if clear:
 cam=s.camera;savecam=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width)
 changes=[(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',2),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',512),(s.render,'resolution_y',384),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','JPEG'),(s.render.image_settings,'color_mode','RGB'),(s.render.image_settings,'color_depth','8'),(s.render.image_settings,'quality',92),(s.render,'filepath','')]
 saves=[(ob,k,getattr(ob,k)) for ob,k,_ in changes]
 for ob,k,val in changes:setattr(ob,k,val)
 lane=Lane(actions);lane.on()
 for view in ['front','quarter','side']:
  p=O/view;p.mkdir();oldcam=json.loads((B/'alpha-c1-reach-preview-r1'/view/'RENDER_RECEIPT_R4.json').read_bytes())['camera'];cam.data.type=oldcam['type'];cam.data.lens=oldcam['lens_mm'];cam.data.sensor_width=oldcam['sensor_width_mm'];cam.location=oldcam['location'];cam.rotation_euler=oldcam['rotation_euler'];renders[view]=oldcam
  for f in range(1,62):s.frame_set(f);bpy.context.view_layer.update();s.render.filepath=str(p/f'{f:04}.jpg');bpy.ops.render.render(write_still=True)
 lane.off();cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width=savecam;s.render.resolution_x=960;s.render.resolution_y=920;s.cycles.samples=8;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(O/'NEW_CANDIDATE_OFF_SOURCE_NEUTRAL.png');bpy.ops.render.render(write_still=True)
 for ob,k,val in saves:setattr(ob,k,val)
 assert snapshot(names)==before and snapshot(source_names)==source_sig
assert sha(C)==d['candidate_SHA'] and sha(P)==d['source_SHA']
meta={'task':'ROOT_PM_EXISTING_REACH_CONTACT_CLOSURE_R1_ONE_ALLOWED_SOURCE_UPPER_CORRECTION','source':str(P),'source_SHA':sha(P),'old_candidate':str(C),'old_candidate_SHA':sha(C),'candidate':str(candidate),'candidate_SHA':sha(candidate),'candidate_bytes':candidate.stat().st_size,'library':{'file':str(lib),'sha256':sha(lib),'bytes':lib.stat().st_size,'actions':4,'objects':0,'meshes':0,'armatures':0},'actions':actions,'source_original78_and_prior82Actions_preserved':True,'source_raw_OFF_snapshot_equal_including_texture_paths':True,'restored6_original_canonical_locator_strings_only_texture_bytes_nodes_materials_unchanged':True,'one_candidate_no_angle_sweeps_no_dance':True,'reused_original_native_Reach_upper12':upper,'native_phase_from_to':[1,97],'fps':30,'frames':[1,61],'upper_original_trajectory_variant_not_old_donor_hand_path':True,'all_other_body_curves_exact':True,'root_action_exact_old_C1':True,'rows_private':rows,'phase_rows':phase_rows,'views':renders,'verdict':'SCOPED_ALL61_CONTACT_PASS_VISUAL_PENDING' if clear else 'FAIL_HOLD_ONE_SOURCE_CORRECTION_STOP','TierP':0,'no_save_original_no_Unity_physics_prop_facial_gaze_driver_change':True}
(O/'NATIVE_UPPER_SOURCE_CORRECTION_PRIVATE_C1.json').write_text(json.dumps(meta,indent=2),encoding='utf8');print('ONE_NATIVE_UPPER_C1_RESULT',meta['verdict'],sha(candidate),flush=True)
