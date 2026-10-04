"""Fixed saved OFF oracle with explicit texture locator/content domains; no writes to assets."""
import bpy,json,sys,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference,props,digest
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');source=HERE.parent/'local/model-handoff-r4/Character_Master_NeckSkin_R4.blend'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def textures():
 out={}
 for i in bpy.data.images:
  if i.type=='RENDER_RESULT':continue
  raw=props(i);canonical=dict(raw)
  for k in ['filepath','filepath_raw']:
   if k in canonical and canonical[k]:canonical[k]=str(Path(bpy.path.abspath(canonical[k])).resolve())
  out[i.name]={'raw':raw,'resolved':canonical,'colorspace':props(i.colorspace_settings),'packed_SHA':[hashlib.sha256(p.packed_file.data).hexdigest() for p in i.packed_files]}
 return out
assert sha(source)=='a30fc513a6da3782742c337ee4a50ab3523b82467517d91d84eb0cc0ede2aafa';out=BASE/'alpha-first4-reopen-off-r2';out.mkdir(exist_ok=False)
bpy.ops.wm.open_mainfile(filepath=str(source),use_scripts=False);names=[a.name for a in bpy.data.actions];authority=snapshot(names);original=textures();result={}
for step in ['a2','a3','a4']:
 d=json.loads((BASE/f'alpha-{step}-contact-candidate-r2/CONTACT_CANDIDATE_PRIVATE_R2.json').read_bytes());candidate=Path(d['candidate']);assert sha(candidate)==d['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=str(candidate),use_scripts=False);actual=snapshot(names);diff=difference(authority,actual);images=textures();assert set(images)==set(original);texdiff={};resolved_ok=True
 for n in original:
  raw_a=original[n]['raw'];raw_b=images[n]['raw'];delta={k:[raw_a.get(k),raw_b.get(k)] for k in set(raw_a)|set(raw_b) if raw_a.get(k)!=raw_b.get(k)}
  if delta:texdiff[n]=delta
  resolved_ok &= original[n]['resolved']==images[n]['resolved'] and original[n]['colorspace']==images[n]['colorspace'] and original[n]['packed_SHA']==images[n]['packed_SHA']
 result[step]={'candidate_SHA':sha(candidate),'source_SHA':sha(source),'raw_snapshot_diff':diff,'texture_property_first_divergence':texdiff,'resolved_texture_properties_colorspace_packed_content_exact':resolved_ok,'all_nontexture_source_categories_exact':all(k=='textures' for k in diff),'original_action_count':len(names),'scene_fps':bpy.context.scene.render.fps/bpy.context.scene.render.fps_base,'action_fps':float(bpy.data.actions[d['action']]['source_fps']),'no_save_render_export_source_Unity_write':True}
with (out/'SAVED_OFF_LOCATOR_DOMAIN_READBACK_R2.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
assert all(r['resolved_texture_properties_colorspace_packed_content_exact'] and r['all_nontexture_source_categories_exact'] for r in result.values()),'Unresolved saved-source data difference; keep candidate HOLD'
print('SAVED_OFF_SOURCE_CONTENT_AND_RESOLVED_TEXTURE_EXACT',list(result),flush=True)
