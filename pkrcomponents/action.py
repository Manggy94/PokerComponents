from attrs import define, field
from attrs.validators import instance_of, ge

from pkrcomponents.constants import ActionMove
from pkrcomponents.table_player import TablePlayer


@define
class Action:
    """
    This class represents an action made by a player in a poker game

    Attributes:
        player(TablePlayer): The player making the action
        move(ActionMove): The move made by the player
        value(float): The value of the move made by the player

    Methods:
        __str__(): Returns a string representation of the action

    """

    player = field(validator=[instance_of(TablePlayer)])
    move = field(default=ActionMove.CALL, validator=[instance_of(ActionMove)], converter=ActionMove)
    value = field(default=0, validator=[ge(0), instance_of(float)], converter=float)

    def __str__(self) -> str:
        return f"{self.player.name} does a {self.move} for {self.value}"
