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
        self.add_to_history()
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
                if self.player.face_raise:
                    self.player.hand_stats.flag_preflop_face_raise = True
                if self.table.cnt_cold_calls > 0 and self.player.can_3bet:
                    self.player.hand_stats.flag_preflop_squeeze_opportunity = True
                if self.player.can_3bet:
                    self.player.hand_stats.flag_preflop_3bet_opportunity = True
                if self.player.face_3bet:
                    self.player.hand_stats.flag_preflop_face_3bet = True
                if self.table.cnt_bets >= 4:
                    self.player.hand_stats.flag_preflop_face_4bet = True
                if self.player.can_4bet:
                    self.player.hand_stats.flag_preflop_4bet_opportunity = True
            case Street.FLOP:
                if self.player.can_open:
                    self.player.hand_stats.flag_flop_open_opportunity = True
                if self.player.can_cbet:
                    self.player.hand_stats.flag_flop_cbet_opportunity = True
                if self.player.can_donk_bet:
                    self.player.hand_stats.flag_flop_donk_bet_opportunity = True
                if self.player.face_raise:
                    self.player.hand_stats.flag_flop_first_raise = True
                if self.player.can_3bet:
                    self.player.hand_stats.flag_flop_3bet_opportunity = True
            case Street.TURN:
                pass
            case Street.RIVER:
                pass

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

        self.player.folded = True
        super().execute()

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
                self.player.hand_stats.flag_flop_check = True
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
        self.table.is_opened = True

    def update_hand_stats(self):
        super().update_hand_stats()
        match self.table.street:
            case Street.PREFLOP:
                self.player.hand_stats.flag_vpip = True
                self.player.hand_stats.flag_preflop_opened = True
                self.player.hand_stats.count_preflop_player_calls += 1
                if self.player.can_first_raise:
                    self.player.hand_stats.flag_preflop_limp = True
                else:
                    self.player.hand_stats.flag_preflop_cold_called = True
                    self.table.cnt_cold_calls += 1

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
        self.table.cnt_bets += 1
        self.player.take_initiative()
        super().execute()

    def update_hand_stats(self):
        super().update_hand_stats()
        match self.table.street:
            case Street.FLOP:
                if self.player.can_open:
                    self.player.hand_stats.flag_flop_open = True
                self.player.hand_stats.flag_flop_bet = True
                if self.player.has_initiative:
                    self.player.hand_stats.flag_flop_cbet = True
                else:
                    self.player.hand_stats.flag_flop_donk_bet = True
            case Street.TURN:
                self.player.hand_stats.flag_turn_bet = True
            case Street.RIVER:
                self.player.hand_stats.flag_river_bet = True


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
        self.table.cnt_bets += 1
        self.table.is_opened = True
        self.player.take_initiative()
        super().execute()

    def update_hand_stats(self):
        super().update_hand_stats()
        match self.table.street:
            case Street.PREFLOP:
                self.player.hand_stats.flag_vpip = True
                self.player.hand_stats.flag_preflop_opened = True
                self.player.hand_stats.count_preflop_player_raises += 1
                if self.player.can_first_raise:
                    self.player.hand_stats.flag_preflop_first_raise = True
                if self.table.cnt_bets == 2:
                    self.player.hand_stats.flag_preflop_3bet = True
                    if self.table.cnt_cold_calls > 0:
                        self.player.hand_stats.flag_preflop_squeeze = True
                if self.table.cnt_bets >= 3:
                    self.player.hand_stats.flag_preflop_4bet = True

            case Street.FLOP:
                if self.player.can_first_raise:
                    self.player.hand_stats.flag_flop_first_raise = True
                if self.table.cnt_bets == 2:
                    self.player.hand_stats.flag_flop_3bet = True
                if self.table.cnt_bets >= 3:
                    self.player.hand_stats.flag_flop_4bet = True

            case Street.TURN:
                pass
            case Street.RIVER:
                pass
