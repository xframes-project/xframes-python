import rx
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Callable, Optional, Union
from rx import operators as ops
from rx.subject import BehaviorSubject
from services import WidgetRegistrationService
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

def create_raw_childless_widget_node_with_id(id: int, node: WidgetNode) -> RawChildlessWidgetNodeWithId:
    return RawChildlessWidgetNodeWithId(id=id, type=node.type)

class BaseComponent:
    def __init__(self, id: int, props: Dict[str, any]):
        self.id = id
        self.props = props

    def render(self):
        pass

Renderable = Union[BaseComponent, WidgetNode]

class ShadowNode:
    def __init__(self, id: int, renderable_type: str, renderable: Renderable):
        self.id = id
        self.type = renderable_type
        self.renderable = renderable
        self.current_props = {}
        self.children: List[ShadowNode] = []
        self.props_change_subscription: Optional[rx.core.Disposable] = None
        self.children_change_subscription: Optional[rx.core.Disposable] = None

    def init(self):
        self.subscribe_to_props(self)

class ShadowNodeTraversalHelper:
    def __init__(self, widget_registration_service: WidgetRegistrationService):
        self.widget_registration_service = widget_registration_service

    def are_props_equal(self, props1: Dict[str, any], props2: Dict[str, any]) -> bool:
        return props1 == props2

    def subscribe_to_props_helper(self, shadow_node: ShadowNode):
        if isinstance(shadow_node.renderable, BaseComponent):
            component = shadow_node.renderable
            shadow_node.props_change_subscription = component.props.pipe(
                ops.skip(1),
                ops.subscribe(lambda new_props: self.handle_component_props_change(shadow_node, component, new_props))
            )
        elif isinstance(shadow_node.renderable, WidgetNode):
            widget_node = shadow_node.renderable
            shadow_node.props_change_subscription = widget_node.props.pipe(
                ops.skip(1),
                ops.subscribe(lambda new_props: self.handle_widget_node_props_change(shadow_node, widget_node, new_props))
            )

    def handle_widget_node(self, widget: RawChildlessWidgetNodeWithId):
        if widget.type == WidgetTypes.BUTTON:
            on_click = widget.props["on_click"]
            if on_click:
                self.widget_registration_service.register_on_click(widget.id, on_click)
                pass
            else:
                print("Button widget must have on_click prop")

    def handle_component_props_change(self, shadow_node: ShadowNode, component: BaseComponent, new_props):
        if self.are_props_equal(shadow_node.current_props, new_props):
            return
        
        shadow_child = component.render()
        shadow_node.children = [self.traverse_tree(shadow_child)]
        shadow_node.current_props = new_props

        self.widget_registration_service.link_children(component.id, [child.id for child in shadow_node.children])

    def handle_widget_node_props_change(self, shadow_node: ShadowNode, widget_node: WidgetNode, new_props):
        self.widget_registration_service.create_widget(widget_node.id, widget_node)

        shadow_children = [self.traverse_tree(child) for child in widget_node.children]
        shadow_node.children = shadow_children
        shadow_node.current_props = new_props
        
        self.widget_registration_service.link_children(widget_node.id, [child.id for child in shadow_node.children])

    def traverse_tree(self, root: Renderable) -> ShadowNode:
        if isinstance(root, BaseComponent):
            component = root
            shadow_child = self.traverse_tree(component.render())
            id = self.widget_registration_service.get_next_component_id()
            shadow_node = ShadowNode(id, WidgetTypes.Component, component)
            shadow_node.children = [shadow_child]
            shadow_node.current_props = component.props

            self.subscribe_to_props_helper(shadow_node)

            return shadow_node
        elif isinstance(root, WidgetNode):
            id = self.get_next_widget_node_id()
            raw_node = create_raw_childless_widget_node_with_id(id, root)

            self.widget_registration_service.create_widget(raw_node)

            shadow_children = [self.traverse_tree(child) for child in root.children]
            shadow_node = ShadowNode(id, WidgetNode, root)
            shadow_node.children = shadow_children
            shadow_node.current_props = root.props

            self.subscribe_to_props_helper(shadow_node)

            return shadow_node
        else:
            raise Exception("Unknown renderable type")



