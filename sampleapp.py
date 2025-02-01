from dataclasses import dataclass
from typing import List
from basecomponent import BaseComponent
from widgetnode import button, makeRootNode, node
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
    def __init__(self, id: int):
        super().__init__(id, {})

    def render(self):
        return node([
            button("Add todo", onClick)
        ])
        

class Root(BaseComponent):
    def __init__(self, id: int):
        super().__init__(id, {})

    def render(self):
        return makeRootNode([
            App()
        ])
