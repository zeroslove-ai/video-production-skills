"""Semantic acting scores: degrees/normalized intents, not target facial weights.
Each channel owns a separate smooth timing curve. No Blender dependency.
"""
import math
FPS=24
DURATION=5.0
PHASES={'anticipation':[0,.65],'motion':[.65,1.55],'emotional_peak':[1.55,2.2],
        'hold':[2.2,3.0],'follow_through':[3.0,3.75],'recovery':[3.75,5.0]}

def curve(t,points):
    if t<=points[0][0]:return points[0][1]
    for (a,x),(b,y) in zip(points,points[1:]):
        if t<=b:
            u=(t-a)/(b-a);u=u*u*(3-2*u)
            return x+(y-x)*u
    return points[-1][1]

def pulse(t,centre,width=.10):
    return max(0,1-abs(t-centre)/width)

def score(clip,t,head_gain=1.0,gaze_lead=.18,blink_profile='r2_triangular'):
    r={}; f={}; gaze=[0.,0.]
    # Baselines return exactly; shoulder/chest breath is gated by the acting arc.
    arc=curve(t,[(0,0),(.5,1),(3.7,1),(5,0)])
    r['chest']=(.55*math.sin(t*3.1)*arc,0,0)
    if clip=='greeting_wave':
        lift=curve(t,[(0,0),(.35,0),(.65,-.06),(1.58,1),(2.75,1),(3.25,.86),(4.6,0),(5,0)])
        wave=math.sin((t-1.72)*2*math.pi*1.55)*curve(t,[(0,0),(1.72,0),(1.92,1),(2.55,1),(2.95,0),(5,0)])
        r.update({'upper_arm.R':(-55*lift,0,5*lift),'forearm.R':(-145*lift,0,7*wave),
                  'hand.R':(3*lift,5*lift,18*wave),'neck':(0,0,-2*lift),
                  'head':(-3*lift,1.7*lift,-4*lift*head_gain),
                  'forearm.L':(-5*arc,0,0)})
        f['smile']=curve(t,[(0,0),(.3,.10),(1.35,.66),(2.30,.78),(3.05,.65),(4.7,0),(5,0)])
        f['squint_l']=.23*f['smile'];f['squint_r']=.19*f['smile']
        f['brow_up_l']=curve(t,[(0,0),(.32,.12),(1.3,.08),(3.1,.04),(4.8,0),(5,0)])
        f['brow_up_r']=.65*f['brow_up_l']
        f['jaw_open']=curve(t,[(0,0),(1.25,0),(1.65,.22),(2.0,.05),(3.1,.02),(4.7,0),(5,0)])
        gaze=[curve(t,[(0,0),(.32,.12),(.65,0),(5,0)]),.02*arc]
        centres=[.52,3.18]
    elif clip=='shy_lookaway':
        away=curve(t,[(0,0),(.70,0),(1.42,1),(2.90,1),(3.22,.88),(3.85,-.09),(4.7,0),(5,0)])
        head=curve(t,[(0,0),(.70+gaze_lead,0),(1.42+gaze_lead,1),(3.12,1),(3.95,-.07),(4.8,0),(5,0)])
        r.update({'head':(7*head,18*head*head_gain,-3*head),
                  'neck':(1.2*head,2.5*head,0),'chest':(1.3*head,1.5*head,-1*head),
                  'forearm.L':(-12*arc,0,4*arc),'forearm.R':(-8*arc,0,-2*arc)})
        gaze=[.78*away,-.37*away]
        f['smile']=curve(t,[(0,0),(.45,.18),(1.6,.35),(2.85,.24),(3.72,.52),(4.9,0),(5,0)])
        f['squint_l']=.18*f['smile'];f['squint_r']=.13*f['smile']
        f['brow_up_l']=.18*head;f['brow_up_r']=.11*head
        f['jaw_open']=curve(t,[(0,0),(.7,.03),(1.3,0),(5,0)])
        centres=[.86,3.30]
    elif clip=='please_tilt':
        ask=curve(t,[(0,0),(.45,-.07),(1.4,1),(2.95,1),(3.35,1.045),(4.65,0),(5,0)])
        tilt=curve(t,[(0,0),(.70,0),(1.68,1),(3.05,1),(3.4,.86),(4.85,0),(5,0)])
        r.update({'head':(-2*ask,0,-11*tilt*head_gain),'neck':(0,0,-2*tilt),
                  'chest':(2.3*ask,0,0),'forearm.L':(-38*ask,0,-3*ask),
                  'forearm.R':(-33*ask,0,2*ask),'hand.L':(0,0,-3*ask),'hand.R':(0,0,2*ask)})
        gaze=[.05*ask,curve(t,[(0,0),(.5,.14),(2.95,.14),(4.65,0),(5,0)])]
        f['brow_up_l']=curve(t,[(0,0),(.48,.08),(1.6,.37),(3.15,.35),(4.7,0),(5,0)])
        f['brow_up_r']=.78*f['brow_up_l']
        f['smile']=curve(t,[(0,0),(.9,.06),(1.95,.23),(3.2,.39),(4.8,0),(5,0)])
        f['squint_l']=.13*f['smile'];f['squint_r']=.10*f['smile']
        f['jaw_open']=curve(t,[(0,0),(1.32,0),(1.85,.11),(2.15,.02),(5,0)])
        centres=[.62,3.42]
    else:raise ValueError(clip)
    for side,delay in [('l',0),('r',.020 if blink_profile=='r3_hold' else .035)]:
        if blink_profile=='r3_hold':
            # Aligned closure plateau survives 24fps sampling; slight opening asymmetry.
            snapped=[round(c*FPS)/FPS+delay for c in centres]
            f['blink_'+side]=max(curve(t,[(c-.070,0),(c-.020,1),(c+.026,1),(c+.120,0)]) for c in snapped)
        else:f['blink_'+side]=max(pulse(t,c+delay,.105) for c in centres)
    return {'rotations_degrees':r,'face_intents':f,'gaze_xy':gaze}

def timing_sheet(clip,blink_profile='r2_triangular'):
    return {'id':clip,'fps':FPS,'duration_seconds':DURATION,'phases':PHASES,
            'gaze_lead_seconds':.18 if clip=='shy_lookaway' else None,
            'profile_experiment':{'A':'head_gain=1 natural amplitude','B':'head_gain=1.45 exaggerated head ONLY; body/face/hold unchanged'},
            'status':'SEMANTIC_TIMING_PROXY_NOT_ACTUAL_AVATAR_CALIBRATION',
            'blink_profile':blink_profile,
            'samples':[{'frame':f,'time':f/FPS,**score(clip,f/FPS,blink_profile=blink_profile)} for f in range(121)]}
