"""Exact Dots baseline comparison only. No saves, renders, exports or source edits."""
import bpy,sys,json,hashlib
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from r4_appearance_signature import snapshot,props,anim,attribute_hash
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');I=B/'dots-exact-baseline-inputs-r1';O=B/'dots-exact-baseline-custody-r1';O.mkdir(exist_ok=False)
receipt=json.loads((I/'BASELINE_RECEIVER_RECEIPT_R1.json').read_bytes())
files={a['asset_id']:(Path(a['native']),a['native_sha256']) for a in receipt['assets']}
files['r2']=(Path('C:/Users/JAEWAN/projects/yuri-root-pm-r1/artifacts/reviews/dots-thumb-r2/native-review-only/Yuri_Mug_ThumbVolume_VolumeRedistribution_R2_DEFAULT_OFF.blend'),'67fd96b796ea510644c7c65549f410d4e277f04db91b1c57c991b430245904dc')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dig(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()
def coords(data):
 x=np.empty(len(data)*3,np.float32);data.foreach_get('co',x);return x.reshape(-1,3)
def arrhash(x):return hashlib.sha256(x.tobytes()).hexdigest()
def collect():
 s=bpy.context.scene;full=snapshot(list(bpy.data.actions.keys()));meshes={};correctives=[]
 for ob in bpy.data.objects:
  if ob.type!='MESH':continue
  m=ob.data;sk=m.shape_keys;keys={}
  for k in sk.key_blocks if sk else []:
   keys[k.name]={'coords':arrhash(coords(k.data)),'settings':dig(props(k))}
   if 'VolumeRedistribution_R2' in k.name:
    delta=coords(k.data)-coords(sk.key_blocks[0].data);world=delta.astype(float)@np.array(ob.matrix_world)[:3,:3].T
    correctives.append({'object':ob.name,'key':k.name,'value':k.value,'changed_vertices':int(np.any(delta!=0,axis=1).sum()),'max_world_delta_m':float(np.linalg.norm(world,axis=1).max()),'action':sk.animation_data.action.name if sk.animation_data and sk.animation_data.action else None,'drivers':len(sk.animation_data.drivers) if sk.animation_data else 0})
  meshes[ob.name]={'data_name':m.name,'base':arrhash(coords(m.vertices)),'topology':dig([[*p.vertices,p.material_index,p.use_smooth] for p in m.polygons]),'weights':dig([[[g.group,g.weight] for g in v.groups] for v in m.vertices]),'group_names':dig([[g.name,g.index,g.lock_weight] for g in ob.vertex_groups]),'keys':keys,'shape_anim':dig(anim(sk)) if sk else None,'attributes':dig([[a.name,a.data_type,a.domain,attribute_hash(a)] for a in m.attributes]),'material_slots':[x.name for x in ob.material_slots]}
 envelopes=[]
 for a in bpy.data.actions:
  for layer in a.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      if 'VolumeRedistribution_R2' in fc.data_path:
       vals=[float(fc.evaluate(i)) for i in range(1,170)]
       envelopes.append({'action':a.name,'path':fc.data_path,'keys':len(fc.keyframe_points),'min':min(vals),'max':max(vals),'nonzero_frames':[i+1 for i,v in enumerate(vals) if abs(v)>1e-8],'sample_sha':dig(vals)})
 return {'frame':s.frame_current,'objects':sorted(bpy.data.objects.keys()),'actions':sorted(bpy.data.actions.keys()),'full':full,'meshes':meshes,'correctives':correctives,'envelopes':envelopes,'texts':{t.name:dig(t.as_string()) for t in bpy.data.texts}}
data={}
for label,(p,h) in files.items():
 assert sha(p)==h
 bpy.ops.wm.open_mainfile(filepath=str(p),use_scripts=False);data[label]=collect();assert sha(p)==h
 print('READONLY_COLLECTED',label,len(data[label]['objects']),len(data[label]['actions']),flush=True)
def compare(a,b):
 result={'objects_added':sorted(set(b['objects'])-set(a['objects'])),'objects_removed':sorted(set(a['objects'])-set(b['objects'])),'actions_added':sorted(set(b['actions'])-set(a['actions'])),'actions_removed':sorted(set(a['actions'])-set(b['actions'])),'original_domain_differences':{},'meshes':{},'texts_added':sorted(set(b['texts'])-set(a['texts']))}
 for cat,av in a['full'].items():
  bv=b['full'][cat]
  result['original_domain_differences'][cat]=[k for k in av if av[k]!=bv.get(k)] if isinstance(av,dict) else (['value'] if av!=bv else [])
 for name,am in a['meshes'].items():
  bm=b['meshes'].get(name)
  if bm is None:result['meshes'][name]={'removed':True};continue
  result['meshes'][name]={'original_fields_changed':[k for k in am if k!='keys' and am[k]!=bm.get(k)],'original_keys_changed':[k for k in am['keys'] if am['keys'][k]!=bm['keys'].get(k)],'keys_added':sorted(set(bm['keys'])-set(am['keys']))}
 return result
report={'scope':'ROOT_PM_DOTS_EXACT_BASELINE_CUSTODY_COMPARE_R1','files':{k:{'path':str(p),'sha256':h,'bytes':p.stat().st_size,'unchanged':sha(p)==h} for k,(p,h) in files.items()},'inventory':{k:{'frame':v['frame'],'objects':len(v['objects']),'actions':len(v['actions']),'mesh_count':len(v['meshes'])} for k,v in data.items()},'master_to_control':compare(data['pristine_master'],data['dots_mug_control']),'control_to_r2':compare(data['dots_mug_control'],data['r2']),'r2_correctives':data['r2']['correctives'],'r2_envelopes':data['r2']['envelopes'],'canonical_R4_equivalence':'NOT_ASSERTED: distinct Dots derived master','read_only_no_save_render_export':True,'TierP':0,'contact_quality':'HOLD: no new contact or visual acceptance','pixel_render_parity':'NOT_TESTED in this custody comparison'}
(O/'EXACT_BASELINE_COMPARE_PRIVATE_R1.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('EXACT_BASELINE_COMPARE_DONE',flush=True)
