import bpy
import bmesh
import webbrowser
from mathutils import Vector
from bpy.props import (StringProperty, PointerProperty, EnumProperty, BoolProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

class VIEW3D_PT_MeshManpltion_panel(bpy.types.Panel):
    """Creates a panel in the 3D Viewport"""
    bl_space_type = "VIEW_3D"  # 3D Viewport area
    bl_region_type = "UI"  # Sidebar region
    bl_label = "Mesh Miniplation"  # Panel label
    bl_category = "UE5CS"
    bl_order = 2
    
    def draw(self, context):
        """Defines the layout of the panel"""
        layout = self.layout
        row = layout.row()
        row.operator("my_operator.my_cut_operator_plus", icon='PARTICLEMODE')
        row.operator("my_operator.my_cut_operator_neg", icon='PARTICLEMODE')

        # Add a button to add Mirror modifier
        layout.operator("my_operator.my_mirror_operator",icon='MOD_MIRROR')

        # Add a button to add Decimate modifier
        layout.operator("my_operator.my_decimate_operator", icon='MOD_DECIM')
        scene = context.scene


class MyCutOperatorplus(bpy.types.Operator):
    """cuts the object in half, with anything in right side of facing dirction"""
    bl_idname = "my_operator.my_cut_operator_plus"  # Changed bl_idname
    bl_label = "Cut +X"

    def execute(self, context):
        # Get the last selected object
        selected_objects = bpy.context.selected_objects
        if len(selected_objects) > 0:
            obj = selected_objects[-1]
        else:
            return  # No selected object

        # Switch to Edit mode
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')

        # Select all vertices
        bpy.ops.mesh.select_all(action='SELECT')

        # Cut the object along the X axis
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(0, 1, 0), clear_inner=True)

        # Switch back to Object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, "Cut is Compelete")
        return {'FINISHED'}

class MyCutOperatorNeg(bpy.types.Operator):
    """cuts the object in half, with anything in right side of facing dirction"""
    bl_idname = "my_operator.my_cut_operator_neg"  # Changed bl_idname
    bl_label = "Cut -X"


    def execute(self, context):
        # Get the last selected object
        selected_objects = bpy.context.selected_objects
        if len(selected_objects) > 0:
            obj = selected_objects[-1]
        else:
            return  # No selected object

        # Switch to Edit mode
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')

        # Select all vertices
        bpy.ops.mesh.select_all(action='SELECT')

        # Cut the object along the X axis
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(0, -1, 0), clear_inner=True)

        # Switch back to Object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, "Cut is Compelete")
        return {'FINISHED'}


class MyMirrorOperator(bpy.types.Operator):
    """adds Mirror modifier"""
    bl_idname = "my_operator.my_mirror_operator"
    bl_label = "Add Mirror Y"

    def execute(self, context):    
        # Get the last selected object
        selected_objects = bpy.context.selected_objects
        if len(selected_objects) > 0:
            obj = selected_objects[-1]
        else:
            return  # No selected object

        # Add Mirror modifier with Y-axis mirror
        mirror_modifier = obj.modifiers.new(name="Mirror", type='MIRROR')
        mirror_modifier.use_axis[1] = True
        mirror_modifier.use_axis[0] = False  # Disable X-axis mirroring
        mirror_modifier.use_bisect_axis[0] = False
        return {'FINISHED'}

class MyDecimateOperator(bpy.types.Operator):
    """Operator to add Decimate modifier"""
    bl_idname = "my_operator.my_decimate_operator"
    bl_label = "Add Modifier"

    def execute(self, context):
        # Get the last selected object
        selected_objects = bpy.context.selected_objects
        if len(selected_objects) > 0:
            obj = selected_objects[-1]
        else:
            return  # No selected object

        # Add Decimate modifier with ratio 0.05
        decimate_modifier = obj.modifiers.new(name="Decimate", type='DECIMATE')
        decimate_modifier.ratio = 0.5
        return {'FINISHED'}


def register():
    bpy.utils.register_class(VIEW3D_PT_MeshManpltion_panel)
    bpy.utils.register_class(MyCutOperatorplus)
    bpy.utils.register_class(MyCutOperatorNeg)
    bpy.utils.register_class(MyMirrorOperator)
    bpy.utils.register_class(MyDecimateOperator)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_MeshManpltion_panel)
    bpy.utils.unregister_class(MyCutOperatorplus)
    bpy.utils.unregister_class(MyCutOperatorNeg)
    bpy.utils.unregister_class(MyMirrorOperator)
    bpy.utils.unregister_class(MyDecimateOperator)

if __name__ == "__main__":
    register()