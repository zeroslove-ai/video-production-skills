import bpy,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from r4_appearance_adapter import ReactionLane
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'alpha-a1-pose-diagnostic-r1';OUT.mkdir(exist_ok=False)
bpy.ops.wm.open_mainfile(filepath=str(BASE/'alpha-a1-idle-candidate-r1/Character_R4_A1_Female_Idle_BODY_CANDIDATE_OFF_20261004.blend'),use_scripts=False)
r=bpy.data.objects['Meshy_Fitted_Rig']
def state():
    return {'world':[list(v) for v in r.matrix_world],'bones':{n:{'matrix':[list(v) for v in r.pose.bones[n].matrix],'basis':[list(v) for v in r.pose.bones[n].matrix_basis],'location':list(r.pose.bones[n].location),'quaternion':list(r.pose.bones[n].rotation_quaternion),'inherit_rotation':r.data.bones[n].use_inherit_rotation,'local_location':r.data.bones[n].use_local_location} for n in ['root','pelvis','thigh.L','foot.L']}}
off=state();lane=ReactionLane();lane.on('YURI_R4_A1_Female_Idle_BODY_CANDIDATE_R1');on=state()
with (OUT/'POSE_DIAGNOSTIC_PRIVATE_R1.json').open('x') as f:json.dump({'OFF':off,'ON':on},f,indent=2)
print(json.dumps({'OFF':off,'ON':on}),flush=True)
