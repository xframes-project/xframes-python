import rx
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Callable, Optional, Union
from rx import operators as ops
from rx.subject import BehaviorSubject
import json

class WidgetTypes:
    COMPONENT = "component"
    NODE = "node"
    UNFORMATTED_TEXT = "unformatted-text"
    BUTTON = "button"

@dataclass
class WidgetNode:
    type: WidgetTypes
    props: BehaviorSubject[Dict[str, any]] = field(default_factory=lambda: BehaviorSubject({}))
    children: BehaviorSubject[List[Renderable]] = field(default_factory=lambda: BehaviorSubject([]))

@dataclass
class RawChildlessWidgetNodeWithId:
    id: int
    type: WidgetTypes
    props: Dict[str, any] = field(default_factory=dict)

class BaseComponent:
    def __init__(self, props):
        self.props = props

    def render(self):
        pass

class WidgetNode:
    def __init__(self, props, children=None):
        self.props = props
        self.children = children or []

Renderable = Union[BaseComponent, WidgetNode]

class Renderable:
    pass

class ShadowNode:
    def __init__(self, id: int, renderable_type: str, renderable: Renderable, subscribe_to_props: Callable):
        self.id = id
        self.type = renderable_type
        self.renderable = renderable
        self.current_props = {}
        self.children: List[ShadowNode] = []
        self.props_change_subscription: Optional[rx.core.Disposable] = None
        self.children_change_subscription: Optional[rx.core.Disposable] = None
        self.subscribe_to_props = subscribe_to_props

    def init(self):
        self.subscribe_to_props(self)

def are_props_equal(props1: Dict[str, any], props2: Dict[str, any]) -> bool:
    return props1 == props2

def subscribe_to_props_helper(shadow_node: ShadowNode):
    if isinstance(shadow_node.renderable, BaseComponent):
        component = shadow_node.renderable
        shadow_node.props_change_subscription = component.props.pipe(
            ops.skip(1),
            ops.subscribe(lambda new_props: handle_component_props_change(shadow_node, component, new_props))
        )
    elif isinstance(shadow_node.renderable, WidgetNode):
        widget_node = shadow_node.renderable
        shadow_node.props_change_subscription = widget_node.props.pipe(
            ops.skip(1),
            ops.subscribe(lambda new_props: handle_widget_node_props_change(shadow_node, widget_node, new_props))
        )

def handle_widget_node(widget: RawChildlessWidgetNodeWithId):
    if widget.type == WidgetTypes.BUTTON:
        on_click = widget.props["on_click"]
        if on_click:
            # register widget for onclick event
            pass
        else:
            print("Button widget must have on_click prop")

def handle_component_props_change(shadow_node: ShadowNode, component: BaseComponent, new_props):
    if are_props_equal(shadow_node.current_props, new_props):
        return
    
    shadow_child = component.render()
    shadow_node.children = [traverse_tree(shadow_child)]
    shadow_node.current_props = new_props

    # update children link

def handle_widget_node_props_change(shadow_node: ShadowNode, widget_node: WidgetNode, new_props):
    # patch 
    shadow_children = [traverse_tree(child) for child in widget_node.children]
    shadow_node.children = shadow_children
    shadow_node.current_props = new_props
    # link

def traverse_tree(root: Renderable) -> ShadowNode:
    if isinstance(root, BaseComponent):
        component = root
        shadow_child = traverse_tree(component.render())
        id = get_next_component_id()
        shadow_node = ShadowNode(id, WidgetTypes.Component, component, subscribe_to_props_helper)
        shadow_node.children = [shadow_child]
        shadow_node.current_props = component.props
        shadow_node.init()
        return shadow_node
    elif isinstance(root, WidgetNode):
        id = get_next_widget_node_id()
        raw_node = create_raw_childless_widget_node_with_id(id, root)
        # create widget
        shadow_children = [traverse_tree(child) for child in root.children]
        shadow_node = ShadowNode(id, WidgetTypes.WidgetNode, root, subscribe_to_props_helper)
        shadow_node.children = shadow_children
        shadow_node.current_props = root.props
        shadow_node.init()
        return shadow_node
    else:
        raise Exception("Unknown renderable type")

def get_next_component_id():
    return 1

def get_next_widget_node_id():
    return 1

