"""Two synced before/after whole-motion native comparisons; immutable source bytes."""
from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
import numpy as np
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');P=B/'alpha-grasp-left-thumb-preview-c2';O=B/'alpha-grasp-left-thumb-delivery-c2';O.mkdir(exist_ok=False)
assert json.loads((B/'o1-grasp-left-thumb-preview-c2/NATIVE_GUARD_RESULT.json').read_bytes())['guard_status']=='PASS_STRICT_LIVE_BARRIERS_TERMINAL_DRAIN'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();movies=[]
for view,base_movie,base_frames in [('left_hand_close',B/'alpha-grasp-left-thumb-delivery-c1/left_hand_close_AFTER_C1_1x.mp4',B/'alpha-grasp-left-thumb-preview-c1/left_hand_close'),('waist_3q',B/'alpha-grasp-left-thumb-delivery-c1/waist_3q_AFTER_C1_1x.mp4',B/'alpha-grasp-left-thumb-preview-c1/waist_3q')]:
 assert len(list((P/view).glob('*.jpg')))==169;after=O/(view+'_AFTER_C2_1x.mp4');comp=O/(view+'_BEFORE_AFTER_C2_1x.mp4')
 subprocess.run(['ffmpeg','-v','error','-framerate','24','-i',str(P/view/'%04d.jpg'),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2','-n',str(after)],check=True)
 subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(base_movie),'-threads','2','-i',str(after),'-filter_complex','hstack=inputs=2','-c:v','libx264','-preset','fast','-crf','18','-threads','2','-n',str(comp)],check=True)
 for out in [after,comp]:
  subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(out),'-f','null','-'],check=True);probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]));assert int(probe['streams'][0]['nb_frames'])==169;movies.append({'file':str(out),'SHA':sha(out),'bytes':out.stat().st_size,'whole169_decode':'PASS','probe':probe,'before_file_unchanged':str(base_movie),'before_SHA':sha(base_movie)})
 grid=Image.new('RGB',(13*192,13*116),'white');dr=ImageDraw.Draw(grid)
 for ix in range(169):
  x=ix%13*192;y=ix//13*116;grid.paste(Image.open(base_frames/f'{ix+1:04}.jpg').resize((96,96)),(x,y+20));grid.paste(Image.open(P/view/f'{ix+1:04}.jpg').resize((96,96)),(x+96,y+20));dr.text((x+2,y+2),f'f{ix+1} before | C2',fill='black')
 grid.save(O/(view+'_ALL169_BEFORE_AFTER_C2.jpg'),quality=96)
before=np.asarray(Image.open(B/'alpha-a1-contact-qa-r3/CANDIDATE_OFF_SOURCE_CAMERA_NEUTRAL.png'));after=np.asarray(Image.open(P/'CANDIDATE_OFF_SOURCE_NEUTRAL_C2.png'));assert before.shape==after.shape;pixel={'changed_RGBA_pixels':int(np.count_nonzero(np.any(before!=after,axis=2))),'max_channel_error':int(np.abs(before.astype(int)-after.astype(int)).max()),'PASS':bool(np.array_equal(before,after))};assert pixel['PASS'];(O/'OFF_PIXEL_ORACLE_C2.json').write_text(json.dumps(pixel,indent=2),encoding='utf-8');(O/'VIDEO_CUSTODY_C2.json').write_text(json.dumps(movies,indent=2),encoding='utf-8')
html='<!doctype html><meta charset="utf-8"><title>R4 LEFT thumb C2 before-after</title><style>body{background:#222;color:white;font:17px system-ui}video{max-width:100%;width:1024px}button{padding:16px}img{max-width:100%}</style><h1>R4 LEFT thumb C2 · C1 failed | C2 phase-only</h1><p>Same169frames24fps7.041667sec. ONLY thumb1.L quaternion4channels changed on separate native Action COPY. Wrist/body/root/feet/source timing and remaining290curves unchanged. Technical preservation/OFF0; C1 contact FAIL47–61; C2 actual all169 nonadjacent thumb/palm/other-digit intersection0. Changed ONLY thumb phase: onset62–85, release119–135 before native return136. No convincing physical grip approval. Thumb opposition is not physical grasp/Unity/TierP approval.</p><button onclick="document.querySelectorAll(\'video\').forEach(v=>{v.currentTime=0;v.playbackRate=1;v.play()})">Play both comparisons at normal speed</button>'
for view in ['left_hand_close','waist_3q']:html+=f'<h2>{view} · C1 left / C2 right</h2><video controls preload="auto" src="{view}_BEFORE_AFTER_C2_1x.mp4"></video>'
html+='<p>LEFT camera follows wrist world translation only with constant offset/fixed rotation. Whole body/root/feet judged only by fixed waist and native geometry. Inclusive all-body triangles include palm/webbing/other digit weak weights; adjacency counts explicitly retained. No source/model/weight/material/exporter/prop changes. C1 failure retained; ONE C2 temporal correction only. No C3 amplitude/axis sweep.</p>'
for view in ['left_hand_close','waist_3q']:html+=f'<img src="{view}_ALL169_BEFORE_AFTER_C2.jpg">'
(O/'REVIEW_R4_LEFT_THUMB_C2.html').write_text(html,encoding='utf-8');print(json.dumps({'normal_speed_movies':len(movies),'OFF_pixels':pixel,'full169_before_after_comparisons':2}))
