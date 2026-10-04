"""Fresh source + three Actions, BOTH actual arm/digit surface cohorts all169 frames."""
import bpy,sys,json,hashlib
from pathlib import Path
import numpy as np
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_native_grasp_adapter_r1 import NativeGraspLane
from r4_c1_contact_surface_oracle_r3 import SurfaceOracle as Left
from r4_native_talk_right_surface_oracle_r1 import SurfaceOracle as Right
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-native-grasp-library-contact-qa-r1';O.mkdir(exist_ok=False);d=json.loads((B/'alpha-native-grasp-candidate-r1b/NATIVE_GRASP_CANDIDATE_PRIVATE_R1B.json').read_bytes());lib=json.loads((B/'alpha-native-grasp-preview-r1/ACTION_ONLY_CUSTODY_R1.json').read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(d['source'])==d['source_SHA'] and sha(lib['file'])==lib['SHA'];bpy.ops.wm.open_mainfile(filepath=d['source'],use_scripts=False);s=bpy.context.scene;names=list(bpy.data.actions.keys());before=snapshot(names);oracles={'L':Left(),'R':Right()};source={n:oracles['L'].geometry(bpy.data.objects[n])[0] for n in ['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4']};baseline={n:o.capture() for n,o in oracles.items()}
with bpy.data.libraries.load(lib['file'],link=False) as (src,dst):assert len(src.actions)==3 and not src.objects and not src.meshes and not src.armatures;dst.actions=list(src.actions)
for a in dst.actions:a.use_fake_user=True
assert snapshot(names)==before;lane=NativeGraspLane();lane.on();rows=[];endpoints={};maxima={n:{k:0 for k in p} for n,p in baseline.items()};added={n:{k:0 for k in p} for n,p in baseline.items()};root=np.array(bpy.data.objects['Assembly_Root'].matrix_world)
for f in range(1,170):
 s.frame_set(f);bpy.context.view_layer.update();assert np.array_equal(root,np.array(bpy.data.objects['Assembly_Root'].matrix_world));row={'frame':f,'sides':{}}
 for side,o in oracles.items():
  p=o.capture();counts={k:len(v) for k,v in p.items()};new={k:len(v-baseline[side][k]) for k,v in p.items()};row['sides'][side]={'actual_triangle_pair_counts':counts,'new_vs_source_neutral_triangle_pair_counts':new}
  for k in p:maxima[side][k]=max(maxima[side][k],counts[k]);added[side][k]=max(added[side][k],new[k])
 if f in [1,169]:endpoints[str(f)]={n:float(np.max(np.abs(oracles['L'].geometry(bpy.data.objects[n])[0]-v))) for n,v in source.items()}
 rows.append(row)
 if f%24==1:print('GRASP_ACTUAL_BOTH_HAND_CONTACT_FRAME',f,sum(sum(v['actual_triangle_pair_counts'].values()) for v in row['sides'].values()),flush=True)
lane.off();assert snapshot(names)==before;assert sha(d['source'])==d['source_SHA'];result={'task':'ROOT_PM_INDEPENDENT_STAGE_AB_GRASP_SOURCE_R1','source_SHA':d['source_SHA'],'candidate_SHA':d['candidate_SHA'],'library_SHA':lib['SHA'],'fresh_source_plus_ONLY3Actions_and_fixed_adapter':True,'new_objects_meshes_rigs':0,'original78Actions_source_OFF_snapshot_exact':True,'root_same_all169':True,'endpoint_source_geometry_component_error_m':endpoints,'source_neutral_pair_counts':{n:{k:len(v) for k,v in p.items()} for n,p in baseline.items()},'maximum_actual_surface_pairs_by_side':maxima,'maximum_added_vs_original_neutral_pairs_by_side':added,'frames_private':rows,'bounded_contact_subset':'PASS' if not any(v for x in maxima.values() for v in x.values()) else 'FAIL_HOLD','scope':'Existing dominant >=.5 original-weight L/R arm/hand/digit triangle cohorts, actual dynamic evaluated triangulation, preserved original polygons/vertex counts, epsilon0; weak webbing/adjacency/full-character/depth/physical contact not certified','TierP':0};(O/'NATIVE_GRASP_BOTH_ARM_SURFACE_PRIVATE_R1.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print('GRASP_FRESH_LIBRARY_CONTACT_RESULT',result['bounded_contact_subset'],endpoints,flush=True)
