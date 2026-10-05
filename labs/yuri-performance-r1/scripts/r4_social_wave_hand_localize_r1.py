"""Read-only localization of inclusive Wave pairs and full hand-close framing; no new motion."""
import bpy,sys,json,hashlib,ast,gzip,collections
from pathlib import Path
import numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_appearance_adapter import ReactionLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-social-wave-hand-localize-r1';O.mkdir(exist_ok=False);m=json.loads((B/'alpha-social-wave-hand-quality-r1/WAVE_HAND_QUALITY_PRIVATE_R1.json').read_bytes());old=json.loads((H.parent/'evidence/alpha-social-greeting-source-candidate-r1/SOCIAL_GREETING_MANIFEST_R1.json').read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(old['candidate'])==m['unchanged_candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=old['candidate'],use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered'];names=list(bpy.data.actions.keys());before=snapshot(names);gn={g.index:g.name for g in body.vertex_groups};fingerbones={p.name for p in r.pose.bones if p.name.endswith('.R') and any(n in p.name for n in ['thumb','index','middle','ring','pinky'])};handbones=fingerbones|{'hand.R'};handids=np.array([v.index for v in body.data.vertices if sum(g.weight for g in v.groups if gn[g.group] in handbones)>.5],int);ns={'bpy':bpy,'np':np,'fixed':{}};tree=ast.parse((H/'r4_existing_reach_contact_closure_r1.py').read_text(encoding='utf8'));exec(compile(ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='geom'],type_ignores=[]),'<same_geom>','exec'),ns);geom=ns['geom'];ledger=json.loads(gzip.open(B/'alpha-social-wave-hand-quality-r1/WAVE_HAND_INCLUSIVE_CONTACT_PRIVATE_R1.json.gz','rt',encoding='utf8').read());key=body.name+'__self_nonadjacent';owners=[]
for row in ledger:
 if row['frame'] not in [23,41]:continue
 for pair in row['new_pair_identities'][key]:
  w=collections.Counter()
  for t in pair:
   for i in t:w.update({gn[g.group]:g.weight for g in body.data.vertices[i].groups if gn[g.group] in r.pose.bones})
  owners.append({'frame':row['frame'],'pair_private':pair,'dominant_source_bones':w.most_common(4),'touches_actual_hand_vertex':any(i in set(handids.tolist()) for t in pair for i in t)})
cam=s.camera;savecam=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale);cam.data.type='ORTHO';cam.data.ortho_scale=.19;direction=Vector((.6,-1,0)).normalized();cam.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler();lane=ReactionLane();lane.on('YURI_R4_SOCIAL_GREETING_WAVE_BODY_R1');frames=[]
for row in m['rows_private']:
 f=row['frame'];s.frame_set(f);bpy.context.view_layer.update();data=geom(body)[0];assert hashlib.sha256(data.tobytes()).hexdigest()==row['actual_mesh_SHA_private'][body.name];cam.location=Vector(row['camera_location_private']);bpy.context.view_layer.update();pp=np.array([list(world_to_camera_view(s,cam,Vector(data[i]))) for i in handids]);inside=((pp[:,0]>=0)&(pp[:,0]<=1)&(pp[:,1]>=0)&(pp[:,1]<=1)&(pp[:,2]>0));frames.append({'frame':f,'actual_hand_vertices':len(handids),'outside_camera_count':int((~inside).sum()),'projected_min_max_private':[pp.min(axis=0).tolist(),pp.max(axis=0).tolist()]})
lane.off();cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale=savecam;assert snapshot(names)==before and sha(old['candidate'])==old['candidate_SHA']
(O/'WAVE_PAIR_OWNERSHIP_FRAMING_PRIVATE_R1.json').write_text(json.dumps({'unchanged_candidate_SHA':old['candidate_SHA'],'source79_OFF_restored':True,'pair_ownership_private':owners,'framing_rows_scalar':frames,'source_hand_vertex_ids_private':handids.tolist(),'new_motion_or_candidate':False},indent=2),encoding='utf8');print('WAVE_PAIR_OWNERSHIP_AND91_HAND_FRAMING_READONLY_COMPLETE',max(x['outside_camera_count'] for x in frames),flush=True)
