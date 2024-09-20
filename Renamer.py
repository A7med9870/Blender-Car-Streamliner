import bpy

class AddTextToObjectNameOperator(bpy.types.Operator):
    bl_idname = "object.add_text_to_object_name"
    bl_label = "Add Text to Object Name"
    def execute(self, context):
        text_to_add = context.scene.text_to_add
        for obj in context.selected_objects:
            obj.name += "" + text_to_add
        return {'FINISHED'}

class OBJECT_PT_add_text_panel(bpy.types.Panel):
    bl_label = "ExtraName"
    bl_idname = "OBJECT_PT_add_text_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'UE5CS'
    bl_order = 9

    @classmethod
    def poll(cls, context):
        preferences = context.preferences.addons['Blender-Car-Streamliner'].preferences
        return preferences.show_ExtraName_panel
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Add text to selected")
        row = layout.row()
        row.label(text="object(s) name:")
        row = layout.row()
        row.prop(context.scene, "text_to_add")
        row = layout.row()
        row.operator("object.add_text_to_object_name", text="Add Text")

def register():
    bpy.types.Scene.text_to_add = bpy.props.StringProperty(name="Text", default="Enter text")
    bpy.utils.register_class(AddTextToObjectNameOperator)
    bpy.utils.register_class(OBJECT_PT_add_text_panel)

def unregister():
    del bpy.types.Scene.text_to_add
    bpy.utils.unregister_class(AddTextToObjectNameOperator)
    bpy.utils.unregister_class(OBJECT_PT_add_text_panel)

if __name__ == "__main__":
    register()
