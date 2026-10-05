"""Exact local4.04sec original/corrected exposed-elbow 1x proof and custody."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image,ImageDraw
import numpy as np
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-tour302-delivery-r1';O.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();m=json.loads((B/'alpha-tour302-elbow-c1d/TOUR302_ELBOW_C1_PRIVATE.json').read_bytes());guard=json.loads((B/'o1-tour302-elbow-c1d/NATIVE_GUARD_RESULT.json').read_bytes());assert guard['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN';movies=[];captures=[]
def verify(p):
 subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(p),'-f','null','-'],check=True);j=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(p)]));st=j['streams'][0];assert int(st['nb_read_frames'])==97 and st['avg_frame_rate']=='24/1';return {'file':str(p),'SHA':sha(p),'bytes':p.stat().st_size,'frames':97,'fps':24,'duration_seconds':float(st['duration']),'whole_decode':'PASS','source_frames':[289,385],'native_time_scale':1}
for view in ['front','quarter']:
 R=B/f'alpha-tour302-capture-{view}-r1';G=B/f'o1-tour302-capture-{view}-r1/NATIVE_GUARD_RESULT.json';g=json.loads(G.read_bytes());assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN';c=json.loads((R/'TOUR302_CAPTURE_PRIVATE_R1.json').read_bytes());assert c['candidate_SHA']==m['candidate_SHA'] and len(c['rows_private'])==194
 for row in c['rows_private']:assert sha(R/row['mode']/f'{row["ordinal"]:04}.png')==row['file_SHA']
 for mode in ['ORIGINAL','CORRECTED']:
  out=O/f'{view}_{mode}_LOCAL97_24FPS_1x.mp4';subprocess.run(['ffmpeg','-v','error','-framerate','24','-i',str(R/mode/'%04d.png'),'-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-threads','2','-filter_threads','2','-n',str(out)],check=True);movies.append(verify(out))
 pair=O/f'{view}_MATCHED_ORIGINAL_LEFT_CORRECTED_RIGHT_1x.mp4';subprocess.run(['ffmpeg','-v','error','-i',str(O/f'{view}_ORIGINAL_LOCAL97_24FPS_1x.mp4'),'-i',str(O/f'{view}_CORRECTED_LOCAL97_24FPS_1x.mp4'),'-filter_complex','[0:v][1:v]hstack=inputs=2[v]','-map','[v]','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-threads','2','-filter_complex_threads','1','-n',str(pair)],check=True);movies.append(verify(pair));captures.append({'view':view,'guard_SHA':sha(G),'same_candidate_SHA':c['candidate_SHA'],'actual_all194_frame_geometry_matching':True,'source81_OFF_restored':True})
 baseline=np.array(Image.open(B/'alpha-a1-contact-qa-r3/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png').convert('RGBA'));off=np.array(Image.open(R/'OFF_SOURCE_CAMERA_NEUTRAL.png').convert('RGBA'));assert np.array_equal(baseline,off)
 for f in [302,337,371]:
  ordinal=f-288;grid=Image.new('RGB',(768,410),'white');dr=ImageDraw.Draw(grid)
  for col,mode in enumerate(['ORIGINAL','CORRECTED']):grid.paste(Image.open(R/mode/f'{ordinal:04}.png').convert('RGB'),(col*384,26));dr.text((col*384+5,5),f'{view} f{f} {mode} native24fps SAME CAMERA',fill='black')
  grid.save(O/f'MATCHED_{view}_f{f}_R1.jpg',quality=96)
(O/'VIDEO_CUSTODY_R1.json').write_text(json.dumps({'candidate_SHA':m['candidate_SHA'],'movies':movies,'captures':captures,'OFF_RGBA_unequal_channels_each_view':0,'local_pose_data_gate':m['scoped_local_QA_pass'],'whole_Tour':'HOLD wrists472 untouched; source supply packet absent'},indent=2),encoding='utf8')
html='<!doctype html><meta charset="utf-8"><title>R4 Tour left elbow local correction C1</title><style>body{background:#222;color:#eee;font:16px system-ui}video{width:49%}section{display:flex;gap:8px}button{padding:12px;font-size:20px}</style><h1>Tour · left elbow C1 · local 1x comparison</h1><p>LEFT original / RIGHT corrective Action-copy. Original frames289–385 @24fps, 4.041667sec. Same fixed exposed-elbow front/quarter cameras. One forearm.L local-Z amplitude change; original clock, other local joints, immutable R4 appearance preserved. This deliberately changes the original pose. Whole Tour stays HOLD: wrists472 and original head/hair contacts untouched. No Unity/TierP/F2/StageB acceptance or source packet.</p><button onclick="document.querySelectorAll(\'video\').forEach(v=>{v.currentTime=0;v.playbackRate=1;v.play()})">Play both matched phrases at native 1x</button><section>'
for v in ['front','quarter']:html+=f'<video controls preload="auto" src="{v}_MATCHED_ORIGINAL_LEFT_CORRECTED_RIGHT_1x.mp4"></video>'
html+='</section><p>Original and corrective both start/end at the same native boundaries. Fixed source material/lighting, CPU8samples; internal triangle penetration depth is evaluated by geometry QA, not shading.</p>'
(O/'REVIEW_TOUR302_LOCAL_C1.html').write_text(html,encoding='utf8');print('TOUR302_LOCAL_MATCHED_NATIVE1X_FULL_DECODE_OFF_PASS')
