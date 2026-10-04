"""Fixed A1 all-frame sole reference/geometry checks plus exact OFF neutral PNG."""
import bpy,sys,json,hashlib,math,numpy as np
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_adapter import ReactionLane
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'alpha-a1-contact-qa-r3';OUT.mkdir(exist_ok=False)
SOURCE=BASE/'alpha-a1-idle-candidate-r3/Character_R4_A1_Female_Idle_BODY_CANDIDATE_OFF_R3_20261004.blend'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered']
def worldpoints(o):
    e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();a=np.array([list(e.matrix_world@v.co) for v in m.vertices]);e.to_mesh_clear();return a
baseline=worldpoints(body);floor=float(baseline[:,2].min())
sole_ids={side:np.where((baseline[:,2]<floor+.028)&((baseline[:,0]>.00195) if side=='L' else (baseline[:,0]<.00195)))[0] for side in ['L','R']}
assert all(len(ids)>10 for ids in sole_ids.values())
neutral=s.camera;assert neutral.name=='Assembly_Review_Camera'
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=8;s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=False
s.render.threads_mode='FIXED';s.render.threads=2;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.image_settings.color_depth='8'
s.render.filepath=str(OUT/'CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png');bpy.ops.render.render(write_still=True)
lane=ReactionLane();lane.on('YURI_R4_A1_Female_Idle_BODY_CANDIDATE_R3');frames=[]
roots=[];hands=[]
for f in range(1,302):
    s.frame_set(f);bpy.context.view_layer.update();v=worldpoints(body);assert v.shape==baseline.shape and np.isfinite(v).all()
    root=list((r.matrix_world@r.pose.bones['root'].matrix).translation);roots.append(root)
    soles={side:{'minimum_z':float(v[ids,2].min()),'centroid':v[ids].mean(0).tolist()} for side,ids in sole_ids.items()}
    frames.append({'frame':f,'soles':soles,'body_bounds_min':v.min(0).tolist(),'body_bounds_max':v.max(0).tolist()})
    hands.append({side:list((r.matrix_world@r.pose.bones['hand.'+side].matrix).translation) for side in ['L','R']})
lane.off();assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='a6eaea6d2a5e4de9896c05af40bc581f6f48ccb5b623db815762c56e7c6ce0e1'
report={'frames_checked':301,'FPS':30,'candidate_SHA':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'root_world_range_m':np.ptp(np.array(roots),axis=0).tolist(),'source_neutral_body_min_z_reference':floor,'sole_reference':'Same immutable body vertex IDs selected within28mm of source neutral minimum; not external collider/floor or triangle-contact certification','sole_vertex_counts':{k:len(ids) for k,ids in sole_ids.items()},'soles':{side:{'min_z_offset_to_source_floor_m':min(x['soles'][side]['minimum_z']-floor for x in frames),'max_z_offset_to_source_floor_m':max(x['soles'][side]['minimum_z']-floor for x in frames),'centroid_range_m':np.ptp(np.array([x['soles'][side]['centroid'] for x in frames]),axis=0).tolist()} for side in ['L','R']},'body_finite_all_frames':True,'hand_trajectory_range_m':{side:np.ptp(np.array([x[side] for x in hands]),axis=0).tolist() for side in ['L','R']},'frames_private':frames,'foot_contact_physics_certified':False,'mesh_self_intersection_certified':False,'gate':'1x visual/contact defect review required; no product promotion'}
with (OUT/'A1_CONTACT_QA_PRIVATE_R3.json').open('x') as fp:json.dump(report,fp,indent=2)
print('A1_ALL_FRAME_CONTACT_REFERENCE_COMPLETE',flush=True)
