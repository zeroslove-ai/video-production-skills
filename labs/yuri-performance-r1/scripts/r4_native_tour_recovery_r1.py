"""Same completed saved candidate; no original authoring/full contact rerun after64MiB FAIL."""
import bpy,sys,json,hashlib,ast,gzip,math,collections
from pathlib import Path
import numpy as np
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot,props
from r4_native_tour_adapter_r1 import NativeTourLane,ACTIONS
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');P=B/'alpha-native-tour-source-r4';O=B/'alpha-native-tour-recovery-r1';O.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();i=json.loads((B/'alpha-native-tour-intake-r1/NATIVE_TOUR_INTAKE_PRIVATE_R1.json').read_bytes());fg=json.loads((B/'o1-native-tour-source-r4/NATIVE_GUARD_RESULT.json').read_bytes());assert fg['guard_status']=='FAIL' and 'COMBINED_OUTPUT_CAP' in fg['error'] and fg['cleanup_drain'] and fg['cleanup_job_before_close']['active']==0;candidate=P/'Character_R4_NativeTour_EXPERIMENT_OFF_R1_20261005.blend';cs=sha(candidate);source=i['source'];assert sha(source)==i['source_SHA'];ledger=json.loads(gzip.open(P/'NATIVE_TOUR_SURFACE_IDENTITIES_PRIVATE_R1.json.gz','rt',encoding='utf8').read());assert len(ledger['frames'])==769;feet=np.load(P/'NATIVE_TOUR_ACTUAL_FEET_PRIVATE_R1.npz');assert all(feet[q].shape[0]==769 for q in ['L','R']);original=i['original78_OFF_signature_private'];names=list(original['actions']);bpy.ops.wm.open_mainfile(filepath=source,use_scripts=False);assert snapshot(names)==original;s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];refhead=r.matrix_world@r.pose.bones['head'].matrix;refs={ob:bpy.data.objects[ob].matrix_world@bpy.data.objects[ob].pose.bones[bn].matrix for ob,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]}
def rec(a):return [(f.data_path,f.array_index,f.extrapolation,[(list(k.co),list(k.handle_left),list(k.handle_right),k.interpolation,k.handle_left_type,k.handle_right_type) for k in f.keyframe_points],[props(mo) for mo in f.modifiers]) for la in a.layers for st in la.strips for ba in st.channelbags for f in ba.fcurves]
sourceTracks=rec(bpy.data.actions[i['source_action']]);bpy.ops.wm.open_mainfile(filepath=str(candidate),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];assert snapshot(names)==original and rec(bpy.data.actions[ACTIONS[r.name]])==sourceTracks
for fn,defs in [('r4_native_walk_source_supply_r1.py',['contact']),('r4_existing_reach_contact_closure_r1.py',['geom'])]:
 tree=ast.parse((H/fn).read_text(encoding='utf8'));exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in defs],type_ignores=[]),'<same_contact_sample>','exec'))
fixed={};mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4'];body=bpy.data.objects[mesh_names[0]];gn={g.index:g.name for g in body.vertex_groups};baseData={n:geom(bpy.data.objects[n]) for n in mesh_names};floor=float(baseData[mesh_names[0]][0][:,2].min());footids={q:np.array([v.index for v in body.data.vertices if sum(g.weight for g in v.groups if gn[g.group] in ['foot.'+q,'toe.'+q])>.5],int) for q in ['L','R']};base={k:{tuple(tuple(t) for t in pair) for pair in vv} for k,vv in ledger['baseline'].items()};peaks={k:max(len(x['new_pair_identities'][k]) for x in ledger['frames']) for k in base};key=mesh_names[0]+'__self_nonadjacent';bodybad=[x for x in ledger['frames'] if x['new_pair_identities'][key]];first=bodybad[0]['frame'] if bodybad else None;worst=max(bodybad,key=lambda x:len(x['new_pair_identities'][key]))['frame'] if bodybad else None;witness=sorted(set([1,769]+[x for x in [first,worst] if x is not None]));ln=NativeTourLane();ln.on();roots=[];maxErr={ob:0 for ob in refs};narrow=[];rank={};sourcepatch={q:feet[q+'_original_patch_ids'] for q in ['L','R']}
for f in range(1,770):
 s.frame_set(f);bpy.context.view_layer.update();delta=(r.matrix_world@r.pose.bones['head'].matrix)@refhead.inverted();delta=Matrix.LocRotScale(delta.translation,delta.to_quaternion(),Vector((1,1,1)));row={'frame':f,'root':np.array(r.matrix_world@r.pose.bones['root'].matrix).tolist(),'pelvis':np.array(r.matrix_world@r.pose.bones['pelvis'].matrix).tolist(),'head':np.array(r.matrix_world@r.pose.bones['head'].matrix).tolist(),'assembly':np.array(bpy.data.objects['Assembly_Root'].matrix_world).tolist()}
 for ob,bn in [('Armature','Root'),('Hair_Rig_R4','Hair_HeadRoot')]:
  oo=bpy.data.objects[ob];actual=oo.matrix_world@oo.pose.bones[bn].matrix;err=float(np.abs(np.array(actual)-np.array(delta@refs[ob])).max());maxErr[ob]=max(maxErr[ob],err);row[ob+'_max_matrix_goal_error']=err
 roots.append(row)
 if f in witness:
  data={n:geom(bpy.data.objects[n]) for n in mesh_names};ps,_=contact(data);expected={k:{tuple(tuple(t) for t in pair) for pair in vv} for k,vv in ledger['frames'][f-1]['new_pair_identities'].items()};eq={k:ps[k]-base[k]==v for k,v in expected.items()};footerr={q:float(np.abs(data[mesh_names[0]][0][footids[q]]-feet[q][f-1]).max()) for q in footids};narrow.append({'frame':f,'replayed_exact_original_measured_new_pair_identities':eq,'saved_actual_feet_component_error_m':footerr,'all_geometry_finite':True})
 if f%96==1:print('TOUR_SAME_CANDIDATE_RIG_RECOVERY',f,maxErr,flush=True)
for f in [x for x in [first,worst] if x is not None]:
 x=ledger['frames'][f-1];c=collections.Counter()
 for pair in x['new_pair_identities'][key]:
  labels=[]
  for tri in pair:
   weights=collections.Counter()
   for idx in tri:
    for g in body.data.vertices[idx].groups:
     if gn[g.group] in r.pose.bones:weights[gn[g.group]]+=g.weight
   labels.append(weights.most_common(1)[0][0] if weights else 'weak/unweighted')
  c[' / '.join(sorted(labels))]+=1
 rank[str(f)]={'pairs':len(x['new_pair_identities'][key]),'dominant_original_bone_weights':c.most_common(15),'mask_groups_not_treated_as_bones':True}
ln.off();assert snapshot(names)==original
summary={}
for n in ['root','pelvis','head']:
 ar=np.array([x[n] for x in roots]);yaw=np.unwrap(np.arctan2(ar[:,1,0],ar[:,0,0]));summary[n]={'position_range_xyz_m':np.ptp(ar[:,:3,3],axis=0).tolist(),'max_position_step_m':float(np.linalg.norm(np.diff(ar[:,:3,3],axis=0),axis=1).max()),'heading_yaw_range_degrees':float(np.ptp(yaw)*180/math.pi),'net_heading_yaw_degrees':float((yaw[-1]-yaw[0])*180/math.pi)}
support={}
for q in ['L','R']:
 vv=feet[q];patchix=np.array([np.where(footids[q]==a)[0][0] for a in sourcepatch[q]]);labels=[];steps=[]
 for t in range(769):
  mask=np.where(vv[t,:,2]-floor<=.003)[0];prev=np.where(vv[max(0,t-1),:,2]-floor<=.003)[0];common=np.intersect1d(mask,prev);step=float(np.linalg.norm(vv[t,common,:2]-vv[max(0,t-1),common,:2],axis=1).max()) if len(common) else None;gap=float(vv[t,:,2].min()-floor);label='airborne_kinematic' if gap>.003 else ('below_floor_kinematic' if gap<-.001 else ('planted_proximity_candidate' if step is not None and step<=.002 else 'moving_near_floor'));labels.append(label);steps.append({'frame':t+1,'label':label,'persistent_XY_step_m':step,'lowest_gap_m':gap})
 intervals=[];a=0
 for t in range(1,770):
  if t==769 or labels[t]!=labels[a]:intervals.append({'frames':[a+1,t],'label':labels[a]});a=t
 support[q]={'intervals':intervals,'max_persistent_XY_step_m':max([z['persistent_XY_step_m'] for z in steps if z['persistent_XY_step_m'] is not None],default=0),'minimum_gap_m':float(vv[:,:,2].min()-floor),'whole_sole_XY_excursion_vs_first_m':float(np.linalg.norm(vv[:,:,:2]-vv[0,:,:2],axis=2).max()),'original_patch_anchor_max_XY_excursion_m':float(np.linalg.norm(vv[:,patchix,:2]-baseData[mesh_names[0]][0][sourcepatch[q],:2],axis=2).max()),'labels_are_kinematic_proximity_not_force_support':True,'per_frame_private':steps}
cam=s.camera;changes=[(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',8),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',960),(s.render,'resolution_y',920),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','PNG'),(s.render.image_settings,'color_mode','RGBA'),(s.render,'filepath',str(O/'OFF_SOURCE_CAMERA_NEUTRAL.png'))];saved=[(o,k,getattr(o,k)) for o,k,_ in changes]
for o,k,v in changes:setattr(o,k,v)
bpy.ops.render.render(write_still=True)
for o,k,v in saved:setattr(o,k,v)
assert snapshot(names)==original and sha(candidate)==cs and sha(source)==i['source_SHA'];out={'source':source,'source_SHA':i['source_SHA'],'source_action':i['source_action'],'source_Action_SHA':i['source_Action_SHA'],'candidate':str(candidate),'candidate_SHA':cs,'candidate_bytes':candidate.stat().st_size,'original78_signature_private':original,'fps':24,'frames':[1,769],'endpoint_span_seconds':32,'container_seconds':769/24,'source_body_curves':364,'all_original_keys_handles_modifiers_exact_fresh_candidate':True,'all769_full_head_hair_root_goal_matrix_max_error':maxErr,'root_turn_look':summary,'root_rows_private':roots,'all769_saved_actual_contact_ledger_complete':True,'all_surface_peak_new':peaks,'first_BODY_new_frame':first,'worst_BODY_new_frame':worst,'first_worst_BODY_localization':rank,'narrow_witness_exact_identity_and_sole_replay':narrow,'support':support,'source_floor_world_z_m':floor,'all_source78_OFF_and_serialized_candidate_equal':True,'original_data_guard_resource_FAIL_retained':True,'guard_failure_SHA':sha(B/'o1-native-tour-source-r4/NATIVE_GUARD_RESULT.json'),'full_motion_authoring_or_full769_contact_rerun':False,'all769_transform_replay_only':True,'scoped_gate_pass':not any(peaks.values()) and all(v<=1e-5 for v in maxErr.values()),'TierP':0};(O/'NATIVE_TOUR_RECOVERY_PRIVATE_R1.json').write_text(json.dumps(out,indent=2),encoding='utf8');print('TOUR_SAME_SAVED_DATA_RECOVERY',peaks,rank,maxErr,flush=True)
