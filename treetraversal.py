from __future__ import annotations
import rx
from typing import Any, Dict, List, Optional
from rx import operators as ops
from services import WidgetRegistrationService
import widgetnode
from widgettypes import WidgetTypes

class ShadowNode:
    def __init__(self, id: int, renderable: widgetnode.Renderable):
        self.id = id
        self.renderable = renderable
        self.current_props = {}
        self.children: List[ShadowNode] = []
        self.props_change_subscription: Optional[rx.core.Disposable] = None
        self.children_change_subscription: Optional[rx.core.Disposable] = None

    # def init(self):
        # self.subscribe_to_props(self)

class ShadowNodeTraversalHelper:
    def __init__(self, widget_registration_service: WidgetRegistrationService):
        self.widget_registration_service = widget_registration_service

    def are_props_equal(self, props1: Dict[str, Any], props2: Dict[str, Any]) -> bool:
        return props1 == props2

    def subscribe_to_props_helper(self, shadow_node: ShadowNode):
        if isinstance(shadow_node.renderable, widgetnode.BaseComponent):
            component = shadow_node.renderable
            shadow_node.props_change_subscription = component.props.pipe(
                ops.skip(1)
            ).subscribe(lambda new_props: self.handle_component_props_change(shadow_node, component, new_props))
        elif isinstance(shadow_node.renderable, widgetnode.WidgetNode):
            shadow_node.props_change_subscription = shadow_node.renderable.props.pipe(
                ops.skip(1)
            ).subscribe(lambda new_props: self.handle_widget_node_props_change(shadow_node, shadow_node.renderable, new_props))

    def handle_widget_node(self, widget: widgetnode.RawChildlessWidgetNodeWithId):
        if widget.type == WidgetTypes.BUTTON:
            on_click = widget.props["on_click"]
            if on_click:
                self.widget_registration_service.register_on_click(widget.id, on_click)
                pass
            else:
                print("Button widget must have on_click prop")

    def handle_component_props_change(self, shadow_node: ShadowNode, component: widgetnode.BaseComponent, new_props):
        if self.are_props_equal(shadow_node.current_props, new_props):
            return
        
        shadow_child = component.render()
        shadow_node.children = [self.traverse_tree(shadow_child)]
        shadow_node.current_props = new_props

        self.widget_registration_service.link_children(component.id, [child.id for child in shadow_node.children])

    def handle_widget_node_props_change(self, shadow_node: ShadowNode, widget_node: widgetnode.WidgetNode, new_props):
        self.widget_registration_service.create_widget(widget_node.id, widget_node)

        shadow_children = [self.traverse_tree(child) for child in widget_node.children]
        shadow_node.children = shadow_children
        shadow_node.current_props = new_props
        
        self.widget_registration_service.link_children(widget_node.id, [child.id for child in shadow_node.children])

    def traverse_tree(self, root: widgetnode.Renderable) -> ShadowNode:
        if isinstance(root, widgetnode.BaseComponent):
            shadow_child = self.traverse_tree(root.render())
            id = self.widget_registration_service.get_next_component_id()
            shadow_node = ShadowNode(id, root)
            shadow_node.children = [shadow_child]
            shadow_node.current_props = root.props

            self.subscribe_to_props_helper(shadow_node)

            return shadow_node
        else:
            id = self.widget_registration_service.get_next_widget_id()
            raw_node = widgetnode.create_raw_childless_widget_node_with_id(id, root)

            self.widget_registration_service.create_widget(raw_node)

            shadow_children = [self.traverse_tree(child) for child in root.children.value]
            shadow_node = ShadowNode(id, root)
            shadow_node.children = shadow_children
            shadow_node.current_props = root.props

            self.subscribe_to_props_helper(shadow_node)

            return shadow_node



