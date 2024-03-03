import bpy

class VIEW3D_PT_A7med_Tips(bpy.types.Panel):
    bl_label = "Tips"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "UE5CS"
    bl_order = 10

    @classmethod
    def poll(cls, context):
        preferences = context.preferences.addons['UE_Car_Streamliner'].preferences
        return preferences.show_tips_panel

    def draw(self, context):
        layout = self.layout
        layout.label(text="-Wheels go with Front left, Front right")

def register():
    bpy.utils.register_class(VIEW3D_PT_A7med_Tips)
    # Register other classes

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_A7med_Tips)
    # Unregister other classes
