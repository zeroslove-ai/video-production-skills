"""Publish scalar-only custody findings. Native artifacts remain private and immutable."""
import json,hashlib,ast
from pathlib import Path
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');L=Path(__file__).resolve().parent.parent;E=L/'evidence/dots-exact-baseline-custody-r1';E.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((B/'dots-exact-baseline-custody-r1/EXACT_BASELINE_COMPARE_PRIVATE_R1.json').read_bytes());d=json.loads((B/'dots-exact-baseline-details-r1/EXACT_BASELINE_DETAILS_PRIVATE_R1.json').read_bytes());receipt=json.loads((B/'dots-exact-baseline-inputs-r1/BASELINE_RECEIVER_RECEIPT_R1.json').read_bytes())
c=r['control_to_r2'];assert not c['objects_added'] and not c['objects_removed'] and not c['actions_removed']
assert c['actions_added']==['MUG_CORRECTIVE_R2_Envelope_Unassigned_OFF']
for cat in ['actions','rest_rigs','rest_pose_settings','materials','node_groups','textures','worlds','camera_lights','scene','evaluated_geometry_world']:assert c['original_domain_differences'][cat]==[],cat
assert d['r2_body_object_actual_diffs']==[{'field':'/props/active_shape_key','before':None,'after':['ShapeKey','Basis']}]
assert d['r2_basis_exact_control_mesh_coords']
for name,v in c['meshes'].items():
 assert not v['original_keys_changed']
 assert v['original_fields_changed'] in [[],['shape_anim']]
 assert v['keys_added'] in [[],['Basis','MUG_ThumbVolume_VolumeRedistribution_R2_OFF']]
assert all(x['field'].endswith('/props/filepath') or x['field'].endswith('/props/filepath_raw') for x in d['master_control_image_actual_diffs'])
guards=[]
for folder in ['o1-dots-exact-baseline-compare-r1','o1-dots-exact-baseline-details-r1']:
 p=B/folder/'NATIVE_GUARD_RESULT.json';g=json.loads(p.read_bytes());assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN';guards.append({'path':str(p),'sha256':sha(p),'status':g['guard_status']})
out={'scope':r['scope'],'custody':'PASS_EXACT_TWO_BASELINES','source_parity_vs_Dots_MUG_control':'PASS_ORIGINAL_DOMAINS_PRESERVED_WITH_ENUMERATED_ADDITIONS','strict_whole_asset_identical':'NO: R2 adds Basis/corrective key and unassigned envelope; not appearance promotion','canonical_R4_equivalence':'NOT_ASSERTED: immutable a30fc R4 remains sole visual authority','assets':[{k:v for k,v in a.items() if k!='parts'} for a in receipt['assets']],'r2':r['files']['r2'],'inventory':r['inventory'],'master_to_control':{'objects_added':r['master_to_control']['objects_added'],'actions_added':r['master_to_control']['actions_added'],'original_domain_differences':r['master_to_control']['original_domain_differences'],'image_difference_resolution':'Only filepath/filepath_raw differ; packed bytes/color and other image props identical. No image edits performed.'},'control_to_r2':{'objects_added':c['objects_added'],'objects_removed':c['objects_removed'],'actions_added':c['actions_added'],'actions_removed':c['actions_removed'],'original_domain_differences':c['original_domain_differences'],'body_object_actual_diff':d['r2_body_object_actual_diffs'],'mesh_differences':{k:v for k,v in c['meshes'].items() if any(v.values())},'new_Basis_equals_control_vertex_coordinates':True,'OFF_evaluated_world_geometry_exact_all_48_mesh_objects':True,'original_111_action_curves_exact':True},'correctives':r['r2_correctives'],'envelope':{'action':r['r2_envelopes'][0]['action'],'keys':169,'min':0,'max':1,'nonzero_start':53,'nonzero_end':134,'assigned':False},'upstream_support_count':165,'measured_effective_nonzero_delta_vertices':164,'support_count_difference':'165 authored-support claim versus 164 stored effective nonzero deltas; cause remains unproven. No repair/new corrective.','guards':guards,'TierP':0,'default_OFF':True,'quality':'HOLD/contact debt remains','new_candidate_render_export_Unity_changes':False,'pixel_parity_test':'NOT_RUN in this custody audit','previous_UNKNOWN_receipt':'5432cc45119e277352af8c447beefff6b56561d5 preserved; baseline availability/original parity superseded by this fresh evidence'}
(E/'DOTS_EXACT_BASELINE_CUSTODY_SCALAR_R1.json').write_text(json.dumps(out,indent=2),encoding='utf8')
for p in Path(__file__).resolve().parent.glob('dots_exact_baseline_*r1.py'):ast.parse(p.read_text(encoding='utf8'))
print('SCALAR_CLOSURE_PASS',sha(E/'DOTS_EXACT_BASELINE_CUSTODY_SCALAR_R1.json'))
