from dataclasses import dataclass
from typing import List
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

def onClick():
    new_todo_item = TodoItem(text="New Todo", done=False)

    current_state = sampleAppState.value

    new_state = AppState(
        todo_text=current_state.todo_text,
        todo_items=current_state.todo_items + [new_todo_item]
    )

    sampleAppState.on_next(new_state)

class App(BaseComponent):
    def __init__(self):
        super().__init__({})

        self.sub = sampleAppState.subscribe(lambda latest_app_state: self.props.on_next({
            "todo_text": latest_app_state.todo_text,
            "todo_items": latest_app_state.todo_items,
        }))

    def render(self):
        children = [button("Add todo", onClick)]

        for todo_item in self.props.value["todo_items"]:
            text = f"{todo_item.text} ({'done' if todo_item.done else 'to do'})."
            children.append(unformatted_text(text))

        return node(children)

class Root(BaseComponent):
    def __init__(self):
        super().__init__({})

    def render(self):
        return root_node([
            App()
        ])
