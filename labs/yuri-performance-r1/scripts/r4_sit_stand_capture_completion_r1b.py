"""Render-only completion of SAME failed source candidate after owned600s budget expiry."""
import bpy,sys,json,hashlib,time,gzip,collections,math,shutil
from pathlib import Path
import numpy as np
from mathutils import Vector
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
from r4_sit_stand_adapter_r1 import SitStandLane
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');P=B/'alpha-sit-stand-source-candidate-r1';O=B/'alpha-sit-stand-capture-completion-r1b';O.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();m=json.loads((P/'SIT_STAND_SOURCE_PRIVATE_R1.json').read_bytes());fg=json.loads((B/'o1-sit-stand-source-candidate-r1b/NATIVE_GUARD_RESULT.json').read_bytes());assert fg['guard_status']!='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN' and fg['cleanup_job_before_close']['active']==0 and fg['cleanup_drain'];assert sha(m['source'])==m['source_SHA'] and sha(m['candidate'])==m['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=m['candidate'],use_scripts=False);s=bpy.context.scene;names=list(m['original78_signature_private']['actions']);before=snapshot(names);assert before==m['original78_signature_private'];r=bpy.data.objects['Meshy_Fitted_Rig'];offs={n:r.pose.bones[n].rotation_quaternion.copy() for n in ['thigh.L','thigh.R','shin.L','shin.R','upper_arm.L','upper_arm.R']}
# First and worst frozen BODY phases, classify existing exact pair identities by unchanged original skin weights; no second collision scan/candidate.
key='Meshy_Body_NeutralCovered__self_nonadjacent';firstrow=next(x for x in m['rows_private'] if x['new_surface_pair_counts_vs_source_OFF'][key]>0);worstrow=max(m['rows_private'],key=lambda x:x['new_surface_pair_counts_vs_source_OFF'][key]);ledger=json.loads(gzip.open(P/'SIT_STAND_TRIANGLE_IDENTITIES_PRIVATE_R1.json.gz','rt',encoding='utf8').read());body=bpy.data.objects['Meshy_Body_NeutralCovered'];groupnames={g.index:g.name for g in body.vertex_groups};localizations=[]
for row in [firstrow,worstrow]:
 pairs=next(x for x in ledger['frames'] if x['frame']==row['frame'])['new_pair_identities'][key];rank=collections.Counter();unmapped=0
 for a,b in pairs:
  labels=[]
  for tri in [a,b]:
   sums=collections.Counter()
   for idx in tri:
    if idx>=len(body.data.vertices):unmapped+=1;continue
    for gg in body.data.vertices[idx].groups:
     if gg.weight>.001:sums[groupnames[gg.group]]+=gg.weight
   labels.append(sums.most_common(1)[0][0] if sums else 'unmapped')
  rank[' / '.join(sorted(labels))]+=1
 localizations.append({'actual_body_frame':row['frame'],'new_nonadjacent_BODY_pairs':len(pairs),'top_skin_bone_pair_distribution':rank.most_common(16),'unmapped_evaluated_indices':unmapped})
localization={'first_and_worst':localizations,'scope':'Only already-measured first and worst exact pair identities + immutable skin weights; no new pose/contact family or corpus scan.'}
# Actual local joint comparison against donor and intended world goals at first failure, seated anchor, worst failure.
from mathutils import Matrix,Quaternion
intake=json.loads((B/'alpha-sit-stand-source-intake-r1/SIT_STAND_SOURCE_INTAKE_PRIVATE_R1.json').read_bytes());C=Quaternion(Vector((0,0,1)),math.pi);source_rest={n:Matrix(v) for n,v in intake['rest_world_private'].items()};source_first={n:Matrix(v) for n,v in intake['samples_private']['Sitting_Enter'][0].items()};offworld={b.name:r.matrix_world@b.matrix for b in r.pose.bones};author={x['frame']:x for x in m['author_rows_private']};compare=[]
# Neutral actual source mesh OFF for first source support displacement, not a render/source corpus sweep.
mod=__import__('ast').parse((H/'r4_existing_reach_contact_closure_r1.py').read_text(encoding='utf8'));exec(compile(__import__('ast').Module(body=[x for x in mod.body if isinstance(x,__import__('ast').FunctionDef) and x.name=='geom'],type_ignores=[]),'<pinned_actual_mesh>','exec'));fixed={};neutral=geom(body)[0];sole=np.load(P/'SIT_STAND_ACTUAL_SOLES_PRIVATE_R1.npz');footids={q:np.array([v.index for v in body.data.vertices if sum(g.weight for g in v.groups if groupnames[g.group] in ['foot.'+q,'toe.'+q])>.5],int) for q in ['L','R']};firstfoot={}
for q in footids:
 vv=sole[q];patchid=sole[q+'_original_support_patch_vertex_ids'];patch=np.array([np.where(footids[q]==idx)[0][0] for idx in patchid]);d=np.linalg.norm(vv[:,patch,:2]-vv[0,patch,:2],axis=2).max(axis=1);step=np.linalg.norm(np.diff(vv[:,patch,:2],axis=0),axis=2).max(axis=1);ii=next((j for j,x in enumerate(d) if x>1e-6),None);firstfoot[q]={'original_source_patch_ON_frame1_vs_OFF_max_XY_displacement_m':float(np.linalg.norm(vv[0,patch,:2]-neutral[patchid,:2],axis=1).max()),'first_ON_anchored_displacement_over1micron_frame':None if ii is None else ii+1,'first_ON_anchored_displacement_m':None if ii is None else float(d[ii]),'first_adjacent_original_patch_step_m':float(step[0]),'whole_mask_proximity3mm_not_force':True}
ln=SitStandLane();ln.on()
for f in sorted(set([firstrow['frame'],40,worstrow['frame']])):
 s.frame_set(f);bpy.context.view_layer.update();a=author[f];src={n:Matrix(v) for n,v in intake['samples_private'][a['source_action']][a['source_local_frame']-1].items()};records={}
 for n in ['pelvis','thigh.L','thigh.R','shin.L','shin.R','upper_arm.L','upper_arm.R']:
  sn=m['mapping'][n];ref=source_first[sn] if n.startswith('upper_arm') else source_rest[sn];expected=(C@src[sn].to_quaternion()@ref.to_quaternion().inverted()@C.inverted())@offworld[n].to_quaternion();actual=(r.matrix_world@r.pose.bones[n].matrix).to_quaternion();ang=expected.rotation_difference(actual).angle;parent=intake['bones'][sn]['parent'];relrest=source_rest[parent].inverted()@source_rest[sn] if parent else source_rest[sn];relpose=src[parent].inverted()@src[sn] if parent else src[sn];donorlocal=relrest.to_quaternion().inverted()@relpose.to_quaternion();da=donorlocal.angle;ta=r.pose.bones[n].rotation_quaternion.angle
  records[n]={'intended_world_rotation_goal_error_degrees':math.degrees(min(ang,2*math.pi-ang)),'donor_local_delta_anatomical_rest_shortest_degrees':math.degrees(min(da,2*math.pi-da)),'target_local_quaternion_shortest_degrees':math.degrees(min(ta,2*math.pi-ta)),'upper_reference_is_different_common_standing_neutral':n.startswith('upper_arm')}
 source_knees={}
 for q,u in [('L','l'),('R','r')]:
  aa=np.array(src['thigh_'+u].translation)-np.array(src['calf_'+u].translation);bb=np.array(src['foot_'+u].translation)-np.array(src['calf_'+u].translation);source_knees[q]=180-math.degrees(math.acos(float(np.clip(np.dot(aa,bb)/(np.linalg.norm(aa)*np.linalg.norm(bb)),-1,1))))
 compare.append({'frame':f,'source_action':a['source_action'],'source_local_frame':a['source_local_frame'],'joint_comparison':records,'donor_knee_flexion_degrees':source_knees})
ln.off();assert snapshot(names)==before
print('SIT_FIRST_WORST_CAUSAL_RECORD',localization,firstfoot,compare,flush=True)
cache=json.loads((B/'SIT_STAND_VALID_EXISTING_CAPTURE_R1.json').read_bytes());validcache={(x['view'],x['frame']):x for x in cache['valid']}
ln=SitStandLane();ln.on();rom={n:[] for n in offs};knees={q:[] for q in ['L','R']}
for f in range(1,122):
 s.frame_set(f);bpy.context.view_layer.update()
 for n in rom:
  ang=offs[n].rotation_difference(r.pose.bones[n].rotation_quaternion).angle;rom[n].append(math.degrees(min(ang,2*math.pi-ang)))
 j=m['rows_private'][f-1]['joint_world_private']
 for q in knees:
  a=np.array(j['thigh.'+q])-np.array(j['shin.'+q]);b=np.array(j['foot.'+q])-np.array(j['shin.'+q]);knees[q].append(180-math.degrees(math.acos(float(np.clip(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)),-1,1)))))
ln.off();assert snapshot(names)==before
# Reuse every valid existing completed native JPG byte-exact; preserve corrupted/partial originals, never overwrite first job.
cam=s.camera;savecam=(cam.location.copy(),cam.rotation_euler.copy(),cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width);changes=[(s.render,'engine','CYCLES'),(s.cycles,'device','CPU'),(s.cycles,'samples',2),(s.cycles,'seed',0),(s.cycles,'use_animated_seed',False),(s.cycles,'use_denoising',False),(s.render,'threads_mode','FIXED'),(s.render,'threads',2),(s.render,'resolution_x',384),(s.render,'resolution_y',384),(s.render,'resolution_percentage',100),(s.render.image_settings,'file_format','JPEG'),(s.render.image_settings,'color_mode','RGB'),(s.render.image_settings,'color_depth','8'),(s.render.image_settings,'quality',92),(s.render,'filepath','')];saves=[(ob,k,getattr(ob,k)) for ob,k,_ in changes]
for ob,k,v in changes:setattr(ob,k,v)
ln=SitStandLane();ln.on();custody=[];views={};newframes=0;reused=0
for view,direction in [('front',(0,-1,0)),('quarter',(.6,-1,0)),('side',(1,0,0))]:
 folder=O/view;folder.mkdir();target=Vector((.002,.02,.48));cam.data.type='ORTHO';cam.data.ortho_scale=1.18;cam.location=target+Vector(direction).normalized()*.8;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();views[view]={'type':'ORTHO','ortho_scale':1.18,'target':list(target),'location':list(cam.location),'rotation_euler':list(cam.rotation_euler),'resolution':[384,384],'fps':30,'frames':[1,121],'fixed':True}
 for f in range(1,122):
  old=P/view/f'{f:04}.jpg';out=folder/f'{f:04}.jpg';valid=(view,f) in validcache
  if valid:assert sha(old)==validcache[(view,f)]['sha256']
  if valid:shutil.copyfile(old,out);assert sha(old)==sha(out);reused+=1;custody.append({'view':view,'frame':f,'reused_existing_native_SHA':sha(old),'original_file':str(old),'unchanged':True})
  else:s.frame_set(f);bpy.context.view_layer.update();s.render.filepath=str(out);bpy.ops.render.render(write_still=True);newframes+=1;custody.append({'view':view,'frame':f,'new_native_SHA':sha(out),'original_partial_preserved':old.exists()})
ln.off();cam.location,cam.rotation_euler,cam.data.type,cam.data.ortho_scale,cam.data.lens,cam.data.sensor_width=savecam;s.render.resolution_x=960;s.render.resolution_y=920;s.cycles.samples=8;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(O/'SIT_STAND_OFF_SOURCE_NEUTRAL_R1.png');bpy.ops.render.render(write_still=True)
for ob,k,v in saves:setattr(ob,k,v)
assert snapshot(names)==before and sha(m['source'])==m['source_SHA'] and sha(m['candidate'])==m['candidate_SHA'] and sha(m['library']['file'])==m['library']['sha256'] and sha(m['FBX_source'])==m['FBX_SHA'];receipt={'same_candidate_SHA':m['candidate_SHA'],'source78_fresh_serialized_fullraw_OFF_equal_before_after':True,'all363_native_capture_complete':True,'source_baseline_rerendered':False,'first_job_failure_guard_SHA':sha(B/'o1-sit-stand-source-candidate-r1b/NATIVE_GUARD_RESULT.json'),'same_candidate_no_motion_rerun':'Authoring and all121fullmesh/contact/sole measurements NOT repeated; render-only missing capture completion plus corrected narrow ROM/worst-pair localization. Original candidate bytes untouched.','reused_native_images':reused,'new_native_images':newframes,'views':views,'shortest_local_quaternion_delta_vs_original_OFF_degrees':{n:[min(v),max(v)] for n,v in rom.items()},'anatomical_knee_flexion_from_actual_world_joints_degrees':{q:[min(v),max(v)] for q,v in knees.items()},'body_failure_localization':localization,'first_original_support_displacement':firstfoot,'donor_target_actual_joint_comparison':compare,'fresh_OFF_restored_after_capture':True};(O/'SIT_STAND_CAPTURE_COMPLETION_R1.json').write_text(json.dumps(receipt,indent=2),encoding='utf8');(O/'NATIVE_FRAME_REUSE_CUSTODY_R1.json').write_text(json.dumps(custody,indent=2),encoding='utf8');print('SAME_CANDIDATE_CAPTURE_COMPLETED',reused,newframes,localization,flush=True)
