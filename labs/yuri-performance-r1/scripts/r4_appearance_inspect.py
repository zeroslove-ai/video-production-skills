import bpy,json
from pathlib import Path
p=Path(r'C:/Users/JAEWAN/projects/yuri-motion-previs-lab-r1/labs/yuri-performance-r1/local/model-handoff-r4/Character_Master_NeckSkin_R4.blend')
bpy.ops.wm.open_mainfile(filepath=str(p),use_scripts=False)
s=bpy.context.scene
print('SOURCE_INSPECT',json.dumps({'frame':s.frame_current,'range':[s.frame_start,s.frame_end],'render':[s.render.engine,s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage],'camera':s.camera.name if s.camera else None,'camera_data':{'type':s.camera.data.type,'lens':s.camera.data.lens,'ortho_scale':s.camera.data.ortho_scale},'rigs':{o.name:{'mode':sorted(set(b.rotation_mode for b in o.pose.bones)),'action':o.animation_data.action.name if o.animation_data and o.animation_data.action else None,'nla':[(t.name,t.mute) for t in o.animation_data.nla_tracks] if o.animation_data else [],'nonidentity_pose':[b.name for b in o.pose.bones if any(abs(v)>1e-7 for v in b.location) or b.rotation_quaternion.angle>1e-7 or any(abs(v)>1e-7 for v in b.rotation_euler)]} for o in bpy.data.objects if o.type=='ARMATURE'},'actions':len(bpy.data.actions),'scene_names':[s.name for s in bpy.data.scenes]},indent=2))
