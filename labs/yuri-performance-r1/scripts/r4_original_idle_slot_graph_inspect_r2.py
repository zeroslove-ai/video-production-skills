"""PREPARED read-only graph inspection. No Action assignment/frame sampling/export.

Native invocation requires an exact new external PM receipt and owned Job route.
"""
from pathlib import Path
import hashlib,json,sys
import bpy

HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference,props,anim,digest
from r4_installed_addon_origin_gate_r2 import inspect_and_require
LAB=HERE.parent
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'o1-original-idle-slot-graph-inspection-r2'
E=LAB/'evidence/o1-original-idle-slot-graph-preparation-r2'
SOURCE=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
NAMES=[f'MESHY_R2_{lane}_Idle' for lane in ['BODY','FACE','GAZE','HAIR']]

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def write(n,v):
    with (OUT/n).open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
def identity(o):return {'ID_name':o.name,'RNA_ID_type':o.bl_rna.identifier,'library':o.library.filepath if o.library else None}

def binding(o):
    ad=getattr(o,'animation_data',None)
    if not ad:return None
    slots=ad.action_slot
    result={'action':ad.action.name if ad.action else None,'slot_identifier':slots.identifier if slots else None,'slot_handle':ad.action_slot_handle,'use_nla':ad.use_nla,'nla':[]}
    def strip_info(strip):
        slot=getattr(strip,'action_slot',None);action=getattr(strip,'action',None)
        result={'name':strip.name,'type':strip.type,'action':action.name if action else None,'slot_identifier':slot.identifier if slot else None,'slot_handle':getattr(strip,'action_slot_handle',None),'mute':getattr(strip,'mute',None),'blend_type':getattr(strip,'blend_type',None),'influence':getattr(strip,'influence',None),'frame_start':strip.frame_start,'frame_end':strip.frame_end,'action_frame_start':getattr(strip,'action_frame_start',None),'action_frame_end':getattr(strip,'action_frame_end',None)}
        if strip.type=='META':result['children']=[strip_info(s) for s in strip.strips]
        return result
    for track in ad.nla_tracks:result['nla'].append({'name':track.name,'mute':track.mute,'solo':track.is_solo,'strips':[strip_info(s) for s in track.strips]})
    return result

def main():
    proposal=json.loads((E/'INSPECTION_PROPOSAL_R2.json').read_bytes())
    review=json.loads((OUT/'PM_APPROVAL_ORIGINAL_IDLE_GRAPH_R2.json').read_bytes())
    assert review['scope']=='ORIGINAL_LIVING_IDLE_SLOT_GRAPH_READ_ONLY' and review['approved'] is True
    assert review['proposal_sha256']==sha(E/'INSPECTION_PROPOSAL_R2.json') and review['collector_sha256']==sha(__file__) and review['argv']==proposal['argv']
    assert review['reviewed_owned_job_terminal_behavior'] is True
    assert review['custom_native_build_trace_capture_approved'] is False and review['large_resource_acquisition_approved'] is False
    assert bpy.app.background and bpy.app.build_hash.decode()=='9e2066aef7ef'
    assert Path(bpy.data.filepath).resolve()==SOURCE.resolve() and sha(SOURCE)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa'
    assert not (OUT/'IDLE_SLOT_GRAPH_RESULT_R1.json').exists()
    assert all(sha(p)==r['sha256'] for p,r in proposal['inputs'].items())
    manifest=LAB/'evidence/o1-exact-local-stage-factory-addon-preparation-r2/INSTALLED_BUNDLED_ADDON_ORIGIN_MANIFEST_R2.json'
    origin_before=inspect_and_require(bpy,manifest,OUT,'before')
    all_actions=[a.name for a in bpy.data.actions];assert len(all_actions)==78
    before=snapshot(all_actions)
    objects=list(bpy.data.objects);keys=list(bpy.data.shape_keys)
    # Read references directly. RNA-path compatibility is a candidate relation,
    # not authoring intent; no guessed candidate is assigned to animation_data.
    owner_rows=[]
    for owner in objects+keys:
        row={'ID':identity(owner),'binding':binding(owner)}
        if isinstance(owner,bpy.types.Object):row.update(object_type=owner.type,parent=owner.parent.name if owner.parent else None)
        else:row['mesh_owner_Object_IDs']=[o.name for o in objects if o.type=='MESH' and o.data.shape_keys==owner]
        owner_rows.append(row)
    actions=[]
    for name in NAMES:
        a=bpy.data.actions[name];slots=[]
        for slot in a.slots:
            bags=[];curves=[];unresolved_bags=0;missing_apis=[];matched_bags=0
            known_handles={s.handle for s in a.slots}
            for li,layer in enumerate(a.layers):
                for si,strip in enumerate(layer.strips):
                    if not hasattr(strip,'channelbags'):
                        missing_apis.append({'layer':li,'strip':si,'reason':'MISSING_CHANNELBAGS_API'});continue
                    for bi,bag in enumerate(strip.channelbags):
                        handle=getattr(bag,'slot_handle',None)
                        if handle is None or handle not in known_handles:
                            unresolved_bags+=1
                            bags.append({'layer':li,'strip':si,'bag':bi,'slot_handle':'UNKNOWN_API_FIELD' if handle is None else handle,'cannot_attribute_curves':True,'reason':'UNKNOWN_HANDLE_OR_ORPHAN_BAG'});continue
                        if handle!=slot.handle:continue
                        matched_bags+=1
                        if not hasattr(bag,'fcurves'):
                            missing_apis.append({'layer':li,'strip':si,'bag':bi,'reason':'MISSING_FCURVES_API'});continue
                        paths=[]
                        for fc in bag.fcurves:
                            record={'RNA_path':fc.data_path,'array_index':fc.array_index,'mute':fc.mute,'keyframe_count':len(fc.keyframe_points),'sampled_point_count':len(fc.sampled_points),'modifiers':[[m.type,m.mute] for m in fc.modifiers],'original_curve_fingerprint':digest([[*k.co,*k.handle_left,*k.handle_right,k.interpolation] for k in fc.keyframe_points])}
                            curves.append(record);paths.append(record)
                        bags.append({'layer':li,'strip':si,'bag':bi,'slot_handle':handle,'fcurves':paths})
            complete_attribution=(unresolved_bags==0 and not missing_apis and matched_bags>0 and len(curves)>0)
            incomplete_reasons=[]
            if unresolved_bags:incomplete_reasons.append('UNRESOLVED_CHANNELBAG_HANDLES')
            if missing_apis:incomplete_reasons.append('MISSING_CHANNELBAG_OR_FCURVE_API')
            if matched_bags==0:incomplete_reasons.append('NO_MATCHED_CHANNELBAGS')
            if not curves:incomplete_reasons.append('NO_ATTRIBUTED_CURVES')
            candidates=[]
            target_ids=keys if slot.target_id_type=='KEY' else objects if slot.target_id_type=='OBJECT' else []
            for target in target_ids:
                failures=[]
                for curve in curves:
                    try:
                        value=target.path_resolve(curve['RNA_path'])
                        try:length=len(value)
                        except TypeError:length=1
                        if curve['array_index']<0 or curve['array_index']>=length:failures.append({'path':curve['RNA_path'],'index':curve['array_index'],'reason':'array component unavailable'})
                    except (ValueError,AttributeError,KeyError,TypeError) as error:failures.append({'path':curve['RNA_path'],'reason':repr(error)})
                candidates.append({'target':identity(target),'compatible_all_recorded_RNA_paths':bool(curves) and not failures,'complete_original_curve_attribution':complete_attribution,'compatible_all_original_curves':(not failures) if complete_attribution else None,'compatibility_status':('COMPATIBLE_COMPLETE_ENUMERATED_CURVES' if not failures else 'INCOMPATIBLE_COMPLETE_ENUMERATED_CURVES') if complete_attribution else 'UNKNOWN_INCOMPLETE_GRAPH','curves_checked':len(curves),'failed_paths':failures,'mesh_owner_Object_IDs':[o.name for o in objects if o.type=='MESH' and o.data.shape_keys==target] if slot.target_id_type=='KEY' else None})
            slots.append({'identifier':slot.identifier,'target_id_type':slot.target_id_type,'actual_handle':slot.handle,'channelbags':bags,'matched_channelbag_count':matched_bags,'attributed_curve_count':len(curves),'unresolved_bag_count':unresolved_bags,'missing_API_records':missing_apis,'complete_original_curve_attribution':complete_attribution,'graph_completeness_status':'COMPLETE_ENUMERATED_CURVE_GRAPH' if complete_attribution else 'UNKNOWN_INCOMPLETE_GRAPH','incomplete_reasons':incomplete_reasons,'candidate_compatibility':candidates,'intended_owner':'NOT_SELECTED; require actual binding/user reference or separate authoring authority; compatibility alone insufficient'})
        references=[]
        for owner in objects+keys:
            ad=getattr(owner,'animation_data',None)
            if ad and ad.action==a:references.append({'owner':identity(owner),'reference':'DIRECT_ACTION','binding':binding(owner)})
            if ad:
                def visit(strips,track):
                    for strip in strips:
                        if getattr(strip,'action',None)==a:references.append({'owner':identity(owner),'reference':'NLA_STRIP','track':track.name,'track_mute':track.mute,'strip':strip.name,'strip_mute':getattr(strip,'mute',None),'slot_handle':getattr(strip,'action_slot_handle',None)})
                        if strip.type=='META':visit(strip.strips,track)
                for track in ad.nla_tracks:visit(track.strips,track)
        actions.append({'exact_Action':name,'frame_range':list(a.frame_range),'curve_fingerprint':before['actions'][name],'slots':slots,'complete_original_curve_attribution':bool(slots) and all(s['complete_original_curve_attribution'] for s in slots),'graph_completeness_status':'COMPLETE_ENUMERATED_CURVE_GRAPH' if slots and all(s['complete_original_curve_attribution'] for s in slots) else 'UNKNOWN_INCOMPLETE_GRAPH','actual_owner_references':references,'target_intent_acceptance':'PENDING_MANUAL_REVIEW; no activation performed'})
    rigs=[{'Object_ID':o.name,'parent':o.parent.name if o.parent else None,'bones':len(o.data.bones),'ordered_bone_names':[b.name for b in o.data.bones],'rest_fingerprint':before['rest_pose_settings'][o.name],'binding':binding(o),'driver_graph':anim(o)} for o in objects if o.type=='ARMATURE']
    assert len(rigs)==4 and sum(r['bones'] for r in rigs)==137
    muted=[]
    for owner in objects+keys:
        ad=getattr(owner,'animation_data',None)
        if ad:
            muted.extend({'owner_ID':identity(owner),'RNA_path':f.data_path,'array_index':f.array_index,'expression':f.driver.expression} for f in ad.drivers if f.mute)
    assert len(muted)==13
    origin_after=inspect_and_require(bpy,manifest,OUT,'after')
    assert origin_before['preferences_module_names']==origin_after['preferences_module_names'] and origin_before['loaded_enabled_module_names']==origin_after['loaded_enabled_module_names']
    after=snapshot(all_actions);diff=difference(before,after);assert not diff,diff
    assert all(sha(p)==r['sha256'] for p,r in proposal['inputs'].items())
    write('SCENE_SIGNATURE_BEFORE_AFTER.json',{'before':before,'after':after,'differences':diff})
    scene=bpy.context.scene
    all_complete=all(a['complete_original_curve_attribution'] for a in actions)
    write('IDLE_SLOT_GRAPH_RESULT_R1.json',{'status':'ORIGINAL_IDLE_GRAPH_READ_ONLY_NOT_TARGET_ASSIGNMENT_OR_PLAYBACK_PASS' if all_complete else 'UNKNOWN_INCOMPLETE_GRAPH','graph_completeness_status':'COMPLETE_ENUMERATED_CURVE_GRAPH' if all_complete else 'UNKNOWN_INCOMPLETE_GRAPH','all_original_curves_attributed':all_complete,'source_pre_post_sha256':sha(SOURCE),'original137bones':True,'original78Actions':True,'original13muted_bridges':muted,'original_scene_signature_differences':diff,'fps':scene.render.fps,'fps_base':scene.render.fps_base,'effective_fps':scene.render.fps/scene.render.fps_base,'frame_current':scene.frame_current,'scene_range':[scene.frame_start,scene.frame_end],'Actions':actions,'original_rigs':rigs,'Object_Key_owner_binding_graph':owner_rows,'endpoint_playback':'NOT_RUN','exports_activations_saves':0,'input_hashes':proposal['inputs'],'data_rule':'Existing binding references and compatibility results reported separately; ambiguous/unbound slots never auto-assigned. KEY curves are not rig poses.'})
    print('ORIGINAL_IDLE_GRAPH_INSPECTION_COMPLETE_NO_ACTIVATION',flush=True)

if __name__=='__main__':main()
