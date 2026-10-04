"""Measure same spans and assemble fixed-camera actual1x before/after using proven untouched frames."""
from pathlib import Path
import json,hashlib,subprocess,math
import numpy as np
from PIL import Image,ImageDraw
BASE=Path(r'C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');D=BASE/'walk-contact-delivery-r1'
def load(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
 with p.open('x',encoding='utf8') as f:json.dump(v,f,indent=2)
c=load(BASE/'walk-contact-candidate-r2/CONTACT_CANDIDATE_RECEIPT_R2.json');assert sha(c['candidate'])==c['candidate_SHA']
before=load(BASE/'walk-contact-candidate-r2/R3_FULL_NATIVE_BASELINE_PRIVATE_R1.json');after=load(BASE/'walk-contact-candidate-r2/AFTER_FULL_NATIVE_PRIVATE_R1.json');phases=load(BASE/'walk-contact-candidate-r2/CONTACT_PHASE_SOLVE_PRIVATE_R1.json')
metrics={}
for span in [(81,98),(243,264)]:
 key=f'{span[0]}_{span[1]}';metrics[key]={}
 for label,rows in [('before',before),('after',after)]:
  rr=rows[span[0]-1:span[1]];metrics[key][label]={}
  for side in ['L','R']:
   xy=np.array([r['soles'][side]['centroid'][:2] for r in rr]);z=np.array([r['soles'][side]['min_z_offset_m'] for r in rr]);metrics[key][label][side]={'XY_range_m':np.ptp(xy,axis=0).tolist(),'max_XY_speed_m_s':float(np.linalg.norm(np.diff(xy,axis=0),axis=1).max()*30),'lowest_vertex_clearance_range_m':[float(z.min()),float(z.max())]}
 metrics[key]['semantics']='UNLABELED original procedural ground-skimming transfer; unchanged, no new authored donor/contact labels, remains HOLD.' if span[0]==81 else 'Before simultaneous low-clearance stance widening. After one designed sequential L then R step,35mm sin^2 lift + <=10mm pelvis support. New design labels, not extracted/authored donor contacts.'
support={}
for side,(a,b) in {'R':(244,253),'L':(253,263)}.items():
 rr=after[a-1:b];xy=np.array([r['soles'][side]['centroid'][:2] for r in rr]);v=np.linalg.norm(np.diff(xy,axis=0),axis=1)*30;support[side]={'frames':[a,b],'annotation':'procedural support; sole cohort proxy, not physical stance certification','XY_range_m':np.ptp(xy,axis=0).tolist(),'max_XY_speed_m_s':float(v.max()),'RMS_XY_speed_m_s':float(np.sqrt(np.mean(v*v)))}
knee={}
for side in ['L','R']:
 values=[]
 for a,b in zip(before[243:263],after[243:263]):
  normals=[]
  for r in [a,b]:
   hip=np.array(r['joints']['thigh.'+side]);k=np.array(r['joints']['shin.'+side]);ank=np.array(r['joints']['foot.'+side]);normal=np.cross(k-hip,ank-k);norm=np.linalg.norm(normal);normals.append(normal/norm if norm>1e-4 else None)
  if all(n is not None for n in normals):values.append(float(normals[0]@normals[1]))
 knee[side]={'reliable_plane_samples':len(values),'min_before_after_bend_plane_cosine':min(values) if values else None,'note':'Near-straight configurations omitted below1e-4 cross magnitude. Plane cosine is diagnostic, not a flip/self-intersection certificate.'}
write(D/'CONTACT_SPAN_BEFORE_AFTER_QA_R1.json',{'same_spans':metrics,'procedural_support':support,'knee_direction_diagnostic':knee,'root_unchanged_all293':all(a['carrier']==b['carrier'] for a,b in zip(before,after)),'unmodified273_vertex_hash_exact':all(a['body_world_vertex_hash']==b['body_world_vertex_hash'] for a,b in zip(before,after) if not 244<=a['frame']<=263),'max_solve_residual_m':c['max_solver_residual_m'],'source_contact_ground_truth':False})
video=[]
for view in ['front','quarter','side']:
 dst=D/f'pair-frames-{view}';dst.mkdir(exist_ok=False)
 for f in range(1,294):
  old=BASE/f'alpha-walk-turn-preview-{view}-r4'/f'{f:04}.jpg';new=BASE/'walk-contact-preview-r2'/view/f'{f:04}.jpg' if 244<=f<=263 else old
  im=Image.new('RGB',(1024,408),'white');draw=ImageDraw.Draw(im);im.paste(Image.open(old),(0,24));im.paste(Image.open(new),(512,24));draw.text((8,4),f'{view} BEFORE R3 | frame {f} | {(f-1)/30:.3f}s',fill='black');draw.text((520,4),'AFTER R2 | stop bridge only; source quality HOLD',fill='black');im.save(dst/f'{f:04}.jpg',quality=94)
 movie=D/f'R4_STOP_CONTACT_BEFORE_AFTER_{view}_1x.mp4'
 subprocess.run(['ffmpeg','-v','error','-framerate','30','-i',str(dst/'%04d.jpg'),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2','-n',str(movie)],check=True)
 subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(movie),'-f','null','-'],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)]));video.append({'view':view,'path':str(movie),'sha256':sha(movie),'bytes':movie.stat().st_size,'ffprobe':probe,'all293_frames_whole_decode':'PASS'})
 frames=[243,248,253,258,263,264];sheet=Image.new('RGB',(1024*len(frames),408),'white')
 for i,f in enumerate(frames):sheet.paste(Image.open(dst/f'{f:04}.jpg'),(i*1024,0))
 sheet.save(D/f'STOP_BRIDGE_BEFORE_AFTER_{view}_R1.jpg',quality=94)
write(D/'FIXED_CAMERA_VIDEO_CUSTODY_R1.json',video)
html='<!doctype html><meta charset="utf-8"><title>R4 stop bridge contact before/after QA</title><style>body{background:#222;color:#eee;font:16px system-ui}video{width:100%;max-width:1100px}button{font-size:20px;padding:12px}</style><h1>R4 original appearance · one stop-bridge correction</h1><p>BEFORE left / AFTER right. Same fixed cameras and30fps source clock. Entire9.766667s played1x. Only244..263 changed; all273 other native body vertex hashes exact. Actual world root unchanged. Turn/stop remain proxies; contact physics/F2/F3/Unity HOLD.</p><button onclick="document.querySelectorAll(\'video\').forEach(v=>{v.currentTime=0;v.playbackRate=1;v.play()})">Play all three before/after at normal speed</button>'
for v in video:html+=f'<h2>{v["view"]}</h2><video controls preload="auto" src="{Path(v["path"]).name}"></video>'
(D/'REVIEW_STOP_CONTACT_BEFORE_AFTER_R1.html').write_text(html,encoding='utf8');print(json.dumps({'support':support,'knee':knee,'videos':len(video)},indent=2))
