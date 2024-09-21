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

class hamadacarsPanelExportAll(bpy.types.Panel):
    bl_label = "Export panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ExportToUE"
    bl_context = "objectmode"
    bl_order = 7

#   @classmethod
#   def poll(cls, context):
#      preferences = context.preferences.addons['Blender-Car-Streamliner'].preferences
#      return preferences.show_Export_panel
    @classmethod
    def poll(cls, context):
        preferences = bpy.context.preferences.addons['Blender-Car-Streamliner'].preferences
        return preferences.FBXEdropdown_enum1 == "OPTION1"
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        scene = context.scene
        layout.label(text="Export Path Location:")
        layout.prop(scn.my_tool, "path", text="")
        row = layout.row()
        if scene.uncheckwarn:
            row.label(text="Don't forget to UNCHECK RELATIVE PATH")
            layout.label(text="")
            row = layout.row()
        row.prop(scene, "uncheckwarn", text="ok") #enables the refernce explains; placed here to make the ui much cleaner        row.operator("preferences.addon_show", icon='SETTINGS').module = 'Blender-Car-Streamliner'
        layout.operator("object.select_all_and_set_active_main_body", text="Select Hole Car parts")
        layout.operator("myops.batch_exporter", text='Export Separate', icon='TRIA_RIGHT')
        layout.operator("myops.export_zero_pos", text='Export Separate at Zero Position', icon='TRIA_RIGHT')
        layout.label(text="")
        layout.operator("myops.combined_exporter", text='Export Combined', icon='TRIA_RIGHT')
        layout.operator("myops.combined_export_zero_pos", text='Export Combined at Zero Position', icon='TRIA_RIGHT')

        # Check unit scale and show warning if it's not 0.01
        # for some awful reasons, it has to be this number, something about double float shit
        if scene.unit_settings.scale_length != 0.009999999776482582:
            layout.label(text="WRONG UNIT SCALE FOR UE", icon='ERROR')

        layout.label(text=f"Current Unit Scale: {scene.unit_settings.scale_length:.6f}")

bpy.types.Scene.uncheckwarn = bpy.props.BoolProperty(
    name="Show a tip",
    description="the warning, might be bloated for experinced; yet needed if you are new to using this add-on",
    default=True
)

class hamadacarsBatchExport(bpy.types.Operator):
    bl_idname = "myops.batch_exporter"
    bl_label = "Export Selected"
    bl_options = {"UNDO"}

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        hamadacarsexport_export_all(context.scene.my_tool.path)
        self.report({'INFO'}, 'ExportedBatchExport')
        return {'FINISHED'}

class hamadacarsExportZeroPos(bpy.types.Operator):
    """Export at zero Position"""
    bl_idname = "myops.export_zero_pos"
    bl_label = "Export Selected at Zero Position"
    bl_options = {"UNDO"}

    def execute(self, context):
        objects = context.selected_objects
        for obj in objects:
            obj.location = (0, 0, 0)
        hamadacarsexport_export_all(context.scene.my_tool.path)
        self.report({'INFO'}, 'Exported at Zero Position')
        return {'FINISHED'}

class hamadacarsUnitScale(bpy.types.Operator):
    """Sets the scale of world to correct scale to export to unreal"""
    bl_idname = "my_operator.my_unitscale_operator"
    bl_label = "Set Unit Scale"

    def execute(self, context):
        bpy.context.scene.unit_settings.scale_length = 0.01
        return {'FINISHED'}

class hamadacarsCombinedExporter(bpy.types.Operator):
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
        hamadacarsexport_combined(context.scene.my_tool.path, suffix)
        self.report({'INFO'}, 'Exported Combined')
        return {'FINISHED'}

class hamadacarsCombinedExportZeroPos(bpy.types.Operator):
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
        hamadacarsexport_combined(context.scene.my_tool.path, suffix)
        self.report({'INFO'}, 'Exported Combined at Zero Position')
        return {'FINISHED'}

def hamadacarsexport_combined(export_folder, suffix=''):
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

def hamadacarsexport_combinedZero(export_folder, suffix=''):
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

def hamadacarsexport_export_all(export_folder):
    objects = bpy.context.selected_objects
    for obj in objects:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        if obj.type not in ['MESH']:
            continue
        export_name = export_folder + obj.name + '.fbx'
        bpy.ops.export_scene.fbx(filepath=export_name, use_selection=True, mesh_smooth_type='FACE')

def hamadacarsexport_export_allZero(export_folder):
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
    hamadacarsPanelExportAll,
    hamadacarsBatchExport,
    hamadacarsCombinedExporter,
    hamadacarsExportZeroPos,
    hamadacarsCombinedExportZeroPos,
    MySettings,
    hamadacarsUnitScale
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
