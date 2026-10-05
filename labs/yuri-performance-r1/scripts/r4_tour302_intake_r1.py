"""Readonly ONE existing Tour left elbow interval and hinge intake."""
import bpy,sys,json,hashlib,math,gzip
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_native_tour_adapter_r1 import NativeTourLane
from r4_appearance_signature import snapshot
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-tour302-intake-r1';O.mkdir(exist_ok=False)
m=json.loads((B/'alpha-native-tour-recovery-r2/NATIVE_TOUR_RECOVERY_PRIVATE_R2.json').read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(m['candidate'])==m['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=m['candidate'],use_scripts=False)
s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];names=list(m['original78_signature_private']['actions']);before=snapshot(names);assert before==m['original78_signature_private']
ln=NativeTourLane();ln.on();rows=[]
for f in range(289,386):
 s.frame_set(f);bpy.context.view_layer.update();p=r.pose.bones['forearm.L'];rows.append({'frame':f,'quaternion_private':list(p.rotation_quaternion),'EulerXYZ_degrees':[(x*180/math.pi) for x in p.rotation_quaternion.to_euler('XYZ')],'pose_basis_private':[list(x) for x in p.matrix_basis],'constraints':[{'name':c.name,'type':c.type,'influence':c.influence,'mute':c.mute} for c in p.constraints]})
ln.off();assert snapshot(names)==before and sha(m['candidate'])==m['candidate_SHA']
(O/'TOUR302_HINGE_INTAKE_PRIVATE_R1.json').write_text(json.dumps({'source_action_SHA':m['source_Action_SHA'],'candidate_SHA':m['candidate_SHA'],'source78_OFF_restored':True,'local_clock':[289,385],'native_fps':24,'rows_private':rows},indent=2),encoding='utf8')
print('TOUR302_READONLY_HINGE_INTAKE_COMPLETE',flush=True)
