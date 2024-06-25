from attrs import define, field
from attrs.validators import instance_of


@define
class ActionsSequence:
    actions = field(validator=instance_of(list))

    @property
    def symbol(self):
        return "".join([action.move.symbol for action in self.actions])

    @property
    def name(self):
        return "-".join([action.move.name for action in self.actions])

