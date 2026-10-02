"""Finite metric depth, camera silhouettes and custom pose metadata; no model acceptance."""
from pathlib import Path
import json,numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];e=ROOT/'evidence/native-camera-r4';receipt=json.loads((e/'conditioning.json').read_text());rows=[]
for sample in receipt['samples']:
    p=Path(sample['path']);meta=json.loads((p/'metadata.json').read_text());depth=np.load(p/'depth_m.npy');ids=np.load(p/'object_id.npy');h,w=depth.shape
    assert ids.shape==depth.shape and np.isfinite(depth).all() and (depth[ids==0]==0).all() and (depth[ids>0]>0).all();assert len(meta['pose'])==57
    y,x=np.nonzero(ids);margins=[int(x.min()),int(y.min()),int(w-1-x.max()),int(h-1-y.max())]
    hair_ids=[int(k) for k,v in meta['object_ids'].items() if v in ('tripo_node_8d1987b0','Hair_Scalp_Coverage')];hy,hx=np.nonzero(np.isin(ids,hair_ids));hair_margin=[int(hx.min()),int(hy.min()),int(w-1-hx.max()),int(h-1-hy.max())] if len(hx) else None
    require_full=sample['camera'] in ('full_body','vertical');status='PASS' if not require_full or min(margins)>1 else 'REVIEW_CLIPPING'
    rows.append({**sample,'subject_margins_left_top_right_bottom_px':margins,'hair_margins_px':hair_margin,'depth_mask_pose_schema':'PASS','full_silhouette_gate':status,'body_clipping_expected_in_closeup':not require_full,'target_face_acceptance':False})
out=ROOT/'local/native-conditioning-r4';contact=Image.new('RGB',(5*320,3*205),'#20242d');draw=ImageDraw.Draw(contact)
for clip_index,clip in enumerate(('greeting_wave','shy_lookaway','please_tilt')):
    for cam_index,camera in enumerate(('full_body','waist_threequarter','hand_face','face_close','vertical')):
        p=out/clip/camera/'0061/depth_near_white.png';im=Image.open(p).convert('RGB');im.thumbnail((320,180));x=cam_index*320;y=clip_index*205;contact.paste(im,(x+(320-im.width)//2,y));draw.text((x+5,y+183),clip+'/'+camera,fill='white')
contact.save(out/'depth_camera_contact.jpg',quality=90);(e/'conditioning_qa.json').write_text(json.dumps({'samples':rows,'all_depth_schema_pass':True,'silhouette_review_samples':[x for x in rows if x['full_silhouette_gate']!='PASS'],'model_control_compatibility':'UNTESTED'},indent=2));print('CONDITION_QA',len(rows),'silhouette reviews',sum(x['full_silhouette_gate']!='PASS' for x in rows))
