"""Small fixed C1/left-finger transient NLA recipe; no general layer framework."""
import bpy
from r4_appearance_adapter import ReactionLane
BODY='YURI_R4_C1_REACH_BODY_R1';FINGER='YURI_R4_C1_LEFT_PREGRASP_FINGERS_R1'
TRANSPORT={'Armature':'YURI_R4_C1_REACH_BODY_HEAD_TRANSPORT_R1','Hair_Rig_R4':'YURI_R4_C1_REACH_BODY_HAIR_TRANSPORT_R1'}
ROOT='YURI_R4_C1_REACH_ROOT_PATH_R1'
class ReachFingerLane:
 def on(self,include_fingers=True):
  self.lanes=[];self.track=None;self.carrier=bpy.data.objects['Assembly_Root'];ad=self.carrier.animation_data;self.saved={'had_ad':ad is not None,'action':ad.action if ad else None,'slot':ad.action_slot if ad else None,'handle':ad.action_slot_handle if ad else 0,'last':ad.last_slot_identifier if ad else '', 'location':self.carrier.location.copy()}
  for obj,name in {'Meshy_Fitted_Rig':BODY,**TRANSPORT}.items():
   lane=ReactionLane(obj);lane.on(name);self.lanes.append(lane)
  ad=self.carrier.animation_data_create();ad.action=bpy.data.actions[ROOT];ad.action_slot=ad.action.slots[0]
  if include_fingers:
   rig=bpy.data.objects['Meshy_Fitted_Rig'];ad=rig.animation_data;assert not ad.nla_tracks, 'Existing NLA ownership would need a separate consumer decision'
   self.track=ad.nla_tracks.new();self.track.name='C1_REACH_LEFT_FINGER_SOURCE_ONLY_R1';strip=self.track.strips.new('R4_LEFT_FINGER_CLOCK_1_TO_61',1,bpy.data.actions[FINGER]);strip.action_slot=bpy.data.actions[FINGER].slots[0];strip.action_frame_start=1;strip.action_frame_end=61;strip.scale=1;strip.frame_start=1;strip.frame_end=61;strip.blend_type='REPLACE';strip.extrapolation='HOLD';strip.influence=1
  bpy.context.scene.frame_set(1);bpy.context.view_layer.update()
 def off(self):
  if self.track is not None:bpy.data.objects['Meshy_Fitted_Rig'].animation_data.nla_tracks.remove(self.track);self.track=None
  for lane in reversed(self.lanes):lane.off()
  v=self.saved;ad=self.carrier.animation_data;ad.action=v['action']
  if v['action'] and v['slot']:ad.action_slot=v['slot']
  ad.action_slot_handle=v['handle'];ad.last_slot_identifier=v['last'];self.carrier.location=v['location']
  if not v['had_ad']:self.carrier.animation_data_clear()
  bpy.context.view_layer.update()
