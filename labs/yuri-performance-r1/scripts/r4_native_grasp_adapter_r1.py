"""Fixed three-rig Action binding on immutable R4. Restore all raw poses on OFF."""
from r4_appearance_adapter import ReactionLane
ACTIONS={'Meshy_Fitted_Rig':'YURI_R4_NATIVE_GRASP_HAND_EXISTING_ACTION_R1','Armature':'YURI_R4_NATIVE_GRASP_HAND_HEAD_TRANSPORT_R1','Hair_Rig_R4':'YURI_R4_NATIVE_GRASP_HAND_HAIR_TRANSPORT_R1'}
class NativeGraspLane:
 def on(self):
  self.lanes=[]
  for obj,name in ACTIONS.items():lane=ReactionLane(obj);lane.on(name);self.lanes.append(lane)
 def off(self):
  for lane in reversed(self.lanes):lane.off()
