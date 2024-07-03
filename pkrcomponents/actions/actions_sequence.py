from attrs import define, field
from attrs.validators import instance_of
from pkrcomponents.actions.action import Action


@define
class ActionsSequence:
    actions = field(validator=instance_of(list), default=[])

    @property
    def symbol(self):
        return "".join([action.move.symbol for action in self.actions])

    @property
    def name(self):
        return "-".join([action.move.name for action in self.actions])

    def add(self, action: Action):
        self.actions.append(action)

    def reset(self):
        self.actions = []