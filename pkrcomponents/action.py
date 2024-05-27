from attrs import define, field
from attrs.validators import instance_of, ge

from pkrcomponents.constants import ActionMove
from pkrcomponents.table_player import TablePlayer


@define
class Action:
    """Class defining different possible actions and amounts a table_player can do"""

    player = field(validator=[instance_of(TablePlayer)])
    move = field(default=ActionMove.CALL, validator=[instance_of(ActionMove)])
    value = field(default=0, validator=[ge(0), instance_of((float, int))])

    def __str__(self):
        return f"{self.player.name} does a {self.move} for {self.value}"
