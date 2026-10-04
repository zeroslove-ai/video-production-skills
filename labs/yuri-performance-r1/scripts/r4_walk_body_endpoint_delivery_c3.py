"""C2 images reused byte-exact, C3 actual two-cycle QA delivery."""
from pathlib import Path
import json,hashlib,subprocess,zipfile
import numpy as np
from PIL import Image,ImageDraw
LAB=Path(__file__).resolve().parents[1];B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');P=B/'alpha-walk-body-endpoint-c3';C2=B/'alpha-walk-root-endpoint-c2b';D=B/'alpha-walk-body-endpoint-delivery-c3';E=LAB/'evidence/walk-body-endpoint-c3';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();js=lambda p:json.loads(Path(p).read_bytes());m=js(P/'WALK_BODY_ENDPOINT_PRIVATE_C3.json');g=js(B/'o1-walk-body-endpoint-c3/NATIVE_GUARD_RESULT.json');assert g['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN' and g['terminal_job']['active']==0 and m['actual_two_cycle_capture_complete'];D.mkdir(exist_ok=False);E.mkdir(exist_ok=False)
oldzip=B/'YURI_R4_WALK_ROOT_ENDPOINT_EXPERIMENT_C2_20261005.zip';assert sha(oldzip)=='2986aafb398a2626f8603ce9e953324ea9332366215e666dca3bfe10ad7aeb15'
with zipfile.ZipFile(oldzip) as z:oldidx=json.loads(z.read('PACKET_INDEX_C2.json'));oldhash={x['path']:x['sha256'] for x in oldidx['members']}
movies=[];custody=[]
for view in m['views']:
 outputs={}
 for role,frames in [('C2',C2/'C2_two_cycles_native'/view),('C3',P/'C3_two_cycles_native'/view)]:
  assert len(list(frames.glob('*.jpg')))==192
  if role=='C2':
   assert all(sha(frames/f'{f:04}.jpg')==oldhash[f'C2-native-qa/C2_two_cycles_native/{view}/{f:04}.jpg'] for f in range(1,193))
   custody.extend({'view':view,'frame':f,'file':str(frames/f'{f:04}.jpg'),'sha256':sha(frames/f'{f:04}.jpg'),'reuse':'Existing C2 actual native fixed-camera frame unchanged, no baseline rerender/reframe.'} for f in range(1,193))
  out=D/f'{view}_{role}_TWO_CYCLES_NATIVE24FPS_1x.mp4';subprocess.run(['ffmpeg','-v','error','-framerate','24','-i',str(frames/'%04d.jpg'),'-frames:v','192','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-threads','2','-n',str(out)],check=True);outputs[role]=out
  for cyc in [0,1]:
   grid=Image.new('RGB',(256*8,280*12),'white');dr=ImageDraw.Draw(grid)
   for i in range(96):
    f=cyc*96+i+1;x=i%8*256;y=i//8*280;grid.paste(Image.open(frames/f'{f:04}.jpg').resize((256,256)),(x,y+24));dr.text((x+3,y+3),f'{role} {view} {f} {(f-1)/24:.3f}s',fill='black')
   grid.save(D/f'ALL96_{view}_{role}_cycle{cyc+1}.jpg',quality=94)
 comparison=D/f'{view}_C2_LEFT_C3_RIGHT_TWO_CYCLES_NATIVE24FPS_1x.mp4';subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(outputs['C2']),'-threads','2','-i',str(outputs['C3']),'-filter_complex','[0:v][1:v]hstack=inputs=2[v]','-map','[v]','-frames:v','192','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-threads','2','-filter_complex_threads','2','-n',str(comparison)],check=True)
 for out in [*outputs.values(),comparison]:
  subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(out),'-f','null','-'],check=True);q=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(out)]))['streams'][0];assert int(q['nb_read_frames'])==192 and q['avg_frame_rate']=='24/1' and abs(float(q['duration'])-8)<1e-6;movies.append({'file':str(out),'sha256':sha(out),'view':view,'comparison':out==comparison,'frames':192,'fps':24,'duration':8,'whole_decode':'PASS'})
a=np.asarray(Image.open(B/'alpha-a1-contact-qa-r3/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png').convert('RGBA'));z=np.asarray(Image.open(P/'BODY_ENDPOINT_OFF_SOURCE_NEUTRAL_C3.png').convert('RGBA'));assert np.array_equal(a,z);pixel={'changed_pixels':0,'max_RGBA_delta':0,'exact_decoded_RGBA_equal':True,'dimensions':list(a.shape)};(D/'OFF_PIXEL_QA_C3.json').write_text(json.dumps(pixel,indent=2),encoding='utf8')
scalar={k:v for k,v in m.items() if k not in ['rows_private','original87_signature_private','source','candidate','library','C2_candidate']};scalar['candidate_SHA']=m['candidate_SHA'];scalar['library_SHA']=m['library']['sha256'];scalar['OFF_pixels']=pixel;scalar['max_geometry_pose_change_m']={n:max(x['geometry_delta_vs_C2_m'][n] for x in m['rows_private']) for n in m['rows_private'][0]['geometry_delta_vs_C2_m']};scalar['actual_changed_bones']=sorted({n for x in m['rows_private'] for n in x['changed_pose_bones']});scalar['changed_global_frames']=[x['frame'] for x in m['rows_private'] if x['geometry_delta_vs_C2_m']['Meshy_Body_NeutralCovered']>1e-7];scalar['contact_new_pair_max']=max(v for x in m['contact_regression'] for v in x['new_pair_identities_vs_C2'].values());scalar['visual']='PENDING_ACTUAL_TWO_CYCLE_1X';scalar['verdict']='PENDING_VISUAL_AND_CONTACT_TRADEOFF_REVIEW';(E/'WALK_BODY_ENDPOINT_SCALAR_QA_C3.json').write_text(json.dumps(scalar,indent=2),encoding='utf8');(D/'C2_CACHE_BYTE_EXACT_CUSTODY_C3.json').write_text(json.dumps(custody,indent=2),encoding='utf8');(D/'VIDEO_CUSTODY_C3.json').write_text(json.dumps(movies,indent=2),encoding='utf8')
html='<!doctype html><meta charset="utf-8"><title>R4 C2 versus C3 BODY seam trial</title><style>body{background:#222;color:#eee;font:16px system-ui}video{width:640px;max-width:100%}button{padding:12px}</style><h1>C2 left / C3 right: TWO accumulated Walk cycles</h1><p>192frames/24fps/8sec/1x, root path unchanged and no reset. ONE left thigh/shin/foot quaternion tangent correction, first/last3samples only. C2 fixed-camera footage reused byte-exact. C3 actual new native captures. Contact/source/Unity/TierP/F2/StageB approval withheld.</p><button onclick="document.querySelectorAll(\'video\').forEach(v=>{v.currentTime=0;v.playbackRate=1;v.play()})">Play C2 versus C3 full two cycles at 1x</button>'
for x in movies:
 if x['comparison']:html+=f'<h2>{x["view"]}</h2><video controls preload="auto" src="{Path(x["file"]).name}"></video>'
(D/'REVIEW_WALK_BODY_ENDPOINT_C3.html').write_text(html,encoding='utf8');print(json.dumps(scalar,indent=2))
