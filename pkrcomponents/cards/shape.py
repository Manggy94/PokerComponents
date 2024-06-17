from pkrcomponents.utils.common import PokerEnum


class Shape(PokerEnum):
    """
    Shape of a Hand
    """
    OFFSUIT = "o", "offsuit", "off"
    SUITED = "s", "suited"
    PAIR = "", "paired"

    @property
    def name(self):
        return self._name_

    @property
    def symbol(self):
        return self._value_[0]

    @property
    def adjective(self):
        return self._value_[1]
