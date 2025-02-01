from dataclasses import dataclass, field
from __future__ import annotations
from rx.subject import BehaviorSubject
from widgettypes import WidgetTypes
from typing import Any, Callable, Dict, List, Optional
from renderable import Renderable

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

def widgetNodeFactory(widgetType: WidgetTypes, props: Dict[str, Any], children: List[Renderable]):
    return WidgetNode(widgetType, BehaviorSubject(props), BehaviorSubject(children))
    

def create_raw_childless_widget_node_with_id(id: int, node: WidgetNode) -> RawChildlessWidgetNodeWithId:
    return RawChildlessWidgetNodeWithId(id=id, type=node.type)

def makeRootNode(children: List[Renderable]):
    props: Dict[str, Any] = {
        "root": True
    }

    return widgetNodeFactory(WidgetTypes.NODE, props, children)

def node (children: List[Renderable]):
    props: Dict[str, Any] = {
        "root": False
    }

    return widgetNodeFactory(WidgetTypes.NODE, props, children)

def unformattedText (text: str, style: Optional[Dict[str, Any]] = None):
    props: Dict[str, Any] = {
        "text": text
    }

    if style:
        props["style"] = style

    widgetNodeFactory(WidgetTypes.UNFORMATTED_TEXT, props, [])

def button (label: str, onClick: Optional[Callable] = None, style: Optional[Dict[str, Any]] = None):
    props: Dict[str, Any] = {
        "label": label
    }
    
    if onClick:
        props["onClick"] = onClick
    
    if style:
        props["style"] = style

    return widgetNodeFactory(WidgetTypes.BUTTON, props, [])