from pkrcomponents.components.utils.common import PokerEnum


class Street(PokerEnum):
    """
    Class describing the street

    """
    PREFLOP = "PF", "PreFlop", "Pf", "pf", "PREFLOP", "Preflop", "preflop", "Préflop", "préflop",
    FLOP = "F", "Flop", "f", "FLOP", "flop"
    TURN = "T", "Turn", "t", "TURN", "turn"
    RIVER = "R", "River", "r", "RIVER", "river"
    SHOWDOWN = "SD", "ShowDown", 'Sd', "sd", "SHOWDOWN", "Showdown", "showdown"

    @property
    def symbol(self) -> str:
        """
        Returns the symbol of the street
        """
        return self._value_[0]

    @property
    def name(self) -> str:
        """
        Returns the name of the street
        """
        return self._name_

    @property
    def parsing_name(self) -> str:
        """
        Returns the name of the street in a format that can be used for parsing
        """
        return self._value_[1]

    @property
    def short_name(self) -> str:
        """
        Returns the short name of the street
        """
        return self._value_[0]

    @property
    def is_preflop(self) -> bool:
        """
        Returns True if the street is the preflop
        """
        return self.name == "PREFLOP"
