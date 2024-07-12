from attrs import define, Factory
import csv
from pkrcomponents.components.players.datafields import preflop, flop, turn, river, general


@define
class HandStats:
    """
    This class represents the statistics of a player's hand in a poker game

    Methods:
        reset: Resets all stats
    """
    # A. Preflop stats
    # 1. Flags
    flag_vpip = preflop.FLAG_VPIP
    flag_preflop_open_opportunity = preflop.FLAG_PREFLOP_OPEN_OPPORTUNITY
    flag_preflop_open = preflop.FLAG_PREFLOP_OPEN
    flag_preflop_first_raise = preflop.FLAG_PREFLOP_FIRST_RAISE
    flag_preflop_fold = preflop.FLAG_PREFLOP_FOLD
    flag_preflop_limp = preflop.FLAG_PREFLOP_LIMP
    flag_preflop_cold_called = preflop.FLAG_PREFLOP_COLD_CALLED
    flag_preflop_raise_opportunity = preflop.FLAG_PREFLOP_RAISE_OPPORTUNITY
    flag_preflop_raise = preflop.FLAG_PREFLOP_RAISE
    flag_preflop_face_raise = preflop.FLAG_PREFLOP_FACE_RAISE
    flag_preflop_3bet_opportunity = preflop.FLAG_PREFLOP_3BET_OPPORTUNITY
    flag_preflop_3bet = preflop.FLAG_PREFLOP_3BET
    flag_preflop_face_3bet = preflop.FLAG_PREFLOP_FACE_3BET
    flag_preflop_4bet_opportunity = preflop.FLAG_PREFLOP_4BET_OPPORTUNITY
    flag_preflop_4bet = preflop.FLAG_PREFLOP_4BET
    flag_preflop_face_4bet = preflop.FLAG_PREFLOP_FACE_4BET
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
    flag_voluntary_all_in_preflop = preflop.FLAG_VOLUNTARY_ALL_IN_PREFLOP
    # 2. Counts
    count_preflop_player_raises = preflop.COUNT_PREFLOP_PLAYER_RAISES
    count_preflop_player_calls = preflop.COUNT_PREFLOP_PLAYER_CALLS
    count_faced_limps = preflop.COUNT_FACED_LIMPS
    # 3. Sequences
    preflop_actions_sequence = preflop.PREFLOP_ACTIONS_SEQUENCE
    # 4. Amounts
    amount_preflop_effective_stack = preflop.AMOUNT_PREFLOP_EFFECTIVE_STACK
    amount_to_call_facing_preflop_bb = preflop.AMOUNT_TO_CALL_FACING_PREFLOP_BB
    amount_to_call_facing_preflop_2bet = preflop.AMOUNT_TO_CALL_FACING_PREFLOP_2BET
    amount_to_call_facing_preflop_3bet = preflop.AMOUNT_TO_CALL_FACING_PREFLOP_3BET
    amount_to_call_facing_preflop_4bet = preflop.AMOUNT_TO_CALL_FACING_PREFLOP_4BET
    amount_first_raise_made_preflop = preflop.AMOUNT_FIRST_RAISE_MADE_PREFLOP
    amount_second_raise_made_preflop = preflop.AMOUNT_SECOND_RAISE_MADE_PREFLOP
    ratio_to_call_facing_preflop_bb = preflop.RATIO_TO_CALL_FACING_PREFLOP_BB
    ratio_to_call_facing_preflop_2bet = preflop.RATIO_TO_CALL_FACING_PREFLOP_2BET
    ratio_to_call_facing_preflop_3bet = preflop.RATIO_TO_CALL_FACING_PREFLOP_3BET
    ratio_to_call_facing_preflop_4bet = preflop.RATIO_TO_CALL_FACING_PREFLOP_4BET
    ratio_first_raise_made_preflop = preflop.RATIO_FIRST_RAISE_MADE_PREFLOP
    ratio_second_raise_made_preflop = preflop.RATIO_SECOND_RAISE_MADE_PREFLOP
    total_preflop_bet_amount = preflop.TOTAL_PREFLOP_BET_AMOUNT
    # 5. Moves
    move_facing_preflop_2bet = preflop.MOVE_FACING_PREFLOP_2BET
    move_facing_preflop_3bet = preflop.MOVE_FACING_PREFLOP_3BET
    move_facing_preflop_4bet = preflop.MOVE_FACING_PREFLOP_4BET
    move_facing_squeeze = preflop.MOVE_FACING_SQUEEZE
    move_facing_steal_attempt = preflop.MOVE_FACING_STEAL_ATTEMPT
    # B. Flop stats
    # 1. Flags
    flag_saw_flop = flop.FLAG_SAW_FLOP
    flag_flop_first_to_talk = flop.FLAG_FLOP_FIRST_TO_TALK
    flag_flop_has_position = flop.FLAG_FLOP_HAS_POSITION
    flag_flop_bet = flop.FLAG_FLOP_BET
    flag_flop_open_opportunity = flop.FLAG_FLOP_OPEN_OPPORTUNITY
    flag_flop_open = flop.FLAG_FLOP_OPEN
    flag_flop_cbet_opportunity = flop.FLAG_FLOP_CBET_OPPORTUNITY
    flag_flop_cbet = flop.FLAG_FLOP_CBET
    flag_flop_face_cbet = flop.FLAG_FLOP_FACE_CBET
    flag_flop_donk_bet_opportunity = flop.FLAG_FLOP_DONK_BET_OPPORTUNITY
    flag_flop_donk_bet = flop.FLAG_FLOP_DONK_BET
    flag_flop_face_donk_bet = flop.FLAG_FLOP_FACE_DONK_BET
    flag_flop_first_raise = flop.FLAG_FLOP_FIRST_RAISE
    flag_flop_fold = flop.FLAG_FLOP_FOLD
    flag_flop_check = flop.FLAG_FLOP_CHECK
    flag_flop_check_raise = flop.FLAG_FLOP_CHECK_RAISE
    flag_flop_face_raise = flop.FLAG_FLOP_FACE_RAISE
    flag_flop_3bet_opportunity = flop.FLAG_FLOP_3BET_OPPORTUNITY
    flag_flop_3bet = flop.FLAG_FLOP_3BET
    flag_flop_face_3bet = flop.FLAG_FLOP_FACE_3BET
    flag_flop_4bet_opportunity = flop.FLAG_FLOP_4BET_OPPORTUNITY
    flag_flop_4bet = flop.FLAG_FLOP_4BET
    flag_flop_face_4bet = flop.FLAG_FLOP_FACE_4BET
    # 2. Counts
    count_flop_player_raises = flop.COUNT_FLOP_PLAYER_RAISES
    count_flop_player_calls = flop.COUNT_FLOP_PLAYER_CALLS
    # 3. Sequences
    flop_actions_sequence = flop.FLOP_ACTIONS_SEQUENCE
    # 4. Amounts
    amount_flop_effective_stack = flop.AMOUNT_FLOP_EFFECTIVE_STACK
    amount_to_call_facing_flop_bet = flop.AMOUNT_TO_CALL_FACING_FLOP_BET
    amount_to_call_facing_flop_2bet = flop.AMOUNT_TO_CALL_FACING_FLOP_2BET
    amount_to_call_facing_flop_3bet = flop.AMOUNT_TO_CALL_FACING_FLOP_3BET
    amount_to_call_facing_flop_4bet = flop.AMOUNT_TO_CALL_FACING_FLOP_4BET
    amount_bet_made_flop = flop.AMOUNT_BET_MADE_FLOP
    amount_first_raise_made_flop = flop.AMOUNT_FIRST_RAISE_MADE_FLOP
    amount_second_raise_made_flop = flop.AMOUNT_SECOND_RAISE_MADE_FLOP
    ratio_to_call_facing_flop_bet = flop.RATIO_TO_CALL_FACING_FLOP_BET
    ratio_to_call_facing_flop_2bet = flop.RATIO_TO_CALL_FACING_FLOP_2BET
    ratio_to_call_facing_flop_3bet = flop.RATIO_TO_CALL_FACING_FLOP_3BET
    ratio_to_call_facing_flop_4bet = flop.RATIO_TO_CALL_FACING_FLOP_4BET
    ratio_bet_made_flop = flop.RATIO_BET_MADE_FLOP
    ratio_first_raise_made_flop = flop.RATIO_FIRST_RAISE_MADE_FLOP
    ratio_second_raise_made_flop = flop.RATIO_SECOND_RAISE_MADE_FLOP
    total_flop_bet_amount = flop.TOTAL_FLOP_BET_AMOUNT
    # 5. Moves
    move_facing_flop_bet = flop.MOVE_FACING_FLOP_BET
    move_facing_flop_2bet = flop.MOVE_FACING_FLOP_2BET
    move_facing_flop_3bet = flop.MOVE_FACING_FLOP_3BET
    move_facing_flop_4bet = flop.MOVE_FACING_FLOP_4BET
    move_facing_flop_cbet = flop.MOVE_FACING_FLOP_CBET
    move_facing_flop_donk_bet = flop.MOVE_FACING_FLOP_DONK_BET
    # C. Turn stats
    # 1. Flags
    flag_saw_turn = turn.FLAG_SAW_TURN
    flag_turn_first_to_talk = turn.FLAG_TURN_FIRST_TO_TALK
    flag_turn_has_position = turn.FLAG_TURN_HAS_POSITION
    flag_turn_bet = turn.FLAG_TURN_BET
    flag_turn_open_opportunity = turn.FLAG_TURN_OPEN_OPPORTUNITY
    flag_turn_open = turn.FLAG_TURN_OPEN
    flag_turn_cbet_opportunity = turn.FLAG_TURN_CBET_OPPORTUNITY
    flag_turn_cbet = turn.FLAG_TURN_CBET
    flag_turn_face_cbet = turn.FLAG_TURN_FACE_CBET
    flag_turn_donk_bet_opportunity = turn.FLAG_TURN_DONK_BET_OPPORTUNITY
    flag_turn_donk_bet = turn.FLAG_TURN_DONK_BET
    flag_turn_face_donk_bet = turn.FLAG_TURN_FACE_DONK_BET
    flag_turn_first_raise = turn.FLAG_TURN_FIRST_RAISE
    flag_turn_fold = turn.FLAG_TURN_FOLD
    flag_turn_check = turn.FLAG_TURN_CHECK
    flag_turn_check_raise = turn.FLAG_TURN_CHECK_RAISE
    flag_turn_face_raise = turn.FLAG_TURN_FACE_RAISE
    flag_turn_3bet_opportunity = turn.FLAG_TURN_3BET_OPPORTUNITY
    flag_turn_3bet = turn.FLAG_TURN_3BET
    flag_turn_face_3bet = turn.FLAG_TURN_FACE_3BET
    flag_turn_4bet_opportunity = turn.FLAG_TURN_4BET_OPPORTUNITY
    flag_turn_4bet = turn.FLAG_TURN_4BET
    flag_turn_face_4bet = turn.FLAG_TURN_FACE_4BET
    # 2. Counts
    count_turn_player_raises = turn.COUNT_TURN_PLAYER_RAISES
    count_turn_player_calls = turn.COUNT_TURN_PLAYER_CALLS
    # 3. Sequences
    turn_actions_sequence = turn.TURN_ACTIONS_SEQUENCE
    # 4. Amounts
    amount_turn_effective_stack = turn.AMOUNT_TURN_EFFECTIVE_STACK
    amount_to_call_facing_turn_bet = turn.AMOUNT_TO_CALL_FACING_TURN_BET
    amount_to_call_facing_turn_2bet = turn.AMOUNT_TO_CALL_FACING_TURN_2BET
    amount_to_call_facing_turn_3bet = turn.AMOUNT_TO_CALL_FACING_TURN_3BET
    amount_to_call_facing_turn_4bet = turn.AMOUNT_TO_CALL_FACING_TURN_4BET
    amount_bet_made_turn = turn.AMOUNT_BET_MADE_TURN
    amount_first_raise_made_turn = turn.AMOUNT_FIRST_RAISE_MADE_TURN
    amount_second_raise_made_turn = turn.AMOUNT_SECOND_RAISE_MADE_TURN
    ratio_to_call_facing_turn_bet = turn.RATIO_TO_CALL_FACING_TURN_BET
    ratio_to_call_facing_turn_2bet = turn.RATIO_TO_CALL_FACING_TURN_2BET
    ratio_to_call_facing_turn_3bet = turn.RATIO_TO_CALL_FACING_TURN_3BET
    ratio_to_call_facing_turn_4bet = turn.RATIO_TO_CALL_FACING_TURN_4BET
    ratio_bet_made_turn = turn.RATIO_BET_MADE_TURN
    ratio_first_raise_made_turn = turn.RATIO_FIRST_RAISE_MADE_TURN
    ratio_second_raise_made_turn = turn.RATIO_SECOND_RAISE_MADE_TURN
    total_turn_bet_amount = turn.TOTAL_TURN_BET_AMOUNT
    # 5. Moves
    move_facing_turn_bet = turn.MOVE_FACING_TURN_BET
    move_facing_turn_2bet = turn.MOVE_FACING_TURN_2BET
    move_facing_turn_3bet = turn.MOVE_FACING_TURN_3BET
    move_facing_turn_4bet = turn.MOVE_FACING_TURN_4BET
    move_facing_turn_cbet = turn.MOVE_FACING_TURN_CBET
    move_facing_turn_donk_bet = turn.MOVE_FACING_TURN_DONK_BET
    # D. River stats
    # 1. Flags
    flag_saw_river = river.FLAG_SAW_RIVER
    flag_river_first_to_talk = river.FLAG_RIVER_FIRST_TO_TALK
    flag_river_has_position = river.FLAG_RIVER_HAS_POSITION
    flag_river_bet = river.FLAG_RIVER_BET
    flag_river_open_opportunity = river.FLAG_RIVER_OPEN_OPPORTUNITY
    flag_river_open = river.FLAG_RIVER_OPEN
    flag_river_cbet_opportunity = river.FLAG_RIVER_CBET_OPPORTUNITY
    flag_river_cbet = river.FLAG_RIVER_CBET
    flag_river_face_cbet = river.FLAG_RIVER_FACE_CBET
    flag_river_donk_bet_opportunity = river.FLAG_RIVER_DONK_BET_OPPORTUNITY
    flag_river_donk_bet = river.FLAG_RIVER_DONK_BET
    flag_river_face_donk_bet = river.FLAG_RIVER_FACE_DONK_BET
    flag_river_first_raise = river.FLAG_RIVER_FIRST_RAISE
    flag_river_fold = river.FLAG_RIVER_FOLD
    flag_river_check = river.FLAG_RIVER_CHECK
    flag_river_check_raise = river.FLAG_RIVER_CHECK_RAISE
    flag_river_face_raise = river.FLAG_RIVER_FACE_RAISE
    flag_river_3bet_opportunity = river.FLAG_RIVER_3BET_OPPORTUNITY
    flag_river_3bet = river.FLAG_RIVER_3BET
    flag_river_face_3bet = river.FLAG_RIVER_FACE_3BET
    flag_river_4bet_opportunity = river.FLAG_RIVER_4BET_OPPORTUNITY
    flag_river_4bet = river.FLAG_RIVER_4BET
    flag_river_face_4bet = river.FLAG_RIVER_FACE_4BET
    # 2. Counts
    count_river_player_raises = river.COUNT_RIVER_PLAYER_RAISES
    count_river_player_calls = river.COUNT_RIVER_PLAYER_CALLS
    # 3. Sequences
    river_actions_sequence = river.RIVER_ACTIONS_SEQUENCE
    # 4. Amounts
    amount_river_effective_stack = river.AMOUNT_RIVER_EFFECTIVE_STACK
    amount_to_call_facing_river_bet = river.AMOUNT_TO_CALL_FACING_RIVER_BET
    amount_to_call_facing_river_2bet = river.AMOUNT_TO_CALL_FACING_RIVER_2BET
    amount_to_call_facing_river_3bet = river.AMOUNT_TO_CALL_FACING_RIVER_3BET
    amount_to_call_facing_river_4bet = river.AMOUNT_TO_CALL_FACING_RIVER_4BET
    amount_bet_made_river = river.AMOUNT_BET_MADE_RIVER
    amount_first_raise_made_river = river.AMOUNT_FIRST_RAISE_MADE_RIVER
    amount_second_raise_made_river = river.AMOUNT_SECOND_RAISE_MADE_RIVER
    ratio_to_call_facing_river_bet = river.RATIO_TO_CALL_FACING_RIVER_BET
    ratio_to_call_facing_river_2bet = river.RATIO_TO_CALL_FACING_RIVER_2BET
    ratio_to_call_facing_river_3bet = river.RATIO_TO_CALL_FACING_RIVER_3BET
    ratio_to_call_facing_river_4bet = river.RATIO_TO_CALL_FACING_RIVER_4BET
    ratio_bet_made_river = river.RATIO_BET_MADE_RIVER
    ratio_first_raise_made_river = river.RATIO_FIRST_RAISE_MADE_RIVER
    ratio_second_raise_made_river = river.RATIO_SECOND_RAISE_MADE_RIVER
    total_river_bet_amount = river.TOTAL_RIVER_BET_AMOUNT
    # 5. Moves
    move_facing_river_bet = river.MOVE_FACING_RIVER_BET
    move_facing_river_2bet = river.MOVE_FACING_RIVER_2BET
    move_facing_river_3bet = river.MOVE_FACING_RIVER_3BET
    move_facing_river_4bet = river.MOVE_FACING_RIVER_4BET
    move_facing_river_cbet = river.MOVE_FACING_RIVER_CBET
    move_facing_river_donk_bet = river.MOVE_FACING_RIVER_DONK_BET
    # E. General stats
    combo = general.COMBO
    starting_stack = general.STARTING_STACK
    amount_won = general.AMOUNT_WON
    amount_expected_won = general.AMOUNT_EXPECTED_WON
    flag_went_to_showdown = general.FLAG_WENT_TO_SHOWDOWN
    flag_is_hero = general.FLAG_IS_HERO
    flag_won_hand = general.FLAG_WON_HAND
    total_bet_amount = general.TOTAL_BET_AMOUNT
    fold_street = general.FOLD_STREET
    all_in_street = general.ALL_IN_STREET
    face_covering_bet_street = general.FACE_COVERING_BET_STREET
    face_all_in_street = general.FACE_ALL_IN_STREET
    facing_covering_bet_move = general.FACING_COVERING_BET_MOVE
    facing_all_in_move = general.FACING_ALL_IN_MOVE

    def reset(self):
        """
        Resets the statistics
        """
        for attribute in self.__attrs_attrs__:
            if not isinstance(attribute.default, Factory):
                setattr(self, attribute.name, attribute.default)
            else:
                setattr(self, attribute.name, attribute.default.factory())

#     @classmethod
#     def generate_description_file(cls):
#         """
#         Generate a csv file to describe data from class
#         """
#         with open('hand_stats_description.csv', 'w', newline='') as csvfile:
#             fieldnames = ['name', 'default', 'description', 'type']
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#             writer.writeheader()
#             for attribute in cls.__attrs_attrs__:
#                 row = {
#                     'name': attribute.name,
#                     'default': attribute.default if not isinstance(attribute.default, Factory)
#                     else attribute.default.factory(),
#                     'description': attribute.metadata.get('description', 'No description'),
#                     'type': attribute.metadata.get('type', 'No type')
#                 }
#                 writer.writerow(row)
#         print("CSV file 'class_description.csv' generated successfully.")
#
#
# if __name__ == '__main__':
#     HandStats.generate_description_file()
