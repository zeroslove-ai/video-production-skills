"""Original-rig four-Action R1 binder; accumulated cycles are in Action modifiers."""
import bpy
from r4_appearance_adapter import ReactionLane
ACTIONS={'Meshy_Fitted_Rig':'YURI_R4_SIT_STAND_BODY_R1','Armature':'YURI_R4_SIT_STAND_HEAD_R1','Hair_Rig_R4':'YURI_R4_SIT_STAND_HAIR_R1','Assembly_Root':'YURI_R4_SIT_STAND_PATH_R1'}
class SitStandLane:
 def __init__(self,mapping=None):self.mapping=mapping or ACTIONS
 def on(self):
  ob=bpy.data.objects['Assembly_Root'];ad=ob.animation_data;self.root=ob;self.saved={'had_ad':ad is not None,'action':ad.action if ad else None,'slot':ad.action_slot if ad else None,'handle':ad.action_slot_handle if ad else 0,'last':ad.last_slot_identifier if ad else '', 'location':ob.location.copy()};self.lanes=[]
  for name in ['Meshy_Fitted_Rig','Armature','Hair_Rig_R4']:
   ln=ReactionLane(name);ln.on(self.mapping[name]);self.lanes.append(ln)
  ad=ob.animation_data_create();ad.action=bpy.data.actions[self.mapping[ob.name]];ad.action_slot=next(x for x in ad.action.slots if x.target_id_type=='OBJECT' and x.identifier=='OB'+ob.name);bpy.context.scene.frame_set(1);bpy.context.view_layer.update()
 def off(self):
  ad=self.root.animation_data;v=self.saved;ad.action=v['action']
  if v['action'] and v['slot']:ad.action_slot=v['slot']
  ad.action_slot_handle=v['handle'];ad.last_slot_identifier=v['last'];self.root.location=v['location']
  if not v['had_ad']:self.root.animation_data_clear()
  for ln in reversed(self.lanes):ln.off()
  bpy.context.view_layer.update()
