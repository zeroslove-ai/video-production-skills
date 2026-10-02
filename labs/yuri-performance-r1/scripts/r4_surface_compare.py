"""Independent face delta and actual deform-group audits (exclude surface masks)."""
import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];L=ROOT/'local/model-handoff-r4';E=ROOT/'evidence/model-handoff-r4'
def read(name):
 bpy.ops.wm.open_mainfile(filepath=str(L/name));o=bpy.data.objects['Character_Body_Head'];k=o.data.shape_keys.key_blocks;basis=k[0]
 head={'basis':[v.co.copy() for v in basis.data],'delta':{s.name:[v.co-b.co for v,b in zip(s.data,basis.data)] for s in k}}
 meshes=[]
 for o in bpy.data.objects:
  mods=[m for m in o.modifiers if m.type=='ARMATURE' and m.object]
  if o.type!='MESH' or not mods or o.hide_render:continue
  bones={b.name for m in mods for b in m.object.data.bones};sums=[sum(g.weight for g in v.groups if o.vertex_groups[g.group].name in bones) for v in o.data.vertices]
  meshes.append({'name':o.name,'deform_weight_sum_error':max(abs(x-1) for x in sums),'deform_unweighted_vertices':sum(x<1e-8 for x in sums),'deform_gt4':sum(sum(g.weight>1e-8 and o.vertex_groups[g.group].name in bones for g in v.groups)>4 for v in o.data.vertices),'surface_mask_groups_excluded':[g.name for g in o.vertex_groups if g.name not in bones]})
 return head,meshes
a,_=read('Character_Surface_Motion_R3d_20261002.blend');b,meshes=read('Character_Master_NeckSkin_R4.blend')
d={'same_head_vertex_count':len(a['basis'])==len(b['basis']),'max_head_vertex_delta_above_z843_m':max((v-w).length for v,w in zip(a['basis'],b['basis']) if v.z>.843),'max_expression_delta_difference_m':{n:max((v-w).length for v,w in zip(d,b['delta'][n])) for n,d in a['delta'].items()},'r4_visible_skin':meshes,'weight_mask_note':'R3_* procedural masks are not deform influences; all group sums alone would produce a false normalization failure.'}
(E/'surface_compare.json').write_text(json.dumps(d,indent=2),encoding='utf8');print('R4_SURFACE_AUDIT',d['max_head_vertex_delta_above_z843_m'],max(d['max_expression_delta_difference_m'].values()),[(x['name'],x['deform_weight_sum_error']) for x in meshes],flush=True)
