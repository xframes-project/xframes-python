import threading
import time
import json
import xframes

from enum import Enum

from services import WidgetRegistrationService
from treetraversal import ShadowNodeTraversalHelper

class ImGuiCol(Enum):
    Text = 0
    TextDisabled = 1
    WindowBg = 2
    ChildBg = 3
    PopupBg = 4
    Border = 5
    BorderShadow = 6
    FrameBg = 7
    FrameBgHovered = 8
    FrameBgActive = 9
    TitleBg = 10
    TitleBgActive = 11
    TitleBgCollapsed = 12
    MenuBarBg = 13
    ScrollbarBg = 14
    ScrollbarGrab = 15
    ScrollbarGrabHovered = 16
    ScrollbarGrabActive = 17
    CheckMark = 18
    SliderGrab = 19
    SliderGrabActive = 20
    Button = 21
    ButtonHovered = 22
    ButtonActive = 23
    Header = 24
    HeaderHovered = 25
    HeaderActive = 26
    Separator = 27
    SeparatorHovered = 28
    SeparatorActive = 29
    ResizeGrip = 30
    ResizeGripHovered = 31
    ResizeGripActive = 32
    Tab = 33
    TabHovered = 34
    TabActive = 35
    TabUnfocused = 36
    TabUnfocusedActive = 37
    PlotLines = 38
    PlotLinesHovered = 39
    PlotHistogram = 40
    PlotHistogramHovered = 41
    TableHeaderBg = 42
    TableBorderStrong = 43
    TableBorderLight = 44
    TableRowBg = 45
    TableRowBgAlt = 46
    TextSelectedBg = 47
    DragDropTarget = 48
    NavHighlight = 49
    NavWindowingHighlight = 50
    NavWindowingDimBg = 51
    ModalWindowDimBg = 52
    COUNT = 53

theme2_colors = {
    "darkestGrey": "#141f2c",
    "darkerGrey": "#2a2e39",
    "darkGrey": "#363b4a",
    "lightGrey": "#5a5a5a",
    "lighterGrey": "#7A818C",
    "evenLighterGrey": "#8491a3",
    "black": "#0A0B0D",
    "green": "#75f986",
    "red": "#ff0062",
    "white": "#fff",
}

theme2 = {
    "colors": {
        str(ImGuiCol.Text.value): [theme2_colors["white"], 1],
        str(ImGuiCol.TextDisabled.value): [theme2_colors["lighterGrey"], 1],
        str(ImGuiCol.WindowBg.value): [theme2_colors["black"], 1],
        str(ImGuiCol.ChildBg.value): [theme2_colors["black"], 1],
        str(ImGuiCol.PopupBg.value): [theme2_colors["white"], 1],
        str(ImGuiCol.Border.value): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.BorderShadow.value): [theme2_colors["darkestGrey"], 1],
        str(ImGuiCol.FrameBg.value): [theme2_colors["black"], 1],
        str(ImGuiCol.FrameBgHovered.value): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.FrameBgActive.value): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.TitleBg.value): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.TitleBgActive.value): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.TitleBgCollapsed.value): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.MenuBarBg.value): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.ScrollbarBg.value): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.ScrollbarGrab.value): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.ScrollbarGrabHovered.value): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.ScrollbarGrabActive.value): [theme2_colors["darkestGrey"], 1],
        str(ImGuiCol.CheckMark.value): [theme2_colors["darkestGrey"], 1],
        str(ImGuiCol.SliderGrab.value): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.SliderGrabActive.value): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.Button.value): [theme2_colors["black"], 1],
        str(ImGuiCol.ButtonHovered.value): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.ButtonActive.value): [theme2_colors["black"], 1],
        str(ImGuiCol.Header.value): [theme2_colors["black"], 1],
        str(ImGuiCol.HeaderHovered.value): [theme2_colors["black"], 1],
        str(ImGuiCol.HeaderActive.value): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.Separator.value): [theme2_colors["darkestGrey"], 1],
        str(ImGuiCol.SeparatorHovered.value): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.SeparatorActive.value): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.ResizeGrip.value): [theme2_colors["black"], 1],
        str(ImGuiCol.ResizeGripHovered.value): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.ResizeGripActive.value): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.Tab.value): [theme2_colors["black"], 1],
        str(ImGuiCol.TabHovered.value): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.TabActive.value): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.TabUnfocused.value): [theme2_colors["black"], 1],
        str(ImGuiCol.TabUnfocusedActive.value): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.PlotLines.value): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.PlotLinesHovered.value): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.PlotHistogram.value): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.PlotHistogramHovered.value): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.TableHeaderBg.value): [theme2_colors["black"], 1],
        str(ImGuiCol.TableBorderStrong.value): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.TableBorderLight.value): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.TableRowBg.value): [theme2_colors["darkGrey"], 1],
        str(ImGuiCol.TableRowBgAlt.value): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.TextSelectedBg.value): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.DragDropTarget.value): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.NavHighlight.value): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.NavWindowingHighlight.value): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.NavWindowingDimBg.value): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.ModalWindowDimBg.value): [theme2_colors["darkerGrey"], 1],
    }
}

font_defs = {
    "defs": [
        {"name": "roboto-regular", "sizes": [16, 18, 20, 24, 28, 32, 36, 48]}
    ]
}

font_defs["defs"] = [
    {"name": entry["name"], "size": size}
    for entry in font_defs["defs"]
    for size in entry["sizes"]
]

widget_registration_service = WidgetRegistrationService()
shadow_node_traversal_helper = ShadowNodeTraversalHelper(widget_registration_service)

def run():
    def init():
        print("init!")

        rootNode = {
            "id": 0,
            "type": "node",
            "root": True
        }

        textNode = {
            "id": 1,
            "type": "unformatted-text",
            "text": "Hello, world!"
        }

        xframes.setElement(json.dumps(rootNode))
        xframes.setElement(json.dumps(textNode))
        xframes.setChildren(0, json.dumps([1]))

    def on_text_changed(id, value):
        print(f"text changed, widget {id} value {value}")

    def on_combo_changed(id, value):
        print(f"combo changed, widget {id} value {value}")

    def on_numeric_value_changed(id, value):
        print(f"numeric value changed, widget {id} value {value}")

    def on_boolean_value_changed(id, value):
        print(f"boolean value changed, widget {id} value {value}")

    def on_multiple_numeric_values_changed(id, values):
        print(f"multiple numeric values changed, widget {id} value {values}")

    def on_click(id):
        print(f"widget {id} clicked")

    xframes.init(
        "./assets", 
        json.dumps(font_defs), 
        json.dumps(theme2), 
        init, 
        on_text_changed, 
        on_combo_changed, 
        on_numeric_value_changed, 
        on_boolean_value_changed, 
        on_multiple_numeric_values_changed, 
        on_click
    )

run()


flag = True

def keep_process_running():
    while flag:
        time.sleep(1)

# Start the keep-alive process in a separate thread
thread = threading.Thread(target=keep_process_running)
thread.daemon = True  # Ensure the thread doesn't block program exit
thread.start()

# Main thread can perform other tasks
print("Main process continues to run...")
# time.sleep(5)
# flag = False  # Stop the keep-alive process
thread.join()  # Wait for the thread to finish