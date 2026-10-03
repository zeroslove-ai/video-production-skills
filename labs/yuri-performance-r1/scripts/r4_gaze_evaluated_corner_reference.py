"""Sequential small CPU phase: actual evaluated gaze split normals/tangents.
No render/bake/export/source save. Run after body reference job completes.
"""
import bpy,sys,json,hashlib,time
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference
LAB=HERE.parent;BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
REC=BASE/'o1-source-fidelity-recovery-r1';OUT=BASE/'o1-gaze-evaluated-corner-reference-r1'
E=LAB/'evidence/o1-gaze-evaluated-corner-reference-r1';OUT.mkdir(parents=True,exist_ok=True);E.mkdir(parents=True,exist_ok=True)
SOURCE=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
def write(n,v):
    for p in (E/n,OUT/n):p.write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf8')
def arr(c,f,w=3,dtype=np.float32):
    a=np.empty(len(c)*w,dtype=dtype);c.foreach_get(f,a);return a.reshape(-1,w) if w>1 else a
cases=[('neutral',0,0),('gaze_-1_0',-1,0),('gaze_1_0',1,0),('gaze_0_-1',0,-1),('gaze_0_1',0,1)]
names=['Character_Body_Head','Globe.L','Globe.R']
inputs=[SOURCE,REC/'metadata/executable_geometry_node_graphs.json',REC/'metadata/evaluated_driver_geometry_references.json',
    REC/'metadata/mesh_slot_UV_attributes_shape_deltas.json',REC/'metadata/CORNER_BASIS_RECEIPT.json',
    HERE/'r4_recovery_source_data.py']+[REC/'data'/f'{n}_original_mesh.npz' for n in names]+[REC/'data'/f'{n}_corner_basis.npz' for n in names]+[REC/'data'/f'{tag}.npz' for tag,_,_ in cases]
hashes={str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in inputs}
assert hashes[str(SOURCE)]['sha256']=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
start=time.monotonic();bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False)
s=bpy.context.scene;actions=[a.name for a in bpy.data.actions];before=snapshot(actions)
assert s.frame_current==1;head=bpy.data.objects[names[0]]
saved={k:head[k] for k in ('Face_GazeYaw','Face_GazePitch')};assert saved=={'Face_GazeYaw':0.,'Face_GazePitch':0.}
topology={n:np.load(REC/'data'/f'{n}_original_mesh.npz',allow_pickle=False) for n in names}
bridge=head.data.shape_keys.animation_data.drivers
muted=[{'path':f.data_path,'mute':f.mute,'valid':f.driver.is_valid} for f in bridge if 'slide / 0.055' in f.driver.expression]
assert len(muted)==13 and all(f['mute'] for f in muted)
results=[];filemeta=[];baseline={}
for tag,yaw,pitch in cases:
    head['Face_GazeYaw']=yaw;head['Face_GazePitch']=pitch;head.update_tag();s.frame_set(1);bpy.context.view_layer.update()
    deps=bpy.context.evaluated_depsgraph_get();arrays={};meshes=[]
    frozen=np.load(REC/'data'/f'{tag}.npz',allow_pickle=False)
    for name in names:
        original=bpy.data.objects[name];o=original.evaluated_get(deps);m=o.to_mesh(preserve_all_data_layers=True,depsgraph=deps)
        try:
            topo=topology[name]
            assert len(m.vertices)==len(original.data.vertices) and len(m.loops)==len(original.data.loops)
            for key,col,field in [('loop_vertex_indices',m.loops,'vertex_index'),('polygon_loop_start',m.polygons,'loop_start'),('polygon_loop_total',m.polygons,'loop_total'),('polygon_material_slot',m.polygons,'material_index')]:assert np.array_equal(arr(col,field,1,np.int32),topo[key]),(tag,name,key)
            for i,uv in enumerate(m.uv_layers):assert np.array_equal(arr(uv.data,'uv',2),topo['uv_'+str(i)]),(tag,name,'UV',i)
            local=arr(m.vertices,'co');mw=np.array(o.matrix_world,dtype=np.float64);linear=mw[:3,:3];inverse=np.linalg.inv(linear)
            world=(local.astype(np.float64)@linear.T+mw[:3,3]).astype(np.float32)
            dl=float(np.max(np.abs(local-frozen[name+'_local_position'])));dw=float(np.max(np.abs(world-frozen[name+'_world_position'])))
            assert dl==dw==0,(tag,name,'frozen position mismatch',dl,dw)
            cn=arr(m.corner_normals,'vector');assert len(cn)==len(m.loops)
            def norm(a):
                length=np.linalg.norm(a,axis=1);assert np.all(length>1e-12)
                return (a/length[:,None]).astype(np.float32)
            wn=norm(cn.astype(np.float64)@inverse)
            arrays[name+'_local_corner_normal']=cn;arrays[name+'_world_corner_normal']=wn
            tangents=[]
            for i,uv in enumerate(m.uv_layers):
                m.calc_tangents(uvmap=uv.name);tl=arr(m.loops,'tangent');sign=arr(m.loops,'bitangent_sign',1)
                tw=tl.astype(np.float64)@linear.T;tw-=np.sum(tw*wn,axis=1)[:,None]*wn
                tw=norm(tw);sw=sign*np.sign(np.linalg.det(linear))
                bl=sign[:,None]*np.cross(cn,tl);bw=sw[:,None]*np.cross(wn,tw)
                for key,value in [('local_tangent',tl),('world_tangent',tw),('local_bitangent',bl),('world_bitangent',bw),('local_bitangent_sign',sign),('world_bitangent_sign',sw.astype(np.float32))]:arrays[f'{name}_uv{i}_{key}']=value
                tangents.append({'UV':uv.name,'index':i,'corners':len(tl),'sign_values':sorted(set(sign.tolist()))})
            assert all(np.isfinite(v).all() for k,v in arrays.items() if k.startswith(name+'_'))
            dnormal=np.linalg.norm(cn-arr(m.vertices,'normal')[topo['loop_vertex_indices']],axis=1)
            if tag=='neutral':baseline[name]=wn.copy()
            row={'mesh':name,'vertices':len(local),'loops':len(m.loops),'polygons':len(m.polygons),
                'frozen_local_position_max_element_delta':dl,'frozen_world_position_max_element_delta':dw,
                'topology_indices_and_UV_identical':True,'evaluated_has_custom_normals':m.has_custom_normals,
                'original_has_custom_normals':original.data.has_custom_normals,
                'original_polygon_use_smooth_true_count':sum(p.use_smooth for p in original.data.polygons),
                'evaluated_polygon_use_smooth_true_count':sum(p.use_smooth for p in m.polygons),
                'split_corner_vs_vertex_normal_max_vector_delta':float(dnormal.max()),
                'split_corner_vs_vertex_normal_differing_count_over1e-6':int(np.count_nonzero(dnormal>1e-6)),
                'actual_world_corner_normal_motion_max_vector_delta_from_neutral':float(np.linalg.norm(wn-baseline[name],axis=1).max()),
                'object_world':mw.tolist(),'UV_tangents':tangents,'original_mesh_NPZ_pointer':str(REC/'data'/f'{name}_original_mesh.npz')}
            meshes.append(row)
        finally:o.to_mesh_clear()
    p=OUT/(tag+'_evaluated_corners.npz');assert not p.exists(),('do not overwrite frozen data',p)
    np.savez_compressed(p,**arrays);assert p.stat().st_size<100*1024**2
    with np.load(p,allow_pickle=False) as check:
        assert all(np.array_equal(check[k],v) for k,v in arrays.items())
    filemeta.append({'path':p.name,'sha256':sha(p),'bytes':p.stat().st_size,'arrays':{k:{'shape':list(v.shape),'dtype':str(v.dtype)} for k,v in arrays.items()}})
    results.append({'case':tag,'frame':1,'controls':{'Face_GazeYaw':yaw,'Face_GazePitch':pitch},'meshes':meshes})
    print('GAZE_CASE_FROZEN',tag,p.stat().st_size,flush=True)
for k,v in saved.items():head[k]=v
head.update_tag();s.frame_set(1);bpy.context.view_layer.update()
# Evaluate OFF corner return, not merely control values.
off=[];deps=bpy.context.evaluated_depsgraph_get()
for name in names:
    o=bpy.data.objects[name].evaluated_get(deps);m=o.to_mesh(preserve_all_data_layers=True,depsgraph=deps)
    try:
        n=arr(m.corner_normals,'vector').astype(np.float64)@np.linalg.inv(np.array(o.matrix_world,dtype=np.float64)[:3,:3]);n=(n/np.linalg.norm(n,axis=1)[:,None]).astype(np.float32)
        d=float(np.max(np.abs(n-baseline[name])));assert d==0;off.append({'mesh':name,'world_corner_normal_OFF_return_max_delta':d})
    finally:o.to_mesh_clear()
diff=difference(before,snapshot(actions));assert not diff,diff
assert all(sha(p)==hashes[str(p)]['sha256'] for p in inputs)
manifest={'task_id':'YURI_O1_GAZE_CORNER_NORMAL_PRIORITY_ADDENDUM_R1','inputs':hashes,'cases':results,'files':filemeta,
    'source_component_diff':diff,'source_preserved':True,'source_actions_preserved':len(actions),'source_saved':False,
    'muted13_bridge_drivers':muted,'OFF_restore':off,'CPU_job':{'workers':1,'Blender_threads':4,'Blender':bpy.app.version_string,'wall_seconds':time.monotonic()-start,'no_render_export_bake_GUI':True},
    'normal_domain':'ACTUAL evaluated modifier/GN mesh CORNER per original loop, separately retained local/world; not POINT averaged normals and not unevaluated original corner basis.',
    'coordinate_policy':'World meters Blender Z-up. Position p_local A^T+t once. Normal row n_local inverse(A), normalized float64 then float32. Tangent row t_local A^T projected orthogonal to world normal, normalized. Bitangent=sign cross(normal,tangent); world sign=local sign*determinant parity of A. Exact evaluated UV tangent basis per original UV, no Y flip.',
    'topology_policy':'Every case loop_vertex_indices/polygon loop start/total/material slots/UV equality exact vs frozen original mesh NPZ. Correspondence original stable loops; no corner collapse or new remap.',
    'quality':'Source reference only. Prior POINT-vs-splitCORNER149deg comparison is domain mismatch, not measured CORNER FAIL or waived gate. Actual Unity corner/gaze/PBR/F2/Player acceptance remains independent.'}
write('GAZE_EVALUATED_CORNER_MANIFEST.json',manifest);write('SOURCE_COMPONENT_DIFF.json',{'differences':diff,'before':before,'after':snapshot(actions)})
print('GAZE_CORNER_REFERENCE_COMPLETE',sum(v['bytes'] for v in filemeta),flush=True)
