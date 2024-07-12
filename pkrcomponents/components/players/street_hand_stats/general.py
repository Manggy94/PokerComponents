from attrs import define, Factory
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

    def reset(self):
        """
        Resets the statistics
        """
        for attribute in self.__attrs_attrs__:
            if not isinstance(attribute.default, Factory):
                setattr(self, attribute.name, attribute.default)
            else:
                setattr(self, attribute.name, attribute.default.factory())