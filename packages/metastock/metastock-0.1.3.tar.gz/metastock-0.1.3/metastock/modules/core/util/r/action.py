from typing import Any, Callable


class Action:
    def __init__(self, name: str, payload: Any = None):
        self.name = name
        self.payload = payload

    def __repr__(self):
        return f"Action(name={self.name}, payload={self.payload})"


def create_action(name: str) -> Callable[[Any], Action]:
    def action_factory(payload: Any = None) -> Action:
        return Action(name=name, payload=payload)

    # Đặt một hàm represent cho action_factory
    def represent():
        return f"<Action: [magenta u]{name}[/magenta u]>"

    # action_factory.__repr__ = lambda: represent()
    action_factory.name = name

    # Update wrapper không cần thiết trong trường hợp này nhưng được đề cập
    # để biết cách thêm các thuộc tính khác nếu cần
    # update_wrapper(action_factory, represent, assigned=[], updated=["__dict__"])

    return action_factory


def match_action(action: Action, action_factory: Any) -> bool:
    if isinstance(action_factory, Callable):
        action_factory = action_factory()

    if isinstance(action, Action) and isinstance(action_factory, Action):
        return action.name == action_factory.name

    return False


EMPTY = create_action("EMPTY")
