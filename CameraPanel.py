import bpy
import bmesh
import webbrowser
from mathutils import Vector
from bpy.props import (StringProperty, PointerProperty, EnumProperty, BoolProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)


class VIEW3D_PT_Camera_support_panel(bpy.types.Panel):
    """Creates a panel for Camera support"""
    bl_label = "Camera Support"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "UE5CS"
    bl_order = 6
    
    @classmethod
    def poll(cls, context):
        preferences = context.preferences.addons['UE_Car_Streamliner'].preferences
        return preferences.show_Camera_panel

    def draw(self, context):
        layout = self.layout
        # Clip the camera to the new unit scale
        if bpy.context.space_data.clip_end < 10000:
            layout.operator("my_operator.my_clipend_operator", icon='OUTLINER_OB_CAMERA')
            layout.label(text="to view far")
        if bpy.context.space_data.clip_end == 10000:   
            layout.label(text="View is good")
  
class MyClipEndOperator(bpy.types.Operator):
    """Set the clip end value"""
    bl_idname = "my_operator.my_clipend_operator"
    bl_label = "Set Clip End"

    def execute(self, context):
        # Set the clip end value for the active 3D Viewport
        space = bpy.context.space_data
        if space.type == 'VIEW_3D':
            space.clip_end = 10000
        return {'FINISHED'}

classes = (
    VIEW3D_PT_Camera_support_panel,
    MyClipEndOperator,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
