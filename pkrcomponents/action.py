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
        execute(): Executes the action
        pay(value): Pays the value of the action
        play(): Plays the action on the table and advances the seat playing

    """

    player = field(validator=[instance_of(TablePlayer)])
    move = field(default=ActionMove.CALL, validator=[instance_of(ActionMove)], converter=ActionMove)
    value = field(default=0, validator=[ge(0), instance_of(float)], converter=float)

    def __str__(self) -> str:
        """
        Returns a string representation of the action

        Returns:
            str: A string representation of the action
        """
        return f"{self.player.name} does a {self.move} for {self.value}"

    def execute(self):
        """
        Executes the action
        """
        self.pay(self.value)
        self.player.current_bet += self.value
        if self.player.current_bet > self.player.table.pot.highest_bet:
            self.player.table.pot.highest_bet = self.player.current_bet
        self.player.actions.get(f"{self.player.table.street}").append(self)

    def play(self):
        """
        Plays the action on the table and advances the seat playing
        """
        self.execute()
        self.player.table.advance_seat_playing()
        self.player.played = True

    def pay(self, value: float):
        """
        Pays the value of the action
        """
        amount = self.player.max_bet(value)
        self.player.stack -= amount
        self.player.table.pot.add(amount)


class FoldAction(Action):
    """
    This class represents a fold action made by a player in a poker game
    """
    def __init__(self, player):
        super().__init__(player=player, move=ActionMove.FOLD)

    def execute(self):
        super().execute()
        self.player.folded = True


class CheckAction(Action):
    """
    This class represents a check action made by a player in a poker game
    """
    def __init__(self, player: TablePlayer):
        super().__init__(player=player, move=ActionMove.CHECK)


class CallAction(Action):
    """
    This class represents a call action made by a player in a poker game
    """
    def __init__(self, player: TablePlayer):
        super().__init__(player=player, move=ActionMove.CALL, value=player.to_call)

    def execute(self):
        super().execute()


class BetAction(Action):
    """
    This class represents a bet action made by a player in a poker game
    """
    def __init__(self, player: TablePlayer, value: float):
        if value < player.table.min_bet:
            raise ValueError(f"Bet value must be at least {player.table.min_bet}.")
        super().__init__(player=player, move=ActionMove.BET, value=value)

    def execute(self):
        self.player.table.min_bet = 2 * self.value - self.player.table.pot.highest_bet
        super().execute()


class RaiseAction(Action):
    """
    This class represents a raise action made by a player in a poker game
    """
    def __init__(self, player: TablePlayer, value: float):
        total_value = value + player.to_call
        if total_value < player.table.min_bet and total_value != player.stack:
            raise ValueError(f"Raise value must be at least {value} or player should go all-in.")
        super().__init__(player=player, move=ActionMove.RAISE, value=total_value)

    def execute(self):
        self.player.table.min_bet = 2 * self.value - self.player.table.pot.highest_bet
        super().execute()
