"""Read-only correction localization and raw source/candidate OFF reopening verification."""
import bpy,sys,json,hashlib
from pathlib import Path
import numpy as np
from mathutils.bvhtree import BVHTree
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'dance03-constrained-readonly-c1b';O.mkdir(exist_ok=False);R=B/'dance03-constrained-native-c1'
d=json.loads((R/'DANCE03_CONSTRAINED_PRIVATE_MANIFEST_C1.json').read_bytes());P=Path(d['source']);C=Path(d['candidate']);L=Path(d['action_only_library']['file']);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
pins={str(p):sha(p) for p in [P,C,L,*R.glob('*.png')]}
bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);names=list(bpy.data.actions.keys());before=snapshot(names);body=bpy.data.objects['Meshy_Body_NeutralCovered']
def geom():
 e=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();m.calc_loop_triangles();v=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',v);w=np.array(e.matrix_world);v=v.reshape(-1,3).astype(float)@w[:3,:3].T+w[:3,3];t=[tuple(x.vertices) for x in m.loop_triangles];edges=np.array([tuple(x.vertices) for x in m.edges],int);e.to_mesh_clear();return v,t,edges
v0,t0,edges=geom()
with bpy.data.libraries.load(str(L),link=False) as (aa,bb):assert len(aa.actions)==1 and not aa.objects and not aa.meshes and not aa.armatures;bb.actions=list(aa.actions)
assert snapshot(names)==before
lane=ReactionLane();lane.on(next(iter(d['action_names'].values())));v,t,_=geom()
groups={g.index:g.name for g in body.vertex_groups};selected=[g.index for g in body.vertex_groups if g.name.endswith('.L') and any(g.name.startswith(x) for x in ['clavicle','upper_arm','forearm','hand','thumb','index','middle','ring','pinky'])]
verts={x.index for x in body.data.vertices if sum(g.weight for g in x.groups if g.group in selected)>.01};ids=[i for i,x in enumerate(t) if any(j in verts for j in x)];a=BVHTree.FromPolygons(v.tolist(),[t[i] for i in ids],all_triangles=True,epsilon=0);alltree=BVHTree.FromPolygons(v.tolist(),t,all_triangles=True,epsilon=0);pairs=set()
for i,j in a.overlap(alltree):
 x=t[ids[i]];y=t[j]
 if not set(x)&set(y):pairs.add(tuple(sorted([tuple(sorted(x)),tuple(sorted(y))])))
def topweights(indices):
 sums={}
 for i in indices:
  for g in body.data.vertices[i].groups:
   if g.weight>.001:sums[groups[g.group]]=sums.get(groups[g.group],0)+g.weight
 return sorted(sums.items(),key=lambda x:-x[1])[:5]
points=sorted({i for x,y in pairs for i in (*x,*y)});bbox=[v[points].min(axis=0).tolist(),v[points].max(axis=0).tolist()] if points else None
pairrows=[{'triangles':[list(x),list(y)],'world_centroid_m':v[list((*x,*y))].mean(axis=0).tolist(),'dominant_weight_sums':topweights(set((*x,*y)))} for x,y in pairs]
old=np.linalg.norm(v0[edges[:,0]]-v0[edges[:,1]],axis=1);new=np.linalg.norm(v[edges[:,0]]-v[edges[:,1]],axis=1);valid=old>1e-6;idx=np.flatnonzero(valid);ratios=new[valid]/old[valid];extreme=[]
for j in [idx[np.argmax(ratios)],idx[np.argmin(ratios)]]:
 extreme.append({'vertex_indices':edges[j].tolist(),'source_edge_length_m':float(old[j]),'posed_edge_length_m':float(new[j]),'ratio':float(new[j]/old[j]),'posed_midpoint_m':v[edges[j]].mean(axis=0).tolist(),'dominant_weights':topweights(edges[j])})
contact_weights=topweights(points)
lane.off();assert snapshot(names)==before
bpy.ops.wm.open_mainfile(filepath=str(C),use_scripts=False);cand=snapshot(names);diff=[k for k in before if before[k]!=cand[k]];assert not diff;assert all(sha(p)==h for p,h in pins.items())
report={'task':'ROOT_PM_DANCE03_CONSTRAINED_NATIVE_CORRECTION_R1','input_pins':pins,'source_Action_library_import_ON_OFF_full_snapshot_equal':True,'candidate_raw_reopened_OFF_snapshot_equal':True,'candidate_raw_filepath_difference_categories':diff,'left_arm_nonadjacent_actual_count':len(pairs),'left_arm_contact_bounds_world_m':bbox,'left_arm_contact_dominant_groups':contact_weights,'actual_contact_pairs_private':pairrows,'edge_extremes':extreme,'candidate_bytes_unchanged':True,'no_new_pose_no_rerender':True,'verdict':'FAIL_HOLD_LEFT_ARM_METHOD_STOP','TierP':0}
(O/'READONLY_LOCALIZATION_OFF_PRIVATE_C1.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('CONSTRAINED03_READONLY_LEFT_CONTACT',len(pairs),contact_weights,'EDGE_EXTREMES',extreme,'RAW_OFF_EQUAL',flush=True)
