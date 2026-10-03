"""Four-frame read-only CPU source probe. Actual evaluated Blender inputs,
not an actual Cycles renderer-buffer capture; no save/export/render/rig edits.
"""
import bpy,sys,json,gzip,hashlib,time,os
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference
from r4_appearance_adapter import ReactionLane
LAB=HERE.parent;BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-dynamic-body-cycles-input-reference-r1';E=LAB/'evidence/o1-dynamic-body-cycles-input-reference-r1'
OUT.mkdir(exist_ok=True);E.mkdir(exist_ok=True)
assert not (OUT/'DYNAMIC_BODY_CYCLES_INPUT_MANIFEST.json').exists() and not list(OUT.glob('*.npz')),'Do not overwrite prior outputs'
SOURCE=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
LIB=BASE/'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'
R=BASE/'o1-source-fidelity-recovery-r1';N=BASE/'o1-native-unity-probe-r1';FULL=BASE/'o1-full-body-deformation-reference-r1'
inputs={}
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def record(p):inputs[str(p)]={'sha256':sha(p),'bytes':p.stat().st_size};return p
def load(p):return json.loads(record(p).read_text(encoding='utf8'))
def write(n,v):
    for p in (OUT,E):(p/n).write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf8')
def arr(c,f,w=3,dtype=np.float32):
    a=np.empty(len(c)*w,dtype);c.foreach_get(f,a);return a.reshape(-1,w) if w>1 else a
record(SOURCE);record(LIB)
assert inputs[str(SOURCE)]['sha256']=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
assert inputs[str(LIB)]['sha256']=='6874ec69d5721f385d31edaa06ef0d58c89a543b98bacd961f8f575ff57eef4d'
full=load(FULL/'FULL_BODY_DEFORMATION_MANIFEST.json')
ref=json.loads(gzip.decompress(record(N/'reference/native_evaluated_all_frames.json.gz').read_bytes()))
topo=np.load(record(R/'data/Meshy_Body_NeutralCovered_original_mesh.npz'),allow_pickle=False)
rest=np.load(record(R/'data/Meshy_Body_NeutralCovered_corner_basis.npz'),allow_pickle=False)
meta=next(m for m in load(R/'metadata/mesh_slot_UV_attributes_shape_deltas.json') if m['renderer']=='Meshy_Body_NeutralCovered')
record(N/'metadata/source_expanded_rigs.json')
for name in ('r4_appearance_adapter.py','r4_appearance_signature.py','native_preservation.py'):record(HERE/name)
start=time.monotonic();bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False)
s=bpy.context.scene;original_actions=[a.name for a in bpy.data.actions]
assert len(original_actions)==78 and s.frame_current==1
before=snapshot(original_actions)
body=bpy.data.objects['Meshy_Body_NeutralCovered'];rig=bpy.data.objects['Meshy_Fitted_Rig']
assert len(rig.pose.bones)==57 and sum(len(o.pose.bones) for o in bpy.data.objects if o.type=='ARMATURE')==137
bridge=bpy.data.objects['Character_Body_Head'].data.shape_keys.animation_data.drivers
muted=[{'path':f.data_path,'mute':f.mute,'expression':f.driver.expression} for f in bridge if 'slide / 0.055' in f.driver.expression]
assert len(muted)==13 and all(f['mute'] for f in muted)
assert [m.type for m in body.modifiers]==['ARMATURE','ARMATURE','CORRECTIVE_SMOOTH','SMOOTH','SMOOTH','SMOOTH','SMOOTH']
cases=[('YRA_R4_Startle_Short',1),('YRA_R4_Startle_Short',11),('YRA_R4_Struggle_Strong_Loop',6),('YRA_R4_Struggle_Strong_Loop',44)]
with bpy.data.libraries.load(str(LIB),link=False) as (src,dst):dst.actions=list(dict.fromkeys(clip for clip,_ in cases))
lane=ReactionLane();rows=[];files=[];max_pose_delta=0
def triangle_stats(tris,polys):
    rt=rest['loop_triangle_loops'];rp=rest['triangle_polygon_index']
    assert tris.shape==rt.shape and np.array_equal(polys,rp),'Triangle count/polygon route changed'
    changed=np.any(tris!=rt,axis=1);changed_poly=np.unique(polys[changed])
    # Compare actual corner sets to distinguish diagonal changes from mere triangle ordering.
    diagonal=[];order=[]
    for pi in changed_poly:
        mask=polys==pi
        a=sorted(tuple(sorted(v)) for v in tris[mask].tolist())
        b=sorted(tuple(sorted(v)) for v in rt[mask].tolist())
        (diagonal if a!=b else order).append(int(pi))
    sizes=topo['polygon_loop_total']
    return {'triangle_rows_different_from_rest':int(changed.sum()),'polygons_with_different_rows':len(changed_poly),
        'corner_set_topology_changed_polygons':len(diagonal),'triangle_order_or_winding_only_polygons':len(order),
        'quad_diagonal_changed_polygons':int(sum(sizes[i]==4 for i in diagonal)),
        'ngon_triangulation_changed_polygons':int(sum(sizes[i]>4 for i in diagonal)),
        'changed_source_polygon_ids':diagonal,'order_only_source_polygon_ids':order}
try:
    for clip,frame in cases:
        lane.on(clip);s.frame_set(frame);bpy.context.view_layer.update()
        for rn,bones in ref[clip][frame-1].items():
            o=bpy.data.objects[rn]
            for name,v in bones.items():
                delta=float(np.max(np.abs(np.array(o.matrix_world@o.pose.bones[name].matrix,np.float64)-np.array(v['world_matrix'],np.float64))))
                max_pose_delta=max(max_pose_delta,delta);assert delta==0,(clip,frame,rn,name,delta)
        deps=bpy.context.evaluated_depsgraph_get();ev=body.evaluated_get(deps)
        mesh=ev.to_mesh(preserve_all_data_layers=True,depsgraph=deps)
        try:
            for k,col,field in [('loop_vertex_indices',mesh.loops,'vertex_index'),('polygon_loop_start',mesh.polygons,'loop_start'),('polygon_loop_total',mesh.polygons,'loop_total'),('polygon_material_slot',mesh.polygons,'material_index')]:
                assert np.array_equal(arr(col,field,1,np.int32),topo[k]),k
            assert len(mesh.vertices)==63561 and len(mesh.loops)==254602
            uv=arr(mesh.uv_layers['UVMap'].data,'uv',2);assert np.array_equal(uv,topo['uv_0'])
            p=arr(mesh.vertices,'co');cn=arr(mesh.corner_normals,'vector');mw=np.array(ev.matrix_world,np.float64)
            world=(p.astype(np.float64)@mw[:3,:3].T+mw[:3,3]).astype(np.float32)
            wn=cn.astype(np.float64)@np.linalg.inv(mw[:3,:3]);wn/=np.linalg.norm(wn,axis=1)[:,None];wn=wn.astype(np.float32)
            mesh.calc_loop_triangles()
            tc=arr(mesh.loop_triangles,'loops',3,np.int32);tv=arr(mesh.loop_triangles,'vertices',3,np.int32)
            tp=arr(mesh.loop_triangles,'polygon_index',1,np.int32)
            assert np.array_equal(tv,topo['loop_vertex_indices'][tc])
            polygon_of_corner=np.repeat(np.arange(len(topo['polygon_loop_total']),dtype=np.int32),topo['polygon_loop_total'])
            assert np.array_equal(polygon_of_corner[tc],np.repeat(tp[:,None],3,axis=1))
            packed_attr=mesh.attributes['custom_normal'];packed=np.empty((len(mesh.loops),2),np.int32)
            packed_attr.data.foreach_get('value',packed.reshape(-1));assert np.array_equal(packed,topo['attribute_13_value'])
            sharp=arr(mesh.attributes['sharp_edge'].data,'value',1,np.int32);assert np.array_equal(sharp,topo['attribute_8_value'])
            data={'current_local_position':p,'current_world_position':world,'current_local_corner_normal':cn,'current_world_corner_normal':wn,
                'current_corner_UVMap':uv,'current_triangle_source_corners':tc,'current_triangle_source_vertices':tv,
                'current_triangle_source_polygon':tp,'current_triangle_material_slot':topo['polygon_material_slot'][tp],
                'body_object_world':mw,'source_vertex_id':np.arange(len(p),dtype=np.int32),
                'original_corner_to_source_vertex':topo['loop_vertex_indices'],
                'original_custom_normal_short2':packed.astype(np.int16)}
            assert all(np.isfinite(v).all() for v in data.values())
            chunk=next(c for c in full['chunks'] if c['clip']==clip and frame in c['source_frames'])
            f=record(FULL/chunk['path']);assert sha(f)==chunk['sha256']
            with np.load(f,allow_pickle=False) as z:
                ix=chunk['source_frames'].index(frame)
                diffs={k:float(np.max(np.abs(a-z[rk][ix]))) for k,a,rk in [
                    ('local_position',p,'local_position'),('world_position',world,'world_position'),
                    ('local_corner_normal',cn,'local_corner_normal'),('world_corner_normal',wn,'world_corner_normal')]}
                assert all(v==0 for v in diffs.values()),(clip,frame,diffs)
            target=OUT/f'{clip}_frame{frame:03d}_actual_evaluated_cycles_inputs.npz';assert not target.exists()
            np.savez_compressed(target,**data)
            with np.load(target,allow_pickle=False) as z:
                for key,val in data.items():assert np.array_equal(z[key],val) and np.isfinite(z[key]).all()
            item={'path':target.name,'bytes':target.stat().st_size,'sha256':sha(target),
                'uncompressed_bytes':sum(v.nbytes for v in data.values()),'arrays':{k:{'shape':list(v.shape),'dtype':str(v.dtype)} for k,v in data.items()}}
            files.append(item)
            row={'clip':clip,'frame':frame,'authored_seconds':(frame-1)/24,'Action':rig.animation_data.action.name,
                'action_slot':rig.animation_data.action_slot.identifier,'file':item,'triangles':len(tc),
                'raw_body_pose_quaternion_wxyz':[[b.name,list(b.rotation_quaternion)] for b in rig.pose.bones],
                'original_modifier_factors':[{'name':m.name,'factor':m.factor} for m in body.modifiers if m.type in ('SMOOTH','CORRECTIVE_SMOOTH')],
                'full_body_reference_exact_deltas':diffs,'reference_chunk':chunk['path'],'reference_chunk_sha256':chunk['sha256'],
                'original_packed_custom_normal_unchanged':True,'sharp_edges_unchanged':True,
                'rest_triangulation_comparison':triangle_stats(tc,tp),'evaluated_topology_and_UV_exact_original':True,
                'not_actual_Cycles_renderer_buffer':True}
            rows.append(row);print('DYNAMIC_INPUT_CAPTURED',clip,frame,item['bytes'],row['rest_triangulation_comparison'],flush=True)
        finally:ev.to_mesh_clear()
        lane.off()
finally:lane.off()
after=snapshot(original_actions);diff=difference(before,after);assert not diff,diff
assert all(sha(Path(p))==v['sha256'] for p,v in inputs.items())
assert all(f.mute for f in bridge if 'slide / 0.055' in f.driver.expression)
write('SOURCE_COMPONENT_DIFF.json',{'differences':diff,'before':before,'after':after})
manifest={'task_id':'ROOT_PM_O1_DYNAMIC_BODY_CYCLES_INPUT_REFERENCE_R1','status':'DONE_EVALUATED_INPUT_REFERENCE_ACTUAL_CYCLES_BUFFER_HOLD',
    'inputs':inputs,'source_input_bytes_unchanged':True,'source_component_diff':diff,'original_Actions_preserved':len(original_actions),
    'original137_rest_and_hierarchy_preserved':True,'muted13_bridge_drivers':muted,'all137_frozen_world_pose_max_element_delta':max_pose_delta,
    'source_saved':False,'export_render_GPU_tasks':0,'existing_GUI_touched':False,
    'coordinate_policy':'Actual evaluated Blender local geometry and world meters Z-up. World normal row=normalize(local normal @ inverse(object linear)); position world transform applied once. Original polygon/source corner/vertex indices retained, no Unity basis conversion.',
    'scope_limit':'Four selected actual Blender-evaluated inputs only. Full-body chunks are identity/position/normal QA references, not substitutes for dynamic tessellation. No Cycles packed-normal/tangent/shader buffers captured.',
    'frames':rows,'files':files,'CPU_job':{'job_count':1,'workers':1,'threads':4,'pid':os.getpid(),'Blender':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode(),'wall_seconds':time.monotonic()-start},
    'runtime_tangent_PBR_verdict':'HOLD'}
write('DYNAMIC_BODY_CYCLES_INPUT_MANIFEST.json',manifest)
print('DYNAMIC_BODY_CYCLES_INPUT_COMPLETE',manifest['CPU_job']['wall_seconds'],sum(v['bytes'] for v in files),flush=True)
