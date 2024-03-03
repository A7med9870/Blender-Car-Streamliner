import bpy
import bmesh

class VIEW3D_PT_wheels_support_panel(bpy.types.Panel):
    """Creates a panel for wheels support"""
    bl_label = "Wheels Support"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "UE5CS"
    bl_order = 3

    def draw(self, context):
        layout = self.layout

        # Add a button to set origin to geometry
        layout.operator("my_operator.my_origin_operator", icon='OBJECT_ORIGIN')
        layout.operator("my_operator.my_set_originto_3d_cursor", icon='ORIENTATION_CURSOR')
        layout.operator("my_operator.set_origin_to_selected", icon='RESTRICT_SELECT_OFF')

class MyOriginOperator(bpy.types.Operator):
    """Operator to set origin to geometry"""
    bl_idname = "my_operator.my_origin_operator"
    bl_label = "Set Origin to Geometry"

    def execute(self, context):
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        return {'FINISHED'}

class MySetOriginTo3DCursor(bpy.types.Operator):
    """Moves origin to the cursor, helpful for brake pedals"""
    bl_idname = "my_operator.my_set_originto_3d_cursor"
    bl_label = "Set Origin to 3D Cursor"
    
    def execute(self, context):
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        return {'FINISHED'}

class MySetOriginToSelectedOperator(bpy.types.Operator):
    """Operator to set origin to selected"""
    bl_idname = "my_operator.set_origin_to_selected"
    bl_label = "Set Origin to Selected"

    @classmethod
    def poll(cls, context):
        return context.object is not None  # Ensure there is an active object

    def execute(self, context):
        if bpy.context.mode == 'EDIT_MESH':
            self.report({'ERROR'}, "This action is disabled in Edit Mode, you need to be in object mode to work")
            return {'CANCELLED'}

        bpy.ops.object.editmode_toggle()
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        return {'FINISHED'}

def register():
    bpy.utils.register_class(VIEW3D_PT_wheels_support_panel)
    bpy.utils.register_class(MyOriginOperator)
    bpy.utils.register_class(MySetOriginTo3DCursor)
    bpy.utils.register_class(MySetOriginToSelectedOperator)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_wheels_support_panel)
    bpy.utils.unregister_class(MyOriginOperator)
    bpy.utils.unregister_class(MySetOriginTo3DCursor)
    bpy.utils.unregister_class(MySetOriginToSelectedOperator)

if __name__ == "__main__":
    register()
