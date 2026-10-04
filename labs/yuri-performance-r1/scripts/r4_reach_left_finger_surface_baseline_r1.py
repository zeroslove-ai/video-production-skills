"""Bounded actual evaluated finger-surface QA; no solver/correction/asset save."""
import bpy,json,sys,hashlib,itertools
from pathlib import Path
import numpy as np
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_reach_left_finger_adapter_r1 import ReachFingerLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-reach-left-finger-surface-baseline-r1';O.mkdir(exist_ok=False);d=json.loads((B/'alpha-reach-left-finger-candidate-r1/REACH_LEFT_FINGER_CANDIDATE_PRIVATE_R1.json').read_bytes());P=Path(d['candidate']);assert hashlib.sha256(P.read_bytes()).hexdigest()==d['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);body=bpy.data.objects['Meshy_Body_NeutralCovered'];digits=['index','middle','ring','pinky','thumb'];lookup={body.vertex_groups[n+str(j)+'.L'].index:n for n in digits for j in [1,2,3]};cohorts={n:set() for n in digits}
for v in body.data.vertices:
 scores={n:0 for n in digits}
 for g in v.groups:
  if g.group in lookup:scores[lookup[g.group]]+=g.weight
 n=max(scores,key=scores.get)
 if scores[n]>=.5:cohorts[n].add(v.index)
hand_idx=body.vertex_groups['hand.L'].index;excluded={v.index for v in body.data.vertices if any((g.group in lookup or g.group==hand_idx) and g.weight>.01 for g in v.groups)}
lane=ReachFingerLane();lane.on(include_fingers=False);rows=[];prev=None;maximum_vertex_step=0;baseline=None;outside_step=0
for f in range(1,62):
 bpy.context.scene.frame_set(f);bpy.context.view_layer.update();e=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();m.calc_loop_triangles();xyz=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',xyz);xyz=xyz.reshape(-1,3);assert np.isfinite(xyz).all();tri=[tuple(t.vertices) for t in m.loop_triangles];trees={};coverage={}
 for n in digits:
  faces=[t for t in tri if all(v in cohorts[n] for v in t)];coverage[n]={'vertices':len(cohorts[n]),'triangles':len(faces)};trees[n]=BVHTree.FromPolygons(xyz.tolist(),faces,all_triangles=True,epsilon=0)
 other_faces=[t for t in tri if all(v not in excluded for v in t)];other=BVHTree.FromPolygons(xyz.tolist(),other_faces,all_triangles=True,epsilon=0)
 overlaps={a+'__'+b:len(trees[a].overlap(trees[b])) for a,b in itertools.combinations(digits,2)};overlaps.update({n+'__body_other':len(trees[n].overlap(other)) for n in digits})
 if baseline is None:baseline=xyz.copy()
 if prev is not None:maximum_vertex_step=max(maximum_vertex_step,float(np.linalg.norm(xyz-prev,axis=1).max())*body.matrix_world.to_scale().x)
 prev=xyz.copy();rows.append({'frame':f,'inter_digit_surface_triangle_overlaps':overlaps});e.to_mesh_clear()
lane.off();report={'candidate_SHA':d['candidate_SHA'],'frames_sampled':61,'dominant_existing_weight_threshold':.5,'evaluated_topology_cohort':coverage,'maximum_evaluated_mesh_vertex_frame_step_world_m':maximum_vertex_step,'max_overlap_counts':{n:max(x['inter_digit_surface_triangle_overlaps'][n] for x in rows) for n in rows[0]['inter_digit_surface_triangle_overlaps']},'baseline_overlap_counts':rows[0]['inter_digit_surface_triangle_overlaps'],'endpoint_overlap_counts':rows[-1]['inter_digit_surface_triangle_overlaps'],'frames_private':rows,'scope':'Actual evaluated native mesh, disjoint dominant-weight digit triangle cohorts, epsilon0 BVH intersections at all61 frames. Also checks digit triangles against body triangles outside left-hand/finger weight>1percent; weak-weight palm/webbing and same-digit folds excluded; this bounded measurement is not full mesh collision certification. Visual full playback required. No prop/contact/grasp/Unity/MUG certification.','no_asset_source_edit':True};(O/'C1_FINGER_OFF_SURFACE_QA_PRIVATE_R1.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('FINGER_SURFACE_QA_DONE',report['max_overlap_counts'],maximum_vertex_step,flush=True)

