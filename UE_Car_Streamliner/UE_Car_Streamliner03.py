bl_info = {
    "name" : "UE Car modeling Helper",
    "author" : "A7med9870",
    "description" : "Helps with building a car with right scale and settings for unreal engine",
    "blender" : (4, 0, 0),
    "version" : (0, 0, 3),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}


import bpy
import bmesh
import webbrowser
from mathutils import Vector
from bpy.props import (StringProperty, PointerProperty, EnumProperty, BoolProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

def cut_mirror_and_decimate():
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

def add_mirror_modifier():
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

def add_decimate_modifier():
    # Get the last selected object
    selected_objects = bpy.context.selected_objects
    if len(selected_objects) > 0:
        obj = selected_objects[-1]
    else:
        return  # No selected object

    # Add Decimate modifier with ratio 0.05
    decimate_modifier = obj.modifiers.new(name="Decimate", type='DECIMATE')
    decimate_modifier.ratio = 0.5

class VIEW3D_PT_my_Welcoming_panel(bpy.types.Panel):
    """Creates a custom panel in the 3D Viewport"""
    bl_space_type = "VIEW_3D"  # 3D Viewport area
    bl_region_type = "UI"  # Sidebar region
    bl_label = "UE5 Cars Modeling Streamlinear"  # Panel label
    bl_category = "UE5CMS"
    bl_order = 10
    icon='MOD_DECIM'

    def draw(self, context):
        """Defines the layout of the panel"""
        layout = self.layout
        layout.operator("my_operator.open_url", text="By A7med9870").url = "https://www.youtube.com/@A7med9870"
        layout.operator("my_operator.open_url", text="YT Tutorial Playlist").url = "https://youtu.be/_RQuv0_pWFs?list=PLSgjCbppcrmXvVqM1zvBN5j7n6MQ6iU1l"
        layout.label(text="Credits")
        layout.label(text="For Legit inspiration")
        layout.operator("my_operator.open_url", text="Sina Qadri").url = "https://www.youtube.com/channel/UCCJIOWZkxTimMVtOp-FMHEA"
        layout.label(text="For Exporter")
        layout.operator("my_operator.open_url", text="To POLYCOSM").url = "https://polycosm.gumroad.com/l/BatchExporterAddon?layout=profile"
        layout.label(text="For Great tutorials")
        layout.operator("my_operator.open_url", text="Royal Skies").url = "https://www.youtube.com/@TheRoyalSkies"
        layout.label(text="For Great UE Car tutorials")
        layout.operator("my_operator.open_url", text="Math B").url = "https://www.youtube.com/@MathB_Official"
        layout.label(text="Recommended to use with")
        layout.label(text="Continuebreak Addon")
        layout.operator("my_operator.open_url", text="Continuebreak Addonq").url = "https://continuebreak.gumroad.com/l/uYsaQ?layout=profile&recommended_by=library"

class VIEW3D_PT_my_References_panel(bpy.types.Panel):
    """Creates a panel in the 3D Viewport"""
    bl_space_type = "VIEW_3D"  # 3D Viewport area
    bl_region_type = "UI"  # Sidebar region
    bl_label = "References"  # Panel label
    bl_category = "UE5CMS"
    bl_order = 1
    def draw(self, context):
        """Defines the layout of the panel"""
        layout = self.layout
        scn = context.scene
        scene = context.scene
        layout.label(text="Creates a box to", icon='MESH_CUBE')
        layout.label(text="reference your car towards")
        #Add a button to refernce your car to
        layout.operator("my_operator.my_car_reference_operator", icon='AUTO')
        # Add a button to create Tires refernce
        layout.operator("my_operator.my_tires_operator",icon='PROP_CON')
        if scene.unit_settings.scale_length == 1:
            layout.operator("my_operator.my_unitscale_operator", icon='IMAGE_BACKGROUND')
        elif scene.unit_settings.scale_length != 0.009999999776482582 and scene.unit_settings.scale_length != 1:
            layout.operator("my_operator.my_unitscale_operator", icon='IMAGE_BACKGROUND')
    
class VIEW3D_PT_MeshManpltion_panel(bpy.types.Panel):
    """Creates a panel in the 3D Viewport"""
    bl_space_type = "VIEW_3D"  # 3D Viewport area
    bl_region_type = "UI"  # Sidebar region
    bl_label = "Mesh Miniplation"  # Panel label
    bl_category = "UE5CMS"
    bl_order = 2
    
    def draw(self, context):
        """Defines the layout of the panel"""
        layout = self.layout
        # Add a button to cut, mirror, and decimate the object
        layout.operator("my_operator.my_button_operator", icon='PARTICLEMODE')

        # Add a button to add Mirror modifier
        layout.operator("my_operator.my_mirror_operator", icon='MOD_MIRROR')

        # Add a button to add Decimate modifier
        layout.operator("my_operator.my_decimate_operator", icon='MOD_DECIM')
        scene = context.scene

class VIEW3D_PT_wheels_support_panel(bpy.types.Panel):
    """Creates a panel for wheels support"""
    bl_label = "Wheels Support"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "UE5CMS"
    bl_order = 3

    def draw(self, context):
        layout = self.layout

        # Add a button to set origin to geometry
        layout.operator("my_operator.my_origin_operator", icon='OBJECT_ORIGIN')
        layout.operator("my_operator.my_set_originto_3d_cursor", icon='ORIENTATION_CURSOR')
        layout.operator("my_operator.set_origin_to_selected", icon='RESTRICT_SELECT_OFF')
        # Remove the code that sets the enabled attribute
        # operator.enabled = True
        #if bpy.context.mode == 'EDIT_MESH':
        #   operator.enabled = False
            
class VIEW3D_PT_positions_support_panel(bpy.types.Panel):
    bl_label = "Positions Support"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "UE5CMS"
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

class VIEW3D_PT_my_Export_panel(bpy.types.Panel):
    bl_label = "Export Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "UE5CMS"
    bl_order = 7

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        scene = context.scene
        layout.label(text="By polycosm")
        layout.label(text="Export Path Location:", icon='EXPORT')
        layout.prop(scn.my_tool, "path", text="")
        layout.label(text="UNCHECK RELATIVE PATH")
        layout.label(text="IN TOP RIGHT SIDE", icon='PREFERENCES')
        
        if scene.unit_settings.scale_length == 0.009999999776482582:
            layout.operator("myops.combined_exporter", text='Export Only Selected', icon='TRIA_RIGHT')
        elif scene.unit_settings.scale_length == 1:
            layout.label(text="EXPORT BUTTON WILL") 
            layout.label(text="SHOW UP IF YOU")
            layout.label(text="SET PRESS UNIT SCALE")
            layout.operator("my_operator.my_unitscale_operator", icon='IMAGE_BACKGROUND')
        elif scene.unit_settings.scale_length != 0.009999999776482582 and scene.unit_settings.scale_length != 1:
            # This block will only execute if neither of the above conditions are true
            layout.label(text="EXPORT BUTTON WILL") 
            layout.label(text="SHOW UP IF YOU")
            layout.label(text="SET PRESS UNIT SCALE")
            layout.operator("my_operator.my_unitscale_operator", icon='IMAGE_BACKGROUND')        
        
class VIEW3D_PT_Camera_support_panel(bpy.types.Panel):
    """Creates a panel for Camera support"""
    bl_label = "Camera Support"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "UE5CMS"
    bl_order = 6
    
    def draw(self, context):
        layout = self.layout
        # Clip the camera to the new unit scale
        if bpy.context.space_data.clip_end < 10000:
            layout.operator("my_operator.my_clipend_operator", icon='OUTLINER_OB_CAMERA')
            layout.label(text="to view far")
        if bpy.context.space_data.clip_end == 10000:   
            layout.label(text="View is good")
        
class VIEW3D_PT_A7med_Tips(bpy.types.Panel):
    bl_label = "Tips"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "UE5CMS"
    bl_order = 9

    def draw(self, context):
        layout = self.layout
        layout.label(text="-Wheels go with Front left, Front right")

class OBJECT_PT_car_setup(bpy.types.Panel):
    bl_label = "Car Setup"
    bl_idname = "OBJECT_PT_car_setup"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'UE5CMS'
    bl_order = 5
    def draw(self, context):
        layout = self.layout
        
        # Main Car Body Selector
        layout.label(text="Main Car Body:")
        layout.prop_search(context.scene, "main_car_body_object", bpy.data, "objects", text="")
        
        # Car Wheels Selector
        layout.label(text="Car Wheels:")
        wheel_labels = ["Front Left", "Front Right", "Rear Left", "Rear Right"]
        for i, label in enumerate(wheel_labels):
            layout.label(text=f"Wheel {label}:")
            layout.prop_search(context.scene, f"car_wheel_{i+1}_object", bpy.data, "objects", text="")
        
        # Extra Car Parts Selector
        layout.label(text="Extra Car Parts:")
        if hasattr(context.scene, "extra_car_parts"):
            for index, part in enumerate(context.scene.extra_car_parts):
                row = layout.row()
                row.prop(part, "name", text="")
                row.prop_search(part, "object", bpy.data, "objects", text="Object")
                row.operator("object.remove_car_part_extra", text="", icon='X').index = index
        
        # Add Extra Car Parts Button
        layout.operator("object.add_car_part_extra", text="Add Extra Car Part")
        
        # Set Vehicle Up Button
        layout.operator("object.select_car_objects", text="Set Vehicle Up", icon='HAND')

#create a button to apply scale of the car, possbily force the user into applying before export
class MyScalingApply(bpy.types.Operator):
    """Scale apply, Fixes your Car collison being small"""   
    bl_idname = "my_operator.my_scale_apply"
    bl_label = "Apply Object Scale" 
    def excute(self,context):
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        self.report({'INFO'}, "Scale applying is Compelete, your object should have now the proper scale inside unreal")
        return {'FINISHED'}

class MyCutOperator(bpy.types.Operator):
    """cuts the object in half, with anything in right side of facing dirction"""
    bl_idname = "my_operator.my_button_operator"
    bl_label = "Cut On X axis"

    def execute(self, context):
        # Call the function to cut, mirror, and decimate the object
        cut_mirror_and_decimate()
        self.report({'INFO'}, "Cut is Compelete")
        return {'FINISHED'}

class MyMirrorOperator(bpy.types.Operator):
    """adds Mirror modifier"""
    bl_idname = "my_operator.my_mirror_operator"
    bl_label = "Add Mirror Modifier Along Y"

    def execute(self, context):
        # Call the function to add Mirror modifier
        add_mirror_modifier()
        return {'FINISHED'}

class MyDecimateOperator(bpy.types.Operator):
    """Operator to add Decimate modifier"""
    bl_idname = "my_operator.my_decimate_operator"
    bl_label = "Add Decimate Modifier"

    def execute(self, context):
        # Call the function to add Decimate modifier
        add_decimate_modifier()
        return {'FINISHED'}
        
class mysetoriginto3dcursor(bpy.types.Operator):
    """Moves origin to the cursor, helpfull for brake pedals"""
    bl_idname = "my_operator.my_set_originto_3d_cursor"
    bl_label = "Set Origin to 3D Cursor"
    
    def execute(self, context):
        # Call the function to set origin to 3d cursor
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        return {'FINISHED'}

class MyOriginOperator(bpy.types.Operator):
    """Operator to set origin to geometry"""
    bl_idname = "my_operator.my_origin_operator"
    bl_label = "Set Origin to Geometry"

    def execute(self, context):
        # Set origin to geometry
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
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

class MyTransformApplyOperator(bpy.types.Operator):
    """Sets current location as the Defualt location"""
    bl_idname = "my_operator.my_transform_apply_operator"
    bl_label = "Apply Transform"

    def execute(self, context):
        # Apply location transform
        bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
        return {'FINISHED'}

class MySeparateBumperSelected(bpy.types.Operator):
    bl_idname = "my_operator.my_separate_bumper_selected"
    bl_label = "Front bumper"

    def execute(self, context):
        obj = bpy.context.edit_object
        mesh = obj.data
        selected_faces = [f.index for f in mesh.polygons if f.select]

        # Separate by selection
        bpy.ops.mesh.separate(type='SELECTED')

        # Rename the new object
        new_obj = bpy.context.active_object
        new_obj.name = obj.name + "_FrontBumper"
        return {'FINISHED'}

class MySnapToCursorOperator(bpy.types.Operator):
    """Operator to snap selected objects to the 3D cursor"""
    bl_idname = "my_operator.my_snap_to_cursor_operator"
    bl_label = "Snap Selected to Cursor"

    def execute(self, context):
        # Snap selected objects to the 3D cursor
        bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
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
        return {'FINISHED'}

class MyResetCursorOperator(bpy.types.Operator):
    """Operator to reset the 3D cursor"""
    bl_idname = "my_operator.my_reset_cursor_operator"
    bl_label = "Reset Cursor"

    def execute(self, context):
        # Reset the 3D cursor to the origin
        bpy.context.scene.cursor.location = (0, 0, 0)
        return {'FINISHED'}
    
class MyResetPositionOperator(bpy.types.Operator):
    """Move Object To 0,0,0"""
    bl_idname = "my_operator.my_reset_position_operator"
    bl_label = "Obj 0,0,0 Position"

    def execute(self, context):
        # Reset the object's position
        bpy.context.object.location[0] = 0
        bpy.context.object.location[1] = 0
        bpy.context.object.location[2] = 0
        return {'FINISHED'}

class MyTiresReference(bpy.types.Operator):
    """Please don't forget separating each tire and setting the correct origin"""
    bl_idname = "my_operator.my_tires_operator"
    bl_label = "Tires Reference"

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

class MyCarReferenceOperator(bpy.types.Operator):
    """Creates a box to reference your car towards"""
    bl_idname = "my_operator.my_car_reference_operator"
    bl_label = "Car Reference"

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
        
class MySettings(PropertyGroup):

    path : StringProperty(
        #name="",
        description="Path to Directory",
        #default="",
        maxlen=1024,
        subtype='FILE_PATH')
        
    suffix_enum: EnumProperty(
        name="Dropdown:",
        description="Apply Data to attribute.",
        items=[ ('OP1', "No Suffix", "Do not include any suffix"),
                ('OP2', "_high", "adds _high for baking in Substance Painter"),
                ('OP3', "_low", "adds _low for baking in Substance Painter"),
               ]
        )
        
    apply_bool: BoolProperty(
        name="Export Object's Origin?",
        description="Whether to use the objects origin as the export origin",
        default = False
        )
        
def exportCombined(exportFolder, suffix=''):
    isOrigin = bpy.context.scene.my_tool.apply_bool 
    objects = bpy.context.selected_objects
    origLocs = []
        
    for object in objects:
        if isOrigin:
            origLocs.append(object.location.copy())
            object.location = (0.0,0.0,0.0)
        object.name = object.name + suffix

    exportName = exportFolder + bpy.context.active_object.name + '.fbx'
    bpy.ops.export_scene.fbx(filepath=exportName, use_selection=True, mesh_smooth_type='FACE')
    
    for object in objects:  
        if isOrigin:
            object.location = origLocs.pop(0)
        if not suffix is '':
            object.name = object.name[:-(len(suffix))]

class OBJECT_OT_CombinedExporter(bpy.types.Operator):
    """Export what you have Selected as of now, Don't forget the armture"""
    bl_idname = "myops.combined_exporter"
    bl_label = "Export Selected"
    bl_options = {"UNDO"}

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        if context.scene.my_tool.suffix_enum == 'OP1': 
            exportCombined(context.scene.my_tool.path)    
        
        if context.scene.my_tool.suffix_enum == 'OP2':
            exportCombined(context.scene.my_tool.path, '_high')
        
        if context.scene.my_tool.suffix_enum == 'OP3':
            exportCombined(context.scene.my_tool.path, '_low')

        self.report({'INFO'}, 'Exported')
        return {'FINISHED'}

class OpenURLOperator(bpy.types.Operator):
    """Open a URL"""
    bl_idname = "my_operator.open_url"
    bl_label = "Open URL"
    url: bpy.props.StringProperty(default="https://www.youtube.com/@A7med9870")

    def execute(self, context):
        webbrowser.open(self.url)
        return {'FINISHED'}

class VIEW3D_PT_URL_Panel(bpy.types.Panel):
    """Creates a panel with a button to open a URL"""
    bl_label = "PlaceHolder panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'UE5CMS'
    bl_order = 11
    
    def draw(self, context):
        layout = self.layout
        layout.operator("my_operator.open_url", text="Open URL").url = "https://www.youtube.com/@A7med9870"
        
class Button1Operator(bpy.types.Operator):
    bl_idname = "wm.button1_operator"
    bl_label = "Button 1"

    def execute(self, context):
        bpy.context.scene.unit_settings.scale_length = 1
        return {'FINISHED'}

class Button2Operator(bpy.types.Operator):
    bl_idname = "wm.button2_operator"
    bl_label = "Button 2"

    def execute(self, context):
        bpy.context.scene.unit_settings.scale_length = 0.01
        return {'FINISHED'}
#Create a class to display the wheels and vehicle info, in order to trobleshoot any problems that comes with exporting to unreal, upcoming if you are reading this

class ExtraCarPartProperty(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="")
    object: bpy.props.PointerProperty(name="Object", type=bpy.types.Object)

class SelectCarObjectsOperator(bpy.types.Operator):
    bl_idname = "object.select_car_objects"
    bl_label = "Select Car Objects"
    
    def execute(self, context):
        main_car_body = context.scene.main_car_body_object
        
        # Parent the car wheels to the main car body
        for i in range(4):
            wheel_object = getattr(context.scene, f"car_wheel_{i+1}_object", None)
            if wheel_object:
                wheel_object.select_set(True)
                bpy.context.view_layer.objects.active = main_car_body
                bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
                # Rename the car wheels
                if i == 0:
                    wheel_object.name = "FL"
                elif i == 1:
                    wheel_object.name = "FR"
                elif i == 2:
                    wheel_object.name = "RL"
                elif i == 3:
                    wheel_object.name = "RR"
        
        # Parent the extra car parts to the main car body
        if hasattr(context.scene, "extra_car_parts"):
            for part in context.scene.extra_car_parts:
                if part and part.object:
                    part_obj = part.object
                    part_obj.select_set(True)
                    bpy.context.view_layer.objects.active = main_car_body
                    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
                    # Rename the extra car part
                    part_obj.name = part.name
        
        return {'FINISHED'}

class AddCarPartExtraOperator(bpy.types.Operator):
    bl_idname = "object.add_car_part_extra"
    bl_label = "Add Extra Car Part"
    
    def execute(self, context):
        if not hasattr(context.scene, "extra_car_parts"):
            bpy.types.Scene.extra_car_parts = bpy.props.CollectionProperty(type=ExtraCarPartProperty)
        new_part = context.scene.extra_car_parts.add()
        new_part.name = "New Part Name"
        if new_part.object:
            new_part.object.name = new_part.name
        return {'FINISHED'}

class RemoveCarPartExtraOperator(bpy.types.Operator):
    bl_idname = "object.remove_car_part_extra"
    bl_label = "Remove Extra Car Part"
    index: bpy.props.IntProperty()

    def execute(self, context):
        if hasattr(context.scene, "extra_car_parts") and self.index < len(context.scene.extra_car_parts):
            context.scene.extra_car_parts.remove(self.index)
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
    bpy.utils.register_class(VIEW3D_PT_my_Welcoming_panel)
    bpy.utils.register_class(VIEW3D_PT_my_References_panel)
    bpy.utils.register_class(VIEW3D_PT_MeshManpltion_panel)
    bpy.utils.register_class(VIEW3D_PT_wheels_support_panel)
    bpy.utils.register_class(VIEW3D_PT_positions_support_panel)
    bpy.utils.register_class(VIEW3D_PT_my_Export_panel)
    bpy.utils.register_class(VIEW3D_PT_Camera_support_panel)
    bpy.utils.register_class(VIEW3D_PT_A7med_Tips)
    bpy.utils.register_class(Myaddemptyplainaxis)
    bpy.utils.register_class(mysetoriginto3dcursor)
    bpy.utils.register_class(MyCutOperator)
    bpy.utils.register_class(MyMirrorOperator)
    bpy.utils.register_class(MyScalingApply)
    bpy.utils.register_class(MyDecimateOperator)
    bpy.utils.register_class(MyOriginOperator)
    bpy.utils.register_class(MyTransformApplyOperator)
    bpy.utils.register_class(MySetOriginToSelectedOperator)
    bpy.utils.register_class(MySeparateBumperSelected)
    bpy.utils.register_class(MyCursorToObjectOperator)
    bpy.utils.register_class(MyResetCursorOperator)
    bpy.utils.register_class(MyResetPositionOperator)
    bpy.utils.register_class(MyCarReferenceOperator)
    bpy.utils.register_class(MyTiresReference)
    bpy.utils.register_class(MyUnitScale)
    bpy.utils.register_class(MyClipEndOperator)
    bpy.utils.register_class(MySettings)  # Register MySettings class
    bpy.utils.register_class(OBJECT_OT_CombinedExporter)  # Register OBJECT_OT_CombinedExporter class
    bpy.types.Scene.my_tool = PointerProperty(type=MySettings)
    bpy.utils.register_class(OpenURLOperator)
    bpy.utils.register_class(VIEW3D_PT_URL_Panel)
    bpy.utils.register_class(Button1Operator)
    bpy.utils.register_class(Button2Operator)
    bpy.utils.register_class(ExtraCarPartProperty)
    bpy.utils.register_class(OBJECT_PT_car_setup)
    bpy.utils.register_class(SelectCarObjectsOperator)
    bpy.utils.register_class(AddCarPartExtraOperator)
    bpy.utils.register_class(RemoveCarPartExtraOperator)
    bpy.types.Scene.main_car_body_object = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.car_wheel_1_object = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.car_wheel_2_object = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.car_wheel_3_object = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.car_wheel_4_object = bpy.props.PointerProperty(type=bpy.types.Object)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_my_Welcoming_panel)
    bpy.utils.unregister_class(VIEW3D_PT_my_References_panel)
    bpy.utils.unregister_class(VIEW3D_PT_MeshManpltion_panel)
    bpy.utils.unregister_class(VIEW3D_PT_wheels_support_panel)
    bpy.utils.unregister_class(VIEW3D_PT_my_Export_panel)
    bpy.utils.unregister_class(VIEW3D_PT_positions_support_panel)
    bpy.utils.unregister_class(VIEW3D_PT_Camera_support_panel)
    bpy.utils.unregister_class(VIEW3D_PT_A7med_Tips)
    bpy.utils.unregister_class(Myaddemptyplainaxis)
    bpy.utils.unregister_class(mysetoriginto3dcursor)
    bpy.utils.unregister_class(MyCutOperator)
    bpy.utils.unregister_class(MyMirrorOperator)
    bpy.utils.unregister_class(MyScalingApply)
    bpy.utils.unregister_class(MyDecimateOperator)
    bpy.utils.unregister_class(MyOriginOperator)
    bpy.utils.unregister_class(MyTransformApplyOperator)
    bpy.utils.unregister_class(MySetOriginToSelectedOperator)
    bpy.utils.unregister_class(MySeparateBumperSelected)
    bpy.utils.unregister_class(MyCursorToObjectOperator)
    bpy.utils.unregister_class(MyResetCursorOperator)
    bpy.utils.unregister_class(MyResetPositionOperator)
    bpy.utils.unregister_class(MyCarReferenceOperator)
    bpy.utils.unregister_class(MyTiresReference)
    bpy.utils.unregister_class(MyUnitScale)
    bpy.utils.unregister_class(MyClipEndOperator)
    bpy.utils.unregister_class(MySettings)  # Unregister MySettings class
    bpy.utils.unregister_class(OBJECT_OT_CombinedExporter)  # Unregister OBJECT_OT_CombinedExporter class
    del bpy.types.Scene.my_tool  # Remove the scene link to MySettings
    bpy.utils.register_class(OpenURLOperator)
    bpy.utils.register_class(VIEW3D_PT_URL_Panel)
    bpy.utils.unregister_class(Button1Operator)
    bpy.utils.unregister_class(Button2Operator)
    bpy.utils.unregister_class(ExtraCarPartProperty)
    bpy.utils.unregister_class(OBJECT_PT_car_setup)
    bpy.utils.unregister_class(SelectCarObjectsOperator)
    bpy.utils.unregister_class(AddCarPartExtraOperator)
    bpy.utils.unregister_class(RemoveCarPartExtraOperator)
    del bpy.types.Scene.main_car_body_object
    for i in range(4):
        del bpy.types.Scene[f"car_wheel_{i+1}_object"]
    if hasattr(bpy.types.Scene, "extra_car_parts"):
        del bpy.types.Scene.extra_car_parts
    
if __name__ == "__main__":
    register()
