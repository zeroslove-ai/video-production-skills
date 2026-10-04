"""Fixed A2-A4 source-candidate encoding, diagnostics and private custody packet."""
import argparse,hashlib,json,subprocess,zipfile,shutil
from pathlib import Path
from PIL import Image,ImageDraw
LAB=Path(__file__).resolve().parents[1]
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):
 with Path(p).open('x',encoding='utf8') as f:json.dump(d,f,indent=2,ensure_ascii=False)
def review(step):
 out=BASE/f'alpha-{step}-contact-candidate-r2';d=json.loads((out/'CONTACT_CANDIDATE_PRIVATE_R2.json').read_bytes());movies={}
 for view in ['front','quarter','side']:
  frames=BASE/f'alpha-{step}-preview-{view}-r2';r=json.loads((frames/'RENDER_RECEIPT.json').read_bytes());movie=out/f'{step.upper()}_{view}_1x.mp4'
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-framerate',str(r['preview_fps']),'-i',str(frames/'%04d.png'),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2','-n',str(movie)],check=True)
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,duration,nb_frames','-of','json',str(movie)]))['streams'][0]
  assert int(probe['nb_frames'])==r['video_frame_count'] and abs(float(probe['duration'])-r['preview_container_duration_sec'])<.001
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(movie),'-threads','2','-f','null','-'],check=True)
  movies[view]={'path':str(movie),'bytes':movie.stat().st_size,'sha256':sha(movie),**probe,'whole_decode':True,'render_receipt_sha256':sha(frames/'RENDER_RECEIPT.json')}
 grid=Image.new('RGB',(768,410),(24,24,24));draw=ImageDraw.Draw(grid)
 for i,v in enumerate(['front','quarter','side']):
  frames=BASE/f'alpha-{step}-preview-{v}-r2';r=json.loads((frames/'RENDER_RECEIPT.json').read_bytes());im=Image.open(frames/f"{(r['video_frame_count']+1)//2:04d}.png");grid.paste(im,(256*i,26));draw.text((256*i+10,8),v,fill='white')
 grid.save(out/f'{step.upper()}_MULTIVIEW_GRID_R2.png')
 title={'a2':'idle_02 (long idle)','a3':'l_aro_2_32 (look proxy, not authored listen)','a4':'wei_rl_11 (weight shift)'}[step]
 html='<meta charset="utf-8"><title>'+step.upper()+' R4 body QA</title><style>body{background:#222;color:#eee;font:16px sans-serif}video{width:30%}button{padding:14px}</style><h1>'+title+'</h1><p>Original R4 OFF preserved. Body Action 30fps; source scene 24fps. Playback 1x. '+('A2 preview samples every 4 native frames at 7.5fps; all 3608 native geometry frames separately evaluated.' if step=='a2' else 'All native frames rendered at 30fps.')+'</p><button onclick="document.querySelectorAll(`video`).forEach(v=>{v.currentTime=0;v.playbackRate=1;v.play()})">Play all three at normal speed</button><div>'+''.join('<video controls preload="auto" src="'+step.upper()+'_'+v+'_1x.mp4"></video>' for v in movies)+'</div><p>CPU 2 samples, 256x384; TierP=0 / F2-F3 / PRIMARY HOLD.</p>'
 with (out/f'REVIEW_{step.upper()}_R2.html').open('x',encoding='utf8') as f:f.write(html)
 metrics={}
 for side in ['L','R']:
  rows=d['clean_frames_private'];runs=[];run=[]
  for row in rows:
   if row['soles'][side]['offset_m']<=.002:run.append(row)
   elif run:runs.append(run);run=[]
  if run:runs.append(run)
  speed=[]
  for a,b in zip(rows,rows[1:]):
   if a['soles'][side]['offset_m']<=.002 and b['soles'][side]['offset_m']<=.002:
    aa=a['soles'][side]['centroid'];bb=b['soles'][side]['centroid'];speed.append(sum((aa[i]-bb[i])**2 for i in [0,1])**.5*30)
  longest=max(runs,key=len)
  xy=[r['soles'][side]['centroid'][:2] for r in longest]
  metrics[side]={'near_floor_threshold_m':.002,'near_floor_frames':sum(len(r) for r in runs),'near_floor_runs':len(runs),'longest_near_floor_run_frames':[longest[0]['frame'],longest[-1]['frame']],'longest_run_centroid_xy_range_m':[max(p[i] for p in xy)-min(p[i] for p in xy) for i in [0,1]],'near_floor_centroid_speed_max_mps':max(speed,default=0),'domain':'Evaluated original neutral sole vertex cohort centroid; near-floor proxy only, not authored stance/contact labels or physics. Range is not automatic sliding FAIL.'}
 write(out/'ENCODE_AND_CONTACT_PROXY_RECEIPT_R1.json',{'movies':movies,'contact_proxy':metrics,'body_min_z_offset_min_m':min(r['body_min_z_offset_m'] for r in d['clean_frames_private']),'whole_native_geometry_frames':len(d['clean_frames_private']),'whole_video_decode':True,'UI_playback':'PENDING observed UI review; do not infer from decode'})
 print(json.dumps({'step':step,'movies':movies,'contact_proxy':metrics},indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('step',choices=['a2','a3','a4']);a=ap.parse_args();review(a.step)
