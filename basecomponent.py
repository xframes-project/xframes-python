from typing import Dict

class BaseComponent:
    def __init__(self, id: int, props: Dict[str, any]):
        self.id = id
        self.props = props

    def render(self):
        pass