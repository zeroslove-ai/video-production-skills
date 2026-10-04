"""Exact same-frame ON/OFF triangle-pair sets, timing-only derivative, all61 frames."""
import bpy,json,sys,hashlib,itertools
from pathlib import Path
import numpy as np
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_reach_left_finger_timing_adapter_r2 import ReachFingerLane
from r4_appearance_signature import snapshot
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-reach-left-finger-timing-paired-qa-r2';O.mkdir(exist_ok=False);d=json.loads((B/'alpha-reach-left-finger-timing-candidate-r2/REACH_LEFT_FINGER_TIMING_CANDIDATE_PRIVATE_R2.json').read_bytes());P=Path(d['candidate']);assert hashlib.sha256(P.read_bytes()).hexdigest()==d['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);original=[a.name for a in bpy.data.actions];before=snapshot(original);body=bpy.data.objects['Meshy_Body_NeutralCovered'];digits=['index','middle','ring','pinky','thumb'];lookup={body.vertex_groups[n+str(j)+'.L'].index:n for n in digits for j in [1,2,3]};cohorts={n:set() for n in digits}
for v in body.data.vertices:
 scores={n:0 for n in digits}
 for g in v.groups:
  if g.group in lookup:scores[lookup[g.group]]+=g.weight
 n=max(scores,key=scores.get)
 if scores[n]>=.5:cohorts[n].add(v.index)
hand=body.vertex_groups['hand.L'].index;excluded={v.index for v in body.data.vertices if any((g.group in lookup or g.group==hand) and g.weight>.01 for g in v.groups)}
def capture():
 e=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();m.calc_loop_triangles();xyz=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',xyz);xyz=xyz.reshape(-1,3);assert np.isfinite(xyz).all();tri=[tuple(t.vertices) for t in m.loop_triangles];trees={};ids={}
 for n in digits:
  ids[n]=[i for i,t in enumerate(tri) if all(v in cohorts[n] for v in t)];trees[n]=BVHTree.FromPolygons(xyz.tolist(),[tri[i] for i in ids[n]],all_triangles=True,epsilon=0)
 ids['body_other']=[i for i,t in enumerate(tri) if all(v not in excluded for v in t)];trees['body_other']=BVHTree.FromPolygons(xyz.tolist(),[tri[i] for i in ids['body_other']],all_triangles=True,epsilon=0)
 pairs={a+'__'+b:{(ids[a][i],ids[b][j]) for i,j in trees[a].overlap(trees[b])} for a,b in [*itertools.combinations(digits,2),*[(n,'body_other') for n in digits]]};e.to_mesh_clear();return pairs
base=[];lane=ReachFingerLane();lane.on(include_fingers=False)
for f in range(1,62):bpy.context.scene.frame_set(f);bpy.context.view_layer.update();base.append(capture())
lane.off();assert snapshot(original)==before;rows=[];lane=ReachFingerLane();lane.on()
for f in range(1,62):
 bpy.context.scene.frame_set(f);bpy.context.view_layer.update();on=capture();off=base[f-1];rows.append({'frame':f,'pairs':{n:{'OFF':len(off[n]),'ON':len(on[n]),'new_triangle_pairs':len(on[n]-off[n]),'removed_triangle_pairs':len(off[n]-on[n]),'count_increase':len(on[n])-len(off[n])} for n in on}})
lane.off();assert snapshot(original)==before and hashlib.sha256(P.read_bytes()).hexdigest()==d['candidate_SHA'];summary={n:{'baseline_max':max(x[n].__len__() for x in base),'ON_max':max(x['pairs'][n]['ON'] for x in rows),'max_new_triangle_pairs':max(x['pairs'][n]['new_triangle_pairs'] for x in rows),'new_pair_frames':[x['frame'] for x in rows if x['pairs'][n]['new_triangle_pairs']>0],'max_count_increase':max(x['pairs'][n]['count_increase'] for x in rows)} for n in base[0]};clean=all(x['max_new_triangle_pairs']==0 for x in summary.values());report={'candidate_SHA':d['candidate_SHA'],'source_SHA':d['source_SHA'],'frames':61,'same_frame_pair_identity_comparison':True,'pairs':summary,'frames_private':rows,'added_intersections_subset':'PASS' if clean else 'FAIL','C1_baseline_collision':'FAIL_HOLD','original_neutral_return':'HOLD','OFF_snapshot_exact':True,'scope':'Actual evaluated epsilon0 triangle intersections, identical topology IDs, dominant digit weight>=.5, other body excludes left finger/hand weight>.01; pair counts not depth/volume/full character certification','TierP':0};(O/'PAIRED_SURFACE_ORACLE_PRIVATE_R2.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print('TIMING_PAIRED_ORACLE',clean,summary,flush=True)
