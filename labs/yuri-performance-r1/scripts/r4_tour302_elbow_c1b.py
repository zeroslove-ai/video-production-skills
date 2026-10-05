"""ONE local Tour forearm.L hinge-amplitude copy; preserve clock and immutable R4."""
import bpy,sys,json,hashlib,math,ast,gzip,collections
from pathlib import Path
import numpy as np
from mathutils import Vector,Euler
from mathutils.bvhtree import BVHTree
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot,props
from r4_appearance_adapter import ReactionLane
from r4_native_tour_adapter_r1 import ACTIONS
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-tour302-elbow-c1b';O.mkdir(exist_ok=False)
m=json.loads((B/'alpha-native-tour-recovery-r2/NATIVE_TOUR_RECOVERY_PRIVATE_R2.json').read_bytes());it=json.loads((B/'alpha-tour302-intake-r1/TOUR302_HINGE_INTAKE_PRIVATE_R1.json').read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(m['candidate'])==m['candidate_SHA'];assert sha(m['source'])==m['source_SHA']
ledger=json.loads(gzip.open(B/'alpha-native-tour-source-r4/NATIVE_TOUR_SURFACE_IDENTITIES_PRIVATE_R1.json.gz','rt',encoding='utf8').read())
bpy.ops.wm.open_mainfile(filepath=m['candidate'],use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];names=list(bpy.data.actions.keys());before=snapshot(names);assert snapshot(list(m['original78_signature_private']['actions']))==m['original78_signature_private']
for fn,defs in [('r4_native_walk_source_supply_r1.py',['contact']),('r4_existing_reach_contact_closure_r1.py',['geom'])]:
 tree=ast.parse((H/fn).read_text(encoding='utf8'));exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in defs],type_ignores=[]),'<same_actual_mesh_oracle>','exec'))
fixed={};mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4'];body=bpy.data.objects[mesh_names[0]]
base={k:{tuple(tuple(t) for t in pair) for pair in v} for k,v in ledger['baseline'].items()};bodykey=mesh_names[0]+'__self_nonadjacent'
initial7={tuple(tuple(t) for t in pair) for pair in ledger['frames'][301]['new_pair_identities'][bodykey]}
def curves(a):return [f for la in a.layers for st in la.strips for ba in st.channelbags for f in ba.fcurves]
def record(a):return {(f.data_path,f.array_index):{'extrapolation':f.extrapolation,'points':[(list(k.co),list(k.handle_left),list(k.handle_right),k.interpolation,k.handle_left_type,k.handle_right_type) for k in f.keyframe_points],'modifiers':[props(mm) for mm in f.modifiers]} for f in curves(a)}
def bind(name):
 lanes=[]
 for ob,an in ACTIONS.items():
  lane=ReactionLane(ob);lane.on(name if ob==r.name else an);lanes.append(lane)
 return lanes
def off(lanes):
 for ln in reversed(lanes):ln.off()
parent=bpy.data.actions[ACTIONS[r.name]];original_records=record(parent);a=parent.copy();a.name='YURI_R4_NATIVE_TOUR_LEFT_ELBOW_C1';a.use_fake_user=True
source_peak=max(abs(x['EulerXYZ_degrees'][2]) for x in it['rows_private']);safe=abs(next(x for x in it['rows_private'] if x['frame']==301)['EulerXYZ_degrees'][2])-2.;scale=safe/source_peak
path='pose.bones["forearm.L"].rotation_quaternion';fcs={f.array_index:f for f in curves(a) if f.data_path==path};assert set(fcs)=={0,1,2,3}
modified=[]
for f in range(290,385):
 q=r.pose.bones['forearm.L'].rotation_quaternion.copy()
 for k in range(4):q[k]=fcs[k].evaluate(f)
 eu=q.to_euler('XYZ');eu.z*=scale;nq=eu.to_quaternion()
 if nq.dot(q)<0:nq.negate()
 for k in range(4):
  point=next(p for p in fcs[k].keyframe_points if p.co.x==f);assert point.interpolation=='LINEAR';delta=nq[k]-point.co.y;point.co.y=nq[k];point.handle_left.y+=delta;point.handle_right.y+=delta
 modified.append(f)
for f in fcs.values():
 f.update()
 original_points=original_records[(f.data_path,f.array_index)]['points']
 for p,rr in zip(f.keyframe_points,original_points):
  if rr[0][0] not in modified:
   p.co=rr[0];p.handle_left=rr[1];p.handle_right=rr[2]
a['scope']='ONE forearm.L local-Z amplitude reduction on existing289..385 gesture; source clock unchanged; original pose deviation explicit; other local joints untouched; wrists472 HOLD'
a['source_Action_SHA']=m['source_Action_SHA'];a['hinge_scale']=scale;a['frame_boundary']=[289,385]
new_records=record(a);outside_equal=True;others_equal=True
for key,rr in original_records.items():
 nn=new_records[key]
 if key[0]!=path:others_equal=others_equal and rr==nn
 else:
  assert rr['extrapolation']==nn['extrapolation'] and rr['modifiers']==nn['modifiers']
  for x,y in zip(rr['points'],nn['points']):
   assert x[0][0]==y[0][0] and x[3:]==y[3:]
   if x[0][0] not in modified:outside_equal=outside_equal and x==y
assert outside_equal and others_equal, ('outside',outside_equal,'others',others_equal)
neutral=geom(body)[0];gn={g.index:g.name for g in body.vertex_groups};footids={q:np.array([v.index for v in body.data.vertices if sum(g.weight for g in v.groups if gn[g.group] in ['foot.'+q,'toe.'+q])>.5],int) for q in ['L','R']}
floor=float(neutral[:,2].min());sourcepatch={q:ids[neutral[ids,2]<=floor+.003] for q,ids in footids.items()};npz=np.load(B/'alpha-native-tour-foot-oracle-verified-r2/NATIVE_TOUR_SUPPORT_PATCH_VERIFIED_ATOMIC_R2.npz');assert all(np.array_equal(sourcepatch[q],npz[q+'_original_patch_ids']) for q in ['L','R'])
descendants={p.name for p in r.pose.bones['forearm.L'].children_recursive}|{'forearm.L'}
references={};ln=bind(parent.name)
for f in range(288,387):
 s.frame_set(f);bpy.context.view_layer.update();data={n:geom(bpy.data.objects[n]) for n in mesh_names};assert {n:hashlib.sha256(z[0].tobytes()).hexdigest() for n,z in data.items()}==m['all_rows_private'][f-1]['actual_mesh_hash_private']
 references[f]={'data':data,'basis':{p.name:np.array(p.matrix_basis) for p in r.pose.bones},'world':{p.name:np.array(r.matrix_world@p.matrix) for p in r.pose.bones},'q':r.pose.bones['forearm.L'].rotation_quaternion.copy()}
off(ln);assert snapshot(names)==before
def areas(v,t):
 t=np.asarray(t,dtype=int);return np.linalg.norm(np.cross(v[t[:,1]]-v[t[:,0]],v[t[:,2]]-v[t[:,0]]),axis=1)*.5
rows=[];pairledger=[];qold=[];qnew=[];newpairs_peak={k:0 for k in base};footerror={q:0. for q in ['L','R']};ln=bind(a.name)
for f in range(288,387):
 s.frame_set(f);bpy.context.view_layer.update();ref=references[f];data={n:geom(bpy.data.objects[n]) for n in mesh_names};ps,_=contact(data);new={k:ps[k]-base[k] for k in ps};oldpairs={k:{tuple(tuple(t) for t in pair) for pair in vv} for k,vv in ledger['frames'][f-1]['new_pair_identities'].items()};introduced={k:new[k]-oldpairs[k] for k in new}
 for k in new:newpairs_peak[k]=max(newpairs_peak[k],len(introduced[k]))
 bodyv,bodytri,_=data[mesh_names[0]];baseline_v=ref['data'][mesh_names[0]][0];ar=areas(bodyv,bodytri);ar0=areas(baseline_v,bodytri);valid=ar0>1e-10;ratio=ar[valid]/ar0[valid];collapse=int(((ar<1e-12)&(ar0>1e-10)).sum());ratio_low=int((ratio<.1).sum());localothers=max(float(np.abs(np.array(p.matrix_basis)-ref['basis'][p.name]).max()) for p in r.pose.bones if p.name!='forearm.L');unrelatedworld=max(float(np.abs(np.array(r.matrix_world@p.matrix)-ref['world'][p.name]).max()) for p in r.pose.bones if p.name not in descendants)
 q=r.pose.bones['forearm.L'].rotation_quaternion.copy();e0=ref['q'].to_euler('XYZ');e1=q.to_euler('XYZ');otherhinge=max(abs(e1.x-e0.x),abs(e1.y-e0.y));qold.append(ref['q']);qnew.append(q)
 for side,ids in sourcepatch.items():footerror[side]=max(footerror[side],float(np.abs(bodyv[ids]-npz[side][f-1]).max()));assert np.array_equal(bodyv[footids[side]],baseline_v[footids[side]])
 same_head_hair=all(np.array_equal(data[n][0],ref['data'][n][0]) for n in mesh_names[1:]);assert same_head_hair and localothers==0 and unrelatedworld==0 and otherhinge<1e-6
 rows.append({'frame':f,'actual_mesh_hash_private':{n:hashlib.sha256(z[0].tobytes()).hexdigest() for n,z in data.items()},'BODY_new_vs_OFF':len(new[bodykey]),'original_BODY_new_vs_OFF':len(oldpairs[bodykey]),'original_first7_remaining':len(new[bodykey]&initial7),'introduced_vs_same_original_frame':{k:len(v) for k,v in introduced.items()},'finite':True,'new_triangle_area_collapse':collapse,'triangle_area_ratio_below_point1':ratio_low,'minimum_actual_triangle_area_ratio_vs_original':float(ratio.min()),'other_local_joint_max_component_error':localothers,'non_descendant_world_max_component_error':unrelatedworld,'other_hinge_Euler_XY_error_radians':otherhinge,'head_hair_actual_geometry_identical':same_head_hair})
 pairledger.append({'frame':f,'new_pair_identities':{k:sorted(v) for k,v in new.items()},'introduced_pair_identities':{k:sorted(v) for k,v in introduced.items()}})
 if f%12==0:print('TOUR302_LOCAL_ACTUAL',f,len(new[bodykey]),{k:len(v) for k,v in introduced.items()},flush=True)
off(ln);assert snapshot(names)==before
def velocities(qs):
 inc=[(a.rotation_difference(b)).angle*180/math.pi*24 for a,b in zip(qs,qs[1:])];return {'max_angular_velocity_degrees_sec':max(inc),'max_adjacent_angular_velocity_magnitude_jump_degrees_sec':max(abs(b-a) for a,b in zip(inc,inc[1:])),'boundary_velocities_degrees_sec':[inc[0],inc[1],inc[-2],inc[-1]],'per_step_private':inc}
vo=velocities(qold);vn=velocities(qnew);velocitypass=vn['max_angular_velocity_degrees_sec']<=vo['max_angular_velocity_degrees_sec']+1 and vn['max_adjacent_angular_velocity_magnitude_jump_degrees_sec']<=vo['max_adjacent_angular_velocity_magnitude_jump_degrees_sec']+1
passed=all(x['BODY_new_vs_OFF']==0 and not any(x['introduced_vs_same_original_frame'].values()) and x['new_triangle_area_collapse']==0 and x['triangle_area_ratio_below_point1']==0 for x in rows) and not any(footerror.values()) and velocitypass
corrective_name=a.name;candidate=O/'Character_R4_Tour302_LEFT_ELBOW_C1_OFF_20261005.blend';bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=False);bpy.ops.wm.open_mainfile(filepath=str(candidate),use_scripts=False);assert snapshot(names)==before
reopened=record(bpy.data.actions[corrective_name]);assert reopened==new_records, 'Serialized modified Action differs'
with gzip.open(O/'LOCAL_SURFACE_IDENTITIES_PRIVATE_C1.json.gz','wt',encoding='utf8') as ff:json.dump(pairledger,ff)
meta={'source_SHA':m['source_SHA'],'source_Action_SHA':m['source_Action_SHA'],'parent_candidate_SHA':m['candidate_SHA'],'candidate':str(candidate),'candidate_SHA':sha(candidate),'candidate_bytes':candidate.stat().st_size,'corrective_action':corrective_name,'preserved81_signature_private':before,'original78_signature_private':m['original78_signature_private'],'clock':[1,769],'fps':24,'changed_key_frames':modified,'local_QA_frames':[288,386],'gesture_zero_boundaries':[289,385],'source_peak_hinge_degrees':source_peak,'candidate_peak_hinge_degrees':safe,'hinge_scale':scale,'only_forearmL_EulerZ_changed':True,'outside_key_handles_exact':outside_equal,'other_body_curves_exact':others_equal,'local_rows_private':rows,'introduced_new_pair_identity_peaks':newpairs_peak,'support_patch_component_error_m':footerror,'original_velocity':vo,'candidate_velocity':vn,'angular_velocity_jump_gate':velocitypass,'scoped_local_QA_pass':passed,'first_local_failure':next((x for x in rows if x['BODY_new_vs_OFF'] or any(x['introduced_vs_same_original_frame'].values()) or x['new_triangle_area_collapse'] or x['triangle_area_ratio_below_point1']),None),'whole_Tour_source_acceptance':'HOLD wrists472 and other original head/hair contacts untouched','TierP':0}
(O/'TOUR302_ELBOW_C1_PRIVATE.json').write_text(json.dumps(meta,indent=2),encoding='utf8');assert sha(m['candidate'])==m['candidate_SHA'] and sha(m['source'])==m['source_SHA'];print('TOUR302_ONE_CANDIDATE_LOCAL_DATA_COMPLETE',passed,'first',meta['first_local_failure'],'velocity',vo['max_adjacent_angular_velocity_magnitude_jump_degrees_sec'],vn['max_adjacent_angular_velocity_magnitude_jump_degrees_sec'],flush=True)
