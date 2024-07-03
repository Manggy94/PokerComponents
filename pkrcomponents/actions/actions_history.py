from attrs import define, field, Factory
from attrs.validators import instance_of
from pkrcomponents.actions.actions_sequence import ActionsSequence


@define
class ActionsHistory:
    preflop = field(validator=instance_of(ActionsSequence), default=Factory(lambda: ActionsSequence()))
    flop = field(validator=instance_of(ActionsSequence), default=Factory(lambda: ActionsSequence()))
    turn = field(validator=instance_of(ActionsSequence), default=Factory(lambda: ActionsSequence()))
    river = field(validator=instance_of(ActionsSequence), default=Factory(lambda: ActionsSequence()))

    def reset(self):
        self.preflop.reset()
        self.flop.reset()
        self.turn.reset()
        self.river.reset()
