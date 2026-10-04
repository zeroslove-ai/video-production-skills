"""Actual evaluated source-owned left arm/digit contact cohorts, world triangles."""
import bpy,itertools
import numpy as np
from mathutils.bvhtree import BVHTree
class SurfaceOracle:
 def __init__(self):
  self.body=bpy.data.objects['Meshy_Body_NeutralCovered'];self.digits=['index','middle','ring','pinky','thumb'];lookup={self.body.vertex_groups[n+str(j)+'.L'].index:n for n in self.digits for j in [1,2,3]};self.cohorts={n:set() for n in self.digits}
  for v in self.body.data.vertices:
   scores={n:0 for n in self.digits}
   for g in v.groups:
    if g.group in lookup:scores[lookup[g.group]]+=g.weight
   n=max(scores,key=scores.get)
   if scores[n]>=.5:self.cohorts[n].add(v.index)
  hand=self.body.vertex_groups['hand.L'].index;fingers=set(lookup);self.hand_excluded={v.index for v in self.body.data.vertices if any((g.group in fingers or g.group==hand) and g.weight>.01 for g in v.groups)}
  armidx={self.body.vertex_groups[n].index for n in ['upper_arm.L','forearm.L','hand.L']};self.arm_excluded={v.index for v in self.body.data.vertices if any((g.group in fingers or g.group in armidx) and g.weight>.01 for g in v.groups)}
  for n in ['upper_arm.L','forearm.L','hand.L']:
   idx=self.body.vertex_groups[n].index;self.cohorts[n]={v.index for v in self.body.data.vertices if any(g.group==idx and g.weight>=.5 for g in v.groups)}
  self.topology=None
 def geometry(self,obj):
  e=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();m.calc_loop_triangles();a=np.empty(len(m.vertices)*3,np.float32);m.vertices.foreach_get('co',a);w=np.array(e.matrix_world);a=a.reshape(-1,3).astype(np.float64)@w[:3,:3].T+w[:3,3];assert np.isfinite(a).all();tri=[tuple(t.vertices) for t in m.loop_triangles];e.to_mesh_clear();return a,tri
 def capture(self):
  a,tri=self.geometry(self.body)
  if self.topology is None:self.topology=tri
  assert tri==self.topology
  ids={n:[i for i,t in enumerate(tri) if all(v in self.cohorts[n] for v in t)] for n in self.cohorts};ids['body_other']=[i for i,t in enumerate(tri) if all(v not in self.hand_excluded for v in t)];ids['arm_body_other']=[i for i,t in enumerate(tri) if all(v not in self.arm_excluded for v in t)];trees={n:BVHTree.FromPolygons(a.tolist(),[tri[i] for i in k],all_triangles=True,epsilon=0) for n,k in ids.items()};pairs={}
  checks=[*itertools.combinations(self.digits,2),*[(n,'body_other') for n in self.digits],*[(n,'arm_body_other') for n in ['upper_arm.L','forearm.L','hand.L']]]
  for x,y in checks:pairs[x+'__'+y]={(ids[x][i],ids[y][j]) for i,j in trees[x].overlap(trees[y])}
  for label,objname in [('head_surface','Character_Body_Head'),('hair_surface','Hair_Replacement_R4')]:
   h,ht=self.geometry(bpy.data.objects[objname]);tree=BVHTree.FromPolygons(h.tolist(),ht,all_triangles=True,epsilon=0)
   for n in self.cohorts:pairs[n+'__'+label]={(ids[n][i],j) for i,j in trees[n].overlap(tree)}
  return pairs
