import bpy
import bmesh
from bpy.props import PointerProperty

class VIEW3D_PT_my_References_panel(bpy.types.Panel):
    """Creates a panel in the 3D Viewport"""
    bl_space_type = "VIEW_3D"  # 3D Viewport area
    bl_region_type = "UI"  # Sidebar region
    bl_label = "References"  # Panel label
    bl_category = "UE5CS"
    bl_order = 1
    @classmethod
    def poll(cls, context):
        preferences = bpy.context.preferences.addons['UE_Car_Streamliner'].preferences
        return preferences.dropdown_enum1 == "OPTION1"
    def draw(self, context):
        """Defines the layout of the panel"""
        layout = self.layout
        scn = context.scene
        scene = context.scene
        layout.label(text="Creates a box to", icon='MESH_CUBE')
        layout.label(text="reference your car towards")
        row = layout.row()
        row.operator("my_operator.my_car_reference_operator", icon='AUTO')
        row.operator("my_operator.my_tires_operator", icon='PROP_CON')
        #Add a button to refernce your car to
        if scene.unit_settings.scale_length == 1:
            layout.operator("my_operator.my_unitscale_operator", icon='IMAGE_BACKGROUND')
        elif scene.unit_settings.scale_length != 0.009999999776482582 and scene.unit_settings.scale_length != 1:
            layout.operator("my_operator.my_unitscale_operator", icon='IMAGE_BACKGROUND')

class VIEW3D_PT_my_References_panel36(bpy.types.Panel):
    """Creates a panel in the 3D Viewport"""
    bl_space_type = "VIEW_3D"  # 3D Viewport area
    bl_region_type = "UI"  # Sidebar region
    bl_label = "References"  # Panel label
    bl_category = "UE5CS"
    bl_order = 1
    @classmethod
    def poll(cls, context):
        preferences = bpy.context.preferences.addons['UE_Car_Streamliner'].preferences
        return preferences.dropdown_enum1 == "OPTION2"
    def draw(self, context):
        """Defines the layout of the panel"""
        layout = self.layout
        scn = context.scene
        scene = context.scene
        layout.label(text="Creates a box to", icon='MESH_CUBE')
        layout.label(text="reference your car towards")
        row = layout.row()
        row.operator("my_operator.my_car_reference_operator36", icon='AUTO')
        row.operator("my_operator.my_tires_operator36", icon='PROP_CON')
        if scene.unit_settings.scale_length == 1:
            layout.operator("my_operator.my_unitscale_operator", icon='IMAGE_BACKGROUND')
        elif scene.unit_settings.scale_length != 0.009999999776482582 and scene.unit_settings.scale_length != 1:
            layout.operator("my_operator.my_unitscale_operator", icon='IMAGE_BACKGROUND')


class MyTiresReference(bpy.types.Operator):
    """Please don't forget separating each tire and setting the correct origin"""
    bl_idname = "my_operator.my_tires_operator"
    bl_label = "Tires"

    def execute(self, context):
        bpy.ops.mesh.primitive_cylinder_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.name = "Tires"
        bpy.ops.transform.rotate(value=-1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, alt_navigation=True)
        bpy.ops.transform.resize(value=(50, 5, 50), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, alt_navigation=True)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.transform.translate(value=(147.62, 8.08377e-06, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, alt_navigation=True)
        bpy.ops.transform.translate(value=(0, 100, 45.6785), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, alt_navigation=True)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        # Add Mirror modifier with Y-axis mirror
        obj = bpy.context.object
        mirror_modifier = obj.modifiers.new(name="Mirror", type='MIRROR')
        mirror_modifier.use_axis[1] = True
        mirror_modifier.use_axis[0] = False  # Disable X-axis mirroring
        mirror_modifier.use_bisect_axis[0] = False

        # Add Array modifier
        array_modifier = obj.modifiers.new(name="Array", type='ARRAY')
        array_modifier.relative_offset_displace[0] = -2.7
        
        bpy.ops.object.modifier_apply(modifier="Mirror", report=True)
        bpy.ops.object.modifier_apply(modifier="Array", report=True)
        bpy.ops.object.editmode_toggle()        
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        return {'FINISHED'}

class MyUnitScale(bpy.types.Operator):
    """Sets the scale of world to correct scale to export to unreal"""
    bl_idname = "my_operator.my_unitscale_operator"
    bl_label = "Set Unit Scale"
    def execute(self, context):    
        bpy.context.scene.unit_settings.scale_length = 0.01
        return {'FINISHED'}


class MyCarReferenceOperator(bpy.types.Operator):
    """Creates a box to reference your car towards"""
    bl_idname = "my_operator.my_car_reference_operator"
    bl_label = "Car"

    def execute(self, context):
        bpy.context.scene.cursor.location = (0, 0, 0)
        # Create a new mesh object (a box)
        bpy.ops.mesh.primitive_cube_add(size=2)
        bpy.context.object.name = "Car_Refernce"
        # Get the active object (the newly created box)
        obj = bpy.context.active_object
        # Enter edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        # Get the mesh data of the object
        mesh = obj.data
        bm = bmesh.from_edit_mesh(mesh)
        # Deselect all faces
        for f in bm.faces:
            f.select = False
        # Apply the deselection
        bmesh.update_edit_mesh(mesh)
        # Select faces facing the X-axis
        for f in bm.faces:
            if f.normal.x == 1.0:  # Check if the face normal is facing the X-axis
                f.select = True
                # Move selected faces along the X-axis by 2 units
                bpy.ops.transform.translate(value=(2, 0, 0))
            elif f.normal.x == -1.0:  # Check if the face normal is facing the -X-axis
                f.select = True
                # Move selected faces along the X-axis by -3 units (negative direction)
                bpy.ops.transform.translate(value=(-2.5, 0, 0))
        # Apply the selection
        bmesh.update_edit_mesh(mesh)
        bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts":1, "smoothness":0, "falloff":'INVERSE_SQUARE', "object_index":0, "edge_index":5, "mesh_select_mode_init":(False, True, False)}, TRANSFORM_OT_edge_slide={"value":0, "single_side":False, "use_even":False, "flipped":False, "use_clamp":True, "mirror":True, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "correct_uv":True, "release_confirm":False, "use_accurate":False, "alt_navigation":False})
        bpy.ops.transform.edge_slide(value=0.380081, mirror=True, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, correct_uv=True, alt_navigation=True)
        bpy.ops.transform.translate(value=(0, 0, 0.290866), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, alt_navigation=True)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.translate(value=(0, 0, 100.14405), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, alt_navigation=True)
        bpy.ops.object.modifier_add(type='WIREFRAME')
        bpy.context.object.modifiers["Wireframe"].thickness = 1
        # Return to object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        # Scale the entire object by 0.2 on the Y-axis
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
        obj.select_set(True)  # Select the current object
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')  # Set the origin to the center of mass
        bpy.ops.transform.resize(value=(100, 100.2, 70), orient_type='GLOBAL')  # Scale the object
        bpy.ops.object.transform_apply(location=True, rotation=False, scale=True)
        return {'FINISHED'}


class MyCarReferenceOperator36(bpy.types.Operator):
    """Creates a box to reference your car towards"""
    bl_idname = "my_operator.my_car_reference_operator36"
    bl_label = "Car"

    def execute(self, context):
        bpy.context.scene.cursor.location = (0, 0, 0)
        # Create a new mesh object (a box)
        bpy.ops.mesh.primitive_cube_add(size=2)
        bpy.context.object.name = "Car_Refernce"


        # Get the active object (the newly created box)
        obj = bpy.context.active_object

        # Enter edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Get the mesh data of the object
        mesh = obj.data
        bm = bmesh.from_edit_mesh(mesh)

        # Deselect all faces
        for f in bm.faces:
            f.select = False

        # Apply the deselection
        bmesh.update_edit_mesh(mesh)

        # Select faces facing the X-axis
        for f in bm.faces:
            if f.normal.x == 1.0:  # Check if the face normal is facing the X-axis
                f.select = True
                # Move selected faces along the X-axis by 2 units
                bpy.ops.transform.translate(value=(2, 0, 0))
            elif f.normal.x == -1.0:  # Check if the face normal is facing the -X-axis
                f.select = True
                # Move selected faces along the X-axis by -3 units (negative direction)
                bpy.ops.transform.translate(value=(-2.5, 0, 0))

        # Apply the selection
        bmesh.update_edit_mesh(mesh)
        
        
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.transform.edge_slide(value=0.380081, mirror=True, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, correct_uv=True)
        bpy.ops.transform.translate(value=(0, 0, 0.290866), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.translate(value=(0, 0, 100.14405), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
        bpy.ops.object.modifier_add(type='WIREFRAME')
        bpy.context.object.modifiers["Wireframe"].thickness = 1



        # Return to object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Scale the entire object by 0.2 on the Y-axis
        bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
        obj.select_set(True)  # Select the current object
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')  # Set the origin to the center of mass
        bpy.ops.transform.resize(value=(100, 100.2, 70), orient_type='GLOBAL')  # Scale the object
        bpy.ops.object.transform_apply(location=True, rotation=False, scale=True)
        return {'FINISHED'}


class MyTiresReference36(bpy.types.Operator):
    """Please don't forget separating each tire and setting the correct origin"""
    bl_idname = "my_operator.my_tires_operator36"
    bl_label = "Tires"

    def execute(self, context):
        bpy.ops.mesh.primitive_cylinder_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.name = "Tires"
        bpy.ops.transform.rotate(value=-1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
        bpy.ops.transform.resize(value=(50, 5, 50), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.transform.translate(value=(147.62, 8.08377e-06, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, False), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
        bpy.ops.transform.translate(value=(0, 100, 45.6785), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        # Add Mirror modifier with Y-axis mirror
        obj = bpy.context.object
        mirror_modifier = obj.modifiers.new(name="Mirror", type='MIRROR')
        mirror_modifier.use_axis[1] = True
        mirror_modifier.use_axis[0] = False  # Disable X-axis mirroring
        mirror_modifier.use_bisect_axis[0] = False
        # Add Array modifier
        array_modifier = obj.modifiers.new(name="Array", type='ARRAY')
        array_modifier.relative_offset_displace[0] = -2.7
        bpy.ops.object.modifier_apply(modifier="Mirror", report=True)
        bpy.ops.object.modifier_apply(modifier="Array", report=True)
        bpy.ops.object.editmode_toggle()        
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        return {'FINISHED'}


def register():
    bpy.utils.register_class(VIEW3D_PT_my_References_panel)
    bpy.utils.register_class(MyTiresReference)
    bpy.utils.register_class(MyUnitScale)
    bpy.utils.register_class(MyCarReferenceOperator)
    bpy.utils.register_class(VIEW3D_PT_my_References_panel36)
    bpy.utils.register_class(MyTiresReference36)
    bpy.utils.register_class(MyCarReferenceOperator36)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_my_References_panel)
    bpy.utils.unregister_class(MyTiresReference)
    bpy.utils.unregister_class(MyUnitScale)
    bpy.utils.unregister_class(MyCarReferenceOperator)
    bpy.utils.unregister_class(VIEW3D_PT_my_References_panel36)
    bpy.utils.unregister_class(MyTiresReference36)
    bpy.utils.unregister_class(MyCarReferenceOperator36)
    
if __name__ == "__main__":
    register()
