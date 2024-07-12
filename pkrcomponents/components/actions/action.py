from attrs import define, field
from attrs.validators import instance_of, ge

from pkrcomponents.components.actions.action_move import ActionMove
from pkrcomponents.components.actions.street import Street
from pkrcomponents.components.players.table_player import TablePlayer
from pkrcomponents.components.utils.exceptions import NotSufficientRaiseError, NotSufficientBetError


@define
class Action:
    """
    This class represents an action made by a player in a poker game

    Attributes:
        player (TablePlayer): The player making the action
        move (ActionMove): The move made by the player
        value (float): The value of the move made by the player

    Methods:
        __str__(): Returns a string representation of the action
        execute(): Executes the action
        play(): Plays the action on the table and advances the seat playing
        add_to_history(): Adds the action to the history
        update_hand_stats(): Updates the hand statistics of the player according to the action
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
        return f"{self.player.name} does a {self.move.name} for {self.value}"

    @property
    def table(self):
        """
        Returns the table where the action is made
        """
        return self.player.table

    @property
    def hand_stats(self):
        """
        Returns the hand statistics of the player
        """
        return self.player.hand_stats

    @property
    def new_min_bet(self):
        """
        Returns the new minimum bet after the action
        """
        return max(2 * self.value - self.table.pot.highest_bet, self.table.min_bet)

    @property
    def is_all_in(self):
        """
        Returns True if the player is all in
        """
        return self.value >= self.player.stack

    def execute(self):
        """
        Executes the action
        """

        self.player.pay(self.value)
        self.add_to_history()
        self.player.set_first_to_talk()
        self.update_hand_stats()
        self.player.current_bet += self.value
        self.table.update_min_bet(self.new_min_bet)
        self.table.pot.update_highest_bet(self.player.current_bet)

    def play(self):
        """
        Plays the action on the table and advances the seat playing
        """
        self.execute()
        self.table.advance_seat_playing()
        self.player.played = True

    def update_street_hand_stats(self):
        match self.table.street:
            case Street.PREFLOP:
                self.player.hand_stats.preflop.update_hand_stats(self)
            case Street.FLOP:
                self.player.hand_stats.flop.actions_sequence = self.player.actions_history.flop
                self.player.hand_stats.flop.update_hand_stats(self)
            case Street.TURN:
                self.player.hand_stats.turn.actions_sequence = self.player.actions_history.turn
                self.player.hand_stats.turn.update_hand_stats(self)
            case Street.RIVER:
                self.player.hand_stats.river.actions_sequence = self.player.actions_history.river
                self.player.hand_stats.river.update_hand_stats(self)

    def update_hand_stats(self):
        """
        Updates the hand statistics of the player according to the action
        """
        self.update_street_hand_stats()
        self.player.hand_stats.general.update_hand_stats(self)

    def add_to_history(self):
        """
        Adds the action to the history
        """
        match self.table.street:
            case Street.PREFLOP:
                self.player.actions_history.preflop.add(self)
            case Street.FLOP:
                self.player.actions_history.flop.add(self)
            case Street.TURN:
                self.player.actions_history.turn.add(self)
            case Street.RIVER:
                self.player.actions_history.river.add(self)


class FoldAction(Action):
    """
    This class represents a fold action made by a player in a poker game
    """
    def __init__(self, player):
        super().__init__(player=player, move=ActionMove.FOLD)

    def execute(self):
        super().execute()
        self.player.folded = True
        self.player.has_initiative = False


class CheckAction(Action):
    """
    This class represents a check action made by a player in a poker game
    """
    def __init__(self, player: TablePlayer):
        super().__init__(player=player, move=ActionMove.CHECK)

    def execute(self):
        super().execute()
        self.player.has_initiative = False


class CallAction(Action):
    """
    This class represents a call action made by a player in a poker game
    """
    def __init__(self, player: TablePlayer):
        super().__init__(player=player, move=ActionMove.CALL, value=player.to_call)

    def execute(self):
        super().execute()
        self.table.cnt_calls += 1
        self.table.is_opened = True


class BetAction(Action):
    """
    This class represents a bet action made by a player in a poker game
    """
    def __init__(self, player: TablePlayer, value: float):
        if value < player.table.min_bet:
            raise NotSufficientBetError(value, player)
        super().__init__(player=player, move=ActionMove.BET, value=value)

    def execute(self):
        super().execute()
        self.table.cnt_bets += 1
        self.player.take_initiative()
        if self.player.has_initiative:
            self.player.flag_street_cbet = True
        else:
            self.player.flag_street_donk_bet = True


class RaiseAction(Action):
    """
    This class represents a raise action made by a player in a poker game
    """
    def __init__(self, player: TablePlayer, value: float):

        total_value = value + player.to_call
        if value < player.min_raise and total_value != player.stack:
            raise NotSufficientRaiseError(value, player)
        super().__init__(player=player, move=ActionMove.RAISE, value=total_value)

    def execute(self):
        super().execute()
        self.table.cnt_bets += 1
        self.table.is_opened = True
        self.player.take_initiative()
