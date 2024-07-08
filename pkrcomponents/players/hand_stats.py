from attrs import define, field, Factory
from attrs.validators import instance_of, ge, optional

from pkrcomponents.actions.actions_sequence import ActionsSequence
from pkrcomponents.cards.combo import Combo


@define
class HandStats:
    """
    This class represents the statistics of a player's hand in a poker game
    Attributes:
        # A. Preflop stats
        # 1. Flags
        flag_vpip (bool): Whether the player voluntarily put money in the pot
        flag_preflop_open_opportunity (bool): Whether the player had the opportunity to open preflop
        flag_preflop_open (bool): Whether the player opened preflop
        flag_preflop_first_raise (bool): Whether the player made the first raise preflop
        flag_preflop_fold (bool): Whether the player folded preflop
        flag_preflop_limp (bool): Whether the player limped preflop
        flag_preflop_cold_called (bool): Whether the player cold called preflop
        flag_preflop_face_raise (bool): Whether the player faced a raise preflop
        flag_preflop_bet (bool): Whether the player bet preflop (Realized at least one raise)
        flag_preflop_3bet_opportunity (bool): Whether the player had the opportunity to 3bet preflop
        flag_preflop_3bet (bool): Whether the player 3bet preflop
        flag_preflop_face_3bet (bool): Whether the player faced a 3bet preflop
        flag_preflop_4bet_opportunity (bool): Whether the player had the opportunity to 4+bet preflop
        flag_preflop_4bet (bool): Whether the player 4+bet preflop
        flag_preflop_face_4bet (bool): Whether the player faced a 4+bet preflop
        flag_squeeze_opportunity (bool): Whether the player had the opportunity to squeeze preflop
        flag_squeeze (bool): Whether the player squeezed preflop
        flag_face_squeeze (bool): Whether the player faced a squeeze preflop
        flag_steal_opportunity (bool): Whether the player had the opportunity to steal preflop
        flag_steal_attempt (bool): Whether the player attempted to steal preflop
        flag_face_steal_attempt (bool): Whether the player faced a steal attempt preflop
        flag_fold_to_steal_attempt (bool): Whether the player folded to a steal attempt preflop
        flag_blind_defense (bool): Whether the player defended the blinds preflop
        # 2. Counts
        count_preflop_player_raises (int): The number of raises the player made preflop
        count_preflop_player_calls (int): The number of calls the player made preflop
        count_faced_limps (int): The number of limps the player faced preflop
        # 3. Sequences
        preflop_actions_sequence (ActionsSequence): The sequence of actions the player made preflop
        # 4. Amounts
        amount_preflop_effective_stack (float): The effective stack the player had preflop
        amount_to_call_facing_preflop_bet (float): The amount the player had to call facing the preflop blinds
        amount_to_call_facing_preflop_2bet (float): The amount the player had to call facing the preflop 2bet
        amount_to_call_facing_preflop_3bet (float): The amount the player had to call facing the preflop 3bet
        amount_to_call_facing_preflop_4bet (float): The amount the player had to call facing the preflop 4bet
        amount_first_raise_made_preflop (float): The amount the player used on his first raise preflop
        amount_second_raise_made_preflop (float): The amount the player used on his second raise preflop
        total_preflop_bet_amount (float): The total amount the player bet preflop
        # B. Flop stats
        # 1. Flags
        flag_saw_flop (bool): Whether the player saw the flop
        flag_flop_first_to_talk (bool): Whether the player was the first to talk on the flop
        flag_flop_has_position (bool): Whether the player had position on the flop
        flag_flop_bet (bool): Whether the player bet on the flop
        flag_flop_open_opportunity (bool): Whether the player had the opportunity to open on the flop
        flag_flop_open (bool): Whether the player opened on the flop
        flag_flop_cbet_opportunity (bool): Whether the player had the opportunity to make a continuation bet on the flop
        flag_flop_cbet (bool): Whether the player made a continuation bet on the flop
        flag_flop_face_cbet (bool): Whether the player faced a continuation bet on the flop
        flag_flop_donk_bet_opportunity (bool): Whether the player had the opportunity to make a donk bet on the flop
        flag_flop_donk_bet (bool): Whether the player made a donk bet on the flop
        flag_flop_face_donk_bet (bool): Whether the player faced a donk bet on the flop
        flag_flop_first_raise (bool): Whether the player made the first raise on the flop
        flag_flop_fold (bool): Whether the player folded on the flop
        flag_flop_check (bool): Whether the player checked on the flop
        flag_flop_check_raise (bool): Whether the player check-raised on the flop
        flag_flop_face_raise (bool): Whether the player faced a raise on the flop
        flag_flop_3bet_opportunity (bool): Whether the player had the opportunity to 3bet on the flop
        flag_flop_3bet (bool): Whether the player 3bet on the flop
        flag_flop_face_3bet (bool): Whether the player faced a 3bet on the flop
        flag_flop_4bet_opportunity (bool): Whether the player had the opportunity to 4+bet on the flop
        flag_flop_4bet (bool): Whether the player 4+bet on the flop
        flag_flop_face_4bet (bool): Whether the player faced a 4+bet on the flop
        # 2. Counts
        count_flop_player_raises (int): The number of raises the player made on the flop
        count_flop_player_calls (int): The number of calls the player made on the flop
        # 3. Sequences
        flop_actions_sequence (ActionsSequence): The sequence of actions the player made on the flop
        # 4. Amounts
        amount_flop_effective_stack (float): The effective stack the player had on the flop
        amount_to_call_facing_flop_bet (float): The amount the player had to call facing the flop bet
        amount_to_call_facing_flop_2bet (float): The amount the player had to call facing the flop 2bet
        amount_to_call_facing_flop_3bet (float): The amount the player had to call facing the flop 3bet
        amount_to_call_facing_flop_4bet (float): The amount the player had to call facing the flop 4bet
        amount_bet_made_flop (float): The amount the player used to bet on the flop
        amount_first_raise_made_flop (float): The amount the player used on his first raise on the flop
        amount_second_raise_made_flop (float): The amount the player used on his second raise on the flop
        total_flop_bet_amount(float): The total amount the player bet on the flop
        # C. Turn stats
        # 1. Flags
        flag_saw_turn (bool): Whether the player saw the turn
        flag_turn_first_to_talk (bool): Whether the player was the first to talk on the turn
        flag_turn_has_position (bool): Whether the player had position on the turn
        flag_turn_bet (bool): Whether the player bet on the turn
        flag_turn_open_opportunity (bool): Whether the player had the opportunity to open on the turn
        flag_turn_open (bool): Whether the player opened on the turn
        flag_turn_cbet_opportunity (bool): Whether the player had the opportunity to make a continuation bet on the turn
        flag_turn_cbet (bool): Whether the player made a continuation bet on the turn
        flag_turn_face_cbet (bool): Whether the player faced a continuation bet on the turn
        flag_turn_donk_bet_opportunity (bool): Whether the player had the opportunity to make a donk bet on the turn
        flag_turn_donk_bet (bool): Whether the player made a donk bet on the turn
        flag_turn_face_donk_bet (bool): Whether the player faced a donk bet on the turn
        flag_turn_first_raise (bool): Whether the player made the first raise on the turn
        flag_turn_fold (bool): Whether the player folded on the turn
        flag_turn_check (bool): Whether the player checked on the turn
        flag_turn_check_raise (bool): Whether the player check-raised on the turn
        flag_turn_face_raise (bool): Whether the player faced a raise on the turn
        flag_turn_3bet_opportunity (bool): Whether the player had the opportunity to 3bet on the turn
        flag_turn_3bet (bool): Whether the player 3bet on the turn
        flag_turn_face_3bet (bool): Whether the player faced a 3bet on the turn
        flag_turn_4bet_opportunity (bool): Whether the player had the opportunity to 4+bet on the turn
        flag_turn_4bet (bool): Whether the player 4+bet on the turn
        flag_turn_face_4bet (bool): Whether the player faced a 4+bet on the turn
        # 2. Counts
        count_turn_player_raises (int): The number of raises the player made on the turn
        count_turn_player_calls (int): The number of calls the player made on the turn
        # 3. Sequences
        turn_actions_sequence (ActionsSequence): The sequence of actions the player made on the turn
        # 4. Amounts
        amount_turn_effective_stack (float): The effective stack the player had on the turn
        amount_to_call_facing_turn_bet (float): The amount the player had to call facing the turn bet
        amount_to_call_facing_turn_2bet (float): The amount the player had to call facing the turn 2bet
        amount_to_call_facing_turn_3bet (float): The amount the player had to call facing the turn 3bet
        amount_to_call_facing_turn_4bet (float): The amount the player had to call facing the turn 4bet
        amount_bet_made_turn (float): The amount the player used to bet on the turn
        amount_first_raise_made_turn (float): The amount the player used on his first raise on the turn
        amount_second_raise_made_turn (float): The amount the player used on his second raise on the turn
        total_turn_bet_amount(float): The total amount the player bet on the turn
        # D. River stats
        # 1. Flags
        flag_saw_river (bool): Whether the player saw the river
        flag_river_first_to_talk (bool): Whether the player was the first to talk on the river
        flag_river_has_position (bool): Whether the player had position on the river
        flag_river_bet (bool): Whether the player bet on the river
        flag_river_open_opportunity (bool): Whether the player had the opportunity to open on the river
        flag_river_open (bool): Whether the player opened on the river
        flag_river_cbet_opportunity (bool): Whether the player had the opportunity to make a c-bet on the river
        flag_river_cbet (bool): Whether the player made a continuation bet on the river
        flag_river_face_cbet (bool): Whether the player faced a continuation bet on the river
        flag_river_donk_bet_opportunity (bool): Whether the player had the opportunity to make a donk bet on the river
        flag_river_donk_bet (bool): Whether the player made a donk bet on the river
        flag_river_face_donk_bet (bool): Whether the player faced a donk bet on the river
        flag_river_first_raise (bool): Whether the player made the first raise on the river
        flag_river_fold (bool): Whether the player folded on the river
        flag_river_check (bool): Whether the player checked on the river
        flag_river_check_raise (bool): Whether the player check-raised on the river
        flag_river_face_raise (bool): Whether the player faced a raise on the river
        flag_river_3bet_opportunity (bool): Whether the player had the opportunity to 3bet on the river
        flag_river_3bet (bool): Whether the player 3bet on the river
        flag_river_face_3bet (bool): Whether the player faced a 3bet on the river
        flag_river_4bet_opportunity (bool): Whether the player had the opportunity to 4+bet on the river
        flag_river_4bet (bool): Whether the player 4+bet on the river
        flag_river_face_4bet (bool): Whether the player faced a 4+bet on the river
        # 2. Counts
        count_river_player_raises (int): The number of raises the player made on the river
        count_river_player_calls (int): The number of calls the player made on the river
        # 3. Sequences
        river_actions_sequence (ActionsSequence): The sequence of actions the player made on the river
        # 4. Amounts
        amount_river_effective_stack (float): The effective stack the player had on the river
        amount_to_call_facing_river_bet (float): The amount the player had to call facing the river bet
        amount_to_call_facing_river_2bet (float): The amount the player had to call facing the river 2bet
        amount_to_call_facing_river_3bet (float): The amount the player had to call facing the river 3bet
        amount_to_call_facing_river_4bet (float): The amount the player had to call facing the river 4bet
        amount_bet_made_river (float): The amount the player used to bet on the river
        amount_first_raise_made_river (float): The amount the player used on his first raise on the river
        amount_second_raise_made_river (float): The amount the player used on his second raise on the river
        total_river_bet_amount(float): The total amount the player bet on the river
        # E. General stats
        combo (Combo): The combo the player had
        starting_stack (float): The starting stack of the player at the beginning of the hand
        starting_stack_bb (float): The starting stack of the player at the beginning of the hand in big blinds
        amount_won (float): The amount the player won in the hand
        flag_went_to_showdown (bool): Whether the player went to showdown
        flag_is_hero (bool): Whether the player is the hero
        flag_won_hand (bool): Whether the player won the hand
        total_bet_amount (float): The total amount the player bet in the hand
    """
    # pylint: disable=too-many-instance-attributes
    # A. Preflop stats
    # 1. Flags
    flag_vpip = field(default=False, validator=instance_of(bool))
    flag_preflop_open_opportunity = field(default=False, validator=instance_of(bool))
    flag_preflop_open = field(default=False, validator=instance_of(bool))
    flag_preflop_first_raise = field(default=False, validator=instance_of(bool))
    flag_preflop_fold = field(default=False, validator=instance_of(bool))
    flag_preflop_limp = field(default=False, validator=instance_of(bool))
    flag_preflop_cold_called = field(default=False, validator=instance_of(bool))
    flag_preflop_face_raise = field(default=False, validator=instance_of(bool))
    flag_preflop_bet = field(default=False, validator=instance_of(bool))
    flag_preflop_3bet_opportunity = field(default=False, validator=instance_of(bool))
    flag_preflop_3bet = field(default=False, validator=instance_of(bool))
    flag_preflop_face_3bet = field(default=False, validator=instance_of(bool))
    flag_preflop_4bet_opportunity = field(default=False, validator=instance_of(bool))
    flag_preflop_4bet = field(default=False, validator=instance_of(bool))
    flag_preflop_face_4bet = field(default=False, validator=instance_of(bool))
    flag_squeeze_opportunity = field(default=False, validator=instance_of(bool))
    flag_squeeze = field(default=False, validator=instance_of(bool))
    flag_face_squeeze = field(default=False, validator=instance_of(bool))
    flag_steal_opportunity = field(default=False, validator=instance_of(bool))
    flag_steal_attempt = field(default=False, validator=instance_of(bool))
    flag_face_steal_attempt = field(default=False, validator=instance_of(bool))
    flag_fold_to_steal_attempt = field(default=False, validator=instance_of(bool))
    flag_blind_defense = field(default=False, validator=instance_of(bool))
    # 2. Counts
    count_preflop_player_raises = field(default=0, validator=ge(0))
    count_preflop_player_calls = field(default=0, validator=ge(0))
    count_faced_limps = field(default=0, validator=ge(0))
    # 3. Sequences
    preflop_actions_sequence = field(default=Factory(lambda: ActionsSequence()), validator=instance_of(ActionsSequence))
    # 4. Amounts
    amount_preflop_effective_stack = field(default=0, validator=instance_of(float))
    amount_to_call_facing_preflop_bet = field(default=0, validator=instance_of(float))
    amount_to_call_facing_preflop_2bet = field(default=0, validator=instance_of(float))
    amount_to_call_facing_preflop_3bet = field(default=0, validator=instance_of(float))
    amount_to_call_facing_preflop_4bet = field(default=0, validator=instance_of(float))
    amount_first_raise_made_preflop = field(default=0, validator=instance_of(float))
    amount_second_raise_made_preflop = field(default=0, validator=instance_of(float))
    total_preflop_bet_amount = field(default=0, validator=instance_of(float))
    # B. Flop stats
    # 1. Flags
    flag_saw_flop = field(default=False, validator=instance_of(bool))
    flag_flop_first_to_talk = field(default=False, validator=instance_of(bool))
    flag_flop_has_position = field(default=False, validator=instance_of(bool))
    flag_flop_bet = field(default=False, validator=instance_of(bool))
    flag_flop_open_opportunity = field(default=False, validator=instance_of(bool))
    flag_flop_open = field(default=False, validator=instance_of(bool))
    flag_flop_cbet_opportunity = field(default=False, validator=instance_of(bool))
    flag_flop_cbet = field(default=False, validator=instance_of(bool))
    flag_flop_face_cbet = field(default=False, validator=instance_of(bool))
    flag_flop_donk_bet_opportunity = field(default=False, validator=instance_of(bool))
    flag_flop_donk_bet = field(default=False, validator=instance_of(bool))
    flag_flop_face_donk_bet = field(default=False, validator=instance_of(bool))
    flag_flop_first_raise = field(default=False, validator=instance_of(bool))
    flag_flop_fold = field(default=False, validator=instance_of(bool))
    flag_flop_check = field(default=False, validator=instance_of(bool))
    flag_flop_check_raise = field(default=False, validator=instance_of(bool))
    flag_flop_face_raise = field(default=False, validator=instance_of(bool))
    flag_flop_3bet_opportunity = field(default=False, validator=instance_of(bool))
    flag_flop_3bet = field(default=False, validator=instance_of(bool))
    flag_flop_face_3bet = field(default=False, validator=instance_of(bool))
    flag_flop_4bet_opportunity = field(default=False, validator=instance_of(bool))
    flag_flop_4bet = field(default=False, validator=instance_of(bool))
    flag_flop_face_4bet = field(default=False, validator=instance_of(bool))
    # 2. Counts
    count_flop_player_raises = field(default=0, validator=ge(0))
    count_flop_player_calls = field(default=0, validator=ge(0))
    # 3. Sequences
    flop_actions_sequence = field(default=Factory(lambda: ActionsSequence()), validator=instance_of(ActionsSequence))
    # 4. Amounts
    amount_flop_effective_stack = field(default=0, validator=instance_of(float))
    amount_to_call_facing_flop_bet = field(default=0, validator=instance_of(float))
    amount_to_call_facing_flop_2bet = field(default=0, validator=instance_of(float))
    amount_to_call_facing_flop_3bet = field(default=0, validator=instance_of(float))
    amount_to_call_facing_flop_4bet = field(default=0, validator=instance_of(float))
    amount_bet_made_flop = field(default=0, validator=instance_of(float))
    amount_first_raise_made_flop = field(default=0, validator=instance_of(float))
    amount_second_raise_made_flop = field(default=0, validator=instance_of(float))
    total_flop_bet_amount = field(default=0, validator=instance_of(float))
    # C. Turn stats
    # 1. Flags
    flag_saw_turn = field(default=False, validator=instance_of(bool))
    flag_turn_first_to_talk = field(default=False, validator=instance_of(bool))
    flag_turn_has_position = field(default=False, validator=instance_of(bool))
    flag_turn_bet = field(default=False, validator=instance_of(bool))
    flag_turn_open_opportunity = field(default=False, validator=instance_of(bool))
    flag_turn_open = field(default=False, validator=instance_of(bool))
    flag_turn_cbet_opportunity = field(default=False, validator=instance_of(bool))
    flag_turn_cbet = field(default=False, validator=instance_of(bool))
    flag_turn_face_cbet = field(default=False, validator=instance_of(bool))
    flag_turn_donk_bet_opportunity = field(default=False, validator=instance_of(bool))
    flag_turn_donk_bet = field(default=False, validator=instance_of(bool))
    flag_turn_face_donk_bet = field(default=False, validator=instance_of(bool))
    flag_turn_first_raise = field(default=False, validator=instance_of(bool))
    flag_turn_fold = field(default=False, validator=instance_of(bool))
    flag_turn_check = field(default=False, validator=instance_of(bool))
    flag_turn_check_raise = field(default=False, validator=instance_of(bool))
    flag_turn_face_raise = field(default=False, validator=instance_of(bool))
    flag_turn_3bet_opportunity = field(default=False, validator=instance_of(bool))
    flag_turn_3bet = field(default=False, validator=instance_of(bool))
    flag_turn_face_3bet = field(default=False, validator=instance_of(bool))
    flag_turn_4bet_opportunity = field(default=False, validator=instance_of(bool))
    flag_turn_4bet = field(default=False, validator=instance_of(bool))
    flag_turn_face_4bet = field(default=False, validator=instance_of(bool))
    # 2. Counts
    count_turn_player_raises = field(default=0, validator=ge(0))
    count_turn_player_calls = field(default=0, validator=ge(0))
    # 3. Sequences
    turn_actions_sequence = field(default=Factory(lambda: ActionsSequence()), validator=instance_of(ActionsSequence))
    # 4. Amounts
    amount_turn_effective_stack = field(default=0, validator=instance_of(float))
    amount_to_call_facing_turn_bet = field(default=0, validator=instance_of(float))
    amount_to_call_facing_turn_2bet = field(default=0, validator=instance_of(float))
    amount_to_call_facing_turn_3bet = field(default=0, validator=instance_of(float))
    amount_to_call_facing_turn_4bet = field(default=0, validator=instance_of(float))
    amount_bet_made_turn = field(default=0, validator=instance_of(float))
    amount_first_raise_made_turn = field(default=0, validator=instance_of(float))
    amount_second_raise_made_turn = field(default=0, validator=instance_of(float))
    total_turn_bet_amount = field(default=0, validator=instance_of(float))
    # D. River stats
    # 1. Flags
    flag_saw_river = field(default=False, validator=instance_of(bool))
    flag_river_first_to_talk = field(default=False, validator=instance_of(bool))
    flag_river_has_position = field(default=False, validator=instance_of(bool))
    flag_river_bet = field(default=False, validator=instance_of(bool))
    flag_river_open_opportunity = field(default=False, validator=instance_of(bool))
    flag_river_open = field(default=False, validator=instance_of(bool))
    flag_river_cbet_opportunity = field(default=False, validator=instance_of(bool))
    flag_river_cbet = field(default=False, validator=instance_of(bool))
    flag_river_face_cbet = field(default=False, validator=instance_of(bool))
    flag_river_donk_bet_opportunity = field(default=False, validator=instance_of(bool))
    flag_river_donk_bet = field(default=False, validator=instance_of(bool))
    flag_river_face_donk_bet = field(default=False, validator=instance_of(bool))
    flag_river_first_raise = field(default=False, validator=instance_of(bool))
    flag_river_fold = field(default=False, validator=instance_of(bool))
    flag_river_check = field(default=False, validator=instance_of(bool))
    flag_river_check_raise = field(default=False, validator=instance_of(bool))
    flag_river_face_raise = field(default=False, validator=instance_of(bool))
    flag_river_3bet_opportunity = field(default=False, validator=instance_of(bool))
    flag_river_3bet = field(default=False, validator=instance_of(bool))
    flag_river_face_3bet = field(default=False, validator=instance_of(bool))
    flag_river_4bet_opportunity = field(default=False, validator=instance_of(bool))
    flag_river_4bet = field(default=False, validator=instance_of(bool))
    flag_river_face_4bet = field(default=False, validator=instance_of(bool))
    # 2. Counts
    count_river_player_raises = field(default=0, validator=ge(0))
    count_river_player_calls = field(default=0, validator=ge(0))
    # 3. Sequences
    river_actions_sequence = field(default=Factory(lambda: ActionsSequence()), validator=instance_of(ActionsSequence))
    # 4. Amounts
    amount_river_effective_stack = field(default=0, validator=instance_of(float))
    amount_to_call_facing_river_bet = field(default=0, validator=instance_of(float))
    amount_to_call_facing_river_2bet = field(default=0, validator=instance_of(float))
    amount_to_call_facing_river_3bet = field(default=0, validator=instance_of(float))
    amount_to_call_facing_river_4bet = field(default=0, validator=instance_of(float))
    amount_bet_made_river = field(default=0, validator=instance_of(float))
    amount_first_raise_made_river = field(default=0, validator=instance_of(float))
    amount_second_raise_made_river = field(default=0, validator=instance_of(float))
    total_river_bet_amount = field(default=0, validator=instance_of(float))
    # E. General stats
    combo = field(default=None, validator=optional(instance_of(Combo)))
    starting_stack = field(default=0, validator=[ge(0), instance_of(float)])
    starting_stack_bb = field(default=0, validator=[ge(0), instance_of(float)])
    amount_won = field(default=0, validator=instance_of(float))
    flag_went_to_showdown = field(default=False, validator=instance_of(bool))
    flag_is_hero = field(default=False, validator=instance_of(bool))
    flag_won_hand = field(default=False, validator=instance_of(bool))
    total_bet_amount = field(default=0, validator=instance_of(float))

    def reset(self):
        """
        Resets the statistics
        """
        # A. Preflop stats
        # 1. Flags
        self.flag_vpip = False
        self.flag_preflop_open_opportunity = False
        self.flag_preflop_open = False
        self.flag_preflop_first_raise = False
        self.flag_preflop_fold = False
        self.flag_preflop_limp = False
        self.flag_preflop_cold_called = False
        self.flag_preflop_face_raise = False
        self.flag_preflop_bet = False
        self.flag_preflop_3bet_opportunity = False
        self.flag_preflop_3bet = False
        self.flag_preflop_face_3bet = False
        self.flag_preflop_4bet_opportunity = False
        self.flag_preflop_4bet = False
        self.flag_preflop_face_4bet = False
        self.flag_squeeze_opportunity = False
        self.flag_squeeze = False
        self.flag_face_squeeze = False
        self.flag_steal_opportunity = False
        self.flag_steal_attempt = False
        self.flag_face_steal_attempt = False
        self.flag_fold_to_steal_attempt = False
        self.flag_blind_defense = False
        # 2. Counts
        self.count_preflop_player_raises = 0
        self.count_preflop_player_calls = 0
        self.count_faced_limps = 0
        # 3. Sequences
        self.preflop_actions_sequence = ActionsSequence()
        # 4. Amounts
        self.amount_preflop_effective_stack = 0
        self.amount_to_call_facing_preflop_bet = 0
        self.amount_to_call_facing_preflop_2bet = 0
        self.amount_to_call_facing_preflop_3bet = 0
        self.amount_to_call_facing_preflop_4bet = 0
        self.amount_first_raise_made_preflop = 0
        self.amount_second_raise_made_preflop = 0
        # B. Flop stats
        # 1. Flags
        self.flag_saw_flop = False
        self.flag_flop_first_to_talk = False
        self.flag_flop_has_position = False
        self.flag_flop_bet = False
        self.flag_flop_cbet_opportunity = False
        self.flag_flop_cbet = False
        self.flag_flop_face_cbet = False
        self.flag_flop_donk_bet_opportunity = False
        self.flag_flop_donk_bet = False
        self.flag_flop_face_donk_bet = False
        self.flag_flop_first_raise = False
        self.flag_flop_check = False
        self.flag_flop_check_raise = False
        self.flag_flop_face_raise = False
        self.flag_flop_3bet_opportunity = False
        self.flag_flop_3bet = False
        self.flag_flop_4bet_opportunity = False
        self.flag_flop_4bet = False
        self.flag_flop_face_4bet = False
        # 2. Counts
        self.count_flop_player_raises = 0
        self.count_flop_player_calls = 0
        # 3. Sequences
        self.flop_actions_sequence = ActionsSequence()
        # 4. Amounts
        self.amount_flop_effective_stack = 0
        self.amount_to_call_facing_flop_bet = 0
        self.amount_to_call_facing_flop_2bet = 0
        self.amount_to_call_facing_flop_3bet = 0
        self.amount_to_call_facing_flop_4bet = 0
        self.amount_bet_made_flop = 0
        self.amount_first_raise_made_flop = 0
        self.amount_second_raise_made_flop = 0
        # C. Turn stats
        # 1. Flags
        self.flag_saw_turn = False
        self.flag_turn_first_to_talk = False
        self.flag_turn_has_position = False
        self.flag_turn_bet = False
        self.flag_turn_cbet_opportunity = False
        self.flag_turn_cbet = False
        self.flag_turn_face_cbet = False
        self.flag_turn_donk_bet_opportunity = False
        self.flag_turn_donk_bet = False
        self.flag_turn_face_donk_bet = False
        self.flag_turn_first_raise = False
        self.flag_turn_fold = False
        self.flag_turn_check = False
        self.flag_turn_check_raise = False
        self.flag_turn_face_raise = False
        self.flag_turn_3bet_opportunity = False
        self.flag_turn_3bet = False
        self.flag_turn_face_3bet = False
        self.flag_turn_4bet_opportunity = False
        self.flag_turn_4bet = False
        self.flag_turn_face_4bet = False
        # 2. Counts
        self.count_turn_player_raises = 0
        self.count_turn_player_calls = 0
        # 3. Sequences
        self.turn_actions_sequence = ActionsSequence()
        # 4. Amounts
        self.amount_turn_effective_stack = 0
        self.amount_to_call_facing_turn_bet = 0
        self.amount_to_call_facing_turn_2bet = 0
        self.amount_to_call_facing_turn_3bet = 0
        self.amount_to_call_facing_turn_4bet = 0
        self.amount_bet_made_turn = 0
        self.amount_first_raise_made_turn = 0
        self.amount_second_raise_made_turn = 0
        # D. River stats
        # 1. Flags
        self.flag_saw_river = False
        self.flag_river_first_to_talk = False
        self.flag_river_has_position = False
        self.flag_river_bet = False
        self.flag_river_cbet_opportunity = False
        self.flag_river_cbet = False
        self.flag_river_face_cbet = False
        self.flag_river_donk_bet_opportunity = False
        self.flag_river_donk_bet = False
        self.flag_river_face_donk_bet = False
        self.flag_river_first_raise = False
        self.flag_river_fold = False
        self.flag_river_check = False
        self.flag_river_check_raise = False
        self.flag_river_face_raise = False
        self.flag_river_3bet_opportunity = False
        self.flag_river_3bet = False
        self.flag_river_face_3bet = False
        self.flag_river_4bet_opportunity = False
        self.flag_river_4bet = False
        self.flag_river_face_4bet = False
        # 2. Counts
        self.count_river_player_raises = 0
        self.count_river_player_calls = 0
        # 3. Sequences
        self.river_actions_sequence = ActionsSequence()
        # 4. Amounts
        self.amount_river_effective_stack = 0
        self.amount_to_call_facing_river_bet = 0
        self.amount_to_call_facing_river_2bet = 0
        self.amount_to_call_facing_river_3bet = 0
        self.amount_to_call_facing_river_4bet = 0
        self.amount_bet_made_river = 0
        self.amount_first_raise_made_river = 0
        self.amount_second_raise_made_river = 0
        # E. General stats
        self.combo = None
        self.starting_stack = 0
        self.starting_stack_bb = 0
        self.flag_went_to_showdown = False
        self.flag_is_hero = False
        self.flag_won_hand = False


