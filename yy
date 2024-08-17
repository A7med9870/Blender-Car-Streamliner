import bpy
import bmesh
import webbrowser
from mathutils import Vector
from bpy.props import (StringProperty, PointerProperty, EnumProperty, BoolProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)


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
        wheel_labels = ["Front Left", "Front Right", "Rear Left", "Rear Right"]
        for i, label in enumerate(wheel_labels):
            layout.label(text=f"{label} Wheel:")
            row = layout.row()
            row.prop_search(context.scene, f"car_wheel_{i+1}_object", bpy.data, "objects", text="")
            row.operator("object.select_car_wheel", text="", icon='RESTRICT_SELECT_OFF').index = i + 1

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
        layout.operator("object.select_all_added_objects", text="Select All Added Objects")

        layout.operator("object.rotate_wheels_x_axis", text="Rotate Wheels X-Axis")
        layout.operator("object.rotate_front_wheels_right", text="Rotate Front Wheels Right")
        layout.operator("object.rotate_front_wheels_left", text="Rotate Front Wheels Left")


class SelectExtraCarPartObjectOperator(bpy.types.Operator):
    bl_idname = "object.select_extra_car_part_object"
    bl_label = "Select Extra Car Part Object"
    index: bpy.props.IntProperty()

    def execute(self, context):
        if hasattr(context.scene, "extra_car_parts") and self.index < len(context.scene.extra_car_parts):
            part = context.scene.extra_car_parts[self.index]
            if part and part.object:
                part.object.select_set(True)
        return {'FINISHED'}


class SelectMainCarBodyOperator(bpy.types.Operator):
    bl_idname = "object.select_main_car_body"
    bl_label = "Select Main Car Body"

    def execute(self, context):
        main_car_body = context.scene.main_car_body_object
        if main_car_body:
            bpy.context.view_layer.objects.active = main_car_body
            main_car_body.select_set(True)
        return {'FINISHED'}


class SelectCarWheelOperator(bpy.types.Operator):
    bl_idname = "object.select_car_wheel"
    bl_label = "Select Car Wheel"
    index: bpy.props.IntProperty()

    def execute(self, context):
        wheel_object = getattr(context.scene, f"car_wheel_{self.index}_object", None)
        if wheel_object:
            wheel_object.select_set(True)
        return {'FINISHED'}



class SelectAllAddedObjectsOperator(bpy.types.Operator):
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

        return {'FINISHED'}


class ExtraCarPartProperty(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="")
    object: bpy.props.PointerProperty(name="Object", type=bpy.types.Object)
    is_selected: bpy.props.BoolProperty(name="Is Selected", default=False)


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


class RotateWheelsXAxisOperator(bpy.types.Operator):
    bl_idname = "object.rotate_wheels_x_axis"
    bl_label = "Rotate Wheels X-Axis"

    def execute(self, context):
        for i in range(4):
            wheel_object = getattr(context.scene, f"car_wheel_{i+1}_object", None)
            if wheel_object:
                bpy.context.view_layer.objects.active = wheel_object
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
                wheel_object.select_set(True)
                bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
                bpy.ops.transform.rotate(value=1.5708, orient_axis='X')  # Rotate 90 degrees on the X-axis
        return {'FINISHED'}

class RotateFrontWheelsRightOperator(bpy.types.Operator):
    bl_idname = "object.rotate_front_wheels_right"
    bl_label = "Rotate Front Wheels Right"

    def execute(self, context):
        for i in [0, 1]:  # Front left and front right wheels
            wheel_object = getattr(context.scene, f"car_wheel_{i+1}_object", None)
            if wheel_object:
                bpy.context.view_layer.objects.active = wheel_object
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
                wheel_object.select_set(True)
                bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
                bpy.ops.transform.rotate(value=0.7854, orient_axis='Z')  # Rotate 45 degrees on the Z-axis
        return {'FINISHED'}

class RotateFrontWheelsLeftOperator(bpy.types.Operator):
    bl_idname = "object.rotate_front_wheels_left"
    bl_label = "Rotate Front Wheels Left"

    def execute(self, context):
        for i in [0, 1]:  # Front left and front right wheels
            wheel_object = getattr(context.scene, f"car_wheel_{i+1}_object", None)
            if wheel_object:
                bpy.context.view_layer.objects.active = wheel_object
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT')
                wheel_object.select_set(True)
                bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
                bpy.ops.transform.rotate(value=-0.7854, orient_axis='Z')  # Rotate -45 degrees on the Z-axis
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
    bpy.utils.register_class(RotateWheelsXAxisOperator)
    bpy.utils.register_class(RotateFrontWheelsRightOperator)
    bpy.utils.register_class(RotateFrontWheelsLeftOperator)
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
    bpy.utils.unregister_class(SelectExtraCarPartObjectOperator)
    bpy.utils.unregister_class(RotateWheelsXAxisOperator)
    bpy.utils.unregister_class(RotateFrontWheelsRightOperator)
    bpy.utils.unregister_class(RotateFrontWheelsLeftOperator)

    del bpy.types.Scene.main_car_body_object
    for i in range(4):
        del bpy.types.Scene[f"car_wheel_{i+1}_object"]
    if hasattr(bpy.types.Scene, "extra_car_parts"):
        del bpy.types.Scene.extra_car_parts



if __name__ == "__main__":
    register()
