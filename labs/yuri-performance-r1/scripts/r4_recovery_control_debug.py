import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'),use_scripts=False)
board=bpy.data.objects['AVATAR_FaceBoard'];head=bpy.data.objects['Character_Body_Head'];b=board.pose.bones['Smile.L']
for enabled in (False,True):
    if enabled:board.hide_viewport=False;board.hide_set(False)
    b.location.y=.055;board.update_tag(refresh={'OBJECT','DATA','TIME'});bpy.context.scene.frame_set(2);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();eb=board.evaluated_get(deps).pose.bones['Smile.L'];eh=head.evaluated_get(deps)
    print('CONTROL_DEBUG',enabled,'autoexecfail',bpy.app.autoexec_fail,'original',list(b.location),'evaluated',list(eb.location),'matrix',list(eb.matrix.translation),'headkey',head.data.shape_keys.name,'values',head.data.shape_keys.key_blocks['Smile.L'].value,eh.data.shape_keys.key_blocks['Smile.L'].value,'valid',[(f.data_path,f.driver.is_valid) for f in head.data.shape_keys.animation_data.drivers if 'Smile.L' in f.data_path],flush=True)
