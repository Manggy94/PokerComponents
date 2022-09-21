import components.constants as cst
from components.table_player import TablePlayer


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
        return f"{self.player.name} {self.move} for {self.value}"

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player):
        if not isinstance(player, TablePlayer):
            raise ValueError("A table_player must be defined")
        else:
            self._player = player

    @property
    def move(self):
        return self._move

    @move.setter
    def move(self, move):
        self._move = cst.Action(move)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = max(0.0, float(value))
