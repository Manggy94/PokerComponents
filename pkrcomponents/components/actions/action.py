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

    def update_hand_stats(self):
        """
        Updates the hand statistics of the player according to the action
        """
        if self.is_all_in:
            self.player.flag_street_went_all_in = True
            self.hand_stats.all_in_street = self.table.street
        if not any(player.flag_street_first_to_talk for player in self.table.players_in_game):
            self.player.flag_street_first_to_talk = True
        if self.player.is_facing_covering_bet:
            self.hand_stats.face_covering_bet_street = self.table.street
            self.hand_stats.facing_covering_bet_move = self.move
        if self.player.is_facing_all_in:
            self.hand_stats.face_all_in_street = self.table.street
            self.hand_stats.facing_all_in_move = self.move
        match self.table.street:
            case Street.PREFLOP:
                self.hand_stats.flag_voluntary_all_in_preflop = self.value >= self.player.effective_stack
                self.hand_stats.preflop_actions_sequence = self.player.actions_history.preflop
                self.hand_stats.total_preflop_bet_amount = sum(
                    [action.value for action in self.hand_stats.preflop_actions_sequence.actions])
                if not self.table.is_opened:
                    self.hand_stats.flag_preflop_open_opportunity = True
                    self.hand_stats.count_faced_limps = self.table.cnt_limps
                if self.hand_stats.amount_preflop_effective_stack == 0:
                    self.hand_stats.amount_preflop_effective_stack = self.player.effective_stack
                if self.player.can_raise:
                    self.hand_stats.flag_preflop_raise_opportunity = True
                if self.player.is_facing_raise:
                    self.hand_stats.flag_preflop_face_raise = True
                if self.player.can_squeeze:
                    self.hand_stats.flag_squeeze_opportunity = True
                if self.player.is_facing_squeeze:
                    self.hand_stats.flag_face_squeeze = True
                    self.hand_stats.move_facing_squeeze = self.move
                if self.player.can_steal:
                    self.hand_stats.flag_steal_opportunity = True
                if self.player.is_facing_steal:
                    self.hand_stats.flag_face_steal_attempt = True
                    self.hand_stats.move_facing_steal_attempt = self.move
                if self.player.is_defending_blinds:
                    self.hand_stats.flag_blind_defense_opportunity = True
                if self.player.is_facing_1bet:
                    self.hand_stats.amount_to_call_facing_preflop_bb = self.player.to_call
                    self.hand_stats.ratio_to_call_facing_preflop_bb = self.player.to_call / self.table.pot_value
                if self.player.is_facing_2bet:
                    self.hand_stats.move_facing_preflop_2bet = self.move
                    self.hand_stats.amount_to_call_facing_preflop_2bet = self.player.to_call
                    self.hand_stats.ratio_to_call_facing_preflop_2bet = self.player.to_call / self.table.pot_value
                if self.player.is_facing_3bet:
                    self.hand_stats.flag_preflop_face_3bet = True
                    self.hand_stats.move_facing_preflop_3bet = self.move
                    self.hand_stats.amount_to_call_facing_preflop_3bet = self.player.to_call
                    self.hand_stats.ratio_to_call_facing_preflop_3bet = self.player.to_call / self.table.pot_value
                if self.player.is_facing_4bet:
                    self.hand_stats.flag_preflop_face_4bet = True
                    self.hand_stats.move_facing_preflop_4bet = self.move
                    self.hand_stats.amount_to_call_facing_preflop_4bet = self.player.to_call
                    self.hand_stats.ratio_to_call_facing_preflop_4bet = self.player.to_call / self.table.pot_value
                if self.player.can_3bet:
                    self.hand_stats.flag_preflop_3bet_opportunity = True
                if self.player.can_4bet:
                    self.hand_stats.flag_preflop_4bet_opportunity = True
            case Street.FLOP:
                self.hand_stats.flag_saw_flop = True
                self.hand_stats.flop_actions_sequence = self.player.actions_history.flop
                self.hand_stats.total_flop_bet_amount = sum(
                    [action.value for action in self.hand_stats.flop_actions_sequence.actions])
                if self.hand_stats.amount_flop_effective_stack == 0:
                    self.hand_stats.amount_flop_effective_stack = self.player.effective_stack
                if self.player.flag_street_first_to_talk:
                    self.hand_stats.flag_flop_first_to_talk = True
                if self.player.is_facing_cbet:
                    self.hand_stats.flag_flop_face_cbet = True
                    self.hand_stats.move_facing_flop_cbet = self.move
                if self.player.is_facing_donk_bet:
                    self.hand_stats.flag_flop_face_donk_bet = True
                    self.hand_stats.move_facing_flop_donk_bet = self.move
                if self.player.is_facing_raise:
                    self.hand_stats.flag_flop_face_raise = True
                if self.player.is_facing_1bet:
                    self.hand_stats.amount_to_call_facing_flop_bet = self.player.to_call
                    self.hand_stats.ratio_to_call_facing_flop_bet = self.player.to_call / self.table.pot_value
                    self.hand_stats.move_facing_flop_bet = self.move
                if self.player.is_facing_2bet:
                    self.hand_stats.amount_to_call_facing_flop_2bet = self.player.to_call
                    self.hand_stats.ratio_to_call_facing_flop_2bet = self.player.to_call / self.table.pot_value
                    self.hand_stats.move_facing_flop_2bet = self.move
                if self.player.is_facing_3bet:
                    self.hand_stats.amount_to_call_facing_flop_3bet = self.player.to_call
                    self.hand_stats.ratio_to_call_facing_flop_3bet = self.player.to_call / self.table.pot_value
                    self.hand_stats.flag_flop_face_3bet = True
                    self.hand_stats.move_facing_flop_3bet = self.move
                if self.player.is_facing_4bet:
                    self.hand_stats.amount_to_call_facing_flop_4bet = self.player.to_call
                    self.hand_stats.ratio_to_call_facing_flop_4bet = self.player.to_call / self.table.pot_value
                    self.hand_stats.flag_flop_face_4bet = True
                    self.hand_stats.move_facing_flop_4bet = self.move
                if self.player.can_open:
                    self.hand_stats.flag_flop_open_opportunity = True
                if self.player.can_cbet:
                    self.hand_stats.flag_flop_cbet_opportunity = True
                if self.player.can_donk_bet:
                    self.hand_stats.flag_flop_donk_bet_opportunity = True
                if self.player.can_3bet:
                    self.hand_stats.flag_flop_3bet_opportunity = True
                if self.player.can_4bet:
                    self.hand_stats.flag_flop_4bet_opportunity = True
            case Street.TURN:
                self.hand_stats.flag_saw_turn = True
                self.hand_stats.turn_actions_sequence = self.player.actions_history.turn
                self.hand_stats.total_turn_bet_amount = sum(
                    [action.value for action in self.hand_stats.turn_actions_sequence.actions])
                if self.hand_stats.amount_turn_effective_stack == 0:
                    self.hand_stats.amount_turn_effective_stack = self.player.effective_stack
                if self.player.flag_street_first_to_talk:
                    self.hand_stats.flag_turn_first_to_talk = True
                if self.player.is_facing_cbet:
                    self.hand_stats.flag_turn_face_cbet = True
                    self.hand_stats.move_facing_turn_cbet = self.move
                if self.player.is_facing_donk_bet:
                    self.hand_stats.flag_turn_face_donk_bet = True
                    self.hand_stats.move_facing_turn_donk_bet = self.move
                if self.player.is_facing_raise:
                    self.hand_stats.flag_turn_face_raise = True
                if self.player.is_facing_1bet:
                    self.hand_stats.amount_to_call_facing_turn_bet = self.player.to_call
                    self.hand_stats.ratio_to_call_facing_turn_bet = self.player.to_call / self.table.pot_value
                    self.hand_stats.move_facing_turn_bet = self.move
                if self.player.is_facing_2bet:
                    self.hand_stats.amount_to_call_facing_turn_2bet = self.player.to_call
                    self.hand_stats.ratio_to_call_facing_turn_2bet = self.player.to_call / self.table.pot_value
                    self.hand_stats.move_facing_turn_2bet = self.move
                if self.player.is_facing_3bet:
                    self.hand_stats.amount_to_call_facing_turn_3bet = self.player.to_call
                    self.hand_stats.ratio_to_call_facing_turn_3bet = self.player.to_call / self.table.pot_value
                    self.hand_stats.flag_turn_face_3bet = True
                    self.hand_stats.move_facing_turn_3bet = self.move
                if self.player.is_facing_4bet:
                    self.hand_stats.amount_to_call_facing_turn_4bet = self.player.to_call
                    self.hand_stats.ratio_to_call_facing_turn_4bet = self.player.to_call / self.table.pot_value
                    self.hand_stats.flag_turn_face_4bet = True
                    self.hand_stats.move_facing_turn_4bet = self.move
                if self.player.can_open:
                    self.hand_stats.flag_turn_open_opportunity = True
                if self.player.can_cbet:
                    self.hand_stats.flag_turn_cbet_opportunity = True
                if self.player.can_donk_bet:
                    self.hand_stats.flag_turn_donk_bet_opportunity = True
                if self.player.can_3bet:
                    self.hand_stats.flag_turn_3bet_opportunity = True
                if self.player.can_4bet:
                    self.hand_stats.flag_turn_4bet_opportunity = True
            case Street.RIVER:
                self.hand_stats.flag_saw_river = True
                self.hand_stats.river_actions_sequence = self.player.actions_history.river
                self.hand_stats.total_river_bet_amount = sum(
                    [action.value for action in self.hand_stats.river_actions_sequence.actions])
                if self.hand_stats.amount_river_effective_stack == 0:
                    self.hand_stats.amount_river_effective_stack = self.player.effective_stack
                if self.player.flag_street_first_to_talk:
                    self.hand_stats.flag_river_first_to_talk = True
                if self.player.is_facing_cbet:
                    self.hand_stats.flag_river_face_cbet = True
                    self.hand_stats.move_facing_river_cbet = self.move
                if self.player.is_facing_donk_bet:
                    self.hand_stats.flag_river_face_donk_bet = True
                    self.hand_stats.move_facing_river_donk_bet = self.move
                if self.player.is_facing_raise:
                    self.hand_stats.flag_river_face_raise = True
                if self.player.is_facing_1bet:
                    self.hand_stats.amount_to_call_facing_river_bet = self.player.to_call
                    self.hand_stats.ratio_to_call_facing_river_bet = self.player.to_call / self.table.pot_value
                    self.hand_stats.move_facing_river_bet = self.move
                if self.player.is_facing_2bet:
                    self.hand_stats.amount_to_call_facing_river_2bet = self.player.to_call
                    self.hand_stats.ratio_to_call_facing_river_2bet = self.player.to_call / self.table.pot_value
                    self.hand_stats.move_facing_river_2bet = self.move
                if self.player.is_facing_3bet:
                    self.hand_stats.amount_to_call_facing_river_3bet = self.player.to_call
                    self.hand_stats.ratio_to_call_facing_river_3bet = self.player.to_call / self.table.pot_value
                    self.hand_stats.flag_river_face_3bet = True
                    self.hand_stats.move_facing_river_3bet = self.move
                if self.player.is_facing_4bet:
                    self.hand_stats.amount_to_call_facing_river_4bet = self.player.to_call
                    self.hand_stats.ratio_to_call_facing_river_4bet = self.player.to_call / self.table.pot_value
                    self.hand_stats.flag_river_face_4bet = True
                    self.hand_stats.move_facing_river_4bet = self.move
                if self.player.can_open:
                    self.hand_stats.flag_river_open_opportunity = True
                if self.player.can_cbet:
                    self.hand_stats.flag_river_cbet_opportunity = True
                if self.player.can_donk_bet:
                    self.hand_stats.flag_river_donk_bet_opportunity = True
                if self.player.can_3bet:
                    self.hand_stats.flag_river_3bet_opportunity = True
                if self.player.can_4bet:
                    self.hand_stats.flag_river_4bet_opportunity = True
        self.hand_stats.total_bet_amount = sum((self.hand_stats.total_preflop_bet_amount,
                                               self.hand_stats.total_flop_bet_amount,
                                               self.hand_stats.total_turn_bet_amount,
                                               self.hand_stats.total_river_bet_amount))

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
        self.player.has_initiative = False

    def update_hand_stats(self):
        super().update_hand_stats()
        self.hand_stats.fold_street = self.table.street
        match self.table.street:
            case Street.PREFLOP:
                self.hand_stats.flag_preflop_fold = True
                if self.player.is_facing_steal:
                    self.hand_stats.flag_fold_to_steal_attempt = True
            case Street.FLOP:
                self.hand_stats.flag_flop_fold = True
            case Street.TURN:
                self.hand_stats.flag_turn_fold = True
            case Street.RIVER:
                self.hand_stats.flag_river_fold = True


class CheckAction(Action):
    """
    This class represents a check action made by a player in a poker game
    """
    def __init__(self, player: TablePlayer):
        super().__init__(player=player, move=ActionMove.CHECK)

    def execute(self):
        super().execute()
        self.player.has_initiative = False

    def update_hand_stats(self):
        super().update_hand_stats()
        match self.table.street:
            case Street.FLOP:
                self.hand_stats.flag_flop_check = True
            case Street.TURN:
                self.hand_stats.flag_turn_check = True
            case Street.RIVER:
                self.hand_stats.flag_river_check = True


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
                self.hand_stats.flag_vpip = True
                self.hand_stats.flag_preflop_open = True
                self.hand_stats.count_preflop_player_calls += 1
                if self.player.is_defending_blinds:
                    self.hand_stats.flag_blind_defense = True
                if self.player.can_first_raise:
                    self.hand_stats.flag_preflop_limp = True
                    self.table.cnt_limps += 1
                else:
                    self.hand_stats.flag_preflop_cold_called = True
                    self.table.cnt_cold_calls += 1

            case Street.FLOP:
                self.hand_stats.count_flop_player_calls += 1
            case Street.TURN:
                self.hand_stats.count_turn_player_calls += 1
            case Street.RIVER:
                self.hand_stats.count_river_player_calls += 1


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

    def update_hand_stats(self):
        super().update_hand_stats()
        if self.player.has_initiative:
            self.player.flag_street_cbet = True
        else:
            self.player.flag_street_donk_bet = True
        match self.table.street:
            case Street.FLOP:
                self.hand_stats.amount_bet_made_flop = self.value
                self.hand_stats.ratio_bet_made_flop = self.value / self.table.pot_value
                self.hand_stats.flag_flop_bet = True
                if self.player.can_open:
                    self.hand_stats.flag_flop_open = True
                if self.player.can_cbet:
                    self.hand_stats.flag_flop_cbet = True
                if self.player.can_donk_bet:
                    self.hand_stats.flag_flop_donk_bet = True
            case Street.TURN:
                self.hand_stats.amount_bet_made_turn = self.value
                self.hand_stats.ratio_bet_made_turn = self.value / self.table.pot_value
                self.hand_stats.flag_turn_bet = True
                if self.player.can_open:
                    self.hand_stats.flag_turn_open = True
                if self.player.can_cbet:
                    self.hand_stats.flag_turn_cbet = True
                if self.player.can_donk_bet:
                    self.hand_stats.flag_turn_donk_bet = True
            case Street.RIVER:
                self.hand_stats.amount_bet_made_river = self.value
                self.hand_stats.ratio_bet_made_river = self.value / self.table.pot_value
                self.hand_stats.flag_river_bet = True
                if self.player.can_open:
                    self.hand_stats.flag_river_open = True
                if self.player.can_cbet:
                    self.hand_stats.flag_river_cbet = True
                if self.player.can_donk_bet:
                    self.hand_stats.flag_river_donk_bet = True


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
        # self.table.update_min_bet(self.new_min_bet)
        self.table.cnt_bets += 1
        self.table.is_opened = True
        self.player.take_initiative()

    def update_hand_stats(self):
        super().update_hand_stats()
        match self.table.street:
            case Street.PREFLOP:
                self.hand_stats.flag_vpip = True
                self.hand_stats.flag_preflop_raise = True
                if self.hand_stats.count_preflop_player_raises == 0:
                    self.hand_stats.amount_first_raise_made_preflop = self.value
                    self.hand_stats.ratio_first_raise_made_preflop = self.value / self.table.pot_value
                if self.hand_stats.count_preflop_player_raises == 1:
                    self.hand_stats.amount_second_raise_made_preflop = self.value
                    self.hand_stats.ratio_second_raise_made_preflop = self.value / self.table.pot_value
                if self.player.can_open:
                    self.hand_stats.flag_preflop_open = True
                if self.player.can_open and self.value >= self.player.effective_stack:
                    self.hand_stats.flag_open_shove = True
                if self.player.can_first_raise:
                    self.hand_stats.flag_preflop_first_raise = True
                if self.player.can_squeeze:
                    self.hand_stats.flag_squeeze = True
                if self.player.can_steal:
                    self.hand_stats.flag_steal_attempt = True
                if self.player.is_defending_blinds:
                    self.hand_stats.flag_blind_defense = True
                if self.player.can_3bet:
                    self.hand_stats.flag_preflop_3bet = True
                if self.player.can_4bet:
                    self.hand_stats.flag_preflop_4bet = True
                self.hand_stats.count_preflop_player_raises += 1
            case Street.FLOP:
                self.hand_stats.flag_flop_bet = True
                if self.hand_stats.count_flop_player_raises == 0:
                    self.hand_stats.amount_first_raise_made_flop = self.value
                    self.hand_stats.ratio_first_raise_made_flop = self.value / self.table.pot_value
                if self.hand_stats.count_flop_player_raises == 1:
                    self.hand_stats.amount_second_raise_made_flop = self.value
                    self.hand_stats.ratio_second_raise_made_flop = self.value / self.table.pot_value
                if self.player.can_first_raise:
                    self.hand_stats.flag_flop_first_raise = True
                if self.player.can_3bet:
                    self.hand_stats.flag_flop_3bet = True
                if self.player.can_4bet:
                    self.hand_stats.flag_flop_4bet = True
                if self.hand_stats.flop_actions_sequence.symbol == "XR":
                    self.hand_stats.flag_flop_check_raise = True
                self.hand_stats.count_flop_player_raises += 1
            case Street.TURN:
                self.hand_stats.flag_turn_bet = True
                if self.hand_stats.count_turn_player_raises == 0:
                    self.hand_stats.amount_first_raise_made_turn = self.value
                    self.hand_stats.ratio_first_raise_made_turn = self.value / self.table.pot_value
                if self.hand_stats.count_turn_player_raises == 1:
                    self.hand_stats.amount_second_raise_made_turn = self.value
                    self.hand_stats.ratio_second_raise_made_turn = self.value / self.table.pot_value
                if self.hand_stats.turn_actions_sequence.symbol == "XR":
                    self.hand_stats.flag_turn_check_raise = True
                if self.player.can_first_raise:
                    self.hand_stats.flag_turn_first_raise = True
                self.hand_stats.count_turn_player_raises += 1
                if self.player.can_3bet:
                    self.hand_stats.flag_turn_3bet = True
                if self.player.can_4bet:
                    self.hand_stats.flag_turn_4bet = True
            case Street.RIVER:
                self.hand_stats.flag_river_bet = True
                if self.hand_stats.count_river_player_raises == 0:
                    self.hand_stats.amount_first_raise_made_river = self.value
                    self.hand_stats.ratio_first_raise_made_river = self.value / self.table.pot_value
                if self.hand_stats.count_river_player_raises == 1:
                    self.hand_stats.amount_second_raise_made_river = self.value
                    self.hand_stats.ratio_second_raise_made_river = self.value / self.table.pot_value
                if self.hand_stats.river_actions_sequence.symbol == "XR":
                    self.hand_stats.flag_river_check_raise = True
                if self.player.can_first_raise:
                    self.hand_stats.flag_river_first_raise = True
                self.hand_stats.count_river_player_raises += 1
                if self.player.can_3bet:
                    self.hand_stats.flag_river_3bet = True
                if self.player.can_4bet:
                    self.hand_stats.flag_river_4bet = True
