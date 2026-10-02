"""CPU-only full-interval preview, 60fps motion baked, 30fps display preview."""
from pathlib import Path
import bpy,json,sys,math,hashlib
R=Path(__file__).resolve().parents[1];L=R/'local/dance-benchmark-r1';E=R/'evidence/dance-benchmark-r1';method=sys.argv[-1];candidate=L/(method+'_DANCE_R1.blend');sha=hashlib.sha256(candidate.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(candidate));s=bpy.context.scene;r=bpy.data.objects['ProxyHumanoid'];s.cycles.device='CPU';s.cycles.samples=2;s.cycles.use_denoising=True;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=320;s.render.resolution_y=480;s.render.image_settings.file_format='PNG';folder=L/(method+'_render_'+sha[:10]);folder.mkdir(exist_ok=True)
qa={'frames':360,'finite':True,'minimum_foot_head_z_m':1e9,'max_quaternion_step_deg':0.,'max_root_step_m':0.,'preview_fps':30,'motion_fps':60,'per_bone_max_step_deg':{b.name:0 for b in r.pose.bones}};prev=None;rootprev=None;points=[]
qa['candidate_sha256']=sha;qa['render_folder']=str(folder)
for fi in range(360):
    s.frame_set(fi+1);bpy.context.view_layer.update();q={b.name:b.matrix.to_quaternion() for b in r.pose.bones};root=r.pose.bones['hips'].head.copy();assert all(math.isfinite(x) for b in r.pose.bones for row in b.matrix for x in row)
    if prev:
        for n,v in q.items():qa['per_bone_max_step_deg'][n]=max(qa['per_bone_max_step_deg'][n],min(math.degrees(prev[n].rotation_difference(v).angle),360-math.degrees(prev[n].rotation_difference(v).angle)))
        worst,step=max(((n,min(math.degrees(prev[n].rotation_difference(v).angle),360-math.degrees(prev[n].rotation_difference(v).angle))) for n,v in q.items()),key=lambda v:v[1])
        if step>qa['max_quaternion_step_deg']:qa['max_quaternion_step_deg']=step;qa['worst_rotation']={'bone':worst,'frame':fi+1}
    if rootprev:qa['max_root_step_m']=max(qa['max_root_step_m'],(root-rootprev).length)
    qa['minimum_foot_head_z_m']=min(qa['minimum_foot_head_z_m'],*(r.pose.bones['foot.'+x].head.z for x in ['L','R']));prev=q;rootprev=root
    points.append({'frame':fi+1,'root':list(root),'joints':{b.name:{'head':list(b.head),'tail':list(b.tail)} for b in r.pose.bones}})
    if fi%2==0 and 'qa' not in sys.argv:
        p=folder/f'{fi//2:04d}.png'
        if not p.exists():s.render.filepath=str(p);bpy.ops.render.render(write_still=True)
    if fi%60==0:print('DANCE_RENDER',method,fi,flush=True)
assert hashlib.sha256(candidate.read_bytes()).hexdigest()==sha,'Candidate changed during run; refuse stale QA'
(E/(method+'_retarget_allframe_qa.json')).write_text(json.dumps(qa,indent=2));(E/(method+'_retarget_joints.json')).write_text(json.dumps(points,separators=(',',':')));print(json.dumps(qa))
