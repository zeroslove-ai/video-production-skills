"""Exhaustive61 existing C1 Reach contact/deformation closure, source-only read-only."""
import bpy,sys,json,hashlib,math
from pathlib import Path
import numpy as np
from mathutils.bvhtree import BVHTree
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'c1-existing-reach-contact-closure-r1';O.mkdir(exist_ok=False)
d=json.loads((B/'alpha-c1-reach-candidate-r1/C1_REACH_CANDIDATE_PRIVATE_R1.json').read_bytes());P=Path(d['source']);C=Path(d['candidate']);L=B/'alpha-c1-reach-off-qa-r1/YURI_R4_C1_REACH_ACTIONS_ONLY_R1.blend';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(P)==d['source_SHA']=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa';assert sha(C)==d['candidate_SHA']=='bad645ae396ebef88564e4b3656f5e73c9375a9b87ee217acbd87a1354964946'
pins={str(p):sha(p) for p in [P,C,L]};bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);s=bpy.context.scene;rig=bpy.data.objects['Meshy_Fitted_Rig'];names=list(bpy.data.actions.keys());source_sig=snapshot(names);source_tex={i.name:(i.filepath,i.filepath_raw,[hashlib.sha256(x.packed_file.data).hexdigest() for x in i.packed_files]) for i in bpy.data.images if i.type!='RENDER_RESULT'}
fixed={};body=None;verts={};regions={};groupnames={};bonegroups={}
def setup():
 global body,verts,regions,groupnames,bonegroups
 body=bpy.data.objects['Meshy_Body_NeutralCovered'];groupnames={g.index:g.name for g in body.vertex_groups};bonegroups={g.index:g.name for g in body.vertex_groups if g.name in bpy.data.objects['Meshy_Fitted_Rig'].pose.bones}
 def cohort(gs):
  idx={body.vertex_groups[n].index for n in gs};return {v.index for v in body.data.vertices if sum(g.weight for g in v.groups if g.group in idx)>.01}
 verts={side:cohort([n+'.'+side for n in ['clavicle','upper_arm','forearm','hand']]+[n+str(j)+'.'+side for n in ['thumb','index','middle','ring','pinky'] for j in [1,2,3]]) for side in ['L','R']}
 regions={n+'.'+side:cohort([n+'.'+side]) for n in ['clavicle','upper_arm','forearm'] for side in ['L','R']}
def geom(obj):
 e=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();m.calc_loop_triangles();a=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',a);w=np.array(e.matrix_world);a=a.reshape(-1,3).astype(float)@w[:3,:3].T+w[:3,3];t=[tuple(x.vertices) for x in m.loop_triangles];ed=np.array([tuple(x.vertices) for x in m.edges],int);poly=[tuple(x.vertices) for x in m.polygons];assert np.isfinite(a).all()
 if obj.name not in fixed:fixed[obj.name]=(len(a),poly)
 else:assert fixed[obj.name]==(len(a),poly)
 e.to_mesh_clear();return a,t,ed
def evaluate():
 v,t,ed=geom(body);h,ht,_=geom(bpy.data.objects['Character_Body_Head']);hair,hairt,_=geom(bpy.data.objects['Hair_Replacement_R4'])
 return v,t,ed,h,ht,hair,hairt
def contacts(data):
 v,t,ed,h,ht,hair,hairt=data;alltree=BVHTree.FromPolygons(v.tolist(),t,all_triangles=True,epsilon=0);htree=BVHTree.FromPolygons(h.tolist(),ht,all_triangles=True,epsilon=0);hairtree=BVHTree.FromPolygons(hair.tolist(),hairt,all_triangles=True,epsilon=0);sets={};counts={}
 for side in ['L','R']:
  ids=[i for i,x in enumerate(t) if any(j in verts[side] for j in x)];tree=BVHTree.FromPolygons(v.tolist(),[t[i] for i in ids],all_triangles=True,epsilon=0);non=set();adj=set();same=set()
  for i,j in tree.overlap(alltree):
   x=t[ids[i]];y=t[j];key=tuple(sorted([tuple(sorted(x)),tuple(sorted(y))]))
   if set(x)==set(y):same.add(key)
   elif set(x)&set(y):adj.add(key)
   else:non.add(key)
  sets[side+'__all_body_nonadjacent']=non;counts[side]={'triangles':len(ids),'nonadjacent_all_body':len(non),'shared_vertex_adjacent_raw':len(adj),'identical_triangle_raw':len(same)}
  for label,other,tri in [('head',htree,ht),('hair',hairtree,hairt)]:
   pairs={(tuple(sorted(t[ids[i]])),tuple(sorted(tri[j]))) for i,j in tree.overlap(other)};sets[side+'__'+label]=pairs;counts[side][label+'_intersections']=len(pairs)
 return counts,sets
def fingerprint(data):return hashlib.sha256(b''.join(x.tobytes() for x in [data[0],data[3],data[5]])).hexdigest()
def topweights(indices):
 scores={}
 for i in indices:
  for g in body.data.vertices[int(i)].groups:
   if g.group in bonegroups and g.weight>.001:scores[bonegroups[g.group]]=scores.get(bonegroups[g.group],0)+g.weight
 return sorted(scores.items(),key=lambda x:-x[1])[:6]
def locations(data,pairs):
 v,t,ed,h,ht,hair,hairt=data;out={}
 for key,ps in pairs.items():
  if not ps:out[key]={'count':0};continue
  idx=sorted({i for a,b in ps for i in (a if '__head' in key or '__hair' in key else (*a,*b))});g=topweights(idx)
  distribution={}
  if key.endswith('nonadjacent'):
   for a,b in ps:
    ga=topweights(a);gb=topweights(b);tag='__'.join(sorted([ga[0][0] if ga else 'unknown',gb[0][0] if gb else 'unknown']));distribution[tag]=distribution.get(tag,0)+1
  out[key]={'count':len(ps),'body_vertices':len(idx),'world_bounds_m':[data[0][idx].min(axis=0).tolist(),data[0][idx].max(axis=0).tolist()],'dominant_bone_weight_sums':g,'pair_anatomical_ranking':sorted(distribution.items(),key=lambda x:-x[1]),'exact_triangle_identities_private':[[list(a),list(b)] for a,b in sorted(ps)]}
 return out
setup();neutral=evaluate();baseline_cache={};source_baselines={}
for f in range(1,62):
 s.frame_set(f);bpy.context.view_layer.update();data=evaluate();key=fingerprint(data)
 if key not in baseline_cache:baseline_cache[key]=contacts(data)
 source_baselines[f]=baseline_cache[key]
s.frame_set(1);bpy.context.view_layer.update();assert snapshot(names)==source_sig
# Native ORIGINAL Reach comparison is normalized phase, not same target/source/choreography.
native=[];lane=ReactionLane();lane.on('MESHY_R2_BODY_Reach')
for f in range(1,62):
 phaseframe=1+(f-1)*96/60;s.frame_set(int(phaseframe),subframe=phaseframe-int(phaseframe));bpy.context.view_layer.update();data=evaluate();co,ps=contacts(data);native.append({'sample':f,'native_source_frame':phaseframe,'counts':co,'sets':ps,'locations':locations(data,ps)})
 if f%10==1:print('ORIGINAL_NATIVE_REACH_CONTACT',f,{k:len(v) for k,v in ps.items()},flush=True)
lane.off();assert snapshot(names)==source_sig
bpy.ops.wm.open_mainfile(filepath=str(C),use_scripts=False);s=bpy.context.scene;rig=bpy.data.objects['Meshy_Fitted_Rig'];setup();candidate_sig=snapshot(names);rawdiff=[k for k in source_sig if source_sig[k]!=candidate_sig[k]];assert all(k=='textures' for k in rawdiff)
packed_equal=all(source_tex[i.name][2]==[hashlib.sha256(x.packed_file.data).hexdigest() for x in i.packed_files] for i in bpy.data.images if i.type!='RENDER_RESULT')
source_paths={n:(a,b) for n,(a,b,_) in source_tex.items()};candidate_paths={i.name:(i.filepath,i.filepath_raw) for i in bpy.data.images if i.type!='RENDER_RESULT'};pathdiff={n:{'source':source_paths[n],'candidate':candidate_paths[n]} for n in source_paths if source_paths[n]!=candidate_paths[n]}
oldv=neutral[0];edges=neutral[2];oldlen=np.linalg.norm(oldv[edges[:,0]]-oldv[edges[:,1]],axis=1);valid=oldlen>1e-6
region_edges={n:np.array([j for j,x in enumerate(edges) if valid[j] and any(int(i) in ids for i in x)],int) for n,ids in regions.items()}
lanes=[]
for obj in ['Meshy_Fitted_Rig','Armature','Hair_Rig_R4']:
 q=ReactionLane(obj);q.on(d['additive_body_actions'][obj]);lanes.append(q)
root=bpy.data.objects['Assembly_Root'];ad=root.animation_data;save={'had_ad':ad is not None,'action':ad.action if ad else None,'slot':ad.action_slot if ad else None,'handle':ad.action_slot_handle if ad else 0,'last':ad.last_slot_identifier if ad else '', 'loc':root.location.copy()}
ad=root.animation_data_create();ad.action=bpy.data.actions[d['additive_body_actions']['Assembly_Root']];ad.action_slot=ad.action.slots[0]
rows=[];mapped_joint_records=[]
for f in range(1,62):
 s.frame_set(f);bpy.context.view_layer.update();data=evaluate();co,ps=contacts(data);baseco,baseps=source_baselines[f];new={k:len(v-baseps[k]) for k,v in ps.items()};native_counts={k:len(v) for k,v in native[f-1]['sets'].items()};new_native={k:len(v-native[f-1]['sets'][k]) for k,v in ps.items()}
 v=data[0];length=np.linalg.norm(v[edges[:,0]]-v[edges[:,1]],axis=1);rat=length[valid]/oldlen[valid];deform={}
 for n,ids in region_edges.items():
  ratio=length[ids]/oldlen[ids];mx=ids[int(np.argmax(ratio))];mn=ids[int(np.argmin(ratio))]
  deform[n]={'p01_p99':np.quantile(ratio,[.01,.99]).tolist(),'min_ratio':float(ratio.min()),'max_ratio':float(ratio.max()),'max_ratio_edge':{'indices':edges[mx].tolist(),'source_m':float(oldlen[mx]),'posed_m':float(length[mx]),'world_midpoint_m':v[edges[mx]].mean(axis=0).tolist(),'dominant_bones':topweights(edges[mx])},'min_ratio_edge':{'indices':edges[mn].tolist(),'source_m':float(oldlen[mn]),'posed_m':float(length[mn]),'world_midpoint_m':v[edges[mn]].mean(axis=0).tolist(),'dominant_bones':topweights(edges[mn])}}
 joints={n:{'quaternion_delta_degrees':math.degrees(rig.pose.bones[n].rotation_quaternion.angle),'world_head_m':list(rig.matrix_world@rig.pose.bones[n].head),'world_tail_m':list(rig.matrix_world@rig.pose.bones[n].tail)} for n in ['clavicle.L','upper_arm.L','forearm.L','clavicle.R','upper_arm.R','forearm.R']}
 row={'frame':f,'time_seconds':(f-1)/30,'finite':True,'topology_equal':True,'counts':co,'new_vs_source_OFF':new,'source_OFF_counts':baseco,'native_original_normalized_phase_counts':native_counts,'new_vs_native_original_phase_identity':new_native,'locations_private':locations(data,ps),'deformation_regions':deform,'all_edge_ratio_p01_p99':np.quantile(rat,[.01,.99]).tolist(),'joints_private':joints}
 rows.append(row);print('EXISTING_C1_FULL_CONTACT',f,new,{k:(round(x['min_ratio'],4),round(x['max_ratio'],4)) for k,x in deform.items()},flush=True)
for q in reversed(lanes):q.off()
ad=root.animation_data;ad.action=save['action']
if save['action'] and save['slot']:ad.action_slot=save['slot']
ad.action_slot_handle=save['handle'];ad.last_slot_identifier=save['last'];root.location=save['loc']
if not save['had_ad']:root.animation_data_clear()
bpy.context.view_layer.update();assert snapshot(names)==candidate_sig
# Raw path restoration explicit/transient: original source strings then strict source equality; restore candidate strings again.
for n,(a,b) in source_paths.items():bpy.data.images[n].filepath=a;bpy.data.images[n].filepath_raw=b
normalized_snapshot=snapshot(names);normalized_diff=[k for k in source_sig if source_sig[k]!=normalized_snapshot[k]];assert not normalized_diff
for n,(a,b) in candidate_paths.items():bpy.data.images[n].filepath=a;bpy.data.images[n].filepath_raw=b
assert snapshot(names)==candidate_sig;assert all(sha(p)==h for p,h in pins.items())
# Source-native comparison evidence serialized without Python sets.
native_public=[{k:v for k,v in x.items() if k!='sets'} for x in native]
ranking=sorted([{'frame':x['frame'],'time_seconds':x['time_seconds'],'new_nonadjacent_body_total_overlapping_cohorts':sum(v for k,v in x['new_vs_source_OFF'].items() if k.endswith('nonadjacent')),'head_hair_total_overlapping_cohorts':sum(v for k,v in x['new_vs_source_OFF'].items() if not k.endswith('nonadjacent')),'max_region_edge_ratio':max(v['max_ratio'] for v in x['deformation_regions'].values())} for x in rows],key=lambda x:(-x['new_nonadjacent_body_total_overlapping_cohorts'],-x['max_region_edge_ratio']))
meta={'task':'ROOT_PM_EXISTING_REACH_CONTACT_CLOSURE_R1','source':str(P),'source_SHA':sha(P),'candidate':str(C),'candidate_SHA':sha(C),'Action_library':{'file':str(L),'sha256':sha(L),'bytes':L.stat().st_size,'actions':4,'objects':0,'meshes':0,'armatures':0},'input_pins':pins,'frames':[1,61],'fps':30,'source_OFF_evaluated_samples':61,'source_OFF_unique_mesh_fingerprints':len(baseline_cache),'original_native_Reach_phase_diagnostic':{'frames':61,'native_frame_range':[1,97],'different_motion_and_targets':True,'phase_normalized_for_diagnostic_only_not_same_kinematic_target':True,'rows_private':native_public},'candidate_ON_OFF_full_raw_snapshot_equal':True,'original78Actions_preserved':len(names)==78,'source_raw_candidate_snapshot_difference_categories':rawdiff,'texture_locator_string_difference_count':len(pathdiff),'texture_locator_string_differences':pathdiff,'packed_bytes_equal':packed_equal,'source_path_transient_normalization_remaining_differences':normalized_diff,'candidate_raw_paths_restored_again':True,'no_save_no_rerender_no_pose_candidate':True,'rows_private':rows,'ranking':ranking,'verdict':'FAIL_HOLD_NONADJACENT_SURFACE_DEFECT' if any(any(v>0 for v in x['new_vs_source_OFF'].values()) for x in rows) else 'SCOPED_61_CONTACT_PASS_DEFORMATION_REVIEW_PENDING','scope':'Actual evaluated weak-weight ANY relevant arm/hand/digit vertex sum>.01 triangles vs ALL body/head/hair. Same/shared vertices raw separated; nonadjacent identities compared sourceOFF eachsample. Cohorts overlap; rank totals are prioritization only. No volumetric containment/adjacent deformation/physical MUG/F2/TierP/Unity certification. No source geometry/weights/material/driver changes. Native original Reach is another motion, not same trajectory ground truth.','TierP':0}
(O/'EXISTING_REACH_CONTACT_CLOSURE_PRIVATE_R1.json').write_text(json.dumps(meta,indent=2),encoding='utf8');print('EXISTING_REACH_CONTACT_CLOSURE_DONE',meta['verdict'],ranking[:5],flush=True)
