from attrs import define, Factory

from pkrcomponents.components.actions.action_move import ActionMove
from pkrcomponents.components.players.datafields import general


@define
class GeneralPlayerHandStats:

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

    def update_hand_stats(self, action):
        """
        Updates the hand statistics of the player according to the action
        """
        stats = action.player.hand_stats
        if action.is_all_in:
            self.all_in_street = action.table.street
        if action.player.is_facing_covering_bet:
            self.face_covering_bet_street = action.table.street
            self.facing_covering_bet_move = action.move
        if action.player.is_facing_all_in:
            self.face_all_in_street = action.table.street
            self.facing_all_in_move = action.move
        if action.move == ActionMove.FOLD:
            self.fold_street = action.table.street
        self.total_bet_amount = sum((stats.preflop.total_bet_amount, stats.flop.total_bet_amount,
                                     stats.turn.total_bet_amount, stats.river.total_bet_amount))

    def reset(self):
        """
        Resets the statistics
        """
        for attribute in self.__attrs_attrs__:
            if not isinstance(attribute.default, Factory):
                setattr(self, attribute.name, attribute.default)
            else:
                setattr(self, attribute.name, attribute.default.factory())