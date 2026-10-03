"""Owned-background capture invocation proposal; import has zero bpy side effects.
Source binding is implemented in R5; compiled module unavailable. No CLI execute.
"""
from pathlib import Path
import struct
from armature_canonical_validate_r4 import verify_arming_inputs,require,CASES,fbytes,sha

def invoke(bpy,native,files,row,approved_build):
    # This receipt must be actual owner-reviewed build/capture custody, not a template.
    require(approved_build.get('actual_owner_capture_approval') is True,'capture approval not granted')
    require(bpy.app.background,'owned background process only')
    executable=Path(bpy.app.binary_path).resolve()
    require(executable.is_relative_to(Path('C:/YuriTransfer/native-cycles-readback-r1').resolve()),'installed/GUI executable prohibited')
    require(sha(executable)==approved_build['executable_sha256'],'compiled executable changed')
    require(approved_build['patch_sha256']=='b2ba72354e36d96f87ef98f7f7c2b1dba39a95338bff2a91f4cdeb48d64989e2','wrong source patch')
    require(approved_build.get('per_TU_compiler_flags_verified') is True,'compiler/backend custody missing')
    require(native.build_info()['binding']=='YURI_ARMATURE_TRACE_R5','wrong built-in binding')
    require(sha(approved_build['compiler_custody_file'])==approved_build['compiler_custody_sha256'],'actual compiler custody file missing/changed')
    # Mandatory bridge operations; no installed ctypes/ABI fallback.
    for name in ('begin','evaluate_and_join','cancel_and_join','finish'):
        require(callable(getattr(native,name,None)),'unimplemented owned native bridge: '+name)
    action,frame=CASES[row] if row in (0,1) else (None,None)
    gate=verify_arming_inputs(files,row,action,frame,'Meshy_Fitted_Rig','Meshy_Body_NeutralCovered')
    # No file/output/scene mutation has happened above this line.
    bpy.ops.wm.open_mainfile(filepath=str(files['source']),use_scripts=False)
    rig=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered']
    require(len(body.data.vertices)==63561,'wrong body cardinality')
    require([b.name for b in rig.data.bones]==gate['request']['bone_names'],'original57 order')
    from armature_live_recipe_r5 import verify_live_recipe
    original_recipe=verify_live_recipe(bpy,files['recipe']) # AFTER actual source load, BEFORE Action/arming.
    import sys
    scripts=Path(__file__).resolve().parents[1]
    sys.path.insert(0,str(scripts))
    from r4_appearance_adapter import ReactionLane
    from r4_appearance_signature import snapshot,difference
    original_actions=[a.name for a in bpy.data.actions];before=snapshot(original_actions)
    with bpy.data.libraries.load(str(files['actions']),link=False) as (src,dst):
        require(action in src.actions,'actual library Action missing');dst.actions=[action]
    require(not difference(before,snapshot(original_actions)),'append changed immutable source components')
    lane=ReactionLane();begun=False;joined=True;finish_ok=None
    try:
        a=lane.on(action);bpy.context.scene.frame_set(frame);bpy.context.view_layer.update()
        ad=rig.animation_data
        require(ad.action is a and a.name==action,'actual live Action mismatch')
        require(ad.action_slot.identifier=='OBMeshy_Fitted_Rig','actual live Action slot mismatch')
        require(bpy.context.scene.frame_current==frame and bpy.context.scene.frame_subframe==0.,'actual live source frame mismatch')
        require(not any(t.mute is False for t in ad.nla_tracks),'mixed active NLA track')
        for index,bone in enumerate(gate['request']['bone_names']):
            actual=[rig.pose.bones[bone].matrix[r][c] for r in range(4) for c in range(4)]
            require(fbytes(actual)==fbytes(gate['request']['pose_inputs'][row]['B_source_exact_pose'][index]),'live native B pose mismatch')
        # Validate actual original ordered five CSR rows including zero/helpers.
        for sample in gate['request']['selected_vertices']:
            v=body.data.vertices[sample['source_vertex']]
            require(fbytes(list(v.co))==fbytes(sample['original_position']),'original vertex coordinate drift')
            groups=list(v.groups);require(len(groups)==len(sample['ordered_CSR']),'original CSR cardinality drift')
            for g,e in zip(groups,sample['ordered_CSR']):
                require(g.group==e['group_index'] and fbytes([g.weight])==fbytes([e['weight']]),'original ordered CSR drift')
        identities=gate['file_sha256']
        begun=native.begin(row,a.name,float(frame),rig.name,body.name,identities['source'],identities['actions'],identities['pose'],identities['recipe'],identities['request'])
        require(begun is True,'native arming rejected; no output accepted')
        joined=False
        # Bridge MUST dirty/re-evaluate intended pose + ordinary modifier only,
        # block until all workers join, reject duplicated evaluation/crazyspace.
        joined=native.evaluate_and_join(row) is True
        require(joined,'native evaluation did not join')
    finally:
        if begun:
            if not joined:joined=native.cancel_and_join() is True
            require(joined,'owned supervisor must terminate failed child; no restoration concurrent with workers')
            finish_ok=native.finish()
        if joined:
            lane.off()
            require(not difference(before,snapshot(original_actions)),'original Action/slot/frame/pose/components restore failed')
            require(sha(files['source'])==identities['source'] if begun else sha(files['source'])==gate['file_sha256']['source'],'source file changed')
            require(sha(files['actions'])==gate['file_sha256']['actions'],'Action library changed')
    require(finish_ok is True,'native failure/flush/close rejected')
    return {'status':'CAPTURE_BYTES_WRITTEN_PENDING_SEPARATE_CANONICAL_VALIDATOR','joined_workers':joined,'source_action_restore':'VERIFIED','original_full_recipe':original_recipe,'installed_equivalence':False}

if __name__=='__main__':
    print('DRY_ONLY: no bpy import/Blender launch; native bridge, recipe and actual build/capture approval required')
