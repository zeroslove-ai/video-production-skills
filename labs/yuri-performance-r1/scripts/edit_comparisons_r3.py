"""Reproducible CPU edit of existing previz frames; no generated/model video."""
from pathlib import Path
import json,hashlib,subprocess,shutil
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'local/acting-r2';OUT=ROOT/'local/comparison-r3';OUT.mkdir(parents=True,exist_ok=True)
delivery=json.loads((ROOT/'evidence/acting-r2/video_delivery.json').read_text());records=[]
cams=('full_body','waist_threequarter','face_close','hand_face','vertical')
jobs=[(c+'__five_cameras',[(c,'natural',camera) for camera in cams],3) for c in ('greeting_wave','shy_lookaway','please_tilt')]
jobs += [(c+'__head_amplitude',[(c,'natural','face_close'),(c,'exaggerated_head','face_close')],2) for c in ('greeting_wave','shy_lookaway','please_tilt')]
jobs += [('shy_lookaway__eye_lead', [('shy_lookaway','natural','face_close'),('shy_lookaway','simultaneous','face_close')],2)]
phases=[(.65,'ANTICIPATION'),(1.55,'MOTION'),(2.2,'EMOTIONAL PEAK'),(3,'HOLD'),(3.75,'FOLLOW THROUGH'),(5,'RECOVERY')]
for name,sources,cols in jobs:
    inputs=[]
    for clip,variant,camera in sources:
        record=next(r for r in delivery['videos'] if (r['clip'],r['variant'],r['camera'])==(clip,variant,camera));file=SOURCE/record['file']
        assert hashlib.sha256(file.read_bytes()).hexdigest()==record['sha256'];inputs.append(record)
    frames=OUT/name;frames.mkdir(exist_ok=True);rows=(len(sources)+cols-1)//cols
    for f in range(1,121):
        canvas=Image.new('RGB',(cols*640,64+rows*390),'#171c26');draw=ImageDraw.Draw(canvas)
        phase=next(label for end,label in phases if (f-1)/24<end)
        draw.text((12,10),f'DESKTOP R&D | PROXY REFERENCE | 1x 24fps | {name}',fill='white')
        draw.text((12,32),f't={(f-1)/24:.3f}s / {phase} | Not AI video / not target-avatar acceptance',fill='#d1c2ff')
        for i,(clip,variant,camera) in enumerate(sources):
            im=Image.open(SOURCE/clip/variant/camera/f'{f:04d}.png').convert('RGB');im.thumbnail((640,360))
            x=(i%cols)*640;y=64+(i//cols)*390;canvas.paste(im,(x+(640-im.width)//2,y))
            draw.text((x+10,y+366),f'{camera} | {variant}',fill='white')
        canvas.save(frames/f'{f:04d}.png')
    video=OUT/(name+'.mp4');subprocess.run([shutil.which('ffmpeg'),'-y','-framerate','24','-start_number','1','-i',str(frames/'%04d.png'),'-frames:v','120','-c:v','libx264','-threads','4','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True,capture_output=True)
    probe=json.loads(subprocess.check_output([shutil.which('ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(video)]));assert probe['streams'][0]['avg_frame_rate']=='24/1' and float(probe['format']['duration'])==5
    contact=Image.new('RGB',(cols*640,3*(64+rows*390)))
    for row,f in enumerate((1,61,120)):contact.paste(Image.open(frames/f'{f:04d}.png'),(0,row*(64+rows*390)))
    contact.save(OUT/(name+'_first_middle_last.jpg'),quality=90)
    records.append({'file':str(video),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'inputs':inputs,'fps':24,'duration_seconds':5,'frame_count':120,'first_middle_last_frames':[1,61,120],'classification':'EDITED_EXISTING_BLENDER_PROXY_REFERENCE_NOT_AI_GENERATION','camera_variable':'same acting score; camera only' if 'five_cameras' in name else 'see original AB invariants; eye-lead head-follow also drives neck/chest/brow'})
    print('EDIT_DONE',name,flush=True)
e=ROOT/'evidence/comparison-r3';e.mkdir(exist_ok=True);(e/'delivery.json').write_text(json.dumps({'videos':records,'new_physical_recipes':0},indent=2))
html='<html><meta charset="utf-8"><style>body{background:#181c26;color:white;font:16px system-ui}video{width:95%;max-width:1600px}</style><h1>Existing previz comparisons, 1x / 24fps</h1><p>Proxy only. Edited Blender reference; zero model inference.</p>'
for r in records:html+=f'<h2>{Path(r["file"]).stem}</h2><video controls preload="metadata" src="{Path(r["file"]).name}"></video>'
(OUT/'REVIEW_COMPARISONS_R3.html').write_text(html,encoding='utf-8')
