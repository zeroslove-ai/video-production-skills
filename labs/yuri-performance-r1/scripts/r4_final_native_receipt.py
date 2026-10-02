"""Final preservation and sequence-boundary validation after foot cleanup."""
import bpy,json,sys,math,hashlib
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).parent));from native_preservation import signature
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence/model-handoff-r4';OUT=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs/r4-model-handoff')
bpy.ops.wm.open_mainfile(filepath=str(OUT/'Character_Master_Reaction_R4_20261002.blend'))
r2=json.loads((E/'R2.json').read_text());r4=json.loads((E/'R4.json').read_text());names=list(r2['fingerprints']['actions'])+list(r4['fingerprints']['actions']);sig=signature(names)
assert all(sig['actions'][n]==h for d in [r2,r4] for n,h in d['fingerprints']['actions'].items());assert sig['meshes_shape_keys_weights']==r4['fingerprints']['meshes_shape_keys_weights'];assert sig['rest_rigs']==r4['fingerprints']['rest_rigs']
r=bpy.data.objects['Meshy_Fitted_Rig'];s=bpy.context.scene
def pose(name,f):
 r.animation_data.action=bpy.data.actions[name];s.frame_set(f);bpy.context.view_layer.update();return {b.name:b.matrix.copy() for b in r.pose.bones}
def diff(a,b):return {'max_bone_position_difference_m':max((a[n].translation-b[n].translation).length*r.matrix_world.to_scale().x for n in a),'max_bone_rotation_difference_deg':max(math.degrees(min(q.angle,2*math.pi-q.angle)) for n in a for q in [a[n].to_quaternion().rotation_difference(b[n].to_quaternion())])}
transitions=[]
for a,f,b in [('YRA_R4_Lift_Start',31,'YRA_R4_Struggle_Light_Loop'),('YRA_R4_Land_Soft',43,'YRA_R4_BalanceRecover')]:transitions.append({'from':a,'to':b,**diff(pose(a,f),pose(b,1))})
seq='YRA_R4_QA_MilestoneA_Sequence';steps=[];old=pose(seq,1)
for f in range(2,266):
 p=pose(seq,f);steps.append({'frame':f,**diff(old,p)});old=p
d={'preservation':'PASS','original_r2_actions':66,'original_r4_actions':78,'original_r4_meshes_weights_keys_rest':'EXACT_SIGNATURE_MATCH','production_retarget_clips':6,'qa_helpers':2,'transitions':transitions,'sequence_frames_evaluated':265,'sequence_max_step_m':max(x['max_bone_position_difference_m'] for x in steps),'sequence_boundary_steps':[x for x in steps if x['frame'] in {31,32,91,92,151,152,169,170,211,212}],'candidate_sha256':hashlib.sha256((OUT/'Character_Master_Reaction_R4_20261002.blend').read_bytes()).hexdigest(),'normal_speed_visual':'PENDING_FULL_PLAYBACK','unity_runtime':'UNTESTED; AlwaysAnimate REQUIRED'}
(E/'final_native_receipt.json').write_text(json.dumps(d,indent=2),encoding='utf8');print('R4_FINAL_NATIVE',d['candidate_sha256'],transitions,flush=True)
