"""Read-only saved OFF oracle and original camera neutral render for new walk candidate."""
import bpy,json,hashlib,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from r4_appearance_signature import snapshot,difference,props
BASE=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');OUT=BASE/'alpha-walk-turn-off-qa-r3';OUT.mkdir(exist_ok=False);d=json.loads((BASE/'alpha-walk-turn-candidate-r3/WALK_TURN_STOP_CANDIDATE_PRIVATE_R3.json').read_bytes());source=Path(d['source']);candidate=Path(d['candidate']);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def images():
 out={}
 for i in bpy.data.images:
  if i.type=='RENDER_RESULT':continue
  raw=props(i);resolved=dict(raw)
  for k in ['filepath','filepath_raw']:
   if resolved.get(k):resolved[k]=str(Path(bpy.path.abspath(resolved[k])).resolve())
  out[i.name]={'raw':raw,'resolved':resolved,'colorspace':props(i.colorspace_settings),'packed':[hashlib.sha256(p.packed_file.data).hexdigest() for p in i.packed_files]}
 return out
assert sha(source)==d['source_SHA'] and sha(candidate)==d['candidate_SHA'];bpy.ops.wm.open_mainfile(filepath=str(source),use_scripts=False);names=[a.name for a in bpy.data.actions];authority=snapshot(names);textures=images();bpy.ops.wm.open_mainfile(filepath=str(candidate),use_scripts=False);actual=snapshot(names);now=images();diff=difference(authority,actual);assert all(k=='textures' for k in diff);assert set(now)==set(textures)
for n in textures:assert textures[n]['resolved']==now[n]['resolved'] and textures[n]['colorspace']==now[n]['colorspace'] and textures[n]['packed']==now[n]['packed']
s=bpy.context.scene;assert s.render.fps/s.render.fps_base==24
for n in d['additive_body_actions'].values():assert bpy.data.actions[n]['source_fps']==30
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=8;s.cycles.seed=0;s.cycles.use_animated_seed=False;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.image_settings.color_depth='8';s.render.filepath=str(OUT/'SAVED_OFF_SOURCE_CAMERA_NEUTRAL.png');bpy.ops.render.render(write_still=True)
with (OUT/'OFF_REOPEN_ORACLE_R3.json').open('x',encoding='utf8') as f:json.dump({'candidate_SHA':sha(candidate),'source_SHA':sha(source),'original_actions':len(names),'raw_snapshot_diff':diff,'all_nontexture_geometry_material_nodes_weights_keys_rest_drivers_bindings_scene_exact':True,'packed_texture_bytes_colorspace_resolved_properties_exact':True,'raw_locator_strings_remapped':bool(diff),'source_scene_fps':24,'all_four_additive_Action_fps':30,'neutral_render':'Original camera/lights/material/color settings; deterministic CPU8samples, compare against existing authoritative witness separately','save_export_source_write':False},f,indent=2)
print('SAVED_OFF_WALK_SOURCE_CONTENT_EXACT',flush=True)
