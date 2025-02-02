from dataclasses import dataclass
from typing import List
from theme import Edge, FontDef, StyleRules, WidgetStyle, WidgetStyleDef, YogaStyle
from widgetnode import button, root_node, node, BaseComponent, unformatted_text
from rx.subject import BehaviorSubject

@dataclass
class TodoItem:
    text: str
    done: bool

@dataclass
class AppState:
    todo_text: str
    todo_items: List[TodoItem]

sampleAppState = BehaviorSubject(AppState(todo_text="", todo_items=[]))

def on_click():
    new_todo_item = TodoItem(text="New Todo", done=False)

    current_state = sampleAppState.value

    new_state = AppState(
        todo_text=current_state.todo_text,
        todo_items=current_state.todo_items + [new_todo_item]
    )

    sampleAppState.on_next(new_state)

text_style = WidgetStyle(
    style=WidgetStyleDef(
        style_rules=StyleRules(
            font=FontDef("roboto-regular", 32)
        )
    )
)

button_style = WidgetStyle(
    style=WidgetStyleDef(
        style_rules=StyleRules(
            font=FontDef("roboto-regular", 32)
        ),
        layout=YogaStyle(
            width="50%", 
            padding={Edge.Vertical: 10}, 
            margin={Edge.Left: 140}
        )
    )
)

class App(BaseComponent):
    def __init__(self):
        super().__init__({})

        self.app_state_subscription = sampleAppState.subscribe(lambda latest_app_state: self.props.on_next({
            "todo_text": latest_app_state.todo_text,
            "todo_items": latest_app_state.todo_items,
        }))

    def render(self):
        children = [button("Add todo", on_click, button_style)]

        for todo_item in self.props.value["todo_items"]:
            text = f"{todo_item.text} ({'done' if todo_item.done else 'to do'})."
            children.append(unformatted_text(text, text_style))

        return node(children)
    
    def dispose(self):
        self.app_state_subscription.dispose()

class Root(BaseComponent):
    def __init__(self):
        super().__init__({})

    def render(self):
        return root_node([
            App()
        ])
