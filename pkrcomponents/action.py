import pkrcomponents.constants as cst
from pkrcomponents.table_player import TablePlayer


class Action:
    """Class defining different possible actions and amounts a table_player can do"""

    _value: float
    _player: TablePlayer
    _move: cst.Action

    def __init__(self, player, move="call", value=0):
        self.player = player
        self.move = move
        self.value = value

    def __str__(self):
        return f"{self.player.name} does a {self.move} for {self.value}"

    @property
    def player(self):
        """
        Player involved in an action
        """
        return self._player

    @player.setter
    def player(self, player):
        """
        Player setter
        """
        if not isinstance(player, TablePlayer):
            raise ValueError("A table_player must be defined")
        else:
            self._player = player

    @property
    def move(self):
        """
        The move realized.
        Ex: Fold, Bet, Call...
        """
        return self._move

    @move.setter
    def move(self, move):
        """
        Move setter
        """
        self._move = cst.Action(move)

    @property
    def value(self):
        """
        The numerical value of the action realized.
        Ex: 0 for a check
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Value Setter
        """
        self._value = max(0.0, float(value))
