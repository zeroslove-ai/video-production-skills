"""One bounded read-only CPU Blender probe; source is never saved/exported.

276 unique authored frames: original pose-channel quaternions and five factors.
Only Strong6/Startle11: cumulative original seven-stage position/corner normals.
"""
import bpy, sys, json, gzip, hashlib, time, os
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference
from r4_appearance_adapter import ReactionLane
LAB=HERE.parent
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-raw-pose-driver-stage-reference-r1';E=LAB/'evidence/o1-raw-pose-driver-stage-reference-r1'
OUT.mkdir(exist_ok=True);E.mkdir(exist_ok=True)
assert not (OUT/'RAW_POSE_DRIVER_STAGE_MANIFEST.json').exists(),'Do not overwrite frozen result'
assert not list(OUT.glob('*.npz')),'Existing data; select a new version rather than overwrite'
SOURCE=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
LIB=BASE/'r4-appearance-preserve-correction-r1/YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'
N=BASE/'o1-native-unity-probe-r1';R=BASE/'o1-source-fidelity-recovery-r1'
FULL=BASE/'o1-full-body-deformation-reference-r1'
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
def arr(c,field,width=3,dtype=np.float32):
    v=np.empty(len(c)*width,dtype);c.foreach_get(field,v);return v.reshape(-1,width) if width>1 else v
record(SOURCE);record(LIB)
assert inputs[str(SOURCE)]['sha256']=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
assert inputs[str(LIB)]['sha256']=='6874ec69d5721f385d31edaa06ef0d58c89a543b98bacd961f8f575ff57eef4d'
reference=json.loads(gzip.decompress(record(N/'reference/native_evaluated_all_frames.json.gz').read_bytes()))
full=load(FULL/'FULL_BODY_DEFORMATION_MANIFEST.json')
metadata=next(x for x in load(R/'metadata/mesh_slot_UV_attributes_shape_deltas.json') if x['renderer']=='Meshy_Body_NeutralCovered')
topology=np.load(record(R/'data/Meshy_Body_NeutralCovered_original_mesh.npz'),allow_pickle=False)
record(HERE/'r4_appearance_adapter.py');record(HERE/'r4_appearance_signature.py');record(HERE/'native_preservation.py')
start=time.monotonic();bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False)
s=bpy.context.scene;original_actions=[a.name for a in bpy.data.actions]
assert s.frame_current==1 and len(original_actions)==78
assert bpy.context.scene.render.threads_mode!='FIXED' or bpy.context.scene.render.threads>=1
before=snapshot(original_actions)
body=bpy.data.objects['Meshy_Body_NeutralCovered'];rig=bpy.data.objects['Meshy_Fitted_Rig']
bone_names=[b.name for b in rig.pose.bones];assert len(bone_names)==57
modifier_names=[m.name for m in body.modifiers];assert len(modifier_names)==7
assert [m.type for m in body.modifiers]==['ARMATURE','ARMATURE','CORRECTIVE_SMOOTH','SMOOTH','SMOOTH','SMOOTH','SMOOTH']
drivers={d['output_path']:d for d in metadata['object_drivers']}
factor_paths=[f'modifiers[{json.dumps(n)}].factor' for n in modifier_names[2:]]
assert set(factor_paths)==set(drivers)
def raw_channels():return np.array([tuple(rig.pose.bones[n].rotation_quaternion) for n in bone_names],np.float32)
def factors():return np.array([getattr(body.modifiers[n],'factor') for n in modifier_names[2:]],np.float32)
baseline_q=raw_channels();baseline_factor=factors()
with bpy.data.libraries.load(str(LIB),link=False) as (src,dst):dst.actions=list(reference)
assert all(a is not None for a in dst.actions)
lane=ReactionLane();arrays={};clips=[];files=[];stage_rows=[];world_pose_max=0.
problems={'YRA_R4_Struggle_Strong_Loop':6,'YRA_R4_Startle_Short':11}
def evaluated(o):
    deps=bpy.context.evaluated_depsgraph_get();ev=o.evaluated_get(deps)
    mesh=ev.to_mesh(preserve_all_data_layers=True,depsgraph=deps)
    try:
        assert len(mesh.vertices)==63561 and len(mesh.loops)==254602
        for key,col,field in [('loop_vertex_indices',mesh.loops,'vertex_index'),('polygon_loop_start',mesh.polygons,'loop_start'),('polygon_loop_total',mesh.polygons,'loop_total'),('polygon_material_slot',mesh.polygons,'material_index')]:
            assert np.array_equal(arr(col,field,1,np.int32),topology[key]),key
        for i,uv in enumerate(mesh.uv_layers):assert np.array_equal(arr(uv.data,'uv',2),topology['uv_'+str(i)])
        local=arr(mesh.vertices,'co');cn=arr(mesh.corner_normals,'vector')
        mw=np.array(ev.matrix_world,np.float64);world=(local.astype(np.float64)@mw[:3,:3].T+mw[:3,3]).astype(np.float32)
        wn=cn.astype(np.float64)@np.linalg.inv(mw[:3,:3]);wn/=np.linalg.norm(wn,axis=1)[:,None];wn=wn.astype(np.float32)
        assert all(np.isfinite(v).all() for v in (world,wn))
        return {'world_position':world,'world_corner_normal':wn},local,cn
    finally:ev.to_mesh_clear()
def metrics(a,b):
    d=np.linalg.norm(a.astype(np.float64)-b.astype(np.float64),axis=1)
    return {'max_m':float(d.max()),'RMS_m':float(np.sqrt(np.mean(d*d))),'p95_m':float(np.percentile(d,95)),'worst_source_vertex':int(d.argmax())}
def capture_stages(clip,frame):
    clone=body.copy();clone.name='R4_BOUNDED_STAGE_READONLY';s.collection.objects.link(clone)
    clone.hide_render=True;clone.hide_viewport=False;clone.hide_set(False)
    data={};rows=[];previous=None
    try:
        for last in range(7):
            flags=[]
            for i,(m,src) in enumerate(zip(clone.modifiers,body.modifiers)):
                m.show_viewport=bool(src.show_viewport and i<=last)
                m.show_render=bool(src.show_render and i<=last)
                flags.append({'order':i,'name':m.name,'type':m.type,'show_viewport':m.show_viewport,'show_render':m.show_render})
            clone.update_tag();bpy.context.view_layer.update()
            for i in range(2,7):assert clone.modifiers[i].factor==body.modifiers[i].factor,(clip,frame,i)
            stage,local,cn=evaluated(clone)
            for key,value in stage.items():data[f'stage_{last:02d}_{key}']=value
            row={'clip':clip,'source_frame':frame,'last_enabled_order':last,'modifier_flags':flags,
                'original_driver_factors':factors().tolist(),'world_object_matrix':[list(r) for r in clone.matrix_world],
                'later_modifiers_disabled_on_disposable_object_only':True}
            if previous is not None:
                row['incremental_world_position_delta']=metrics(stage['world_position'],previous['world_position'])
                row['incremental_world_corner_normal_vector_max_delta']=float(np.max(np.linalg.norm(stage['world_corner_normal']-previous['world_corner_normal'],axis=1)))
            if last==6:
                chunk=next(c for c in full['chunks'] if c['clip']==clip and frame in c['source_frames'])
                pointer=record(FULL/chunk['path']);assert sha(pointer)==chunk['sha256']
                with np.load(pointer,allow_pickle=False) as z:
                    ix=chunk['source_frames'].index(frame)
                    diffs={'local_position':float(np.max(np.abs(local-z['local_position'][ix]))),
                        'local_corner_normal':float(np.max(np.abs(cn-z['local_corner_normal'][ix]))),
                        'world_position':float(np.max(np.abs(stage['world_position']-z['world_position'][ix]))),
                        'world_corner_normal':float(np.max(np.abs(stage['world_corner_normal']-z['world_corner_normal'][ix])))}
                    assert all(v==0 for v in diffs.values()),(clip,frame,diffs)
                row['existing_full_stack_reference_exact_deltas']=diffs
                row['reference_chunk']={'path':chunk['path'],'sha256':chunk['sha256'],'frame_offset':ix}
            rows.append(row);previous=stage
            print('STAGE_CAPTURED',clip,frame,last,row.get('incremental_world_position_delta'),flush=True)
        target=OUT/f'{clip}_frame{frame:03d}_seven_stages.npz'
        assert not target.exists();np.savez_compressed(target,**data)
        with np.load(target,allow_pickle=False) as z:
            for key,val in data.items():assert np.array_equal(val,z[key]) and np.isfinite(z[key]).all()
        files.append({'path':target.name,'sha256':sha(target),'bytes':target.stat().st_size,
            'uncompressed_bytes':sum(v.nbytes for v in data.values()),'arrays':{k:{'shape':list(v.shape),'dtype':str(v.dtype)} for k,v in data.items()}})
        stage_rows.extend(rows)
    finally:bpy.data.objects.remove(clone,do_unlink=True);bpy.context.view_layer.update()
for ci,(clip,frames) in enumerate(reference.items()):
    lane.on(clip);q=[];fac=[];paths=[]
    ad=rig.animation_data;assert ad.action.name==clip and ad.action_slot.identifier=='OBMeshy_Fitted_Rig'
    for frame,expected in enumerate(frames,1):
        s.frame_set(frame);bpy.context.view_layer.update()
        for rn,bones in expected.items():
            obj=bpy.data.objects[rn]
            for name,v in bones.items():
                delta=float(np.max(np.abs(np.array(obj.matrix_world@obj.pose.bones[name].matrix,np.float64)-np.array(v['world_matrix'],np.float64))))
                world_pose_max=max(world_pose_max,delta);assert delta==0,(clip,frame,rn,name,delta)
        q.append(raw_channels());fac.append(factors())
        assert all(np.isfinite(a).all() for a in (q[-1],fac[-1]))
        if problems.get(clip)==frame:capture_stages(clip,frame)
    arrays[f'clip_{ci}_raw_quaternion_wxyz']=np.stack(q)
    arrays[f'clip_{ci}_five_driver_factors']=np.stack(fac)
    end=len(frames);count=2*(end-1)+1 if 'Loop' in clip else end
    semantics=[{'sample':v,'source_frame':1+(v-1)%(end-1) if 'Loop' in clip and v>end else v,'time_seconds':(v-1)/24} for v in range(1,count+1)]
    repeated=0
    for sample in semantics[end:]:
        f=sample['source_frame'];s.frame_set(f);bpy.context.view_layer.update()
        assert np.array_equal(raw_channels(),q[f-1]) and np.array_equal(factors(),fac[f-1]),('second cycle mismatch',clip,f)
        repeated+=1
    clips.append({'clip':clip,'array_prefix':f'clip_{ci}','unique_source_frames':end,'loop_inclusive_samples':count,
        'fps':24,'time_policy':'source_frame f evaluated directly; authored seconds=(f-1)/24',
        'Action':ad.action.name,'action_slot':ad.action_slot.identifier,'samples':semantics,'second_cycle_actual_rechecks':repeated})
    lane.off();assert np.array_equal(raw_channels(),baseline_q) and np.array_equal(factors(),baseline_factor)
    print('RAW_CLIP_COMPLETE',clip,end,count,flush=True)
target=OUT/'R4_All6_Raw_Pose_Quaternions_And_Five_Driver_Factors.npz';assert not target.exists()
np.savez_compressed(target,**arrays)
with np.load(target,allow_pickle=False) as z:
    for key,val in arrays.items():assert np.array_equal(val,z[key]) and np.isfinite(z[key]).all()
files.append({'path':target.name,'sha256':sha(target),'bytes':target.stat().st_size,
    'arrays':{k:{'shape':list(v.shape),'dtype':str(v.dtype)} for k,v in arrays.items()}})
after=snapshot(original_actions);diff=difference(before,after);assert not diff,diff
assert all(sha(Path(p))==v['sha256'] for p,v in inputs.items())
write('SOURCE_COMPONENT_DIFF.json',{'differences':diff,'before':before,'after':after})
manifest={'task_id':'YURI_O1_RAW_POSE_DRIVER_AND_BOUNDED_STAGE_REFERENCE_R1','status':'DONE_SOURCE_REFERENCE_RUNTIME_GATE_PENDING',
    'inputs':inputs,'source_input_bytes_unchanged':True,'source_component_diff':diff,'original_actions_preserved':len(original_actions),
    'master_saved':False,'source_exports':0,'renders':0,'existing_GUI_touched':False,
    'original_body_bone_order':bone_names,'original_bone_rotation_modes':[rig.pose.bones[n].rotation_mode for n in bone_names],
    'raw_channel_policy':'Original pose.bones[name].rotation_quaternion[0..3] SINGLE_PROP wxyz; no world/local TRS conversion or additional normalization.',
    'five_factor_paths':factor_paths,'original_driver_definitions':metadata['object_drivers'],
    'ordered_original_modifiers':metadata['modifiers'],'clips':clips,'unique_frames':sum(len(v) for v in reference.values()),
    'loop_inclusive_samples':sum(v['loop_inclusive_samples'] for v in clips),'all137_frozen_world_pose_max_element_delta':world_pose_max,
    'stage_references':stage_rows,'stage_normal_policy':'Original polygon CORNER index; world normal = normalize(local normal @ inverse(object linear matrix)) computed float64 then float32. No vertex averaging, UV tangent substitution or Unity axis conversion.',
    'stage_evaluation_policy':'Cumulative stages0..last on disposable original-body object copy sharing read-only mesh; later modifiers disabled on copy only. Exact原 settings/masks/driver factors kept. Full cumulative stage6 agrees existing frozen full stack arrays bit-for-bit at both frames.',
    'limitations':'Intermediate corner normals are recomputed by native Blender at each ablation; not the final normals with an isolated last-stage normal delta. Stage contribution deltas are cumulative/nonlinear, not additive correction vectors for general motion.',
    'CPU_job':{'job_count':1,'workers':1,'threads':4,'pid':os.getpid(),'Blender':bpy.app.version_string,'build_hash':bpy.app.build_hash.decode(),'wall_seconds':time.monotonic()-start},
    'files':files,'all_file_readbacks_exact_and_finite':True,'acceptance':'Source reference custody only; no Unity runtime/appearance/AlwaysAnimate PASS.'}
assert manifest['unique_frames']==276 and manifest['loop_inclusive_samples']==384
write('RAW_POSE_DRIVER_STAGE_MANIFEST.json',manifest)
print('RAW_POSE_DRIVER_STAGE_COMPLETE',manifest['CPU_job']['wall_seconds'],sum(v['bytes'] for v in files),flush=True)
