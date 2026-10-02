"""Standalone CSV/SVG timing sheets and controlled semantic A/B invariants."""
from pathlib import Path
import json,csv,sys,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from acting_recipe import score,PHASES
E=ROOT/'evidence/acting-r2';OUT=ROOT/'local/acting-r2';reports=[]
def channels(v):
    r=v['rotations_degrees'];f=v['face_intents']
    return {'head_yaw_deg':r.get('head',(0,0,0))[1],'head_tilt_deg':r.get('head',(0,0,0))[2],
            'arm_lift_deg':r.get('upper_arm.R',(0,0,0))[0],'wrist_deg':r.get('hand.R',(0,0,0))[2],
            'gaze_x':v['gaze_xy'][0],'gaze_y':v['gaze_xy'][1],'blink_l':f['blink_l'],'blink_r':f['blink_r'],
            'brow_l':f['brow_up_l'],'brow_r':f['brow_up_r'],'smile':f['smile'],'squint_l':f['squint_l'],'jaw_open':f['jaw_open']}
for clip in ('greeting_wave','shy_lookaway','please_tilt'):
    samples=[channels(score(clip,f/24)) for f in range(121)]
    with (E/(clip+'_timing.csv')).open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['frame','time_s',*samples[0]]);writer.writeheader()
        for f,row in enumerate(samples):writer.writerow({'frame':f+1,'time_s':f/24,**row})
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="920" viewBox="0 0 1200 920"><rect width="1200" height="920" fill="#20242d"/>',f'<text x="20" y="25" fill="white" font-size="20">{clip}: independent semantic curves / not calibrated target weights</text>']
    for i,(phase,(a,b)) in enumerate(PHASES.items()):
        x=180+a*195;svg += [f'<rect x="{x}" y="42" width="{(b-a)*195}" height="850" fill="{["#293242","#313d48"][i%2]}"/>',f'<text x="{x+3}" y="57" fill="#cbd7e6" font-size="10">{phase}</text>']
    for i,name in enumerate(samples[0]):
        values=[x[name] for x in samples];low=min(0,min(values));high=max(.05,max(values));span=high-low
        y=90+i*62
        svg += [f'<text x="10" y="{y+20}" fill="white" font-size="12">{name} [{low:.2f}, {high:.2f}]</text>',f'<path d="M180 {y+40} H1155" stroke="#657082"/>']
        points=' '.join(f'{180+j/24*195:.1f},{y+40-(v-low)/span*36:.1f}' for j,v in enumerate(values))
        svg.append(f'<polyline points="{points}" fill="none" stroke="#98dce5" stroke-width="2"/>')
    svg.append('</svg>');(OUT/(clip+'_timing.svg')).write_text(''.join(svg))
    # Isolate head amplitude; all other timing/channel scores identical.
    for f in range(121):
        a=score(clip,f/24);b=score(clip,f/24,head_gain=1.45)
        assert a['face_intents']==b['face_intents'] and a['gaze_xy']==b['gaze_xy']
        for bone in a['rotations_degrees']:
            if bone!='head':assert a['rotations_degrees'][bone]==b['rotations_degrees'][bone]
    report={'clip':clip,'head_exaggeration_AB':'Only one head angle amplitude changes; all face/gaze/other bones/timing identical','neutral_return':all(abs(v)<1e-9 for v in samples[-1].values()),'semantic_gaze_head_lead_frames':None,'actual_target_calibration':False}
    if clip=='shy_lookaway':
        eye=next(f for f,v in enumerate(samples) if abs(v['gaze_x'])>.005)
        head=next(f for f,v in enumerate(samples) if abs(v['head_yaw_deg'])>.05)
        report['semantic_gaze_head_lead_frames']=head-eye
        for f in range(121):
            a=score(clip,f/24);b=score(clip,f/24,gaze_lead=0)
            assert a['face_intents']['smile']==b['face_intents']['smile'] and a['gaze_xy']==b['gaze_xy']
        report['lead_AB_caveat']='Lead modifies head, dependent neck/chest and head-follow brows; smile/gaze/blink fixed. It is a head-follow timing intervention, not eyes-only change.'
    reports.append(report)
(E/'timing_experiments.json').write_text(json.dumps(reports,indent=2));print('TIMING_SHEETS_PASS',reports)
