from pkrcomponents.utils.common import PokerEnum, _ReprMixin
from itertools import combinations


class Position(_ReprMixin, PokerEnum):
    """Class describing the table position"""
    UTG = "UTG", 1, 3, "under the gun"
    UTG1 = "UTG1", 2, 4, "utg+1", "utg + 1"
    UTG2 = "UTG2", 3, 5, "utg+2", "utg + 2"
    UTG3 = "UTG3", 4, 6, "utg+3", "utg + 3"
    LJ = "LJ", 5, 7, "UTG4", "lojack", "lowjack", "utg+4", "utg + 4"
    HJ = "HJ", 6, 8, "hijack", "highjack", "utg+5", "utg + 5"
    CO = "CO", 7, 9, "cutoff", "cut off", "cut-off"
    BTN = "BTN", 8, 10, "bu", "button"
    SB = "SB", 9, 1, "small blind"
    BB = "BB", 10, 2, "big blind"

    @property
    def name(self):
        return self._name_

    @property
    def short_name(self):
        return self.name

    @property
    def symbol(self):
        return self.name

    @property
    def is_early(self):
        return self.name in ["UTG", "UTG1", "UTG2", "UTG3"]

    @property
    def is_middle(self):
        return self.name in ["LJ", "HJ"]

    @property
    def is_late(self):
        return self.name in ["CO", "BTN"]

    @property
    def is_blind(self):
        return self.name in ["SB", "BB"]

    @property
    def preflop_order(self):
        return self._value_[1]

    @property
    def postflop_order(self):
        return self._value_[2]

    @classmethod
    def get_mapper(cls):
        return {
            1: [Position.BB],
            2: [Position.SB, Position.BB],
            3: [Position.BTN, Position.SB, Position.BB],
            4: [Position.CO, Position.BTN, Position.SB, Position.BB],
            5: [Position.HJ, Position.CO, Position.BTN, Position.SB, Position.BB],
            6: [Position.UTG, Position.HJ, Position.CO, Position.BTN, Position.SB, Position.BB],
            7: [Position.UTG, Position.LJ, Position.HJ, Position.CO, Position.BTN, Position.SB, Position.BB],
            8: [Position.UTG, Position.UTG1, Position.LJ, Position.HJ, Position.CO, Position.BTN, Position.SB,
                Position.BB],
            9: [Position.UTG, Position.UTG1, Position.UTG2, Position.LJ, Position.HJ, Position.CO, Position.BTN,
                Position.SB, Position.BB],
            10: [Position.UTG, Position.UTG1, Position.UTG2, Position.UTG3, Position.LJ, Position.HJ, Position.CO,
                 Position.BTN,
                 Position.SB, Position.BB]
        }

    @classmethod
    def get_maps(cls):
        positions = list(cls)
        mapper = cls.get_mapper()
        positions_lookups = []
        for nb_total_positions in range(2, 10):
            available_positions = mapper[nb_total_positions + 1]
            ref_positions = positions[-3:]
            for nb_ref_positions_occupied in range(2, min(nb_total_positions + 1, 4)):
                nb_left_positions_to_pick = nb_total_positions - nb_ref_positions_occupied
                for ref_positions_picked in (combinations(ref_positions, nb_ref_positions_occupied)):
                    left_positions = available_positions[:nb_left_positions_to_pick]
                    final_positions_picked = left_positions + list(ref_positions_picked)
                    positions_lookups.append(final_positions_picked)
        positions_lookups.append(mapper[10])
        return positions_lookups
