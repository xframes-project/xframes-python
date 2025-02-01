from enum import Enum

class WidgetTypes(Enum):
    COMPONENT = "component"
    NODE = "node"
    UNFORMATTED_TEXT = "unformatted-text"
    BUTTON = "di-button"

    def __str__(self):
        return self.value