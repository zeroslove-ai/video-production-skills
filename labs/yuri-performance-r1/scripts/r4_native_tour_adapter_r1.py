"""Original R4 native Tour BODY + existing head/hair root transport only."""
from r4_appearance_adapter import ReactionLane
ACTIONS={'Meshy_Fitted_Rig':'YURI_R4_NATIVE_TOUR_BODY_R1','Armature':'YURI_R4_NATIVE_TOUR_HEAD_R1','Hair_Rig_R4':'YURI_R4_NATIVE_TOUR_HAIR_R1'}
class NativeTourLane:
 def on(self):
  self.lanes=[]
  for ob,a in ACTIONS.items():
   ln=ReactionLane(ob);ln.on(a);self.lanes.append(ln)
 def off(self):
  for ln in reversed(self.lanes):ln.off()
