from dataclasses import asdict
import json
from threading import RLock
from typing import Any, Callable, Dict, List, Optional
from rx.subject import ReplaySubject, BehaviorSubject
from rx.operators import debounce
import widgetnode
import xframes

class WidgetRegistrationService:
    def __init__(self):
        self.id_generator_lock = RLock()
        self.id_registration_lock = RLock()

        self.events_subject = ReplaySubject(buffer_size=10)
        self.events_subject.pipe(debounce(0.001)).subscribe(lambda fn: fn())

        self.widget_registry: Dict[int, Any] = {}
        self.on_click_registry = BehaviorSubject({})

        self.last_widget_id = 0
        self.last_component_id = 0

    def get_widget_by_id(self, widget_id: int) -> Optional[Any]:
        with self.id_registration_lock:
            return self.widget_registry.get(widget_id)
        
    def register_widget(self, widget_id: int, widget: Any):
        with self.id_registration_lock:
            self.widget_registry[widget_id] = widget

    def get_next_widget_id(self) -> int:
        with self.id_generator_lock:
            widget_id = self.last_widget_id
            self.last_widget_id += 1
            return widget_id
        
    def get_next_component_id(self) -> int:
        with self.id_generator_lock:
            component_id = self.last_component_id
            self.last_component_id += 1
            return component_id
        
    def register_on_click(self, widget_id: int, on_click: Callable):
        # We should probably have a mutex here too
        new_registry = self.on_click_registry.value.copy()
        new_registry[widget_id] = on_click
        self.on_click_registry.on_next(new_registry)

    def dispatch_on_click_event(self, widget_id: int):
        on_click = self.on_click_registry.value.get(widget_id)
        if on_click:
            self.events_subject.on_next(on_click)
        else:
            print(f"Widget with id {widget_id} has no on_click handler")

    def create_widget(self, widget: widgetnode.RawChildlessWidgetNodeWithId):
        widget_json = json.dumps(widget.to_serializable_dict(), cls=widgetnode.RawChildlessWidgetNodeWithIdEncoder)
        self.set_element(widget_json)

    def patch_widget(self, widget_id: int, widget: Any):
        widget_json = json.dumps(widget)
        self.patch_element(widget_id, widget_json)

    def link_children(self, widget_id: int, child_ids: List[int]):
        children_json = json.dumps(child_ids)
        self.set_children(widget_id, children_json)

    # These methods need work
    def set_data(self, widget_id: int, data: Any):
        data_json = json.dumps(data)
        self.element_internal_op(widget_id, data_json)

    def append_data(self, widget_id: int, data: Any):
        data_json = json.dumps(data)
        self.element_internal_op(widget_id, data_json)

    def reset_data(self, widget_id: int):
        data_json = json.dumps("")
        self.element_internal_op(widget_id, data_json)

    def reset_data(self, widget_id: int, data: Any):
        data_json = json.dumps(data)
        self.element_internal_op(widget_id, data_json)

    def append_data_to_plot_line(self, widget_id: int, x: float, y: float):
        plot_data = {"x": x, "y": y}
        self.element_internal_op(widget_id, json.dumps(plot_data))

    def set_plot_line_axes_decimal_digits(self, widget_id: int, x: float, y: float):
        axes_data = {"x": x, "y": y}
        self.element_internal_op(widget_id, json.dumps(axes_data))

    def append_text_to_clipped_multi_line_text_renderer(self, widget_id: int, text: str):
        self.extern_append_text(widget_id, text)

    def set_input_text_value(self, widget_id: int, value: str):
        input_text_data = {"value": value}
        self.element_internal_op(widget_id, value)

    def set_combo_selected_index(self, widget_id: int, index: int):
        selected_index_data = {"index": index}
        self.element_internal_op(widget_id, json.dumps(selected_index_data))

    def set_element(self, json_data: str):
        xframes.setElement(json_data)

    def patch_element(self, widget_id: int, json_data: str):
        pass

    def set_children(self, widget_id: int, json_data: str):
        xframes.setChildren(widget_id, json_data)

    def element_internal_op(self, widget_id: int, json_data: str):
        pass

    