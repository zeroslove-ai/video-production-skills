"""Dark opening measurements for the fixed mouth-detail camera, not phonetic QA."""
from pathlib import Path
from PIL import Image
import json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'local/source-face-r2/mouth-detail';records=[]
for case in ('neutral','A_calibrated','O_calibrated'):
    image=Image.open(OUT/case/'front.png').convert('L');pixels=image.load();remaining={(x,y) for x in range(200,440) for y in range(150,330) if pixels[x,y]<70};components=[]
    while remaining:
        seed=remaining.pop();component=[seed];queue=[seed]
        while queue:
            x,y=queue.pop()
            for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if q in remaining:remaining.remove(q);queue.append(q);component.append(q)
        components.append(component)
    if components:
        comp=max(components,key=len);xs=[p[0] for p in comp];ys=[p[1] for p in comp];w=max(xs)-min(xs)+1;h=max(ys)-min(ys)+1
        record={'case':case,'dark_component_pixels':len(comp),'bbox':[min(xs),min(ys),max(xs),max(ys)],'width_px':w,'height_px':h,'width_height_ratio':w/h}
    else:record={'case':case,'dark_component_pixels':0,'width_height_ratio':None}
    records.append(record)
data={'camera':'Fixed orthographic mouth detail, 640x480; no image rescale','method':'largest 4-connected luminance<70 component in ROI x200..439/y150..329','scope':'Auxiliary silhouette evidence; lighting-dependent, not a phoneme classifier','cases':records,'visual_verdict':'A/O semantic distinction insufficient at face framing; both horizontally open in detail. Actual-face gate remains FAIL_A_O_READABILITY.'}
(ROOT/'evidence/source-face-r2/mouth_measurement.json').write_text(json.dumps(data,indent=2));print(json.dumps(records))
