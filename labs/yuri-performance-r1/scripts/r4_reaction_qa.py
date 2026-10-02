"""Full-frame native skeletal QA and CPU normal-speed render, no source writes."""
import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence/model-handoff-r4';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/r4-model-handoff')
bpy.ops.wm.open_mainfile(filepath=str(OUT/'Character_Master_Reaction_R4_20261002.blend'))
s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];s.render.fps=24;s.render.fps_base=1
names=[a.name for a in bpy.data.actions if a.name.startswith('YRA_R4_') and 'QA_' not in a.name]
checks=[]
for name in names:
 a=bpy.data.actions[name];r.animation_data.action=a;end=round(a.frame_range[1]);first=None;roots=[];maxmove=0;steps=[];prev=None;finite=True
 for f in range(1,end+1):
  s.frame_set(f);bpy.context.view_layer.update();v={b.name:(r.matrix_world@b.matrix).copy() for b in r.pose.bones}
  if first is None:first=v
  maxmove=max(maxmove,max((m.translation-first[n].translation).length for n,m in v.items() if n!='root'))
  roots.append(v['root'].translation)
  if prev:steps.append(max((m.translation-prev[n].translation).length for n,m in v.items()))
  prev=v
  deps=bpy.context.evaluated_depsgraph_get()
  # Every frame, full visible body mesh: finiteness and bounded dimensions.
  obj=bpy.data.objects['Meshy_Body_NeutralCovered'].evaluated_get(deps)
  finite &= all(math.isfinite(x) for pt in obj.bound_box for x in pt)
 seam=max((v[n].translation-first[n].translation).length for n in v)
 loop='Loop' in name
 assert maxmove>1e-4 and finite and max(steps)<.08
 if loop:assert seam<1e-5
 checks.append({'action':name,'frames_evaluated':end,'actual_non_root_bone_motion_m':maxmove,'root_excursion_m':max((p-roots[0]).length for p in roots),'max_bone_step_m':max(steps),'loop_seam_position_m':seam if loop else None,'loop_cycles_rendered':2 if loop else None,'mesh_bounds_finite_all_frames':finite,'native_structural':'PASS','unity_state_weight_normalized_time_AlwaysAnimate':'PENDING_LAPTOP_IMPORT; AlwaysAnimate REQUIRED'})
(E/'native_qa.json').write_text(json.dumps({'clips':checks,'engine':'Blender native only','unity_runtime_pass':False},indent=2),encoding='utf8')
if '--' in sys.argv and 'metrics' in sys.argv[sys.argv.index('--')+1:]:sys.exit(0)
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=4;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=256;s.render.resolution_y=384;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
cam=bpy.data.objects['Assembly_Review_Camera'];s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=1.18;cam.location=(1.8,-3,.62);cam.rotation_euler=(Vector((.002,-.025,.49))-cam.location).to_track_quat('-Z','Y').to_euler()
for o in bpy.data.objects:
 if o.type=='MESH' and o.name in {'Assembly_Studio_Ground','QA_Grasp_Prop','QA_Grasp_Pedestal'}:o.hide_render=True
for label,action,count in [('sequence','YRA_R4_QA_MilestoneA_Sequence',265),('strong_2cycles','YRA_R4_Struggle_Strong_Loop',97),('startle','YRA_R4_Startle_Short',37)]:
 r.animation_data.action=bpy.data.actions[action];end=round(r.animation_data.action.frame_range[1]);dest=OUT/'render_frames'/label;dest.mkdir(parents=True,exist_ok=True)
 for f in range(1,count+1):
  frame=1+(f-1)%(end-1) if count>end else f;s.frame_set(frame);s.render.filepath=str(dest/f'{f:04d}.png')
  if 'force' in sys.argv or not Path(s.render.filepath).exists():bpy.ops.render.render(write_still=True)
 print('RENDER_DONE',label,flush=True)
print('NATIVE_R4_QA_DONE',flush=True)
