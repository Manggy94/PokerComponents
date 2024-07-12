from attrs import define, Factory

from pkrcomponents.components.actions.action_move import ActionMove
from pkrcomponents.components.actions.actions_sequence import ActionsSequence
from pkrcomponents.components.players.datafields import preflop


@define
class PreflopPlayerHandStats:
    flag_vpip = preflop.FLAG_VPIP
    flag_open_opportunity = preflop.FLAG_PREFLOP_OPEN_OPPORTUNITY
    flag_open = preflop.FLAG_PREFLOP_OPEN
    flag_first_raise = preflop.FLAG_PREFLOP_FIRST_RAISE
    flag_fold = preflop.FLAG_PREFLOP_FOLD
    flag_limp = preflop.FLAG_PREFLOP_LIMP
    flag_cold_called = preflop.FLAG_PREFLOP_COLD_CALLED
    flag_raise_opportunity = preflop.FLAG_PREFLOP_RAISE_OPPORTUNITY
    flag_raise = preflop.FLAG_PREFLOP_RAISE
    flag_face_raise = preflop.FLAG_PREFLOP_FACE_RAISE
    flag_3bet_opportunity = preflop.FLAG_PREFLOP_3BET_OPPORTUNITY
    flag_3bet = preflop.FLAG_PREFLOP_3BET
    flag_face_3bet = preflop.FLAG_PREFLOP_FACE_3BET
    flag_4bet_opportunity = preflop.FLAG_PREFLOP_4BET_OPPORTUNITY
    flag_4bet = preflop.FLAG_PREFLOP_4BET
    flag_face_4bet = preflop.FLAG_PREFLOP_FACE_4BET
    flag_squeeze_opportunity = preflop.FLAG_SQUEEZE_OPPORTUNITY
    flag_squeeze = preflop.FLAG_SQUEEZE
    flag_face_squeeze = preflop.FLAG_FACE_SQUEEZE
    flag_steal_opportunity = preflop.FLAG_STEAL_OPPORTUNITY
    flag_steal_attempt = preflop.FLAG_STEAL_ATTEMPT
    flag_face_steal_attempt = preflop.FLAG_FACE_STEAL_ATTEMPT
    flag_fold_to_steal_attempt = preflop.FLAG_FOLD_TO_STEAL_ATTEMPT
    flag_blind_defense_opportunity = preflop.FLAG_BLIND_DEFENSE_OPPORTUNITY
    flag_blind_defense = preflop.FLAG_BLIND_DEFENSE
    flag_open_shove = preflop.FLAG_OPEN_SHOVE
    flag_voluntary_all_in = preflop.FLAG_VOLUNTARY_ALL_IN_PREFLOP
    # 2. Counts
    count_player_raises = preflop.COUNT_PREFLOP_PLAYER_RAISES
    count_player_calls = preflop.COUNT_PREFLOP_PLAYER_CALLS
    count_faced_limps = preflop.COUNT_FACED_LIMPS
    # 3. Sequences
    actions_sequence = preflop.PREFLOP_ACTIONS_SEQUENCE
    # 4. Amounts
    amount_effective_stack = preflop.AMOUNT_PREFLOP_EFFECTIVE_STACK
    amount_to_call_facing_bet = preflop.AMOUNT_TO_CALL_FACING_PREFLOP_BB
    amount_to_call_facing_2bet = preflop.AMOUNT_TO_CALL_FACING_PREFLOP_2BET
    amount_to_call_facing_3bet = preflop.AMOUNT_TO_CALL_FACING_PREFLOP_3BET
    amount_to_call_facing_4bet = preflop.AMOUNT_TO_CALL_FACING_PREFLOP_4BET
    amount_first_raise_made = preflop.AMOUNT_FIRST_RAISE_MADE_PREFLOP
    amount_second_raise_made = preflop.AMOUNT_SECOND_RAISE_MADE_PREFLOP
    ratio_to_call_facing_bet = preflop.RATIO_TO_CALL_FACING_PREFLOP_BB
    ratio_to_call_facing_2bet = preflop.RATIO_TO_CALL_FACING_PREFLOP_2BET
    ratio_to_call_facing_3bet = preflop.RATIO_TO_CALL_FACING_PREFLOP_3BET
    ratio_to_call_facing_4bet = preflop.RATIO_TO_CALL_FACING_PREFLOP_4BET
    ratio_first_raise_made = preflop.RATIO_FIRST_RAISE_MADE_PREFLOP
    ratio_second_raise_made = preflop.RATIO_SECOND_RAISE_MADE_PREFLOP
    total_bet_amount = preflop.TOTAL_PREFLOP_BET_AMOUNT
    # 5. Moves
    move_facing_2bet = preflop.MOVE_FACING_PREFLOP_2BET
    move_facing_3bet = preflop.MOVE_FACING_PREFLOP_3BET
    move_facing_4bet = preflop.MOVE_FACING_PREFLOP_4BET
    move_facing_squeeze = preflop.MOVE_FACING_SQUEEZE
    move_facing_steal_attempt = preflop.MOVE_FACING_STEAL_ATTEMPT

    def __attrs_post_init__(self):
        self.reset()
        self.actions_sequence = ActionsSequence([])

    def fold_action_update(self, action):
        self.flag_fold = True
        if action.player.is_facing_steal:
            self.flag_fold_to_steal_attempt = True

    def call_action_update(self, action):
        self.flag_vpip = True
        self.flag_open = True
        self.count_player_calls += 1
        if action.player.is_defending_blinds:
            self.flag_blind_defense = True
        if action.player.can_first_raise:
            self.flag_limp = True
            action.table.cnt_limps += 1
        else:
            self.flag_cold_called = True
            action.table.cnt_cold_calls += 1

    def raise_action_update(self, action):
        self.flag_vpip = True
        self.flag_raise = True
        if self.count_player_raises == 0:
            self.amount_first_raise_made = action.value
            self.ratio_first_raise_made = action.value / action.table.pot_value
        if self.count_player_raises == 1:
            self.amount_second_raise_made = action.value
            self.ratio_second_raise_made = action.value / action.table.pot_value
        if action.player.can_open:
            self.flag_open = True
        if action.player.can_open and action.value >= action.player.effective_stack:
            self.flag_open_shove = True
        if action.player.can_first_raise:
            self.flag_first_raise = True
        if action.player.can_squeeze:
            self.flag_squeeze = True
        if action.player.can_steal:
            self.flag_steal_attempt = True
        if action.player.is_defending_blinds:
            self.flag_blind_defense = True
        if action.player.can_3bet:
            self.flag_3bet = True
        if action.player.can_4bet:
            self.flag_4bet = True
        self.count_player_raises += 1

    def update_hand_stats(self, action):
        self.flag_voluntary_all_in = action.value >= action.player.effective_stack
        self.actions_sequence = action.player.actions_history.preflop
        self.total_bet_amount = sum([action.value for action in self.actions_sequence.actions])
        if not action.table.is_opened:
            self.flag_open_opportunity = True
            self.count_faced_limps = action.table.cnt_limps
        if self.amount_effective_stack == 0:
            self.amount_effective_stack = action.player.effective_stack
        if action.player.can_raise:
            self.flag_raise_opportunity = True
        if action.player.is_facing_raise:
            self.flag_face_raise = True
        if action.player.can_squeeze:
            self.flag_squeeze_opportunity = True
        if action.player.is_facing_squeeze:
            self.flag_face_squeeze = True
            self.move_facing_squeeze = action.move
        if action.player.can_steal:
            self.flag_steal_opportunity = True
        if action.player.is_facing_steal:
            self.flag_face_steal_attempt = True
            self.move_facing_steal_attempt = action.move
        if action.player.is_defending_blinds:
            self.flag_blind_defense_opportunity = True
        if action.player.is_facing_1bet:
            self.amount_to_call_facing_bet = action.player.to_call
            self.ratio_to_call_facing_bet = action.player.to_call / action.table.pot_value
        if action.player.is_facing_2bet:
            self.move_facing_2bet = action.move
            self.amount_to_call_facing_2bet = action.player.to_call
            self.ratio_to_call_facing_2bet = action.player.to_call / action.table.pot_value
        if action.player.is_facing_3bet:
            self.flag_face_3bet = True
            self.move_facing_3bet = action.move
            self.amount_to_call_facing_3bet = action.player.to_call
            self.ratio_to_call_facing_3bet = action.player.to_call / action.table.pot_value
        if action.player.is_facing_4bet:
            self.flag_face_4bet = True
            self.move_facing_4bet = action.move
            self.amount_to_call_facing_4bet = action.player.to_call
            self.ratio_to_call_facing_4bet = action.player.to_call / action.table.pot_value
        if action.player.can_3bet:
            self.flag_3bet_opportunity = True
        if action.player.can_4bet:
            self.flag_4bet_opportunity = True
        match action.move:
            case ActionMove.FOLD:
                self.fold_action_update(action)
            case ActionMove.CALL:
                self.call_action_update(action)
            case ActionMove.RAISE:
                self.raise_action_update(action)

    def reset(self):
        """
        Resets the statistics
        """
        for attribute in self.__attrs_attrs__:
            # noinspection PyTypeChecker
            if isinstance(attribute.default, Factory):
                # noinspection PyUnresolvedReferences
                setattr(self, attribute.name, attribute.default.factory())
            else:
                setattr(self, attribute.name, attribute.default)
