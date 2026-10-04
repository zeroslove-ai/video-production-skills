"""Offline native head visual comparison packaging preparation; no model changes."""
from pathlib import Path
import json,hashlib,subprocess
import numpy as np
from PIL import Image,ImageDraw
LAB=Path(__file__).resolve().parents[1];B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');P=B/'alpha-native-head-visual-source-r1';D=B/'alpha-native-head-visual-delivery-r1';E=LAB/'evidence/native-head-visual-source-r1'
D.mkdir(exist_ok=False);E.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();js=lambda p:json.loads(Path(p).read_bytes())
m=js(P/'NATIVE_HEAD_VISUAL_SOURCE_PRIVATE_R1.json');g=js(B/'o1-native-head-visual-source-r1/NATIVE_GUARD_RESULT.json');assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN' and g['terminal_job']['active']==0 and m['all97_both_views_complete'] and m['full_raw_OFF_snapshot_equal']
aa=np.asarray(Image.open(B/'alpha-a1-contact-qa-r3/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png').convert('RGBA'));bb=np.asarray(Image.open(P/'NATIVE_HEAD_VISUAL_OFF_SOURCE_NEUTRAL_R1.png').convert('RGBA'));assert np.array_equal(aa,bb)
pixel={'changed_pixels':0,'max_RGBA_delta':0,'dimensions':list(aa.shape),'decoded_RGBA_exact':True};(D/'OFF_PIXEL_QA_R1.json').write_text(json.dumps(pixel,indent=2),encoding='utf8')
movies=[]
for view in m['views']:
 assert len(list((P/view).glob('*.png')))==97
 out=D/f'{view}_NATIVE_HEAD_FULL97_24FPS_1x.mp4';subprocess.run(['ffmpeg','-v','error','-framerate','24','-start_number','1','-i',str(P/view/'%04d.png'),'-frames:v','97','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-threads','2','-n',str(out)],check=True);subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(out),'-f','null','-'],check=True)
 q=js_probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(out)]))['streams'][0];assert int(q['nb_read_frames'])==97 and q['avg_frame_rate']=='24/1'
 movies.append({'file':str(out),'sha256':sha(out),'frames':97,'fps':24,'duration':float(q['duration']),'speed_factor':1,'whole_decode':'PASS','view':view})
 grid=Image.new('RGB',(256*8,280*13),'white');dr=ImageDraw.Draw(grid)
 for i,f in enumerate(range(1,98)):
  x=i%8*256;y=i//8*280;grid.paste(Image.open(P/view/f'{f:04}.png').resize((256,256)),(x,y+24));dr.text((x+4,y+3),f'{view} f{f} {(f-1)/24:.3f}s',fill='black')
 grid.save(D/f'ALL97_{view}_R1.jpg',quality=94)
frames=[1,13,25,37,49,61,73,85,97];grid=Image.new('RGB',(384*len(frames),408*2),'white');dr=ImageDraw.Draw(grid)
for row,view in enumerate(m['views']):
 for i,f in enumerate(frames):grid.paste(Image.open(P/view/f'{f:04}.png').convert('RGB'),(i*384,row*408+24));dr.text((i*384+3,row*408+3),f'{view} f{f} {(f-1)/24:.3f}s',fill='black')
grid.save(D/'MATCHED_HEAD_NECK_REFERENCE_R1.jpg',quality=94)
ranges={k:[min(r['morph_values'][k] for r in m['rows_private']),max(r['morph_values'][k] for r in m['rows_private'])] for k in m['neutral_morph_values']};assert all(a==b for a,b in ranges.values())
scalar={k:m[k] for k in ['task','source_SHA','existing_action','action_signature_SHA','slot','all_original_curve_RNA_compatible_targets','target_binding','curve_count','range','source_fps','source_fps_base','endpoint_span_seconds','encoded_duration_seconds','speed_factor','source78_preserved','no_additive_transport_no_FACE_GAZE_HAIR_action_assignment','scope','max_actual_mesh_displacement_vs_OFF_m','views','all97_both_views_complete','full_raw_OFF_snapshot_equal','source_bytes_unchanged','collector_elapsed_seconds','TierP']};scalar['morph_values_change_count']=0;scalar['morph_value_count']=len(ranges);scalar['OFF_pixels']=pixel;scalar['guard_sha256']=sha(B/'o1-native-head-visual-source-r1/NATIVE_GUARD_RESULT.json');scalar['visual']='PENDING_ACTUAL_REVIEW';scalar['auxiliary_face_gaze_hair_original_actions_not_exercised']=True
(E/'NATIVE_HEAD_VISUAL_SCALAR_QA_R1.json').write_text(json.dumps(scalar,indent=2),encoding='utf8');(D/'VIDEO_CUSTODY_R1.json').write_text(json.dumps(movies,indent=2),encoding='utf8')
# Private matched frames preserve exact morph values, source camera/view, mesh fingerprints and original Action authority.
refs={'source_SHA':m['source_SHA'],'action':m['existing_action'],'action_signature_SHA':m['action_signature_SHA'],'target':'Meshy_Fitted_Rig','slot':m['slot'],'fps':24,'source_signature':m['original_source_signature'],'views':m['views'],'frames':[m['rows_private'][f-1]|{'images':{view:{'file':str(P/view/f'{f:04}.png'),'sha256':sha(P/view/f'{f:04}.png')} for view in m['views']}} for f in frames],'limit':'Static morph values; native BODY action only. No native FACE KEY/GAZE/HAIR take or Unity runtime acceptance.'};(D/'LAPTOP_MATCHED_SOURCE_REFERENCE_PRIVATE_R1.json').write_text(json.dumps(refs,indent=2),encoding='utf8')
html='<!doctype html><meta charset="utf-8"><title>Original R4 native head visual reference</title><style>body{background:#222;color:#eee;font:16px system-ui}section{display:flex}video{width:48%}button{padding:12px}</style><h1>R4 immutable source · native BODY_HeadGazeHair</h1><p>Full frames1–97 / original24fps /1x. Head/eye/hair assembly moves; all72 morph values static. Original shader/texture/weights/drivers/rest unchanged. BODY take only; auxiliary FACE/GAZE/HAIR Actions not assigned. No Unity/F2/TierP approval.</p><button onclick="document.querySelectorAll(\'video\').forEach(v=>{v.currentTime=0;v.playbackRate=1;v.play()})">Play original native head front and side at 1x</button><section>'
for x in movies:html+=f'<video controls preload="auto" src="{Path(x["file"]).name}"></video>'
html+='</section><p>Fixed front/positiveX-side orthographic head-neck view,384×384 CPU8samples. Hair pearl gray-white is already present in canonical Blender shader, not a new candidate substitution. Morph-motion shader stability remains untested.</p>'
(D/'REVIEW_NATIVE_HEAD_VISUAL_R1.html').write_text(html,encoding='utf8');print(json.dumps({'movies':movies,'OFF':pixel,'morph_change_count':0},indent=2))
