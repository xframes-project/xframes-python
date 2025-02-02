from dataclasses import dataclass
from enum import Enum, IntFlag
from typing import Dict, List, Optional, Tuple, NamedTuple, Union

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

    def __str__(self):
        return self.value

class ImPlotScale(Enum):
    Linear = 0
    Time = 1
    Log10 = 2
    SymLog = 3

    def __str__(self):
        return self.value

class ImPlotMarker(Enum):
    None_ = -1
    Circle = 0
    Square = 1
    Diamond = 2
    Up = 3
    Down = 4
    Left = 5
    Right = 6
    Cross = 7
    Plus = 8
    Asterisk = 9

    def __str__(self):
        return self.value

class ImGuiStyleVar(Enum):
    Alpha = 0  # float 
    DisabledAlpha = 1  # float 
    WindowPadding = 2  # ImVec2
    WindowRounding = 3  # float 
    WindowBorderSize = 4  # float 
    WindowMinSize = 5  # ImVec2
    WindowTitleAlign = 6  # ImVec2
    ChildRounding = 7  # float 
    ChildBorderSize = 8  # float 
    PopupRounding = 9  # float 
    PopupBorderSize = 10  # float 
    FramePadding = 11  # ImVec2
    FrameRounding = 12  # float 
    FrameBorderSize = 13  # float 
    ItemSpacing = 14  # ImVec2
    ItemInnerSpacing = 15  # ImVec2
    IndentSpacing = 16  # float 
    CellPadding = 17  # ImVec2
    ScrollbarSize = 18  # float 
    ScrollbarRounding = 19  # float 
    GrabMinSize = 20  # float 
    GrabRounding = 21  # float 
    TabRounding = 22  # float 
    TabBorderSize = 23  # float 
    TabBarBorderSize = 24  # float 
    TableAngledHeadersAngle = 25  # float 
    TableAngledHeadersTextAlign = 26  # ImVec2
    ButtonTextAlign = 27  # ImVec2
    SelectableTextAlign = 28  # ImVec2
    SeparatorTextBorderSize = 29  # float 
    SeparatorTextAlign = 30  # ImVec2
    SeparatorTextPadding = 31  # ImVec2

    def __str__(self):
        return self.value

class ImGuiDir(Enum):
    None_ = -1
    Left = 0
    Right = 1
    Up = 2
    Down = 3

    def __str__(self):
        return self.value

class ImGuiHoveredFlags(IntFlag):
    None_ = 0  # "None" is a reserved keyword in Python
    ChildWindows = 1 << 0
    RootWindow = 1 << 1
    AnyWindow = 1 << 2
    NoPopupHierarchy = 1 << 3
    # DockHierarchy = 1 << 4 
    AllowWhenBlockedByPopup = 1 << 5
    # AllowWhenBlockedByModal = 1 << 6
    AllowWhenBlockedByActiveItem = 1 << 7
    AllowWhenOverlappedByItem = 1 << 8
    AllowWhenOverlappedByWindow = 1 << 9
    AllowWhenDisabled = 1 << 10
    NoNavOverride = 1 << 11
    AllowWhenOverlapped = AllowWhenOverlappedByItem | AllowWhenOverlappedByWindow
    RectOnly = AllowWhenBlockedByPopup | AllowWhenBlockedByActiveItem | AllowWhenOverlapped
    RootAndChildWindows = RootWindow | ChildWindows
    ForTooltip = 1 << 12
    Stationary = 1 << 13
    DelayNone = 1 << 14
    DelayShort = 1 << 15
    DelayNormal = 1 << 16
    NoSharedDelay = 1 << 17

    def __str__(self):
        return self.value

HEXA = Tuple[str, float]

class FontDef(NamedTuple):
    name: str
    size: int

    def to_dict(self):
        return {
            "name": self.name,
            "size": self.size
        }

class ImVec2(NamedTuple):
    x: float
    y: float

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y
        }

StyleColValue = Union[str, HEXA]
StyleVarValue = Union[float, ImVec2]

class Align(Enum):
    Left = "left"
    Right = "right"

    def __str__(self):
        return self.value

@dataclass
class StyleRules:
    align: Optional[Align] = None
    font: Optional[FontDef] = None
    colors: Optional[Dict[ImGuiCol, StyleColValue]] = None
    vars: Optional[Dict[ImGuiStyleVar, StyleVarValue]] = None

    def to_dict(self):
        out = {}

        if self.align is not None:
            out['align'] = self.align
        if self.font is not None:
            out['font'] = self.font.to_dict()
        if self.colors is not None:
            out['colors'] = {key: value for key, value in self.colors.items()}
        if self.vars is not None:
            out['vars'] = {key: value for key, value in self.vars.items()}


        return out

class Direction(Enum):
    Inherit = "inherit"
    Ltr = "ltr"
    Rtl = "rtl"

    def __str__(self):
        return self.value

class FlexDirection(Enum):
    Column = "column"
    ColumnReverse = "column-reverse"
    Row = "row"
    RowReverse = "row-reverse"

    def __str__(self):
        return self.value

class JustifyContent(Enum):
    FlexStart = "flex-start"
    Center = "center"
    FlexEnd = "flex-end"
    SpaceBetween = "space-between"
    SpaceAround = "space-around"
    SpaceEvenly = "space-evenly"

    def __str__(self):
        return self.value

class AlignContent(Enum):
    Auto = "auto"
    FlexStart = "flex-start"
    Center = "center"
    FlexEnd = "flex-end"
    Stretch = "stretch"
    SpaceBetween = "space-between"
    SpaceAround = "space-around"
    SpaceEvenly = "space-evenly"

    def __str__(self):
        return self.value

class AlignItems(Enum):
    Auto = "auto"
    FlexStart = "flex-start"
    Center = "center"
    FlexEnd = "flex-end"
    Stretch = "stretch"
    Baseline = "baseline"

    def __str__(self):
        return self.value

class AlignSelf(Enum):
    Auto = "auto"
    FlexStart = "flex-start"
    Center = "center"
    FlexEnd = "flex-end"
    Stretch = "stretch"
    Baseline = "baseline"

    def __str__(self):
        return self.value

class PositionType(Enum):
    Static = "static"
    Relative = "relative"
    Absolute = "absolute"

    def __str__(self):
        return self.value

class FlexWrap(Enum):
    NoWrap = "no-wrap"
    Wrap = "wrap"
    WrapReverse = "wrap-reverse"

    def __str__(self):
        return self.value

class Overflow(Enum):
    Visible = "visible"
    Hidden = "hidden"
    Scroll = "scroll"

    def __str__(self):
        return self.value

class Display(Enum):
    Flex = "flex"
    DisplayNone = "none"

    def __str__(self):
        return self.value

class Edge(Enum):
    Left = "left"
    Top = "top"
    Right = "right"
    Bottom = "bottom"
    Start = "start"
    End = "end"
    Horizontal = "horizontal"
    Vertical = "vertical"
    All = "all"

    def __str__(self):
        return self.value

class Gutter(Enum):
    Column = "column"
    Row = "row"
    All = "all"

    def __str__(self):
        return self.value

DimensionValue = Union[str, float]

class RoundCorners(Enum):
    All = "all"
    TopLeft = "topLeft"
    TopRight = "topRight"
    BottomLeft = "bottomLeft"
    BottomRight = "bottomRight"

    def __str__(self):
        return self.value

@dataclass
class BorderStyle:
    color: StyleColValue
    thickness: Optional[float] = None

    def to_dict(self):
        out = {"color": self.color}

        if self.thickness:
            out["thickness"] = self.thickness

        return out

@dataclass
class YogaStyle:
    direction: Optional[Direction] = None
    flexDirection: Optional[FlexDirection] = None
    justifyContent: Optional[JustifyContent] = None
    alignContent: Optional[AlignContent] = None
    alignItems: Optional[AlignItems] = None
    alignSelf: Optional[AlignSelf] = None
    positionType: Optional[PositionType] = None
    flexWrap: Optional[FlexWrap] = None
    overflow: Optional[Overflow] = None
    display: Optional[Display] = None
    flex: Optional[float] = None
    flexGrow: Optional[float] = None
    flexShrink: Optional[float] = None
    flexBasis: Optional[float] = None
    flexBasisPercent: Optional[float] = None
    position: Optional[Dict[Edge, float]] = None
    margin: Optional[Dict[Edge, float]] = None
    padding: Optional[Dict[Edge, float]] = None
    gap: Optional[Dict[Gutter, float]] = None
    aspectRatio: Optional[float] = None
    width: Optional[Union[float, str]] = None
    minWidth: Optional[Union[float, str]] = None
    maxWidth: Optional[Union[float, str]] = None
    height: Optional[Union[float, str]] = None
    minHeight: Optional[Union[float, str]] = None
    maxHeight: Optional[Union[float, str]] = None

    def to_dict(self):
        out = {}

        if self.direction is not None:
            out['direction'] = self.direction
        if self.flexDirection is not None:
            out['flexDirection'] = self.flexDirection
        if self.justifyContent is not None:
            out['justifyContent'] = self.justifyContent
        if self.alignContent is not None:
            out['alignContent'] = self.alignContent
        if self.alignItems is not None:
            out['alignItems'] = self.alignItems
        if self.alignSelf is not None:
            out['alignSelf'] = self.alignSelf
        if self.positionType is not None:
            out['positionType'] = self.positionType
        if self.flexWrap is not None:
            out['flexWrap'] = self.flexWrap
        if self.overflow is not None:
            out['overflow'] = self.overflow
        if self.display is not None:
            out['display'] = self.display
        if self.flex is not None:
            out['flex'] = self.flex
        if self.flexGrow is not None:
            out['flexGrow'] = self.flexGrow
        if self.flexShrink is not None:
            out['flexShrink'] = self.flexShrink
        if self.flexBasis is not None:
            out['flexBasis'] = self.flexBasis
        if self.flexBasisPercent is not None:
            out['flexBasisPercent'] = self.flexBasisPercent
        if self.position is not None:
            out['position'] = {str(edge): value for edge, value in self.position.items()}
        if self.margin is not None:
            out['margin'] = {str(edge): value for edge, value in self.margin.items()}
        if self.padding is not None:
            out['padding'] = {str(edge): value for edge, value in self.padding.items()}
        if self.gap is not None:
            out['gap'] = {str(gutter): value for gutter, value in self.gap.items()}
        if self.aspectRatio is not None:
            out['aspectRatio'] = self.aspectRatio
        if self.width is not None:
            out['width'] = self.width
        if self.minWidth is not None:
            out['minWidth'] = self.minWidth
        if self.maxWidth is not None:
            out['maxWidth'] = self.maxWidth
        if self.height is not None:
            out['height'] = self.height
        if self.minHeight is not None:
            out['minHeight'] = self.minHeight
        if self.maxHeight is not None:
            out['maxHeight'] = self.maxHeight

        return out

@dataclass
class BaseDrawStyle:
    backgroundColor: Optional[StyleColValue] = None
    border: Optional[BorderStyle] = None
    borderTop: Optional[BorderStyle] = None
    borderRight: Optional[BorderStyle] = None
    borderBottom: Optional[BorderStyle] = None
    borderLeft: Optional[BorderStyle] = None
    rounding: Optional[float] = None
    roundCorners: Optional[List[RoundCorners]] = None

    def to_dict(self):
        out = {}

        if self.backgroundColor is not None:
            out['backgroundColor'] = self.backgroundColor
        if self.border is not None:
            out['border'] = self.border.to_dict()
        if self.borderTop is not None:
            out['borderTop'] = self.borderTop.to_dict()
        if self.borderRight is not None:
            out['borderRight'] = self.borderRight.to_dict()
        if self.borderBottom is not None:
            out['borderBottom'] = self.borderBottom.to_dict()
        if self.borderLeft is not None:
            out['borderLeft'] = self.borderLeft.to_dict()
        if self.rounding is not None:
            out['rounding'] = self.rounding
        if self.roundCorners is not None:
            out['roundCorners'] = self.roundCorners


        return out

@dataclass
class NodeStyleDef():
    layout: Optional[YogaStyle] = None
    base_draw: Optional[BaseDrawStyle] = None

    def to_dict(self):
        out = {}

        if self.layout is not None:
            out.update(self.layout.to_dict())
        if self.base_draw is not None:
            out.update(self.base_draw.to_dict())

        return out

@dataclass
class WidgetStyleDef():
    style_rules: Optional[StyleRules] = None
    layout: Optional[YogaStyle] = None
    base_draw: Optional[BaseDrawStyle] = None

    def to_dict(self):
        out = {}

        if self.style_rules is not None:
            out.update(self.style_rules.to_dict())
        if self.layout is not None:
            out.update(self.layout.to_dict())
        if self.base_draw is not None:
            out.update(self.base_draw.to_dict())

        return out

@dataclass
class NodeStyle:
    style: Optional[NodeStyleDef] = None
    hoverStyle: Optional[NodeStyleDef] = None
    activeStyle: Optional[NodeStyleDef] = None
    disabledStyle: Optional[NodeStyleDef] = None

@dataclass
class WidgetStyle:
    style: Optional[WidgetStyleDef] = None
    hoverStyle: Optional[WidgetStyleDef] = None
    activeStyle: Optional[WidgetStyleDef] = None
    disabledStyle: Optional[WidgetStyleDef] = None

    
