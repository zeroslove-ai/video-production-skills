"""Bind three additive Walk Actions on immutable original R4; restore raw state."""
from r4_appearance_adapter import ReactionLane
ACTIONS={'Meshy_Fitted_Rig':'YURI_R4_NATIVE_WALK_EXISTING_ACTION_R1','Armature':'YURI_R4_NATIVE_WALK_HEAD_TRANSPORT_R1','Hair_Rig_R4':'YURI_R4_NATIVE_WALK_HAIR_TRANSPORT_R1'}
class NativeWalkLane:
 def on(self):
  self.lanes=[]
  for obj,n in ACTIONS.items():
   lane=ReactionLane(obj);lane.on(n);self.lanes.append(lane)
 def off(self):
  for lane in reversed(self.lanes):lane.off()
