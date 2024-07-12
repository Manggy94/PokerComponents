from attrs import define, Factory

from pkrcomponents.components.actions.action_move import ActionMove
from pkrcomponents.components.actions.actions_sequence import ActionsSequence
from pkrcomponents.components.players.datafields import postflop


@define
class PostflopPlayerHandStats:
    flag_saw = postflop.FLAG_SAW
    flag_first_to_talk = postflop.FLAG_FIRST_TO_TALK
    flag_has_position = postflop.FLAG_HAS_POSITION
    flag_bet = postflop.FLAG_BET
    flag_open_opportunity = postflop.FLAG_OPEN_OPPORTUNITY
    flag_open = postflop.FLAG_OPEN
    flag_cbet_opportunity = postflop.FLAG_CBET_OPPORTUNITY
    flag_cbet = postflop.FLAG_CBET
    flag_face_cbet = postflop.FLAG_FACE_CBET
    flag_donk_bet_opportunity = postflop.FLAG_DONK_BET_OPPORTUNITY
    flag_donk_bet = postflop.FLAG_DONK_BET
    flag_face_donk_bet = postflop.FLAG_FACE_DONK_BET
    flag_first_raise = postflop.FLAG_FIRST_RAISE
    flag_fold = postflop.FLAG_FOLD
    flag_check = postflop.FLAG_CHECK
    flag_check_raise = postflop.FLAG_CHECK_RAISE
    flag_face_raise = postflop.FLAG_FACE_RAISE
    flag_3bet_opportunity = postflop.FLAG_3BET_OPPORTUNITY
    flag_3bet = postflop.FLAG_3BET
    flag_face_3bet = postflop.FLAG_FACE_3BET
    flag_4bet_opportunity = postflop.FLAG_4BET_OPPORTUNITY
    flag_4bet = postflop.FLAG_4BET
    flag_face_4bet = postflop.FLAG_FACE_4BET
    # 2. Counts
    count_player_raises = postflop.COUNT_PLAYER_RAISES
    count_player_calls = postflop.COUNT_PLAYER_CALLS
    # 3. Sequences
    actions_sequence = postflop.ACTIONS_SEQUENCE
    # 4. Amounts
    amount_effective_stack = postflop.AMOUNT_EFFECTIVE_STACK
    amount_to_call_facing_bet = postflop.AMOUNT_TO_CALL_FACING_BET
    amount_to_call_facing_2bet = postflop.AMOUNT_TO_CALL_FACING_2BET
    amount_to_call_facing_3bet = postflop.AMOUNT_TO_CALL_FACING_3BET
    amount_to_call_facing_4bet = postflop.AMOUNT_TO_CALL_FACING_4BET
    amount_bet_made = postflop.AMOUNT_BET_MADE
    amount_first_raise_made = postflop.AMOUNT_FIRST_RAISE_MADE
    amount_second_raise_made = postflop.AMOUNT_SECOND_RAISE_MADE
    ratio_to_call_facing_bet = postflop.RATIO_TO_CALL_FACING_BET
    ratio_to_call_facing_2bet = postflop.RATIO_TO_CALL_FACING_2BET
    ratio_to_call_facing_3bet = postflop.RATIO_TO_CALL_FACING_3BET
    ratio_to_call_facing_4bet = postflop.RATIO_TO_CALL_FACING_4BET
    ratio_bet_made = postflop.RATIO_BET_MADE
    ratio_first_raise_made = postflop.RATIO_FIRST_RAISE_MADE
    ratio_second_raise_made = postflop.RATIO_SECOND_RAISE_MADE
    total_bet_amount = postflop.TOTAL_BET_AMOUNT
    # 5. Moves
    move_facing_bet = postflop.MOVE_FACING_BET
    move_facing_2bet = postflop.MOVE_FACING_2BET
    move_facing_3bet = postflop.MOVE_FACING_3BET
    move_facing_4bet = postflop.MOVE_FACING_4BET
    move_facing_cbet = postflop.MOVE_FACING_CBET
    move_facing_donk_bet = postflop.MOVE_FACING_DONK_BET

    def __attrs_post_init__(self):
        self.reset()
        self.actions_sequence = ActionsSequence()

    def fold_action_update(self):
        self.flag_fold = True

    def check_action_update(self):
        self.flag_check = True

    def call_action_update(self):
        self.count_player_calls += 1

    def bet_action_update(self, action):
        self.amount_bet_made = action.value
        self.ratio_bet_made = action.value / action.table.pot_value
        self.flag_bet = True
        if action.player.can_open:
            self.flag_open = True
        if action.player.can_cbet:
            self.flag_cbet = True
        if action.player.can_donk_bet:
            self.flag_donk_bet = True

    def raise_action_update(self, action):
        self.flag_bet = True
        if self.count_player_raises == 0:
            self.amount_first_raise_made = action.value
            self.ratio_first_raise_made = action.value / action.table.pot_value
        if self.count_player_raises == 1:
            self.amount_second_raise_made = action.value
            self.ratio_second_raise_made = action.value / action.table.pot_value
        if action.player.can_first_raise:
            self.flag_first_raise = True
        if action.player.can_3bet:
            self.flag_3bet = True
        if action.player.can_4bet:
            self.flag_4bet = True
        if self.actions_sequence.symbol == "XR":
            self.flag_check_raise = True
        self.count_player_raises += 1

    def update_hand_stats(self, action):
        self.flag_saw = True
        if self.amount_effective_stack == 0:
            self.amount_effective_stack = action.player.effective_stack
        self.flag_first_to_talk = action.player.flag_street_first_to_talk
        if action.player.is_facing_cbet:
            self.flag_face_cbet = True
            self.move_facing_cbet = action.move
        if action.player.is_facing_donk_bet:
            self.flag_face_donk_bet = True
            self.move_facing_donk_bet = action.move
        if action.player.is_facing_raise:
            self.flag_face_raise = True
        if action.player.is_facing_1bet:
            self.amount_to_call_facing_bet = action.player.to_call
            self.ratio_to_call_facing_bet = action.player.to_call / action.table.pot_value
            self.move_facing_bet = action.move
        if action.player.is_facing_2bet:
            self.amount_to_call_facing_2bet = action.player.to_call
            self.ratio_to_call_facing_2bet = action.player.to_call / action.table.pot_value
            self.move_facing_2bet = action.move
        if action.player.is_facing_3bet:
            self.amount_to_call_facing_3bet = action.player.to_call
            self.ratio_to_call_facing_3bet = action.player.to_call / action.table.pot_value
            self.flag_face_3bet = True
            self.move_facing_3bet = action.move
        if action.player.is_facing_4bet:
            self.amount_to_call_facing_4bet = action.player.to_call
            self.ratio_to_call_facing_4bet = action.player.to_call / action.table.pot_value
            self.flag_face_4bet = True
            self.move_facing_4bet = action.move
        if action.player.can_open:
            self.flag_open_opportunity = True
        if action.player.can_cbet:
            self.flag_cbet_opportunity = True
        if action.player.can_donk_bet:
            self.flag_donk_bet_opportunity = True
        if action.player.can_3bet:
            self.flag_3bet_opportunity = True
        if action.player.can_4bet:
            self.flag_4bet_opportunity = True
        self.total_bet_amount = sum(
            [action.value for action in self.actions_sequence.actions])
        match action.move:
            case ActionMove.FOLD:
                self.fold_action_update()
            case ActionMove.CHECK:
                self.check_action_update()
            case ActionMove.CALL:
                self.call_action_update()
            case ActionMove.BET:
                self.bet_action_update(action)
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
