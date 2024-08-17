bl_info = {
    "name" : "Car Streamliner",
    "author" : "A7med9870",
    "description" : "Offers tools to start making your cars faster",
    "blender" : (4, 1, 0),
    "version" : (0, 1, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}

import bpy
from bpy.types import Panel, AddonPreferences
from bpy.props import BoolProperty, EnumProperty
from . import car_setup_panel           #The set up part, where your car parts get attached to the main body, for later to load in unreal
from . import Referencetab              #Spawns the box and wheels for the user to reference their car into the right scale for Unreal Engine
from . import MeshMenipli               #Some actions that i keep using a lot
from . import wheels_support            #Mainly for beginners, but make it faster to fix your wheels into unreal
from . import positions_support_panel   #s
from . import CameraPanel               #Increases the view distance, as it's too low when you scale everything up
from . import TipsPanel                 #This might get removed in future, in older versions; it was more completed form
from . import Renamer                   #Very early in development, will help adding a list of text added to the names of existing objects; mainly made to nfs modding
try:
    # Load another Blender file
    from . import ex
    from . import ExportPanel #this will be fully removed in future
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
        name="Show Export to FBX Panel",
        description="Toggle visibility of the Export to FBX Panel",
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
        default=False,
        update=lambda self, context: context.area.tag_redraw(),
    )
    CarRefenceCarRefencedropdown_enum1: EnumProperty(
        name="Reference Tab",
        description="For more compactily",
        items=[
            ("OPTION1", "4.0 UE4/5", "Description for Option 1"),
            ("OPTION2", "3.6 & 4.1 UE4/5", "Description for Option 2"),
            ("OPTION3", "Off", "Disable Reference Panel"),
        ],
        default="OPTION2"
    )
    FBXEdropdown_enum1: EnumProperty(
        name="Export Tab",
        description="For Backwords Compaptily",
        items=[
            ("OPTION1", "Modern Export", "Description for Option 1"),
            ("OPTION2", "Old Export", "Description for Option 2"),
            ("OPTION3", "Off", "Disable Reference Panel"),
        ],
        default="OPTION1"
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

        layout.prop(self, "CarRefenceCarRefencedropdown_enum1")

        layout.prop(self, "FBXEdropdown_enum1")

        row = layout.row()
        row.operator("wm.url_open", text="Github Page").url = self.documentation_url
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
    ExportPanel.register()

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
    ExportPanel.unregister()


if __name__ == "__main__":
    register()
