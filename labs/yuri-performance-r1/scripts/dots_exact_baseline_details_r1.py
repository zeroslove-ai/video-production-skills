"""Read-only details for differences found in exact-baseline custody comparison."""
import bpy,sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from r4_appearance_signature import props,custom,anim
B=Path('C:/Users/JAEWAN/Documents/Codex/2026-10-02/files-pasted-by-the-user-yuri/outputs');I=B/'dots-exact-baseline-inputs-r1';O=B/'dots-exact-baseline-details-r1';O.mkdir(exist_ok=False)
r=json.loads((B/'dots-exact-baseline-custody-r1/EXACT_BASELINE_COMPARE_PRIVATE_R1.json').read_bytes())
def meshco(data):return hashlib.sha256(json.dumps([list(v.co) for v in data],separators=(',',':')).encode()).hexdigest()
data={}
for label,f in r['files'].items():
 p=Path(f['path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
 bpy.ops.wm.open_mainfile(filepath=str(p),use_scripts=False);ob=bpy.data.objects['Meshy_Body_NeutralCovered'];m=ob.data
 data[label]={'object':{'props':props(ob),'custom':custom(ob),'anim':anim(ob),'modifiers':[[x.name,props(x),custom(x)] for x in ob.modifiers],'constraints':[[x.name,props(x)] for x in ob.constraints],'materials':[[x.name,props(x)] for x in ob.material_slots],'groups':[[x.name,x.index,x.lock_weight] for x in ob.vertex_groups]},'mesh_base_coords_hash':meshco(m.vertices),'basis_coords_hash':meshco(m.shape_keys.key_blocks['Basis'].data) if m.shape_keys and 'Basis' in m.shape_keys.key_blocks else None,'images':{x.name:{'props':props(x),'colorspace':props(x.colorspace_settings),'packed_sha':[hashlib.sha256(a.packed_file.data).hexdigest() for a in x.packed_files]} for x in bpy.data.images if x.type!='RENDER_RESULT'}}
 assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
def diff(a,b,prefix=''):
 if isinstance(a,dict) and isinstance(b,dict):return [v for k in sorted(set(a)|set(b)) for v in diff(a.get(k),b.get(k),prefix+'/'+k)]
 return [{'field':prefix,'before':a,'after':b}] if a!=b else []
out={'r2_body_object_actual_diffs':diff(data['dots_mug_control']['object'],data['r2']['object']),'master_control_image_actual_diffs':diff(data['pristine_master']['images'],data['dots_mug_control']['images']),'r2_basis_exact_control_mesh_coords':data['r2']['basis_coords_hash']==data['dots_mug_control']['mesh_base_coords_hash'],'read_only_files_unchanged':True}
(O/'EXACT_BASELINE_DETAILS_PRIVATE_R1.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,ensure_ascii=True),flush=True)
