from dataclasses import dataclass
from typing import List
from widgetnode import button, makeRootNode, node, BaseComponent, unformatted_text
from rx.subject import BehaviorSubject

@dataclass
class TodoItem:
    Text: str
    Done: bool

# Define AppState using dataclass
@dataclass
class AppState:
    TodoText: str
    TodoItems: List[TodoItem]

sampleAppState = BehaviorSubject(AppState(TodoText="", TodoItems=[]))

def onClick():
    # Create a new TodoItem
    new_todo_item = TodoItem(Text="New Todo", Done=False)

    # Update the AppState with the new TodoItem appended
    current_state = sampleAppState.value  # Get the current state

    new_state = AppState(
        TodoText=current_state.TodoText,
        TodoItems=current_state.TodoItems + [new_todo_item]  # Append new item
    )

    # Emit the new state to the BehaviorSubject
    sampleAppState.on_next(new_state)

class App(BaseComponent):
    def __init__(self):
        super().__init__({})

        self.sub = sampleAppState.subscribe(lambda latest_app_state: self.props.on_next({
            "todo_text": latest_app_state.TodoText,
            "todo_items": latest_app_state.TodoItems,
        }))

    def render(self):
        children = [button("Add todo", onClick)]

        # text_nodes = []
        todo_items = self.props.value["todo_items"]

        if todo_items:
            for todo_item in todo_items:
                text = f"{todo_item.Text} ({'done' if todo_item.Done else 'to do'})."
                children.append(unformatted_text(text))

        return node(children)
        
        

class Root(BaseComponent):
    def __init__(self):
        super().__init__({})

    def render(self):
        return makeRootNode([
            App()
        ])
