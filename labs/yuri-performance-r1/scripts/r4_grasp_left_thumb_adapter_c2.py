"""Separate thumb-opposition source copy, fixed bindings on original three rigs."""
from r4_appearance_adapter import ReactionLane
ACTIONS={'Meshy_Fitted_Rig':'YURI_R4_GRASP_LEFT_THUMB_OPPOSITION_BODY_C2','Armature':'YURI_R4_NATIVE_GRASP_HAND_HEAD_TRANSPORT_R1','Hair_Rig_R4':'YURI_R4_NATIVE_GRASP_HAND_HAIR_TRANSPORT_R1'}
class ThumbLane:
 def on(self):
  self.lanes=[]
  for obj,name in ACTIONS.items():x=ReactionLane(obj);x.on(name);self.lanes.append(x)
 def off(self):
  for x in reversed(self.lanes):x.off()
