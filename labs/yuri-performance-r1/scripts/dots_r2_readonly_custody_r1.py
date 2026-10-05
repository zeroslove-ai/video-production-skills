"""One isolated read-only R2 custody audit. No canonical/baseline equivalence claim."""
import bpy,sys,json,hashlib,math
from pathlib import Path
import numpy as np
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from r4_appearance_signature import snapshot
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');O=B/'dots-r2-readonly-custody-r1';O.mkdir(exist_ok=False)
P=Path('C:/Users/JAEWAN/projects/yuri-root-pm-r1/artifacts/reviews/dots-thumb-r2/native-review-only/Yuri_Mug_ThumbVolume_VolumeRedistribution_R2_DEFAULT_OFF.blend');SHA='67fd96b796ea510644c7c65549f410d4e277f04db91b1c57c991b430245904dc';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(P)==SHA and P.stat().st_size==31630511
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()
def inspect():
 s=bpy.context.scene;names=list(bpy.data.actions.keys());sig=snapshot(names);rigs={a.name:{'bones':len(a.bones),'rest_parent_hash':digest([(b.name,b.parent.name if b.parent else None,list(map(list,b.matrix_local))) for b in a.bones])} for a in bpy.data.armatures};keys=[]
 for ob in bpy.data.objects:
  if ob.type!='MESH' or not ob.data.shape_keys:continue
  sk=ob.data.shape_keys;base=np.empty(len(sk.key_blocks[0].data)*3,np.float32);sk.key_blocks[0].data.foreach_get('co',base);base=base.reshape(-1,3)
  for k in sk.key_blocks:
   if not any(word in k.name.lower() for word in ['thumb','correct','redistrib']):continue
   coords=np.empty(base.size,np.float32);k.data.foreach_get('co',coords);delta=coords.reshape(-1,3)-base;changed=np.any(delta!=0,axis=1);world=delta.astype(float)@np.array(ob.matrix_world)[:3,:3].T;ad=sk.animation_data
   keys.append({'object':ob.name,'key':k.name,'default_value':k.value,'mute':k.mute,'relative_key':k.relative_key.name if k.relative_key else None,'changed_vertices':int(changed.sum()),'max_mesh_local_delta_m':float(np.linalg.norm(delta,axis=1).max()),'max_object_world_delta_m':float(np.linalg.norm(world,axis=1).max()),'finite':bool(np.isfinite(delta).all()),'delta_hash':hashlib.sha256(delta.tobytes()).hexdigest(),'shape_action':ad.action.name if ad and ad.action else None,'shape_drivers':len(ad.drivers) if ad else 0,'nla_tracks':len(ad.nla_tracks) if ad else 0})
 action_inventory=[];envelopes=[]
 for a in bpy.data.actions:
  fc=[f for la in a.layers for st in la.strips for bag in st.channelbags for f in bag.fcurves];action_inventory.append({'name':a.name,'curves':len(fc),'frames':list(a.frame_range),'signature':sig['actions'][a.name]})
  for f in fc:
   if 'key_blocks' in f.data_path or ('thumb' in a.name.lower() and f.data_path.endswith('value')):
    vals=[float(f.evaluate(i)) for i in range(1,170)];assert all(math.isfinite(v) for v in vals);envelopes.append({'action':a.name,'path':f.data_path,'index':f.array_index,'key_count':len(f.keyframe_points),'range':list(f.range()),'min':min(vals),'max':max(vals),'at_frames':{str(i):vals[i-1] for i in [1,49,52,69,85,101,119,136,169]},'active_frames_over1e-8':[i+1 for i,v in enumerate(vals) if abs(v)>1e-8],'sample_hash':digest(vals)})
 return sig,{'frame':s.frame_current,'fps':s.render.fps,'objects':len(bpy.data.objects),'object_names':sorted(bpy.data.objects.keys()),'rigs':rigs,'bones':sum(len(a.bones) for a in bpy.data.armatures),'materials':len(bpy.data.materials),'actions':action_inventory,'correctives':keys,'envelopes':envelopes,'domain_hashes':{k:digest(v) for k,v in sig.items()}}
bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);sig1,a=inspect();assert a['frame']==1
bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);sig2,b=inspect();same=sig1==sig2;assert same and a==b;assert sha(P)==SHA
# Do not manufacture the unavailable Dots control from canonical R4.
m={'scope':'ROOT_PM_DOTS_R2_CUSTODY_ONLY_SAFE_BOUNDARY','candidate':str(P),'candidate_SHA':SHA,'candidate_bytes':P.stat().st_size,'read_only_no_save':True,'source_bytes_unchanged':True,'cold_reopen_same_file_full_snapshot_exact':same,'candidate_inventory':a,'appropriate_control':'Yuri_Mug_GraspRelease_POSE_STUDY_IndependentSupport_DEFAULT_OFF.blend','appropriate_control_SHA_reported':'40fa19e9f276fdc5c6dc08e9e75bda6da90b578a1320443468eb423f580d5374','pristine_Dots_master_SHA_reported':'16440ac619b43f2a9cbc5d0f6660ba1341e08961126d50e19c43493ccf5a646b','baseline_available':False,'original_object_rig_rest_bind_weights_actions_preservation':'UNKNOWN: appropriate Dots control/master bytes unavailable locally. Same-file cold reopen is custody consistency, not source parity. Upstream receipts not independent original comparison.','canonical_R4_equivalence':'NOT_ASSERTED; derived Dots study source is distinct','contact_or_visual_acceptance':'HOLD / upstream contact debt; no new geometry/contact/render/quality tests','TierP':0,'new_candidate':False,'Unity_or_export':False}
(O/'DOTS_R2_READONLY_CUSTODY_PRIVATE_R1.json').write_text(json.dumps(m,indent=2),encoding='utf8');print('DOTS_R2_CUSTODY_COLD_REOPEN_EXACT_BASELINE_UNKNOWN',[(k['key'],k['default_value'],k['changed_vertices']) for k in a['correctives']],flush=True)
