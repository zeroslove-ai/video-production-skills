"""ONE left wrist twist-only native Action copy; unchanged swing/pivot/time and immutable source."""
import bpy,sys,json,gzip,hashlib,math,ast
from pathlib import Path
import numpy as np
from mathutils import Quaternion,Vector
from mathutils.bvhtree import BVHTree
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot,props
from r4_appearance_adapter import ReactionLane
from r4_native_tour_adapter_r1 import ACTIONS
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-tour472-wrist-w1b';O.mkdir(exist_ok=False);m=json.loads((B/'alpha-native-tour-recovery-r2/NATIVE_TOUR_RECOVERY_PRIVATE_R2.json').read_bytes());it=json.loads((B/'alpha-tour472-wrist-intake-r1/TOUR472_WRIST_INTAKE_PRIVATE_R1.json').read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(m['candidate'])==m['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=m['candidate'],use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered'];names=list(bpy.data.actions.keys());before=snapshot(names);assert len(names)==81
for fn,defs in [('r4_native_walk_source_supply_r1.py',['contact']),('r4_existing_reach_contact_closure_r1.py',['geom']),('r4_tour302_softcap_c2.py',['curves','record','bind','off','areas','velocities'])]:
 tree=ast.parse((H/fn).read_text(encoding='utf8'));exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in defs],type_ignores=[]),'<existing_exact_helpers>','exec'))
fixed={};mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4'];ledger=json.loads(gzip.open(B/'alpha-native-tour-source-r4/NATIVE_TOUR_SURFACE_IDENTITIES_PRIVATE_R1.json.gz','rt',encoding='utf8').read());base={k:{tuple(tuple(t) for t in p) for p in vv} for k,vv in ledger['baseline'].items()};bodykey=body.name+'__self_nonadjacent';region=set(it['region_vertex_ids_private']);target_pairs={tuple(tuple(t) for t in p) for p in next(x for x in it['contact_rows_private'] if x['frame']==472)['left_wrist_pairs_private']};parent=bpy.data.actions[ACTIONS[r.name]];original_records=record(parent);a=parent.copy();a.name='YURI_R4_NATIVE_TOUR_LEFT_WRIST_TWIST_W1';a.use_fake_user=True;path='pose.bones["hand.L"].rotation_quaternion';fcs={f.array_index:f for f in curves(a) if f.data_path==path};assert set(fcs)=={0,1,2,3};modified=[]
def decompose(q):
 q=q.normalized();tw=Quaternion((q.w,0,q.y,0)).normalized();return q@tw.conjugated(),tw,2*math.atan2(tw.y,tw.w)
for f in range(455,491):
 q=Quaternion([fcs[k].evaluate(f) for k in range(4)]);swing,tw,theta=decompose(q);deg=abs(theta)*180/math.pi
 if deg<=75:continue
 t=min(1.,(deg-75)/20);newdeg=85-10*(1-t)**2;nq=swing@Quaternion(Vector((0,1,0)),math.copysign(newdeg*math.pi/180,theta))
 if nq.dot(q)<0:nq.negate()
 for k in range(4):
  p=next(p for p in fcs[k].keyframe_points if p.co.x==f);assert p.interpolation=='LINEAR';delta=nq[k]-p.co.y;p.co.y=nq[k];p.handle_left.y+=delta;p.handle_right.y+=delta
 modified.append(f)
for fc in fcs.values():
 fc.update()
 for p,rr in zip(fc.keyframe_points,original_records[(fc.data_path,fc.array_index)]['points']):
  if rr[0][0] not in modified:p.co=rr[0];p.handle_left=rr[1];p.handle_right=rr[2]
new_records=record(a)
for key,rr in original_records.items():
 nn=new_records[key]
 if key[0]!=path:assert rr==nn
 else:
  assert rr['extrapolation']==nn['extrapolation'] and rr['modifiers']==nn['modifiers']
  for x,y in zip(rr['points'],nn['points']):
   assert x[0][0]==y[0][0] and x[3:]==y[3:]
   if x[0][0] not in modified:assert x==y
neutral=geom(body)[0];gn={g.index:g.name for g in body.vertex_groups};footids={q:np.array([v.index for v in body.data.vertices if sum(g.weight for g in v.groups if gn[g.group] in ['foot.'+q,'toe.'+q])>.5],int) for q in ['L','R']};handids=np.array([v.index for v in body.data.vertices if sum(g.weight for g in v.groups if gn[g.group]=='hand.L')>.5],int);descendants={p.name for p in r.pose.bones['hand.L'].children_recursive}|{'hand.L'};rows=[];pairs=[];qo=[];qn=[];peaks={k:0 for k in base};footerror=0
for f in range(453,493):
 ln=bind(parent.name);s.frame_set(f);bpy.context.view_layer.update();orig={n:geom(bpy.data.objects[n]) for n in mesh_names};assert {n:hashlib.sha256(z[0].tobytes()).hexdigest() for n,z in orig.items()}==m['all_rows_private'][f-1]['actual_mesh_hash_private'];ref={'data':orig,'basis':{p.name:np.array(p.matrix_basis) for p in r.pose.bones},'world':{p.name:np.array(r.matrix_world@p.matrix) for p in r.pose.bones},'q':r.pose.bones['hand.L'].rotation_quaternion.copy()};off(ln)
 ln=bind(a.name);s.frame_set(f);bpy.context.view_layer.update();data={n:geom(bpy.data.objects[n]) for n in mesh_names};ps,_=contact(data);new={k:ps[k]-base[k] for k in ps};old={k:{tuple(tuple(t) for t in p) for p in vv} for k,vv in ledger['frames'][f-1]['new_pair_identities'].items()};introduced={k:new[k]-old[k] for k in new}
 for k in peaks:peaks[k]=max(peaks[k],len(introduced[k]))
 localothers=max(float(np.abs(np.array(p.matrix_basis)-ref['basis'][p.name]).max()) for p in r.pose.bones if p.name!='hand.L');worldothers=max(float(np.abs(np.array(r.matrix_world@p.matrix)-ref['world'][p.name]).max()) for p in r.pose.bones if p.name not in descendants);q=r.pose.bones['hand.L'].rotation_quaternion.copy();sw0,tw0,_=decompose(ref['q']);sw1,tw1,_=decompose(q);swing_error=sw0.rotation_difference(sw1).angle*180/math.pi;qo.append(ref['q']);qn.append(q);bv,tri,_=data[body.name];vref=ref['data'][body.name][0];ar=areas(bv,tri);ar0=areas(vref,tri);valid=ar0>1e-10;ratio=ar[valid]/ar0[valid];collapse=int(((ar<1e-12)&valid).sum());finite=all(np.isfinite(z[0]).all() for z in data.values());pivoterror=float(np.abs(np.array((r.matrix_world@r.pose.bones['hand.L'].matrix).translation)-ref['world']['hand.L'][:3,3]).max());same_headhair=all(np.array_equal(data[n][0],ref['data'][n][0]) for n in mesh_names[1:]);assert finite and localothers==0 and worldothers==0 and pivoterror==0 and same_headhair and swing_error<.01
 for side,ids in footids.items():footerror=max(footerror,float(np.abs(bv[ids]-vref[ids]).max()))
 if f not in modified:assert all(np.array_equal(data[n][0],ref['data'][n][0]) for n in mesh_names)
 wristpairs={p for p in new[bodykey] if all(i in region for t in p for i in t)};oldwrist={p for p in old[bodykey] if all(i in region for t in p for i in t)};rows.append({'frame':f,'actual_mesh_hash_private':{n:hashlib.sha256(z[0].tobytes()).hexdigest() for n,z in data.items()},'left_wrist_pairs':len(wristpairs),'original_left_wrist_pairs':len(oldwrist),'f472_original14_remaining':len(new[bodykey]&target_pairs),'BODY_new_vs_OFF':len(new[bodykey]),'original_BODY_new_vs_OFF':len(old[bodykey]),'introduced_vs_same_original_frame':{k:len(v) for k,v in introduced.items()},'finite':bool(finite),'area_collapse':collapse,'area_ratio_below_point1':int((ratio<.1).sum()),'minimum_area_ratio':float(ratio.min()),'swing_angle_error_degrees':swing_error,'wrist_orientation_change_degrees':ref['q'].rotation_difference(q).angle*180/math.pi,'wrist_pivot_component_error_m':pivoterror,'palm_centroid_change_m':float(np.linalg.norm(bv[handids].mean(axis=0)-vref[handids].mean(axis=0))),'other_local_joints_error':localothers,'non_descendant_world_error':worldothers,'head_hair_identical':same_headhair});pairs.append({'frame':f,'new_pair_identities':{k:sorted(v) for k,v in new.items()},'introduced_pair_identities':{k:sorted(v) for k,v in introduced.items()}});off(ln);del orig,ref,data
assert snapshot(names)==before and footerror==0;vo=velocities(qo);vn=velocities(qn);vg=vn['max_angular_velocity_degrees_sec']<=vo['max_angular_velocity_degrees_sec']+1 and vn['max_adjacent_angular_velocity_magnitude_jump_degrees_sec']<=vo['max_adjacent_angular_velocity_magnitude_jump_degrees_sec']+1
passed=not any(peaks.values()) and all(x['left_wrist_pairs']==0 and not x['area_collapse'] and not x['area_ratio_below_point1'] for x in rows) and vg
candidate=O/'Character_R4_Tour472_LEFT_WRIST_TWIST_W1_OFF_20261005.blend';name=a.name;a['source_Action_SHA']=m['source_Action_SHA'];a['scope']='ONE LEFT wrist localY twist softcap75..95 cap85, source swing/pivot/clock455..490 only; wholeTour HOLD';bpy.ops.wm.save_as_mainfile(filepath=str(candidate),relative_remap=False);bpy.ops.wm.open_mainfile(filepath=str(candidate),use_scripts=False);assert snapshot(names)==before and record(bpy.data.actions[name])==new_records
with gzip.open(O/'LOCAL_SURFACE_IDENTITIES_PRIVATE_W1.json.gz','wt',encoding='utf8') as ff:json.dump(pairs,ff)
meta={'source_SHA':m['source_SHA'],'source_Action_SHA':m['source_Action_SHA'],'parent_candidate_SHA':m['candidate_SHA'],'candidate':str(candidate),'candidate_SHA':sha(candidate),'corrective_action':name,'preserved81_signature_private':before,'changed_key_frames':modified,'local_QA_frames':[453,492],'native_phrase':[454,491],'fps':24,'twist_softcap_degrees':[75,85,95],'swing_preserved':True,'other_curves_outside_keys_handles_exact':True,'rows_private':rows,'introduced_pair_identity_peaks':peaks,'foot_component_error_m':footerror,'original_velocity':vo,'candidate_velocity':vn,'angular_velocity_jump_gate':vg,'scoped_left_wrist_QA_pass':passed,'whole_Tour':'HOLD untouched right wrist/headhair/clavicle','TierP':0}
(O/'TOUR472_WRIST_W1_PRIVATE.json').write_text(json.dumps(meta,indent=2),encoding='utf8');assert sha(m['candidate'])==m['candidate_SHA'] and sha(m['source'])==m['source_SHA'];print('TOUR472_ONE_LEFT_WRIST_W1_LOCAL_QA_COMPLETE',passed,'newpairs',peaks,flush=True)
