"""Original-camera pixel equality + all-frame motion + native normal-speed proof.

Render overrides are in memory only. Original camera retained for authority PNG.
Secondary full-body QA framing is identical for OFF comparisons and all motion.
"""
import bpy,sys,json,hashlib,math,array
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_adapter import ReactionLane
ROOT=HERE.parent;OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/r4-appearance-preserve-correction-r1');E=ROOT/'evidence/r4-appearance-preserve-correction-r1'
SOURCE=ROOT/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend';MASTER=OUT/'Character_R4_Animation_OFF_20261003.blend'
mode=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'neutral'
def write(name,value):
    for p in (E/name,OUT/'metadata'/name):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf8')
def setup(full=False):
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=8;s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=False
    s.render.threads_mode='FIXED';s.render.threads=4;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.image_settings.color_depth='8';s.render.resolution_percentage=100
    if full:
        s.render.resolution_x=256;s.render.resolution_y=384
        cam=s.camera;cam.data.ortho_scale=1.18;cam.location=(1.8,-3,.62);cam.rotation_euler=(Vector((.002,-.025,.49))-cam.location).to_track_quat('-Z','Y').to_euler()
    return s
def render(path):
    path.parent.mkdir(parents=True,exist_ok=True);bpy.context.scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
def pixels(path):
    i=bpy.data.images.load(str(path),check_existing=False);a=array.array('f',[0])*len(i.pixels);i.pixels.foreach_get(a);size=list(i.size);bpy.data.images.remove(i);return a,size
def compare(a,b):
    aa,sa=pixels(a);bb,sb=pixels(b);assert sa==sb
    n=sum(x!=y for x,y in zip(aa,bb));maximum=max(abs(x-y) for x,y in zip(aa,bb))
    return {'size':sa,'unequal_channels':n,'max_abs_pixel_channel_difference':maximum,'pixel_float_sha256_before':hashlib.sha256(aa.tobytes()).hexdigest(),'pixel_float_sha256_after':hashlib.sha256(bb.tobytes()).hexdigest(),'PASS':n==0}
if mode=='neutral':
    for kind,full in [('authority_source_camera',False),('full_body_QA',True)]:
        paths=[]
        for label,file in [('before',SOURCE),('after_OFF',MASTER),('after_ON_then_OFF',MASTER)]:
            bpy.ops.wm.open_mainfile(filepath=str(file),use_scripts=False)
            if label=='after_ON_then_OFF':
                lane=ReactionLane();lane.on('YRA_R4_Struggle_Strong_Loop');bpy.context.scene.frame_set(19);lane.off()
            setup(full);path=OUT/'neutral'/f'{kind}_{label}.png';render(path);paths.append(path)
        result={'before_after_OFF':compare(paths[0],paths[1]),'before_after_ON_then_OFF':compare(paths[0],paths[2])}
        write(f'pixels_{kind}.json',result)
        assert all(v['PASS'] for v in result.values()),result
    print('NEUTRAL_PIXEL_EQUAL_PASS',flush=True)
elif mode=='library':
    bpy.ops.wm.open_mainfile(filepath=str(OUT/'YURI_REACTION_R4_ACTIONS_ONLY_20261003.blend'),use_scripts=False)
    data={'objects':len(bpy.data.objects),'meshes':len(bpy.data.meshes),'armatures':len(bpy.data.armatures),'materials':len(bpy.data.materials),'images':len(bpy.data.images),'actions':[a.name for a in bpy.data.actions]}
    assert data['objects']==data['meshes']==data['armatures']==data['materials']==data['images']==0,data
    assert len(data['actions'])==8,data
    write('action_library_only.json',data);print('ACTION_LIBRARY_ONLY_PASS',flush=True)
elif mode=='motion':
    bpy.ops.wm.open_mainfile(filepath=str(MASTER),use_scripts=False)
    s=bpy.context.scene;lane=ReactionLane();r=lane.rig;checks=[]
    names=['YRA_R4_'+n for n in ['Startle_Short','Lift_Start','Struggle_Light_Loop','Struggle_Strong_Loop','Land_Soft','BalanceRecover']]
    for name in names:
        a=lane.on(name);end=round(a.frame_range[1]);loop='Loop' in name;count=2*(end-1)+1 if loop else end
        first=None;prev=None;motion=0;step=0;roots=[];finite=True;seam=None
        for f in range(1,count+1):
            local=1+(f-1)%(end-1) if loop and f>end else f
            s.frame_set(local);bpy.context.view_layer.update()
            v={b.name:(r.matrix_world@b.matrix).copy() for b in r.pose.bones}
            if first is None:first=v
            motion=max(motion,max((m.translation-first[n].translation).length for n,m in v.items() if n!='root'))
            if prev:step=max(step,max((m.translation-prev[n].translation).length for n,m in v.items()))
            prev=v;roots.append(v['root'].translation.copy())
            if f==end:seam=max((v[n].translation-first[n].translation).length for n in v)
            deps=bpy.context.evaluated_depsgraph_get()
            for mesh in ['Meshy_Body_NeutralCovered','Character_Body_Head','Hair_Replacement_R4']:
                evaluated=bpy.data.objects[mesh].evaluated_get(deps)
                finite &= all(math.isfinite(x) for p in evaluated.bound_box for x in p)
        assert motion>1e-4 and step<.08 and finite,(name,motion,step,finite)
        if loop:assert seam<1e-5,(name,seam)
        checks.append({'action':name,'frames_sampled':count,'cycles':2 if loop else 1,'actual_non_root_bone_motion_m':motion,'max_bone_step_m':step,'root_excursion_m':max((p-roots[0]).length for p in roots),'loop_seam_m':seam if loop else None,'body_face_hair_bounds_finite':finite,'native_motion':'PASS','Unity_state_weight_normalized_time_AlwaysAnimate':'PENDING; REQUIRED regression gate'})
        lane.off()
    write('all_frame_motion.json',{'clips':checks,'source_hierarchy':'original four rigs; no merged GameRig','FPS':24,'Unity_PASS':False})
    print('ALL_FRAME_MOTION_PASS',flush=True)
elif mode=='render':
    bpy.ops.wm.open_mainfile(filepath=str(MASTER),use_scripts=False);s=setup(True);s.render.fps=24;s.render.fps_base=1;lane=ReactionLane()
    for label,name,count in [('sequence','YRA_R4_QA_MilestoneA_Sequence',265),('strong_2cycles','YRA_R4_Struggle_Strong_Loop',97),('startle','YRA_R4_Startle_Short',37)]:
        a=lane.on(name);end=round(a.frame_range[1]);dest=OUT/'render_frames'/label;dest.mkdir(parents=True,exist_ok=True)
        for f in range(1,count+1):
            local=1+(f-1)%(end-1) if count>end else f;s.frame_set(local);path=dest/f'{f:04d}.png'
            if not path.exists():render(path)
        lane.off();print('NATIVE_PRESERVED_RENDER_DONE',label,flush=True)
else:raise ValueError(mode)
