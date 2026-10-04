"""Exact native BVH over all769 saved evaluated mesh vertices AND dynamic triangles."""
import bpy,sys,json,hashlib,ast,gzip,collections,time
from pathlib import Path
import numpy as np
from mathutils.bvhtree import BVHTree
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');P=B/'alpha-native-tour-source-r3';O=B/'alpha-native-tour-contact-r1';O.mkdir(exist_ok=False);m=json.loads((P/'NATIVE_TOUR_SOURCE_PRIVATE_R1.json').read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(m['candidate'])==m['candidate_SHA'] and sha(m['actual_geometry_cache']['file'])==m['actual_geometry_cache']['SHA'];bpy.ops.wm.open_mainfile(filepath=m['candidate'],use_scripts=False);names=list(m['original78_signature_private']['actions']);before=snapshot(names);assert before==m['original78_signature_private'];mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4'];tree=ast.parse((H/'r4_native_walk_source_supply_r1.py').read_text(encoding='utf8'));exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='contact'],type_ignores=[]),'<same_actual_BVH>','exec'));cache=np.load(m['actual_geometry_cache']['file']);body=bpy.data.objects[mesh_names[0]];gn={g.index:g.name for g in body.vertex_groups};start=time.perf_counter()
def data(prefix):return {n:(cache[prefix+n+'_v'],[tuple(z) for z in cache[prefix+n+'_t'].tolist()],None) for n in mesh_names}
base,raw=contact(data('OFF_'));ledger={'baseline':{k:sorted(v) for k,v in base.items()},'frames':[]};rows=[];first={};worst={};rank={}
for ix,f in enumerate(range(m['frames'][0],m['frames'][1]+1)):
 actual=data('f'+str(f)+'_');assert all(hashlib.sha256(z[0].tobytes()).hexdigest()==m['all_rows_private'][ix]['actual_mesh_hash_private'][n] for n,z in actual.items());ps,_=contact(actual);new={k:v-base[k] for k,v in ps.items()};counts={k:len(v) for k,v in new.items()};rows.append({'frame':f,'new_pairs':counts,'absolute_pairs':{k:len(v) for k,v in ps.items()},'exact_all_actual_mesh_cache_SHA':True});ledger['frames'].append({'frame':f,'new_pairs':{k:sorted(v) for k,v in new.items()}})
 for k,v in new.items():
  if v and k not in first:first[k]={'frame':f,'count':len(v),'identities':sorted(v)}
  if k not in worst or len(v)>worst[k]['count']:worst[k]={'frame':f,'count':len(v),'identities':sorted(v)}
 if f%96==1:print('TOUR_EXACT_NATIVE_CACHE_SURFACE',f,counts,flush=True)
for label,samples in [('first',first),('worst',worst)]:
 k=mesh_names[0]+'__self_nonadjacent'
 if k not in samples:continue
 c=collections.Counter()
 for pair in samples[k]['identities']:
  labels=[]
  for tri in pair:
   w=collections.Counter()
   for idx in tri:
    for gg in body.data.vertices[idx].groups:w[gn[gg.group]]+=gg.weight
   labels.append(w.most_common(1)[0][0] if w else 'unweighted')
  c[' / '.join(sorted(labels))]+=1
 rank[label]={'frame':samples[k]['frame'],'new_BODY_pairs':samples[k]['count'],'original_weight_region_pair_distribution':c.most_common(20),'not_weights_only_causality':True}
peaks={k:max(x['new_pairs'][k] for x in rows) for k in base};passed=not any(peaks.values()) and m['head_hair_attachment_matrix_gate_pass'];result={'same_candidate_SHA':m['candidate_SHA'],'actual_geometry_cache_SHA':m['actual_geometry_cache']['SHA'],'all_frames':m['frames'],'all769_actual_mesh_vertex_and_dynamic_triangle_cache_SHA_valid':True,'all_original78_OFF_equal':True,'all_surface_peak_new':peaks,'first_new_frame_by_pair_kind':{k:{'frame':v['frame'],'count':v['count']} for k,v in first.items()},'worst_frame_by_pair_kind':{k:{'frame':v['frame'],'count':v['count']} for k,v in worst.items()},'first_worst_BODY_localization':rank,'original_OFF_absolute_pairs':{k:len(v) for k,v in base.items()},'head_hair_attachment_matrix_gate_pass':m['head_hair_attachment_matrix_gate_pass'],'scoped_gate_pass':passed,'verdict':'PASS_SOURCE_CONTACT_SCOPE_PENDING_VISUAL_OFF' if passed else 'FAIL_HOLD_SOURCE_SURFACE_OR_ATTACHMENT','rows_private':rows,'first_private':first,'worst_private':worst,'scope':'Exact same all native actual world vertices and dynamic triangles; ALL weak/unweighted meshes/selfnonadjacent/cross. No new pose/authoring or body/face/skin change; no depth/volume/force inference.','seconds':time.perf_counter()-start};(O/'NATIVE_TOUR_CONTACT_PRIVATE_R1.json').write_text(json.dumps(result,indent=2),encoding='utf8')
with gzip.open(O/'NATIVE_TOUR_ALL769_IDENTITIES_PRIVATE_R1.json.gz','wt',encoding='utf8') as f:json.dump(ledger,f)
assert snapshot(names)==before and sha(m['candidate'])==m['candidate_SHA'];print('TOUR_ALL769_CONTACT_COMPLETE',peaks,rank,flush=True)
