"""Prepare one Wan5B first-frame-presence A/B; NEVER submits either graph.
Reuses installed official template choices, existing weights, and sampled schema.
"""
from pathlib import Path
import json,copy,hashlib
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence/acting-r2';D=ROOT/'workflows/acting-r2';D.mkdir(parents=True,exist_ok=True)
INSTALL=Path(r'C:\Users\JAEWAN\Downloads\ComfyUI-Easy-Install\ComfyUI-Easy-Install')
template=INSTALL/'python_embeded/Lib/site-packages/comfyui_workflow_templates_json/templates/video_wan2_2_5B_ti2v.json'
schema=json.loads((E/'comfy_node_schema.json').read_text())
brief={'id':'wave_AB_first_frame','classification':'ORIGINAL_PROXY_VIDEO_CONDITIONING_RESEARCH_NOT_YURI_IDENTITY','duration_seconds':5,
       'acting_brief':'One original lavender-suit stylized proxy figure alone on a neutral studio floor. Notice a friend beside the lens, small anticipation, raise one open hand beside the face, two soft wrist waves, warm asymmetric smile, hold, settle the wrist, lower the hand and recover. One continuous fixed hand-and-face framing. No new subject or cut.',
       'prompt':'Exactly one stylized lavender-suit friendly humanoid proxy, alone on a plain gray studio background. A small preparatory motion, then raises the right hand beside the face, a gentle open-palm greeting wave with warm smile, holds a short pause, softly lowers the hand and returns to rest. One continuous fixed close-medium three-quarter shot, stable face and fingers, the whole head and waving hand visible, no camera movement.',
       'negative':'multiple people, duplicate subject, crowd, mirror person, extra limbs, fused fingers, changing face, abrupt pose reset, camera cut, zoom, text, subtitles',
       'source_camera':'hand_face','single_variable':'presence of identical Blender first frame at Wan22ImageToVideoLatent.start_image',
       'fixed':['seed 2026100201','same positive/negative prompt','same installed weights','512x288','121 frames','24fps','20 steps','cfg5','uni_pc/simple','model shift8'],
       'gates':['GPU lease explicitly released by owner','no other queued model jobs','same installed model files present','RAM/VRAM watchdog','one job at a time','first/middle/last and full playback QA'],
       'six_rubrics':['identity/subject count','face stability','hand stability','motion continuity','acting readability','camera adherence'],
       'first_frame_reference':'local/acting-r2/greeting_wave/natural/hand_face/0001.png','driving_video':'not accepted by Wan TI2V5B core graph; previz is an acting reference only',
       'result':'PREPARED_NOT_SUBMITTED; video quality effect cannot be measured without inference'}
g={
 '1':{'class_type':'UNETLoader','inputs':{'unet_name':'wan2.2_ti2v_5B_fp16.safetensors','weight_dtype':'default'}},
 '2':{'class_type':'CLIPLoader','inputs':{'clip_name':'umt5_xxl_fp8_e4m3fn_scaled.safetensors','type':'wan','device':'default'}},
 '3':{'class_type':'VAELoader','inputs':{'vae_name':'wan2.2_vae.safetensors'}},
 '4':{'class_type':'CLIPTextEncode','inputs':{'clip':['2',0],'text':brief['prompt']}},
 '5':{'class_type':'CLIPTextEncode','inputs':{'clip':['2',0],'text':brief['negative']}},
 '6':{'class_type':'ModelSamplingSD3','inputs':{'model':['1',0],'shift':8}},
 '7':{'class_type':'Wan22ImageToVideoLatent','inputs':{'vae':['3',0],'width':512,'height':288,'length':121,'batch_size':1}},
 '8':{'class_type':'KSampler','inputs':{'model':['6',0],'seed':2026100201,'steps':20,'cfg':5,'sampler_name':'uni_pc','scheduler':'simple','positive':['4',0],'negative':['5',0],'latent_image':['7',0],'denoise':1}},
 '9':{'class_type':'VAEDecode','inputs':{'samples':['8',0],'vae':['3',0]}},
 '10':{'class_type':'CreateVideo','inputs':{'images':['9',0],'fps':24}},
 '11':{'class_type':'SaveVideo','inputs':{'video':['10',0],'filename_prefix':'yuri-rnd-r2/firstframe_AB','format':'auto','codec':'auto'}}}
i2v=copy.deepcopy(g);i2v['12']={'class_type':'LoadImage','inputs':{'image':'acting_first.png'}};i2v['7']['inputs']['start_image']=['12',0]
for name,graph in [('A_t2v',g),('B_first_frame',i2v)]:
    for node in graph.values():
        typ=node['class_type'];inputs=node['inputs']
        # Verify cached local schema where available; two types also occur in official template.
        if typ in schema and schema[typ]:
            definition=schema[typ]['input']
            assert set(definition.get('required',{})).issubset(inputs),(typ,definition.get('required'),inputs)
            for key,spec in {**definition.get('required',{}),**definition.get('optional',{})}.items():
                if key in inputs and isinstance(spec[0],list):assert inputs[key] in spec[0],(typ,key,inputs[key])
        for value in inputs.values():
            if isinstance(value,list):assert len(value)==2 and value[0] in graph
    (D/(name+'.json')).write_text(json.dumps(graph,indent=2))
files=[]
for group,file in [('diffusion_models','wan2.2_ti2v_5B_fp16.safetensors'),('text_encoders','umt5_xxl_fp8_e4m3fn_scaled.safetensors'),('vae','wan2.2_vae.safetensors')]:
    p=INSTALL/'ComfyUI/models'/group/file;files.append({'file':file,'path':str(p),'present':p.exists(),'bytes':p.stat().st_size if p.exists() else None})
assert all(f['present'] for f in files)
brief['installed_template']=str(template);brief['installed_template_sha256']=hashlib.sha256(template.read_bytes()).hexdigest();brief['installed_weights']=files
brief['schema_validation']='Offline required fields/enum/reference checks against sampled CPU schema; two node classes grounded in installed official template. NOT backend prompt acceptance or inference success.'
brief['higgsfield_same_brief']='CinemaStudio3.0 first image only, 5s 720p quote25 credits, no driving video role. Requires concrete reference review and explicit spend approval.'
(E/'video_AB_plan.json').write_text(json.dumps(brief,indent=2))
print('VIDEO_AB_PREPARED_NO_JOBS',files)
