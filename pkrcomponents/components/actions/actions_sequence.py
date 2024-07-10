from attrs import define, field
from attrs.validators import instance_of


@define(repr=False, eq=False)
class ActionsSequence:
    actions = field(validator=instance_of(list), default=[])

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return f"ActionsSequence({self.name})"

    def __eq__(self, other):
        return self.symbol == other.symbol

    @property
    def symbol(self):
        return "".join([action.move.symbol for action in self.actions])

    @property
    def name(self):
        return "-".join([action.move.name for action in self.actions])

    def add(self, action):
        self.actions.append(action)

    def reset(self):
        self.actions = []