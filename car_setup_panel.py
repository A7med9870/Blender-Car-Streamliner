import bpy
import bmesh
import webbrowser
from mathutils import Vector
from bpy.props import (StringProperty, PointerProperty, EnumProperty, BoolProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)


class SelectCarObjectsOperator(bpy.types.Operator):
    """parents all added parts to the main body, and renames them respectfully"""
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

        self.report({'INFO'}, "Car set up has been applied")
        return {'FINISHED'}


class OBJECT_PT_car_setup(bpy.types.Panel):
    bl_label = "Car Setup"
    bl_idname = "OBJECT_PT_car_setup"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CS'
    bl_order = 5

    @classmethod
    def poll(cls, context):
        preferences = context.preferences.addons['Blender-Car-Streamliner'].preferences
        return preferences.show_CarS_panel

    def draw(self, context):
        layout = self.layout

        # Main Car Body Selector
        layout.label(text="Main Car Body:")
        row = layout.row()
        row.prop_search(context.scene, "main_car_body_object", bpy.data, "objects", text="")
        row.operator("object.select_main_car_body", text="", icon='RESTRICT_SELECT_OFF')

        # Car Wheels Selector
        layout.label(text="Car Wheels:")

        # Creating rows for front and rear wheels
        wheel_labels = ["Front Left", "Front Right", "Rear Left", "Rear Right"]

        # Front wheels
        row = layout.row(align=True)
        col_left = row.column()  # Column for the left wheel
        col_right = row.column()  # Column for the right wheel

        # Add front left wheel in the left column
        col_left.label(text=f"{wheel_labels[0]} Wheel:")
        sub_row = col_left.row()
        sub_row.prop_search(context.scene, "car_wheel_1_object", bpy.data, "objects", text="")
        sub_row.operator("object.select_car_wheel", text="", icon='RESTRICT_SELECT_OFF').index = 1

        # Add front right wheel in the right column
        col_right.label(text=f"{wheel_labels[1]} Wheel:")
        sub_row = col_right.row()
        sub_row.prop_search(context.scene, "car_wheel_2_object", bpy.data, "objects", text="")
        sub_row.operator("object.select_car_wheel", text="", icon='RESTRICT_SELECT_OFF').index = 3

        # Rear wheels
        row = layout.row(align=True)
        col_left = row.column()  # Column for the left wheel
        col_right = row.column()  # Column for the right wheel

        # Add rear left wheel in the left column
        col_left.label(text=f"{wheel_labels[2]} Wheel:")
        sub_row = col_left.row()
        sub_row.prop_search(context.scene, "car_wheel_4_object", bpy.data, "objects", text="")
        sub_row.operator("object.select_car_wheel", text="", icon='RESTRICT_SELECT_OFF').index = 2

        # Add rear right wheel in the right column
        col_right.label(text=f"{wheel_labels[3]} Wheel:")
        sub_row = col_right.row()
        sub_row.prop_search(context.scene, "car_wheel_3_object", bpy.data, "objects", text="")
        sub_row.operator("object.select_car_wheel", text="", icon='RESTRICT_SELECT_OFF').index = 4

        # Extra Car Parts Selector
        layout.label(text="Extra Car Parts:")
        if hasattr(context.scene, "extra_car_parts"):
            for index, part in enumerate(context.scene.extra_car_parts):
                row = layout.row()
                row.prop(part, "name", text="")
                row.prop_search(part, "object", bpy.data, "objects", text="")
                row.operator("object.select_extra_car_part_object", text="", icon='RESTRICT_SELECT_OFF').index = index
                row.operator("object.remove_car_part_extra", text="", icon='X').index = index

        # Add Extra Car Parts Button
        layout.operator("object.add_car_part_extra", text="Add Extra Car Part", icon='PLUS')

        # Set Vehicle Up Button
        layout.operator("object.select_car_objects", text="Set Vehicle Up", icon='HAND')

        # Select All Added Objects Button
        layout.operator("object.select_all_added_objects", text="Select Everything not Main Body", icon='RESTRICT_SELECT_OFF')

        # Animation and selection operators
        layout.operator("object.select_all_and_set_active_main_body", text="Select Whole Car Parts", icon='RESTRICT_SELECT_ON')
        layout.operator("object.animate_rotate_front_wheels_right", text="Test Animation", icon='ANIM_DATA')


class SelectExtraCarPartObjectOperator(bpy.types.Operator):
    """Selects the optional part of the car"""
    bl_idname = "object.select_extra_car_part_object"
    bl_label = "Select Extra Car Part Object"
    index: bpy.props.IntProperty()

    def execute(self, context):
        if hasattr(context.scene, "extra_car_parts") and self.index < len(context.scene.extra_car_parts):
            part = context.scene.extra_car_parts[self.index]
            if part and part.object:
                part.object.select_set(True)
                self.report({'INFO'}, f"Selected: {part.object.name}!")
        return {'FINISHED'}


class SelectMainCarBodyOperator(bpy.types.Operator):
    """To select the main car's body"""
    bl_idname = "object.select_main_car_body"
    bl_label = "Select Main Car Body"

    def execute(self, context):
        main_car_body = context.scene.main_car_body_object
        if main_car_body:
            bpy.context.view_layer.objects.active = main_car_body
            main_car_body.select_set(True)
            self.report({'INFO'}, f"Selected!! {main_car_body.name}")
        return {'FINISHED'}


class SelectCarWheelOperator(bpy.types.Operator):
    """To select the wheel"""
    bl_idname = "object.select_car_wheel"
    bl_label = "Select Car Wheel"
    index: bpy.props.IntProperty()

    def execute(self, context):
        wheel_object = getattr(context.scene, f"car_wheel_{self.index}_object", None)
        if wheel_object:
            wheel_object.select_set(True)
            self.report({'INFO'}, f"Selected!! {wheel_object.name}")
        return {'FINISHED'}

class SelectAllAddedObjectsOperator(bpy.types.Operator):
    """Selects the entire car, expect main car body"""
    bl_idname = "object.select_all_added_objects"
    bl_label = "Select All Added Objects"

    def execute(self, context):
        for i in range(4):
            wheel_object = getattr(context.scene, f"car_wheel_{i+1}_object", None)
            if wheel_object:
                wheel_object.select_set(True)

        if hasattr(context.scene, "extra_car_parts"):
            for part in context.scene.extra_car_parts:
                if part and part.object:
                    part.object.select_set(True)
        self.report({'INFO'}, "Selected everything not main car's body")
        return {'FINISHED'}

class ExtraCarPartProperty(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="")
    object: bpy.props.PointerProperty(name="Object", type=bpy.types.Object)
    is_selected: bpy.props.BoolProperty(name="Is Selected", default=False)

class AddCarPartExtraOperator(bpy.types.Operator):
    """adds more optional objects to parented to the main car body"""
    bl_idname = "object.add_car_part_extra"
    bl_label = "Add Extra Car Part"

    def execute(self, context):
        if not hasattr(context.scene, "extra_car_parts"):
            bpy.types.Scene.extra_car_parts = bpy.props.CollectionProperty(type=ExtraCarPartProperty)
        new_part = context.scene.extra_car_parts.add()
        new_part.name = "New Part Name"
        if new_part.object:
            new_part.object.name = new_part.name
        self.report({'INFO'}, "New part now can be attached to the car")
        return {'FINISHED'}

class RemoveCarPartExtraOperator(bpy.types.Operator):
    """removes the extra car part, no longer will be selected with other buttons"""
    bl_idname = "object.remove_car_part_extra"
    bl_label = "Remove Extra Car Part"
    index: bpy.props.IntProperty()

    def execute(self, context):
        if hasattr(context.scene, "extra_car_parts") and self.index < len(context.scene.extra_car_parts):
            part_name = context.scene.extra_car_parts[self.index].name  # Get the name first
            context.scene.extra_car_parts.remove(self.index)  # Then remove the part
            self.report({'INFO'}, f"Removed {part_name} from the car :(")
        return {'FINISHED'}


class AnimateRotateFrontWheelsRightOperator(bpy.types.Operator):
    """Will put the car in animation loop, if it's moving everything right; then your car is corrrect, if not; you need to reapply rotation and scale; sometimes location as well"""
    bl_idname = "object.animate_rotate_front_wheels_right"
    bl_label = "Animate Rotate Front Wheels Right"

    def execute(self, context):
        # Rotate all wheels forward
        for i in range(4):  # All wheels
            wheel_object = getattr(context.scene, f"car_wheel_{i+1}_object", None)
            if wheel_object:
                bpy.context.view_layer.objects.active = wheel_object
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
                wheel_object.select_set(True)

                # Set initial keyframe
                wheel_object.rotation_euler = (0, 0, 0)
                wheel_object.keyframe_insert(data_path="rotation_euler", frame=0)
                # Set initial keyframe
                wheel_object.rotation_euler = (0, 0, 0)
                wheel_object.keyframe_insert(data_path="rotation_euler", frame=1)

                # Set forward rotation keyframe
                wheel_object.rotation_euler = (0, 5.0708, 0)  # Rotate 90 degrees on the Y-axis
                wheel_object.keyframe_insert(data_path="rotation_euler", frame=50)

        # Rotate front wheels right and left
        for i in [0, 1]:  # Front left and front right wheels
            wheel_object = getattr(context.scene, f"car_wheel_{i+1}_object", None)
            if wheel_object:
                bpy.context.view_layer.objects.active = wheel_object
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
                wheel_object.select_set(True)

                # Set nothing rotation keyframe
                wheel_object.rotation_euler = (0, 0, 0)  # Rotate 45 degrees on the Z-axis
                wheel_object.keyframe_insert(data_path="rotation_euler", frame=0)
                # Set nothing rotation keyframe
                wheel_object.rotation_euler = (0, 0, 0)  # Rotate 45 degrees on the Z-axis
                wheel_object.keyframe_insert(data_path="rotation_euler", frame=1)
                # Set nothing rotation keyframe
                wheel_object.rotation_euler = (0, 1.5708, 0)  # Rotate 45 degrees on the Z-axis
                wheel_object.keyframe_insert(data_path="rotation_euler", frame=20)

                # Set right rotation keyframe
                wheel_object.rotation_euler = (0, 1.5708, 0.7854)  # Rotate 45 degrees on the Z-axis
                wheel_object.keyframe_insert(data_path="rotation_euler", frame=30)

                # Set left rotation keyframe
                wheel_object.rotation_euler = (0, 3.0708, -0.7854)  # Rotate -45 degrees on the Z-axis
                wheel_object.keyframe_insert(data_path="rotation_euler", frame=40)

                # Set REST rotation keyframe
                wheel_object.rotation_euler = (0, 5.0708, 0.0)  # Rotate -45 degrees on the Z-axis
                wheel_object.keyframe_insert(data_path="rotation_euler", frame=50)

        # Set end frame to 40
        context.scene.frame_end = 50
        self.report({'INFO'}, "an animation has been added, remember to remove it before exporting to unreal")
        return {'FINISHED'}

class SelectAllAndSetActiveMainBodyOperator(bpy.types.Operator):
    """Selects the entire car, with the main body active, your selection should now be ready for exporting to UE"""
    bl_idname = "object.select_all_and_set_active_main_body"
    bl_label = "Select All and Set Active Main Body"

    def execute(self, context):
        main_car_body = context.scene.main_car_body_object
        if main_car_body:
            bpy.ops.object.select_all_added_objects()
            bpy.context.view_layer.objects.active = main_car_body
            main_car_body.select_set(True)
            self.report({'INFO'}, "Selected everything car that has been set'in up with the car, export the car with .export combined. button")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ExtraCarPartProperty)
    bpy.utils.register_class(OBJECT_PT_car_setup)
    bpy.utils.register_class(SelectCarObjectsOperator)
    bpy.utils.register_class(AddCarPartExtraOperator)
    bpy.utils.register_class(RemoveCarPartExtraOperator)
    bpy.utils.register_class(SelectAllAddedObjectsOperator)
    bpy.utils.register_class(SelectExtraCarPartObjectOperator)
    bpy.utils.register_class(SelectMainCarBodyOperator)
    bpy.utils.register_class(SelectCarWheelOperator)
    bpy.utils.register_class(SelectAllAndSetActiveMainBodyOperator)
    bpy.utils.register_class(AnimateRotateFrontWheelsRightOperator)
    bpy.types.Scene.main_car_body_object = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.car_wheel_1_object = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.car_wheel_2_object = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.car_wheel_3_object = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.car_wheel_4_object = bpy.props.PointerProperty(type=bpy.types.Object)

def unregister():
    bpy.utils.unregister_class(ExtraCarPartProperty)
    bpy.utils.unregister_class(OBJECT_PT_car_setup)
    bpy.utils.unregister_class(SelectCarObjectsOperator)
    bpy.utils.unregister_class(SelectMainCarBodyOperator)
    bpy.utils.unregister_class(SelectCarWheelOperator)
    bpy.utils.unregister_class(AddCarPartExtraOperator)
    bpy.utils.unregister_class(RemoveCarPartExtraOperator)
    bpy.utils.unregister_class(SelectAllAddedObjectsOperator)
    bpy.utils.unregister_class(SelectAllAndSetActiveMainBodyOperator)
    bpy.utils.unregister_class(AnimateRotateFrontWheelsRightOperator)
    bpy.utils.unregister_class(SelectExtraCarPartObjectOperator)

    del bpy.types.Scene.main_car_body_object
    for i in range(4):
        del bpy.types.Scene[f"car_wheel_{i+1}_object"]
    if hasattr(bpy.types.Scene, "extra_car_parts"):
        del bpy.types.Scene.extra_car_parts



if __name__ == "__main__":
    register()
