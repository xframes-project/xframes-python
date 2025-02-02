from enum import Enum

class WidgetTypes(Enum):
    Component = "component"
    Node = "node"
    UnformattedText = "unformatted-text"
    Button = "di-button"

    def __str__(self):
        return self.value