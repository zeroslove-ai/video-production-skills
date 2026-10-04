"""Fixed A2-A4 grounded-idle support-floor QA/Action copy. No framework/export."""
import bpy,sys,json,hashlib,numpy as np
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_adapter import ReactionLane
from r4_appearance_signature import snapshot
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(step):
    assert step in ['a2','a3','a4']
    OUT=BASE/('alpha-'+step+'-contact-candidate-r2');OUT.mkdir(exist_ok=False)
    prior=json.loads((BASE/('alpha-'+step+'-candidate-r1')/(step.upper()+'_RETARGET_RECEIPT_PRIVATE_R1.json')).read_bytes())
    SOURCE=Path(prior['candidate']);assert sha(SOURCE)==prior['candidate_SHA']
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False);s=bpy.context.scene;r=bpy.data.objects['Meshy_Fitted_Rig'];body=bpy.data.objects['Meshy_Body_NeutralCovered'];names=[a.name for a in bpy.data.actions];before=snapshot(names)
    def points():
        e=body.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();buf=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',buf);world=np.array(e.matrix_world,dtype=np.float64);v=buf.reshape(-1,3).astype(np.float64)@world[:3,:3].T+world[:3,3];e.to_mesh_clear();return v
    baseline=points();floor=float(baseline[:,2].min());ids={side:np.where((baseline[:,2]<floor+.028)&((baseline[:,0]>.00195) if side=='L' else (baseline[:,0]<.00195)))[0] for side in ['L','R']};assert all(len(v)>10 for v in ids.values())
    original_scene_fps=s.render.fps/s.render.fps_base
    # Source-camera neutral witness; render overrides only, then restore settings.
    render_saved=(s.render.engine,s.cycles.device,s.cycles.samples,s.cycles.seed,s.cycles.use_animated_seed,s.cycles.use_denoising,s.render.threads_mode,s.render.threads,s.render.image_settings.file_format,s.render.image_settings.color_mode,s.render.image_settings.color_depth,s.render.filepath)
    s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=8;s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.image_settings.color_depth='8';s.render.filepath=str(OUT/'CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png');bpy.ops.render.render(write_still=True)
    (s.render.engine,s.cycles.device,s.cycles.samples,s.cycles.seed,s.cycles.use_animated_seed,s.cycles.use_denoising,s.render.threads_mode,s.render.threads,s.render.image_settings.file_format,s.render.image_settings.color_mode,s.render.image_settings.color_depth,s.render.filepath)=render_saved
    bpy.data.images.remove(bpy.data.images['Render Result'])
    lane=ReactionLane();a=lane.on(prior['action']);fps=float(a['source_fps']);assert fps==30 and original_scene_fps==24
    count=prior['frames'][1];support_offsets=[];raw_min=[]
    for f in range(1,count+1):
        s.frame_set(f);bpy.context.view_layer.update();v=points();assert v.shape==baseline.shape and np.isfinite(v).all()
        offsets={side:float(v[index,2].min()-floor) for side,index in ids.items()};support_offsets.append(min(offsets.values()));raw_min.append(offsets)
        if f%600==0:print('GROUND_REFERENCE',step,f,count,flush=True)
    lane.off()
    # Grounded idle/weight-shift only. Correct support sole height; do NOT horizontal-lock intentional steps.
    assert max(abs(x) for x in support_offsets)<.15,'Support correction too large for bounded idle adaptation'
    clean=a.copy();clean.name='YURI_R4_'+step.upper()+'_BODY_CANDIDATE_R2';clean.use_fake_user=True;clean['source_fps']=fps;clean['original_BVH_fps']=a['original_BVH_fps'];clean['root_policy']='Original root fixed; donor normalized pelvis first-frame displacement; per-frame grounded support-sole Z correction only; intentional horizontal motion retained';clean['loop_authored']=False
    pelvis=r.data.bones['pelvis'];vector=pelvis.matrix_local.to_quaternion().inverted()@r.matrix_world.to_quaternion().inverted()@Vector((0,0,1))/r.matrix_world.to_scale().x
    changed=0
    for layer in clean.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    if fc.data_path=='pose.bones["pelvis"].location':
                        assert len(fc.keyframe_points)==count
                        for k in fc.keyframe_points:
                            frame=round(k.co.x);delta=-support_offsets[frame-1]*vector[fc.array_index]
                            k.co.y+=delta;k.handle_left.y+=delta;k.handle_right.y+=delta
                        fc.update();changed+=1
    assert changed==3
    frames=[];roots=[];max_step=0;previous=None
    lane.on(clean.name)
    for f in range(1,count+1):
        s.frame_set(f);bpy.context.view_layer.update();v=points();assert np.isfinite(v).all()
        joint={n:list((r.matrix_world@r.pose.bones[n].matrix).translation) for n in ['root','pelvis','hand.L','hand.R','foot.L','foot.R','head']}
        if previous:max_step=max(max_step,max((Vector(joint[n])-Vector(previous[n])).length for n in joint))
        previous=joint;roots.append(joint['root'])
        frames.append({'frame':f,'soles':{side:{'offset_m':float(v[index,2].min()-floor),'centroid':v[index].mean(0).tolist()} for side,index in ids.items()},'body_min_z_offset_m':float(v[:,2].min()-floor),'joints':joint})
        if f%600==0:print('GROUND_CLEAN_QA',step,f,count,flush=True)
    lane.off();assert before==snapshot(names),'Existing source/candidate bindings, original actions or OFF structure changed'
    dest=OUT/('Character_R4_'+step.upper()+'_BODY_CANDIDATE_OFF_R2_20261004.blend');bpy.ops.wm.save_as_mainfile(filepath=str(dest))
    original=HERE.parent/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend';assert sha(original)==prior['source_SHA']
    receipt={'step':step,'source_SHA':prior['source_SHA'],'donor_SHA':prior['donor_SHA'],'previous_candidate_SHA':prior['candidate_SHA'],'previous_candidate_preserved':str(SOURCE),'candidate':str(dest),'candidate_SHA':sha(dest),'candidate_bytes':dest.stat().st_size,'action':clean.name,'mapped_bones':21,'frame_range':[1,count],'action_source_fps_readback':fps,'source_scene_fps_readback':original_scene_fps,'original_BVH_fps_readback':float(clean['original_BVH_fps']),'key_interval_sec':(count-1)/fps,'original_actions_and_OFF_snapshot_exact':True,'face_gaze_hair_channel_writes':0,'support_z_correction_range_m':[min(support_offsets),max(support_offsets)],'raw_support_z_offsets_private':support_offsets,'raw_soles_private':raw_min,'clean_frames_private':frames,'root_range_m':np.ptp(np.array(roots),0).tolist(),'max_joint_frame_step_m':max_step,'clean_sole_offsets_m':{side:[min(row['soles'][side]['offset_m'] for row in frames),max(row['soles'][side]['offset_m'] for row in frames)] for side in ['L','R']},'loop_authored':False,'foot_contact_physics_certified':False,'self_intersection_certified':False,'TierP':0,'root_policy':clean['root_policy'],'consumer_export_clock':'Read Action source_fps30 / clip mapping fps30, never source scene24; actual Unity/export not performed','limits':'Support-floor correction only for grounded idle/weight-shift; no horizontal foot locking, no donated fingers/face/gaze, no jump semantics, source scene24 retained'}
    with (OUT/'CONTACT_CANDIDATE_PRIVATE_R2.json').open('x') as f:json.dump(receipt,f,indent=2)
    print('GROUNDED_BODY_CANDIDATE_SAVED',step,receipt['candidate_SHA'],receipt['candidate_bytes'],flush=True)
