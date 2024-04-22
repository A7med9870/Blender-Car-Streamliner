import bpy
import bmesh
import webbrowser
from mathutils import Vector
from bpy.props import (StringProperty, PointerProperty, EnumProperty, BoolProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

class VIEW3D_PT_my_Export_panel(bpy.types.Panel):
    bl_label = "Export Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "UE5CS"
    bl_order = 7
    
    @classmethod
    def poll(cls, context):
        preferences = context.preferences.addons['Blender-Car-Streamliner'].preferences
        return preferences.show_Export_panel
    #@classmethod
    #def poll(cls, context):
    #    preferences = context.preferences.addons['Blender-Car-Streamliner'].preferences
    #    return not preferences.Disable_Export_force
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        scene = context.scene
        layout.label(text="By polycosm")
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

class VIEW3D_PT_my_Export_panel2(bpy.types.Panel):
    bl_label = "Export Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "UE5CS"
    bl_order = 7
    
    @classmethod
    def poll(cls, context):
        preferences = context.preferences.addons['Blender-Car-Streamliner'].preferences
        return preferences.show_Export_panel
    @classmethod
    def poll(cls, context):
        preferences = context.preferences.addons['Blender-Car-Streamliner'].preferences
        return preferences.Disable_Export_force


    def draw(self, context):
        layout = self.layout
        scn = context.scene
        scene = context.scene
        layout.label(text="By polycosm")
        layout.label(text="Export Path Location:", icon='EXPORT')
        layout.prop(scn.my_tool, "path", text="")
        layout.label(text="UNCHECK RELATIVE PATH")
        layout.label(text="IN TOP RIGHT SIDE", icon='PREFERENCES')
        layout.operator("myops.combined_exporter", text='Export Only Selected', icon='TRIA_RIGHT')


class MyUnitScale(bpy.types.Operator):
    """Sets the scale of world to correct scale to export to unreal"""
    bl_idname = "my_operator.my_unitscale_operator"
    bl_label = "Set Unit Scale"
    
    def execute(self, context):    
        bpy.context.scene.unit_settings.scale_length = 0.01
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

classes = (
    VIEW3D_PT_my_Export_panel,
    VIEW3D_PT_my_Export_panel2,
    MyUnitScale,
    MySettings,
    OBJECT_OT_CombinedExporter
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_tool = PointerProperty(type=MySettings)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()
