bl_info = {
    "name" : "Car Streamliner git",
    "author" : "A7med9870",
    "description" : "Helps with building a car with right scale and settings for unreal engine",
    "blender" : (4, 1, 0),
    "version" : (0, 0, 8),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}

import bpy
from bpy.types import Panel, AddonPreferences
from bpy.props import BoolProperty, EnumProperty
from . import car_setup_panel
from . import Referencetab
from . import MeshMenipli
from . import wheels_support
from . import positions_support_panel
#from . import ExportPanel this will be fully removed in future
from . import CameraPanel
from . import TipsPanel
from . import Renamer
try:
    # Load another Blender file
    from . import ex
except Exception as e:
    print("Error loading file:", e)
    
class UECarStreamlinerPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    show_tips_panel: bpy.props.BoolProperty(
        name="Show Tips Panel",
        description="Toggle visibility of the Tips Panel",
        default=True,
        update=lambda self, context: context.area.tag_redraw(),
    )
    show_Camera_panel: bpy.props.BoolProperty(
        name="Show Camera Panel",
        description="Toggle visibility of the Camera Panel",
        default=True,
        update=lambda self, context: context.area.tag_redraw(),
    )
    show_Export_panel: bpy.props.BoolProperty(
        name="Show Export Panel",
        description="Toggle visibility of the Export Panel",
        default=False,
        update=lambda self, context: context.area.tag_redraw(),
    )
    Disable_Export_force: bpy.props.BoolProperty(
        name="Disable Export Forced Unit Scale",
        description="Toggle visibility of the Export Panel",
        default=False,
        update=lambda self, context: context.area.tag_redraw(),
    )
    show_CarS_panel: bpy.props.BoolProperty(
        name="Show Car Set up Panel",
        description="Toggle visibility of the Camera Panel",
        default=True,
        update=lambda self, context: context.area.tag_redraw(),
    )
    show_ExtraName_panel: bpy.props.BoolProperty(
    name="Show ExtraName Panel",
    description="Toggle visibility of the ExtraName Panel",
    default=True,
    update=lambda self, context: context.area.tag_redraw(),
    )
    dropdown_enum1: EnumProperty(
        name="Reference Tab",
        description="For more compactily",
        items=[
            ("OPTION1", "4.0", "Description for Option 1"),
            ("OPTION2", "3.6 & 4.1", "Description for Option 2"),
        ],
        default="OPTION2"
    )
    documentation_url: bpy.props.StringProperty(
        name="Documentation URL",
        description="URL for the addon documentation",
        default="https://github.com/A7med9870/Blender-Car-Streamliner",
    )
    YT_url: bpy.props.StringProperty(
        name="YT URL",
        description="URL for the Creator Youtube",
        default="https://www.youtube.com/channel/UCMbA857nJ9w5FzfjrhBzq8A",
    )
    IG_url: bpy.props.StringProperty(
        name="IG URL",
        description="URL for the Creator Instagram",
        default="https://www.instagram.com/a7hmed9870/reels/?hl=en",
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "show_tips_panel")
        row.prop(self, "show_Camera_panel")

        row = layout.row()
        row.prop(self, "show_Export_panel")
        row.prop(self, "Disable_Export_force")

        row = layout.row()
        row.prop(self, "show_CarS_panel")
        row.prop(self, "show_ExtraName_panel")

        layout.prop(self, "dropdown_enum1")
        
        row = layout.row()
        row.operator("wm.url_open", text="Github").url = self.documentation_url
        row.operator("wm.url_open", text="Creator's Youtube").url = self.YT_url
        row.operator("wm.url_open", text="Creator's Instagram").url = self.IG_url

    def invoke(self, context, event):
        import webbrowser
        webbrowser.open(self.documentation_url)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(UECarStreamlinerPreferences)
    car_setup_panel.register()
    Referencetab.register()
    MeshMenipli.register()
    wheels_support.register()
    positions_support_panel.register()
    CameraPanel.register()
    TipsPanel.register()
    Renamer.register()
    ex.register()
#    ExportPanel.register()

def unregister():
    bpy.utils.unregister_class(UECarStreamlinerPreferences)
    car_setup_panel.unregister()
    Referencetab.unregister()
    MeshMenipli.unregister()
    wheels_support.unregister()
    positions_support_panel.unregister()
    CameraPanel.unregister()
    TipsPanel.unregister()
    Renamer.unregister()
    ex.unregister()
#    ExportPanel.unregister()


if __name__ == "__main__":
    register()
