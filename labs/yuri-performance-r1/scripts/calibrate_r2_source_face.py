"""User-supplied R2 source → private research copy → CPU facial calibration.
No topology/weight/rest-rig edits, no elaborate acting before the source face gate.
No product write. A/O are approximate semantic mouth recipes, not certified visemes.
"""
from pathlib import Path
import bpy,json,hashlib,math,time,sys
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'local/source-face-r2';OUT.mkdir(parents=True,exist_ok=True)
E=ROOT/'evidence/source-face-r2';E.mkdir(parents=True,exist_ok=True)
SWEEP='--' in sys.argv and 'sweep' in sys.argv[sys.argv.index('--')+1:]
if SWEEP:OUT=OUT/'amplitude-sweep';OUT.mkdir(exist_ok=True)
DETAIL='--' in sys.argv and 'detail' in sys.argv[sys.argv.index('--')+1:]
if DETAIL:OUT=OUT/'mouth-detail';OUT.mkdir(exist_ok=True)
SOURCE=Path(r'C:\Users\JAEWAN\Downloads\Character_Master_R2_20261002.blend')
fingerprint=hashlib.sha256(SOURCE.read_bytes()).hexdigest();assert fingerprint=='5e88819a61120b74c9a0e3de03f90b9890b7ac13eea2113e10fcada321d21d2e'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));s=bpy.context.scene;r=bpy.data.objects['Armature'];head=bpy.data.objects['Character_Body_Head'];r.hide_set(False)
original_actions={a.name for a in bpy.data.actions};original_bones=[b.name for b in r.data.bones]
# Checkpoint source scene first; no shared or source file writes.
copy=OUT/'R2_SOURCE_CALIBRATION_COPY.blend';bpy.ops.wm.save_as_mainfile(filepath=str(copy))
r.animation_data.action=bpy.data.actions['MOTION5H_WeightShift_Loop_8s'];s.frame_set(1)
for o in bpy.data.objects:
    if o.animation_data and o!=r:
        o.animation_data.action=None
        for track in o.animation_data.nla_tracks:track.mute=True
    if o.type=='MESH' and o.data.shape_keys and o.data.shape_keys.animation_data:
        o.data.shape_keys.animation_data.action=None
        for track in o.data.shape_keys.animation_data.nla_tracks:track.mute=True
allowed={o.name for o in bpy.data.objects if o.type=='MESH' and any(m.type=='ARMATURE' and m.object==r for m in o.modifiers)}|{'Globe.L','Globe.R','Hair_Scalp_Coverage'}
for o in bpy.data.objects:
    if o.type=='MESH':o.hide_render=o.name not in allowed
channels=['JawOpen','Smile.L','Smile.R','Blink.L','Blink.R','BrowRaise.L','BrowRaise.R','BrowKnit.L','BrowKnit.R','CheekLift.L','CheekLift.R','LipPucker','MouthWide','ExprSmileCurve','ExprMouthDown','ExprBrowInnerUp']
all_keys=[o.data.shape_keys for o in bpy.data.objects if o.type=='MESH' and o.data.shape_keys]
def state(values=None,gaze=(0.,0.)):
    values=values or {}
    for keys in all_keys:
        for key in keys.key_blocks:
            if key.name in channels:key.value=float(values.get(key.name,0))
    head['Face_GazeYaw']=float(gaze[0]);head['Face_GazePitch']=float(gaze[1]);bpy.context.view_layer.update()
state();deps=bpy.context.evaluated_depsgraph_get()
reference=[v.co.copy() for v in head.evaluated_get(deps).data.vertices]
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=12;s.cycles.use_denoising=True
s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=384;s.render.resolution_y=512;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.world.color=(.12,.14,.18)
for name,location,energy in [('RND_FaceKey',(-1,-2,2),140),('RND_FaceFill',(1,-1,1.3),65)]:
    data=bpy.data.lights.new(name,'AREA');o=bpy.data.objects.new(name,data);s.collection.objects.link(o);o.location=location;data.energy=energy;data.shape='DISK';data.size=1.4
    o.rotation_euler=(Vector((0,0,.89))-o.location).to_track_quat('-Z','Y').to_euler()
camdata=bpy.data.cameras.new('RND_CalibrationFace');cam=bpy.data.objects.new('RND_CalibrationFace',camdata);s.collection.objects.link(cam);s.camera=cam;camdata.type='ORTHO';camdata.ortho_scale=.30
cases=[('neutral',{},(0,0)),('blink_L',{'Blink.L':1},(0,0)),('blink_R',{'Blink.R':1},(0,0)),('blink_both',{'Blink.L':1,'Blink.R':1},(0,0)),('blink_half',{'Blink.L':.5,'Blink.R':.5},(0,0)),
       ('gaze_left',{},(-.65,0)),('gaze_right',{},(.65,0)),('gaze_up',{},(0,.4)),('gaze_down',{},(0,-.4)),
       ('A_approx',{'JawOpen':.55,'MouthWide':.18},(0,0)),('O_approx',{'JawOpen':.40,'LipPucker':.5},(0,0)),
       ('smile_squint',{'Smile.L':.4,'Smile.R':.33,'CheekLift.L':.2,'CheekLift.R':.16,'Blink.L':.10,'Blink.R':.08},(0,0)),
       ('shy_return_smile',{'Smile.L':.25,'Smile.R':.19,'BrowRaise.L':.14,'BrowRaise.R':.09,'ExprBrowInnerUp':.18},(-.4,-.25))]
views={'front':(0,-3,.895),'quarter':(1.1,-3,.895),'side':(3,-.15,.895)}
if SWEEP:
    # One control family at a time, all others neutral; no edits to key geometry.
    cases=[('neutral',{},(0,0))]
    cases += [(f'jaw_{v}',{'JawOpen':v},(0,0)) for v in (.4,.7,1.)]
    cases += [(f'wide_{v}',{'JawOpen':.7,'MouthWide':v},(0,0)) for v in (.3,.6,1.)]
    cases += [(f'pucker_{v}',{'JawOpen':.7,'LipPucker':v},(0,0)) for v in (.3,.6,1.)]
    cases += [(f'yaw_{v}',{},(v,0)) for v in (-2.,-1.,1.,2.)]
    cases += [(f'pitch_{v}',{},(0,v)) for v in (-1.,1.)]
    views={'front':views['front'],'quarter':views['quarter']}
target=Vector((0,-.025,.895))
if DETAIL:
    cases=[('neutral',{},(0,0)),('A_calibrated',{'JawOpen':.7,'MouthWide':1.},(0,0)),('O_calibrated',{'JawOpen':.7,'LipPucker':1.},(0,0))]
    camdata.ortho_scale=.065;s.render.resolution_x=640;s.render.resolution_y=480
    s.cycles.samples=24;target=Vector((.00195,-.078,.8505))
    views={k:(x,y,.8505) for k,(x,y,z) in views.items()}
reports=[];start=time.monotonic()
drivers=[{'key_id':k.name,'path':d.data_path,'mute':d.mute} for k in all_keys if k.animation_data for d in k.animation_data.drivers]
for name,values,gaze in cases:
    state(values,gaze);evaluated=head.evaluated_get(bpy.context.evaluated_depsgraph_get())
    assert len(evaluated.data.vertices)==len(reference)
    assert all(math.isfinite(c) for v in evaluated.data.vertices for c in v.co)
    delta=max((v.co-p).length for v,p in zip(evaluated.data.vertices,reference))
    images=[]
    for view,location in views.items():
        cam.location=location;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
        p=OUT/name/(view+'.png');p.parent.mkdir(exist_ok=True);s.render.filepath=str(p);bpy.ops.render.render(write_still=True);images.append(str(p))
    reports.append({'case':name,'native_shape_values':values,'native_gaze_controls':gaze,'evaluated_vertex_delta_m':delta,'frames':images,'structural':'FINITENESS_AND_CHANNEL_RESPONSE_CHECK_ONLY','visual_verdict':'PENDING'})
state();assert original_actions=={a.name for a in bpy.data.actions} and original_bones==[b.name for b in r.data.bones]
assert fingerprint==hashlib.sha256(SOURCE.read_bytes()).hexdigest()
receipt={'source':str(SOURCE),'source_sha256':fingerprint,'provenance':'Existing user-supplied asset from this session; private research reference only; no redistribution license asserted','research_copy':str(copy),'source_actions_preserved_count':len(original_actions),'body_bones':len(original_bones),'original_data_edits':'NONE: no mesh/skin/rest bone/key geometry/driver edits; disposable render settings and current channel values only','render_engine':'CYCLES_CPU_4_THREADS','elapsed_seconds':time.monotonic()-start,'cases':reports,'driver_mute_state':drivers,'A_O':'Approximate semantic jaw/wide/pucker recipes. Native dedicated A/O viseme keys absent; phonetic acceptance NOT established.','actual_face_gate':'PENDING_RENDER_REVIEW; no elaborate target acting authored yet','actual_yuri_approved_performances':0}
receipt['missing_external_images']=[{'name':im.name,'path':bpy.path.abspath(im.filepath)} for im in bpy.data.images if im.source=='FILE' and not im.packed_file and im.filepath and not Path(bpy.path.abspath(im.filepath)).exists()]
(E/('mouth_detail.json' if DETAIL else 'amplitude_sweep.json' if SWEEP else 'calibration.json')).write_text(json.dumps(receipt,indent=2));print('SOURCE_FACE_RENDER_DONE',len(reports))
