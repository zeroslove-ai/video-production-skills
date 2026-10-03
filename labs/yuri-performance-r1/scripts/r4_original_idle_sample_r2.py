"""Prepared original four-lane sampler. Requires exact external owned-Job receipt."""
from pathlib import Path
import array, gzip, hashlib, json, sys, time, traceback
import bpy
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference,props,val,digest
from r4_installed_addon_origin_gate_r2 import inspect_and_require
LAB=HERE.parent
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-original-idle-sampling-r2'
E=LAB/'evidence/o1-original-idle-sampling-preparation-r2'
SOURCE=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
SCOPE='ORIGINAL_IDLE_EXPLICIT_FOUR_QA_BINDING_145_FRAME_SAMPLING'
CHANNELS=('location','rotation_quaternion','rotation_euler','rotation_axis_angle','scale')

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def write(n,v):
    with (OUT/n).open('x',encoding='utf8') as f:json.dump(v,f,indent=2)

def matrix(m):return [list(r) for r in m]

def scalar(owner,path,index):
    v=owner.path_resolve(path)
    try:return float(v[index])
    except TypeError:
        assert index==0
        return float(v)

def curves(a,slot):
    found=[]
    for layer in a.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                assert bag.slot_handle in {s.handle for s in a.slots}
                if bag.slot_handle==slot.handle:found.extend(bag.fcurves)
    return found

def channel_state(o):return {k:list(getattr(o,k)) for k in CHANNELS}

def restore_channels(o,state):
    for k,v in state.items():setattr(o,k,v)

def structural_graph(owners):
    def strip(s):return {'RNA':props(s),'children':[strip(c) for c in s.strips] if s.type=='META' else []}
    result=[]
    for o in owners:
        ad=o.animation_data
        result.append({'owner':o.name,'type':o.bl_rna.identifier,'use_nla':ad.use_nla if ad else None,'nla':[{'RNA':props(t),'strips':[strip(s) for s in t.strips]} for t in ad.nla_tracks] if ad else [],'drivers':[{'path':f.data_path,'index':f.array_index,'mute':f.mute,'expression':f.driver.expression,'type':f.driver.type,'variables':[{'RNA':props(v),'targets':[props(t) for t in v.targets]} for v in f.driver.variables]} for f in ad.drivers] if ad else []})
    return result

def driver_records(owners,deps):
    result=[]
    for owner in owners:
        ad=owner.animation_data
        if not ad:continue
        evaluated=owner.evaluated_get(deps)
        for fc in ad.drivers:
            variables=[]
            for var in fc.driver.variables:
                variables.append({'name':var.name,'type':var.type,'targets':[props(t) for t in var.targets]})
            result.append({'owner_type':owner.bl_rna.identifier,'owner':owner.name,'path':fc.data_path,'index':fc.array_index,'mute':fc.mute,'is_valid':fc.is_valid,'driver_is_valid':fc.driver.is_valid,'expression':fc.driver.expression,'variables':variables,'original_RNA':scalar(owner,fc.data_path,fc.array_index),'evaluated_RNA':scalar(evaluated,fc.data_path,fc.array_index)})
    return result

def main():
    proposal=json.loads((E/'SAMPLING_PROPOSAL_R2.json').read_bytes())
    review=json.loads((OUT/'PM_APPROVAL_ORIGINAL_IDLE_SAMPLE_R2.json').read_bytes())
    assert review['scope']==SCOPE and review['approved'] and review['reviewed_owned_job_terminal_behavior']
    assert review['proposal_sha256']==sha(E/'SAMPLING_PROPOSAL_R2.json') and review['collector_sha256']==sha(__file__) and review['argv']==proposal['argv']
    assert review['max_attempts']==1 and not review['custom_native_build_trace_capture_approved'] and not review['large_resource_acquisition_approved']
    assert bpy.app.background and bpy.app.build_hash.decode()=='9e2066aef7ef'
    assert Path(bpy.data.filepath).resolve()==SOURCE.resolve() and sha(SOURCE)==proposal['source_sha256']
    assert all(sha(p)==r['sha256'] for p,r in proposal['inputs'].items())
    assert not (OUT/'IDLE_SAMPLING_RESULT_R2.json').exists()
    scene=bpy.context.scene
    assert scene.render.fps==24 and scene.render.fps_base==1
    origin_manifest=LAB/'evidence/o1-exact-local-stage-factory-addon-preparation-r2/INSTALLED_BUNDLED_ADDON_ORIGIN_MANIFEST_R2.json'
    origin_before=inspect_and_require(bpy,origin_manifest,OUT,'before')
    actions=[a.name for a in bpy.data.actions]
    owners=list(bpy.data.objects)+list(bpy.data.shape_keys)
    rigs=[o for o in bpy.data.objects if o.type=='ARMATURE']
    assert len(actions)==78 and len(rigs)==4 and sum(len(o.data.bones) for o in rigs)==137
    assert len(bpy.data.shape_keys['FaceControls_TEST_Jaw_Smile.001'].key_blocks)==72
    assert bpy.data.objects['Character_Body_Head'].data.shape_keys==bpy.data.shape_keys['FaceControls_TEST_Jaw_Smile.001']
    muted=[(o.name,f.data_path,f.array_index) for o in owners if o.animation_data for f in o.animation_data.drivers if f.mute]
    assert len(muted)==13
    before=snapshot(actions)
    structural_before=structural_graph(owners)
    write('ORIGINAL_BINDING_KEY_INPUTS_PRIVATE_R1.json',{'bindings':[{'owner':o.name,'type':o.bl_rna.identifier,'animation_data':props(o.animation_data) if o.animation_data else None} for o in owners],'structure':structural_before,'Keys':[{'Key':k.name,'blocks':[{'name':b.name,'saved_value':b.value,'slider_min':b.slider_min,'slider_max':b.slider_max,'RNA':props(b)} for b in k.key_blocks]} for k in bpy.data.shape_keys]})
    saved_frame=(scene.frame_current,scene.frame_subframe)
    object_state=[(o,channel_state(o)) for o in bpy.data.objects]
    pose_state=[(b,channel_state(b)) for o in rigs for b in o.pose.bones]
    key_state=[(k,k.value) for owner in bpy.data.shape_keys for k in owner.key_blocks]
    resolved=[]
    for row in proposal['bindings']:
        target=bpy.data.shape_keys[row['target_name']] if row['target_id_type']=='KEY' else bpy.data.objects[row['target_name']]
        action=bpy.data.actions[row['exact_Action']]
        slot=next(s for s in action.slots if s.handle==row['slot_handle'] and s.identifier==row['slot_identifier'])
        assert slot.target_id_type==row['target_id_type'] and before['actions'][action.name]==row['curve_fingerprint']
        fc=curves(action,slot)
        assert len(fc)==row['curve_count']
        touched=[(c.data_path,c.array_index,scalar(target,c.data_path,c.array_index)) for c in fc]
        ad=target.animation_data
        resolved.append({'target':target,'action':action,'slot':slot,'curves':fc,'touched':touched,'had_ad':ad is not None,'original_action':ad.action if ad else None,'original_slot':ad.action_slot if ad else None})
    # Store complete modifier RNA, including CYCLES modes/offset before evaluation.
    original_curves=[{'Action':r['action'].name,'slot_handle':r['slot'].handle,'curves':[{'path':f.data_path,'index':f.array_index,'mute':f.mute,'group':props(f.group) if f.group else None,'RNA':props(f),'modifiers':[props(m) for m in f.modifiers],'keys':[[*k.co,*k.handle_left,*k.handle_right,k.interpolation,k.handle_left_type,k.handle_right_type] for k in f.keyframe_points]} for f in r['curves']]} for r in resolved]
    source_properties=[]
    for r in resolved:
        for path,index,value in r['touched']:
            if path.startswith('["'):
                name=path[2:-2]
                source_properties.append({'owner':r['target'].name,'property':name,'saved_value':value,'UI_metadata':val(r['target'].id_properties_ui(name).as_dict()),'units':'SOURCE_UI_METADATA_IF_PRESENT_ELSE_UNKNOWN; NO_NORMALIZATION_OR_CLAMP'})
    write('ORIGINAL_PROPERTY_AND_REST_METADATA_PRIVATE_R1.json',{'properties':source_properties,'rigs':[{'object':o.name,'parent':o.parent.name if o.parent else None,'matrix_world':matrix(o.matrix_world),'matrix_parent_inverse':matrix(o.matrix_parent_inverse),'bones':[{'name':b.name,'parent':b.parent.name if b.parent else None,'matrix_local':matrix(b.matrix_local),'use_deform':b.use_deform} for b in o.data.bones]} for o in rigs]})
    write('ORIGINAL_CURVES_AND_MODIFIERS_PRIVATE_R1.json',original_curves)
    modifier_fingerprint=digest([[props(m) for m in f.modifiers] for r in resolved for f in r['curves']])
    write('ORIGINAL_DRIVER_GRAPH_PRIVATE_R1.json',driver_records(owners,bpy.context.evaluated_depsgraph_get()))
    mesh_objects=[o for o in bpy.data.objects if o.type=='MESH']
    write('MESH_TOPOLOGY_PRIVATE_R1.json',[{'object':o.name,'materials':[s.name for s in o.material_slots],'polygon_vertices':[list(p.vertices) for p in o.data.polygons],'source_vertices':len(o.data.vertices)} for o in mesh_objects])
    records=[];offset=0;error=None;start=time.monotonic()
    try:
        for r in resolved:
            ad=r['target'].animation_data_create()
            ad.action=r['action'];ad.action_slot=r['slot']
            assert ad.action==r['action'] and ad.action_slot_handle==r['slot'].handle
        on_snapshot=snapshot(actions)
        write('ON_SOURCE_SIGNATURE_R1.json',on_snapshot)
        structural_on=structural_graph(owners)
        write('STRUCTURAL_OFF_ON_OFF_R1.json',{'before':structural_before,'on':structural_on,'same_before_on':structural_before==structural_on})
        assert structural_before==structural_on,'Driver/NLA structure changed'
        for category in ['meshes_shape_keys_weights','rest_rigs','actions','rest_pose_settings','materials','node_groups','textures','worlds']:
            assert on_snapshot[category]==before[category],('ON invariant',category)
        with gzip.open(OUT/'FRAMES_PRIVATE_R1.jsonl.gz','xb',compresslevel=1) as jf, gzip.open(OUT/'ALL_MESH_NATIVE_LOCAL_F32_PRIVATE_R1.bin.gz','xb',compresslevel=1) as gf:
            for frame in range(1,146):
                scene.frame_set(frame,subframe=0);bpy.context.view_layer.update()
                deps=bpy.context.evaluated_depsgraph_get()
                domains=[]
                for r in resolved:
                    evaluated=r['target'].evaluated_get(deps)
                    domains.append({'Action':r['action'].name,'target':r['target'].name,'slot_handle':r['slot'].handle,'channels':[{'path':f.data_path,'index':f.array_index,'mute':f.mute,'is_valid':f.is_valid,'native_FCurve_evaluate':float(f.evaluate(frame)),'original_RNA':scalar(r['target'],f.data_path,f.array_index),'evaluated_RNA':scalar(evaluated,f.data_path,f.array_index)} for f in r['curves']]})
                rig_rows=[]
                for o in rigs:
                    ev=o.evaluated_get(deps)
                    rig_rows.append({'object':o.name,'matrix_world':matrix(ev.matrix_world),'bones':[{'name':b.name,'matrix':matrix(b.matrix),'matrix_basis':matrix(b.matrix_basis),'head':list(b.head),'tail':list(b.tail),'quaternion_wxyz':list(b.rotation_quaternion)} for b in ev.pose.bones]})
                keys=[{'Key':k.name,'values':[[b.name,b.value] for b in k.evaluated_get(deps).key_blocks]} for k in bpy.data.shape_keys]
                geometry=[]
                for o in mesh_objects:
                    ev=o.evaluated_get(deps);mesh=ev.to_mesh()
                    try:
                        buf=array.array('f',[0])*(len(mesh.vertices)*3)
                        mesh.vertices.foreach_get('co',buf)
                        assert buf.itemsize==4 and sys.byteorder=='little'
                        data=buf.tobytes();gf.write(data)
                        loops=array.array('i',[0])*len(mesh.loops)
                        starts=array.array('i',[0])*len(mesh.polygons)
                        totals=array.array('i',[0])*len(mesh.polygons)
                        mesh.loops.foreach_get('vertex_index',loops)
                        mesh.polygons.foreach_get('loop_start',starts)
                        mesh.polygons.foreach_get('loop_total',totals)
                        geometry.append({'object':o.name,'vertices':len(mesh.vertices),'offset_uncompressed_bytes':offset,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'matrix_world':matrix(ev.matrix_world),'native_evaluated_topology_sha256':hashlib.sha256(loops.tobytes()+starts.tobytes()+totals.tobytes()).hexdigest()})
                        offset+=len(data)
                    finally:ev.to_mesh_clear()
                row={'frame':frame,'time_seconds':(frame-1)/24,'domains':domains,'rigs':rig_rows,'Keys':keys,'drivers':driver_records(owners,deps),'object_transforms':[{'object':o.name,'type':o.type,'matrix_world':matrix(o.evaluated_get(deps).matrix_world)} for o in bpy.data.objects],'geometry':geometry}
                jf.write((json.dumps(row,separators=(',',':'))+'\n').encode())
                # All channels retained for endpoint/velocity measurements; no threshold filtering.
                records.append([v for d in domains for c in d['channels'] for v in (c['native_FCurve_evaluate'],c['evaluated_RNA'])]+[v for r in rig_rows for b in r['bones'] for v in b['head']])
                if frame%24==1:print('ORIGINAL_IDLE_FRAME',frame,flush=True)
    except BaseException:
        error=traceback.format_exc()
    finally:
        for r in resolved:
            ad=r['target'].animation_data
            ad.action=r['original_action']
            if r['original_action'] is not None:ad.action_slot=r['original_slot']
            for path,index,value in r['touched']:
                if path.startswith('["'):
                    r['target'][path[2:-2]]=value
            if not r['had_ad']:r['target'].animation_data_clear()
        for o,state in object_state:restore_channels(o,state)
        for b,state in pose_state:restore_channels(b,state)
        for k,value in key_state:k.value=value
        scene.frame_set(saved_frame[0],subframe=saved_frame[1]);bpy.context.view_layer.update()
        after=snapshot(actions)
        diff=difference(before,after)
        write('SCENE_SIGNATURE_BEFORE_AFTER.json',{'before':before,'after':after,'differences':diff})
        origin_after=inspect_and_require(bpy,origin_manifest,OUT,'after')
        assert origin_before['preferences_module_names']==origin_after['preferences_module_names'] and origin_before['loaded_enabled_module_names']==origin_after['loaded_enabled_module_names']
        assert not diff,diff
        structural_after=structural_graph(owners)
        write('STRUCTURAL_RESTORED_R1.json',{'after':structural_after,'same_before_after':structural_before==structural_after})
        assert structural_before==structural_after,'Driver/NLA structure restore mismatch'
        assert modifier_fingerprint==digest([[props(m) for m in f.modifiers] for r in resolved for f in r['curves']])
        assert muted==[(o.name,f.data_path,f.array_index) for o in owners if o.animation_data for f in o.animation_data.drivers if f.mute]
        assert all(sha(p)==r['sha256'] for p,r in proposal['inputs'].items())
        if error:write('SAMPLING_ERROR_R1.json',{'error':error,'sample_count':len(records),'restored':True});raise RuntimeError(error)
    assert len(records)==145
    def delta(a,b):return [y-x for x,y in zip(a,b,strict=True)]
    measurements={'vector_order':'Action order, channel order: FCurve/evaluatedRNA alternating; then all137bone headxyz rig order','value_1_73':delta(records[0],records[72]),'value_73_145':delta(records[72],records[144]),'seam_73_74_step':delta(records[72],records[73]),'velocity_1_2':[v*24 for v in delta(records[0],records[1])],'velocity_72_73':[v*24 for v in delta(records[71],records[72])],'velocity_73_74':[v*24 for v in delta(records[72],records[73])],'velocity_144_145':[v*24 for v in delta(records[143],records[144])],'closure_verdict':'MEASUREMENTS_ONLY_NO_AUTOMATIC_LOOP_OR_VISUAL_PASS'}
    write('ENDPOINT_SEAM_MEASUREMENTS_PRIVATE_R1.json',measurements)
    write('IDLE_SAMPLING_RESULT_R2.json',{'status':'NATIVE_FOUR_DOMAIN_145_FRAME_CAPTURE_RESTORED_NOT_VISUAL_OR_PRODUCT_PASS','sample_count':145,'frames':[1,145],'fps':24,'fps_base':1,'original137bones':True,'original78Actions':True,'original13muted_bridges':muted,'original_scene_signature_differences':diff,'source_sha256':sha(SOURCE),'geometry_uncompressed_bytes':offset,'eye_evidence':'Every native evaluated mesh sampled losslessly; no separate eye ID found by cached mesh-name inventory. Material/topology plus complete Character_Body_Head geometry preserved for eye attribution; no guessed eye-only subset. Object transforms and driver variable targets recorded every frame.','static_or_overridden_channels':'Every channel retained, native FCurve values separate from evaluated RNA; muted/invalid flags retained','runtime_seconds':time.monotonic()-start,'exports_saves_aliases':0,'collector_manifest_scope':'CLOSED_COLLECTOR_PAYLOAD_ONLY; live fixed-capture.log excluded; final log and Job receipt custody deferred until owned terminal/drain/close','files':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in OUT.iterdir() if p.is_file() and p.name not in {'PM_APPROVAL_ORIGINAL_IDLE_SAMPLE_R2.json','fixed-capture.log','OWNED_JOB_RESULT_R1.json','TERMINAL_FILE_CUSTODY_R2.json','IDLE_SAMPLING_RESULT_R2.json'}}})

if __name__=='__main__':main()
