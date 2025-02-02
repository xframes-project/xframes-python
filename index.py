import threading
import time
import json
from sampleapp import Root
import xframes
from services import WidgetRegistrationService
from theme import ImGuiCol
from treetraversal import ShadowNodeTraversalHelper

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

def start_app():
    root = Root()
    shadow_node_traversal_helper.traverse_tree(root)

def init():
    start_app()


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
    widget_registration_service.dispatch_on_click_event(id)

def run():
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