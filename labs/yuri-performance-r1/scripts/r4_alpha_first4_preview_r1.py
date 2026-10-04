"""Fixed A2-A4 CPU multiview preview at source time; no saves or runtime path."""
import bpy,sys,json,hashlib
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_adapter import ReactionLane
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
def main(step,view):
    assert step in ['a2','a3','a4'] and view in ['front','quarter','side']
    out=BASE/('alpha-'+step+'-preview-'+view+'-r2');out.mkdir(exist_ok=False)
    expected=json.loads((BASE/('alpha-'+step+'-contact-candidate-r2')/'CONTACT_CANDIDATE_PRIVATE_R2.json').read_bytes());source=Path(expected['candidate']);assert hashlib.sha256(source.read_bytes()).hexdigest()==expected['candidate_SHA']
    bpy.ops.wm.open_mainfile(filepath=str(source),use_scripts=False);s=bpy.context.scene
    source_scene_fps=s.render.fps/s.render.fps_base;assert source_scene_fps==24
    s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=2;s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2
    s.render.resolution_x=256;s.render.resolution_y=384;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_depth='8';s.render.image_settings.color_mode='RGB'
    cam=s.camera;cam.data.type='ORTHO';cam.data.ortho_scale=1.18;cam.location={'front':(0,-3,.49),'quarter':(1.8,-3,.49),'side':(3,-.025,.49)}[view];cam.rotation_euler=(Vector((.002,-.025,.49))-cam.location).to_track_quat('-Z','Y').to_euler()
    lane=ReactionLane();a=lane.on(expected['action']);fps=float(a['source_fps']);assert fps==30 and list(a.frame_range)==expected['frame_range']
    count=expected['frame_range'][1];step_frames=4 if step=='a2' else 1;frames=list(range(1,count+1,step_frames));preview_fps=fps/step_frames
    if step=='a2':assert count%4==0 # exact native container duration, no slowed playback
    for index,f in enumerate(frames,1):
        s.frame_set(f);bpy.context.view_layer.update();s.render.filepath=str(out/f'{index:04d}.png');bpy.ops.render.render(write_still=True)
        if index%200==0:print('NORMAL_TIME_PREVIEW',step,view,index,len(frames),flush=True)
    if frames[-1]!=count:
        s.frame_set(count);s.render.filepath=str(out/f'FINAL_NATIVE_FRAME_{count}.png');bpy.ops.render.render(write_still=True)
    lane.off()
    receipt={'step':step,'view':view,'candidate_SHA':expected['candidate_SHA'],'action':a.name,'source_scene_fps_preserved':source_scene_fps,'action_source_fps_native_readback':fps,'preview_fps':preview_fps,'pose_sampling_step_frames':step_frames,'source_frames_in_video':frames,'supplemental_final_native_pose_frame':count if frames[-1]!=count else None,'video_frame_count':len(frames),'native_container_duration_sec':count/fps,'preview_container_duration_sec':len(frames)/preview_fps,'resolution':[256,384],'CPU_threads':2,'samples':2,'no_save_export_source_Unity_write':True,'limits':'A2 long120s preview samples native poses every4frames at7.5fps, full native3608frame geometry QA separate. Other clips every native frame30fps. All playback1x source time, no final performance/contact-physics promotion.'}
    with (out/'RENDER_RECEIPT.json').open('x') as f:json.dump(receipt,f,indent=2)
