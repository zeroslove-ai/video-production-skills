"""Native body adapter all-frame gates, then CPU contact frames or a single movie shot."""
from pathlib import Path
import bpy,json,sys,math,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'local/native-body-r3';E=ROOT/'evidence/native-body-r3'
meta=json.loads((E/'build_receipt.json').read_text());p=Path(meta['candidate']);assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['candidate_sha256']
bpy.ops.wm.open_mainfile(filepath=str(p));s=bpy.context.scene;r=bpy.data.objects['Armature']
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['qa']
def bind(clip):r.animation_data.action=bpy.data.actions[meta['action_registry'][clip]];s.frame_set(1)
def camera(name):
    c=meta['cameras'][name];s.camera=bpy.data.objects[c['object']];s.render.resolution_x,s.render.resolution_y=c['resolution'];s.render.resolution_percentage=100
def angular_distance(a,b):
    # q and -q encode the same orientation. Report shortest physical rotation.
    angle=math.degrees(a.rotation_difference(b).angle)
    return min(angle,360-angle)
if args[0]=='qa':
    reports=[]
    for clip in meta['action_registry']:
        bind(clip);initial={b.name:b.matrix.copy() for b in r.pose.bones};foot0=[r.pose.bones[f'J_Bip_{x}_Foot'].head.copy() for x in ('L','R')];root0=r.pose.bones['Root'].head.copy()
        previous=None;maxstep=0;maxroot=0;maxfoot=0;maxmove=0;motion_bones=set();worst=None
        # Half frames expose quaternion interpolation as well as sampled key poses.
        for half in range(241):
            frame=1+half/2;s.frame_set(int(frame),subframe=frame-int(frame));bpy.context.view_layer.update()
            current={b.name:b.matrix.to_quaternion() for b in r.pose.bones}
            assert all(math.isfinite(x) for b in r.pose.bones for row in b.matrix for x in row)
            if previous:
                name,step=max(((n,angular_distance(previous[n],q)) for n,q in current.items()),key=lambda pair:pair[1])
                if step>maxstep:maxstep=step;worst={'bone':name,'frame':frame,'step_degrees':step}
            previous=current
            maxroot=max(maxroot,(r.pose.bones['Root'].head-root0).length)
            maxfoot=max(maxfoot,max((r.pose.bones[f'J_Bip_{x}_Foot'].head-pos).length for x,pos in zip(('L','R'),foot0)))
            for b in r.pose.bones:
                delta=angular_distance(initial[b.name].to_quaternion(),current[b.name])
                maxmove=max(maxmove,delta)
                if delta>.1:motion_bones.add(b.name)
        endpoint=max(abs(b.matrix[i][j]-initial[b.name][i][j]) for b in r.pose.bones for i in range(4) for j in range(4))
        report={'clip':clip,'samples':241,'max_step_deg_per_half_frame':maxstep,'worst_step':worst,'root_drift_m':maxroot,'foot_anchor_drift_m':maxfoot,'endpoint_matrix_delta':endpoint,'max_motion_deg':maxmove,'moving_bones':sorted(motion_bones),'technical':'PASS' if maxstep<10 and maxroot<1e-5 and maxfoot<1e-5 and endpoint<1e-5 and len(motion_bones)>2 else 'FAIL','visual':'PENDING'};reports.append(report)
    (E/'structural_qa.json').write_text(json.dumps({'candidate_sha256':meta['candidate_sha256'],'clips':reports},indent=2));print(json.dumps(reports));assert all(x['technical']=='PASS' for x in reports)
elif args[0]=='contacts':
    for clip in meta['action_registry']:
        bind(clip)
        for view in ('full_body','waist_threequarter','hand_face'):
            camera(view)
            for f in (1,25,49,73,97,121):
                path=OUT/clip/view/f'{f:04d}.png';path.parent.mkdir(parents=True,exist_ok=True);s.frame_set(f);s.render.filepath=str(path);bpy.ops.render.render(write_still=True)
elif args[0]=='video':
    clip,view=args[1:3];bind(clip);camera(view)
    for f in range(1,122):
        path=OUT/clip/view/f'{f:04d}.png';path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists():continue
        s.frame_set(f);s.render.filepath=str(path);bpy.ops.render.render(write_still=True)
else:raise ValueError(args)
