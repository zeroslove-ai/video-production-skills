"""24fps single-variable eyelid comparison; no target face acceptance."""
from pathlib import Path
import json
from acting_recipe import score,FPS
ROOT=Path(__file__).resolve().parents[1];reports=[]
for clip in ('greeting_wave','shy_lookaway','please_tilt'):
    common={'A':[],'B':[]};maximum={k:{s:0 for s in ('l','r')} for k in common}
    for frame in range(121):
        a=score(clip,frame/FPS);b=score(clip,frame/FPS,blink_profile='r3_hold')
        assert a['rotations_degrees']==b['rotations_degrees'] and a['gaze_xy']==b['gaze_xy']
        assert {k:v for k,v in a['face_intents'].items() if not k.startswith('blink_')}=={k:v for k,v in b['face_intents'].items() if not k.startswith('blink_')}
        for label,data in [('A',a),('B',b)]:
            for side in ('l','r'):maximum[label][side]=max(maximum[label][side],data['face_intents']['blink_'+side])
            if all(data['face_intents']['blink_'+s]>=.999 for s in ('l','r')):common[label].append(frame+1)
    assert len(common['B'])>=2,(clip,common)
    reports.append({'clip':clip,'maximum_intent_at_24fps':maximum,'both_eyes_full_closure_frames':common,'all_non_blink_channels_identical':True})
out=ROOT/'evidence/acting-r3-blink/blink_ab_qa.json';out.write_text(json.dumps({'status':'SEMANTIC_SAMPLING_PASS_NOT_ACTUAL_RIG_FACE_PASS','clips':reports},indent=2));print(out.read_text())
