from enum import Enum
import json
import xframes

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
        str(ImGuiCol.Text): [theme2_colors["white"], 1],
        str(ImGuiCol.TextDisabled): [theme2_colors["lighterGrey"], 1],
        str(ImGuiCol.WindowBg): [theme2_colors["black"], 1],
        str(ImGuiCol.ChildBg): [theme2_colors["black"], 1],
        str(ImGuiCol.PopupBg): [theme2_colors["white"], 1],
        str(ImGuiCol.Border): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.BorderShadow): [theme2_colors["darkestGrey"], 1],
        str(ImGuiCol.FrameBg): [theme2_colors["black"], 1],
        str(ImGuiCol.FrameBgHovered): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.FrameBgActive): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.TitleBg): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.TitleBgActive): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.TitleBgCollapsed): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.MenuBarBg): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.ScrollbarBg): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.ScrollbarGrab): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.ScrollbarGrabHovered): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.ScrollbarGrabActive): [theme2_colors["darkestGrey"], 1],
        str(ImGuiCol.CheckMark): [theme2_colors["darkestGrey"], 1],
        str(ImGuiCol.SliderGrab): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.SliderGrabActive): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.Button): [theme2_colors["black"], 1],
        str(ImGuiCol.ButtonHovered): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.ButtonActive): [theme2_colors["black"], 1],
        str(ImGuiCol.Header): [theme2_colors["black"], 1],
        str(ImGuiCol.HeaderHovered): [theme2_colors["black"], 1],
        str(ImGuiCol.HeaderActive): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.Separator): [theme2_colors["darkestGrey"], 1],
        str(ImGuiCol.SeparatorHovered): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.SeparatorActive): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.ResizeGrip): [theme2_colors["black"], 1],
        str(ImGuiCol.ResizeGripHovered): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.ResizeGripActive): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.Tab): [theme2_colors["black"], 1],
        str(ImGuiCol.TabHovered): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.TabActive): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.TabUnfocused): [theme2_colors["black"], 1],
        str(ImGuiCol.TabUnfocusedActive): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.PlotLines): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.PlotLinesHovered): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.PlotHistogram): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.PlotHistogramHovered): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.TableHeaderBg): [theme2_colors["black"], 1],
        str(ImGuiCol.TableBorderStrong): [theme2_colors["lightGrey"], 1],
        str(ImGuiCol.TableBorderLight): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.TableRowBg): [theme2_colors["darkGrey"], 1],
        str(ImGuiCol.TableRowBgAlt): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.TextSelectedBg): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.DragDropTarget): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.NavHighlight): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.NavWindowingHighlight): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.NavWindowingDimBg): [theme2_colors["darkerGrey"], 1],
        str(ImGuiCol.ModalWindowDimBg): [theme2_colors["darkerGrey"], 1],
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

def run():
    def init():
        pass

    def on_text_change(id):
        pass

    xframes.init("./assets", json.dumps(font_defs), json.dumps(theme2), init, on_text_change, on_text_change, on_text_change, on_text_change, on_text_change, on_text_change)

run()
