"""One CPU source-data job; exact existing direct-morph flow, no video/export.
Evaluate all original vertices including loose indices. Immutable source only.
"""
import bpy,sys,json,hashlib,ast
import numpy as np
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference,props,val
ROOT=HERE.parent;E=ROOT/'evidence/o1-dense-half-expression-r1';E.mkdir(parents=True,exist_ok=True)
OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/o1-dense-half-expression-r1');OUT.mkdir(parents=True,exist_ok=True)
PRIOR=OUT.parent/'o1-source-fidelity-recovery-r1';SOURCE=ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ah(a):return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
def write(n,v):
    for p in (E/n,OUT/n):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
assert sha(SOURCE)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False);s=bpy.context.scene;actions=[a.name for a in bpy.data.actions];before=snapshot(actions)
head=bpy.data.objects['Character_Body_Head'];keys=head.data.shape_keys;groups={'blink':['Blink.L','Blink.R'],'smile':['Smile.L','Smile.R'],'jaw':['JawOpen'],'brow':['BrowRaise.L','BrowRaise.R']};saved={k:keys.key_blocks[k].value for g in groups.values() for k in g}
meta=json.loads((PRIOR/'metadata/mesh_slot_UV_attributes_shape_deltas.json').read_text(encoding='utf8'));meshes=[bpy.data.objects[r['renderer']] for r in meta];assert len(meshes)==21
flow=HERE/'r4_recovery_manual_morph.py';module=ast.parse(flow.read_text(encoding='utf8'));functions=[n for n in module.body if isinstance(n,ast.FunctionDef) and n.name in ('setinput','evaluate')];assert len(functions)==2
exec(compile(ast.Module(body=functions,type_ignores=[]),str(flow),'exec'),globals())
neutral=evaluate();arrays={};index_receipts=[]
for row,o in zip(meta,meshes):
    m=o.data;mask=np.zeros(len(m.vertices),np.uint8);loops=np.empty(len(m.loops),np.int32);m.loops.foreach_get('vertex_index',loops);mask[loops]=1
    # Original mesh loops all belong to source polygons. Count source corners,
    # stable vertex indices and loose vertices, never prune a vertex.
    corners=np.empty(len(m.polygons),np.int32);m.polygons.foreach_get('loop_total',corners);assert int(corners.sum())==len(loops)
    arrays[o.name+'_polygon_used_mask']=mask
    originalnpz=np.load(PRIOR/row['file']['path']);position=np.empty((len(m.vertices),3),np.float32);m.vertices.foreach_get('co',position.reshape(-1));assert np.array_equal(position,originalnpz['positions'])
    index_receipts.append({'renderer':o.name,'vertices':len(m.vertices),'polygons':len(m.polygons),'source_corners':len(m.loops),'polygon_used_vertices':int(mask.sum()),'loose_vertices':int(len(mask)-mask.sum()),'mask_array':o.name+'_polygon_used_mask','mask_sha256_uint8_bytes':ah(mask),'source_index_policy':'All evaluated vertices retain source original index; no split/prune/normalization','basis_positions_sha256_float32_bytes':ah(position),'original_mesh_data_pointer':{'frozen_recovery_ZIP_sha256':'080352e24adb9db33e76e92d8aca9836aeaf444ed75818c29e2970a32dae47df','path':row['file']['path'],'bytes':row['file']['bytes'],'sha256':row['file']['sha256'],'basis_array':'positions','corner_array':'loop_vertex_indices','polygon_arrays':['polygon_loop_start','polygon_loop_total']}})
head_indices=next(r for r in index_receipts if r['renderer']==head.name);assert (head_indices['vertices'],head_indices['polygon_used_vertices'],head_indices['loose_vertices'])==(12928,12093,835)
def output():
    deps=bpy.context.evaluated_depsgraph_get();geometrykeys=[]
    for o in meshes:
        if o.data.shape_keys:
            ev=o.evaluated_get(deps);ek=ev.data.shape_keys
            geometrykeys.append({'renderer':o.name,'key_owner':o.data.shape_keys.name,'original_key_values':{k.name:k.value for k in o.data.shape_keys.key_blocks},'evaluated_key_values':{k.name:k.value for k in ek.key_blocks} if ek else None})
    shader=[];gn=[]
    for mat in bpy.data.materials:
        t=mat.node_tree
        if not t or not t.animation_data:continue
        for f in t.animation_data.drivers:
            v=t.path_resolve(f.data_path);v=v[f.array_index] if hasattr(v,'__len__') and not isinstance(v,str) else v
            shader.append({'owner':'Material/'+mat.name+'/node_tree','path':f.data_path,'index':f.array_index,'value':val(v),'mute':f.mute,'valid':f.driver.is_valid})
    for t in bpy.data.node_groups:
        if not t.animation_data:continue
        for f in t.animation_data.drivers:
            v=t.path_resolve(f.data_path);v=v[f.array_index] if hasattr(v,'__len__') and not isinstance(v,str) else v
            gn.append({'group':t.name,'path':f.data_path,'index':f.array_index,'value':val(v),'mute':f.mute,'valid':f.driver.is_valid})
    return {'head_lash_and_other_key_values':geometrykeys,'material_driver_socket_outputs':shader,'GN_control_driver_outputs':gn,'head_custom_properties':{k:val(head[k]) for k in head.keys()},'head_bridge13': [{'path':f.data_path,'mute':f.mute,'valid':f.driver.is_valid} for f in keys.animation_data.drivers if 'slide / 0.055' in f.driver.expression]}
def stats(p,q,mask=None):
    d=np.linalg.norm(p-q,axis=1)
    if mask is not None:d=d[mask]
    return {'max_world_vertex_delta_m':float(d.max()) if len(d) else 0,'RMS_m':float(np.sqrt(np.mean(d*d))) if len(d) else 0,'changed_vertex_count':int(np.count_nonzero(d>1e-8)),'vertices_counted':len(d)}
priorreceipt=json.loads((PRIOR/'metadata/MANUAL_MORPH_RECEIPT.json').read_text(encoding='utf8'));cases=[];restores=[]
for group in groups:
    setinput(group,.5);evaluated=evaluate();metrics=[]
    for name,p in evaluated.items():
        assert p.shape==neutral[name].shape and len(p)==next(r['vertices'] for r in index_receipts if r['renderer']==name)
        arrayname=group+'_'+name;arrays[arrayname]=p;mask=arrays[name+'_polygon_used_mask'].astype(bool)
        metrics.append({'mesh':name,'dense_array':arrayname,'dtype':'float32 little-endian','shape':list(p.shape),'array_sha256':ah(p),'all_original_vertices':stats(p,neutral[name]),'polygon_used_only':stats(p,neutral[name],mask),'loose_only':stats(p,neutral[name],~mask)})
    old=next(c for c in priorreceipt['cases'] if c['group']==group and c['input_value']==.5);oldbyname={r['mesh']:r for r in old['geometry']};comparison=[]
    for r in metrics:
        oldstats=oldbyname[r['mesh']];new=r['all_original_vertices'];comparison.append({'mesh':r['mesh'],'max_metric_difference_m':new['max_world_vertex_delta_m']-oldstats['max_world_vertex_delta_m'],'RMS_metric_difference_m':new['RMS_m']-oldstats['RMS_m'],'changed_vertex_count_difference':new['changed_vertex_count']-oldstats['changed_vertex_count'],'exact_previous_summary_match':all(new[k]==oldstats[k] for k in ('max_world_vertex_delta_m','RMS_m','changed_vertex_count'))})
    cases.append({'group':group,'input_value':.5,'input_paths':['Character_Body_Head.data.shape_keys.key_blocks['+repr(k)+'].value' for k in groups[group]],'input_default_values':{k:saved[k] for k in groups[group]},'metrics':metrics,'downstream_outputs':output(),'prior_half_summary_comparison':comparison})
    for k,v in saved.items():keys.key_blocks[k].value=v
    keys.update_tag();head.update_tag();s.frame_set(1);bpy.context.view_layer.update();off=evaluate();restores.append({'group':group,'OFF_return_max_world_vertex_delta_m':max(stats(p,neutral[n])['max_world_vertex_delta_m'] for n,p in off.items()),'downstream_outputs':output()})
path=OUT/'R4_Existing_DirectMorph_Half_Dense_20261003_R1.npz';np.savez_compressed(path,**arrays)
oldneutral=np.load(PRIOR/'data/neutral.npz');neutral_match=[{'renderer':n,'reused_zero_reference_equal_exact':np.array_equal(p,oldneutral[n+'_world_position']),'max_zero_reference_delta_m':stats(p,oldneutral[n+'_world_position'])['max_world_vertex_delta_m']} for n,p in neutral.items()]
# Prior SOURCE_DATA zero uses explicit float64 matrix multiplication, whereas
# the reused manual-morph function takes np.array(mathutils.Matrix) dtype.
# Record exact observed residual; do not assert byte equality or change source.
assert all(r['OFF_return_max_world_vertex_delta_m']==0 for r in restores)
assert all(r['exact_previous_summary_match'] for c in cases for r in c['prior_half_summary_comparison'])
assert len(cases[0]['downstream_outputs']['head_bridge13'])==13 and all(r['mute'] for r in cases[0]['downstream_outputs']['head_bridge13'])
delta=difference(before,snapshot(actions));assert not delta,delta;assert sha(SOURCE)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
write('DENSE_HALF_SOURCE_RECEIPT.json',{'source_SHA256':sha(SOURCE),'source_component_diff':delta,'source_saved':False,'source_actions_preserved':len(actions),'flow_script':{'path':flow.name,'sha256':sha(flow),'reuse':'AST extract exact setinput/evaluate functions only; no top-level load/render/bake/export executed'},'completed_data_job_count':1,'data_job_attempts':2,'retry_reason':'Initial overstrict reused-zero byte equality guard; zero extraction used explicit float64 matrix, manual flow uses matrix buffer dtype; receipt now records residual without altering inputs. No other task/export trial.','Blender':bpy.app.version_string,'factory_CPU_only':True,'no_GUI_video_bake_export':True,'coordinate_policy':'Original evaluated world meters; exact frozen manual-morph evaluate flow and final float32 output; original .535 exactly once. Matrix dtype audited below, not assumed float64.','matrix_array_dtypes':{o.name:str(np.array(o.matrix_world).dtype) for o in meshes},'prior_source_data_zero_matrix_dtype':'explicit float64','index_receipts':index_receipts,'half_cases':cases,'restored_OFF':restores,'reused_zero_reference_comparison':neutral_match,'dense_file':{'path':path.name,'bytes':path.stat().st_size,'sha256':sha(path),'arrays':len(arrays)},'quality':'Reference data only; no F2/F3/appearance/Player/Unity PASS','parent_checkpoint':'5137bcd9d8fd015f60792f6919635b9e67027100'})
reuse=[]
for rel in ('data/neutral.npz','data/manual_morph_peak_geometry.npz','metadata/MANUAL_MORPH_RECEIPT.json','metadata/mesh_slot_UV_attributes_shape_deltas.json','metadata/executable_geometry_node_graphs.json','metadata/MATERIAL_SHADER_DRIVER_RECEIPT.json'):
    p=PRIOR/rel;reuse.append({'frozen_ZIP_sha256':'080352e24adb9db33e76e92d8aca9836aeaf444ed75818c29e2970a32dae47df','path':rel,'bytes':p.stat().st_size,'sha256':sha(p),'zero_array':'<renderer>_world_position' if 'neutral.npz' in rel else None,'peak_array':'<group>_<renderer>' if 'peak_geometry.npz' in rel else None})
write('REUSED_ZERO_PEAK_BASIS_POINTERS.json',reuse)
print('DENSE_HALF_COMPLETE',path.stat().st_size,head_indices['vertices'],head_indices['polygon_used_vertices'],head_indices['loose_vertices'])
