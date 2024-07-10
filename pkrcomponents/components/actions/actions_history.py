from attrs import define, field, Factory
from attrs.validators import instance_of
from pkrcomponents.components.actions.actions_sequence import ActionsSequence


@define
class ActionsHistory:
    """
    This class represents the history of actions in a poker game

    Attributes:
        preflop (ActionsSequence): The sequence of actions preflop
        flop (ActionsSequence): The sequence of actions on the flop
        turn (ActionsSequence): The sequence of actions on the turn
        river (ActionsSequence): The sequence of actions on the river

    Methods:
        reset(): Resets the history of actions
    """
    preflop = field(validator=instance_of(ActionsSequence), default=Factory(lambda: ActionsSequence()))
    flop = field(validator=instance_of(ActionsSequence), default=Factory(lambda: ActionsSequence()))
    turn = field(validator=instance_of(ActionsSequence), default=Factory(lambda: ActionsSequence()))
    river = field(validator=instance_of(ActionsSequence), default=Factory(lambda: ActionsSequence()))

    def reset(self):
        """
        Resets the history of actions
        """
        self.preflop.reset()
        self.flop.reset()
        self.turn.reset()
        self.river.reset()
