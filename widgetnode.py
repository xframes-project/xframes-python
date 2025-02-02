from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
import json
from rx.subject import BehaviorSubject
from theme import NodeStyle, NodeStyleDef, WidgetStyle, WidgetStyleDef
from widgettypes import WidgetTypes
from typing import Any, Callable, Dict, List, Optional, Union

class BaseComponent(ABC):
    def __init__(self, props: Dict[str, Any]):
        self.props = BehaviorSubject(props)

    @abstractmethod
    def render(self):
        raise NotImplementedError

@dataclass
class WidgetNode:
    type: WidgetTypes
    props: BehaviorSubject[Dict[str, Any]] = field(default_factory=lambda: BehaviorSubject({}))
    children: BehaviorSubject[List[Renderable]] = field(default_factory=lambda: BehaviorSubject([]))

@dataclass
class RawChildlessWidgetNodeWithId:
    id: int
    type: WidgetTypes
    props: Dict[str, Any] = field(default_factory=dict)

    def to_serializable_dict(self):
        out = {
            "id": self.id,
            "type": self.type.value,
        }

        for key, value in self.props.items():
            if not callable(value):
                out[key] = value

        return out

def widget_node_factory(widgetType: WidgetTypes, props: Dict[str, Any], children: List[Renderable]) -> WidgetNode:
    return WidgetNode(widgetType, BehaviorSubject(props), BehaviorSubject(children))
    

def create_raw_childless_widget_node_with_id(id: int, node: WidgetNode) -> RawChildlessWidgetNodeWithId:
    return RawChildlessWidgetNodeWithId(id=id, type=node.type, props=node.props.value)

def init_props_with_style(style: Optional[Union[NodeStyle, WidgetStyle]]):
    props: Dict[str, Any] = {}

    if style:
        if style.style:
            props["style"] = style.style
        if style.activeStyle:
            props["activeStyle"] = style.activeStyle
        if style.hoverStyle:
            props["hoverStyle"] = style.hoverStyle
        if style.disabledStyle:
            props["disabledStyle"] = style.disabledStyle

    return props

def root_node(children: List[Renderable], style: Optional[NodeStyle] = None) -> WidgetNode:
    props = init_props_with_style(style)

    props["root"] = True
    
    return widget_node_factory(WidgetTypes.Node, props, children)

def node (children: List[Renderable], style: Optional[NodeStyle] = None) -> WidgetNode:
    props = init_props_with_style(style)

    props["root"] = False

    return widget_node_factory(WidgetTypes.Node, props, children)

def unformatted_text (text: str, style: Optional[WidgetStyle] = None) -> WidgetNode:
    props = init_props_with_style(style)

    props["text"] = text

    return widget_node_factory(WidgetTypes.UnformattedText, props, [])

def button (label: str, on_click: Optional[Callable] = None, style: Optional[WidgetStyle] = None) -> WidgetNode:
    props = init_props_with_style(style)

    props["label"] = label

    if on_click:
        props["on_click"] = on_click

    return widget_node_factory(WidgetTypes.Button, props, [])

Renderable = Union[BaseComponent, WidgetNode]

class RawChildlessWidgetNodeWithIdEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if callable(obj):
            return None
        if isinstance(obj, WidgetStyleDef):
            return obj.to_dict()
        if isinstance(obj, NodeStyleDef):
            return obj.to_dict()
        return super().default(obj)