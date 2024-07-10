from attrs import define, field
from attrs.validators import instance_of


@define(repr=False, eq=False)
class ActionsSequence:
    """
    This class represents a sequence of actions in a poker game

    Attributes:
        actions (list): The list of actions in the sequence

    Methods:
        add (Action): Adds an action to the sequence
        reset(): Resets the sequence of actions
    """
    actions = field(validator=instance_of(list), default=[])

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return f"ActionsSequence({self.name})"

    def __eq__(self, other):
        return self.symbol == other.symbol

    @property
    def symbol(self) -> str:
        """
        Returns the symbol representation of the sequence of actions
        """
        return "".join([action.move.symbol for action in self.actions])

    @property
    def name(self) -> str:
        """
        Returns the name representation of the sequence of actions
        """
        return "-".join([action.move.name for action in self.actions])

    def add(self, action):
        """
        Adds an action to the sequence
        """
        self.actions.append(action)

    def reset(self):
        """
        Resets the sequence of actions
        """
        self.actions = []