from attrs import define, field
from attrs.validators import instance_of, ge

from pkrcomponents.actions.action_move import ActionMove
from pkrcomponents.actions.street import Street
from pkrcomponents.players.table_player import TablePlayer


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
        return f"{self.player.name} does a {self.move.name} for {self.value}"

    @property
    def table(self):
        """
        Returns the table where the action is made
        """
        return self.player.table

    @property
    def new_min_bet(self):
        """
        Returns the new minimum bet after the action
        """
        return max(2 * self.value - self.table.pot.highest_bet, self.table.min_bet)

    def execute(self):
        """
        Executes the action
        """
        self.table.update_min_bet(self.new_min_bet)
        self.player.pay(self.value)
        self.player.current_bet += self.value
        self.table.pot.update_highest_bet(self.player.current_bet)
        self.player.actions.get(f"{self.table.street}").append(self)
        self.update_hand_stats()

    def play(self):
        """
        Plays the action on the table and advances the seat playing
        """
        self.execute()
        self.table.advance_seat_playing()
        self.player.played = True

    def update_hand_stats(self):
        """
        Updates the hand statistics of the player according to the action
        """
        match self.table.street:
            case Street.PREFLOP:
                if not self.table.is_opened:
                    self.player.hand_stats.flag_preflop_open_opportunity = True
                if self.table.cnt_bets >= 2:
                    self.player.hand_stats.flag_preflop_face_raise = True
                if self.table.cnt_bets == 2 and self.player.stack > self.player.to_call:
                    self.player.hand_stats.flag_preflop_3bet_opportunity = True
                if self.table.cnt_bets == 3:
                    self.player.hand_stats.flag_preflop_face_3bet = True
                if self.table.cnt_bets >= 4:
                    self.player.hand_stats.flag_preflop_face_4bet = True
                if self.table.cnt_bets >= 3 and self.player.stack > self.player.to_call:
                    self.player.hand_stats.flag_preflop_4bet_opportunity = True
            case Street.FLOP:
                pass
            case Street.TURN:
                pass
            case Street.RIVER:
                pass



class FoldAction(Action):
    """
    This class represents a fold action made by a player in a poker game
    """
    def __init__(self, player):
        super().__init__(player=player, move=ActionMove.FOLD)

    def execute(self):
        super().execute()
        self.player.folded = True

    def update_hand_stats(self):
        super().update_hand_stats()
        match self.table.street:
            case Street.PREFLOP:
                self.player.hand_stats.flag_preflop_fold = True


class CheckAction(Action):
    """
    This class represents a check action made by a player in a poker game
    """
    def __init__(self, player: TablePlayer):
        super().__init__(player=player, move=ActionMove.CHECK)

    def update_hand_stats(self):
        super().update_hand_stats()
        match self.table.street:
            case Street.PREFLOP:
                pass
            case Street.FLOP:
                pass
            case Street.TURN:
                pass
            case Street.RIVER:
                pass


class CallAction(Action):
    """
    This class represents a call action made by a player in a poker game
    """
    def __init__(self, player: TablePlayer):
        super().__init__(player=player, move=ActionMove.CALL, value=player.to_call)

    def execute(self):
        super().execute()
        self.table.cnt_calls += 1

    def update_hand_stats(self):
        super().update_hand_stats()
        match self.table.street:
            case Street.PREFLOP:
                self.player.hand_stats.flag_vpip = True
                self.player.hand_stats.flag_preflop_opened = True
                self.player.hand_stats.count_preflop_player_calls += 1
                self.table.is_opened = True
                if self.table.cnt_bets == 1:
                    self.player.hand_stats.flag_preflop_limp = True
                else:
                    self.player.hand_stats.flag_preflop_cold_called = True
            case Street.FLOP:
                pass
            case Street.TURN:
                pass
            case Street.RIVER:
                pass


class BetAction(Action):
    """
    This class represents a bet action made by a player in a poker game
    """
    def __init__(self, player: TablePlayer, value: float):
        if value < player.table.min_bet:
            raise ValueError(f"Bet value must be at least {player.table.min_bet}.")
        super().__init__(player=player, move=ActionMove.BET, value=value)

    def execute(self):
        super().execute()
        self.table.cnt_bets += 1

    def update_hand_stats(self):
        super().update_hand_stats()
        match self.table.street:
            case Street.FLOP:
                pass
            case Street.TURN:
                pass
            case Street.RIVER:
                pass


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
        super().execute()
        self.table.cnt_bets += 1

    def update_hand_stats(self):
        super().update_hand_stats()
        match self.table.street:
            case Street.PREFLOP:
                self.player.hand_stats.flag_vpip = True
                self.player.hand_stats.flag_preflop_opened = True
                self.player.hand_stats.count_preflop_player_raises += 1
                self.table.is_opened = True
                if self.table.cnt_bets == 1:
                    self.player.hand_stats.flag_preflop_first_raise = True
                if self.table.cnt_bets == 2:
                    self.player.hand_stats.flag_preflop_3bet = True
                if self.table.cnt_bets >= 3:
                    self.player.hand_stats.flag_preflop_4bet = True

            case Street.FLOP:
                pass
            case Street.TURN:
                pass
            case Street.RIVER:
                pass
