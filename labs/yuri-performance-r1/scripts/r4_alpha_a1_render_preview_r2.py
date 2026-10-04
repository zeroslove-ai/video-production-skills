"""Fixed A1 preserved-rig candidate multiview CPU preview; no scene save."""
import bpy,sys,json,hashlib
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_adapter import ReactionLane
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
SOURCE=BASE/'alpha-a1-idle-candidate-r2/Character_R4_A1_Female_Idle_BODY_CANDIDATE_OFF_R2_20261004.blend'
def main(view,frames):
    out=BASE/('alpha-a1-idle-preview-'+view+'-r2');out.mkdir(exist_ok=False)
    expected=json.loads((BASE/'alpha-a1-idle-candidate-r2/A1_RETARGET_RECEIPT_PRIVATE_R1.json').read_bytes())
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==expected['candidate_SHA']
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False);s=bpy.context.scene
    s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=2;s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=False
    s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=256;s.render.resolution_y=384;s.render.resolution_percentage=100
    s.render.image_settings.file_format='PNG';s.render.image_settings.color_depth='8';s.render.image_settings.color_mode='RGB'
    s.render.fps=30;s.render.fps_base=1
    cam=s.camera;cam.data.type='ORTHO';cam.data.ortho_scale=1.18
    cam.location={'front':(0,-3,.49),'quarter':(1.8,-3,.49),'side':(3,-.025,.49)}[view]
    cam.rotation_euler=(Vector((.002,-.025,.49))-cam.location).to_track_quat('-Z','Y').to_euler()
    lane=ReactionLane();a=lane.on(expected['action']);assert list(a.frame_range)==[1,301]
    for f in frames:
        s.frame_set(f);bpy.context.view_layer.update();s.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
    lane.off()
    with (out/'RENDER_RECEIPT.json').open('x',encoding='utf8') as fp:json.dump({'candidate_SHA':expected['candidate_SHA'],'action':a.name,'frames':list(frames),'fps':30,'camera_view':view,'resolution':[256,384],'samples':2,'device':'CPU','original_materials_lights':True,'no_source_or_candidate_save':True,'purpose':'1x body-contact/silhouette preview; noisy low-sample evidence, not final lighting/F2-F3'},fp,indent=2)
