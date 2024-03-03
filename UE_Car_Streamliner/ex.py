import bpy
import bmesh
import webbrowser
from mathutils import Vector
from bpy.props import (StringProperty, PointerProperty, EnumProperty, BoolProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

class MySettings(PropertyGroup):

    path: StringProperty(
        description="Path to Directory",
        maxlen=1024,
        subtype='FILE_PATH')

    suffix_enum: EnumProperty(
        name="Suffix:",
        description="Choose a suffix for export",
        items=[('OP1', "No Suffix", "Do not include any suffix"),
               ('OP2', "_high", "Add _high for baking in Substance Painter"),
               ('OP3', "_low", "Add _low for baking in Substance Painter")]
    )

    apply_origin: BoolProperty(
        name="Export Object's Origin?",
        description="Whether to use the object's origin as the export origin",
        default=False
    )

class VIEW3D_PT_PanelExportAll(bpy.types.Panel):
    bl_label = "Export panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ExportToUE"
    bl_context = "objectmode"
    bl_order = 7


    def draw(self, context):
        layout = self.layout
        scn = context.scene
        layout.label(text="Export Path Location:")
        layout.prop(scn.my_tool, "path", text="")
        layout.label(text="Don't forget to UNCHECK RELATIVE PATH")
        layout.operator("myops.batch_exporter", text='Export Separate', icon='TRIA_RIGHT')
        layout.operator("myops.export_zero_pos", text='Export Separate at Zero Position', icon='TRIA_RIGHT')
        layout.label(text="")
        layout.prop(scn.my_tool, "apply_origin", text="Export Object's Origin?")
        layout.prop(scn.my_tool, "suffix_enum", text="Suffix")
        layout.operator("myops.combined_exporter", text='Export Combined', icon='TRIA_RIGHT')
        layout.operator("myops.combined_export_zero_pos", text='Export Combined at Zero Position', icon='TRIA_RIGHT')

class OBJECT_OT_BatchExport(bpy.types.Operator):
    bl_idname = "myops.batch_exporter"
    bl_label = "Export Selected"
    bl_options = {"UNDO"}

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        export_all(context.scene.my_tool.path)
        self.report({'INFO'}, 'ExportedBatchExport')
        return {'FINISHED'}

class OBJECT_OT_ExportZeroPos(bpy.types.Operator):
    bl_idname = "myops.export_zero_pos"
    bl_label = "Export Selected at Zero Position"
    bl_options = {"UNDO"}

    def execute(self, context):
        objects = context.selected_objects
        for obj in objects:
            obj.location = (0, 0, 0)
        export_all(context.scene.my_tool.path)
        self.report({'INFO'}, 'Exported at Zero Position')
        return {'FINISHED'}

class OBJECT_OT_CombinedExporter(bpy.types.Operator):
    bl_idname = "myops.combined_exporter"
    bl_label = "Export Combined"
    bl_options = {"UNDO"}

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        suffix = ''
        if context.scene.my_tool.suffix_enum == 'OP1':
            pass
        elif context.scene.my_tool.suffix_enum == 'OP2':
            suffix = '_high'
        elif context.scene.my_tool.suffix_enum == 'OP3':
            suffix = '_low'
        export_combined(context.scene.my_tool.path, suffix)
        self.report({'INFO'}, 'Exported Combined')
        return {'FINISHED'}

class OBJECT_OT_CombinedExportZeroPos(bpy.types.Operator):
    bl_idname = "myops.combined_export_zero_pos"
    bl_label = "Export Combined at Zero Position"
    bl_options = {"UNDO"}

    def execute(self, context):
        objects = context.selected_objects
        for obj in objects:
            obj.location = (0, 0, 0)
        suffix = ''
        if context.scene.my_tool.suffix_enum == 'OP1':
            pass
        elif context.scene.my_tool.suffix_enum == 'OP2':
            suffix = '_high'
        elif context.scene.my_tool.suffix_enum == 'OP3':
            suffix = '_low'
        export_combined(context.scene.my_tool.path, suffix)
        self.report({'INFO'}, 'Exported Combined at Zero Position')
        return {'FINISHED'}

def export_combined(export_folder, suffix=''):
    is_origin = bpy.context.scene.my_tool.apply_origin
    objects = bpy.context.selected_objects
    orig_locs = []

    for obj in objects:
        orig_locs.append(obj.location.copy())
        obj.name = obj.name + suffix

    export_name = export_folder + bpy.context.active_object.name + '.fbx'
    bpy.ops.export_scene.fbx(filepath=export_name, use_selection=True, mesh_smooth_type='FACE')

    for obj in objects:
        obj.location = orig_locs.pop(0)
        if suffix != '':
            obj.name = obj.name[:-len(suffix)]
            
def export_combinedZero(export_folder, suffix=''):
    is_origin = bpy.context.scene.my_tool.apply_origin
    objects = bpy.context.selected_objects
    orig_locs = []

    for obj in objects:
        orig_locs.append(obj.location.copy())
        obj.location = (0.0, 0.0, 0.0)
        obj.name = obj.name + suffix

    export_name = export_folder + bpy.context.active_object.name + '.fbx'
    bpy.ops.export_scene.fbx(filepath=export_name, use_selection=True, mesh_smooth_type='FACE')

    for obj in objects:
        obj.location = orig_locs.pop(0)
        if suffix != '':
            obj.name = obj.name[:-len(suffix)]

def export_all(export_folder):
    objects = bpy.context.selected_objects
    for obj in objects:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        if obj.type not in ['MESH']:
            continue
        export_name = export_folder + obj.name + '.fbx'
        bpy.ops.export_scene.fbx(filepath=export_name, use_selection=True, mesh_smooth_type='FACE')

def export_allZero(export_folder):
    objects = bpy.context.selected_objects
    for obj in objects:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        if obj.type not in ['MESH']:
            continue
        obj.location = (0, 0, 0)
        export_name = export_folder + obj.name + '.fbx'
        bpy.ops.export_scene.fbx(filepath=export_name, use_selection=True, mesh_smooth_type='FACE')


classes = (
    VIEW3D_PT_PanelExportAll,
    OBJECT_OT_BatchExport,
    OBJECT_OT_CombinedExporter,
    OBJECT_OT_ExportZeroPos,
    OBJECT_OT_CombinedExportZeroPos,
    MySettings
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MySettings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()
