"""One bounded CPU source extraction: full original body modifier stack.
Incremental <=80MiB uncompressed chunks; no export/render/bake/source save.
"""
import bpy,sys,json,gzip,hashlib,time,os
import numpy as np
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference
from r4_appearance_adapter import ReactionLane
LAB=HERE.parent;BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-full-body-deformation-reference-r1';E=LAB/'evidence/o1-full-body-deformation-reference-r1'
OUT.mkdir(parents=True,exist_ok=True);E.mkdir(parents=True,exist_ok=True)
SOURCE=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
LIB=BASE/'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'
NATIVE=BASE/'o1-native-unity-probe-r1';REC=BASE/'o1-source-fidelity-recovery-r1'
REF=NATIVE/'reference/native_evaluated_all_frames.json.gz'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def write(n,v):
    for p in (E/n,OUT/n):p.write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf8')
def arr(c,f,width=3,dtype=np.float32):
    a=np.empty(len(c)*width,dtype=dtype);c.foreach_get(f,a)
    return a.reshape(-1,width) if width>1 else a
inputs=[SOURCE,LIB,REF,NATIVE/'metadata/source_expanded_rigs.json',NATIVE/'metadata/source_renderers_bind.json',
    REC/'metadata/mesh_slot_UV_attributes_shape_deltas.json',REC/'metadata/CORNER_BASIS_RECEIPT.json',
    REC/'data/Meshy_Body_NeutralCovered_original_mesh.npz',REC/'data/Meshy_Body_NeutralCovered_corner_basis.npz',
    REC/'data/neutral.npz',HERE/'r4_appearance_adapter.py']
before_hash={str(p):{'sha256':sha(p),'bytes':p.stat().st_size} for p in inputs}
assert before_hash[str(SOURCE)]['sha256']=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
assert before_hash[str(LIB)]['sha256']=='6874ec69d5721f385d31edaa06ef0d58c89a543b98bacd961f8f575ff57eef4d'
start=time.monotonic();bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False)
s=bpy.context.scene;action_names=[a.name for a in bpy.data.actions];before=snapshot(action_names)
assert s.frame_current==1
body=bpy.data.objects['Meshy_Body_NeutralCovered'];rig_names=['Meshy_Fitted_Rig','Armature','Hair_Rig_R4','AVATAR_FaceBoard']
assert all(not bpy.data.objects[n].animation_data or not bpy.data.objects[n].animation_data.action for n in rig_names)
assert len(body.data.vertices)==63561
topology=np.load(inputs[7],allow_pickle=False)
def topology_check(m):
    for key,col,field in [('loop_vertex_indices',m.loops,'vertex_index'),('polygon_loop_start',m.polygons,'loop_start'),('polygon_loop_total',m.polygons,'loop_total'),('polygon_material_slot',m.polygons,'material_index')]:
        assert np.array_equal(arr(col,field,1,np.int32),topology[key]),key
    assert len(m.vertices)==63561 and len(m.uv_layers)==len(body.data.uv_layers)
    for i,u in enumerate(m.uv_layers):assert np.array_equal(arr(u.data,'uv',2),topology['uv_'+str(i)]),('uv',i)
def evaluate():
    deps=bpy.context.evaluated_depsgraph_get();o=body.evaluated_get(deps)
    m=o.to_mesh(preserve_all_data_layers=True,depsgraph=deps)
    try:
        topology_check(m);local=arr(m.vertices,'co');vn=arr(m.vertices,'normal');cn=arr(m.corner_normals,'vector')
        assert len(cn)==len(body.data.loops)
        mw=np.array(o.matrix_world,dtype=np.float64);linear=mw[:3,:3];inverse=np.linalg.inv(linear)
        def normal(n):
            world=n.astype(np.float64)@inverse;length=np.linalg.norm(world,axis=1)
            assert np.all(length>1e-12)
            return (world/length[:,None]).astype(np.float32)
        data={'local_position':local,'world_position':(local.astype(np.float64)@linear.T+mw[:3,3]).astype(np.float32),
            'local_vertex_normal':vn,'world_vertex_normal':normal(vn),
            'local_corner_normal':cn,'world_corner_normal':normal(cn)}
        assert all(np.isfinite(a).all() for a in data.values())
        return data
    finally:o.to_mesh_clear()
neutral=evaluate();frozenzero=np.load(inputs[9],allow_pickle=False)['Meshy_Body_NeutralCovered_world_position']
zero_delta=float(np.max(np.linalg.norm(neutral['world_position']-frozenzero,axis=1)))
assert zero_delta==0,('frozen OFF geometry mismatch',zero_delta)
inspection={'source_SHA256':sha(SOURCE),'frame':s.frame_current,'body_Action':None,'vertices':63561,'loops':len(body.data.loops),
    'polygons':len(body.data.polygons),'modifiers':[(m.name,m.type,m.show_viewport,m.show_render) for m in body.modifiers],
    'body_object_world':[list(r) for r in body.matrix_world],'source_expanded_bones':137,'OFF_matches_frozen_position_exact':True,
    'original_mesh_has_custom_normals':body.data.has_custom_normals,'CPU_factory_only':True,'pid':os.getpid()}
write('LIVE_SOURCE_INSPECTION.json',inspection);print('LIVE_INSPECTION_CONFIRMED',inspection,flush=True)
with gzip.open(REF,'rt',encoding='utf8') as f:refs=json.load(f)
assert len(refs)==6 and sum(len(v) for v in refs.values())==276
with bpy.data.libraries.load(str(LIB),link=False) as (src,dst):dst.actions=list(refs)
loaded={a.name:a for a in dst.actions};assert set(loaded)==set(refs)
lane=ReactionLane();chunks=[];clips=[];all_pose_delta=0;split_max=0;split_count_max=0
bytes_per_frame=sum(a.nbytes for a in neutral.values());chunk_frames=min(4,max(1,(80*1024**2)//bytes_per_frame))
assert bytes_per_frame<80*1024**2
for ci,(clip,frames) in enumerate(refs.items()):
    lane.on(clip);ad=bpy.data.objects['Meshy_Fitted_Rig'].animation_data
    assert ad.action==loaded[clip] and ad.action_slot.identifier=='OBMeshy_Fitted_Rig'
    folder=OUT/clip;folder.mkdir(exist_ok=True);buffer=[];frame_index=[];motion_max=0;first=None;pose_max=0;sample_reuse=[]
    def flush():
        if not buffer:return
        lo,hi=frame_index[0],frame_index[-1];p=folder/f'frames_{lo:03d}_{hi:03d}.npz'
        assert not p.exists(),('do not overwrite prior chunk',p)
        a={key:np.stack([v[key] for v in buffer]) for key in buffer[0]};a['source_frames']=np.array(frame_index,dtype=np.int32)
        assert sum(v.nbytes for v in a.values())<=80*1024**2
        np.savez_compressed(p,**a);assert p.stat().st_size<=100*1024**2
        # Read-back finite/count/hash validation at the chunk boundary.
        with np.load(p,allow_pickle=False) as z:
            for key,value in a.items():assert np.array_equal(z[key],value) and np.isfinite(z[key]).all()
        chunks.append({'path':p.relative_to(OUT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size,
            'clip':clip,'source_frames':list(frame_index),'uncompressed_bytes':sum(v.nbytes for v in a.values()),
            'arrays':{k:{'shape':list(v.shape),'dtype':str(v.dtype)} for k,v in a.items()}})
        buffer.clear();frame_index.clear();print('CHUNK_FROZEN',clip,lo,hi,flush=True)
    for f,reference in enumerate(frames,1):
        s.frame_set(f);bpy.context.view_layer.update()
        for n in rig_names:
            o=bpy.data.objects[n];assert len(o.pose.bones)==len(reference[n])
            for b in o.pose.bones:
                delta=float(np.max(np.abs(np.array(o.matrix_world@b.matrix,dtype=np.float64)-np.array(reference[n][b.name]['world_matrix'],dtype=np.float64))))
                pose_max=max(pose_max,delta);assert delta==0,(clip,f,n,b.name,delta)
        data=evaluate()
        if first is None:first=data['world_position'].copy()
        motion_max=max(motion_max,float(np.max(np.linalg.norm(data['world_position']-first,axis=1))))
        difference_normal=np.linalg.norm(data['local_corner_normal']-data['local_vertex_normal'][topology['loop_vertex_indices']],axis=1)
        split_max=max(split_max,float(difference_normal.max()));split_count_max=max(split_count_max,int(np.count_nonzero(difference_normal>1e-6)))
        buffer.append(data);frame_index.append(f)
        if len(buffer)==chunk_frames:flush()
    flush();assert motion_max>0
    end=len(frames);count=2*(end-1)+1 if 'Loop' in clip else end
    for sample in range(1,count+1):
        local=1+(sample-1)%(end-1) if 'Loop' in clip and sample>end else sample
        sample_reuse.append({'sample':sample,'source_frame':local,'time_seconds':(sample-1)/24})
    # Prove repeated sample resolves to exactly the same source evaluation, including
    # all downstream original modifiers: compare every frame repeated in cycle 2.
    reuse_max=0
    if 'Loop' in clip:
        cache=None;cachepath=None
        for sample in sample_reuse[end:]:
            f=sample['source_frame'];entry=next(c for c in chunks if c['clip']==clip and f in c['source_frames'])
            if cachepath!=entry['path']:
                if cache is not None:cache.close()
                cache=np.load(OUT/entry['path'],allow_pickle=False);cachepath=entry['path']
            s.frame_set(f);bpy.context.view_layer.update();again=evaluate();ix=entry['source_frames'].index(f)
            for key,val in again.items():
                d=float(np.max(np.abs(val-cache[key][ix])));reuse_max=max(reuse_max,d)
                assert np.array_equal(val,cache[key][ix]),('loop repeat differs',clip,f,key,d)
        if cache is not None:cache.close()
    lane.off();off=evaluate();off_deltas={k:float(np.max(np.abs(off[k]-neutral[k]))) for k in neutral}
    assert all(v==0 for v in off_deltas.values()),('OFF restore',clip,off_deltas)
    clips.append({'clip':clip,'authored_source_frames':end,'fps':24,'loop_inclusive_samples':count,
        'samples':sample_reuse,'all137_pose_matrix_element_delta_max':pose_max,'full_body_actual_motion_max_from_clip_frame1_m':motion_max,
        'loop_second_cycle_re_evaluation_array_max_delta':reuse_max,'loop_repeated_samples_verified':count-end,
        'OFF_return_deltas_all_arrays':off_deltas})
    all_pose_delta=max(all_pose_delta,pose_max);print('CLIP_COMPLETE',clip,end,count,motion_max,flush=True)
after=snapshot(action_names);component_diff=difference(before,after);assert not component_diff,component_diff
assert all(sha(p)==before_hash[str(p)]['sha256'] for p in inputs)
manifest={'task_id':'YURI_O1_FULL_BODY_DEFORMATION_REFERENCE_R1','inputs':before_hash,'source_component_diff':component_diff,
    'source_input_bytes_unchanged':True,'original_actions_preserved':len(action_names),'master_saved':False,
    'clip_count':6,'unique_authored_frames':276,'loop_inclusive_samples':384,'source_vertices':63561,'source_loops':len(body.data.loops),
    'all137_source_pose_matrix_max_element_delta':all_pose_delta,'frozen_OFF_world_position_max_delta_m':zero_delta,
    'coordinate_normal_policy':'Blender source world meters Z-up. Position row vector p_world=p_local A^T+t, object world transform once. Normal row vector n_world=normalize(n_local inverse(A)); equivalent column inverse-transpose, not position transform. Full evaluated source corner normal per original loop retained separately from averaged vertex normal; world normal normalized in float64 then float32 storage. No handedness/Y conversion.',
    'index_topology_policy':'Original ordered63561vertices and original corner/loop order; exact per-frame loop_vertex_indices,polygon_loop_start/total/material_slot and UV checked against frozen source original mesh NPZ. Split normals not averaged. Triangulation/UV/material/rest original pointers reused.',
    'normal_split_diagnostic':{'max_local_corner_vs_averaged_vertex_normal_vector_difference':split_max,'max_corners_differing_over_1e-6':split_count_max},
    'chunks':chunks,'clips':clips,'chunk_frame_limit':chunk_frames,'max_chunk_uncompressed_bytes':max(c['uncompressed_bytes'] for c in chunks),
    'total_NPZ_bytes':sum(c['bytes'] for c in chunks),'CPU_job':{'job_count':1,'workers':1,'Blender_threads':4,'Blender':bpy.app.version_string,'pid':os.getpid(),'wall_seconds':time.monotonic()-start,'frames_data_evaluated':1+276+108+6,'no_GUI_export_render_bake':True},
    'acceptance':'Reference custody only; not Unity deformation/PBR/F2/Player PASS. Native source rig, posed5helper scales, .535 hierarchy, modifiers/morphs/drivers/rest/weights untouched; existing Blender imported rotation FAIL unaffected.'}
write('FULL_BODY_DEFORMATION_MANIFEST.json',manifest)
write('SOURCE_COMPONENT_DIFF.json',{'differences':component_diff,'before':before,'after':after})
print('FULL_BODY_REFERENCE_COMPLETE',len(chunks),manifest['total_NPZ_bytes'],manifest['CPU_job']['wall_seconds'],flush=True)
