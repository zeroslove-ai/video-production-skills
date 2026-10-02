"""Owned CPU rendering and structured all-frame QA of the existing R2 checkpoint."""
from pathlib import Path
import bpy,json,sys,math
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'local/acting-r2';E=ROOT/'evidence/acting-r2'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'YURI_PERFORMANCE_ACTING_R2.blend'))
s=bpy.context.scene;r=bpy.data.objects['ProxyHumanoid']
registry=json.loads((E/'action_registry.json').read_text());cameras=json.loads((E/'camera_metadata.json').read_text())
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=12;s.cycles.use_denoising=True
s.render.threads_mode='FIXED';s.render.threads=4
def bind(clip,mode='natural'):
    for o in bpy.data.objects:
        if o.animation_data:o.animation_data.action=None
        if o.type=='MESH' and o.data.shape_keys and o.data.shape_keys.animation_data:o.data.shape_keys.animation_data.action=None
    for owner,name in registry[clip][mode]:
        o=bpy.data.objects.get(owner) or bpy.data.shape_keys.get(owner)
        o.animation_data_create();o.animation_data.action=bpy.data.actions[name]
def cam(name):
    c=cameras[name];s.camera=bpy.data.objects[c['object']]
    s.render.resolution_x,s.render.resolution_y=c['resolution'];s.render.resolution_percentage=100
def render(clip,camera,frame,mode='natural'):
    bind(clip,mode);cam(camera);s.frame_set(frame)
    d=OUT/clip/mode/camera;d.mkdir(parents=True,exist_ok=True)
    s.render.filepath=str(d/f'{frame:04d}.png');bpy.ops.render.render(write_still=True)
def qa():
    results=[]
    for clip in ('greeting_wave','shy_lookaway','please_tilt'):
        bind(clip);matrices=[];motion=[];points=[]
        for frame in range(1,122):
            s.frame_set(frame);bpy.context.view_layer.update()
            matrices.append({b.name:b.matrix.copy() for b in r.pose.bones})
            points.append({b.name:list(r.matrix_world@b.head) for b in r.pose.bones})
        max_step=max(math.degrees(min((m[b].to_quaternion().rotation_difference(p[b].to_quaternion())).angle,2*math.pi-(m[b].to_quaternion().rotation_difference(p[b].to_quaternion())).angle)) for p,m in zip(matrices,matrices[1:]) for b in p)
        root=max((m['hips'].translation-matrices[0]['hips'].translation).length for m in matrices)
        feet=max((m[b].translation-matrices[0][b].translation).length for m in matrices for b in ('foot.L','foot.R'))
        neutral=max(abs(matrices[0][b][i][j]-matrices[-1][b][i][j]) for b in matrices[0] for i in range(4) for j in range(4))
        print('QA_METRICS',clip,root,feet,neutral,max_step,flush=True)
        assert root<1e-7 and feet<1e-7 and neutral<1e-6 and max_step<15, (clip,root,feet,neutral,max_step)
        framing={}
        for name in cameras:
            cam(name);coords=[]
            for frame in range(1,122):
                s.frame_set(frame)
                bones=('hips','head','hand.R','hand.L','foot.L','foot.R') if name in ('full_body','vertical') else ('head',)
                for b in bones:
                    p=world_to_camera_view(s,s.camera,r.matrix_world@r.pose.bones[b].head);coords.append(list(p))
            framing[name]={'bone_anchor_min_xy':[min(p[i] for p in coords) for i in (0,1)],'bone_anchor_max_xy':[max(p[i] for p in coords) for i in (0,1)],'all_tested_anchors_in_frame':all(0<=p[0]<=1 and 0<=p[1]<=1 and p[2]>0 for p in coords),'bounds_scope':'bone anchors only; rendered silhouette review required'}
        results.append({'clip':clip,'max_bone_rotation_step_deg':max_step,'hips_excursion_m':root,'foot_anchor_drift_m':feet,'neutral_matrix_error':neutral,'camera_anchors':framing,'actual_yuri_face_acceptance':False})
        (E/(clip+'_pose17.json')).write_text(json.dumps({'convention':'17 original proxy bone heads; NOT OpenPose compatible','space':'Blender Z-up meters','fps':24,'frames':points},indent=2))
    (E/'motion_qa.json').write_text(json.dumps({'result':'STRUCTURAL_PROXY_PASS','clips':results},indent=2))
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['contacts']
mode=args[0]
if mode=='qa':qa()
elif mode=='contacts':
    for clip in ('greeting_wave','shy_lookaway','please_tilt'):
        for camera in cameras:
            for f in (1,13,25,43,61,85,109,121):render(clip,camera,f)
elif mode=='video':
    clip=args[1];camera=args[2];variant=args[3] if len(args)>3 else 'natural'
    for f in range(1,122):render(clip,camera,f,variant)
else:raise ValueError(mode)
print('RENDER_R2_PASS',args)
