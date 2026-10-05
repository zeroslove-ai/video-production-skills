"""Readonly residual first failure surface ownership + untouched wrist472 witness."""
import bpy,sys,json,gzip,hashlib,ast,collections
from pathlib import Path
import numpy as np
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
from r4_native_tour_adapter_r1 import ACTIONS
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-tour302-residual-localize-c2';O.mkdir(exist_ok=False);m=json.loads((B/'alpha-tour302-softcap-c2/TOUR302_SOFTCAP_C2_PRIVATE.json').read_bytes());old=json.loads((B/'alpha-native-tour-recovery-r2/NATIVE_TOUR_RECOVERY_PRIVATE_R2.json').read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(m['candidate'])==m['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=m['candidate'],use_scripts=False)
s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered'];names=list(m['preserved81_signature_private']['actions']);before=snapshot(names);assert before==m['preserved81_signature_private'];gn={g.index:g.name for g in body.vertex_groups};ledger=json.loads(gzip.open(B/'alpha-tour302-softcap-c2/LOCAL_SURFACE_IDENTITIES_PRIVATE_C2.json.gz','rt',encoding='utf8').read());pair=next(x for x in ledger if x['frame']==303)['new_pair_identities']['Meshy_Body_NeutralCovered__self_nonadjacent'][0];ids=sorted({v for tri in pair for v in tri});weights=[]
for tri in pair:
 c=collections.Counter();per=[]
 for idx in tri:
  ww={gn[g.group]:g.weight for g in body.data.vertices[idx].groups if gn[g.group] in r.pose.bones};c.update(ww);per.append({'vertex':idx,'original_bone_weights':ww})
 weights.append({'triangle_private':tri,'dominant_original_bones':c.most_common(6),'per_vertex_private':per})
tree=ast.parse((H/'r4_existing_reach_contact_closure_r1.py').read_text(encoding='utf8'));ns={'bpy':bpy,'np':np,'fixed':{}};exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='geom'],type_ignores=[]),'<same_geom>','exec'),ns);geom=ns['geom'];mesh_names=['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4'];actual={}
for mode,an in [('ORIGINAL',ACTIONS[r.name]),('CORRECTED',m['corrective_action'])]:
 lanes=[]
 for ob,aa in ACTIONS.items():
  ln=ReactionLane(ob);ln.on(an if ob==r.name else aa);lanes.append(ln)
 actual[mode]={}
 for f in [303,337,472]:
  s.frame_set(f);bpy.context.view_layer.update();data={n:geom(bpy.data.objects[n]) for n in mesh_names};hh={n:hashlib.sha256(z[0].tobytes()).hexdigest() for n,z in data.items()};expected=old['all_rows_private'][f-1]['actual_mesh_hash_private'] if mode=='ORIGINAL' or f==472 else m['local_rows_private'][f-288]['actual_mesh_hash_private'];assert hh==expected;actual[mode][f]={'pair_vertices_private':data[mesh_names[0]][0][ids].tolist(),'mesh_SHA_private':hh}
 for ln in reversed(lanes):ln.off()
assert snapshot(names)==before and sha(m['candidate'])==m['candidate_SHA'];errs={str(f):float(np.abs(np.array(actual['ORIGINAL'][f]['pair_vertices_private'])-np.array(actual['CORRECTED'][f]['pair_vertices_private'])).max()) for f in [303,337]}
(O/'RESIDUAL_SURFACE_OWNERSHIP_PRIVATE_C2.json').write_text(json.dumps({'candidate_SHA':m['candidate_SHA'],'first_residual_frame':303,'residual_original_weights_private':weights,'source_to_corrected_pair_vertex_component_error_m':errs,'actual_witness_private':actual,'wrist472_actual_all_three_mesh_SHA_same_original':True,'source81_OFF_restored':True},indent=2),encoding='utf8');print('TOUR302_RESIDUAL_LOCALIZED',[(x['dominant_original_bones']) for x in weights],errs,'WRIST472_UNTOUCHED',flush=True)

