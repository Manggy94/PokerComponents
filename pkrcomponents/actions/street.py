from pkrcomponents.utils.common import PokerEnum


class Street(PokerEnum):
    """Class describing the street"""
    PREFLOP = "PF", "PreFlop", "Pf", "pf", "PREFLOP", "Preflop", "preflop", "Préflop", "préflop",
    FLOP = "F", "Flop", "f", "FLOP", "flop"
    TURN = "T", "Turn", "t", "TURN", "turn"
    RIVER = "R", "River", "r", "RIVER", "river"
    SHOWDOWN = "SD", "ShowDown", 'Sd', "sd", "SHOWDOWN", "Showdown", "showdown"

    @property
    def symbol(self):
        return self._value_[0]

    @property
    def name(self):
        return self._name_

    @property
    def parsing_name(self):
        return self._value_[1]

    @property
    def short_name(self):
        return self._value_[0]

    @property
    def is_preflop(self):
        return self.name == "PREFLOP"
