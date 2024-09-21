import bpy
import bmesh

class VIEW3D_PT_positions_support_panel(bpy.types.Panel):
    bl_label = "Positions Support"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "UE5CS"
    bl_order = 4

    def draw(self, context):
        layout = self.layout

        # Add a button to reset the object's position to (0, 0, 0)
        layout.operator("my_operator.my_reset_position_operator", icon="META_CUBE")
        # Add a button to apply location transform
        layout.operator("my_operator.my_transform_apply_operator", icon='OUTLINER_DATA_EMPTY')
        # Add a button to reset the 3D cursor
        layout.operator("my_operator.my_reset_cursor_operator", icon='PIVOT_CURSOR')
        # Add a button to set the 3D cursor to the current or last selected object
        layout.operator("my_operator.my_cursor_to_object_operator", icon='CURSOR')
        layout.operator("my_operator.my_scale_apply", icon='SNAP_VOLUME')
        layout.operator("my_operator.myemptyaxis", icon='EMPTY_AXIS')

class MyResetPositionOperator(bpy.types.Operator):
    """Move Object To 0,0,0"""
    bl_idname = "my_operator.my_reset_position_operator"
    bl_label = "Obj 0,0,0 Position"

    def execute(self, context):
        # Reset the object's position
        bpy.context.object.location[0] = 0
        bpy.context.object.location[1] = 0
        bpy.context.object.location[2] = 0
        self.report({'INFO'}, 'Position has been rested')
        return {'FINISHED'}

class MyTransformApplyOperator(bpy.types.Operator):
    """Sets current location as the Default location"""
    bl_idname = "my_operator.my_transform_apply_operator"
    bl_label = "Apply Transform"

    def execute(self, context):
        # Apply location transform
        bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
        self.report({'INFO'}, 'Transform has been applied')
        return {'FINISHED'}

class MyResetCursorOperator(bpy.types.Operator):
    """Operator to reset the 3D cursor"""
    bl_idname = "my_operator.my_reset_cursor_operator"
    bl_label = "Reset Cursor"

    def execute(self, context):
        # Reset the 3D cursor to the origin
        bpy.context.scene.cursor.location = (0, 0, 0)
        self.report({'INFO'}, 'Cursor has been rested')
        return {'FINISHED'}

class MyCursorToObjectOperator(bpy.types.Operator):
    """Operator to set the 3D cursor to the current or last selected object"""
    bl_idname = "my_operator.my_cursor_to_object_operator"
    bl_label = "Cursor to Selected Object"

    def execute(self, context):
        # Get the last selected object
        selected_objects = bpy.context.selected_objects
        if len(selected_objects) > 0:
            obj = selected_objects[-1]
            bpy.context.scene.cursor.location = obj.location
        self.report({'INFO'}, 'Cursor has been set to the selected')
        return {'FINISHED'}

class MyScalingApply(bpy.types.Operator):
    """Scale apply, Fixes your Car collision being small"""
    bl_idname = "my_operator.my_scale_apply"
    bl_label = "Apply Object Scale"
    def execute(self,context):
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        self.report({'INFO'}, "Scale applying is Complete, your object should have now the proper scale inside Unreal")
        return {'FINISHED'}

class Myaddemptyplainaxis(bpy.types.Operator):
    """Adds a plain axis in selected area"""
    bl_idname = "my_operator.myemptyaxis"
    bl_label = "Add Box to selected"
    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', scale=(4, 4, 4))
        return {'FINISHED'}

def register():
    bpy.utils.register_class(VIEW3D_PT_positions_support_panel)
    bpy.utils.register_class(MyResetPositionOperator)
    bpy.utils.register_class(MyTransformApplyOperator)
    bpy.utils.register_class(MyResetCursorOperator)
    bpy.utils.register_class(MyCursorToObjectOperator)
    bpy.utils.register_class(MyScalingApply)
    bpy.utils.register_class(Myaddemptyplainaxis)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_positions_support_panel)
    bpy.utils.unregister_class(MyResetPositionOperator)
    bpy.utils.unregister_class(MyTransformApplyOperator)
    bpy.utils.unregister_class(MyResetCursorOperator)
    bpy.utils.unregister_class(MyCursorToObjectOperator)
    bpy.utils.unregister_class(MyScalingApply)
    bpy.utils.unregister_class(Myaddemptyplainaxis)

if __name__ == "__main__":
    register()
