"""NOT AUTHORIZED. Two inputs/head only; requires NEW reviewed owner guard receipt.
Syntax-check only until Root PM approves this exact collector and a passing guard.
"""
import argparse, hashlib, json, os, sys
from pathlib import Path

SOURCE_SHA='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
INPUT_SHA={'WORST':'170accdfe80954ae2fe340e1aca3bdef5ac2e7fd25049be2089ab69766bd77a2',
           'NEUTRAL':'b775d6252cc4e9c3703d76e5747a7113bfb5d8318f1d1ff5e9b2b73df5d53961'}
FACE=['JawOpen','Smile.L','Smile.R','Blink.L','Blink.R','BrowRaise.L','BrowRaise.R',
      'BrowKnit.L','BrowKnit.R','CheekLift.L','CheekLift.R','LipPucker','MouthWide',
      'ExprSmileCurve','ExprMouthDown','ExprBrowInnerUp']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--clone',required=True);ap.add_argument('--inputs',required=True)
    ap.add_argument('--out',required=True);ap.add_argument('--new-approval',required=True);ap.add_argument('--guard-before',required=True)
    args=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    approval=json.loads(Path(args.new_approval).read_text());guard=json.loads(Path(args.guard_before).read_text())
    assert approval['task']=='ROOT_PM_MORPH67_TWO_INPUT_SOURCE_NORMAL_GAP_R1'
    assert approval['new_exact_packet_authorized'] is True and approval['historical_sampler_approval_reused'] is False
    assert approval['collector_sha256']==sha(Path(__file__))
    assert guard['status']=='STRICT_IDENTITY_BEFORE_PASS' and guard['owned_pid']==os.getpid()
    assert guard['QueryFullProcessImageName_success'] is True and guard['job_active_limit']==1
    assert guard['executable_sha256']=='284f4041f98e113f3dc10654a7193ffaaa9bfdfec8b87fa116620a48b5f6d4cb'
    clone=Path(args.clone);inputs=Path(args.inputs);out=Path(args.out)
    master=Path(__file__).resolve().parent.parent/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
    assert clone.resolve()!=master.resolve() and sha(master)==sha(clone)==SOURCE_SHA
    assert not out.exists();out.mkdir()
    data={tag:json.loads((inputs/(tag+'_source_inputs_PRIVATE_R1.json')).read_bytes()) for tag in INPUT_SHA}
    assert all(sha(inputs/(tag+'_source_inputs_PRIVATE_R1.json'))==v for tag,v in INPUT_SHA.items())
    import bpy
    import numpy as np
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    from r4_appearance_signature import snapshot,difference
    bpy.ops.wm.open_mainfile(filepath=str(clone),use_scripts=False)
    scene=bpy.context.scene;assert scene.frame_current==1
    head=bpy.data.objects['Character_Body_Head'];keys=head.data.shape_keys
    assert keys.name=='FaceControls_TEST_Jaw_Smile.001' and len(keys.key_blocks)==72
    assert [m.type for m in head.modifiers]==['NODES','ARMATURE']
    assert head.animation_data is None or head.animation_data.action is None
    assert keys.animation_data.action is None
    muted=[(d.data_path,d.mute) for d in keys.animation_data.drivers if d.mute]
    assert len(muted)==13
    actions=[a.name for a in bpy.data.actions];assert len(actions)==78
    saved={k:keys.key_blocks[k].value for k in FACE};gaze={k:head[k] for k in ['Face_GazeYaw','Face_GazePitch']}
    flags=[(m.show_viewport,m.show_render) for m in head.modifiers]
    before=snapshot(actions)
    npz=inputs.parent/'o1-source-fidelity-recovery-r1/data/Character_Body_Head_original_mesh.npz'
    assert sha(npz)=='1a48cf823cb6cf0c95c7eee6d4b7e7e8a952cbaadd50d1d9ad18d909be34f473'
    topology=np.load(npz,allow_pickle=False)
    def arr(c,field,width=3,dtype=np.float32):
        v=np.empty(len(c)*width,dtype=dtype);c.foreach_get(field,v);return v.reshape(-1,width) if width>1 else v
    def capture(label):
        head.update_tag();keys.update_tag();scene.frame_set(1);bpy.context.view_layer.update()
        deps=bpy.context.evaluated_depsgraph_get();obj=head.evaluated_get(deps)
        mesh=obj.to_mesh(preserve_all_data_layers=True,depsgraph=deps)
        try:
            assert (len(mesh.vertices),len(mesh.loops),len(mesh.polygons))==(12928,66861,21701)
            a={'local_position':arr(mesh.vertices,'co'),'local_CORNER_normal':arr(mesh.corner_normals,'vector'),
               'loop_vertex_indices':arr(mesh.loops,'vertex_index',1,np.int32),
               'polygon_loop_start':arr(mesh.polygons,'loop_start',1,np.int32),
               'polygon_loop_total':arr(mesh.polygons,'loop_total',1,np.int32),
               'polygon_material_slot':arr(mesh.polygons,'material_index',1,np.int32),
               'polygon_use_smooth':arr(mesh.polygons,'use_smooth',1,np.int32),
               'UVMap':arr(mesh.uv_layers['UVMap'].data,'uv',2),
               'world_matrix':np.array(obj.matrix_world,dtype=np.float64)}
            for field in ['loop_vertex_indices','polygon_loop_start','polygon_loop_total','polygon_material_slot']:
                assert np.array_equal(a[field],topology[field]),(label,field)
            assert np.array_equal(a['UVMap'],topology['uv_0'])
            attr=mesh.attributes.get('custom_normal')
            attr_meta={'present':attr is not None,'domain':attr.domain if attr else None,'data_type':attr.data_type if attr else None}
            if attr and attr.data_type=='INT16_2D':a['custom_normal_short2']=arr(attr.data,'value',2,np.int32)
            elif attr and attr.data_type=='FLOAT_VECTOR':a['custom_normal_vector']=arr(attr.data,'vector')
            for name in ['sharp_edge','sharp_face']:
                at=mesh.attributes.get(name)
                if at is not None:a[name]=arr(at.data,'value',1,np.int32)
            mesh.calc_loop_triangles();a['triangle_source_corners']=arr(mesh.loop_triangles,'loops',3,np.int32)
            a['triangle_source_polygon']=arr(mesh.loop_triangles,'polygon_index',1,np.int32)
            # Head is tri/quad only; use same RNA route as existing head authority.
            mesh.calc_tangents(uvmap='UVMap');a['local_CORNER_tangent']=arr(mesh.loops,'tangent')
            a['bitangent_sign']=arr(mesh.loops,'bitangent_sign',1)
            assert all(np.isfinite(v).all() for v in a.values())
            assert np.all(np.linalg.norm(a['local_CORNER_normal'],axis=1)>0)
            p=out/(label+'_PRIVATE_R1.npz');np.savez_compressed(p,**a)
            assert sum(x.stat().st_size for x in out.iterdir() if x.is_file())<64*1024**2
            return {'case':label,'file':p.name,'bytes':p.stat().st_size,'sha256':sha(p),
                    'has_custom_normals':mesh.has_custom_normals,
                    'evaluated_custom_normal_attribute':attr_meta,
                    'arrays':{k:{'shape':list(v.shape),'dtype':str(v.dtype)} for k,v in a.items()}}
        finally:obj.to_mesh_clear()
    records=[];key_readbacks={};morph_comparison={}
    try:
        baseline=capture('OFF_before')
        for tag,d in data.items():
            assert d['ReactionIntent']=='NONE' and len(d['native_face'])==16
            for name,v in zip(FACE,d['native_face']):keys.key_blocks[name].value=v
            head['Face_GazeYaw']=d['NativeYaw'];head['Face_GazePitch']=d['NativePitch']
            for stage,mask in [('SHAPE_ONLY',[False,False]),('SHAPE_GN',[True,False]),('FULL_SOURCE',[True,True])]:
                for m,enabled in zip(head.modifiers,mask):m.show_viewport=m.show_render=enabled
                records.append(capture(tag+'_'+stage))
            key_readbacks[tag]={k.name:k.value for k in keys.key_blocks}
            named={m['name']:m['weight']/100 for m in d['original_morph_weights']}
            common=set(named)&set(key_readbacks[tag])
            morph_comparison[tag]={'compared_named_keys':len(common),
                'missing_source_keys':sorted(set(named)-set(key_readbacks[tag])),
                'max_abs_source_vs_consumer_weight100':max(abs(key_readbacks[tag][k]-named[k]) for k in common),
                'scope':'Diagnostic readback; no tolerance waiver or forced source corrective weights'}
    finally:
        for name,v in saved.items():keys.key_blocks[name].value=v
        for name,v in gaze.items():head[name]=v
        for m,(v,r) in zip(head.modifiers,flags):m.show_viewport=v;m.show_render=r
        head.update_tag();keys.update_tag();scene.frame_set(1);bpy.context.view_layer.update()
    after=capture('OFF_after');diff=difference(before,snapshot(actions));assert not diff,diff
    with np.load(out/baseline['file']) as a,np.load(out/after['file']) as b:
        assert a.files==b.files and all(np.array_equal(a[k],b[k]) for k in a.files)
    assert muted==[(d.data_path,d.mute) for d in keys.animation_data.drivers if d.mute]
    assert sha(master)==sha(clone)==SOURCE_SHA
    assert all(sha(inputs/(tag+'_source_inputs_PRIVATE_R1.json'))==v for tag,v in INPUT_SHA.items())
    report={'scope':'two FACE16/GAZE2 fixed inputs, head only, original body/Armature OFF/rest; no timeline reconstruction',
            'source_sha256':SOURCE_SHA,'input_sha256':INPUT_SHA,'records':records,'OFF_records':[baseline,after],
            'Key_readback_PRIVATE':key_readbacks,'morph_weight_diagnostic':morph_comparison,'OFF_full_component_diff':diff,
            'no_render_export_save_Unity':True,'native_guard_status':'PENDING_EXTERNAL_STRICT_AFTER_AND_TERMINAL_AUDIT'}
    (out/'TWO_INPUT_NATIVE_RESULT_PRIVATE_R1.json').write_text(json.dumps(report,indent=2))

if __name__=='__main__':main()
