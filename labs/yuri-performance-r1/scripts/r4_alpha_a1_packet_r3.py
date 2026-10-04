"""Existing A1 candidate/evidence custody only; private binaries never enter Git."""
import json,hashlib,zipfile,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
LAB=Path(__file__).resolve().parents[1]
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
OUT=BASE/'alpha-a1-idle-candidate-r3';E=LAB/'evidence/alpha-a1-idle-candidate-r3'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):
    with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2,ensure_ascii=False)
E.mkdir(exist_ok=False)
r=json.loads((OUT/'A1_RETARGET_RECEIPT_PRIVATE_R1.json').read_bytes())
qa=json.loads((BASE/'alpha-a1-contact-qa-r3/A1_CONTACT_QA_PRIVATE_R3.json').read_bytes())
source=LAB/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend';assert sha(source)==r['source_SHA']
assert sha(Path(r['candidate']))==r['candidate_SHA']
baseline=BASE/'r4-appearance-preserve-correction-r1/neutral/authority_source_camera_before.png'
off=BASE/'alpha-a1-contact-qa-r3/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png'
assert np.array_equal(np.array(Image.open(baseline)),np.array(Image.open(off)))
movies={}
for view in ['front','quarter','side']:
    p=OUT/f'A1_Female_Idle_{view}_1x.mp4'
    meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_frames,duration','-of','json',str(p)]))['streams'][0]
    assert meta['nb_frames']=='301' and meta['r_frame_rate']=='30/1'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(p),'-f','null','-'],check=True)
    movies[view]={'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size,**meta,'whole_decode':True,'observed_UI_ended':True,'observed_UI_playback_rate':1,'observed_UI_media_error':None}
guards=[]
for directory in sorted(BASE.glob('alpha-a1-*-broker-r*')):
    p=directory/'NATIVE_GUARD_RESULT.json'
    if not p.exists():continue
    g=json.loads(p.read_bytes());guards.append({'path':str(p),'SHA':sha(p),'status':g['guard_status'],'pid':g.get('pid'),'wall_seconds':g.get('wall_seconds'),'terminal_exit':g.get('terminal_exit_code'),'terminal_job':g.get('terminal_job')})
public={'task':'ROOT_PM_ALPHA_SOURCE_FIRST_IDLE_CANDIDATE_R1','candidate_scope':'A1 body-only R4 Blender candidate; not Unity/Product/PRIMARY acceptance',
    'source_SHA':r['source_SHA'],'donor_SHA':r['donor_SHA'],'candidate_path':r['candidate'],'candidate_SHA':r['candidate_SHA'],'candidate_bytes':r['candidate_bytes'],
    'action':r['action'],'mapped_bones':51,'original_body_rig':'Meshy_Fitted_Rig57','original_actions_preserved':78,'additive_candidate_actions':2,
    'frame_range':[1,301],'action_source_fps_embedded':30,'source_scene_fps_preserved':24,'preview_fps':30,'duration_key_interval_sec':10,'duration_movie_sec':10.033333,
    'root_policy':r['root_policy'],'floor_cleanup_world_z_m':r['floor_cleanup_world_z_m'],
    'OFF_full_signature_exact_R2':True,'OFF_full_signature_exact_R3_copy':True,'reopened_OFF_neutral_pixel_exact':True,'OFF_max_pixel_difference':0,
    'root_world_range_m':qa['root_world_range_m'],'soles':qa['soles'],'hand_trajectory_range_m':qa['hand_trajectory_range_m'],'evaluated_body_finite_all301_frames':True,
    'normal_speed_front_quarter_side':'COMPLETE_1X_ENDED_NO_MEDIA_ERROR','movies':movies,'guard_execution_receipts':guards,
    'remaining_defects':['left sole up to1.18mm above source neutral floor; right up to0.121mm','No external floor/collider/contact-physics certification or exhaustive mesh-self-intersection proof','Static original face/gaze; no F2/F3 performance acceptance','Source scene remains24fps; explicit30fps body Action/preview context required','Mixamo non-loop source; no fabricated loop seam acceptance'],
    'failed_approaches_preserved':['R1 bake used last toe donor channel for pelvis location; neutral structure preserved but ON pelvis collapsed ~0.5m','First preview wrapper import path absent failed before render; R2 wrapper fixed separate','R2 sole float4.8-6.0mm; R3 copied Action constant pelvisZ cleanup'],
    'TierP':0,'StageB_accepted':False,'O1_accepted':False,'PRIMARY':False,'Unity_writes':0,'source_writes':0,'face_gaze_hair_channel_writes':0,
    'next':'Autonomously inspect/adapt A2-A4 within same scope; final promotion stays with PM',
    'forensic_target':'A1 pelvis/sole contact only','first_divergence':'R1 pelvis.location donor channel','cause_status':'PROVEN scoped channel bug; sole gap measured and corrected','oracle':'original OFF signature/pixels; actual301frame native geometry/root/sole;3 full1x videos; exact live owned execution guard','implementation':'single donor-channel reference correction and one constant copied-Action pelvisZ adjustment','KB_reuse':'small rest-axis/channel-ownership note; no new forensic framework'}
dump(E/'A1_CANDIDATE_PUBLIC_RECEIPT_R3.json',public)
files=[(p,'candidate/'+p.name) for p in sorted(OUT.iterdir()) if p.is_file()]
for dirname in ['alpha-a1-idle-inspect-r1','alpha-a1-idle-candidate-r1','alpha-a1-idle-candidate-r2','alpha-a1-contact-qa-r2','alpha-a1-contact-qa-r3','alpha-a1-pose-diagnostic-r1']:
    directory=BASE/dirname
    files.extend((p,'private-evidence/'+dirname+'/'+p.name) for p in directory.glob('*.json'))
files.extend([(off,'private-evidence/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png'),(baseline,'private-evidence/authority_source_camera_before.png')])
for directory in sorted(BASE.glob('alpha-a1-*-broker-r*')):
    files.extend((p,'execution/'+directory.name+'/'+str(p.relative_to(directory)).replace('\\','/')) for p in directory.rglob('*') if p.is_file())
for view in ['front','quarter','side']:
    p=BASE/('alpha-a1-idle-preview-'+view+'-r3/RENDER_RECEIPT.json');files.append((p,'execution/'+view+'_RENDER_RECEIPT.json'))
files.extend((p,'workflow/'+p.name) for p in sorted((LAB/'scripts').glob('r4_alpha_a1*.py')))
for name in ['r4_appearance_adapter.py','r4_appearance_signature.py','native_preservation.py','r4_alpha_owned_job_prepare_r1.py']:
    p=LAB/'scripts'/name;files.append((p,'workflow/'+name))
files.append((E/'A1_CANDIDATE_PUBLIC_RECEIPT_R3.json','A1_CANDIDATE_PUBLIC_RECEIPT_R3.json'))
packet=BASE/'YURI_R4_A1_FEMALE_IDLE_BODY_CANDIDATE_R3_20261004.zip'
index={name:{'bytes':p.stat().st_size,'SHA256':sha(p)} for p,name in files}
assert len(index)==len(files)
with zipfile.ZipFile(packet,'x',zipfile.ZIP_DEFLATED) as z:
    for p,name in files:z.write(p,name)
    z.writestr('FILE_INDEX.json',json.dumps(index,indent=2))
with zipfile.ZipFile(packet) as z:
    assert z.testzip() is None
    for name,row in index.items():assert hashlib.sha256(z.read(name)).hexdigest()==row['SHA256']
dump(E/'PRIVATE_PACKET_RECEIPT_R3.json',{'path':str(packet),'SHA256':sha(packet),'bytes':packet.stat().st_size,'members':len(index)+1,'all_member_SHA_CRC_verified':True,'raw_source_or_donor_FBX_included':False,'license':'Private project-use retarget candidate; no public raw Mixamo redistribution'})
print('A1_PACKET',sha(packet),packet.stat().st_size,len(index)+1)
