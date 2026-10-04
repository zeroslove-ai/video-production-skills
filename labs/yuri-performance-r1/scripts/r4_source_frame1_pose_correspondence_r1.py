"""Single frame1 actual STARTLED source pose/camera correspondence; no render/save/export."""
import bpy,sys,json,hashlib,numpy as np
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
REF=BASE/'r4-actual-startled-mouth-source-reference-r1/SOURCE_REFERENCE_PRIVATE_R1.json'
OUT=BASE/'r4-source-frame1-pose-correspondence-r1'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rows(m):return [list(r) for r in m]
def dump(p,v):
 with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
def main():
 assert not OUT.exists();ref=json.loads(REF.read_bytes());src=Path(ref['source']);assert sha(src)==ref['source_SHA256'];OUT.mkdir()
 bpy.ops.wm.open_mainfile(filepath=str(src),use_scripts=False);s=bpy.context.scene;assert s.frame_current==ref['source_frame']==1
 original=list(bpy.data.actions.keys());before=snapshot(original)
 head=bpy.data.objects['Character_Body_Head'];keys=head.data.shape_keys;saved=[k.value for k in keys.key_blocks];gaze=[head['Face_GazeYaw'],head['Face_GazePitch']]
 for n,v in ref['native_FACE16'].items():keys.key_blocks[n].value=v
 head['Face_GazeYaw'],head['Face_GazePitch']=ref['native_GAZE2'];head.update_tag();keys.update_tag();s.frame_set(1);bpy.context.view_layer.update()
 assert {k.name:k.value for k in keys.key_blocks}==ref['evaluated_key_readback'],'Expression differs from original image evaluation'
 deps=bpy.context.evaluated_depsgraph_get();rigs={}
 selected={'Meshy_Fitted_Rig':['root','pelvis','spine','chest','neck','head','clavicle.L','clavicle.R'],'Armature':['Root','J_Bip_C_Hips','J_Bip_C_Spine','J_Bip_C_Chest','J_Bip_C_UpperChest','J_Bip_C_Neck','J_Bip_C_Head'],'Hair_Rig_R4':['Hair_HeadRoot']}
 for name,bnames in selected.items():
  o=bpy.data.objects[name];e=o.evaluated_get(deps);bones={}
  for n in bnames:
   b=o.data.bones[n];p=o.pose.bones[n];ep=e.pose.bones[n];skin=ep.matrix@b.matrix_local.inverted()
   bones[n]={'parent':b.parent.name if b.parent else None,'rest_bone_to_armature':rows(b.matrix_local),'rest_bone_to_world':rows(o.matrix_world@b.matrix_local),'pose_bone_to_armature':rows(p.matrix),'evaluated_pose_bone_to_armature':rows(ep.matrix),'evaluated_pose_bone_to_world':rows(e.matrix_world@ep.matrix),'pose_basis_relative_to_parent_rest':rows(p.matrix_basis),'skin_rest_armature_to_posed_armature':rows(skin),'use_deform':b.use_deform,'constraints':[{'name':c.name,'type':c.type,'mute':c.mute,'influence':c.influence,'target':getattr(getattr(c,'target',None),'name',None),'subtarget':getattr(c,'subtarget',None)} for c in p.constraints]}
  ad=o.animation_data;rigs[name]={'object_to_world':rows(o.matrix_world),'evaluated_object_to_world':rows(e.matrix_world),'pose_position':o.data.pose_position,'bound_Action':ad.action.name if ad and ad.action else None,'bones':bones}
 objects={}
 for n in ['Assembly_Root','Character_Body_Head','Meshy_Body_NeutralCovered','Hair_Replacement_R4']:
  o=bpy.data.objects[n];e=o.evaluated_get(deps);objects[n]={'type':o.type,'parent':o.parent.name if o.parent else None,'parent_type':o.parent_type,'parent_bone':o.parent_bone,'object_to_world':rows(o.matrix_world),'evaluated_object_to_world':rows(e.matrix_world),'matrix_parent_inverse':rows(o.matrix_parent_inverse),'armature_modifiers':[{'name':m.name,'target':m.object.name if m.object else None,'show_viewport':m.show_viewport,'show_render':m.show_render,'use_vertex_groups':m.use_vertex_groups,'use_bone_envelopes':m.use_bone_envelopes,'use_deform_preserve_volume':m.use_deform_preserve_volume} for m in o.modifiers if m.type=='ARMATURE']}
 cam=s.camera;ec=cam.evaluated_get(deps);assert rows(cam.matrix_world)==ref['camera']['matrix_world'];r=s.render;assert [r.resolution_x,r.resolution_y,r.resolution_percentage]==ref['camera']['resolution']
 assert cam.data.type==ref['camera']['settings']['type'] and cam.data.ortho_scale==ref['camera']['settings']['ortho_scale']
 width=int(r.resolution_x*r.resolution_percentage/100);height=int(r.resolution_y*r.resolution_percentage/100)
 view=ec.matrix_world.normalized().inverted();proj=ec.calc_matrix_camera(deps,x=width,y=height,scale_x=r.pixel_aspect_x,scale_y=r.pixel_aspect_y)
 camera={'name':cam.name,'camera_to_world':rows(cam.matrix_world),'evaluated_camera_to_world':rows(ec.matrix_world),'world_to_camera_view':rows(view),'camera_to_clip_projection':rows(proj),'world_to_clip':rows(proj@view),'type':cam.data.type,'ortho_scale':cam.data.ortho_scale,'shift_xy':[cam.data.shift_x,cam.data.shift_y],'clip_near_far':[cam.data.clip_start,cam.data.clip_end],'sensor_fit':cam.data.sensor_fit,'resolution_native_xy_percentage':[r.resolution_x,r.resolution_y,r.resolution_percentage],'resolution_render_xy':[width,height],'pixel_aspect_xy':[r.pixel_aspect_x,r.pixel_aspect_y],'method':'Blender evaluated Camera.calc_matrix_camera native API; view uses normalized evaluated camera matrix inverse','NDC_to_top_left_pixel':'For c=P*V*[world.xyz,1], ndc=c.xyz/c.w; pixel x=(ndc.x+1)*width/2; pixel y=(1-ndc.y)*height/2. Pixel-center convention for discrete sampling is separate.'}
 result={'scope':'ONE_SOURCE_FRAME1_POSE_CORRESPONDENCE_ONLY','source_path':str(src),'source_SHA256':sha(src),'source_frame':1,'source_subframe':s.frame_subframe,'reference_receipt':str(REF),'reference_receipt_SHA256':sha(REF),'reference_image_SHA256':ref['image_SHA256'],'native_FACE16':ref['native_FACE16'],'native_GAZE2':ref['native_GAZE2'],'all72_key_readback_matches_reference_exact':True,'evaluation':'FULL_SOURCE original modifiers/drivers evaluated after FACE16+GAZE2 assignment; no body/head animation binding changed','coordinates':{'handedness':'Blender right handed','unit':'Blender scene length-unit settings recorded below; source geometry convention metres','up_axis':'+Z','character_forward':'Source avatar generally faces -Y','matrix_storage':'4x4 row-major nested rows; column-vector multiplication p_target=M@p_source; translation last column','bone_local_axis':'+Y along bone; armature-local rest matrix Bone.matrix_local','skin_matrix':'evaluated_pose_bone_to_armature @ inverse(rest_bone_to_armature); parent/rest contribution included in evaluated pose, not raw rotation copy','no_Unity_conversion_applied':True,'camera_basis':'Local +X right,+Y up,-Z optical forward; OpenGL-style clip/NDC returned by native Blender camera API'},'scene_units':{'system':s.unit_settings.system,'scale_length':s.unit_settings.scale_length,'length_unit':s.unit_settings.length_unit},'rigs':rigs,'objects':objects,'camera':camera,'runtime_witness_seconds':ref['runtime_witness_seconds'],'runtime_frame_body_camera_correspondence':'UNKNOWN; runtime Mouth98 label does not establish authored Blender frame98','parity':'NOT_DECLARED; consumer must map names/basis/units and compare actual import bind-rest and witness bone/camera matrices'}
 assert all(np.isfinite(np.array(v['object_to_world'])).all() for v in objects.values())
 for k,v in zip(keys.key_blocks,saved):k.value=v
 head['Face_GazeYaw'],head['Face_GazePitch']=gaze;head.update_tag();keys.update_tag();s.frame_set(1);bpy.context.view_layer.update();after=snapshot(original);diff=difference(before,after);assert not diff,diff;assert sha(src)==ref['source_SHA256']
 result['original_input_restore_signature_difference']=diff;result['source_bytes_unchanged']=True;result['no_render_save_export_product_change']=True
 dump(OUT/'SOURCE_FRAME1_POSE_CAMERA_PRIVATE_R1.json',result);print('ONE_SOURCE_FRAME1_CORRESPONDENCE_PASS',flush=True)
if __name__=='__main__':main()
