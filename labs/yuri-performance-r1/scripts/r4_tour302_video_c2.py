from pathlib import Path
import json,hashlib,subprocess
from PIL import Image,ImageDraw
import numpy as np
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'alpha-tour302-delivery-c2';O.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
m=json.loads((B/'alpha-tour302-softcap-c2/TOUR302_SOFTCAP_C2_PRIVATE.json').read_bytes());old=json.loads((B/'alpha-tour302-delivery-r1/VIDEO_CUSTODY_R1.json').read_bytes());movies=[];reuse=[];captures=[]
def verify(p):
 subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(p),'-f','null','-'],check=True)
 st=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(p)]))['streams'][0];assert int(st['nb_read_frames'])==97 and st['avg_frame_rate']=='24/1'
 return {'file':str(p),'SHA':sha(p),'bytes':p.stat().st_size,'frames':97,'fps':24,'duration_seconds':float(st['duration']),'whole_decode':'PASS','native_time_scale':1}
for view in ['front','quarter']:
 R=B/f'alpha-tour302-capture-{view}-c2';R1=B/f'alpha-tour302-capture-{view}-r1';G=B/f'o1-tour302-capture-{view}-c2/NATIVE_GUARD_RESULT.json';assert json.loads(G.read_bytes())['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN'
 c=json.loads((R/'TOUR302_CAPTURE_PRIVATE_C2.json').read_bytes());c1=json.loads((R1/'TOUR302_CAPTURE_PRIVATE_R1.json').read_bytes());assert c['camera']==c1['camera'] and c['candidate_SHA']==m['candidate_SHA'] and len(c['rows_private'])==97 and c['source81_OFF_restored']
 for x in c['rows_private']:assert sha(R/x['mode']/f'{x["ordinal"]:04}.png')==x['file_SHA'] and x['actual_geometry_matches_local_oracle']
 inputs=[]
 for mode in ['ORIGINAL','CORRECTED']:
  p=B/'alpha-tour302-delivery-r1'/f'{view}_{mode}_LOCAL97_24FPS_1x.mp4';expected=next(x for x in old['movies'] if x['file']==str(p));assert sha(p)==expected['SHA'];reuse.append(verify(p));inputs.append(p)
 out=O/f'{view}_C2_LOCAL97_24FPS_1x.mp4';subprocess.run(['ffmpeg','-v','error','-framerate','24','-i',str(R/'C2/%04d.png'),'-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-threads','2','-n',str(out)],check=True);movies.append(verify(out));inputs.append(out)
 pair=O/f'{view}_MATCHED_ORIGINAL_C1_C2_NATIVE1x.mp4';args=['ffmpeg','-v','error']
 for p in inputs:args+=['-i',str(p)]
 args+=['-filter_complex','[0:v][1:v][2:v]hstack=inputs=3[v]','-map','[v]','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-threads','2','-filter_complex_threads','1','-n',str(pair)];subprocess.run(args,check=True);movies.append(verify(pair))
 assert np.array_equal(np.array(Image.open(R/'OFF_SOURCE_CAMERA_NEUTRAL.png').convert('RGBA')),np.array(Image.open(B/'alpha-a1-contact-qa-r3/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png').convert('RGBA')))
 for f in [298,300,302,337,372,375]:
  grid=Image.new('RGB',(1152,410),'white');dr=ImageDraw.Draw(grid)
  for col,(root,mode,label) in enumerate([(R1,'ORIGINAL','SOURCE'),(R1,'CORRECTED','C1'),(R,'C2','C2')]):
   grid.paste(Image.open(root/mode/f'{f-288:04}.png').convert('RGB'),(col*384,26));dr.text((col*384+5,5),f'{view} f{f} {label} SAME CAMERA native24fps',fill='black')
  grid.save(O/f'MATCHED_{view}_f{f}_C2.jpg',quality=96)
 captures.append({'view':view,'guard_SHA':sha(G),'camera_matches_original_C1':True,'all97_actual_geometry_matching':True,'OFF_RGBA_unequal_channels':0})
(O/'VIDEO_CUSTODY_C2.json').write_text(json.dumps({'candidate_SHA':m['candidate_SHA'],'movies':movies,'reused_original_C1_movies':reuse,'captures':captures,'whole_Tour':'HOLD','scoped_local_QA_pass':False},indent=2),encoding='utf8')
html='<!doctype html><meta charset="utf-8"><title>R4 Tour C2 source motion comparison</title><style>body{background:#222;color:#eee;font:16px system-ui;margin:20px}video{width:100%;max-width:1152px}button{padding:12px;font-size:18px}</style><h1>R4 Tour C2 · local 1x comparison</h1><p>LEFT source / CENTER C1 / RIGHT C2. Frames289–385 @24fps: 4.041667sec. Original and C1 captures reused; C2 alone freshly rendered with exactly matching cameras.</p><p>C2 preserves 17 small-bend keys and reduces mean hand deviation: 33.00 → 28.99mm. Peak deviation remains41.99mm. This changes the source motion, while preserving immutable R4 appearance and source81 Actions.</p><p>HOLD: unchanged clavicle contact f303..370 and whole-Tour wrist/head/hair contacts. No source PASS, source packet, Unity, F2, StageB or TierP acceptance.</p><button onclick="document.querySelectorAll(\'video\').forEach(v=>{v.currentTime=0;v.playbackRate=1;v.play()})">Play both views at native 1x</button>'
for v in ['front','quarter']:html+=f'<p>{v}: SOURCE / C1 / C2</p><video controls preload="auto" src="{v}_MATCHED_ORIGINAL_C1_C2_NATIVE1x.mp4"></video>'
(O/'REVIEW_TOUR302_SOFTCAP_C2.html').write_text(html,encoding='utf8');print('C2_MATCHED_THREE_WAY_FULL_DECODE_OFF_PASS')
