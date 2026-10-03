"""Bind existing R4 Actions only; restore the complete previous body pose/binding.

No objects, meshes, rig bones, constraints, materials, drivers or weights created.
Use on the ORIGINAL R4 hierarchy, never the experimental merged GameRig.
"""
import bpy

class ReactionLane:
    def __init__(self, rig_name='Meshy_Fitted_Rig'):
        self.rig=bpy.data.objects[rig_name]
        self.scene=bpy.context.scene
        self.saved=None

    def on(self, action_name):
        if self.saved is None:
            ad=self.rig.animation_data
            self.saved={'frame':self.scene.frame_current,'subframe':self.scene.frame_subframe,
                'had_ad':ad is not None,'action':ad.action if ad else None,
                'slot':ad.action_slot if ad else None,
                'slot_handle':ad.action_slot_handle if ad else 0,
                'last_slot_identifier':ad.last_slot_identifier if ad else '',
                'pose':{b.name:(b.rotation_mode,tuple(b.location),tuple(b.rotation_quaternion),
                    tuple(b.rotation_euler),tuple(b.rotation_axis_angle),tuple(b.scale)) for b in self.rig.pose.bones}}
        a=bpy.data.actions[action_name]
        ad=self.rig.animation_data_create()
        ad.action=a
        slot=next((s for s in a.slots if s.target_id_type=='OBJECT' and s.identifier=='OB'+self.rig.name),None)
        if slot is None:slot=next(s for s in a.slots if s.target_id_type=='OBJECT')
        ad.action_slot=slot
        # Existing R4 uses quaternion body bones. Do not reset helper bind bones.
        self.scene.frame_set(1)
        bpy.context.view_layer.update()
        return a

    def off(self):
        if self.saved is None:return
        v=self.saved;ad=self.rig.animation_data
        ad.action=v['action']
        if v['action'] and v['slot']:ad.action_slot=v['slot']
        ad.action_slot_handle=v['slot_handle']
        ad.last_slot_identifier=v['last_slot_identifier']
        self.scene.frame_set(v['frame'],subframe=v['subframe'])
        for name,pose in v['pose'].items():
            b=self.rig.pose.bones[name]
            b.rotation_mode,b.location,b.rotation_quaternion,b.rotation_euler,b.rotation_axis_angle,b.scale=pose
        if not v['had_ad']:self.rig.animation_data_clear()
        bpy.context.view_layer.update()
        self.saved=None
