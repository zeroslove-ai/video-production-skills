"""Contact sheets for source calibration. Human review remains separate."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'local/source-face-r2'
for name in ('calibration','amplitude_sweep','mouth_detail'):
    p=ROOT/f'evidence/source-face-r2/{name}.json'
    if not p.exists():continue
    data=json.loads(p.read_text());cases=data['cases']
    # Front and quarter side by side per case. Original images retained.
    width=640;row=450
    canvas=Image.new('RGB',(width*4,row*((len(cases)+3)//4)),'#20242d')
    draw=ImageDraw.Draw(canvas)
    for i,c in enumerate(cases):
        x=i%4*width;y=i//4*row
        for j,impath in enumerate(c['frames'][:2]):
            im=Image.open(impath).convert('RGB');im.thumbnail((320,420));canvas.paste(im,(x+j*320,y))
        draw.text((x+6,y+423),c['case'],fill='white')
    canvas.save(OUT/(name+'_contact.jpg'),quality=90)
    print(OUT/(name+'_contact.jpg'))
