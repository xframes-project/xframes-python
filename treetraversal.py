from __future__ import annotations
import rx
from rx.core.typing import Disposable
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
        self.props_change_subscription: Optional[Disposable] = None
        self.children_change_subscription: Optional[Disposable] = None

    def to_dict(self):
        return {
            "id": self.id,
            "current_props": self.current_props,
            "children": [child.to_dict() for child in self.children]
        }
    
    def get_linkable_children(self):
            """Returns a list of child nodes that can be linked in the widget tree."""
            out: List[ShadowNode] = []
        
            for child in self.children:
                if not child:
                    continue
                if not child.renderable:
                    continue
                if isinstance(child.renderable, widgetnode.WidgetNode):
                    out.append(child)
                elif len(child.children) > 0:
                    out.extend(child.get_linkable_children())
        
            return out


class ShadowNodeTraversalHelper:
    def __init__(self, widget_registration_service: WidgetRegistrationService):
        self.widget_registration_service = widget_registration_service

    def are_props_equal(self, props1: Dict[str, Any], props2: Dict[str, Any]) -> bool:
        return props1 == props2

    def subscribe_to_props_helper(self, shadow_node: ShadowNode):
        if shadow_node.props_change_subscription:
            shadow_node.props_change_subscription.dispose()

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
        if widget.type == WidgetTypes.Button:
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

        linkable_children = shadow_node.get_linkable_children()

        self.widget_registration_service.link_children(shadow_node.id, [child.id for child in linkable_children])

    def handle_widget_node_props_change(self, shadow_node: ShadowNode, widget_node: widgetnode.WidgetNode, new_props):
        self.widget_registration_service.create_widget(
            widgetnode.create_raw_childless_widget_node_with_id(shadow_node.id, widget_node)
        )

        shadow_children = [self.traverse_tree(child) for child in widget_node.children]
        shadow_node.children = shadow_children
        shadow_node.current_props = new_props
        
        self.widget_registration_service.link_children(shadow_node.id, [child.id for child in shadow_node.children])

    def traverse_tree(self, renderable: widgetnode.Renderable) -> ShadowNode:
        if isinstance(renderable, widgetnode.BaseComponent):
            shadow_child = self.traverse_tree(renderable.render())

            id = self.widget_registration_service.get_next_component_id()
            shadow_node = ShadowNode(id, renderable)
            shadow_node.children = [shadow_child]
            shadow_node.current_props = renderable.props.value

            self.subscribe_to_props_helper(shadow_node)

            return shadow_node
        elif isinstance(renderable, widgetnode.WidgetNode):
            id = self.widget_registration_service.get_next_widget_id()
            raw_node = widgetnode.create_raw_childless_widget_node_with_id(id, renderable)

            self.handle_widget_node(raw_node)

            self.widget_registration_service.create_widget(raw_node)

            shadow_node = ShadowNode(id, renderable)
            shadow_node.children = [self.traverse_tree(child) for child in renderable.children.value]
            shadow_node.current_props = renderable.props.value

            linkable_children = shadow_node.get_linkable_children()

            if len(linkable_children) > 0:
                self.widget_registration_service.link_children(id, [child.id for child in linkable_children])

            self.subscribe_to_props_helper(shadow_node)

            return shadow_node
        else:
            raise Exception("Unrecognised renderable")



