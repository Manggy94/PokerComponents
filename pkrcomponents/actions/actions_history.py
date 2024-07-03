from attrs import define, field, Factory
from attrs.validators import instance_of
from pkrcomponents.actions.action import Action
from pkrcomponents.actions.actions_sequence import ActionsSequence


@define
class ActionsHistory:
    preflop = field(validator=instance_of(ActionsSequence), default=Factory(ActionsSequence))
    flop = field(validator=instance_of(ActionsSequence), default=Factory(ActionsSequence))
    turn = field(validator=instance_of(ActionsSequence), default=Factory(ActionsSequence))
    river = field(validator=instance_of(ActionsSequence), default=Factory(ActionsSequence))

    def reset(self):
        self.preflop.reset()
        self.flop.reset()
        self.turn.reset()
        self.river.reset()
